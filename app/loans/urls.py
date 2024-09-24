# urls.py

from django.urls import path

from .views import LoanBookView

urlpatterns = [
    path("loan/", LoanBookView.as_view(), name="loan-book"),
]
