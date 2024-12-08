from rest_framework import serializers

from clusters.models import Cluster
from users.common import ApiSerializer


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ["id", "name", "organization", "ram", "cpu", "gpu"]


class CreateClusterSerializer(ApiSerializer):
    name = serializers.CharField(help_text="Name of the cluster.")
    organization_id = serializers.IntegerField(
        help_text="ID of the organization owning this cluster."
    )
    ram = serializers.FloatField(help_text="RAM size in MB")
    cpu = serializers.FloatField(help_text="Number of CPU cores")
    gpu = serializers.FloatField(help_text="Number of GPUs")
