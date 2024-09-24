from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import User


class UsersViewSetTest(APITestCase):
    """Test the UsersViewSet API"""

    def setUp(self):
        self.url = reverse("users:users-list")
        self.user_data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_create_user(self):
        """Test creating a user"""
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("membership_id", response.data)
        self.assertIn("enrolled_on", response.data)

        # Verify user is created in the database
        user = User.objects.get(email=self.user_data["email"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])

    def test_create_user_with_auto_generated_membership_id(self):
        """Test that membership_id is auto-generated when creating a user"""
        response = self.client.post(self.url, self.user_data, format="json")

        # Check that the user was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("membership_id", response.data)

        # Check that membership_id is not None or an empty string
        membership_id = response.data.get("membership_id")
        self.assertIsNotNone(membership_id)
        self.assertNotEqual(membership_id, "")

        # Verify the user in the database has the auto-generated membership_id
        user = User.objects.get(email=self.user_data["email"])
        self.assertEqual(user.membership_id, membership_id)

    def test_create_user_with_missing_fields(self):
        """Test creating a user with missing required fields"""
        incomplete_data = {
            "first_name": "Test"
            # Missing 'last_name' and 'email'
        }
        response = self.client.post(self.url, incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("last_name", response.data)
