# _*_ coding: utf-8 _*_
# @time     : 2018/12/13
# @Author   : Amir
# @Site     : 
# @File     : filtersets.py
# @Software : PyCharm

# from django_filters.filterset import FilterSet
from django_filters import filters
from django_filters.rest_framework.filterset import FilterSet

from . import models


class NodeFilterSet(FilterSet):
    """节点查询"""
    node = filters.CharFilter(name='node', lookup_expr='icontains')

    class Meta:
        model = models.Node
        fields = '__all__'


class ProcessFilterSet(FilterSet):
    """流程查询"""
    process = filters.CharFilter(name='process', lookup_expr='icontains')

    class Meta:
        model = models.Process
        fields = '__all__'


class TypeProcessFilterSet(FilterSet):
    """目标类型和流程关系表查询"""
    remark = filters.CharFilter(name='remark', lookup_expr='icontains')

    class Meta:
        model = models.TypeProcess
        fields = '__all__'


class ApplyFilterSet(FilterSet):
    """申请表/审核记录表"""
    desc = filters.CharFilter(name='desc', lookup_expr='icontains')

    class Meta:
        model = models.Apply
        fields = '__all__'


class NodeStatusFilterSet(FilterSet):
    """节点状态"""

    class Meta:
        model = models.NodeStatus
        fields = '__all__'


if __name__ == '__main__':
    pass
