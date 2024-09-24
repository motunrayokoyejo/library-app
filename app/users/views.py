from rest_framework import mixins, viewsets

from core.models import User

from . import serializers


class UsersViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):

    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
