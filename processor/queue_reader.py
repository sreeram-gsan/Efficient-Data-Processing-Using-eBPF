import pika
import os
import json
import requests

'''
queue_reader.py 

Polls the toProcessor queue and pushes the source file location to the extractor
'''
def main():
    rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
    print(f"rabbitmq host {rabbitMQHost}")
    rabbitMQ = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()

    rabbitMQChannel.queue_declare(queue='toProcessor')
    rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    body = body.decode('utf-8')
    body = json.loads(body)
    filter, source = body['filter'],body['source']
    print(f"filter :{filter} source_file:{source}")

    headers = {'content-type': 'application/json'}
    extractorHost  = os.getenv("EXTRACTOR_HOST") or "localhost"
    addr = f"http://{extractorHost}:5024"
    add_url = addr + "/api/v1/extract"
    response = requests.post(add_url, json=body, headers=headers)

    # decode response
    print("Response is", response)
    print(json.loads(response.text))

if __name__ == "__main__":
    main()
    