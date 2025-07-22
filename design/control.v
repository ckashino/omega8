module control (
  input i_clk, i_rst,
  
  input [29:0] i_instr_data,
  output reg [15:0] o_instr_addr,
  output reg o_instr_read
);

  
  reg [15:0] sp;
  reg [15:0] pc;
  reg [15:0] ra;

endmodule
