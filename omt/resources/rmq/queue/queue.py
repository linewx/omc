from omt.core import Resource


class Queue(Resource):
    def list(self):
        client = self.context['common']['client']
        client.invoke_list('queues')
        # for name in list(map(lambda x: x.get('name'), client.get_queues())):
        #     print(name)