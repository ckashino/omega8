from cocotb_test.simulator import run
from pathlib import Path

def test_instr_mem():
    design_folder = Path(__file__).resolve().parent.parent
    

    run(
            verilog_sources=[design_folder / "instr_mem.v"],
            sim_build="builds/instr_mem",
            toplevel="instr_mem",
            module="instr_mem_tests",
            timescale="1ns/1ps",
            waves=True
            )

def test_top():
    examples_design_folder = Path(__file__).resolve().parent.parent
    design_folder = Path(__file__).resolve().parent.parent.parent / "design"

    sources = [
            examples_design_folder / "instr_mem.v",
            examples_design_folder / "top.v",
            examples_design_folder / "ram.v",
            design_folder / "core.v",
            design_folder / "alu.v",
            design_folder / "reg_file.v"
            ]

    run(
            verilog_sources=sources,
            sim_build="builds/top",
            toplevel="top",
            module="top_tests",
            timescale="1ns/1ps",
            waves=True
            )
