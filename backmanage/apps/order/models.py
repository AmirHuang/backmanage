from django.db import models
# Create your models here.
from operatorsystem.models import BoxManage
from operatorsystem.models import GoodsManage, Supplier, Group2Price
from users.models import UserProfile
from operatorsystem.models import WareHouse, SupplierGoodsManage
from users.models import MemberProfile
from approval.models import Process
import datetime


def three_days_next():
    this = datetime.datetime.now()
    three_days_next = this + datetime.timedelta(days=3)
    return three_days_next


class PurchaseOrder(models.Model):
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭'),
        (4, '已发货'),
        (5, '部分完成'),
        (6, '已完成')
    )
    recv_types = (
        (0, '仓库'),
        (1, '门店')
    )
    # 采购单选定供应商之后，应当只能从供应商拥有的商品集合中选择要采购的商品
    # 一张采购单，对应多个商品，多个数量，through参数可以允许自己添加g_id,p_id之外的字段到中间表
    num = models.CharField(max_length=14, verbose_name='采购单号', unique=True, null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, auto_created=True, verbose_name='采购单创建时间')
    create_user = models.ForeignKey(to=UserProfile, verbose_name='采购单发起人', on_delete=models.SET_NULL, blank=True,
                                    null=True)
    expire_time = models.DateTimeField(default=three_days_next, auto_created=True, verbose_name='有效时间',
                                       help_text='有效时间')
    finish_time = models.DateTimeField(verbose_name='实际完成时间', help_text='实际完成时间', null=True, blank=True)
    goods = models.ManyToManyField(to=GoodsManage, through='Order2Goods', verbose_name='货物')
    recv_id = models.IntegerField(null=False, blank=False, verbose_name='入库点id', help_text='入库点id')
    recv_type = models.IntegerField(choices=recv_types, default=0, null=False, blank=False, verbose_name='入库类型',
                                    help_text='入库类型')
    supplier = models.ForeignKey(to=Supplier, verbose_name='供应商', on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.CharField(max_length=100, blank=True, null=True, verbose_name='备注', help_text='备注')
    status = models.IntegerField(choices=statuses, default=0, verbose_name='审核状态', help_text='审核状态')

    class Meta:
        verbose_name = '采购单'
        verbose_name_plural = verbose_name
        db_table = 'purchase_order'

    def __str__(self):
        return self.num


# 给goods和purchaseorder中间表添加额外字段
class Order2Goods(models.Model):
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_cg', on_delete=models.SET_NULL,
                              verbose_name='商品id', blank=True, null=True)
    order = models.ForeignKey(to=PurchaseOrder, on_delete=models.CASCADE,
                              verbose_name='采购单id', blank=True, null=True)
    goods_num = models.IntegerField(verbose_name='交易商品数量')

    class Meta:
        verbose_name = '采购单商品中间表'
        verbose_name_plural = verbose_name
        unique_together = (('goods', 'order'),)
        db_table = 'order2goods'

    def __str__(self):
        return self.goods_num, self.goods.name, self.order.num


class DiaoHuoOrder(models.Model):
    """
    调货单： 仓库，门店之间， 门店，门店之间， 仓库，仓库之间调拨
    """
    types = (
        (0, '店到店'),
        (1, '店到仓'),
        (2, '仓到仓'),
        (3, '仓到店')
    )
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭'),
        (4, '待出库'),
        (5, '待入库'),
        (6, '部分完成'),
        (7, '已完成')
    )
    num = models.CharField(max_length=14, blank=False, null=True, unique=True, verbose_name='单号', help_text='单号')
    create_user = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, related_name='dh_orders', null=True,
                                    verbose_name='发起人', help_text='发起人')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='创建时间', help_text='创建时间')
    expire_time = models.DateTimeField(verbose_name='有效时间', help_text='有效时间', null=True)
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间', help_text='完成时间')
    goods = models.ManyToManyField(to=GoodsManage, through='DiaoHuo2Goods')
    type = models.IntegerField(choices=types, null=False, blank=False, default=2, verbose_name='调拨方式', help_text='调拨方式')
    from_id = models.IntegerField(null=False, blank=False, verbose_name='出库点', help_text='出库点')
    to_id = models.IntegerField(null=False, blank=False, verbose_name='入库点', help_text='入库点')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='备注', help_text='备注')
    status = models.IntegerField(choices=statuses, default=0, verbose_name='审核状态', help_text='审核状态')

    class Meta:
        verbose_name = '调货单'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
        db_table = 'diaohuo_order'

    def __str__(self):
        return self.num


