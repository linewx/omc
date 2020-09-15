import pkg_resources

from omt.common import CmdTaskMixin
from omt.core import Resource


class Bean(Resource, CmdTaskMixin):
    def _run(self):
        pass

    def list(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')
        jmx = self.context['jmx']
        cmd = 'echo "open %s && beans"  | java -jar %s -n' % (jmx, jmxterm)
        self.run_cmd(cmd)