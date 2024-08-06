import asyncio
import aio_pika
import os

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv('RABBITMQ_USER', 'user')
rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'password')
queue_name = 'request'

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        # Add your processing logic here
        print(f" [x] Received {message.body.decode()}")

async def main():
    connection = await aio_pika.connect_robust(
        host=rabbitmq_host,
        port=rabbitmq_port,
        login=rabbitmq_user,
        password=rabbitmq_pass
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=False)

        await queue.consume(process_message)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())