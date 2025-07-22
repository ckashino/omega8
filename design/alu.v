module alu (
  input i_clk, i_carry_borrow,
  input [7:0] i_a, i_b,
  input [2:0] i_op,
  output reg o_carry_borrow, o_overflow, o_neg, o_zero,
  output reg [7:0] o_result
);
  wire [7:0] and_result, or_result, xor_result;
  wire [8:0] add_sub_result;
  wire carry_borrow_mod;
  wire [7:0] b_mod;
  wire sub_op = (i_op == 3'b001);

  assign b_mod = sub_op ? ~i_b : i_b;
  assign carry_borrow_mod = sub_op ? ~i_carry_borrow : i_carry_borrow;

  assign add_sub_result = i_a + b_mod + carry_borrow_mod;

  assign and_result = i_a & i_b;
  assign or_result = i_a | i_b;
  assign xor_result = i_a ^ i_b;

  wire overflow_flag;
  assign overflow_flag = sub_op ? ((i_a[7] != i_b[7]) && (add_sub_result[7] != i_a[7]))  // Subtraction rule
                                : ((i_a[7] == i_b[7]) && (add_sub_result[7] != i_a[7])); // Addition rule

  wire negative_flag = add_sub_result[7];
  wire zero_flag = ~|add_sub_result[7:0];

  always @(posedge i_clk) begin
    o_carry_borrow = 0;
    o_neg = 0;
    o_zero = 0;
    o_overflow = 0;
    case (i_op)
      3'b000 : begin
        o_result = add_sub_result[7:0];
        o_carry_borrow = add_sub_result[8];
        o_overflow = overflow_flag;
        o_neg = negative_flag;
        o_zero = zero_flag;
      end
      3'b001 : begin
        o_result = add_sub_result[7:0];
        o_carry_borrow = ~add_sub_result[8];
        o_overflow = overflow_flag;
        o_neg = negative_flag;
        o_zero = zero_flag;
      end
      3'b010 : begin
        o_result = and_result;
        o_neg = or_result[7];
        o_zero = ~|and_result;
      end
      3'b011 : begin
        o_result = or_result;
        o_neg = or_result[7];
        o_zero = ~|or_result;
      end
      3'b100 : begin
        o_result = xor_result;
        o_neg = xor_result[7];
        o_zero = ~|xor_result;
      end
    endcase
  end

endmodule
