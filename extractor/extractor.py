from flask import Flask, request, Response
import logging
import jsonpickle
import os

'''
extractor.py

pull data from the source location and packet the data to the network 
'''
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    r = request
    body = request.get_json(force=True)
    filter, source = body['filter'],body['source']
    print(f" extractor - filter :{filter} source_file:{source}")
    response_pickled = jsonpickle.encode({"source_file":"recieved!"})
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5024)
