from django.db import models

from organizations.models import Organization


# Create your models here.
class Cluster(models.Model):
    name = models.CharField(null=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    total_ram = models.IntegerField(null=False)
    total_cpu = models.IntegerField(null=False)
    total_gpu = models.IntegerField(null=False)

    available_ram = models.IntegerField(null=False)
    available_cpu = models.IntegerField(null=False)
    available_gpu = models.IntegerField(null=False)
