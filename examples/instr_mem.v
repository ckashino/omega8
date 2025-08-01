module instr_mem (
  input [15:0] i_instr_addr,
  input i_instr_read,
  output [29:0] o_instr,
  output o_instr_read_done
);

  reg [29:0] instr = 30'h3FFFFFFF; // nop

  // simple program to compute fibonacci(7)
  // then push it to the stack
  always_comb begin
      case (i_instr_addr)
        16'd0: instr = 30'b000000000000000000000000000110;
        16'd1: instr = 30'b000000000000000010000000000000;
        16'd2: instr = 30'b000000000000000100000000000001;
        16'd3: instr = 30'b000000000000000110000000000000;
        16'd4: instr = 30'b001100000010100110000000000000;
        16'd5: instr = 30'b001000000100000010000000000000;
        16'd6: instr = 30'b001000000110000100000000000000;
        16'd7: instr = 30'b010000000000000000000011111111;
        16'd8: instr = 30'b010100100000000000000000000100;
        16'd9: instr = 30'b100000000110000000000000000000;
        16'd10: instr = 30'b111111110000000000000000000000;
        16'd11: instr = 30'b100000011000000000000000000000;
        default: instr = 30'h3FFFFFFF;
      endcase
  end


  assign o_instr_read_done = 1;
  assign o_instr = instr;
endmodule
