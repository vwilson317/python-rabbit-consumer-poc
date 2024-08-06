import pika
import os

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv('RABBITMQ_USER', 'user')
rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'password')

queue_name = os.getenv('QUEUE_NAME', 'request')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue=queue_name)

def callback(ch, method, properties, body):
    ## todo: add processing logic
    print(f" [x] Received {body}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()