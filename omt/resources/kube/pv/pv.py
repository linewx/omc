from omt.common import CmdTaskMixin
from omt.core.resource import Resource


class Pv(Resource, CmdTaskMixin):
    def _completion(self, short_mode=True):
        super()._completion(True)

        if not self._have_resource_value():
            client = self.context['common']['client']
            ret = client.list_persistent_volume(watch=False)
            self._print_completion([one.metadata.name for one in ret.items], True)

    def list(self):
        client = self.context['common']['client']
        result = client.list_persistent_volume(watch=False)
        print(result)

    def describe(self):
        pass
