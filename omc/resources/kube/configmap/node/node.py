from omc.common import CmdTaskMixin
from omc.resources.kube.kube_section_resource import KubeNodeResource


class Node(KubeNodeResource, CmdTaskMixin):
    def _get_kube_api_resource_type(self):
        return 'config_map'

