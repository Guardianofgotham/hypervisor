from django.shortcuts import render
from rest_framework import viewsets

from deployments.models import Deployment
from deployments.serializers import DeploymentSerializer
from clusters.models import Cluster
from organizations.models import Organization
from clusters.serializers import ClusterSerializer, CreateClusterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


# Create your views here.
class ClusterViewset(viewsets.ViewSet):
    serializer_class = CreateClusterSerializer

    def create(self, request):
        data = CreateClusterSerializer(request.data).get_validated_data()
        org_id = data["organization_id"]
        try:
            org = Organization.objects.get(id=org_id)
            if request.user not in org.users.all():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="You are not authorized for this action",
                )
            cluster = Cluster.objects.create(**data)

        except Organization.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data="Organization not found"
            )

        return Response(
            status=status.HTTP_201_CREATED, data=ClusterSerializer(cluster).data
        )

    @action(methods=["GET"], detail=True)
    def deployments(self, request, pk=None):
        try:
            cluster = Cluster.objects.get(id=pk)
            if request.user not in cluster.organization.users.all():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="You're not allowed to perform this action",
                )
            deployments = Deployment.objects.filter(cluster=cluster)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "cluster": ClusterSerializer(cluster).data,
                    "deployments": DeploymentSerializer(deployments, many=True).data,
                },
            )
        except Cluster.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data="Cluster not found"
            )
