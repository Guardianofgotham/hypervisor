from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from organizations.models import Organization


class OrganizationViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="testpassword123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="testpassword123"
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

    def test_create_organization(self):
        """
        Test that an organization can be created successfully.
        """
        data = {"name": "Test Organization"}
        response = self.client.post("/organizations/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", response.data)
        self.assertEqual(response.data["name"], data["name"])

    def test_create_organization_without_authentication(self):
        """
        Test that creating an organization without authentication fails.
        """
        self.client.credentials()  # No token
        data = {"name": "Test Organization", "description": "A test org"}
        response = self.client.post("/organizations/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_join_organization_with_valid_invite_code(self):
        """
        Test that a user can join an organization with a valid invite code.
        """
        invite_code = "blah"
        Organization.objects.create(name="Test Org", invite_code=invite_code)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token2.key)
        data = {"invite_code": invite_code}
        response = self.client.post("/organizations/join/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_orgs(self):
        """
        Test that a user can list all organizations they belong to.
        """
        org1 = Organization.objects.create(name="Org 1", invite_code="blah")
        org2 = Organization.objects.create(name="Org 2", invite_code="blah2")
        org1.users.add(self.user1)
        org2.users.add(self.user1)

        response = self.client.get("/organizations/list_user_orgs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("orgs", response.data)
        self.assertEqual(len(response.data["orgs"]), 2)

    def test_list_clusters_in_organization(self):
        """
        Test that a user can list clusters in an organization they belong to.
        """
        org = Organization.objects.create(name="Test Org", invite_code="blah-2")
        org.users.add(self.user1)

        response = self.client.get(f"/organizations/{org.id}/clusters/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["clusters"]), 0)
