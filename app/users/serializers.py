from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta(object):
        model = User
        fields = (
            "id",
            "membership_id",
            "email",
            "first_name",
            "last_name",
            "enrolled_on",
        )
        read_only_fields = ("id", "membership_id", "enrolled_on")
