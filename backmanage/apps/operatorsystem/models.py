# coding=utf-8
from django.db import models
# Create your models here.
from datetime import datetime
from users.models import UserProfile
import django.utils.timezone as timezone
from type.models import BigType, MiddleType, SmallType, ChildType
from approval.models import Process
from backmanage.settings import DEFAULT_GOODS_IMG


class BrandCode(models.Model):
    code = models.CharField(max_length=100, verbose_name='品牌代码')
    name = models.CharField(max_length=100, verbose_name='品牌名字', unique=True)

    class Meta:
        verbose_name = '品牌字典'
        verbose_name_plural = verbose_name
        db_table = 'brand_code'

    def __str__(self):
        return self.name


# Create your models here.
class GoodsManage(models.Model):
    mode = (
        (0, '统一配送'),
        (1, '直接采购')
    )
    unit = (
        (0, '包'), (1, '盒'), (2, '袋'), (3, '瓶'), (4, '杯'), (5, '碗'), (6, '桶'), (7, '只'), (8, '把'), (9, '条'), (10, '卡'),
        (11, '罐'), (12, '支'), (13, '块'), (14, '筒'), (15, '组'),
        (16, '套'), (17, '提'), (18, '本'), (19, '个'), (20, '册'), (21, '双'), (22, '件'), (23, '捆'), (24, '听')
    )
    status = (
        (0, '正常'),
        (1, '清退'),
        (2, '淘汰')
    )

    name = models.CharField(max_length=100, verbose_name='商品名称')
    number = models.CharField(max_length=100, verbose_name='商品编号', null=True, blank=True)
    imageUrl = models.CharField(max_length=100, verbose_name='商品图片', default=DEFAULT_GOODS_IMG)
    international_code = models.CharField(max_length=100, verbose_name='国际条码', unique=True, primary_key=True)
    product_addr = models.CharField(max_length=100, verbose_name='产地地址')
    brand_code = models.ForeignKey(BrandCode, verbose_name='品牌字典库', related_name='brand_code',
                                   on_delete=models.SET_NULL, null=True)
    enter_rate = models.IntegerField(choices=((0, '0%'), (1, "6%"), (2, "10%"), (3, "16%")), verbose_name='进项税率')
    sale_rate = models.IntegerField(choices=((0, '0%'), (1, "6%"), (2, "10%"), (3, "16%")), verbose_name='销项税率')
    packing_unit = models.IntegerField(choices=unit, verbose_name='单位')
    guig = models.CharField(max_length=100, verbose_name='规格')
    shelf_life = models.CharField(max_length=100, verbose_name='保证期')
    big_type = models.ForeignKey(BigType, related_name='big_type', verbose_name='大类', on_delete=models.SET_NULL,
                                 null=True, )
    middle_type = models.ForeignKey(MiddleType, related_name='middle_type', verbose_name='中类',
                                    on_delete=models.SET_NULL, null=True, )
    small_type = models.ForeignKey(SmallType, related_name='small_type', verbose_name='小类', on_delete=models.SET_NULL,
                                   null=True, )
    child_type = models.ForeignKey(ChildType, related_name='child_type', verbose_name='子类', on_delete=models.SET_NULL,
                                   null=True, )
    goods_status = models.IntegerField(choices=status, default=0, verbose_name='商品状态')
    goods_detail = models.CharField(max_length=400, verbose_name='商品详情')
    box_code = models.CharField(max_length=100, verbose_name='包装箱码', null=True, blank=True)
    specification = models.CharField(max_length=100, verbose_name='包装规格', null=True, blank=True)
    min_Purchase_num = models.IntegerField(verbose_name='最低采购数量')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '商品管理'
        verbose_name_plural = verbose_name
        db_table = 'goods_manage'

    def __str__(self):
        return self.name


