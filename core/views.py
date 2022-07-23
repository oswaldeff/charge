# Create your views here.
from django.db import transaction
from django.contrib.auth.models import User
from accounts.models import ServiceUser
from stations.models import Station
from payments.models import Card
from coupons.models import CouponCategory, Coupon, CouponHistory
from datetime import datetime


@transaction.atomic()
def gen_db():
    service_user = ServiceUser.objects.first()
    if not service_user:
        user = User.objects.create(
            username='홍길동',
            email='홍길동@gmail.com',
            password=0000
        )
        service_user = ServiceUser.objects.create(
            user=user,
            point=5000
        )
        Card.objects.create(
        service_user=service_user,
        number='1234123412341234',
        valid_date='0925',
        cvc='123',
        birth_date='990909',
        password='12',
        is_agreed=True
        )
    station = Station.objects.first()
    if not station:
        Station.objects.create(
            name='강남 역삼2동주민센터 전기차충전소',
            battery_type='LITHIUM-ION',
            state='USEABLE',
            address='서울 강남구 도곡로43길 25',
            lat='37.4958939',
            lng='127.046844',
            price=173.8
        )
    coupon_category = CouponCategory.objects.first()
    if not coupon_category:
        coupon_category = CouponCategory.objects.create(
            label='SIGNUP',
            code=hex(int(datetime.now().strftime('%Y%m%d')))
        )
        coupon = Coupon.objects.create(
            coupon_category=coupon_category,
            code=hex(int(datetime.now().strftime('%Y%m%d%H%M%S'))),
            name='회원가입프로모션',
            point=5000
        )
        CouponHistory.objects.create(
            coupon=coupon,
            service_user=service_user
        )