class DiaoHuo2Goods(models.Model):
    """调货单所含商品详情页"""
    order = models.ForeignKey(to=DiaoHuoOrder, on_delete=models.CASCADE, null=False, help_text='所属订单',
                              verbose_name='所属订单')
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_dh', on_delete=models.SET_NULL, null=True,
                              verbose_name='商品', help_text='商品')
    goods_num = models.IntegerField(default=1, null=False, blank=False, verbose_name='数量', help_text='数量')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源采购单',
                               help_text='来源采购单')

    class Meta:
        verbose_name = '调货单商品表'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        unique_together = (('order', 'goods', 'source'),)
        db_table = 'diaohuo2goods'

    def __str__(self):
        return self.order.num, self.goods.name


class SaleOrder(models.Model):
    """销售单"""
    statuses = (
        (0, '已完成'),
        (1, '已失效'),
        (2, '已退货'),
        (3, '部分退货')
    )
    num = models.CharField(max_length=16, null=True, blank=False, unique=True, verbose_name='单号', help_text='单号')
    create_time = models.DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name='创建时间',
                                       help_text='创建时间')
    money = models.FloatField(blank=False, null=False, verbose_name='支付金额', help_text='支付金额')
    payments = models.CharField(max_length=20, null=False, blank=False, verbose_name='支付方式', help_text='支付方式')
    pay_time = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='支付时间', help_text='支付时间')
    finish_time = models.DateTimeField(blank=True, null=True, verbose_name='完成时间', help_text='完成时间')
    member = models.ForeignKey(to=MemberProfile, on_delete=models.SET_NULL, null=True, verbose_name='会员',
                               help_text='会员')
    box = models.ForeignKey(to=BoxManage, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='门店',
                            help_text='门店')
    goods = models.ManyToManyField(to=GoodsManage, through='Sale2Goods', verbose_name='订单中的商品', help_text='订单中的商品')
    status = models.IntegerField(choices=statuses, default=0, verbose_name='状态', help_text='状态')

    class Meta:
        verbose_name = '销售单'
        verbose_name_plural = verbose_name
        db_table = 'sale_order'

    def __str__(self):
        return self.num


class Sale2Goods(models.Model):
    """销售单商品中间表"""
    order = models.ForeignKey(to=SaleOrder, on_delete=models.CASCADE, verbose_name='销售单',
                              help_text='销售单')
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_sl', on_delete=models.SET_NULL, null=True,
                              verbose_name='商品', help_text='商品')
    goods_num = models.IntegerField(null=False, blank=False, verbose_name='商品数量', help_text='商品数量')
    is_discount = models.BooleanField(default=False, null=False, verbose_name='促销标记', help_text='促销标记')
    include_tax_cg_price = models.FloatField(null=False, blank=False, verbose_name='含税进价', help_text='含税进价')
    include_tax_sl_price = models.FloatField(null=False, blank=False, verbose_name='含税售价', help_text='含税售价')
    except_tax_cg_price = models.FloatField(null=False, blank=False, verbose_name='不含税进价', help_text='不含税进价')
    except_tax_sl_price = models.FloatField(null=False, blank=False, verbose_name='不含税售价', help_text='不含税售价')
    profit = models.FloatField(null=False, blank=False, verbose_name='毛利额', help_text='毛利额')
    profit_rate = models.FloatField(null=False, blank=False, verbose_name='毛利率', help_text='毛利率')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源采购单',
                               help_text='来源采购单')

    class Meta:
        verbose_name = '销售单商品表'
        verbose_name_plural = verbose_name
        unique_together = (('order', 'goods', 'source'),)
        db_table = 'sale2goods'

    def __str__(self):
        return self.order.num, self.goods.name, self.goods_num


