// single port synchronous ram 


module ram #(
  parameter DATA_WIDTH = 8, 
  parameter ADDR_WIDTH = 4)
(
	input i_clk, i_read, i_write,
  input [ADDR_WIDTH - 1:0] i_address, 
	input [DATA_WIDTH-1:0] i_data,
  output reg o_done,
	output reg [DATA_WIDTH-1:0] o_data
);

  reg [DATA_WIDTH - 1:0] mem [2**ADDR_WIDTH];

  always @(posedge i_clk) begin
    o_done <= 0;

    if (i_write) begin
      mem[i_address] <= i_data;
      o_done <= 1;
    end
    if (i_read) begin
      o_data <= i_data;
      o_done <= 1;
    end
  end

endmodule
