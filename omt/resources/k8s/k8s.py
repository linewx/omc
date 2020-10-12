import functools
import os

import argparse
from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core import simple_completion
from omt.core.resource import Resource
from kubernetes import client, config

class K8s(Resource, CmdTaskMixin):
    def _description(self):
        return 'The Kubernetes command-line tool'

    def _before_sub_resource(self):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        self.context['common'] = {
            'client': v1
        }


if __name__ == '__main__':
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
