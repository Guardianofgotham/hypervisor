from rest_framework import serializers

from users.common import ApiSerializer


class CreateOrganizationSerializer(ApiSerializer):
    name = serializers.CharField(required=True, help_text="Name of organization")


class OrganizationSerializerWithoutInviteCode(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(required=True)


class OrganizationSerializer(OrganizationSerializerWithoutInviteCode):
    invite_code = serializers.CharField(required=False, read_only=True)


class JoinOrganizationSerializer(ApiSerializer):
    invite_code = serializers.CharField(required=True)
