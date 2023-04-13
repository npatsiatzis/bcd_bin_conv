# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
EXTRA_ARGS += --std=08
SIM_ARGS += --wave=wave.ghw

VHDL_SOURCES += $(PWD)/../rtl/dd_bin2bcd.vhd
# use VHDL_SOURCES for VHDL files

bin_2_bcd:
		rm -rf sim_build
		$(MAKE) sim MODULE=tb_bin_2_bcd TOPLEVEL=dd_bin2bcd

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim