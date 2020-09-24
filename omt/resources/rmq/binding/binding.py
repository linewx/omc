from omt.core import Resource


class Binding(Resource):
    def list(self):
        client = self.context['common']['client']
        for one in client.get_bindings():
            print("source: %(source)s, destination: %(destination)s, routing_key: %(routing_key)s" % one)
