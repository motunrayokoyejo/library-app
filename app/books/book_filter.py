from django_filters import rest_framework as django_filters

from core.models import Book


class BookFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="iexact"
    )
    publisher = django_filters.CharFilter(
        field_name="publisher", lookup_expr="icontains"
    )

    class Meta:
        model = Book
        fields = ["category", "publisher"]
