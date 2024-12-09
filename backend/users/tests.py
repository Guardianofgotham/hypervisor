from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserViewSetTests(APITestCase):
    def test_create_user(self):
        """
        Test that a user can be created successfully.
        """
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(
            "/users/", data, format="json"
        )  # Assuming 'users/' is the correct URL for creating users
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], data["username"])

    def test_create_user_invalid_data(self):
        """
        Test creating a user with invalid data.
        """
        data = {"username": "", "password": "testpassword123"}
        response = self.client.post("/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_invalid_credentials(self):
        """
        Test logging in with invalid credentials.
        """
        data = {"username": "wronguser", "password": "wrongpassword"}
        response = self.client.post("/users/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid credentials")
