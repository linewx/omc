from omt.core import Resource


class Exchange(Resource):
    def list(self):
        client = self.context['common']['client']
        client.invoke_list('exchanges')

