from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.http.response import JsonResponse
from . import models
from . import filtersets
from . import serializers
from operatorsystem.views import SetPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = SetPagination
    # 默认serializer
    d_serializer_class = None
    # 查询serializer
    s_serializer_class = None

    def get_serializer_class(self):
        if not self.s_serializer_class or not self.d_serializer_class:
            raise Exception('"d_serializer_class"必须配置!')
        ms = ['list', 'retrieve']
        if self.action in ms:
            return self.s_serializer_class
        return self.d_serializer_class


class NodeViewSet(BaseViewSet):
    """可选审批节点"""
    queryset = models.Node.objects.all()
    d_serializer_class = serializers.NodeSreializer
    s_serializer_class = serializers.NodeDetailSerializer
    filter_class = filtersets.NodeFilterSet


class ProcessViewSet(BaseViewSet):
    """审批流程"""
    queryset = models.Process.objects.all()
    d_serializer_class = serializers.ProcessSerializer
    s_serializer_class = serializers.ProcessDetailSerializer
    filter_class = filtersets.ProcessFilterSet


class NodeStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """数据节点状态只允许查询"""
    queryset = models.NodeStatus.objects.all()
    pagination_class = SetPagination
    filter_class = filtersets.NodeStatusFilterSet
    serializer_class = serializers.NodeStatusDetailSerializer


class TypeProcessViewSet(BaseViewSet):
    """目标类型审批流程关系"""
    queryset = models.TypeProcess.objects.all()
    d_serializer_class = serializers.TypeProcessSerializer
    s_serializer_class = serializers.TypeProcessDetailSerializer
    filter_class = filtersets.TypeProcessFilterSet


class ApplyViewSet(BaseViewSet):
    """审核记录表"""
    queryset = models.Apply.objects.all()
    d_serializer_class = serializers.ApplySerializer
    s_serializer_class = serializers.ApplyDetailSerializer
    filter_class = filtersets.ApplyFilterSet
