import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer,RisingEdge,FallingEdge,ClockCycles,ReadOnly
from cocotb.result import TestFailure
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db
from cocotb.binary import BinaryValue
import numpy as np

g_bcd_width = int(cocotb.top.g_bcd_width)
covered_value = []
full = False

def max_bcd_number():
	max_bcd = ""
	for i in range(int(g_bcd_width/4)):
		max_bcd = max_bcd+"9"
	return(int(max_bcd))
max_bcd=max_bcd_number()

def bcd_to_4bits(bcd_digit):
	a = format(bcd_digit,'b')
	if(len(a) < 4):
		diff = 4 -len(a)
		for i in range(diff):
			a = '0' + a
	return a


def digits_of_integer(p_int):
	digits = []

	p_str = str(p_int)
	for i in range(len(p_str)):
		digits.append(int(p_str[i]))
	return digits

# #Callback functions to capture the bin content showing
def notify_full():
	global full
	full = True



# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.bcd",xf = lambda x : x, bins = list(range(0,max_bcd)), at_least=1)
def number_cover(x):
	covered_value.append(x)

async def init(dut,time_units=1):

	dut.i_bcd.value = 0 

	await Timer(time_units,units = 'ns')
	dut._log.info("the core was initialized")

@cocotb.test()
async def test(dut):

	await init(dut,5)	
	while (full != True):
		bcd = random.randint(0,max_bcd)
		while(bcd in covered_value):
			bcd = random.randint(0,max_bcd)
		number_cover(bcd)
		coverage_db["top.bcd"].add_threshold_callback(notify_full, 100)
		bcd_digits = digits_of_integer(bcd)

		

		bin_strings = []
		zero_string = '0000'
		if(len(bcd_digits) < (g_bcd_width/4)):
			diff = int(g_bcd_width/4) - len(bcd_digits) 
			for i in range(diff):
				bin_strings.insert(0,zero_string)
		for i in bcd_digits:
			bin_strings.append(bcd_to_4bits(i))

		i_bcd = ""
		for i in bin_strings:
			i_bcd = i_bcd + i
		dut.i_bcd.value = BinaryValue(i_bcd)
		await Timer(2,units = 'ns')

		assert not (bcd != dut.o_bin.value),"Actual behavior different than the expected one"

	coverage_db.report_coverage(cocotb.log.info,bins=True)
	coverage_db.export_to_xml(filename="coverage_bcd_bin.xml") 


