from omt.core import Resource
import pika


class Rmq(Resource):
    def _list_resources(self):
        pass


def publish():
    auth = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='omt_test')

    channel.basic_publish(exchange='',
                          routing_key='omt_test',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()


def consume():
    auth = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='omt_test')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(on_message_callback=callback,
                          queue='omt_test',
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    import sys
    if 'consume' in sys.argv:
        consume()
    elif 'publish' in sys.argv:
        publish()

