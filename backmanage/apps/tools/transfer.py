# -*- coding: utf-8 -*-
"""各种视图中获取信息"""
__author__ = 'cn.lujianxin@gmail.com'
__time__ = '18-10-18 下午3:21'


def get_objs_by_target(target):
    """通过apply中的target获取对象"""
    from operatorsystem.models import BoxManage, WareHouse, StoreGroup
    from order.models import (
        DiaoHuoOrder,
        BuChaOrder,
        ReturnOrder,
        PurchaseOrder,
        CuXiaoOrder
    )
    import re
    queryset = None
    if re.match(r'^W[0-9]+$', target):
        queryset = WareHouse.objects.filter(number=target)
    elif re.match(r'^B[0-9]+$', target):
        queryset = BoxManage.objects.filter(number=target)
    elif re.match(r'^DQ[0-9]+$', target):
        queryset = StoreGroup.objects.filter(num=target)
    elif re.match(r'^DH[0-9]+$', target):
        queryset = DiaoHuoOrder.objects.filter(num=target)
    elif re.match(r'^BC[0-9]+$', target):
        queryset = BuChaOrder.objects.filter(num=target)
    elif re.match(r'^TH[0-9]+$', target):
        queryset = ReturnOrder.objects.filter(num=target)
    elif re.match(r'^CG[0-9]+$', target):
        queryset = PurchaseOrder.objects.filter(num=target)
    elif re.match(r'^CX[0-9]+$', target):
        queryset = CuXiaoOrder.objects.filter(num=target)
    return queryset


def get_process_by_target(target):
    import re
    from approval.models import (
        TypeProcess,
        Process
    )
    process = None
    target_type = None
    if re.match(r'^W[0-9]+$', target):
        target_type = 'warehouse'
    elif re.match(r'^B[0-9]+$', target):
        target_type = 'box'
    elif re.match(r'^DQ[0-9]+$', target):
        target_type = 'store_group'
    elif re.match(r'^DH[0-9]+$', target):
        target_type = 'diaohuo'
    elif re.match(r'^BC[0-9]+$', target):
        target_type = 'bucha'
    elif re.match(r'^TH[0-9]+$', target):
        target_type = 'return'
    elif re.match(r'^CG[0-9]+$', target):
        target_type = 'purchase'
    elif re.match(r'^CX[0-9]+$', target):
        target_type = 'cuxiao'
    pid = TypeProcess.objects.filter(target_type=target_type).first().process_id
    process = Process.objects.filter(id=pid).first()

    return process


def update_target(target, target_status, **kwargs):
    """更新目标数据的整体状态
    判断数据目标的类型， 然后创建对应的出入库单.
    """
    code = 0
    from django.db.transaction import atomic
    from order.models import ChuKuOrder, RuKuOrder
    from order.baseview import make_order_num
    from order.models import PurchaseOrder, ReturnOrder, DiaoHuoOrder
    with atomic():
        try:
            # 更新目标数据状态
            objects = get_objs_by_target(target)
            objects.update(status=target_status)
            ck_num = make_order_num(ChuKuOrder, 'CK')  # 生成单号
            rk_num = make_order_num(RuKuOrder, 'RK')  # 生成单号
            # 开启事务--------创建伴随出入库单
            obj = objects.first()
            if not obj:
                raise Exception('target not found.')
            if isinstance(obj, PurchaseOrder):
                # 采购单,调货单---创建入库单
                RuKuOrder.objects.get_or_create(
                    num=rk_num,
                    related_order=obj.num,
                    officer_id=kwargs.get('officer_id')
                )
            elif isinstance(obj, ReturnOrder):
                # 退货单，调货单---创建出库单
                ChuKuOrder.objects.get_or_create(
                    num=ck_num,
                    related_order=obj.num,
                    officer_id=kwargs.get('officer_id')
                )
            elif isinstance(obj, DiaoHuoOrder):
                RuKuOrder.objects.get_or_create(
                    num=rk_num,
                    related_order=obj.num,
                    officer_id=kwargs.get('officer_id')
                )
                ChuKuOrder.objects.get_or_create(
                    num=ck_num,
                    related_order=obj.num,
                    officer_id=kwargs.get('officer_id')
                )
            # 其余目标数据状态改变无需伴随创建出入库单
            else:
                pass
        except:
            code = -1
    return code


def update_apply(apply_id, apply_status):
    # 更新申请记录的状态
    from approval.models import Apply
    code = 0
    try:
        Apply.objects.filter(id=apply_id).update(status=apply_status)
    except:
        code = -1
    return code


def apply_allowed_to_set_node(apply_id):
    # 查看审批记录是否允许变更其中的节点状态
    from approval.models import Apply
    apply = Apply.objects.filter(id=apply_id).first()
    if not apply:
        return False
    return apply.status == 0


# 获取门店直接选的结构和店群所有的结构总和
def get_total_sku_for_box(box_id):
    """
    :param box_id: id field of the box;
    :return: skus for box include both box's skus_control and box's_storegroup's skus_control;
    """
    from operatorsystem.models import Group2Sku, Box2Sku, BoxManage
    skus = []
    box = BoxManage.objects.filter(id=box_id).first()
    if not box:
        raise Exception('id:{}门店记录不存在！'.format(box_id))
    # 查找店群所拥有的sku
    skus_group = Group2Sku.objects.filter(group_id=box.store_group.id)
    # 查找门店直接选取的sku
    skus_box = Box2Sku.objects.filter(box_id=box_id)
    # 去重，以门店直接选取为准
    ids = []
    for sku_b in skus_box:
        sku = {}
        sku['small_type_id'] = sku_b.small_type_id
        sku['sku_min'] = sku_b.sku_min
        sku['sku_max'] = sku_b.sku_max
        ids.append(sku['small_type_id'])
        skus.append(sku)
    for sku_g in skus_group:
        sku = {}
        if sku_g.small_type_id not in ids:
            sku['small_type_id'] = sku_g.small_type_id
            sku['sku_min'] = sku_g.sku_min
            sku['sku_max'] = sku_g.sku_max
            ids.append(sku['small_type_id'])
            skus.append(sku)
        continue
    # 返回结果
    return skus


if __name__ == '__main__':
    pass
