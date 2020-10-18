import functools
import os

import argparse

from omt.resources.kube.kube_resource import KubeResource

from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core import simple_completion
from omt.core.resource import Resource
from prettytable import PrettyTable


class Configmap(KubeResource):
    pass

    def _get_kube_resource_type(self):
        return 'config_map'
