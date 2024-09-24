from rest_framework import serializers

from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Book model serializer"""

    category_names = serializers.SerializerMethodField()

    class Meta(object):
        model = Book
        fields = (
            "id",
            "category_names",
            "publisher",
            "author",
            "title",
            "book_cover",
            "description",
            "upload_book",
            "is_available",
            "created_on",
        )
        read_only_fields = fields

    def get_category_names(self, obj):
        # Return the name of each category related to the book
        return obj.category.values_list("name", flat=True)
