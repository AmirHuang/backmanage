# _*_ coding: utf-8 _*_
# @time     : 2018/12/12
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm


from rest_framework import serializers
from .models import *


class ChildTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildType
        fields = ('id', 'name',)


class SmallTypeSerializer(serializers.ModelSerializer):
    small = ChildTypeSerializer(many=True)

    class Meta:
        model = SmallType
        fields = ('id', 'name', 'small')


class MiddleTypeSerializer(serializers.ModelSerializer):
    middle = SmallTypeSerializer(many=True)

    class Meta:
        model = MiddleType
        fields = ('id', 'name', 'middle')


class BigTypeSerializer(serializers.ModelSerializer):
    bigs = MiddleTypeSerializer(many=True)

    class Meta:
        model = BigType
        fields = ('id', 'name', 'bigs',)


class BigTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BigType
        fields = ('name', 'id')


class MiddleTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddleType
        fields = ('name', 'id')


class SmallTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmallType
        fields = ('name', 'id')


class ChildTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildType
        fields = ('name', 'id')
