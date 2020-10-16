import functools
import os

import argparse
from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core import simple_completion
from omt.core.resource import Resource
from prettytable import PrettyTable


class Service(Resource, CmdTaskMixin):
    def _completion(self, short_mode=True):
        super()._completion(True)

        if not self._have_resource_value():
            client = self.context['common']['client']
            ret = client.list_service_for_all_namespaces(watch=False)
            self._print_completion([one.metadata.name for one in ret.items], True)

    def list(self):
        client = self.context['common']['client']
        ret = client.list_service_for_all_namespaces(watch=False)
        print(ret)
        # table = PrettyTable()
        # table.field_names = ['NAMESPACE', 'NAME', 'TYPE', 'CLUSTER IP', 'PORT']
        # for i in ret.items:
        #     ports = []
        #     if i.spec.type == 'NodePort':
        #         for one_port_info in i.spec.ports:
        #             ports.append("%s:%s/%s" % (one_port_info.port, one_port_info.node_port, one_port_info.protocol))
        #     else:
        #         for one_port_info in i.spec.ports:
        #             ports.append("%s/%s" % (one_port_info.port, one_port_info.protocol))
        #
        #     table.add_row((i.metadata.namespace, i.metadata.name, i.spec.type, i.spec.cluster_ip, ','.join(ports)))
        # print(table)

    def describe(self):
        pass
