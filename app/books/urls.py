from django.urls import include, path
from rest_framework.routers import DefaultRouter

from books import views
from books.apps import BooksConfig

router = DefaultRouter()
router.register("", views.BooksViewSet, basename="books")

app_name = BooksConfig.name

urlpatterns = [path("", include(router.urls))]
