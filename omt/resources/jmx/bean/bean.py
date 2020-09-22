import pkg_resources

from omt.common import CmdTaskMixin
from omt.core import Resource


class Bean(Resource, CmdTaskMixin):
    def _run(self):
        pass

    def _list_resources(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')
        jmx = self.context['jmx']
        cmd = 'echo "open %s && beans"  | java -jar %s -n' % (jmx, jmxterm)
        result = self.run_cmd(cmd, capture_output=True)
        output = result.stdout.decode("utf-8").splitlines()
        for line in output:
            print(line.replace(":", "\:") + ":" + ' ')

    def info(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')
        jmx = self.context['jmx']
        bean = self._get_resource_value()
        bean = bean.replace(" ", "\\ ")
        cmd = 'echo "open %s && bean %s && info"  | java -jar %s -n' % (jmx, bean, jmxterm)
        print(cmd)
        self.run_cmd(cmd)

    def exec(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../../lib/jmxterm-1.0.2-uber.jar')
        jmx = self.context['jmx']
        bean = self._get_resource_value()
        cmd = 'echo "open %s && bean %s && info"  | java -jar %s -n' % (jmx, bean, jmxterm)
        self.run_cmd(cmd)

