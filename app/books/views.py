from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, viewsets

from books.book_filter import BookFilter
from core.models import Book

from . import serializers


class BooksViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.filter(add_to_catalog=True, is_available=True)
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = BookFilter
    ordering_fields = "__all__"
    ordering = ["created_on"]
