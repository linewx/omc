from omt.core import Resource


class Exchange(Resource):
    def list(self):
        client = self.context['common']['client']
        for name in list(map(lambda x: x.get('name'), client.get_exchanges())):
            print(name)
