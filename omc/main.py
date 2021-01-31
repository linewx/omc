#!/usr/bin/env python

import logging
import os
import sys
import traceback

import pkg_resources
from omc.core.decorator import filecache

from omc.config import settings


def usage():
    print('''omc resource action params ''')


def main():
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(__name__)
    resource_type = sys.argv[1]

    try:
        mod = __import__(".".join(['omc', 'resources', resource_type, resource_type]),
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
        usage()


if __name__ == '__main__':
    main()