# -----------------------------------------------------------
#     lujianxin 2018-07-25 退货单
# -----------------------------------------------------------
# 退货单, 绑定仓库，供应商即可创建
class ReturnOrder(models.Model):
    # 退货单绑定仓库和供应商
    send_types = (
        (0, '仓库'),
        (1, '门店')
    )
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭'),
        (4, '已发货'),
        (5, '部分完成'),
        (6, '已完成')
    )
    goods = models.ManyToManyField(to=GoodsManage, through='ReturnOrder2Goods', verbose_name='商品', help_text='商品')
    send_id = models.IntegerField(null=False, blank=False, verbose_name='出库点id', help_text='出库点id')
    send_type = models.IntegerField(default=0, choices=send_types, null=False, blank=False, verbose_name='出库类型',
                                    help_text='出库类型')
    supplier = models.ForeignKey(to=Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='供应商',
                                 help_text='供应商')
    num = models.CharField(max_length=14, verbose_name='退货单号', help_text='退货单号', blank=False, null=True, unique=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间', auto_created=True)
    expire_time = models.DateTimeField(auto_created=True, default=three_days_next, verbose_name='有效时间',
                                       help_text='有效时间')
    finish_time = models.DateTimeField(verbose_name='完成时间', help_text='完成时间', blank=True, null=True)
    create_user = models.ForeignKey(to=UserProfile, verbose_name='创建者', help_text='创建者', on_delete=models.SET_NULL,
                                    null=True, blank=True)
    status = models.IntegerField(choices=statuses, default=0, null=False, verbose_name='审核状态', help_text='审核状态')

    class Meta:
        verbose_name = '退货单'
        verbose_name_plural = verbose_name
        db_table = 'return_order'

    def __str__(self):
        return self.num


class ReturnOrder2Goods(models.Model):
    # 退货单和商品中间表
    order = models.ForeignKey(to=ReturnOrder, verbose_name='退货单', help_text='退货单',
                              on_delete=models.CASCADE, null=True, blank=True)
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_rt', verbose_name='商品', help_text='商品',
                              on_delete=models.SET_NULL, null=True,
                              blank=True)
    goods_num = models.IntegerField(verbose_name='退货数量', help_text='退货数量', null=False, blank=False)
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源采购单',
                               help_text='来源采购单')
    remark = models.CharField(max_length=30, verbose_name='退货备注', help_text='退货备注', default="")

    class Meta:
        verbose_name = '退货商品中间表'
        verbose_name_plural = verbose_name
        db_table = 'returnorder2goods'

    def __str__(self):
        return self.order.num, self.goods.name, self.goods_num


# -------------------------------------------------华丽丽的分割线--------------------------------------------------------
"""出库单和入库单不在自己拥有和商品的中间表，他的商品情况和来源单共享"""


class RuKuOrder(models.Model):
    # 入库单, 对应采购单，调拨单
    status_choices = (
        (0, '待出库'),
        (1, '在途'),
        (2, '部分完成'),
        (3, '已完成')
    )
    related_order = models.CharField(max_length=30, null=False, blank=False, verbose_name='对应单据', help_text='对应单据')
    num = models.CharField(max_length=14, unique=True, null=True, verbose_name='入库单号', help_text='入库单号')
    create_time = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    finish_time = models.DateTimeField(verbose_name='完成时间', help_text='完成时间', blank=True, null=True)
    officer = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='负责人',
                                help_text='负责人')
    remark = models.CharField(max_length=100, blank=True, null=True, verbose_name='备注', help_text='备注')
    status = models.IntegerField(choices=status_choices, default=0)

    class Meta:
        verbose_name = '入库单'
        verbose_name_plural = verbose_name
        db_table = 'ruku_order'

    def __str__(self):
        return self.num, self.status


# 出库单，对应退货单，调拨单， 可分批完成
class ChuKuOrder(models.Model):
    status_choices = (
        (0, '待分拣'),
        (1, '待出库'),
        (2, '在途'),
        (3, '完成')
    )
    num = models.CharField(max_length=14, unique=True, null=True, verbose_name='退货出库单号', help_text='退货出库单号')
    create_time = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    finish_time = models.DateTimeField(blank=True, null=True, verbose_name='完成时间', help_text='完成时间')
    related_order = models.CharField(max_length=30, null=False, blank=False, verbose_name='对应退货单', help_text='对应退货单')
    officer = models.ForeignKey(to=UserProfile, related_name='r_order', on_delete=models.SET_NULL, null=True,
                                verbose_name='负责人', help_text='负责人')
    remark = models.CharField(max_length=100, blank=True, null=True, verbose_name='备注', help_text='备注')
    status = models.IntegerField(choices=status_choices, default=0)

    class Meta:
        verbose_name = '出库单'
        verbose_name_plural = verbose_name
        db_table = 'chuku_order'

    def __str__(self):
        return self.num, self.status


"""出库单和入库单不再自己拥有和商品的中间表，他的商品情况和来源单共享"""


# -------------------------------------------------华丽丽的分割线--------------------------------------------------------

# --------------------------------------------
#     lujianxin   2018-08-24  盘点单，损益单
# --------------------------------------------


