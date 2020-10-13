import functools
import os

import argparse
from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core import simple_completion
from omt.core.resource import Resource


class Pod(Resource, CmdTaskMixin):
    def _completion(self, short_mode=True):
        super()._completion(True)

        if not self._have_resource_value():
            client = self.context['common']['client']
            ret = client.list_pod_for_all_namespaces(watch=False)
            self._print_completion([one.metadata.name for one in ret.items],True)

    def list(self):
        client = self.context['common']['client']
        ret = client.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    def describe(self):
        pass



