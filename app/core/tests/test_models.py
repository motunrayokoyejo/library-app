import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from core.models import Book, Category, Loan, User


class CategoryModelTest(TestCase):
    """Test suite for the Category model"""

    def test_create_category(self):
        """Test creating a category"""
        category = Category.objects.create(name="Fiction")
        self.assertEqual(category.name, "Fiction")
        self.assertEqual(str(category), "Fiction")

    def test_category_ordering(self):
        """Test ordering of categories by name"""
        category1 = Category.objects.create(name="Fantasy")
        category2 = Category.objects.create(name="Biography")
        categories = Category.objects.all()
        self.assertEqual(categories[0], category2)
        self.assertEqual(categories[1], category1)


class BookModelTest(TestCase):
    """Test suite for the Book model"""

    def setUp(self):
        self.category = Category.objects.create(name="Non-Fiction")

    def test_create_book(self):
        """Test creating a book"""
        book = Book.objects.create(
            publisher="Penguin Random House",
            author="George Orwell",
            title="1984",
            description="A dystopian social science fiction novel",
            upload_book=SimpleUploadedFile("1984.pdf", b"file_content"),
            add_to_catalog=True,
        )
        book.category.add(self.category)

        self.assertEqual(book.publisher, "Penguin Random House")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.description, "A dystopian social science fiction novel")
        self.assertTrue(book.add_to_catalog)
        self.assertIn(self.category, book.category.all())
        self.assertEqual(str(book), f"1984 by George Orwell, {book.created_on}")

    def test_book_string_representation(self):
        """Test the string representation of the book model"""
        book = Book.objects.create(
            publisher="HarperCollins",
            author="Aldous Huxley",
            title="Brave New World",
            description="A dystopian science fiction novel",
            upload_book=SimpleUploadedFile("brave_new_world.pdf", b"file_content"),
        )
        book.category.add(self.category)
        self.assertEqual(
            str(book), f"Brave New World by Aldous Huxley, {book.created_on}"
        )

    def test_book_auto_availability(self):
        """Test the default availability of a book"""
        book = Book.objects.create(
            publisher="HarperCollins",
            author="Aldous Huxley",
            title="Brave New World",
            description="A dystopian science fiction novel",
            upload_book=SimpleUploadedFile("brave_new_world.pdf", b"file_content"),
        )
        self.assertTrue(book.is_available)


class UserModelTest(TestCase):
    """Test suite for the User model"""

    def test_create_user_with_auto_generated_membership_id(self):
        """Test creating a user with auto-generated membership_id"""
        user = User.objects.create(
            email="testuser@example.com", first_name="Test", last_name="User"
        )

        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertIsNotNone(user.membership_id)
        self.assertEqual(len(user.membership_id), 8)
        self.assertTrue(user.membership_id.isalnum())

    def test_user_string_representation(self):
        """Test the string representation of the User model"""
        user = User.objects.create(
            email="user@example.com", first_name="John", last_name="Doe"
        )
        self.assertEqual(str(user), f"user@example.com ({user.membership_id})")

    def test_auto_generated_fields(self):
        """Test auto-populated fields like `enrolled_on`"""
        user = User.objects.create(
            email="newuser@example.com", first_name="Jane", last_name="Doe"
        )
        self.assertIsInstance(user.enrolled_on, datetime.datetime)


class LoanModelTest(TestCase):
    """Test suite for the Loan model"""

    def setUp(self):
        self.user = User.objects.create(
            email="borrower@example.com", first_name="Borrower", last_name="User"
        )
        self.book = Book.objects.create(
            publisher="Publisher",
            author="Author Name",
            title="A Great Book",
            description="A great description",
            upload_book=SimpleUploadedFile("book.pdf", b"file_content"),
        )

    def test_create_loan(self):
        """Test creating a loan and setting return due date"""
        loan_duration = 14
        loan = Loan.objects.create(
            borrower=self.user,
            book=self.book,
            borrowed_on=timezone.now(),
            duration_in_days=loan_duration,
        )

        self.book.refresh_from_db()

        expected_due_date = loan.borrowed_on + datetime.timedelta(days=loan_duration)
        self.assertEqual(loan.return_due_date.date(), expected_due_date)
        self.assertFalse(loan.returned_on)
        self.assertFalse(self.book.is_available)

    def test_return_loan(self):
        """Test returning a loan and updating book availability"""
        loan = Loan.objects.create(
            borrower=self.user,
            book=self.book,
            borrowed_on=timezone.now(),
            duration_in_days=7,
        )
        loan.returned_on = timezone.now()
        loan.save()

        self.book.refresh_from_db()
        self.assertTrue(self.book.is_available)

    def test_loan_string_representation(self):
        """Test the string representation of the Loan model"""
        loan = Loan.objects.create(
            borrower=self.user,
            book=self.book,
            borrowed_on=timezone.now(),
            duration_in_days=7,
        )
        self.assertEqual(str(loan), f"A Great Book borrowed by borrower@example.com")
