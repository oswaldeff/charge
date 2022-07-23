from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from core.models import TimeStampedModel


class ServiceUser(TimeStampedModel):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.DO_NOTHING, verbose_name='유저')
    point = models.PositiveBigIntegerField(default=0, verbose_name='포인트')
    is_delete = models.BooleanField(default=False, verbose_name='삭제')
    
    class Meta:
        ordering = ('-user',)
        verbose_name = '서비스 유저'
        verbose_name_plural = '서비스 유저들'
    
    def __str__(self):
        return f'{self.user}'
