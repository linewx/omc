from omt.core import Resource


class Binding(Resource):
    def list(self):
        client = self.context['common']['client']
        client.invoke_list('bindings')

