import os
import sys

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
settings = LazySettings(
    # PRELOAD_FOR_DYNACONF=[os.path.join(os.environ['HOME'], '.omw', 'config', '*')]
    SETTINGS_FILE_FOR_DYNACONF=settings_file,  # <-- Loaded second (the main file)
    INCLUDES_FOR_DYNACONF=[os.path.join(get_home(), 'config', '*.yaml')]
)
