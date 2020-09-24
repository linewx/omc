from omt.core import Resource
import pika
import pyrabbit

from omt.utils import UrlUtils
from omt.utils.rabbitmq import Management


class Rmq(Resource):
    def _list_resources(self):
        pass

    def _before_sub_resource(self):
        url = self._get_resource_value()[0]
        url_utils = UrlUtils(url)
        url_without_identification = url_utils.get_hostname() + ":" + str(url_utils.get_port())
        username = url_utils.get_username()
        password = url_utils.get_password()

        parsed = url_utils.parse()
        self.context['common'] = {
            'client': Management({
                'hostname': parsed.hostname,
                'port': parsed.port,
                'username': parsed.username,
                'password': parsed.password
            })
        }


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

