# -*- coding: utf-8 -*-
import os

import pkg_resources

from omc.common import CmdTaskMixin
from omc.config import settings
from omc.core import Resource
from omc.core.decorator import filecache


class Completion(Resource, CmdTaskMixin):

    def _description(self):
        return 'for resource completion'

    @filecache(duration=-1, file=os.path.join(settings.OMC_COMPLETION_CACHE_DIR, 'completion'))
    def _get_resource_completion(self):
        results = []
        resources = (pkg_resources.resource_listdir('omc', 'resources'))
        resources = list(filter(lambda x: x != '__init__.py' and x not in ['__pycache__'], resources))
        for resource_type in resources:
            mod = __import__(".".join(['omc', 'resources', resource_type, resource_type]),
                             fromlist=[resource_type.capitalize()])
            clazz = getattr(mod, resource_type.capitalize())
            results.append(resource_type + ":" + clazz({})._description())

        return "\n".join(results)


    def _run(self):
        if '--refresh' in self.context['all']:
            self._clean_completin_cache()
        print(self._get_resource_completion())
