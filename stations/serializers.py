from .models import ChargeHistory
from rest_framework import serializers


class ChargeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeHistory
        fields = [
            'id',
            'station',
            'service_user',
            'amount',
            'cost',
            'is_delete',
        ]
