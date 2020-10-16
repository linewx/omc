import functools
import json
import os

import argparse
from datetime import datetime

from omt.common import CmdTaskMixin
from omt.config import settings
from omt.core import simple_completion
from omt.core.resource import Resource
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


def dateconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


class Pod(Resource, CmdTaskMixin):
    def __init__(self, context={}, type='web'):
        super().__init__(context, type)
        self.client = self.context['common']['client']

    def _completion(self, short_mode=True):
        super()._completion(True)

        if not self._have_resource_value():
            client = self.context['common']['client']
            ret = client.list_pod_for_all_namespaces(watch=False)
            self._print_completion([one.metadata.name for one in ret.items], True)

    def list(self):
        client = self.context['common']['client']
        ret = client.list_pod_for_all_namespaces(watch=False)
        print(ret)

    def describe(self):
        pass

    def yaml(self):
        pod = self._get_one_resource_value()
        namespace = self.client.get_namespace('pod', pod)
        result = self.client.read_namespaced_pod(pod, namespace)
        stream = StringIO()
        the_result = result.to_dict()
        yaml = YAML()
        yaml.dump(the_result, stream)
        print(stream.getvalue())

    def json(self):
        pod = self._get_one_resource_value()
        namespace = self.client.get_namespace('pod', pod)
        result = self.client.read_namespaced_pod(pod, namespace)
        the_result = result.to_dict()
        print(json.dumps(the_result, default=dateconverter, indent=4))
