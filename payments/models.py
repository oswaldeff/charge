from django.db import models

# Create your models here.
from core.models import TimeStampedModel
from accounts.models import ServiceUser
from stations.models import ChargeHistory


class Card(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, verbose_name='서비스 유저')
    number = models.CharField(max_length=16, verbose_name='카드번호 16자리')
    valid_date = models.CharField(max_length=4, verbose_name='유효기간 4자리(MM/YY)')
    cvc = models.CharField(max_length=3, verbose_name='보안코드 3자리')
    birth_date = models.CharField(max_length=6, verbose_name='생년월일 6자리')
    password = models.CharField(max_length=2, verbose_name='비밀번호 앞 2자리')
    is_agreed = models.BooleanField(verbose_name='개인정보 제공 동의')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '카드'
        verbose_name_plural = '카드들'
    
    def __str__(self):
        return f'{self.id}'


class PointHistory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    service_user = models.ForeignKey(ServiceUser, on_delete=models.DO_NOTHING, verbose_name='서비스 유저')
    card = models.ForeignKey(Card, on_delete=models.DO_NOTHING, verbose_name='결제카드')
    cost = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='포인트 충전금액')
    is_delete = models.BooleanField(default=False, verbose_name='삭제')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '포인트 충전기록'
        verbose_name_plural = '포인트 충전기록들'
    
    def __str__(self):
        return f'{self.id}'


class Payment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    service_user = models.CharField(max_length=255, verbose_name='서비스 유저')
    card = models.ForeignKey(Card, on_delete=models.DO_NOTHING, verbose_name='결제카드')
    pg = models.CharField(max_length=100, verbose_name='pg사') # pay_method는 신용카드로 default
    method = models.CharField(
        max_length=100,
        choices=(
            ('pre', '선불'),
            ('deferred', '후불'),
        ),
        verbose_name='결제방법'
    )
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '결제'
        verbose_name_plural = '결제들'
    
    def __str__(self):
        return f'{self.id}'


class PaymentHistory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    service_user = models.ForeignKey(ServiceUser, on_delete=models.DO_NOTHING, verbose_name='서비스 유저')
    receipt_id = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='결제번호')
    point_history = models.ForeignKey(PointHistory, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='포인트 기록')
    charge_history = models.ForeignKey(ChargeHistory, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='충전 기록')
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, verbose_name='결제')
    used_point = models.PositiveBigIntegerField(blank=True, null=True, default=None, verbose_name='사용 포인트')
    state = models.CharField(
        max_length=100,
        default='ready',
        choices=(
            ('ready', '결제대기'),
            ('paid', '결제완료'),
            ('failed', '결제실패')
        ),
        verbose_name='결제방법'
    )
    is_delete = models.BooleanField(default=False, verbose_name='삭제')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '결제 기록'
        verbose_name_plural = '결제 기록들'
    
    def __str__(self):
        return f'{self.id}'
