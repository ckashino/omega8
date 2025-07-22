module core #(
  parameter RAM_ADDR_SIZE = 4'hF
)(
  input               i_clk,
  input               i_rst,

  input       [29:0]  i_instr_data,
  output reg  [15:0]  o_instr_addr,
  output reg          o_instr_read,

  output reg  [15:0]  o_ram_addr,
  input       [7:0]   i_ram_data_in,
  output reg  [7:0]   o_ram_data_out,
  output reg          o_ram_read,
  output reg          o_ram_write,
  input               i_ram_done,

  output reg          o_cpu_done
);

  reg [15:0] pc;
  reg [15:0] ra;
  reg [15:0] sp = RAM_ADDR_SIZE;
  reg [29:0] curr_instr;
  reg [1:0]  flags_reg; // {Negative, Zero}

  localparam S_FETCH      = 3'b000;
  localparam S_DECODE     = 3'b001;
  localparam S_EXECUTE    = 3'b010;
  localparam S_MEM_ACCESS = 3'b011;
  localparam S_MEM_WAIT   = 3'b100;
  localparam S_WB         = 3'b101;

  reg [2:0] curr_state, next_state;

  wire [7:0] opcode = curr_instr[29:22];
  wire [3:0] instr_class = opcode[7:4];
  wire [2:0] r1_addr = curr_instr[21:19];
  wire [2:0] r2_addr = curr_instr[18:16];
  wire [2:0] r3_addr = curr_instr[15:13];
  wire [7:0] imm8 = curr_instr[7:0];
  wire [15:0] imm16 = curr_instr[15:0];

  reg reg_read_en, reg_write_en;
  wire [7:0] reg_file_out1, reg_file_out2;
  reg [7:0] reg_write_data;

  reg_file u_reg_file (
    .i_clk(i_clk), .i_rst(i_rst),
    .i_r_address1(r1_addr), .i_r_address2(r2_addr),
    .i_w_address(r3_addr),
    .i_data(reg_write_data),
    .i_read(reg_read_en), .i_write(reg_write_en),
    .o_data1(reg_file_out1), .o_data2(reg_file_out2)
  );

  wire [7:0] alu_result;
  reg [2:0] alu_op;
  wire [7:0] alu_a_operand = reg_file_out1;
  reg alu_b_select = 1'b0;
  wire [7:0] alu_b_operand = (alu_b_select == 1'b0) ? reg_file_out2 : imm8;

  wire alu_carry_out;
  reg alu_carry_select = 1'b1;
  reg alu_carry_in = 1'b0;
  wire alu_carry_in_comb = (alu_carry_select == 1'b0) ? 1'b0 : alu_carry_in;
  wire alu_overflow_out, alu_neg_out, alu_zero_out;

  alu u_alu(
    .i_clk(i_clk),
    .i_carry_borrow(alu_carry_in_comb),
    .i_a(alu_a_operand), .i_b(alu_b_operand),
    .i_op(alu_op),
    .o_carry_borrow(alu_carry_out), .o_overflow(alu_overflow_out),
    .o_neg(alu_neg_out), .o_zero(alu_zero_out),
    .o_result(alu_result)
  );


  always @(posedge i_clk or posedge i_rst) begin
    if (i_rst) begin
      curr_state <= S_FETCH;
      flags_reg  <= 2'b0;
      pc         <= 16'h0000;
      ra         <= 16'h0000;
      sp         <= 16'hFFFF; 
    end else begin
      curr_state <= next_state;

      if (next_state == S_DECODE && curr_state == S_FETCH) begin
        curr_instr <= i_instr_data;
        pc <= pc + 1; 
      end

      if (curr_state == S_DECODE) begin
        case (opcode)
          8'h50: pc <= imm16; // JMP
          8'h51: if (flags_reg[0]) pc <= imm16; // JZ
          8'h52: if (!flags_reg[0]) pc <= imm16; // JNZ
          8'h53: if (flags_reg[1]) pc <= imm16; // JN
          8'h54: if (!flags_reg[1]) pc <= imm16; // JNN
          8'h60: begin // CALL
            ra <= pc; 
            pc <= imm16;
          end
          8'h70: pc <= ra; // RET
        endcase
      end

      if (curr_state == S_MEM_WAIT && i_ram_done) begin
          if(opcode == 8'h80) sp <= sp - 1; // PUSH
          if(opcode == 8'h81) sp <= sp + 1; // POP
      end

      // Update flags register only on ALU operations
      if (curr_state == S_EXECUTE) begin
          flags_reg <= {alu_neg_out, alu_zero_out};
      end
    end
  end


  always_comb begin
    next_state       = curr_state;
    o_instr_read     = 1'b0;

    // mem signals stay stable while waiting
    if (curr_state != S_MEM_WAIT) begin
      o_ram_read       = 1'b0;
      o_ram_write      = 1'b0;
      o_ram_addr       = 16'h0000;
      o_ram_data_out   = 8'h00;
    end

    reg_write_en     = 1'b0;
    reg_read_en      = 1'b0;
    reg_write_data   = 8'h00;
    o_cpu_done       = 1'b0;

    case (curr_state)
      S_FETCH: begin
        o_instr_read = 1'b1;
        o_instr_addr = pc;
        next_state   = S_DECODE;
      end

      S_DECODE: begin
        reg_read_en = 1'b1; // Always read potential operands
        case (instr_class)
          4'h0: next_state = S_WB; // LDI
          4'h1: next_state = S_MEM_ACCESS; // LD, ST
          4'h2: next_state = S_WB; // MOV
          4'h3: begin // ALU Ops
            alu_b_select = 1'b0;
            alu_op = (opcode[3:0] == 4'h0 || opcode[3:0] == 4'h1) ? 3'b000 : // ADD, ADDC
                     (opcode[3:0] == 4'h2 || opcode[3:0] == 4'h3) ? 3'b001 : // SUB, SUBB
                     (opcode[3:0] == 4'h4) ? 3'b010 : // AND
                     (opcode[3:0] == 4'h5) ? 3'b011 : 3'b100; // OR, XOR
            next_state = S_EXECUTE;
            alu_carry_select = (opcode[3:0] == 4'h1 || opcode[3:0] == 4'h3) ? 1'b1 : 1'b1;
          end
          4'h4: begin // ADDI
            alu_b_select = 1'b1;
            alu_op = 3'b000;
            next_state = S_EXECUTE;
          end
          4'h5, 4'h6, 4'h7: begin
            next_state = S_FETCH;// Jumps, CALL, RET are handled in clocked block
            o_cpu_done = 1'b1;
          end
          4'h8: next_state = S_MEM_ACCESS; // PUSH, POP
          default: next_state = S_FETCH; // NOP, invalid
        endcase
        if (opcode == 8'hFF) o_cpu_done = 1'b1; // NOP
      end

      // Clock cycle for ALU ops
      S_EXECUTE: begin
        next_state = S_WB;
      end

      S_MEM_ACCESS: begin
        case(instr_class)
            4'h1: begin // LD, ST
                o_ram_addr = imm16;
                if(opcode == 8'h10) o_ram_read = 1'b1; //LD
                else begin //ST
                    o_ram_write = 1'b1;
                    o_ram_data_out = reg_file_out1;
                end
            end
            4'h8: begin // PUSH, POP
                o_ram_addr = sp;
                if(opcode == 8'h80) begin // PUSH
                    o_ram_write = 1'b1;
                    o_ram_data_out = reg_file_out1;
                end else begin // POP
                    o_ram_read = 1'b1;
                end
            end
        endcase
        next_state = S_MEM_WAIT;
      end

      S_MEM_WAIT: begin
        if (i_ram_done) begin
          // For LD and POP, we need to go to Write-Back.
          // For ST and PUSH, we are finished.
          if (opcode == 8'h10 || opcode == 8'h81) begin // LD, POP
            next_state = S_WB;
          end else begin // ST, PUSH
            o_cpu_done = 1'b1;
            next_state = S_FETCH;
          end
        end else begin
          next_state = S_MEM_WAIT; // Stay here
        end
      end

      S_WB: begin
        o_cpu_done   = 1'b1;
        next_state   = S_FETCH;
        case (instr_class)
          4'h0: reg_write_data = imm8; // LDI
          4'h1: reg_write_data = i_ram_data_in; // LD
          4'h2: reg_write_data = reg_file_out1; // MOV
          4'h3: begin
            reg_write_data = alu_result; // ALU ops
            alu_carry_in = alu_carry_out;
          end
          4'h4: reg_write_data = alu_result; // ADDI
          4'h8: reg_write_data = i_ram_data_in; // POP
        endcase
        reg_write_en = 1'b1;
      end

      default: begin
        next_state = S_FETCH;
      end
    endcase
  end

endmodule
