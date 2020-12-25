import pkg_resources

from omt.common import CmdTaskMixin
from omt.core import Resource


class Config(Resource, CmdTaskMixin):
    def init(self):
        # 1. set up omt-completion.sh
        completion = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')



    def sync_version(self):
        pass
