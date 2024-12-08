from rest_framework.viewsets import ViewSet

from clusters.models import Cluster
from clusters.serializers import ClusterSerializer
from users.serializers import UserSerializer
from organizations.models import Organization
from organizations.serializers import (
    CreateOrganizationSerializer,
    JoinOrganizationSerializer,
    OrganizationSerializer,
    OrganizationSerializerWithoutInviteCode,
)
from rest_framework.response import Response
from rest_framework import status
import uuid
from rest_framework.decorators import action


# Create your views here.
class OrganizationViewSet(ViewSet):
    serializer_class = CreateOrganizationSerializer

    def create(self, request):
        """
        Create organization
        """
        data = CreateOrganizationSerializer(request.data).get_validated_data()
        current_user = request.user
        org: Organization = Organization.objects.create(
            **data, invite_code=uuid.uuid4()
        )
        org.users.add(current_user)
        return Response(
            status=status.HTTP_201_CREATED,
            data=OrganizationSerializer(org).data,
        )

    @action(methods=["POST"], detail=False, serializer_class=JoinOrganizationSerializer)
    def join(self, request):
        """
        Join organization with invite code
        """
        data = JoinOrganizationSerializer(request.data).get_validated_data()

        try:
            org = Organization.objects.get(invite_code=data["invite_code"])
            org.users.add(request.user)
        except Organization.DoesNotExist:
            return Response(
                {"detail": "Invalid invite code."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def list_organization_users(self, request, pk=None):
        """
        List organization users
        """
        try:
            org = Organization.objects.get(pk=pk)
            if request.user not in org.users.all():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="You are not authorized for this action",
                )
            return Response(
                data={
                    "current_organization": OrganizationSerializer(org).data,
                    "users": UserSerializer(org.users.all(), many=True).data,
                }
            )
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Not found")

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["GET"], detail=False)
    def list_user_orgs(self, request):
        """
        List of all organization current user belongs to
        """
        linked_orgs = Organization.objects.filter(users=request.user)

        return Response(
            data={
                "user": UserSerializer(request.user).data,
                "orgs": OrganizationSerializerWithoutInviteCode(
                    linked_orgs, many=True
                ).data,
            }
        )

    @action(methods=["GET"], detail=True)
    def clusters(self, request, pk=None):
        try:
            org = Organization.objects.get(id=pk)
            if request.user not in org.users.all():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="You're not allowed to perform this action",
                )
            clusters = Cluster.objects.filter(organization=org)

            return Response(
                status=status.HTTP_200_OK,
                data={"clusters": ClusterSerializer(clusters, many=True).data},
            )
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Org not found")
