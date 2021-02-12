# -*- coding: utf-8 -*-
import os
import pkgutil

import pkg_resources

from omc.common import CmdTaskMixin
from omc.config import settings
from omc.core import Resource, built_in_resources
from omc.core.decorator import filecache


class Completion(Resource, CmdTaskMixin):

    def _description(self):
        return 'for resource completion'

    @filecache(duration=-1, file=os.path.join(settings.OMC_COMPLETION_CACHE_DIR, 'completion'))
    def _get_resource_completion(self):
        results = []
        resources = (pkg_resources.resource_listdir('omc', 'resources'))

        # for built-in resources
        for resource_type in built_in_resources:
            mod = __import__(".".join(['omc', 'resources', resource_type, resource_type]),
                             fromlist=[resource_type.capitalize()])
            clazz = getattr(mod, resource_type.capitalize())
            results.append(resource_type + ":" + clazz({})._description())

        # for plugins
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith('omc_'):
                resource_type = name.replace('omc_', '').lower()
                mod = __import__(".".join(['omc_' + resource_type, resource_type]),
                                 fromlist=[resource_type.capitalize()])
                clazz = getattr(mod, resource_type.capitalize())
                results.append(resource_type + ":" + clazz({})._description())

        # }

        return "\n".join(results)

    def _run(self):
        if '--refresh' in self.context['all']:
            self._clean_completin_cache()
        print(self._get_resource_completion())
