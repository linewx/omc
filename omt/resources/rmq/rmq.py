import os

from omt.core import Resource
import argparse

from omt.utils import UrlUtils
from omt.utils.rabbitmq import Management
from omt.config import settings


class Rmq(Resource):
    def __init__(self, context={}, type='web'):
        super().__init__(context, type)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--vhost', nargs='?', help='rabbitmq vhost')
        self.parser.add_argument('url', nargs='?', help='rabbitmq connection string', default='')

    def _list_resources(self):
        pass

    def _before_sub_resource(self):
        self.context['common'] = {
            'client': Management(self._build_configuration())
        }

    def _build_configuration(self):
        args = self.parser.parse_args(self._get_resource_value())
        config = {}
        if args.url:
            if 'http://' in args.url:
                # connection string: http://guest:guest@localhost:15672
                url_utils = UrlUtils(args.url)
                parsed = url_utils.parse()
                config = {
                    'hostname': parsed.hostname if parsed.hostname else 'localhost',
                    'port': parsed.port if parsed.port else 15672,
                    'username': parsed.username if parsed.username else 'guest',
                    'password': parsed.password if parsed.password else 'guest'
                }
            else:
                # parsed as instance, read from config file
                import json
                config_file_name = os.path.join(settings.RESOURCE_CONFIG_DIR, self.__class__.__name__.lower()  + '.json')

                with open(config_file_name) as f:
                    instances = json.load(f)
                    if args.url in instances:
                        config = instances[args.url]
                pass
        else:
            # no url provided
            pass

        if args.vhost is not None:
            config['vhost'] = args.vhost
            config['declare_vhost'] = args.vhost
        return config


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