class UploadImageUrl(models.Model):
    imageUrl = models.ImageField(verbose_name='商品图片', upload_to='box_image/')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '图片上传'
        verbose_name_plural = verbose_name
        db_table = 'upload_image'

    def __str__(self):
        return self.imageUrl


class WareHouse(models.Model):
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭'),
        (4, '启用'),
        (5, '停用')
    )

    name = models.CharField(max_length=100, verbose_name='仓库名称', unique=True)
    number = models.CharField(max_length=100, verbose_name='仓库编号', null=True, blank=True)
    province = models.CharField(max_length=100, verbose_name='省份')
    city = models.CharField(max_length=100, verbose_name='城市')
    area = models.CharField(max_length=100, verbose_name='区域')
    addr = models.CharField(max_length=100, verbose_name='详细地址')
    size = models.CharField(max_length=100, verbose_name='面积', default=0)
    latitude_longitude = models.CharField(max_length=100, verbose_name='经纬度', null=True, blank=True)
    develop_user = models.ForeignKey(UserProfile, verbose_name='发展负责人', related_name='w_develop_user',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    operation_user = models.ForeignKey(UserProfile, verbose_name='运维负责人', related_name='w_operation_user',
                                       on_delete=models.SET_NULL, null=True,
                                       blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='仓库创建时间')
    start_time = models.DateField(verbose_name='开业时间', null=True)
    end_time = models.DateField(verbose_name='结业时间', null=True)
    status = models.IntegerField(choices=statuses, default=0, null=False, verbose_name='审核状态', help_text='审核状态')

    class Meta:
        verbose_name = '仓库管理'
        verbose_name_plural = verbose_name
        db_table = 'warehouse'

    def __str__(self):
        return self.name


class StoreGroup(models.Model):
    '''店群, 控制店下面的sku'''
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭')
    )
    num = models.CharField(max_length=32, null=True, unique=True, verbose_name='店群编号', help_text='店群编号')
    group_name = models.CharField(null=False, blank=False, max_length=20, unique=True, verbose_name='店群',
                                  help_text='店群')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='备注', help_text='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    skus = models.ManyToManyField(to=SmallType, through='Group2Sku', verbose_name='sku控制', help_text='sku控制')
    status = models.IntegerField(choices=statuses, default=0, null=False, verbose_name='审核状态',
                                 help_text='审核状态')

    class Meta:
        verbose_name = '店群'
        verbose_name_plural = verbose_name
        db_table = 'storegroup'

    def __str__(self):
        return self.group_name


