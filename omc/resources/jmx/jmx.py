# -*- coding: utf-8 -*-
import json
import os
from os.path import exists

from omc.config import settings

from omc.common import CmdTaskMixin
from omc.core import Resource
import pkg_resources

from omc.core.decorator import filecache
from omc.utils import JmxTermUtils


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

    @filecache(duration=60 * 60 * 24, file=Resource._get_cache_file_name)
    def _completion(self, short_mode=True):
        results = []
        results.append(super()._completion(False))

        if not self._have_resource_value():
            # list rabbitmq connection instance from config file
            config_file_name = os.path.join(settings.CONFIG_DIR, self.__class__.__name__.lower() + '.json')
            if (os.path.exists(config_file_name)):
                with open(config_file_name) as f:
                    instances = json.load(f)
                    results.extend(
                        self._get_completion(
                            [(value.get('host') + ':'+ str(value.get('port')), key) for key, value in instances.items()],
                            False))

        return "\n".join(results)
