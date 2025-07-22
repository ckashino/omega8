SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += ../../../design/core.v
VERILOG_SOURCES += ../../../design/alu.v
VERILOG_SOURCES += ../../../design/reg_file.v
TOPLEVEL = core
MODULE = verify
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
