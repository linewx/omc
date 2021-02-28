import traceback

from omc.core import built_in_resources


class OmcService:
    def exec(self, commands, dry_run=False):
        resource_type = commands[1]
        if resource_type in built_in_resources:
            mod = __import__(".".join(['omc', 'resources', resource_type, resource_type]),
                             fromlist=[resource_type.capitalize()])
        else:
            mod = __import__(".".join(['omc_' + resource_type, resource_type, resource_type]),
                             fromlist=[resource_type.capitalize()])
        clazz = getattr(mod, resource_type.capitalize())
        context = {
            'all': commands,
            'index': 1,
            type: 'cmd'
        }
        return clazz(context)._exec(dry_run)

