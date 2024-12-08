from rest_framework import serializers

from clusters.models import Cluster
from users.common import ApiSerializer


class ClusterSerializer(serializers.ModelSerializer):
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
        ]


class CreateClusterSerializer(ApiSerializer):
    name = serializers.CharField(help_text="Name of the cluster.")
    organization_id = serializers.IntegerField(
        help_text="ID of the organization owning this cluster."
    )
    total_ram = serializers.FloatField(help_text="RAM size in MB")
    total_cpu = serializers.FloatField(help_text="Number of CPU cores")
    total_gpu = serializers.FloatField(help_text="Number of GPUs")
