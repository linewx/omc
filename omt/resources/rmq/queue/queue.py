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
