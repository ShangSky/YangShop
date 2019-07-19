from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser, BaseModel):
    """
    用户
    """
    avatar = models.ImageField(upload_to='users/avatar/', null=True, max_length=200, verbose_name='用户头像', help_text='用户头像')
    nickname = models.CharField(max_length=30, null=True, blank=True, verbose_name='用户昵称', help_text='用户昵称')
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="male", verbose_name="性别", help_text='性别')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱", help_text='邮箱')
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="个人简介", help_text='个人简介')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Address(BaseModel):
    """地址"""
    user = models.ForeignKey(UserProfile, verbose_name='所属用户', on_delete=models.CASCADE, help_text='所属用户')
    name = models.CharField(max_length=20, verbose_name='收货人姓名', help_text='收货人姓名')
    mobile = models.CharField(max_length=11, verbose_name="收货人电话", help_text='收货人电话')
    province = models.CharField(max_length=10, verbose_name='收件省份', help_text='收件省份')
    city = models.CharField(max_length=10, verbose_name='收件城市', help_text='收件城市')
    area = models.CharField(max_length=10, verbose_name='收件区', help_text='收件区')
    detail_address = models.CharField(max_length=200, verbose_name='详细地址', help_text='详细地址')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