class BoxManage(models.Model):
    mode = (
        (0, '盒子'),
        (1, '货柜'),
        (2, '社区店'),
        (3, '改造店')
    )
    Business_circle_type = (
        (0, '社区'),
        (1, '写字楼'),
        (2, '酒店'),
        (3, '车站'),
        (4, '医院'),
        (5, '学校'),
        (6, '景区'),
    )
    operation = (
        (0, '自营'),
        (1, '加盟'),
    )
    statuses = (
        (0, '审核中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭'),
        (4, '营业'),
        (5, '停业'),
        (6, '闭店')
    )

    name = models.CharField(max_length=100, verbose_name='门店名称', null=False, blank=False, unique=True)
    imageUrl = models.CharField(max_length=200, verbose_name='门店照片', null=True, )
    number = models.CharField(max_length=100, verbose_name='门店编号', null=True, blank=True, unique=True)
    store_mode = models.IntegerField(choices=mode, verbose_name='门店形式', default=0)
    store_group = models.ForeignKey(to=StoreGroup, related_name='boxes', on_delete=models.SET_NULL, null=True,
                                    verbose_name='所属店群', help_text='所属店群')
    operation_mode = models.IntegerField(choices=operation, verbose_name='运营模式', default=0)
    province = models.CharField(max_length=100, verbose_name='省份', default="")
    city = models.CharField(max_length=100, verbose_name='城市', default="")
    area = models.CharField(max_length=100, verbose_name='区域', default="")
    addr = models.CharField(max_length=100, verbose_name='详细地址', default="")
    latitude_longitude = models.CharField(max_length=100, verbose_name='经纬度', null=True)
    warehouse = models.ForeignKey(WareHouse, verbose_name='仓库名', on_delete=models.SET_NULL, null=True,
                                  related_name='ware')
    Business_circle = models.IntegerField(choices=Business_circle_type, verbose_name='商圈')
    bindWarehouseTime = models.DateTimeField(auto_now_add=True, verbose_name='绑定仓库时间')
    develop_user = models.ForeignKey(UserProfile, verbose_name='发展负责人', related_name='b_develop_user',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    operation_user = models.ForeignKey(UserProfile, verbose_name='运维负责人', related_name='b_operation_user',
                                       on_delete=models.SET_NULL, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='门店创建时间')
    start_time = models.DateField(verbose_name='开业时间', auto_now_add=True, )
    end_time = models.DateField(verbose_name='结业时间', auto_now_add=True, )
    status = models.IntegerField(choices=statuses, default=0, null=False, verbose_name='审核状态',
                                 help_text='审核状态')

    class Meta:
        verbose_name = '门店管理'
        verbose_name_plural = verbose_name
        db_table = 'box_manage'

    def __str__(self):
        return self.name


class Payments(models.Model):
    '''结算方式'''
    payments = models.CharField(max_length=20, blank=False, null=False, unique=True, verbose_name='结算方式',
                                help_text='结算方式')
    create_time = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注', help_text='备注')

    class Meta:
        verbose_name = '结算方式'
        verbose_name_plural = verbose_name
        db_table = 'payments'

    def __str__(self):
        return self.payments


class CompanyType(models.Model):
    '''公司类型'''
    company_type = models.CharField(max_length=30, blank=False, null=False, unique=True, verbose_name='公司类型',
                                    help_text='公司类型')
    remark = models.CharField(max_length=100, blank=True, null=True, verbose_name='备注', help_text='备注')
    create_time = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name = '公司类型'
        verbose_name_plural = verbose_name
        db_table = 'company_type'

    def __str__(self):
        return self.company_type


class Supplier(models.Model):
    # 基础信息
    name = models.CharField(max_length=60, verbose_name='供应商名称', help_text='供应商名称')
    number = models.CharField(max_length=7, verbose_name='供应商编号', help_text='供应商编号', unique=True, )
    company_type = models.ForeignKey(to=CompanyType, on_delete=models.CASCADE, verbose_name='公司类型',
                                     help_text='公司类型', null=True)
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间', auto_created=True)
    company_regist_num = models.CharField(max_length=18, unique=True, verbose_name='工商注册号', help_text='工商注册号')
    province = models.CharField(max_length=30, verbose_name='省份', help_text='省份')
    city = models.CharField(max_length=30, verbose_name='城市', help_text='市')
    area = models.CharField(max_length=30, verbose_name='区域', help_text='区/县')
    # 联系信息
    product_addr = models.CharField(max_length=100, verbose_name='生产地址', help_text='生产地址', null=True, blank=True)
    business_addr = models.CharField(max_length=100, verbose_name='经营地址', help_text='经营地址', null=True, blank=True)
    company_name = models.CharField(max_length=60, verbose_name='公司名称', help_text='公司名称', blank=True, null=True)
    company_addr = models.CharField(max_length=100, verbose_name='公司地址', help_text='公司地址', blank=True, null=True)
    contact = models.CharField(max_length=100, verbose_name='联系人', help_text='联系人')
    iphone = models.CharField(max_length=100, verbose_name='联系电话', help_text='联系电话')
    email = models.CharField(max_length=100, verbose_name='邮箱', help_text='邮箱', null=True, blank=True)
    fax = models.CharField(max_length=100, verbose_name='传真', help_text='传真', null=True, blank=True)
    remarks = models.CharField(max_length=100, verbose_name='备注', help_text='备注', null=True, blank=True)
    # 结算信息
    payments = models.ForeignKey(to=Payments, on_delete=models.CASCADE, verbose_name='结算方式', help_text='结算方式')
    taxpayer_num = models.CharField(max_length=60, unique=True, verbose_name='纳税人识别号', help_text='纳税人识别号')
    bank_name = models.CharField(max_length=60, verbose_name='开户行', help_text='开户行')
    bank_account = models.CharField(max_length=30, verbose_name='开户行账号', help_text='开户行账号')
    bank_addr = models.CharField(max_length=100, verbose_name='开户行地址', help_text='开户行地址')
    # 运营信息
    goods = models.ManyToManyField(to=GoodsManage, verbose_name='供应商所供商品', help_text='所供商品',
                                   through='SupplierGoodsManage')
    status = models.IntegerField(choices=((0, '启用'), (1, '停用')), default=0, help_text='状态')
    officer = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, verbose_name='负责人', help_text='负责人')
    rate = models.IntegerField(default=0, verbose_name='通道费率', help_text='通道费率')

    class Meta:
        verbose_name = '供应商管理'
        verbose_name_plural = verbose_name
        db_table = 'supplier'

    def __str__(self):
        return self.name


