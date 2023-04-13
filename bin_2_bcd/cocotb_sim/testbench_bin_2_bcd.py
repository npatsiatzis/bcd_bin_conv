import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer,RisingEdge,FallingEdge,ClockCycles,ReadOnly
from cocotb.result import TestFailure
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db
from cocotb.binary import BinaryValue
import numpy as np

g_bin_width = int(cocotb.top.g_bin_width)
g_bcd_width = int(cocotb.top.g_bcd_width)
covered_value = []
full = False


def bcd_to_dec(bcd):
	dec = ""
	for i in range(int(g_bcd_width/4)):
		dec = dec +str(int(bcd[i*4:i*4+3]))
	return int(dec)

# #Callback functions to capture the bin content showing
def notify_full():
	global full
	full = True


# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.bin",xf = lambda x : x.i_bin.value, bins = list(range(2**g_bin_width)), at_least=1)
def number_cover(x):
	covered_value.append(x.i_bin.value)

async def init(dut,time_units=1):

	dut.i_bin.value = 0 

	await Timer(time_units,units = 'ns')
	dut._log.info("the core was initialized")

@cocotb.test()
async def test(dut):

	await init(dut,5)	
	while (full != True):
		bin_input = random.randint(0,2**g_bin_width-1)
		while(bin_input in covered_value):
			bin_input = random.randint(0,2**g_bin_width-1)


		dut.i_bin.value = bin_input
		await Timer(2,units = 'ns')
		number_cover(dut)
		coverage_db["top.bin"].add_threshold_callback(notify_full, 100)
		assert not (bin_input != bcd_to_dec(dut.o_bcd.value)),"Actual behavior different than the expected one"

	coverage_db.report_coverage(cocotb.log.info,bins=True)
	coverage_db.export_to_xml(filename="coverage_bin_bcd.xml") 


