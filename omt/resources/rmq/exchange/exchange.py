import json

from omt.common import CompletionMixin
from omt.common.formater import format_list
from omt.core import Resource
import argparse


class Exchange(Resource, CompletionMixin):
    def _list_resources(self):
    # for completions
        client = self.context['common']['client']
        exchanges = json.loads(client.invoke_list('exchanges'))
        results = [(one['name'], "name is %(name)s, type is %(type)s | vhost is %(vhost)s" % one) for one in exchanges]
        self.print_completion(results, short_mode=True)

    def list(self):
        client = self.context['common']['client']
        exchanges = client.invoke_list('exchanges')
        format_list(exchanges)

    def delete(self):
        client = self.context['common']['client']
        name = self._get_resource_value()[0]
        client.invoke_delete('exchange', ['name=' + name])

    def declare(self):
        parser = argparse.ArgumentParser('exchange declare arguments')
        parser.add_argument('--type', nargs='?', default='direct')

        client = self.context['common']['client']
        name = self._get_resource_value()[0]
        args = parser.parse_args(self._get_params())

        client.invoke_declare('exchange', ['name=' + name, "=".join(['type', args.type])])
