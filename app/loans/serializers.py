# serializers.py

from rest_framework import serializers

from core.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

    def create(self, validated_data):
        loan = Loan(**validated_data)
        loan.save()
        return loan
