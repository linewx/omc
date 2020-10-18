import json
from datetime import datetime

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from omt.common import CmdTaskMixin
from omt.core.resource import Resource
from omt.utils.utils import get_obj_value, get_all_dict_Keys, set_obj_value


def dateconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


class KubeResource(Resource, CmdTaskMixin):
    def __init__(self, context={}, type='web'):
        super().__init__(context, type)
        self.client = self.context['common']['client']

    def _get_kube_resource_type(self):
        return self._get_resource_name()

    def _read_namespaced_resource(self, name, namespace):
        read_func = getattr(self.client, 'read_namespaced_' + self._get_kube_resource_type())
        return read_func(name, namespace)

    def _completion(self, short_mode=True):
        super()._completion(True)

        if not self._have_resource_value():
            ret = self.client.list_resource_for_all_namespaces(watch=False)
            self._print_completion([one.metadata.name for one in ret.items], True)

    def list(self):
        ret = self.client.list_resource_for_all_namespaces(watch=False)
        print(ret)

    def describe(self):
        pass

    def yaml(self):
        resource = self._get_one_resource_value()
        namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
        result = self._read_namespaced_resource(resource, namespace)
        stream = StringIO()
        the_result = result.to_dict()
        yaml = YAML()
        yaml.dump(the_result, stream)
        print(stream.getvalue())

    def json(self):
        resource = self._get_one_resource_value()
        namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
        result = self._read_namespaced_resource(resource, namespace)
        the_result = result.to_dict()
        print(json.dumps(the_result, default=dateconverter, indent=4))

    @staticmethod
    def _build_field_selector(selectors):
        return ','.join(['%s=%s' % (k, v) for (k, v) in selectors.items()])

    def namespace(self):
        resource = self._get_one_resource_value()
        namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
        print(namespace)

    def event(self):
        # https://kubernetes.docker.internal:6443/api/v1/namespaces/default/events?fieldSelector=
        # involvedObject.uid=4bb31f4d-99f1-4acc-a024-8e2484573733,
        # involvedObject.name=itom-xruntime-rabbitmq-6464654786-vnjxz,
        # involvedObject.namespace=default

        resource = self._get_one_resource_value()
        namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
        result = self._read_namespaced_resource(resource, namespace)

        uid = get_obj_value(result, 'metadata.uid')
        name = get_obj_value(result, 'metadata.name')

        the_selector = {
            "involvedObject.uid": uid,
            "involvedObject.namespace": namespace,
            "involvedObject.name": name,
        }

        print(self.client.list_namespaced_event(namespace, field_selector=self._build_field_selector(the_selector)))

    def get(self):
        if 'completion' in self._get_params():
            resource = self._get_one_resource_value()
            namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
            result = self._read_namespaced_resource(resource, namespace)
            prompts = []
            get_all_dict_Keys(result.to_dict(), prompts)
            self._print_completion(prompts)
            return

        resource = self._get_one_resource_value()
        namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
        result = self._read_namespaced_resource(resource, namespace)
        params = self._get_action_params()

        the_params = " ".join(params)

        if not the_params.strip():
            print(result)
        else:
            print(get_obj_value(result, the_params))

    def set(self):
        if 'completion' in self._get_params():
            resource = self._get_one_resource_value()
            namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
            result = self._read_namespaced_resource(resource, namespace)
            prompts = []
            get_all_dict_Keys(result.to_dict(), prompts)
            self._print_completion(prompts)
            return

        resource = self._get_one_resource_value()
        namespace = self.client.get_namespace(self._get_kube_resource_type(), resource)
        result = self._read_namespaced_resource(resource, namespace)
        params = self._get_action_params()
        config_key = params[0]
        config_value = params[1]

        set_obj_value(result, config_key,  config_value)
        print(result)
