from omt.core import Resource
import argparse


class Binding(Resource):
    def __init__(self, context={}, type='web'):
        super().__init__(context, type)
        self.parser = argparse.ArgumentParser("binding arguments parser")
        self.parser.add_argument('--binding-source', nargs='?', type=str, help='binding source')
        self.parser.add_argument('--binding-destination', nargs='?', type=str, help='binding destination')
        self.parser.add_argument('--binding-destination-type', nargs='?', type=str, help='binding destination type')
        self.parser.add_argument('--binding-properties_key', nargs='?', type=str, help='binding property key')

    def list(self):
        client = self.context['common']['client']
        client.invoke_list('bindings')

    def delete(self):
        client = self.context['common']['client']

        args = self.parser.parse_args(self._get_action_params())
        if args.binding_source is None:
            raise Exception("binding source can not be empty")

        if args.binding_destination is None:
            raise Exception("binding destination can not be empty")

        if args.binding_destination_type is None:
            raise Exception("binding destination-type can not be empty")

        delete_args = ['source=' + args.binding_source, 'destination=' + args.binding_destination,
                       'destination_type=' + args.binding_destination_type]

        if args.binding_properties_key is not None:
            delete_args.append('properties_key=' + args.binding_properties_key)

        client.invoke_delete('binding', delete_args)
