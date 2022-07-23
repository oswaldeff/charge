from django.db import models

# Create your models here.
from core.models import TimeStampedModel
from accounts.models import ServiceUser
from payments.models import PaymentHistory


class CouponCategory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    label = models.CharField(
        max_length=100,
        choices=(
            ('SIGNUP', '회원가입발급'),
            ('EVENT', '이벤트발급'),
        ),
        verbose_name='라벨'
    )
    code = models.CharField(max_length=100, verbose_name='코드')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '쿠폰 카테고리'
        verbose_name_plural = '쿠폰 카테고리들'
    
    def __str__(self):
        return f'{self.code}'


class Coupon(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    coupon_category = models.ForeignKey(CouponCategory, on_delete=models.DO_NOTHING, verbose_name='카테고리')
    code = models.CharField(max_length=100, verbose_name='코드')
    name = models.CharField(max_length=100, verbose_name='이름')
    point = models.PositiveBigIntegerField(verbose_name='포인트')
    is_delete = models.BooleanField(default=False, verbose_name='삭제')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '쿠폰'
        verbose_name_plural = '쿠폰들'
    
    def __str__(self):
        return f'{self.coupon_category}{self.code}'


class CouponHistory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    coupon = models.OneToOneField(Coupon, on_delete=models.DO_NOTHING)
    service_user = models.ForeignKey(ServiceUser, on_delete=models.DO_NOTHING, verbose_name='서비스 유저')
    is_delete = models.BooleanField(default=False, verbose_name='삭제')
    
    class Meta:
        ordering = ('-id',)
        verbose_name = '쿠폰 기록'
        verbose_name_plural = '쿠폰 기록들'
    
    def __str__(self):
        return f'{self.id}, {self.coupon}, {self.service_user}'
