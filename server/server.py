from flask import Flask, request, Response
import logging
import pika
import jsonpickle
import os

'''
server.py

Accepts the filter and source file on which the filter has to applied. 
Adds the filter to the rabbitmq - under toprocessor channel/queue


end point - /api/v1/filter
input: {'filter':'filter_value', 'source_file':'source_file_value'}
output: 200 OK: filter accepted by the code
'''

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

@app.route('/api/v1/filter', methods=['POST'])
def analyze():
    r = request
    body = request.get_json(force=True)
    filter, source = body['filter'],body['source']
    print(f"filter :{filter} source_file:{source}")
    
    #create channel in rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost))
    channel = connection.channel()
    #declare queue
    channel.queue_declare(queue='toProcessor')
    message = jsonpickle.encode(body)
    channel.basic_publish(exchange='',routing_key='toProcessor',body=message)
    #close channel
    channel.close()
    connection.close()
    response_pickled = jsonpickle.encode({"action":"filter queued"})
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5023)
