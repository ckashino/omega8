// dual read reg file
module reg_file (
  input [2:0] i_address1, i_address2,
  input [7:0] i_data,
  input i_read, i_write, i_clk,
  output o_done,
  output [7:0] o_data1, o_data2
  );

  reg [7:0] registers [0:7];
  reg [15:0] register_sp;
  reg [15:0] register_pc;
  reg [15:0] register_ra;

  always @(posedge clk) begin
    o_done <= 0;


    if (i_read) begin
      if (i_address1 != 0)
        o_data1 <= registers[i_address1];
      else
        o_data1 <= 8'd0;
      if (i_address2 != 0)
        o_data1 <= registers[i_address2];
      else
        o_data2 <= 8'd0;

      o_done <= 1;

    end else if (i_write) begin
      if (i_address1 != 0)
        registers[i_address1] <= i_data;
      o_done <= 1;
    end
  end
