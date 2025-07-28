import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_program_run(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")
    dut.i_rst.value = 0

    while True:
        await RisingEdge(dut.i_clk)
        if dut.instr_addr.value == 0xC:
            break

