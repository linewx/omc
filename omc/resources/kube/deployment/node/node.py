from omc.common import CmdTaskMixin
from omc.resources.kube.kube_node_resource import KubeNodeResource


class Node(KubeNodeResource, CmdTaskMixin):
    pass
