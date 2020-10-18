import functools
import json
import os

import argparse
from datetime import datetime

from omt.resources.kube.kube_resource import KubeResource

from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core import simple_completion
from omt.core.resource import Resource
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from omt.utils.utils import get_obj_value, get_all_dict_Keys


class Pod(KubeResource):
    pass