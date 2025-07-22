import cocotb
from cocotb.triggers import Timer

clock_timer = Timer(5, units="ps")

@cocotb.test()
async def test_read(dut):
    dut.i_address1.value = 0
    dut.i_address2.value = 1

    dut.i_reg_mask.value = 0b11
    dut.i_clk.value = 0
    dut.i_read.value = 1
    dut.i_write.value = 0

    dut.registers.value = [0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    await clock_timer 

    dut.i_clk.value = 1

    await clock_timer
    
    assert dut.o_done == 1

    dut.i_clk.value = 0

    assert dut.o_data1.value == 1
    assert dut.o_data2.value == 2


@cocotb.test()
async def test_write(dut):
    dut.i_address1.value = 0
    dut.i_address2.value = 1


    dut.i_reg_mask.value = 0b11
    dut.i_clk.value = 0
    dut.i_read.value = 0
    dut.i_write.value = 1
    dut.i_data1.value = 8
    dut.i_data2.value = 16

    await clock_timer

    dut.i_clk.value = 1 

    await clock_timer

    assert dut.o_done == 1
    
    dut.i_clk.value = 0

    assert dut.registers.value[0] == 8
    assert dut.registers.value[1] == 16
    

@cocotb.test()
async def test_write_read(dut):
    dut.i_address1.value = 0
    dut.i_address2.value = 1

    dut.i_reg_mask.value = 0b11
    dut.i_data1.value = 4
    dut.i_data2.value = 8
    dut.i_clk.value = 0
    dut.i_read.value = 0
    dut.i_write.value = 1

    await clock_timer

    dut.i_clk.value = 1

    await clock_timer

    assert dut.o_done == 1

    dut.i_clk.value = 0
    dut.i_write.value = 0
    dut.i_read.value = 1

    await clock_timer

    dut.i_clk.value = 1

    await clock_timer

    assert dut.o_data1.value == 4
    assert dut.o_data2.value == 8
    assert dut.registers.value[0] == 4
    assert dut.registers.value[1] == 8
