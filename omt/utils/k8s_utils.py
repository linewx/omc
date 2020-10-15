from kubernetes import client, config


class KubernetesClient:
    def __init__(self, config_file):
        if not config_file:
            config.load_kube_config()
        else:
            config.load_kube_config(config_file)

        corev1api = client.CoreV1Api()
        appsv1api = client.AppsV1Api()
        self.client_instances = [corev1api, appsv1api]

    def __getattr__(self, item):
        for one_instance in self.client_instances:
            if hasattr(one_instance, item):
                return getattr(one_instance, item)


if __name__ == '__main__':
    client = KubernetesClient(None)
    print(client.list_config_map_for_all_namespaces(watch=False))
    print(client.list_pod_for_all_namespaces(watch=False))
    print(client.list_deployment_for_all_namespaces(watch=False))
    print(client.list_service_for_all_namespaces(watch=False))
    print(client.list_endpoints_for_all_namespaces(watch=False))

