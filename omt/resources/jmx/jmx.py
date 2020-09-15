# -*- coding: utf-8 -*-
from os.path import exists

from omt.core import Resource
import pkg_resources

class Jmx(Resource):
    """
NAME
    jmx - jmx command

SYNOPSIS
    jmx [RESOURCE] action [OPTION]

ACTION LIST

    """

    def _run(self):
        if exists(pkg_resources.resource_filename(__name__, '../../lib/jmxterm-1.0.2-uber.jar')):
            print('exist')
        else:
            print('not exist')


