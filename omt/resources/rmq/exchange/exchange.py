from omt.core import Resource


class Exchange(Resource):
    def list(self):
        client = self.context['common']['client']
        client.invoke_list('exchanges')

    def delete(self):
        client = self.context['common']['client']
        queue_name = self._get_resource_value()[0]
        client.invoke_delete('exchange', ['name=' + queue_name])

