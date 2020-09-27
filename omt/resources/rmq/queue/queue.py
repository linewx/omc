import json

from omt.common import CompletionMixin
from omt.common.formater import format_list
from omt.core import Resource


class Queue(Resource, CompletionMixin):
    def _completion(self, short_mode=True):
        super()._completion(short_mode)

        if not self._have_resource_value():
            # completions for queue name
            client = self.context['common']['client']
            queues = json.loads(client.invoke_list('queues'))
            results = [(one['name'], "auto_delete is %(auto_delete)s | vhost is %(vhost)s" % one) for one in queues]
            self.print_completion(results, short_mode=True)

    def list(self):
        client = self.context['common']['client']
        queues = client.invoke_list('queues')
        format_list(queues)

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
