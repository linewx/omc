import functools
import os

import argparse
from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core import simple_completion
from omt.core.resource import Resource
from kubernetes import client, config

from omt.utils.k8s_utils import KubernetesClient


class K8s(Resource, CmdTaskMixin):
    def _description(self):
        return 'The Kubernetes command-line tool'

    def _completion(self, short_mode=True):
        super()._completion(True)
        if not self._have_resource_value():
            if os.path.exists(settings.OMT_KUBE_CONFIG_DIR):
                resources = os.listdir(settings.OMT_KUBE_CONFIG_DIR)
                self._print_completion(resources, True)

    def _before_sub_resource(self):
        try:
            if self._have_resource_value():
                resource_value = self._get_one_resource_value()
                client = KubernetesClient(os.path.join(settings.OMT_KUBE_CONFIG_DIR, resource_value, 'config'))
            else:
                client = KubernetesClient()

            self.context['common'] = {
                'client': client
            }
        except:
            # some action no need to create load config, get config action e.g.
            pass


if __name__ == '__main__':
    config.load_kube_config()
    client = client.AppsV1Api()
    ret = client.list_service_for_all_namespaces(watch=False)

    # print(client.read_namespaced_pod("postgres-svc-5685d4bc7-l6j4m", 'default'))
    # print(client.read_namespaced_pod_template("postgres-svc-5685d4bc7-l6j4m", 'default'))
    # print(client.read_namspaced_event("postgres-svc-5685d4bc7-l6j4m", 'default'))
    print(ret)
    # for i in ret.items:
    #     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
