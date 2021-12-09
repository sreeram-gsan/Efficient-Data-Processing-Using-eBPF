import platform
import sys
import pika
import os

infoKey = f"{platform.node()}.worker.info"
debugKey = f"{platform.node()}.worker.debug"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

def open_channel():
    #create channel in rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')
    return {'channel': channel, 'connection':connection}

def close_channel(channel_obj):
    channel,connection = channel_obj['channel'], channel_obj['connection']
    channel.close()
    connection.close()

def log_debug_channel(channel, message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    channel.basic_publish(
        exchange='logs', routing_key=key, body=message)
def log_info(channel,message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    channel.basic_publish(
        exchange='logs', routing_key=key, body=message)

def log_debug(message, key=debugKey):
    c_obj = open_channel()
    channel  = c_obj['channel']
    log_debug_channel(channel=channel,message=message)
    close_channel(c_obj)