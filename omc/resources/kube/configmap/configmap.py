from omc.resources.kube.kube_resource import KubeResource


class Configmap(KubeResource):
    pass

    def _get_kube_resource_type(self):
        return 'config_map'
