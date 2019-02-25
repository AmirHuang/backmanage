from django.db import models
from django.contrib.auth.models import AbstractUser


class Permissions(models.Model):
    permission = models.CharField(max_length=100, verbose_name='权限', unique=True, null=False)
    permission_remake = models.CharField('权限备注', max_length=100)

    def __str__(self):
        return self.permission

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        db_table = 'permissions'


class Role(models.Model):
    permission = models.ManyToManyField(Permissions, blank=True, verbose_name='权限')
    role_type = models.CharField(max_length=100, verbose_name='角色种类', unique=True)
    role_remake = models.CharField(max_length=100, verbose_name='角色备注', null=True)

    def __str__(self):
        return self.role_type

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        db_table = 'role'


class Aera(models.Model):
    '''用户区域表'''
    where = models.CharField(max_length=100, verbose_name='区域')

    def __str__(self):
        return self.where

    class Meta:
        verbose_name = '区域'
        verbose_name_plural = verbose_name
        db_table = 'area'


class UserProfile(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=11, verbose_name='电话', null=True)
    role = models.ManyToManyField(to='Role', verbose_name='角色', blank=True)
    area = models.ForeignKey(Aera, verbose_name='所属区域', null=True, blank=True, on_delete=models.SET_NULL)
    superior = models.CharField(max_length=20, verbose_name='上级', help_text='上级', null=True)
    address = models.CharField(max_length=100, verbose_name='地址', null=True)

    class Meta:
        verbose_name = '用户账号'
        verbose_name_plural = verbose_name
        db_table = 'userprofile'


class MemberProfile(models.Model):
    """会员账户"""
    # 基础信息
    num = models.CharField(max_length=11, null=False, blank=False, verbose_name='会员编号', help_text='会员编号',
                           primary_key=True)
    phone = models.CharField(max_length=11, null=False, blank=False, unique=True, verbose_name='手机号', help_text='手机号')
    regist_source = models.CharField(max_length=100, null=False, blank=False, verbose_name='注册来源', help_text='注册来源')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='注册时间', help_text='注册时间')
    # 关联信息
    wechat_id = models.CharField(max_length=32, null=True, verbose_name='微信id', help_text='微信id', unique=True)
    alipay_id = models.CharField(max_length=32, null=True, verbose_name='支付宝id', help_text='支付宝id', unique=True)
    lianhua_id = models.CharField(max_length=32, null=True, verbose_name='联华会员id', help_text='联华会员id', unique=True)
    lianhua_card = models.CharField(max_length=32, null=True, verbose_name='联华会员卡号', help_text='联华会员卡号', unique=True)
    # 身份信息
    user_name = models.CharField(max_length=32, null=True, verbose_name='姓名', help_text='姓名')
    idcard = models.CharField(max_length=18, null=True, verbose_name='身份证', help_text='身份证', unique=True)
    photo = models.ImageField(upload_to='member/', null=True, verbose_name='人像', help_text='人像', unique=True)
    fingerprint = models.CharField(max_length=255, null=True, verbose_name='指纹', help_text='指纹', unique=True)
    # 账户信息
    rank = models.IntegerField(default=0, null=False, verbose_name='会员等级', help_text='会员等级')
    points = models.IntegerField(default=0, null=False, verbose_name='会员积分', help_text='会员积分')
    money = models.FloatField(default=0, null=False, verbose_name='余额', help_text='余额')

    class Meta:
        verbose_name_plural = verbose_name = '会员表'
        db_table = 'memberprofile'

    def __str__(self):
        return self.num