class PanDianOrder(models.Model):
    """盘点单"""
    types = (
        (0, '仓库'),
        (1, '门店')
    )
    statuses = [
        (0, '审批中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭'),
    ]
    num = models.CharField(max_length=32, unique=True, null=True, blank=False, verbose_name='盘点单号', help_text='盘点单号')
    pduser = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='盘点人',
                               help_text='盘点人')
    target = models.IntegerField(null=False, blank=False, verbose_name='盘点目标', help_text='盘点目标')
    type = models.IntegerField(choices=types, null=False, blank=False, verbose_name='盘点对象类型', help_text='盘点对象类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间', help_text='完成时间')
    goods = models.ManyToManyField(to=GoodsManage, through='PanDian2Goods', verbose_name='商品', help_text='商品')
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注', help_text='备注')
    status = models.IntegerField(choices=statuses, default=0, null=False, blank=False, verbose_name='状态',
                                 help_text='状态')

    class Meta:
        verbose_name = verbose_name_plural = '盘点单'
        db_table = 'pandian_order'

    def __str__(self):
        return self.num


# --------------------------------------------
#     lujianxin   2018-08-27  盘点损益
# --------------------------------------------

class PanDian2Goods(models.Model):
    """盘点单商品中间表"""
    order = models.ForeignKey(to=PanDianOrder, on_delete=models.CASCADE, verbose_name='盘点单',
                              help_text='盘点单')
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_pd', on_delete=models.SET_NULL, null=True,
                              verbose_name='商品', help_text='商品')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源采购单',
                               help_text='来源采购单')
    goods_num = models.IntegerField(null=False, blank=False, verbose_name='盘点数量', help_text='盘点数量')

    class Meta:
        verbose_name_plural = verbose_name = '盘点单商品中间表'
        db_table = 'pandian2goods'

    def __str__(self):
        return self.order.num, self.goods.name, self.goods_num


class SunYiOrder(models.Model):
    """损益单"""
    num = models.CharField(max_length=32, null=True, blank=False, unique=True, verbose_name='损益单号', help_text='损益单号')
    goods = models.ManyToManyField(to=GoodsManage, through='SunYi2Goods')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='创建时间', help_text='创建时间')
    pdorder = models.ForeignKey(to=PanDianOrder, null=False, on_delete=models.CASCADE, verbose_name='盘点单',
                                help_text='盘点单')

    class Meta:
        verbose_name_plural = verbose_name = '损益单'
        db_table = 'sunyi_order'

    def __str__(self):
        return self.num


class SunYi2Goods(models.Model):
    """损益单商品中间表"""
    order = models.ForeignKey(to=SunYiOrder, on_delete=models.CASCADE, verbose_name='损益单',
                              help_text='损益单')
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_sy', on_delete=models.SET_NULL, null=True,
                              verbose_name='商品', help_text='商品')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源采购单',
                               help_text='来源采购单')
    ex_num = models.IntegerField(null=False, blank=False, verbose_name='差异数量', help_text='差异数量')

    class Meta:
        verbose_name_plural = verbose_name = '损益商品中间表'
        db_table = 'sunyi2goods'

    def __str__(self):
        return self.order.num, self.goods.name, self.ex_num


# -------------------------------------------------------------------------
#     lujianxin   2018-09-04  促销，补差
# -------------------------------------------------------------------------


class CuXiaoOrder(models.Model):
    """促销单"""
    schemes = (
        (0, '前台让利'),
        (1, '后台补差')
    )
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭')
    )
    num = models.CharField(max_length=14, null=True, verbose_name='单号', help_text='单号')
    create_user = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='发起人',
                                    help_text='发起人')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='创建时间', help_text='创建时间')
    start_time = models.DateTimeField(null=True, verbose_name='促销开始时间', help_text='促销开始时间')
    end_time = models.DateTimeField(null=False, verbose_name='促销结束时间', help_text='促销结束时间')
    scheme = models.IntegerField(choices=schemes, default=1, null=False, verbose_name='促销形式', help_text='促销形式')
    box = models.ManyToManyField(to=BoxManage, verbose_name='门店', help_text='门店')
    goods = models.ManyToManyField(to=GoodsManage, verbose_name='商品', help_text='商品')
    remark = models.CharField(max_length=100, null=True, verbose_name='备注', help_text='备注')
    status = models.IntegerField(default=0, choices=statuses, null=False, verbose_name='审核状态', help_text='审核状态')

    class Meta:
        verbose_name_plural = verbose_name = '促销单'
        db_table = 'cuxiao_order'

    def __str__(self):
        return self.num


