import pika
import uuid

queue_name = 'request'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials('user', 'password')))
channel = connection.channel()
channel.queue_declare(queue=queue_name)

id = str(uuid.uuid4())

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body='{"id":"' + id + '", "someProp:": "someValue"}')

print("queue triggered")

connection.close()