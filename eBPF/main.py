#!/usr/bin/env python3

from bcc import BPF
import time
import ctypes
import sys
import os
import redis
from datetime import datetime
import time


os.system("ulimit -l 10240")
os.system("sudo mount -t debugfs debugfs /sys/kernel/debug")

##ethernet_interface = "lo"
ethernet_interface = "eth0"
sys.stdout = open("log.txt", 'w')

redisHost = "redis"
db = redis.Redis(host=redisHost, db=1)
db.ping()

bpf_obj = BPF(src_file="stringContainsFilter.c")
bpf_func = bpf_obj.load_func("udpstringContainsFilter", BPF.XDP)
bpf_obj.attach_xdp(ethernet_interface, bpf_func, 0)

data_store = {}

try:
  bpf_obj.trace_print()
except KeyboardInterrupt:
  pass
  counter_map = bpf_obj.get_table("counter")
  records_map = bpf_obj.get_table("filteredData")

  row_count = counter_map[0].value

  for i in range(row_count):
    ##print(bytes(records_map[i].record).decode('ascii'))
    a = bytes(records_map[i].record).split(b'\n')[0].decode("ascii")
    key = str(time.time())
    data_store[key] = a
  
  bpf_obj.remove_xdp(ethernet_interface, 0)
  sys.stdout.close()
  db.mset(data_store)