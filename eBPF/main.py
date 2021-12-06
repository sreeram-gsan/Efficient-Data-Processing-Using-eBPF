#!/usr/bin/env python3

from bcc import BPF
import time
import ctypes
import sys
import os


os.system("ulimit -l 10240")
os.system("sudo mount -t debugfs debugfs /sys/kernel/debug")

ethernet_interface = "lo"
sys.stdout = open("log.txt", 'w')

bpf_obj = BPF(src_file="stringContainsFilter.c")
bpf_func = bpf_obj.load_func("udpstringContainsFilter", BPF.XDP)
bpf_obj.attach_xdp(ethernet_interface, bpf_func, 0)

data_store = []

try:
  bpf_obj.trace_print()
except KeyboardInterrupt:
  pass
  counter_map = bpf_obj.get_table("counter")
  records_map = bpf_obj.get_table("filteredData")

  row_count = counter_map[0].value

  print(row_count)

  for i in range(row_count):
    ##print(bytes(records_map[i].record).decode('ascii'))
    a = bytes(records_map[i].record).split(b'\n')[0].decode("ascii")
    data_store.append(a)
  
  file1 = open('result.txt', 'w')
  file1.writelines('\n'.join(str(j) for j in data_store))
  file1.close()

  bpf_obj.remove_xdp(ethernet_interface, 0)
  sys.stdout.close()