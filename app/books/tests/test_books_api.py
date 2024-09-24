from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Book, Category


class BooksViewSetTest(APITestCase):
    """Test the BooksViewSet"""

    def setUp(self):
        """Set up the test data"""
        self.category1 = Category.objects.create(name="Fiction")
        self.category2 = Category.objects.create(name="Non-Fiction")

        self.book1 = Book.objects.create(
            publisher="Publisher 1",
            author="Author 1",
            title="Book 1",
            description="Description for book 1",
            add_to_catalog=True,
            is_available=True,
        )
        self.book1.category.add(self.category1, self.category2)

        self.book2 = Book.objects.create(
            publisher="Publisher 2",
            author="Author 2",
            title="Book 2",
            description="Description for book 2",
            add_to_catalog=False,
            is_available=True,
        )
        self.book2.category.add(self.category1)

        self.book3 = Book.objects.create(
            publisher="Publisher 3",
            author="Author 3",
            title="Book 3",
            description="Description for book 3",
            add_to_catalog=True,
            is_available=False,
        )
        self.book3.category.add(self.category2)

    def test_list_books(self):
        """Test listing books"""
        url = reverse("books:books-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        book = response.data[0]
        self.assertIn("id", book)
        self.assertIn("category_names", book)
        self.assertIn("publisher", book)
        self.assertIn("author", book)
        self.assertIn("title", book)
        self.assertIn("description", book)

        self.assertEqual(book["title"], "Book 1")

    def test_retrieve_book(self):
        """Test retrieving a single book"""
        url = reverse("books:books-detail", args=[self.book1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.id)
        self.assertEqual(response.data["publisher"], self.book1.publisher)
        self.assertEqual(response.data["author"], self.book1.author)
        self.assertEqual(response.data["title"], self.book1.title)
        self.assertEqual(response.data["description"], self.book1.description)

        url = reverse("books:books-detail", args=[self.book2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse("books:books-detail", args=[self.book3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_books_by_category(self):
        """Test filtering books by category"""
        url = reverse("books:books-list")
        response = self.client.get(url, {"category": self.category1.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book 1")

    def test_filter_books_by_publisher(self):
        """Test filtering books by publisher"""
        url = reverse("books:books-list")
        response = self.client.get(url, {"publisher": "Publisher 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book 1")
