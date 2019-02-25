# _*_ coding: utf-8 _*_
# @time     : 2018/12/13
# @Author   : Amir
# @Site     : 
# @File     : filter.py
# @Software : PyCharm

# coding=utf-8
import django_filters
from .models import WareHouse, GoodsManage, Supplier, SupplierGoodsManage, BoxManage, BrandCode
from operatorsystem.models import Payments, CompanyType


class BoxFilter(django_filters.rest_framework.FilterSet):
    """
    店铺过滤类
    """

    class Meta:
        model = BoxManage
        fields = ['name', 'province', 'city', 'area', 'number', 'warehouse', 'status', 'Business_circle',
                  'operation_mode']


class WareHouseFilter(django_filters.rest_framework.FilterSet):
    """
    仓库过滤类
    """

    class Meta:
        model = WareHouse
        fields = '__all__'


class BrandCodeFilter(django_filters.rest_framework.FilterSet):
    """
    品牌码过滤类
    """
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = BrandCode
        fields = '__all__'


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """
    price_min = django_filters.filters.NumberFilter(name="create_time", lookup_expr='gte')
    price_max = django_filters.filters.NumberFilter(name="create_time", lookup_expr='lte')
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = GoodsManage
        fields = ('goods_status', 'big_type', 'middle_type', 'small_type', 'child_type',
                  'international_code', 'name', 'number')


class SupplierFilter(django_filters.rest_framework.FilterSet):
    """
    供应商过滤类
    """
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    number = django_filters.CharFilter(name='number', lookup_expr='icontains')
    province = django_filters.CharFilter(name='province', lookup_expr='icontains')
    city = django_filters.CharFilter(name='city', lookup_expr='icontains')
    area = django_filters.CharFilter(name='area', lookup_expr='icontains')
    product_addr = django_filters.CharFilter(name='product_addr', lookup_expr='icontains')
    business_addr = django_filters.CharFilter(name='business_addr', lookup_expr='icontains')
    contact = django_filters.CharFilter(name='contact', lookup_expr='icontains')
    iphone = django_filters.CharFilter(name='iphone', lookup_expr='icontains')
    email = django_filters.CharFilter(name='email', lookup_expr='icontains')
    fax = django_filters.CharFilter(name='fax', lookup_expr='icontains')
    remarks = django_filters.CharFilter(name='remarks', lookup_expr='icontains')
    company_name = django_filters.CharFilter(name='company_name', lookup_expr='icontains')
    company_addr = django_filters.CharFilter(name='company_addr', lookup_expr='icontains')
    company_regist_num = django_filters.CharFilter(name='company_regist_num', lookup_expr='icontains')
    taxpayer_num = django_filters.CharFilter(name='taxpayer_num', lookup_expr='icontains')
    bank_name = django_filters.CharFilter(name='bank_name', lookup_expr='icontains')
    bank_account = django_filters.CharFilter(name='bank_account', lookup_expr='icontains')
    bank_addr = django_filters.CharFilter(name='bank_addr', lookup_expr='icontains')

    class Meta:
        model = Supplier
        fields = ['name', 'province', 'city', 'area', 'number', 'status']


class SupplierGoodsManageFilterSet(django_filters.FilterSet):
    sale_check_remark = django_filters.CharFilter(name='sale_check_remark', lookup_expr='icontains')
    discount_check_remark = django_filters.CharFilter(name='discount_check_remark', lookup_expr='icontains')

    class Meta:
        model = SupplierGoodsManage
        fields = "__all__"


class PaymentsFilterSet(django_filters.rest_framework.FilterSet):
    payments = django_filters.CharFilter(name='payments', lookup_expr='icontains')

    class Meta:
        model = Payments
        fields = '__all__'


class CompanyTypeFilterSet(django_filters.rest_framework.FilterSet):
    company_type = django_filters.CharFilter(name='company_type', lookup_expr='icontains')

    class Meta:
        model = CompanyType
        fields = '__all__'


from operatorsystem import models
from django_filters.rest_framework.filterset import FilterSet


class StoreGroupFilterSet(FilterSet):
    '''店群'''
    group_name = django_filters.CharFilter(name='group_name', lookup_expr='icontains')

    class Meta:
        model = models.StoreGroup
        fields = '__all__'


class Group2SkuFilterSet(FilterSet):
    '''店群sku中间表'''
    sku_min = django_filters.NumberFilter(name='sku_min', lookup_expr='gte')
    sku_max = django_filters.NumberFilter(name='sku_max', lookup_expr='lte')

    class Meta:
        model = models.Group2Sku
        fields = '__all__'


class Box2SkuFilterSet(FilterSet):
    '''门店sku中间表'''
    sku_min = django_filters.NumberFilter(name='sku_min', lookup_expr='gte')
    sku_max = django_filters.NumberFilter(name='sku_max', lookup_expr='lte')

    class Meta:
        model = models.Box2Sku
        fields = '__all__'


class Group2PriceFilterSet(FilterSet):
    '''店群指导价'''

    class Meta:
        model = models.Group2Price
        fields = '__all__'
