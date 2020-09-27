import argparse
import json

from omt.common.formater import format_list
from omt.core import Resource
import argparse

from omt.utils.rmq_utils import build_admin_params


class Exchange(Resource):
    def _completion(self, short_mode=False):
        super()._completion(True)

        if not self._get_resource_value():
            # resource haven't filled yet
            client = self.context['common']['client']
            exchanges = json.loads(client.invoke_list('exchanges'))
            results = [(one['name'], "name is %(name)s, type is %(type)s | vhost is %(vhost)s" % one) for one in
                       exchanges]
            self._print_completion(results, short_mode=True)

    def list(self):
        client = self.context['common']['client']
        exchanges = client.invoke_list('exchanges')
        format_list(exchanges)

    def delete(self):
        client = self.context['common']['client']
        name = self._get_resource_value()[0]
        client.invoke_delete('exchange', ['name=' + name])

    def declare(self):
        client = self.context['common']['client']
        if not self._have_resource_value():
            raise Exception("no exchange name provided")
        name = self._get_resource_value()[0]
        parser = argparse.ArgumentParser('exchange declare arguments')
        parser.add_argument('--type', nargs='?', default='direct')
        args = parser.parse_args(self._get_params())
        client.invoke_declare('exchange', ['name=' + name, "=".join(['type', args.type])])

    def publish(self):
        client = self.context['common']['client']
        name = self._get_resource_value()[0] if self._have_resource_value() else 'amq.default'
        parser = argparse.ArgumentParser()
        parser.add_argument('--routing-key', nargs='?', help='routing key')
        parser.add_argument('--payload', nargs='?', help='message payload')

        args = parser.parse_args(self._get_params())

        if args.routing_key is None:
            raise Exception("routing-key can't be empty")

        if args.payload is None:
            raise Exception("payload can't be empty")

        params = {
            'exchange': name,
            'routing_key': args.routing_key,
            'payload': args.payload

        }
        client.invoke_publish(build_admin_params(params))
