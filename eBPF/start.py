#!/usr/bin/env python3
from bcc import BPF
import time
import ctypes
import _thread
import sys
import threading
import multiprocessing

class eBPF:
    ethernet_interface = None
    log_file = None
    data_store = []
    bpf_obj = None

    def __init__(self, interface, bpf_src, log_src):
        self.ethernet_interface = interface
        self.bpf_obj = BPF(src_file=bpf_src)
        self.log_file = log_src
        ##self.start_log()

    def start_log(self):
        sys.stdout = open(self.log_file, 'w')
    
    def collect_trace_print(self):
        print("Collecting Trace")
        try:
            self.bpf_obj.trace_print()
        except KeyboardInterrupt:
            print("Exited Trace Collection")
            pass
    
    def collect_filtered_rows(self):
        counter_map = self.bpf_obj.get_table("counter")
        records_map = self.bpf_obj.get_table("filteredData")
        row_count = counter_map[0].value

        for i in range(row_count):
            a = bytes(records_map[i].record).split(b'\n')[0].decode("ascii")
            print(a)
            data_store.append(a)

    def attachBPF(self):
        bpf_func = self.bpf_obj.load_func("udpstringContainsFilter", BPF.XDP)
        self.bpf_obj.attach_xdp(self.ethernet_interface, bpf_func, 0)
        try:
            proc = multiprocessing.Process(target=self.collect_trace_print, args=())
            ##collectRows = multiprocessing.Process(target=self.collect_filtered_rows, args=())
            proc.start()
        except KeyboardInterrupt:
            self.collect_filtered_rows()
            proc.terminate()
            self.shutdown()
            pass
    
    def shutdown(self):
        sys.stdout.close()
        self.bpf_obj.remove_xdp(self.ethernet_interface, 0)

if __name__=='__main__':
    obj = eBPF("lo","stringContainsFilter.c","log.txt")
    obj.attachBPF()
    obj.shutdown()
    