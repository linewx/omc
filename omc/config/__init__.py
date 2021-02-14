import os
import pkgutil
import sys

import pkg_resources
from dynaconf import LazySettings


def get_user_home():
    system = sys.platform
    return os.environ['HOME']
    # if system == 'darwin':
    #     return os.environ['HOME']
    # else:
    #     return os.environ["APPDATA"]


def get_home():
    return os.path.join(get_user_home(), '.omc')


settings_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.yaml')

module_setting_files = []
for finder, name, ispkg in pkgutil.iter_modules():
    if name.startswith('omc_'):
        resource_type = name.replace('omc_', '').lower()
        try:
            module_setting_file = pkg_resources.resource_filename('omc_%(resource_type)s.config' % locals(), 'settings.yaml')
            if os.path.exists(module_setting_file):
                module_setting_files.append(module_setting_file)
        except Exception as error:
            pass

settings = LazySettings(
    # PRELOAD_FOR_DYNACONF=[os.path.join(os.environ['HOME'], '.omw', 'config', '*')]
    SETTINGS_FILE_FOR_DYNACONF=settings_file,  # <-- Loaded second (the main file)
    INCLUDES_FOR_DYNACONF=[*module_setting_files, os.path.join(get_home(), 'config', '*.yaml')]
)
