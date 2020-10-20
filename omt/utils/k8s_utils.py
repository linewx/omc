from kubernetes import client, config
from omt.common import CmdTaskMixin


class KubernetesClient(CmdTaskMixin):
    def __init__(self, config_file=None):
        if not config_file:
            config.load_kube_config()
        else:
            config.load_kube_config(config_file)

        self.config_file = config_file

        corev1api = client.CoreV1Api()
        appsv1api = client.AppsV1Api()
        extensionsv1beta1api = client.ExtensionsV1beta1Api()
        self.client_instances = [corev1api, appsv1api, extensionsv1beta1api]

    def __getattr__(self, item: str):
        for one_instance in self.client_instances:
            if hasattr(one_instance, item):
                return getattr(one_instance, item)

    def get_namespace(self, resource_type: str, resource_name: str):
        list_namespaces = getattr(self, "list_%s_for_all_namespaces" % resource_type)
        all_namespaces = list_namespaces()
        for one in all_namespaces.items:
            if one.metadata.name == resource_name:
                return one.metadata.namespace

    def apply(self, file):
        # todo: since apply not supported, need to impl

        # option1: using kubectl instead
        # option2: upgrade k8s version to support server-side apply
        # option3: implemented in client side myself
        config = ' --kubeconfig %s ' % self.config_file if self.config_file else ''

        cmd = "kubectl %(config)s apply -f %(file)s" % locals()
        result = self.run_cmd(cmd)

    def edit(self, resource_type: str, resource_name: str, namespace: str):
        config = ' --kubeconfig %s ' % self.config_file if self.config_file else ''
        self.run_cmd("kubectl %(config)s edit %(resource_type)s %(resource_name)s --namespace %(namespace)s" % locals())

    def portforward(self):
        pass

    def get(self, resource_type, resource_name, namespace: str, output='yaml'):
        config = ' --kubeconfig %s ' % self.config_file if self.config_file else ''

        result = self.run_cmd(
            "kubectl %(config)s get %(resource_type)s %(resource_name)s --namespace %(namespace)s -o %(output)s" % locals(),
            capture_output=True, verbose=False)
        return result.stdout.decode("utf-8")

    def download(self, resource_name, namespace, local_dir, remote_dir):
        config = ' --kubeconfig %s ' % self.config_file if self.config_file else ''
        cmd = "kubectl %(config)s cp %(namespace)s/%(resource_name)s:%(remote_dir)s %(local_dir)s" % locals()
        self.run_cmd(cmd)

    def upload(self, resource_name, namespace, local_dir, remote_dir):
        config = ' --kubeconfig %s ' % self.config_file if self.config_file else ''
        cmd = "kubectl %(config)s cp %(local_dir)s %(namespace)s/%(resource_name)s:%(remote_dir)s" % locals()
        self.run_cmd(cmd)

    def exec(self, resource_type, resource_name, namespace, command, container=None, stdin=True):
        config = ' --kubeconfig %s ' % self.config_file if self.config_file else ''
        interactive_option = '-it' if stdin else ''
        cmd = 'kubectl %(config)s exec %(interactive_option)s %(resource_type)s/%(resource_name)s --namespace %(namespace)s -- %(command)s' % locals()
        self.run_cmd(cmd)


if __name__ == '__main__':
    client = KubernetesClient("~/.omt/config/kube/nightly1/config")
    the_namespace = client.get_namespace("service", "smarta-smart-ticket-svc")
    print(the_namespace)
    #
    # print(client.list_config_map_for_all_namespaces(watch=False))
    # print(client.list_pod_for_all_namespaces(watch=False))
    # print(client.list_deployment_for_all_namespaces(watch=False))
    # print(client.list_service_for_all_namespaces(watch=False))
    # print(client.list_endpoints_for_all_namespaces(watch=False))
