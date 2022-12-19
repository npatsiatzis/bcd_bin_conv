from cocotb.triggers import Timer
from pyuvm import *
import random
import cocotb
import pyuvm
from utils import BcdBinBfm
from cocotb.binary import BinaryValue



g_bcd_width = int(cocotb.top.g_bcd_width)
covered_values = []

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

def bcd_2_bin(p_bcd):
    digits = ""
    for i in range(int(g_bcd_width/4)):
        digits = digits + str(int(p_bcd[i*4:i*4+3]))
    return int(digits)

def bin_2_bcd(p_bin):
    bcd_digits = digits_of_integer(p_bin)
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
    return BinaryValue(i_bcd)


# Sequence classes
class SeqItem(uvm_sequence_item):

    def __init__(self, name, bcd):
        super().__init__(name)
        self.bcd = bcd


    def randomize_operands(self):
        self.bcd = random.randint(0,max_bcd)

    def randomize(self):
        self.randomize_operands()

    def __eq__(self, other):
        same = self.bcd == other.bcd
        return same


class RandomSeq(uvm_sequence):
    async def body(self):
        while(len(covered_values) != max_bcd):
            data_tr = SeqItem("data_tr", None)
            await self.start_item(data_tr)
            data_tr.randomize_operands()
            while(data_tr.bcd in covered_values):
                data_tr.randomize_operands()
            covered_values.append(data_tr.bcd)
            await self.finish_item(data_tr)


class TestAllSeq(uvm_sequence):

    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        random = RandomSeq("random")
        await random.start(seqr)

class Driver(uvm_driver):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    def start_of_simulation_phase(self):
        self.bfm = BcdBinBfm()

    async def launch_tb(self):
        await self.bfm.reset()
        self.bfm.start_bfm()

    async def run_phase(self):
        await self.launch_tb()
        while True:
            data = await self.seq_item_port.get_next_item()
            bcd_data = bin_2_bcd(data.bcd)
            await self.bfm.send_data(bcd_data)
            result = await self.bfm.get_result()
            self.ap.write(result)
            data.result = result
            self.seq_item_port.item_done()


class Coverage(uvm_subscriber):

    def end_of_elaboration_phase(self):
        self.cvg = set()

    def write(self, data):
        bcd = data
        int = bcd_2_bin(bcd)
        if(bcd_2_bin(bcd) not in self.cvg):
            self.cvg.add(int)

    def report_phase(self):
        try:
            disable_errors = ConfigDB().get(
                self, "", "DISABLE_COVERAGE_ERRORS")
        except UVMConfigItemNotFound:
            disable_errors = False
        if not disable_errors:
            if len(set(covered_values) - self.cvg) > 0:
                self.logger.error(
                    f"Functional coverage error. Missed: {set(covered_values)-self.cvg}")   
                assert False
            else:
                self.logger.info("Covered all input space")
                assert True


class Scoreboard(uvm_component):

    def build_phase(self):
        self.data_fifo = uvm_tlm_analysis_fifo("data_fifo", self)
        self.result_fifo = uvm_tlm_analysis_fifo("result_fifo", self)
        self.data_get_port = uvm_get_port("data_get_port", self)
        self.result_get_port = uvm_get_port("result_get_port", self)
        self.data_export = self.data_fifo.analysis_export
        self.result_export = self.result_fifo.analysis_export

    def connect_phase(self):
        self.data_get_port.connect(self.data_fifo.get_export)
        self.result_get_port.connect(self.result_fifo.get_export)

    def check_phase(self):
        passed = True
        try:
            self.errors = ConfigDB().get(self, "", "CREATE_ERRORS")
        except UVMConfigItemNotFound:
            self.errors = False
        while self.result_get_port.can_get():
            _, actual_result = self.result_get_port.try_get()
            data_success, data = self.data_get_port.try_get()
            if not data_success:
                self.logger.critical(f"result {actual_result} had no command")
            else:
                bcd = data
                if bcd_2_bin(bcd) == int(actual_result):
                    pass
                    self.logger.info("PASSED:")
                else:
                    self.logger.error("FAILED:")

                    passed = False
        assert passed


class Monitor(uvm_component):
    def __init__(self, name, parent, method_name):
        super().__init__(name, parent)
        self.method_name = method_name

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.bfm = BcdBinBfm()
        self.get_method = getattr(self.bfm, self.method_name)

    async def run_phase(self):
        while True:
            datum = await self.get_method()
            self.logger.debug(f"MONITORED {datum}")
            self.ap.write(datum)


class Env(uvm_env):

    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.driver = Driver.create("driver", self)
        self.data_mon = Monitor("data_mon", self, "get_data")
        self.coverage = Coverage("coverage", self)
        self.scoreboard = Scoreboard("scoreboard", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.data_mon.ap.connect(self.scoreboard.data_export)
        self.data_mon.ap.connect(self.coverage.analysis_export)
        self.driver.ap.connect(self.scoreboard.result_export)


@pyuvm.test()
class Test(uvm_test):
    """Test Bcd 2 Bin with random values"""

    def build_phase(self):
        self.env = Env("env", self)

    def end_of_elaboration_phase(self):
        self.test_all = TestAllSeq.create("test_all")

    async def run_phase(self):
        self.raise_objection()
        await self.test_all.start()
        await Timer(2,units = 'ns') # to do last transaction
        self.drop_objection()
