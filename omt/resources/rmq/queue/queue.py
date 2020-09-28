import argparse
import json

from omt.utils.rmq_utils import build_admin_params

from omt.common import CompletionMixin
from omt.common.formater import format_list
from omt.core import Resource


class Queue(Resource, CompletionMixin):
    def _completion(self, short_mode=True):
        super()._completion(short_mode)

        if not self._have_resource_value():
            # completions for queue name
            client = self.context['common']['client']
            queues = json.loads(client.invoke_list('queues'))
            results = [(one['name'], "auto_delete is %(auto_delete)s | vhost is %(vhost)s" % one) for one in queues]
            self.print_completion(results, short_mode=True)

    def list(self):
        client = self.context['common']['client']
        queues = client.invoke_list('queues')
        format_list(queues)

    def get(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--count', nargs="?", help='message count', type=str, default='100')
        args = parser.parse_args(self._get_params())
        client = self.context['common']['client']
        queue_name = self._get_resource_value()[0]
        messages = client.invoke_get(['queue=' + queue_name, 'count=' + args.count])
        format_list(messages)

    def delete(self):
        client = self.context['common']['client']
        queue_name = self._get_resource_value()[0]
        client.invoke_delete('queue', ['name=' + queue_name])

    def declare(self):
        # parser = argparse.ArgumentParser('exchange declare arguments')
        # parser.add_argument('--type', nargs='?', default='direct')

        client = self.context['common']['client']
        name = self._get_resource_value()[0]
        # args = parser.parse_args(self._get_params())

        client.invoke_declare('queue', ['name=' + name])

    def publish(self):
        '''Message will be published to the default exchange(amq.default) with routing key queue_name, routing it to this queue.'''
        client = self.context['common']['client']
        if not self._have_resource_value():
            raise Exception("no queue name provided")
        name = self._get_resource_value()[0]
        parser = argparse.ArgumentParser()
        parser.add_argument('--payload', nargs='?', help='message payload')

        args = parser.parse_args(self._get_params())

        if args.payload is None:
            raise Exception("payload can't be empty")

        params = {
            'exchange': 'amq.default',
            'routing_key': name,
            'payload': args.payload

        }
        client.invoke_publish(build_admin_params(params))

    def purge(self):
        client = self.context['common']['client']
        if not self._have_resource_value():
            raise Exception("no queue name provided")
        name = self._get_resource_value()[0]
        client.invoke_purge('queue', ['name=' + name])