# lujianxin 2018-07-23 供应商商品管理,

class SupplierGoodsManage(models.Model):
    supplier = models.ForeignKey(to=Supplier, related_name='s_goods', verbose_name='供应商', on_delete=models.CASCADE,
                                 blank=True,
                                 null=True, help_text='供应商')
    goods = models.ForeignKey(to=GoodsManage, verbose_name='商品', on_delete=models.CASCADE, blank=True, null=True,
                              help_text='商品')
    apply_user = models.ForeignKey(to=UserProfile, verbose_name='申请人', on_delete=models.CASCADE, blank=True, null=True,
                                   help_text='进价，促销价申请人')
    sale_price = models.FloatField(verbose_name='采购进价', blank=True, null=True, help_text='采购进价')
    discount_price = models.FloatField(verbose_name='促销价', blank=True, null=True, help_text='促销进价')
    sale_min_count = models.IntegerField(verbose_name='采购起始数量', blank=True, null=True, default=100, help_text='采购起始数量')
    discount_min_count = models.IntegerField(verbose_name='促销起始数量', blank=True, null=True, default=200,
                                             help_text='促销起始数量')
    sale_status = models.IntegerField(choices=((0, '待审核'), (1, '审核通过'), (2, "审核未通过")), verbose_name='采购进价审核状态',
                                      blank=True, null=True, default=0, help_text='采购进价审核状态')
    sale_check_remark = models.CharField(max_length=200, null=True, blank=True, verbose_name="采购价审核备注",
                                         help_text="采购价审核备注")
    discount_status = models.IntegerField(choices=((0, '待审核'), (1, '审核通过'), (2, "审核未通过")), verbose_name='促销进价审核状态',
                                          blank=True, null=True, default=0, help_text='促销进价审核状态')
    discount_check_remark = models.CharField(max_length=200, null=True, blank=True, verbose_name="促销进价审核备注",
                                             help_text="促销进价审核备注")
    sale_apply_time = models.DateTimeField(verbose_name='采购进价发起时间', blank=True, null=True, help_text='采购进价发起时间')
    discount_apply_time = models.DateTimeField(verbose_name='促销进价发起时间', blank=True, null=True, help_text='促销进价发起时间')
    sale_check_time = models.DateTimeField(verbose_name='采购进价审核时间', blank=True, null=True, help_text='采购进价审核时间')
    discount_check_time = models.DateTimeField(verbose_name='促销进价审核时间', blank=True, null=True, help_text='促销进价审核时间')
    supply_status = models.IntegerField(choices=((0, '启用'), (1, '停用')), help_text='供应状态', default=0,
                                        verbose_name='供应状态',
                                        blank=True, null=True)
    discount_start_time = models.DateTimeField(verbose_name='促销开始时间', blank=True, null=True, help_text='促销开始时间')
    discount_end_time = models.DateTimeField(verbose_name='促销结束时间', blank=True, null=True, help_text='促销结束时间')
    is_discount = models.BooleanField(default=False, verbose_name='是否打折', help_text='是否打折')

    class Meta:
        verbose_name = '供应商商品管理'
        verbose_name_plural = verbose_name
        unique_together = (("supplier", "goods"),)
        db_table = 'supplier_goods_manage'

    def __str__(self):
        return '%s, %s, %s' % (self.supplier.name, self.goods.name, self.supply_status)


