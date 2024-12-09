from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from deployments.constants import DeploymentPriority, DeploymentStatus
from organizations.models import Organization
from clusters.models import Cluster
from deployments.models import Deployment


class ClusterViewsetTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword2"
        )

        # Create an organization
        self.organization = Organization.objects.create(
            name="Test Organization", invite_code="blah"
        )
        self.organization.users.add(self.user)

        # Create a cluster
        self.cluster_data = {
            "organization_id": self.organization.id,
            "name": "Test Cluster",
            "total_ram": 16,
            "total_cpu": 8,
            "total_gpu": 4,
        }

        # Initialize APIClient
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

    def test_create_cluster_success(self):
        """
        Test that a cluster is created successfully when the user is part of the organization.
        """
        response = self.client.post("/clusters/", self.cluster_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Test Cluster")
        self.assertEqual(response.data["organization"], self.organization.id)

    def test_create_cluster_unauthorized(self):
        """
        Test that an error is returned when a user tries to create a cluster without being part of the organization.
        """
        self.client.login(username="testuser2", password="testpassword2")

        response = self.client.post("/clusters/", self.cluster_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "You are not authorized for this action")

    def test_create_cluster_org_not_found(self):
        """
        Test that an error is returned when the provided organization does not exist.
        """
        invalid_data = self.cluster_data.copy()
        invalid_data["organization_id"] = 9999

        response = self.client.post("/clusters/", invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Organization not found")

    def test_get_deployments_success(self):
        """
        Test that deployments for a cluster are listed correctly.
        """
        cluster = Cluster.objects.create(
            name="Test Cluster",
            organization=self.organization,
            total_ram=32,
            total_cpu=16,
            total_gpu=8,
            available_ram=32,
            available_cpu=16,
            available_gpu=8,
        )
        Deployment.objects.create(
            cluster=cluster,
            name="Test Deployment",
            docker_image_path="blah",
            required_ram=1,
            required_cpu=1,
            required_gpu=1,
            priority=DeploymentPriority.HIGH,
            status=DeploymentStatus.PENDING,
            duration=10,
        )

        response = self.client.get(f"/clusters/{cluster.id}/deployments/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["deployments"]), 1)
        self.assertEqual(response.data["deployments"][0]["name"], "Test Deployment")
