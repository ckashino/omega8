import cocotb
from cocotb.triggers import Timer

clock_timer = Timer(5, units="ps")

@cocotb.test()
async def test_write_read(dut):
    dut.i_read.value = 0
    dut.i_write.value = 1
    dut.i_clk.value = 0
    
    dut.i_data.value = 1
    dut.i_address.value = 0

    await clock_timer

    dut.i_clk.value = 1

    await clock_timer
    dut.i_clk.value = 0

    assert dut.mem.value[0] == 1
    assert dut.done.value == 1

    dut.i_write.value = 0

    await clock_timer

    dut.i_clk.value = 1
    await clock_timer

    assert dut.done.value == 0

    dut.i_clk.value = 0

    dut.i_read.value = 1

    await clock_timer
    
    dut.i_clk.value = 1
    
    await clock_timer

    assert dut.done.value == 1
    assert dut.o_data == 1
