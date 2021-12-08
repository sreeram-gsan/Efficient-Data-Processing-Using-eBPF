from flask import Flask, request, Response
import logging
import socket
import os

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
EBPF_HOST = os.getenv("EBPF_HOST") or "localhost"
EBPF_PORT = 7888

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    #processing request
    r = request
    body = request.get_json(force=True)
    filter, source = body['filter'],body['source']
    
    #reading data from file
    with open(source) as f:
        contents = f.readlines()
    
    #streaming UDP packets
    opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for row,row_data in enumerate(contents):
        if (row<MAX_ROWS_TO_PROCESS):
            opened_socket.sendto(bytes(row_data, encoding='utf8'), (EBPF_HOST, EBPF_PORT))

    return Response(response={"status":"success"}, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="localhost", port=5023)