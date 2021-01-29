from omc.common import CmdTaskMixin
from omc.resources.kube.kube_section_resource import KubeSectionResource


class Section(KubeSectionResource, CmdTaskMixin):
    pass
