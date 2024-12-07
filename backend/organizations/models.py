from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Organization(models.Model):
    name = models.CharField(null=False)
    users = models.ManyToManyField(User, related_name="organizations")
    invite_code = models.CharField(null=False, unique=True)
