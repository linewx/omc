import json

from omt.common import CompletionMixin
from omt.common.formater import format_list
from omt.core import Resource
import argparse


class Binding(Resource, CompletionMixin):
    def __init__(self, context={}, type='web'):
        super().__init__(context, type)
        self.parser = argparse.ArgumentParser("binding arguments parser")
        self.parser.add_argument('--src', nargs='?', type=str, help='binding source')
        self.parser.add_argument('--dest', nargs='?', type=str, help='binding destination')
        self.parser.add_argument('--type', nargs='?', type=str, help='binding destination type')
        self.parser.add_argument('--type', nargs='?', type=str, help='binding property key')

    def default_columns(self):
        client = self.context['common']['client']
        bindings = client.invoke_list('bindings')
        format_list(bindings, ['source', 'destination', 'routing_key'], 'table')

    def _binding_list(self):
        client = self.context['common']['client']
        bindings = json.loads(client.invoke_list('bindings'))
        results = [(
                               "--binding-source %(source)s --binding-destination %(destination)s --binding-destination-type %(destination_type)s --binding-properties_key %(properties_key)s" % one,'')
                   for one in bindings]
        self.print_completion(results, short_mode=True)

    def list(self):
        client = self.context['common']['client']
        bindings = client.invoke_list('bindings')
        format_list(bindings)

    def delete(self):
        if 'completion' in self.__get_params():
            self._binding_list()
            return

        client = self.context['common']['client']

        args = self.parser.parse_args(self.__get_action_params())
        if args.src is None:
            raise Exception("binding source can not be empty")

        if args.binding_destination is None:
            raise Exception("binding destination can not be empty")

        if args.type is None:
            raise Exception("binding destination-type can not be empty")

        delete_args = ['source=' + args.src, 'destination=' + args.dest,
                       'destination_type=' + args.type]

        if args.binding_properties_key is not None:
            delete_args.append('properties_key=' + args.binding_properties_key)

        client.invoke_delete('binding', delete_args)

    def declare(self):
        if 'completion' in self.__get_params():
            params = self.__get_params()
            if len(params) == 1:
                #no params, omt rmq binding completion
                self.print_completion(['--src', '--dest'])

            # omt rmq binding declare

        parser = argparse.ArgumentParser('exchange declare arguments')
        parser.add_argument('--src', nargs='?', required=True, help='binding source')
        parser.add_argument('--dest', nargs='?', required=True, help='binding destination')

        client = self.context['common']['client']
        args = parser.parse_args(self.__get_params())

        client.invoke_declare('binding', self.build_admin_params({
            'source': args.src,
            'destination': args.dest,
        }))

    def build_admin_params(self, params):
        return ['='.join([k, v]) for k, v in params.items()]
