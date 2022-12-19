
from cocotb.triggers import Timer
from cocotb.queue import QueueEmpty, Queue
import cocotb
import enum
import random
from cocotb_coverage import crv 
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db
from pyuvm import utility_classes



class BcdBinBfm(metaclass=utility_classes.Singleton):
    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.data_mon_queue = Queue(maxsize=0)
        self.result_mon_queue = Queue(maxsize=0)

    async def send_data(self, bcd):
        await self.driver_queue.put(bcd)

    async def get_data(self):
        data = await self.data_mon_queue.get()
        return data

    async def get_result(self):
        result = await self.result_mon_queue.get()
        return result

    async def reset(self):
        await Timer(2,units = 'ns')
        self.dut.i_bcd.value = 0
        await Timer(2,units = 'ns')


    async def driver_bfm(self):
        self.dut.i_bcd.value = 0
        while True:
            await Timer(2,units = 'ns')
            try:
                bcd = self.driver_queue.get_nowait()
                self.dut.i_bcd.value = bcd
            except QueueEmpty:
                pass

    async def data_mon_bfm(self):
        while True:
            await Timer(2,units = 'ns')
            bcd  = self.dut.i_bcd.value
            self.data_mon_queue.put_nowait(bcd)

    async def result_mon_bfm(self):
        while True:
            await Timer(2,units = 'ns')
            self.result_mon_queue.put_nowait(self.dut.o_bin.value)


    def start_bfm(self):
        cocotb.start_soon(self.driver_bfm())
        cocotb.start_soon(self.data_mon_bfm())
        cocotb.start_soon(self.result_mon_bfm())



class BinBcdBfm(metaclass=utility_classes.Singleton):
    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.data_mon_queue = Queue(maxsize=0)
        self.result_mon_queue = Queue(maxsize=0)

    async def send_data(self, bin):
        await self.driver_queue.put(bin)

    async def get_data(self):
        data = await self.data_mon_queue.get()
        return data

    async def get_result(self):
        result = await self.result_mon_queue.get()
        return result

    async def reset(self):
        await Timer(2,units = 'ns')
        self.dut.i_bin.value = 0
        await Timer(2,units = 'ns')


    async def driver_bfm(self):
        self.dut.i_bin.value = 0
        while True:
            await Timer(2,units = 'ns')
            try:
                bin = self.driver_queue.get_nowait()
                self.dut.i_bin.value = bin
            except QueueEmpty:
                pass

    async def data_mon_bfm(self):
        while True:
            await Timer(2,units = 'ns')
            bin  = self.dut.i_bin.value
            self.data_mon_queue.put_nowait(bin)

    async def result_mon_bfm(self):
        while True:
            await Timer(2,units = 'ns')
            self.result_mon_queue.put_nowait(self.dut.o_bcd.value)


    def start_bfm(self):
        cocotb.start_soon(self.driver_bfm())
        cocotb.start_soon(self.data_mon_bfm())
        cocotb.start_soon(self.result_mon_bfm())