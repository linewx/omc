from omt.core import Resource
import argparse

class Exchange(Resource):


    def list(self):
        client = self.context['common']['client']
        client.invoke_list('exchanges')

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


