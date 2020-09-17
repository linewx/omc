#!/usr/bin/env python

import sys
import logging
from omt import utils
import omt
import traceback
import pkg_resources


def usage():
    print('''omt resource action params ''')


def list_resources():
    resources = (pkg_resources.resource_listdir('omt', 'resources'))
    resources = list(filter(lambda x: x != '__init__.py' and x != '__pycache__', resources))
    for resource_type in resources:
        mod = __import__(".".join(['omt', 'resources', resource_type, resource_type]),
                         fromlist=[resource_type.capitalize()])
        clazz = getattr(mod, resource_type.capitalize())
        print(resource_type + ":" + clazz({}).description())


def main():
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(__name__)
    resource_type = sys.argv[1]

    if resource_type == 'completion':
        list_resources()
        return

    try:
        mod = __import__(".".join(['omt', 'resources', resource_type, resource_type]),
                         fromlist=[resource_type.capitalize()])
        clazz = getattr(mod, resource_type.capitalize())
        context = {
            'all': sys.argv,
            'index': 1,
            type: 'web'
        }
        clazz(context)._exec()
    except Exception as inst:
        traceback.print_exc()
        logger.error(inst)
        usage()


if __name__ == '__main__':
    main()
