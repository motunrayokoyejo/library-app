import random
import string
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def generate_membership_id(length=8):
    """Generate a unique membership ID with specified length"""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"


class Book(models.Model):
    category = models.ManyToManyField(Category)
    publisher = models.TextField()
    author = models.TextField()
    title = models.CharField(max_length=100)
    book_cover = models.ImageField(blank=True)
    description = models.TextField()
    upload_book = models.FileField()
    add_to_catalog = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s by %s, %s" % (self.title, self.author, self.created_on)

    class Meta:
        verbose_name = "book"
        verbose_name_plural = "books"


class User(models.Model):
    membership_id = models.CharField(
        max_length=8, unique=True, default=generate_membership_id, editable=False
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.membership_id})"

    class Meta:
        verbose_name = "Library User"
        verbose_name_plural = "Library Users"
        ordering = ["enrolled_on"]


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_on = models.DateField(auto_now_add=True)
    duration_in_days = models.PositiveIntegerField()
    return_due_date = models.DateField(null=True, blank=True)
    returned_on = models.DateField(null=True, blank=True)

    def get_return_due_date(self):
        """Calculate return due date based on borrowed_on date and duration."""
        if self.borrowed_on:
            return self.borrowed_on + timedelta(days=self.duration_in_days)
        else:
            return timezone.now().date() + timedelta(days=self.duration_in_days)

    def save(self, *args, **kwargs):
        """Override save to calculate return_due_date before saving."""
        if not self.pk and not self.book.is_available:
            raise ValidationError("This book is currently unavailable.")

        self.return_due_date = self.get_return_due_date()
        if self.returned_on:
            self.book.is_available = True
        else:
            self.book.is_available = False
        self.book.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.email}"
