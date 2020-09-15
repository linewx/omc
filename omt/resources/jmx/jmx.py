# -*- coding: utf-8 -*-
from os.path import exists

from omt.common import CmdTaskMixin
from omt.core import Resource
import pkg_resources


class Jmx(Resource, CmdTaskMixin):
    """
NAME
    jmx - jmx command

SYNOPSIS
    jmx [RESOURCE] action [OPTION]

ACTION LIST

    """

    def _run(self):

        jmxterm = pkg_resources.resource_filename(__name__, '../../lib/jmxterm-1.0.2-uber.jar')
        cmd = 'java -jar %s' % jmxterm
        self.run_cmd('echo %s' % cmd)

    def jvms(self):
        jmxterm = pkg_resources.resource_filename(__name__, '../../lib/jmxterm-1.0.2-uber.jar')
        cmd = 'echo jvms | java -jar %s -n' % jmxterm
        self.run_cmd(cmd)

