from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response

from core.models import Loan, User

from .serializers import LoanSerializer


class LoanBookView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        membership_id = request.data.get("membership_id")
        try:
            user = User.objects.get(membership_id=membership_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        request.data["borrower"] = user.id

        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
