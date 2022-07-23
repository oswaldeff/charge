from django.db import models

# Create your models here.
from core.models import TimeStampedModel
from accounts.models import ServiceUser


class Station(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='이름')
    battery_type = models.CharField(
        max_length=100,
        choices=(
            ('lithium-ion', '리튬이온 배터리'),
            ('nickel-metal', '니켈메탈 배터리'),
        ),
        verbose_name='배터리 타입'
    )
    state = models.CharField(
        max_length=100,
        choices=(
            ('useable', '사용가능'),
            ('occupied', '사용중'),
            ('unuseable', '사용불가능'),
        ),
        verbose_name='상태'
    )
    address = models.CharField(max_length=200, verbose_name='주소')
    lat = models.CharField(max_length=180, verbose_name='위도')
    lng = models.CharField(max_length=180, verbose_name='경도')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='1kw 요금')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '충전소'
        verbose_name_plural = '충전소들'
    
    def __str__(self):
        return f'{self.id}'


class ChargeHistory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, verbose_name='충전소')
    service_user = models.ForeignKey(ServiceUser, on_delete=models.DO_NOTHING, verbose_name='서비스 유저')
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='충전량')
    cost = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='충전비용')
    is_delete = models.BooleanField(default=False, verbose_name='삭제')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '충전 기록'
        verbose_name_plural = '충전 기록들'
    
    def __str__(self):
        return f'{self.id}'