from type.models import SmallType


class Group2Sku(models.Model):
    '''店群和sku中间表'''
    small_type = models.ForeignKey(to=SmallType, on_delete=models.CASCADE, null=False, blank=False, verbose_name='SKU',
                                   help_text='SKU')
    group = models.ForeignKey(to=StoreGroup, related_name='g_skus', on_delete=models.CASCADE, null=False, blank=False,
                              verbose_name='店群', help_text='店群')
    sku_min = models.IntegerField(default=1, null=False, blank=False, verbose_name='sku下限', help_text='sku下限')
    sku_max = models.IntegerField(default=100, null=False, blank=False, verbose_name='sku上限', help_text='sku上限')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注', help_text='备注')
    created = models.DateTimeField(auto_now_add=True, auto_created=True, null=False, blank=False, verbose_name='创建时间',
                                   help_text='创建时间')

    class Meta:
        verbose_name = '店群和sku中间表'
        verbose_name_plural = verbose_name
        unique_together = (('small_type', 'group'),)
        db_table = 'group2sku'


class Box2Sku(models.Model):
    '''门店和sku中间表'''
    small_type = models.ForeignKey(to=SmallType, on_delete=models.CASCADE, null=False, blank=False, verbose_name='SKU',
                                   help_text='SKU')
    box = models.ForeignKey(to=BoxManage, related_name='skus', on_delete=models.CASCADE, null=False, blank=False,
                            verbose_name='门店', help_text='门店')
    sku_min = models.IntegerField(default=1, null=False, blank=False, verbose_name='sku下限', help_text='sku下限')
    sku_max = models.IntegerField(default=100, null=False, blank=False, verbose_name='sku上限', help_text='sku上限')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name='备注', help_text='备注')
    created = models.DateTimeField(auto_now_add=True, auto_created=True, null=False, blank=False, verbose_name='创建时间',
                                   help_text='创建时间')

    class Meta:
        verbose_name = '门店和sku中间表'
        verbose_name_plural = verbose_name
        unique_together = ('small_type', 'box')
        db_table = 'box2sku'

    def __str__(self):
        return self.small_type.name, self.box.name


# 以上三表控制经营方案（商品结构），门店可选择店群获得店群的sku控制， 也可自行选取店群sku之外的small_type


# 店群指导价
class Group2Price(models.Model):
    """每种商品在每个店群都有一个指导价，所以这张表共有 商品数x店群数 条记录"""
    group = models.ForeignKey(to=StoreGroup, related_name='group_guide_prices', on_delete=models.CASCADE,
                              verbose_name='店群',
                              help_text='店群')
    goods = models.ForeignKey(to=GoodsManage, on_delete=models.CASCADE, verbose_name='商品', help_text='店群')
    guide_price = models.FloatField(null=False, blank=False, verbose_name='指导价', help_text='指导价')
    created = models.DateTimeField(auto_now_add=True, auto_created=True, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name = '店群指导价'
        verbose_name_plural = verbose_name
        unique_together = (('group', 'goods'),)
        db_table = 'group2price'

    def __str__(self):
        return self.goods.name, self.group.group_name, self.guide_price
