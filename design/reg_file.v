// dual read, single write reg file. single clock operations
module reg_file (
  input [2:0] i_r_address1, i_r_address2, i_w_address,
  input [7:0] i_data,
  input i_read, i_write,
  input i_clk, i_rst,
  output reg [7:0] o_data1, o_data2
  );

  reg [7:0] registers [0:7];

  integer i;
  initial begin
    for (i=0;i<8;i=i+1) begin
      registers[i] = 0;
    end
  end

  always @(posedge i_clk or posedge i_rst) begin
    if (i_rst) begin
      i = 0;
      for (i=0;i<8;i=i+1) begin
        registers[i] = 0;
      end
    end
    if (i_read) begin
        o_data1 <= registers[i_r_address1];
        o_data2 <= registers[i_r_address2];
    end
    if (i_write) begin
      registers[i_w_address] <= i_data;
    end
  end

endmodule
