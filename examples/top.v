module top (
  input i_clk, i_rst,
  // debug port that outputs the most recent memory written
  output o_mem_view
);

  wire [29:0] instr_data;
  wire instr_read_done;
  wire [15:0] instr_addr;
  wire instr_read;

  wire [15:0] ram_addr;
  wire [7:0] ram_data_read;
  wire [7:0] ram_data_write;
  wire ram_read, ram_write;
  wire ram_done;

  core u_core (
    .i_clk(i_clk),
    .i_rst(i_rst),
    .i_instr_data(instr_data),
    .i_instr_read_done(instr_read_done),
    .o_instr_addr(instr_addr),
    .o_instr_read(instr_read),

    .o_ram_addr(ram_addr),
    .i_ram_data_in(ram_data_read),
    .o_ram_data_out(ram_data_write),
    .o_ram_read(ram_read),
    .o_ram_write(ram_write),
    .i_ram_done(ram_done)
  );

  ram #(
    .ADDR_WIDTH(4), 
    .DATA_WIDTH(8)
  ) u_ram (
    .i_clk(i_clk),
    .i_read(ram_read),
    .i_write(ram_write),
    .i_address(ram_addr[3:0]),
    .i_data(ram_data_write),
    .o_done(ram_done),
    .o_data(ram_data_read)
  );

  instr_mem u_instr_mem (
    .i_instr_addr(instr_addr),
    .i_instr_read(instr_read),
    .o_instr(instr_data),
    .o_instr_read_done(instr_read_done)
  );

endmodule
