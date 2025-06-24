module cpu (
  input i_clk, i_instr_ready, i_mem_ready, i_hold, i_rst,
  input [7:0] i_opcode,
  input [7:0] i_data1, i_data2, 
  input [2:0] i_address,
  output o_wait,
  output [7:0] o_data
  );

  reg [7:0] opcode;
  reg [7:0] data1;
  reg [7:0] data2;

  reg state;
  reg nextstate;
  
  wire register_read;
  wire register_write;

  // multi-cycle single stage

  localparam fetch = 3'd0;
  localparam decode = 3'd1;
  localparam execute = 3'd2;
  localparam memread = 3'd3;
  localparam writeback = 3'd4;
 
  always @(posedge clk or posedge i_rst) begin 
    if (rst)
      reg_state <= fetch;
    else
      reg_state <= reg_nextstate; 
  end 

  always @(*) begin
    case (state)
      
      fetch : begin
        if (i_hold)
          nextstate <= fetch;
        else if (i_instr_ready) begin
          opcode <= i_opcode;
          data1 <= i_data1;
          data2 <= i_data2;
          nextstate <= decode;
        end
      end

      decode : begin 
      end

      execute : begin 
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
