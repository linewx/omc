# -*- coding: utf-8 -*-
import os
import pkgutil

import pkg_resources

from omc.common import CmdTaskMixin
from omc.common.common_completion import completion_cache, CompletionContent
from omc.config import settings
from omc.core import Resource, built_in_resources, console
from omc.core.decorator import filecache


class Completion(Resource, CmdTaskMixin):

    def _description(self):
        return 'for resource completion'

    @completion_cache(duration=-1, file=os.path.join(settings.OMC_COMPLETION_CACHE_DIR, 'completion'))
    def _get_resource_type_completion(self):
        results = []

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
                mod = __import__(".".join(['omc_' + resource_type, resource_type, resource_type]),
                                 fromlist=[resource_type.capitalize()])
                clazz = getattr(mod, resource_type.capitalize())
                results.append(resource_type + ":" + clazz({})._description())

        # }

        return CompletionContent(results)

    def _run(self):
        if '--refresh' in self.context['all']:
            self._clean_completin_cache()
        console.log(self._get_resource_type_completion().get_raw_content())
