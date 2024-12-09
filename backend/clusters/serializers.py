from rest_framework import serializers

from deployments.models import Deployment
from clusters.models import Cluster
from users.common import ApiSerializer
from django.db.models import Count


class ClusterSerializer(serializers.ModelSerializer):
    deployment_count = serializers.SerializerMethodField()

    class Meta:
        model = Cluster
        fields = [
            "id",
            "name",
            "organization",
            "total_ram",
            "total_cpu",
            "total_gpu",
            "available_ram",
            "available_cpu",
            "available_gpu",
            "deployment_count",
        ]

    def get_deployment_count(self, obj):
        deployments = (
            Deployment.objects.filter(cluster_id=obj.id)
            .values("status")
            .annotate(count=Count("id"))
        )
        status_count = {
            deployment["status"]: deployment["count"] for deployment in deployments
        }
        return status_count


class CreateClusterSerializer(ApiSerializer):
    name = serializers.CharField(help_text="Name of the cluster.")
    organization_id = serializers.IntegerField(
        help_text="ID of the organization owning this cluster."
    )
    total_ram = serializers.FloatField(help_text="RAM size in MB")
    total_cpu = serializers.FloatField(help_text="Number of CPU cores")
    total_gpu = serializers.FloatField(help_text="Number of GPUs")
