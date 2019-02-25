# conding=utf-8
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from django.http import HttpResponse
from operatorsystem.models import Group2Sku


class TypeViewSet(viewsets.ModelViewSet):
    queryset = BigType.objects.all()
    serializer_class = BigTypeSerializer


class SmallViewSet(viewsets.ModelViewSet):
    queryset = SmallType.objects.all()
    serializer_class = SmallTypeSerializer

    # 感觉此处会报错，因为当sid为空，这里没有返回值。
    def get_queryset(self):
        data = self.request.query_params
        sid = data.get('sid')
        small_id = []
        if sid:
            groupList = Group2Sku.objects.filter(group=sid)
            for group in groupList:
                print('---group.small_type.id:', group.small_type.id)
                small_id.append(group.small_type.id)
            print('--small_id:', small_id)
            smalls = SmallType.objects.exclude(id__in=small_id)
            return smalls