class CuXiao2Goods(models.Model):
    """促销单商品中间表"""
    order = models.ForeignKey(to=CuXiaoOrder, on_delete=models.CASCADE, verbose_name='促销单', help_text='促销单')
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_cx', on_delete=models.SET_NULL, null=True,
                              verbose_name='商品', help_text='商品')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源采购单',
                               help_text='来源采购单')
    except_tax_cg_price = models.FloatField(null=False, verbose_name='不含税进价', help_text='不含税进价')
    include_tax_cg_price = models.FloatField(null=False, verbose_name='含税进价', help_text='含税进价')
    except_tax_sl_price = models.FloatField(null=False, verbose_name='不含税售价', help_text='不含税售价')
    include_tax_sl_price = models.FloatField(null=False, verbose_name='含税售价', help_text='含税售价')
    profit = models.FloatField(null=False, verbose_name='毛利额', help_text='毛利额')
    profit_rate = models.FloatField(null=False, verbose_name='毛利率', help_text='毛利率')

    class Meta:
        verbose_name_plural = verbose_name = '促销商品中间表'
        db_table = 'cuxiao2goods'

    def __str__(self):
        return self.order.num, self.goods.name


class BuChaOrder(models.Model):
    """促销补差单"""
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭'),
        (4, '待结算'),
        (5, '已结算'),
    )
    num = models.CharField(max_length=14, null=True, verbose_name='单号', help_text='单号')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='创建时间', help_text='创建时间')
    supplier = models.ForeignKey(to=Supplier, on_delete=models.SET_NULL, null=True, verbose_name='供应商', help_text='供应商')
    goods = models.ManyToManyField(to=GoodsManage, through='BuCha2Goods')
    input_time = models.DateTimeField(null=False, verbose_name='进货时间', help_text='进货时间')
    cxorder = models.ForeignKey(to=CuXiaoOrder, on_delete=models.SET_NULL, null=True, verbose_name='促销单',
                                help_text='促销单')
    remark = models.CharField(max_length=100, null=True, verbose_name='备注', help_text='备注')
    status = models.IntegerField(choices=statuses, default=0, null=False, verbose_name='审核状态', help_text='审核状态')

    class Meta:
        verbose_name_plural = verbose_name = '补差单'
        db_table = 'bucha_order'

    def __str__(self):
        return self.num


class BuCha2Goods(models.Model):
    """补差商品中间表"""
    order = models.ForeignKey(to=BuChaOrder, on_delete=models.CASCADE, verbose_name='补差单', help_text='补差单')
    goods = models.ForeignKey(to=GoodsManage, related_name='goods_in_bc', on_delete=models.SET_NULL, null=True,
                              verbose_name='商品', help_text='商品')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源采购单',
                               help_text='来源采购单')
    goods_num = models.IntegerField(null=False, verbose_name='销售数量', help_text='销售数量')
    bcprice = models.FloatField(null=False, verbose_name='补差金额', help_text='补差金额')

    class Meta:
        verbose_name_plural = verbose_name = '补差商品'
        db_table = 'bucha2goods'

    def __str__(self):
        return self.order.num, self.goods.name


class WareHouseInventory(models.Model):
    """仓库库存信息统计
    可能出现上一批商品还有库存又从同一个供应商进同一种货的情况， 因此此处不设置unique_together
    """
    ware_house = models.ForeignKey(to=WareHouse, on_delete=models.CASCADE, verbose_name='仓库', help_text='仓库')
    goods = models.ForeignKey(to=GoodsManage, on_delete=models.SET_NULL, null=True, verbose_name='商品', help_text='商品')
    num = models.IntegerField(default=0, null=False, verbose_name='库存数量', help_text='库存数量')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源单', help_text='来源单')

    class Meta:
        verbose_name_plural = verbose_name = '仓库库存信息'
        db_table = 'warehouse_inventory'

    def __str__(self):
        return self.goods.name, self.num


class BoxInventory(models.Model):
    """门店库存信息"""
    box = models.ForeignKey(to=BoxManage, on_delete=models.CASCADE, verbose_name='门店', help_text='门店')
    goods = models.ForeignKey(to=GoodsManage, on_delete=models.SET_NULL, null=True, verbose_name='商品', help_text='商品')
    num = models.IntegerField(default=0, null=False, verbose_name='库存数量', help_text='库存数量')
    price = models.FloatField(null=True, blank=True, verbose_name='售价', help_text='售价')
    source = models.ForeignKey(to=PurchaseOrder, to_field='num', on_delete=models.SET_NULL, null=True,
                               verbose_name='来源单', help_text='来源单')

    class Meta:
        verbose_name_plural = verbose_name = '门店库存信息'
        db_table = 'box_inventory'

    def __str__(self):
        return self.goods.name, self.num

    @property
    def current_price(self):
        current_price = None
        if not self.price:
            # 查询点群指导价
            group = self.box.store_group
            if group:
                try:
                    current_price = Group2Price.objects.filter(group_id=group.id,
                                                               goods_id=self.goods_id).first().guide_price
                except:
                    current_price = None
        # 否则返回自己的price
        else:
            current_price = self.price
        return current_price
