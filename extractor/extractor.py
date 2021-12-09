from flask import Flask, request, Response
import logging
import socket
import os
import requests
import time
import util.publish_logs as pl
'''
extractor.py

Extract the text from an input file
convers the text to UDP packets and stream them

end point - /api/v1/extract
input: {'filter':'filter_value', 'source_file':'source_file_value'}
output: 200 OK: 
'''

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

MAX_ROWS_TO_PROCESS = 900
EBPF_HOST = os.getenv("EBPF_HOST") or "172.17.0.2"
EBPF_PORT = 7888
EBPF_REST_PORT = "5000"

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    #processing request
    r = request
    body = request.get_json(force=True)
    filter, source = body['filter'],body['source']
    pl.log_debug(f"recieved the data: {filter} : {source}")
    #reading data from file
    with open(source) as f:
        contents = f.readlines()
        f.close()

    eBPF_container_base_url = 'http://'+ EBPF_HOST +':'+ EBPF_REST_PORT

    #call eBPF start API
    eBPF_container_start_api_url = eBPF_container_base_url +'/start/'+filter
    
    try:
        response = requests.get(eBPF_container_start_api_url)
        if(response.status_code != 200):
            return "Failed to end EBPF task"
    except:
        return "Failed to end EBPF task"

    time.sleep(3)

    #streaming UDP packets
    opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for row,row_data in enumerate(contents):
        if (row<MAX_ROWS_TO_PROCESS):
            opened_socket.sendto(bytes(row_data, encoding='utf8'), (EBPF_HOST, EBPF_PORT))
    
    time.sleep(2)

    # call eBPF stop API
    eBPF_container_end_api_url = eBPF_container_base_url + '/end'
    try:
        response = requests.get(eBPF_container_end_api_url)
        if(response.status_code != 200):
            return "Failed to end EBPF task"
    except:
        return "Failed to end EBPF task"

    return Response(response={"status":"success"}, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="localhost", port=5024)

