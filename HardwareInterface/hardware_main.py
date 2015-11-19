#!/usr/bin/env python
#CODE FROM https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit  please press CTRL+C'

def callback(ch, method, properties, body):
	if body != "":
		print body

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

channel.start_consuming()
