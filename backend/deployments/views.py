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

            if (
                cluster.ram < data["required_ram"]
                or cluster.cpu < data["required_cpu"]
                or cluster.gpu < data["required_gpu"]
            ):
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="It is impossible to make this deployment, resources needed for deployment exceeds cluster total resources",
                )

            deployment = Deployment.objects.create(
                **data, status=DeploymentStatus.PENDING, duration=randint(10, 60)
            )
        except Cluster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Cluster not found")

        return Response(
            status=status.HTTP_201_CREATED, data=DeploymentSerializer(deployment).data
        )
