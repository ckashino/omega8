import cocotb
from cocotb.triggers import Timer

clock_timer = Timer(5, units="ps")

@cocotb.test()
async def test_read(dut):
    dut.i_r_address1.value = 0
    dut.i_r_address2.value = 1

    dut.i_clk.value = 0
    dut.i_write.value = 0

    dut.registers.value = [0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    await clock_timer 

    dut.i_clk.value = 1

    await clock_timer

    dut.i_clk.value = 0

    assert dut.o_data1.value == 1
    assert dut.o_data2.value == 2


@cocotb.test()
async def test_write(dut):

    dut.i_clk.value = 0
    dut.i_write.value = 1
    dut.i_w_address.value = 0
    dut.i_data.value = 8

    await clock_timer

    dut.i_clk.value = 1 

    await clock_timer

    dut.i_clk.value = 0

    assert dut.registers.value[0] == 8
