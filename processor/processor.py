import util.publish_logs as pl
from flask import Flask,request, Response
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import jsonpickle


'''
processor.py

Spawns a thread to listen to the queue - toProcessor; thread on queue_reader
Injects eBPF code snippets based on the filter
'''

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"


@app.route('/api/v1/start', methods=['POST'])
def start_ebpf():
    pl.log_debug(message="starting ebpf")
    print("starting ebpf")

@app.route('/api/v1/stop', methods=['POST'])
def stop_ebpf():
    pl.log_debug(message="stoppping and restarting ebpf")
    print("stopping and restarting ebpf")

if __name__ == "__main__":
    pl.log_debug("processor is starting ...")
    print("processor is starting ... ")
    app.run(host="0.0.0.0", port=5025)

    