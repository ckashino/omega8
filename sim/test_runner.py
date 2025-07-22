from pathlib import Path
from cocotb_test.simulator import run

def test_alu():
    sim_file = "unit.alu.verify"
    build_folder = Path(__file__).resolve().parent / "unit" / "alu" / "sim_build"
    design_folder = Path(__file__).resolve().parent.parent / "design"
    alu_source = [design_folder / "alu.v" ]

    run(
            verilog_sources=alu_source,
            sim_build=build_folder,
            toplevel="alu",
            module=sim_file,
            timescale="1ns/1ps",
            )

def test_reg_file():
    sim_file = "unit.reg_file.verify"
    build_folder = Path(__file__).resolve().parent / "unit" / "reg_file" / "sim_build"
    design_folder = Path(__file__).resolve().parent.parent / "design"
    reg_file_source = [design_folder / "reg_file.v" ]

    run(
            verilog_sources=reg_file_source,
            sim_build=build_folder,
            toplevel="reg_file",
            module=sim_file,
            timescale="1ns/1ps",
            )

def test_core():
    sim_file = "unit.core.verify"
    build_folder = Path(__file__).resolve().parent / "unit" / "core" / "sim_build"
    design_folder = Path(__file__).resolve().parent.parent / "design"
    reg_file_source = [design_folder / "core.v", design_folder / "reg_file.v", design_folder / "alu.v" ]

    run(
            verilog_sources=reg_file_source,
            sim_build=build_folder,
            toplevel="core",
            module=sim_file,
            timescale="1ns/1ps",
            )
