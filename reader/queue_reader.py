import pika
import os
import json
import requests
import util.publish_logs as pl
'''
queue_reader.py 

Polls the toProcessor queue and pushes the source file location to the extractor
'''

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
pl.log_debug(f"rabbitmq host {rabbitMQHost}")
print(f"rabbitmq host {rabbitMQHost}")
rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toProcessor')
rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    pl.log_debug(" [x] Received %r" % body)
    body = body.decode('utf-8')
    body = json.loads(body)
    filter, source = body['filter'],body['source']
    pl.log_debug(f"filter :{filter} source_file:{source}")
    print(f"filter :{filter} source_file:{source}")

    headers = {'content-type': 'application/json'}
    extractorHost  = os.getenv("EXTRACTOR_HOST") or "localhost"
    addr = f"http://{extractorHost}"
    add_url = addr + "/api/v1/extract"
    response = requests.post(add_url, json=body, headers=headers)
    pl.log_debug(addr)
    # decode response
    print("Response is", response)
    print(json.loads(response.text))
    pl.log_debug(json.loads(response.text))

rabbitMQChannel.basic_consume(
queue='toProcessor', on_message_callback=callback, auto_ack=True)

rabbitMQChannel.start_consuming()
    