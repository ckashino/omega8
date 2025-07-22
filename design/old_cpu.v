module cpu (
  input i_clk, i_instr_ready, i_mem_ready, i_hold, i_rst,
  input [7:0] i_opcode,
  input [7:0] i_arg1, i_arg2, 
  input [2:0] i_address,
  output o_wait,
  output reg o_instr_read,
  output [7:0] o_data
  );

  reg [7:0] opcode;
  reg [7:0] arg1;
  reg [7:0] arg2;

  reg state;
  reg nextstate;
  reg zero_flag;
  reg negative_flag;
  reg overflow_flag;

  reg alu_carry_borrow = 0;
  reg [2:0] alu_op = 0;
  reg [7:0] alu_result;
  reg [7:0] alu_a;
  reg [7:0] alu_b;

  wire alu_carry_out;

  reg [2:0] reg_address_1, reg_address_2;
  reg [7:0] reg_write_data_1, reg_write_data_2;
  reg reg_read, reg_write;
  reg [1:0] reg_file_mask;
  reg reg_file_done;
  reg [7:0] reg_read_data_1, reg_read_data_2;

  // multi-cycle single stage

  alu alu_inst (.i_clk (i_clk),
                .i_carry_borrow (alu_carry_borrow),
                .i_op (alu_op),
                .i_a (alu_a),
                .i_b (alu_b),
                .o_carry_borrow (alu_carry_out),
                .o_overflow (overflow_flag),
                .o_neg (negative_flag),
                .o_zero (zero_flag),
                .o_result (alu_result));

  reg_file reg_file_inst (.i_address1 (reg_address_1),
                          .i_address2 (reg_address_2),
                          .i_data1 (reg_write_data_1),
                          .i_data2 (reg_write_data_2),
                          .i_read (reg_read),
                          .i_write (reg_write),
                          .i_clk (i_clk),
                          .i_reg_mask (reg_file_mask),
                          .o_done (reg_file_done),
                          .o_data1 (reg_read_data_1),
                          .o_data2 (reg_read_data_2));

  localparam fetch = 3'd0;
  localparam decode = 3'd1;
  localparam execute = 3'd2;
  localparam memread = 3'd3;
  localparam writeback = 3'd4;
 
  always @(posedge i_clk or posedge i_rst) begin 
    if (i_rst)
      state <= fetch;
    else
      state <= nextstate; 
  end 

  always @(*) begin
    case (state)
      
      fetch : begin
        o_instr_read <= 1'b0;
        if (i_hold)
          nextstate <= fetch;
        else if (i_instr_ready) begin
          opcode <= i_opcode;
          arg1 <= i_arg1;
          arg2 <= i_arg2;
          nextstate <= decode;
          o_instr_read <= 1'b1;
        end
      end

      decode : begin
        o_instr_read <= 1'b0;

        reg_read <= 1'b0;
        reg_write <= 1'b0;
        nextstate <= decode;

        case (opcode)
          // needing dual reg reads
          8'h07, 8'h08, 8'h09, 8'h0A, 8'h0B: begin
            reg_read <= 1'b1;
            reg_address_1 <= arg1;
            reg_address_2 <= arg2;
            reg_file_mask <= 2'b11;

            if (reg_file_done) begin
              alu_a <= reg_read_data_1;
              alu_b <= reg_read_data_2;
              nextstate <= execute;
              reg_read <= 1'b0;
            end else begin
              nextstate <= decode;
            end
          end
          default:
            nextstate <= fetch;
        endcase


      end

      execute : begin
        case (opcode)

          8'h07, 8'h08, 8'h09, 8'h0A, 8'h0B: begin
            
          end

          default:
            nextstate <= fetch;
        
      end

      memread : begin 
      end

      writeback : begin
      end

      default : begin
      end

    endcase
  end

endmodule
