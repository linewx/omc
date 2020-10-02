# -*- coding: utf-8 -*-
from os.path import exists

from omt.common import CmdTaskMixin
from omt.core import Resource
import pkg_resources

from omt.utils import JmxTermUtils


class Jmx(Resource, CmdTaskMixin):
    """
NAME
    jmx - jmx command

SYNOPSIS
    jmx [RESOURCE] action [OPTION]

ACTION LIST

    """

    def _description(self):
        return 'JMX(Java Management Extensions) Tool Set'

    def _run(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../lib/jmxterm-1.0.2-uber.jar')
        cmd = 'java -jar %s' % jmxterm
        self.run_cmd('echo %s' % cmd)

    def jvms(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../lib/jmxterm-1.0.2-uber.jar')
        cmd = 'echo jvms | java -jar %s -n' % jmxterm
        self.run_cmd(cmd)

    def _completion(self, short_mode=False):
        super()._completion(True)

        if not self._have_resource_value():
            cmd = JmxTermUtils.build_command("jvms")
            result = self.run_cmd(cmd, capture_output=True, verbose=False)
            output = result.stdout.decode("utf-8").splitlines()
            jvms = [list(map(lambda x: str(x).strip(), str(one).split(" ", 1))) for one in output]
            self._print_completion(jvms)
