# -*- coding: utf-8 -*-
import os

import pkg_resources

from omc.common import CmdTaskMixin
from omc.config import settings
from omc.core import Resource
from omc.core.decorator import filecache


class Arthas(Resource, CmdTaskMixin):
    def _description(self):
        return 'Arthas - JVM Debug Tools'

    @filecache(duration=-1, file=os.path.join(settings.OMC_COMPLETION_CACHE_DIR, 'completion'))
    def _get_resource_completion(self):
        return ""

    def _run(self):
        arthas = pkg_resources.resource_filename(__name__, '../../lib/arthas-boot.jar')
        cmd = "java -jar %s" % arthas
        self.run_cmd(cmd)
