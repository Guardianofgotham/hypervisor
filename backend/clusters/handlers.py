from clusters.models import Cluster
from deployments.models import Deployment


class ClusterHandler:
    def can_allocate_resources(self, cluster: Cluster, deployment: Deployment):
        if (
            cluster.available_ram >= deployment.required_ram
            and cluster.available_cpu >= deployment.required_cpu
            and cluster.available_gpu >= deployment.required_gpu
        ):
            return True
        return False

    def allocate_resources(self, cluster: Cluster, deployment: Deployment):
        if self.can_allocate_resources(cluster, deployment):
            cluster.available_ram -= deployment.required_ram
            cluster.available_cpu -= deployment.required_cpu
            cluster.available_gpu -= deployment.required_gpu
            return cluster
        raise Exception("Can't allocate resource")

    def free_resources(self, cluster: Cluster, deployment: Deployment):
        cluster.available_ram += deployment.required_ram
        cluster.available_cpu += deployment.required_cpu
        cluster.available_gpu += deployment.required_gpu
        return cluster
