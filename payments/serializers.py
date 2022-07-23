from .models import PointHistory, Payment, PaymentHistory
from rest_framework import serializers


class PointHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointHistory
        fields = [
            'id',
            'service_user',
            'card',
            'cost',
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'service_user',
            'card',
            'pg',
            'method',
        ]


class PointPaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = [
            'id',
            'service_user',
            'receipt_id',
            'point_history',
            'payment',
        ]


class ChargePaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = [
            'id',
            'service_user',
            'receipt_id',
            'charge_history',
            'payment',
            'used_point',
        ]
