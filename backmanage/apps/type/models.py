# coding=utf-8
from django.db import models


# Create your models here.
class BigType(models.Model):
    code = models.CharField(max_length=100, verbose_name='大类代码')
    name = models.CharField(max_length=100, verbose_name='大类名称')

    class Meta:
        verbose_name = '大类类型'
        verbose_name_plural = verbose_name
        db_table = 'bigtype'

    def __str__(self):
        return self.name


class MiddleType(models.Model):
    code = models.CharField(max_length=100, verbose_name='中类代码')
    name = models.CharField(max_length=100, verbose_name='中类名称')
    big = models.ForeignKey(BigType, related_name='bigs', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '中类类型'
        verbose_name_plural = verbose_name
        db_table = 'middletype'

    def __str__(self):
        return self.name


class SmallType(models.Model):
    code = models.CharField(max_length=100, verbose_name='小类代码')
    name = models.CharField(max_length=100, verbose_name='小类名称')
    middle = models.ForeignKey(MiddleType, related_name='middle', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '小类类型'
        verbose_name_plural = verbose_name
        db_table = 'smalltype'

    def __str__(self):
        return self.name


class ChildType(models.Model):
    code = models.CharField(max_length=100, verbose_name='子类代码')
    name = models.CharField(max_length=100, verbose_name='子类名称')
    small = models.ForeignKey(SmallType, related_name='small', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '子类类型'
        verbose_name_plural = verbose_name
        db_table = 'childtype'

    def __str__(self):
        return self.name
