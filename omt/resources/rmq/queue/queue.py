from omt.core import Resource


class Queue(Resource):
    def list(self):
        client = self.context['common']['client']
        client.invoke_list('queues')
        # for name in list(map(lambda x: x.get('name'), client.get_queues())):
        #     print(name)

    def get(self):
        client = self.context['common']['client']
        queue_name = self._get_resource_value()[0]
        client.invoke_get(['queue=' + queue_name])

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


