import pkg_resources

from omc.common import CmdTaskMixin
from omc.core import Resource


class Config(Resource, CmdTaskMixin):
    def init(self):
        # 1. set up omc-completion.sh
        completion = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')



    def sync_version(self):
        pass
