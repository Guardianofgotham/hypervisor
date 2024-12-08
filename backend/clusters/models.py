from django.db import models

from organizations.models import Organization


# Create your models here.
class Cluster(models.Model):
    name = models.CharField(null=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    ram = models.IntegerField(null=False)
    cpu = models.IntegerField(null=False)
    gpu = models.IntegerField(null=False)
