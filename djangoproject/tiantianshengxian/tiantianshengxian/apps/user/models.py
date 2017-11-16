from django.db import models
from db.base import BaseModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, BaseModel):
    '''用户的模型类'''

    class Meta:
        db_table = 'tt_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Address(BaseModel):
    recv_name = models.CharField(max_length=20, verbose_name='收件人')
    recv_address = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='手机')
    user = models.ForeignKey('User', verbose_name='用户ID')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    class Meta:
        db_table = 'tt_address'
        verbose_name = '地址表'
        verbose_name_plural = verbose_name
