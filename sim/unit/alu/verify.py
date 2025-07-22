import cocotb
from cocotb.triggers import Timer

wait_timer = Timer(1, units="ps")

@cocotb.test()
async def test_add(dut):

    dut.i_op.value = 0b000
    dut.i_a.value = 4
    dut.i_b.value = 2
    dut.i_carry_borrow.value = 0

    await wait_timer

    assert dut.o_result.value == 6

@cocotb.test()
async def test_add_carry_out(dut):

    dut.i_op.value = 0b000
    dut.i_a.value = 255
    dut.i_b.value = 1
    dut.i_carry_borrow.value= 0


    await wait_timer
    
    assert dut.add_sub_result.value == 0x100
    assert dut.o_result.value == 0x00
    assert dut.o_carry_borrow.value == 0b1

@cocotb.test()
async def test_add_carry_in(dut):

    dut.i_op.value = 0b000
    dut.i_a.value = 1
    dut.i_b.value = 1
    dut.i_carry_borrow.value = 1

    await wait_timer

    assert dut.add_sub_result.value == 0x003
    assert dut.o_result.value == 0x03
    assert dut.o_carry_borrow.value == 0b0


@cocotb.test()
async def test_sub(dut):
    dut.i_op.value = 0b001
    dut.i_a.value = 4
    dut.i_b.value = 2
    dut.i_carry_borrow.value = 0

    await wait_timer
    
    assert dut.add_sub_result.value == 0x102
    assert dut.o_result.value == 0x02
    assert dut.o_carry_borrow.value == 0b0


@cocotb.test()
async def test_sub_neg_arg(dut):
    dut.i_op.value = 0b001
    dut.i_a.value = 4
    dut.i_b.value = -2
    dut.i_carry_borrow.value = 0


    await wait_timer
    
    assert dut.add_sub_result.value == 0x06
    assert dut.o_result.value == 0x06

    # in unsigned arithmetic, 4 < -2 
    assert dut.o_carry_borrow.value == 0b1

@cocotb.test()
async def test_sub_neg_result(dut):
    dut.i_op.value = 0b001
    dut.i_a.value = 4
    dut.i_b.value = 6
    dut.i_carry_borrow.value = 0

    await wait_timer

    assert dut.o_result.value == 0xFE
    assert dut.o_carry_borrow.value == 0b1
