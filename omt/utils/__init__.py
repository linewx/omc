import pkg_resources


class JmxTermUtils:
    @staticmethod
    def build_command(command):
        jmxterm = pkg_resources.resource_filename(__name__, '../lib/jmxterm-1.0.2-uber.jar')
        jmx_cmd = 'echo "%s"  | java -jar %s -n' % (command, jmxterm)
        return jmx_cmd