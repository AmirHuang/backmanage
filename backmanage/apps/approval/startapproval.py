# -*- coding: utf-8 -*-
__author__ = 'lujianxin'
__time__ = '2018/9/6 16:14'

from approval.models import Process, Node, NodeStatus, Apply
from django.db.transaction import atomic
from order.baseview import make_order_num


def get_process_by_obj(obj):
    from approval.models import TypeProcess
    from order.models import (
        BuChaOrder,
        PurchaseOrder,
        ReturnOrder,
        DiaoHuoOrder,
        CuXiaoOrder
    )
    from operatorsystem.models import (
        BoxManage,
        WareHouse,
        StoreGroup
    )
    type = None
    if isinstance(obj, BuChaOrder):
        type = 'bucha'
    elif isinstance(obj, PurchaseOrder):
        type = 'purchase'
    elif isinstance(obj, ReturnOrder):
        type = 'return'
    elif isinstance(obj, DiaoHuoOrder):
        type = 'diaohuo'
    elif isinstance(obj, CuXiaoOrder):
        type = 'cuxiao'
    elif isinstance(obj, BoxManage):
        type = 'box'
    elif isinstance(obj, WareHouse):
        type = 'warehouse'
    elif isinstance(obj, StoreGroup):
        type = 'store_group'
    return TypeProcess.objects.filter(target_type=type).first().process


class StartApproval(object):
    def perform_create(self, serializer):
        from operatorsystem.models import BoxManage, WareHouse
        print('-'*20 + 'perform_create执行了' + '-'*20)
        with atomic():
            a = 1/0
            print(a)
            # try:
            #     a = 1 / 0
            #     print(a)
            # except:
            #     pass


            # try:
            #     instance = serializer.save()
            #     print('--instance:', instance)
            #     target_num = instance.number if isinstance(instance, WareHouse) or isinstance(instance,
            #                                                                                   BoxManage) else instance.num
            #     # 根据审批类型自动生成审批节点状态
            #     # 创建的对象？
            #     print('---serializer.data:', serializer.data)
            #     obj = self.queryset.get(id=serializer.data.get('id'))
            #     print('---obj:', obj)
            #     # print(obj)
            #     # 对象的审批类型以及流程
            #     process = get_process_by_obj(obj)
            #     # 创建一个新的审批申请
            #     apply = Apply.objects.create(
            #         num=make_order_num(model=Apply, start='AP'),
            #         target=target_num,
            #         desc='此申请由创建数据时自动提交.',
            #         create_user_id=self.request.user.id
            #     )
            #     # 每个节点的状态进行初始化
            #     nodes = eval(process.flow)
            #     header = int(nodes.pop(0))
            #     # 头结点初始化
            #     NodeStatus.objects.create(
            #         apply_id=apply.id,
            #         node_id=header,
            #         status='approvaling',
            #     )
            #     # 其余节点的初始化
            #     for node in nodes:
            #         NodeStatus.objects.create(
            #             apply_id=apply.id,
            #             node_id=node,
            #         )
            # except:
            #     pass


if __name__ == '__main__':
    # 2018-09-07 测试成功，插入门店的同时会生成本门店的审批流程，初始化各个节点的状态.
    pass
