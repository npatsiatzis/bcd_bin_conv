# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
EXTRA_ARGS += --std=08
SIM_ARGS += --wave=wave.ghw

VHDL_SOURCES += $(PWD)/../rtl/dd_bcd2bin.vhd
# use VHDL_SOURCES for VHDL files


bcd_2_bin:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_bcd_2_bin TOPLEVEL=dd_bcd2bin
# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim