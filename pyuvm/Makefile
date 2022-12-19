# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
EXTRA_ARGS += --std=08
SIM_ARGS += --wave=wave.ghw

VHDL_SOURCES += $(PWD)/dd_bcd2bin.vhd
VHDL_SOURCES += $(PWD)/dd_bin2bcd.vhd
# use VHDL_SOURCES for VHDL files


bcd_2_bin:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_bcd_2_bin TOPLEVEL=dd_bcd2bin

bin_2_bcd:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_bin_2_bcd TOPLEVEL=dd_bin2bcd

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim