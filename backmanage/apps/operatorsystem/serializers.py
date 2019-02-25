# _*_ coding: utf-8 _*_
# @time     : 2018/12/13
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

# coding=utf-8
from rest_framework import serializers
from operatorsystem.models import BoxManage, StoreGroup, WareHouse, GoodsManage, Supplier, SupplierGoodsManage, \
    BrandCode
import django_filters
from django_filters.filterset import FilterSet
from users.serializers import UserProfileSerializers
from operatorsystem.models import Payments, CompanyType, UploadImageUrl
from type.serializers import BigTypeDetailSerializer, MiddleTypeDetailSerializer, SmallTypeDetailSerializer, \
    ChildTypeDetailSerializer, SmallTypeSerializer

from tools.totalnodes import WithApplySerializer


class WareHouseSerizlizer(WithApplySerializer):
    develop_user = UserProfileSerializers(many=False, read_only=True)
    operation_user = UserProfileSerializers(many=False, read_only=True)

    class Meta:
        model = WareHouse
        fields = '__all__'


class WareHouseSerizlizers(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = '__all__'


class SearchWareHouseSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = ('id', 'name')


class BrandCodeSerizlizers(serializers.ModelSerializer):
    class Meta:
        model = BrandCode
        fields = ('id', 'name')


class UploadImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = UploadImageUrl
        fields = '__all__'


class BoxManageFilter(FilterSet):
    create_min = django_filters.NumberFilter(name='create_time', lookup_expr='gte')
    create_max = django_filters.NumberFilter(name='carete_time', lookup_expr='lte')

    class Meta:
        model = BoxManage
        # fields = '__all__'
        fields = (
            'name', 'number', 'status', 'create_min', 'create_max', 'Business_circle', 'warehouse', 'city', 'province',
            'bindWarehouseTime')


class GoodsManageSerializer(serializers.ModelSerializer):
    '''可对商品表进行增删改查'''

    class Meta:
        model = GoodsManage
        fields = '__all__'


class StoreGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreGroup
        fields = "__all__"


class BoxManageSerializers(serializers.ModelSerializer):
    warehouse = WareHouseSerizlizer(many=False, read_only=True)
    develop_user = UserProfileSerializers(many=False, read_only=True)
    operation_user = UserProfileSerializers(many=False, read_only=True)
    store_group = StoreGroupSerializers(many=False, read_only=True)
    goods_in_box = GoodsManageSerializer(many=True, read_only=True)

    class Meta:
        model = BoxManage
        fields = '__all__'


class BoxManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxManage
        fields = '__all__'


class StoreGroupFilter(FilterSet):
    class Meta:
        model = StoreGroup
        fields = ('group_name',)


# ---------------------------------------------------------------------
# lujianxin 2018-07-24 供应商，商品关联
# ---------------------------------------------------------------------

class GoodsManageSerializers(serializers.ModelSerializer):
    '''可对商品表进行增删改查'''
    big_type = BigTypeDetailSerializer(read_only=True)
    middle_type = MiddleTypeDetailSerializer(read_only=True)
    small_type = SmallTypeDetailSerializer(read_only=True)
    child_type = ChildTypeDetailSerializer(read_only=True)
    # brand_code = BrandCodeSerizlizers(read_only=True)

    class Meta:
        model = GoodsManage
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = '__all__'


class SupplierDetailSerializer(serializers.ModelSerializer):
    '''可提供供应商的增删改，详情查询'''
    goods_type_num = serializers.SerializerMethodField(read_only=True, help_text='所供商品数')
    # 反向关联提供的所有商品
    goods = GoodsManageSerializer(many=True, read_only=True)
    company_type = CompanyTypeSerializer(read_only=True)
    payments = PaymentsSerializer(read_only=True)
    officer = UserProfileSerializers(read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'

    # 查询供应商供应的商品种数
    def get_goods_type_num(self, obj):
        # print(obj.id)
        return SupplierGoodsManage.objects.filter(supplier_id=obj.id).count()


class SupplierGoodsDetailSerializer(serializers.ModelSerializer):
    '''中间表的详情查'''
    # 嵌套序列器
    supplier = SupplierSerializer(many=False, read_only=True)
    goods = GoodsManageSerializer(many=False, read_only=True)
    apply_user = UserProfileSerializers(many=False, read_only=True)
    # 模型中没有但页面需要的字段
    discount_life = serializers.SerializerMethodField(read_only=True)

    def get_discount_life(self, obj):
        base_str = '{start}至{end}'
        return base_str.format(start=obj.discount_start_time, end=obj.discount_end_time)

    class Meta:
        model = SupplierGoodsManage
        fields = '__all__'


class SupplierGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierGoodsManage
        fields = '__all__'
        # list_serializer_class = Supplier2GoodsListAddSerializer


from operatorsystem import models


class StoreGroupSerializer(serializers.ModelSerializer):
    '''店群'''

    class Meta:
        model = models.StoreGroup
        fields = '__all__'

    def create(self, validated_data):
        from order.baseview import make_order_num
        validated_data['num'] = make_order_num(self.Meta.model, 'DQ')
        return super().create(validated_data)


class Group2SkuSerializer(serializers.ModelSerializer):
    '''店群sku中间表'''

    class Meta:
        model = models.Group2Sku
        fields = '__all__'


class Box2SkuSerializer(serializers.ModelSerializer):
    '''门店sku中间表'''

    class Meta:
        model = models.Box2Sku
        fields = '__all__'


class Group2PriceSerializer(serializers.ModelSerializer):
    '''店群指导价'''

    class Meta:
        model = models.Group2Price
        fields = '__all__'


class Group2SkuDetailSerializer(serializers.ModelSerializer):
    '''店群sku中间表详情'''
    group = StoreGroupSerializer(read_only=True, many=False)
    small_type = SmallTypeDetailSerializer(read_only=True, many=False)

    class Meta:
        model = models.Group2Sku
        fields = '__all__'


class Box2SkuDetailSerializer(serializers.ModelSerializer):
    '''门店sku中间表'''
    box = BoxManageSerializer(read_only=True, many=False)
    small_type = SmallTypeSerializer(read_only=True, many=False)

    class Meta:
        model = models.Box2Sku
        fields = '__all__'


class Group2PriceDetailSerializer(serializers.ModelSerializer):
    '''店群指导价'''
    group = StoreGroupSerializer(read_only=True, many=False)
    goods = GoodsManageSerializer(read_only=True, many=False)

    class Meta:
        model = models.Group2Price
        fields = '__all__'


class StoreGroupDetailSerializer(WithApplySerializer):
    '''店群详情，反关联查询下面的依赖'''
    # 店群指导价
    group_guide_prices = Group2PriceSerializer(many=True, read_only=True)
    # 店群商品结构
    g_skus = Group2SkuDetailSerializer(read_only=True, many=True)
    # skus = SmallTypeSerializer(read_only=True, many=True)
    # 店群下的门店
    boxes = BoxManageSerializer(read_only=True, many=True)

    class Meta:
        model = models.StoreGroup
        fields = '__all__'
