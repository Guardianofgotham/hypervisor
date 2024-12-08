from rest_framework import serializers

from deployments.constants import DeploymentPriority
from users.common import ApiSerializer
from .models import Deployment


class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = [
            "id",
            "name",
            "cluster",
            "docker_image_path",
            "required_ram",
            "required_cpu",
            "required_gpu",
            "priority",
            "status",
            "duration",
            "created_at",
            "started_at",
            "completed_at",
        ]


class CreateDeploymentSerializer(ApiSerializer):
    name = serializers.CharField(help_text="Deployment name")
    cluster_id = serializers.IntegerField(help_text="Target cluster id")
    docker_image_path = serializers.CharField(help_text="Docker image path")
    required_ram = serializers.IntegerField(help_text="RAM needed for deployment in MB")
    required_cpu = serializers.IntegerField(help_text="CPU cores needed for deployment")
    required_gpu = serializers.IntegerField(
        help_text="number of GPUs needed for deployment"
    )
    priority = serializers.ChoiceField(
        choices=DeploymentPriority.choices, help_text="Priority of deployment"
    )
