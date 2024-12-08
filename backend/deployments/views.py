from django.shortcuts import render
from rest_framework import viewsets

from deployments.constants import DeploymentStatus
from deployments.models import Deployment
from clusters.models import Cluster
from deployments.serializers import CreateDeploymentSerializer, DeploymentSerializer
from rest_framework.response import Response
from rest_framework import status
from random import randint


# Create your views here.
class DeploymentViewset(viewsets.ViewSet):
    serializer_class = CreateDeploymentSerializer

    def create(self, request):
        data = CreateDeploymentSerializer(request.data).get_validated_data()

        try:
            cluster = Cluster.objects.get(id=data["cluster_id"])
            if request.user not in cluster.organization.users.all():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="You're not allowed to perform this action",
                )
            deployment = Deployment.objects.create(
                **data, status=DeploymentStatus.PENDING, duration=randint(10, 60)
            )
        except Cluster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Cluster not found")

        return Response(
            status=status.HTTP_201_CREATED, data=DeploymentSerializer(deployment).data
        )
