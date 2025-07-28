import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

def reset_inputs(dut):
    dut.i_instr_read_done.value = 1
    dut.i_instr_data.value = 0
    dut.i_ram_data_in.value= 0
    dut.i_clk.value = 0
    dut.i_rst.value = 0
    dut.i_ram_done.value = 0

async def run_instr(dut, instr):
    dut.i_instr_data.value = instr

    cycles_waited = 0

    while dut.o_cpu_done.value != 1:
        await RisingEdge(dut.i_clk)
        cycles_waited += 1

        if cycles_waited >= 100:
            break


@cocotb.test()
async def test_ldi_add_basic(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")

    reset_inputs(dut)

    # small check for multicycle instruction read
    dut.i_instr_read_done.value = 0
    await RisingEdge(dut.i_clk)
    dut.i_instr_data.value = 0b00_00000000_000_000_000_00000_00000001
    await RisingEdge(dut.i_clk)
    dut.i_instr_read_done.value = 1

    cycles_waited = 0

    while dut.o_cpu_done != 1:
        await RisingEdge(dut.i_clk)
        cycles_waited += 1

        if cycles_waited >= 100:
            break

    await FallingEdge(dut.i_clk)

    await run_instr(dut, 0b00_00110000_000_000_000_00000_00000001)
    await RisingEdge(dut.o_instr_read)

    await run_instr(dut, 0b00_00110000_000_000_000_00000_00000001)
    assert dut.reg_write_data.value == 4
    await RisingEdge(dut.o_instr_read)

@cocotb.test()
async def test_addc(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")
    reset_inputs(dut)

    await run_instr(dut, 0b00_00000000_000_000_000_00000_11111110)
    await RisingEdge(dut.o_instr_read)

    await run_instr(dut, 0b00_00000000_000_000_001_00000_00000010)
    await RisingEdge(dut.o_instr_read)

    await run_instr(dut, 0b00_00110000_000_001_010_00000_00000000)
    assert dut.alu_carry_in.value == 0b1
    assert dut.reg_write_data.value == 0
    await RisingEdge(dut.o_instr_read)

    await run_instr(dut, 0b00_00110001_001_001_011_00000_00000000)
    assert dut.reg_write_data.value == (2 + 2 + 1) # reg1 (2) + reg1 (2) + carry (1)
    await RisingEdge(dut.o_instr_read)

@cocotb.test()
async def test_subb(dut):
    # performing the 2 step operation of 0x1001 - 0x0102
    # which should result in 0x0EFF


    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")
    reset_inputs(dut)

    # load 1 into r0
    await run_instr(dut, 0b00_00000000_000_000_000_00000_00000001)
    await RisingEdge(dut.o_instr_read)
    
    # load 16 into r1
    await run_instr(dut, 0b00_00000000_000_000_001_00000_00010000)
    await RisingEdge(dut.o_instr_read)

    # load 2 into r2
    await run_instr(dut, 0b00_00000000_000_000_010_00000_00000010)
    await RisingEdge(dut.o_instr_read)

    # load 1 into r3
    await run_instr(dut, 0b00_00000000_000_000_011_00000_00000001)
    await RisingEdge(dut.o_instr_read)


    # now doing [r1, r0] - [r3, r2] or 0x1001 - 0x0102 = 0xEFF or 4097 - 258 = 3839
    # done by doing r0 - r2, then r1 - r3 - borrow, writing result into [r1, r0]

    await run_instr(dut, 0b00_00110010_000_010_000_00000_00000000)
    assert dut.reg_write_data.value == 0xFF
    await RisingEdge(dut.o_instr_read)


    await run_instr(dut, 0b00_00110011_001_011_001_00000_00000000)
    assert dut.reg_write_data.value == 0x0E
    await RisingEdge(dut.o_instr_read)

@cocotb.test()
async def test_flags(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")
    reset_inputs(dut)

    await run_instr(dut, 0b00_00000000_000_000_000_00000_00000000)
    await RisingEdge(dut.o_instr_read)

    await run_instr(dut, 0b00_01000000_000_000_000_00000_00000000)
    await RisingEdge(dut.o_instr_read)

    assert dut.flags_reg.value == 0b01
    
    await run_instr(dut, 0b00_00000000_000_000_000_00000_00000000)
    await RisingEdge(dut.o_instr_read)

    await run_instr(dut, 0b00_01000000_000_000_000_00000_11111111)
    await RisingEdge(dut.o_instr_read)
    assert dut.flags_reg.value == 0b10


@cocotb.test()
async def test_pc_jumps(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")
    reset_inputs(dut)
    
    assert dut.pc.value == 0

    await run_instr(dut, 0b00_01010000_000_000_0000_0000_0000_0100)
    await RisingEdge(dut.o_instr_read)
    assert dut.pc.value == 4

    dut.flags_reg.value = 0b01

    await run_instr(dut, 0b00_01010001_000_000_0000_0000_0000_1000)
    await RisingEdge(dut.o_instr_read)
    assert dut.pc.value == 8

    dut.flags_reg.value = 0b01
    await run_instr(dut, 0b00_01010010_000_000_0000_0000_0001_0000)
    await RisingEdge(dut.o_instr_read)
    assert dut.pc.value == 9
    
    dut.flags_reg.value = 0b10
    await run_instr(dut, 0b00_01010011_000_000_0000_0000_0001_0000)
    await RisingEdge(dut.o_instr_read)
    assert dut.pc.value == 16
    
    dut.flags_reg.value = 0b10
    await run_instr(dut, 0b00_01010100_000_000_0000_0000_0001_0000)
    await RisingEdge(dut.o_instr_read)
    assert dut.pc.value == 17

@cocotb.test()
async def test_mem_load(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")
    reset_inputs(dut)

    dut.i_instr_data.value = 0b00_00010000_000_000_00000000_00001000

    await RisingEdge(dut.o_ram_read)
    assert dut.o_ram_addr.value == 8

    dut.i_ram_data_in.value = 32
    dut.i_ram_done.value = 1

    await RisingEdge(dut.reg_write_en)
    assert dut.reg_write_data == 32
    dut.i_ram_done.value = 0
    await RisingEdge(dut.o_instr_read)


@cocotb.test()
async def test_mem_store(dut):
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ps").start())
    dut.i_rst.value = 1
    await Timer(20, units="ps")
    reset_inputs(dut)
    
    await run_instr(dut, 0b00_00000000_000_000_000_00000_00000100)
    await RisingEdge(dut.o_instr_read)

    dut.i_instr_data.value = 0b00_00010001_000_000_00000000_00000000

    await RisingEdge(dut.o_ram_write)
    for _ in range(4):
        await RisingEdge(dut.i_clk)

    assert dut.o_ram_data_out.value == 4
    
    dut.i_ram_done.value = 1

    await RisingEdge(dut.o_instr_read)

    dut.i_ram_done.value = 0
