from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Book, User


class LoanBookTest(APITestCase):
    """Test the LoanBookView"""

    def setUp(self):
        """Set up the test data"""
        self.user = User.objects.create(
            email="testuser@example.com", first_name="Test", last_name="User"
        )
        self.available_book = Book.objects.create(
            publisher="Publisher",
            author="Author",
            title="Available Book",
            description="A description for available book.",
            add_to_catalog=True,
            is_available=True,
        )
        self.unavailable_book = Book.objects.create(
            publisher="Publisher",
            author="Author",
            title="Unavailable Book",
            description="A description for unavailable book.",
            add_to_catalog=True,
            is_available=False,
        )

    def test_loan_unavailable_book(self):
        """Test that a user cannot loan an unavailable book"""
        url = reverse("loan-book")
        data = {
            "membership_id": self.user.membership_id,
            "book": self.unavailable_book.id,
            "duration_in_days": 14,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "['This book is currently unavailable.']"
        )

    def test_loan_available_book(self):
        """Test loaning an available book"""
        url = reverse("loan-book")
        data = {
            "membership_id": self.user.membership_id,
            "book": self.available_book.id,
            "duration_in_days": 14,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book"], self.available_book.id)
