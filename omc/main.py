#!/usr/bin/env python

import logging
import os
import sys
import traceback

import pkg_resources
from omc.utils.file_utils import make_directory

from omc.core import built_in_resources, console
from omc.core.decorator import filecache

from omc.config import settings

# plugin implementation
# https://packaging.python.org/guides/creating-and-discovering-plugins/
import importlib
import pkgutil


# discovered_plugins = {
#     name: importlib.import_module(name)
#     for finder, name, ispkg
#     in pkgutil.iter_modules()
#     if name.startswith('omc_')
# }


def usage():
    console.log('''omc resource action params ''')


def init_logger():
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s"
    log_dir = settings.LOG_DIR
    make_directory(log_dir)
    logging.basicConfig(filename=os.path.join(log_dir, 'omc.log'), format=FORMAT, level=logging.INFO)


def main():
    init_logger()
    # logger = logging.getLogger('omc')
    resource_type = sys.argv[1]

    try:
        if resource_type in built_in_resources:
            mod = __import__(".".join(['omc', 'resources', resource_type, resource_type]),
                             fromlist=[resource_type.capitalize()])
        else:
            mod = __import__(".".join(['omc_' + resource_type, resource_type, resource_type]),
                             fromlist=[resource_type.capitalize()])
        clazz = getattr(mod, resource_type.capitalize())
        context = {
            'all': sys.argv,
            'index': 1,
            type: 'cmd'
        }
        clazz(context)._exec()
    except Exception as inst:
        traceback.print_exc()
        # usage()


if __name__ == '__main__':
    main()
