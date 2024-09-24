from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views
from users.apps import UsersConfig

router = DefaultRouter()
router.register("", views.UsersViewSet, basename="users")

app_name = UsersConfig.name

urlpatterns = [path("", include(router.urls))]
