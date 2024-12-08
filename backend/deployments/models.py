from django.db import models

from deployments.constants import DeploymentPriority, DeploymentStatus
from clusters.models import Cluster


# Create your models here.
class Deployment(models.Model):
    name = models.CharField()
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, null=False)
    docker_image_path = models.CharField()
    required_ram = models.IntegerField()
    required_cpu = models.IntegerField()
    required_gpu = models.IntegerField()
    priority = models.CharField(choices=DeploymentPriority.choices, null=False)
    status = models.CharField(choices=DeploymentStatus.choices, null=False)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)
