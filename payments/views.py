# Create your views here.
import os
from iamport import Iamport
from requests import request
from accounts.models import ServiceUser
from .models import Card, PointHistory, Payment, PaymentHistory
from .serializers import (
    PointHistorySerializer,
    PaymentSerializer,
    PointPaymentHistorySerializer,
    ChargePaymentHistorySerializer
)
from stations.serializers import ChargeHistorySerializer
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def confirm_payment_by_iamport(self, receipt_id, history, cost):
    iamport = Iamport(
        imp_key=os.environ.get('IAMPORT_REST_API_KEY'),
        imp_secret=os.environ.get('IAMPORT_REST_API_SECRET')
    )
    try:
        response = iamport.find(imp_uid=receipt_id, merchant_uid=history)
        return iamport.is_paid(amount=cost, response=response)
    except (Iamport.ResponseError, Iamport.HttpError):
        return False


class PointListCreateAPIView(ListCreateAPIView):
    # permission_classes = []
    
    def get(self, request, *args, **kwargs):
        '''
        사용: 포인트 충전기록 확인
        '''
        self.serializer_class = PointHistorySerializer
        return self.list(request, *args, **kwargs)
    
    
    def perform_create(self, serializer):
        created_instance = serializer.save()
        return created_instance
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)
    
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'service_user': openapi.Schema(type=openapi.TYPE_STRING, description='"서비스 유저"'),
            'card': openapi.Schema(type=openapi.TYPE_STRING, description='"충전할 결제카드"'),
            'cost': openapi.Schema(type=openapi.TYPE_STRING, description='"충전할 포인트"'),
            'pg': openapi.Schema(type=openapi.TYPE_STRING, description='"pg사"'),
            'receipt_id': openapi.Schema(type=openapi.TYPE_STRING, description='"결제고유번호"'),
            }
        )
    )
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        '''
        사용: 포인트 충전,
        비고: 서비스 유저 및 등록카드는 임시할당,
        프로세스: 
            1. 유저는 simple jwt인증 or 쿠키로부터 획득,
            2. front에서 사용자가 포인트 충전할 카드선택,
            3. 충전할 포인트 선택
        '''
        request.data['method'] = 'pre' # 선불
        
        created_instances = []
        serializers = [PaymentSerializer, PointHistorySerializer, PointPaymentHistorySerializer]
        for idx, serializer in enumerate(serializers):
            self.serializer_class = serializer
            created_instance = self.create(request, *args, **kwargs)
            created_instances.append(created_instance)
            if idx == 0:
                request.data['payment'] = created_instance.id
            elif idx == 1:
                ServiceUser.objects.filter(user=int(request.data['service_user'])).update(point=F('point')+int(request.data['cost']))
                request.data['point_history'] = created_instance.id
            else:
                if confirm_payment_by_iamport(self, request.data['receipt_id'], request.data['point_history'], int(request.data['cost'])):
                    created_instance.update(state='paid')
                    return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'FAIL'}, status=status.HTTP_400_BAD_REQUEST)


class ChargeListCreateAPIView(ListCreateAPIView):
    # permission_classes = []
    
    def get(self, request, *args, **kwargs):
        '''
        사용: 전기차 충전기록 확인
        '''
        self.serializer_class = ChargeHistorySerializer
        return self.list(request, *args, **kwargs)
    
    
    def perform_create(self, serializer):
        created_instance = serializer.save()
        return created_instance
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)
    
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'station': openapi.Schema(type=openapi.TYPE_STRING, description='"충전소"'),
            'service_user': openapi.Schema(type=openapi.TYPE_STRING, description='"서비스 유저"'),
            'amount': openapi.Schema(type=openapi.TYPE_STRING, description='"충전량"'),
            'card': openapi.Schema(type=openapi.TYPE_STRING, description='"충전할 결제카드"'),
            'pg': openapi.Schema(type=openapi.TYPE_STRING, description='"pg사"'),
            'method': openapi.Schema(type=openapi.TYPE_STRING, description='"결제방법"'),
            'cost': openapi.Schema(type=openapi.TYPE_STRING, description='"충전비용"'),
            'receipt_id': openapi.Schema(type=openapi.TYPE_STRING, description='"결제고유번호"'),
            'payment': openapi.Schema(type=openapi.TYPE_STRING, description='"결제"'),
            'charge_history': openapi.Schema(type=openapi.TYPE_STRING, description='"충전 기록"'),
            'used_point': openapi.Schema(type=openapi.TYPE_STRING, description='"사용 포인트"'),
            }
        )
    )
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        '''
        사용: 충전소 이용에 대한 결제,
        비고: 서비스 유저 및 등록카드는 임시할당,
        프로세스: 
            1. 유저는 simple jwt인증 or 쿠키로부터 획득,
            2. front에서 사용자가 선불/후불에 따른 시나리오 선택,
        '''
        
        serializers = [PaymentSerializer, ChargeHistorySerializer, ChargePaymentHistorySerializer]
        for idx, serializer in enumerate(serializers):
            self.serializer_class = serializer
            created_instance = self.create(request, *args, **kwargs)
            if idx == 0:
                request.data['payment'] = created_instance.id
            elif idx == 1:
                ServiceUser.objects.filter(user=int(request.data['service_user'])).update(point=F('point')-int(request.data['cost']))
                request.data['charge_history'] = created_instance.id
            else:
                if confirm_payment_by_iamport(request.data['receipt_id'], request.data['charge_history'], int(request.data['cost'])):
                    created_instance.update(state='paid')
                    return Response({'message': 'SUCCESSFULLY CREATE DATA'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'DATA CREATION FAIL'}, status=status.HTTP_400_BAD_REQUEST)
