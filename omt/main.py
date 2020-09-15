#!/usr/bin/env python

import sys
import logging
from omt import utils
import omt
import traceback


def usage():
    print('''omt resource action params ''')


if __name__ == '__main__':
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(__name__)
    resource_type = sys.argv[1]

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
