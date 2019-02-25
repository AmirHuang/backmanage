# -*- coding: utf-8 -*-
__author__ = 'lujianxin'
__time__ = '2018/9/13 15:37'

"""获取目标数据的全部节点状态"""

from rest_framework import serializers
from approval.models import NodeStatus, Process, TypeProcess, Apply
from approval.serializers import ApplyDetailSerializer


class WithApplySerializer(serializers.ModelSerializer):
    """目标数据获取apply对象"""
    apply = serializers.SerializerMethodField(read_only=True)

    def get_apply(self, obj):
        from operatorsystem.models import BoxManage, WareHouse
        json = []
        target = obj.number if isinstance(obj, BoxManage) or isinstance(obj, WareHouse) else obj.num
        applys = Apply.objects.filter(target=target)
        if applys:
            for apply in applys:
                apply_json = None
                apply_json = ApplyDetailSerializer(apply).data
                json.append(apply_json)
        return json


if __name__ == '__main__':
    pass
