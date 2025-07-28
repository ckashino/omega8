import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_read(dut):
    dut.i_instr_addr.value = 0
    dut.i_instr_read.value = 1
    await Timer(5, units="ps")
    assert dut.o_instr.value == 0b000000000000000000000000000110
