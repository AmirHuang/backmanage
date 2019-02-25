# coding=utf-8

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import GoodsManageSerializer, WareHouseSerizlizer, SupplierSerializer, BoxManageSerializers, \
    StoreGroupSerializers, WareHouseSerizlizers, UploadImageSerializers, BoxManageSerializer
from .filter import WareHouseFilter, GoodsFilter, SupplierFilter, SupplierGoodsManageFilterSet, BoxFilter, \
    BrandCodeFilter
from .serializers import SupplierGoodsSerializer, SupplierGoodsDetailSerializer, SupplierDetailSerializer, \
    BrandCodeSerizlizers, GoodsManageSerializers, SearchWareHouseSerizlizer
import datetime
from rest_framework.filters import SearchFilter

from approval.startapproval import StartApproval
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


class SetPagination(PageNumberPagination):
    """
    分页设置
    """
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class UploadImageViewSet(viewsets.ModelViewSet):
    queryset = UploadImageUrl.objects.all()
    serializer_class = UploadImageSerializers


class BoxManageViewSet(StartApproval, viewsets.ModelViewSet):
    queryset = BoxManage.objects.all().order_by('-create_time')
    pagination_class = SetPagination
    serializer_class = BoxManageSerializers
    filter_class = BoxFilter
    filter_backends = (DjangoFilterBackend,)

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        print('---data', data)
        box_count = BoxManage.objects.all().count()
        box_number = 'B' + str(box_count + 1).zfill(6)
        data['number'] = box_number
        # if BoxManage.objects.filter(name=data['name']):
        #     return Response({'msg': 'Name is regiter!', 'code': 5000})
        serialized = BoxManageSerializer(data=data, context={'request': request})
        if serialized.is_valid():
            self.perform_create(serialized)
            return Response({'msg': 'Picking Delete Success!', 'code': 2001})
        else:
            errorList = serialized.errors.keys()
            dic = {"name": "姓名", "Business_circle": "商圈"}
            res = ""
            for i in errorList:
                res += dic[i] + ","
                print(res)
            return Response({'msg': '{}不能为空'.format(res[:-1]), 'code': 4001})

    def update(self, request, *args, **kwargs):
        wtype = request.data.get('wtype', None)
        instance = self.get_object()

        if wtype == 'wid':
            instance.warehouse_id = request.data["warehouse_id"]
            instance.bindWarehouseTime = datetime.datetime.now()
            instance.save()
            return Response({'msg': 'Update Success！', 'code': 2003})
        else:
            serializer = self.get_serializer(instance, data=request.data)
            # print(serializer)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response({'msg': 'Update Success！', 'code': 2003})
            else:
                return Response({'msg': serializer.errors, 'code': 4001})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(request.data)
        instance.warehouse_id = None
        instance.save()
        return Response({'msg': 'Update Success！', 'code': 2003})

    def perform_update(self, serializer):
        serializer.save()


class SearchWareHouseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SearchWareHouseSerizlizer
    queryset = WareHouse.objects.all()


class SearchBrandCodeViewSet(viewsets.ModelViewSet):
    serializer_class = BrandCodeSerizlizers
    queryset = BrandCode.objects.all()


class GoodsManageViewSet(viewsets.ModelViewSet):
    """
    商品管理
    """
    pagination_class = SetPagination
    queryset = GoodsManage.objects.all()
    serializer_class = GoodsManageSerializers
    filter_class = GoodsFilter
    filter_backends = (DjangoFilterBackend,)

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        print('---data:', data)
        code = int(data['brand_code'])
        print('---code', code)
        brandcode = BrandCode.objects.get(id=code)
        num = GoodsManage.objects.all().count()
        data['number'] = 'P' + brandcode.code + str(num + 1).zfill(4)
        serialized = GoodsManageSerializer(data=data)
        if serialized.is_valid():
            self.perform_create(serialized)
            return Response({'msg': serialized.data, 'code': 0})
        else:
            return Response({'msg': serialized.errors, 'code': -1})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(request.data)
        serializer = self.get_serializer(instance, data=request.data)
        # print(serializer)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'msg': 'Update Success！', 'code': 0})
        else:
            return Response({'msg': serializer.errors, 'code': -1})

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save()


class WareHouseViewSet(StartApproval, viewsets.ModelViewSet):
    """
    仓库管理
    """
    pagination_class = SetPagination
    queryset = WareHouse.objects.all().order_by('-create_time')
    serializer_class = WareHouseSerizlizer
    filter_backends = (DjangoFilterBackend,)
    filter_class = WareHouseFilter

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        num = WareHouse.objects.all().count()
        data['number'] = 'W' + str(num + 1).zfill(6)
        if WareHouse.objects.filter(name=data['name']):
            return Response({'msg': 'Name is regiter!', 'code': 5000})

        serialized = WareHouseSerizlizers(data=data)
        if serialized.is_valid():
            self.perform_create(serialized)
            return Response({'msg': 'Picking Delete Success!', 'code': 2001})
        else:
            # print(serialized.errors)
            return Response({'msg': 'Picking Delete Success!', 'code': 4001})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(request.data)
        serializer = self.get_serializer(instance, data=request.data)
        # print(serializer)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'msg': 'Update Success！', 'code': 2003})
        else:
            return Response({'msg': serializer.errors, 'code': 4001})

    def perform_update(self, serializer):
        serializer.save()


class BrandCodeViewSet(viewsets.ModelViewSet):
    queryset = BrandCode.objects.all()
    serializer_class = BrandCodeSerizlizers
    filter_class = BrandCodeFilter
    filter_backends = (DjangoFilterBackend,)

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        num = BrandCode.objects.all().count()
        data['code'] = '1' + str(num + 1).zfill(3)
        serialized = BrandCodeSerizlizers(data=data)
        if serialized.is_valid():
            self.perform_create(serialized)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        serializer.save()


class SupplierViewSet(viewsets.ModelViewSet):
    """
    供应商管理
    """
    queryset = Supplier.objects.all().order_by('id')
    pagination_class = SetPagination
    # serializer_class = SupplierSerializer
    filter_class = SupplierFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SupplierDetailSerializer
        return SupplierSerializer

    def create(self, request, *args, **kwargs):
        ret = {'msg': '创建成功!', 'code': '201'}
        data = self.request.data.copy()
        num = self.make_number()
        data['number'] = num
        serialized = SupplierSerializer(data=data)
        if serialized.is_valid():
            self.perform_create(serialized)
            return Response(data=ret, status=status.HTTP_201_CREATED)
        else:
            ret = {'code': '4001', 'error': serialized.errors}
            return Response(data=ret, status=status.HTTP_202_ACCEPTED)

    def make_number(self):
        count = Supplier.objects.all().count() + 1
        num = 'S{}'.format(str(count).zfill(6))
        return num


class SupplierGoodsViewSet(viewsets.ModelViewSet):
    # queryset = SupplierGoodsManage.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = SupplierGoodsManageFilterSet
    pagination_class = SetPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SupplierDetailSerializer
        return SupplierGoodsSerializer

    def create(self, request, *args, **kwargs):
        ret = {'code': 0, 'msg': {}}
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            ret['msg'] = serializer.data
        else:
            ret['code'] = -1
            ret['msg'] = serializer.errors
        return Response(data=ret, status=200)

    def destroy(self, request, *args, **kwargs):
        ret = {'code': 0, 'msg': '删除成功。'}
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            ret['code'], ret['msg'] = -1, '删除失败。'
        # print('\n',ret,'\n')
        return Response(data=ret, status=status.HTTP_200_OK)

    def get_queryset(self):
        import re
        sid = self.request.query_params.get('sid', None)
        if not sid:
            return SupplierGoodsManage.objects.all()
        if not re.match(r'^[0-9]+$', sid):
            sid = 0
        return models.Group2Sku.objects.filter(supplier_id=sid)


# ----------------------------------------------------
#     lujianxin   2018-08-08  结算方式，公司类
# ----------------------------------------------------

from operatorsystem.models import Payments, CompanyType
from operatorsystem.serializers import PaymentsSerializer, CompanyTypeSerializer
from operatorsystem.filter import PaymentsFilterSet, CompanyTypeFilterSet


class PaymentsViewSet(viewsets.ModelViewSet):
    '''结算方式'''
    queryset = Payments.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = PaymentsFilterSet
    serializer_class = PaymentsSerializer


class CompanyTypeViewSet(viewsets.ModelViewSet):
    '''公司类型'''
    queryset = CompanyType.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = CompanyTypeFilterSet
    serializer_class = CompanyTypeSerializer


# 分页
class Pagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 5
    max_page_size = 100


# ----------------------
from operatorsystem import models
import operatorsystem.filter as filters
from operatorsystem import serializers


class StoreGroupViewSet(StartApproval, viewsets.ModelViewSet):
    """店群的增删改查"""
    queryset = models.StoreGroup.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = filters.StoreGroupFilterSet
    pagination_class = Pagination

    def get_serializer_class(self):
        ms = ['list', 'retrieve']
        if self.action in ms:
            return serializers.StoreGroupDetailSerializer
        return serializers.StoreGroupSerializer


class Group2SkuViewSet(viewsets.ModelViewSet):
    """店群sku中间表增删改查， 批量增加"""
    # queryset = models.Group2Sku.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = filters.Group2SkuFilterSet
    pagination_class = Pagination

    def get_serializer_class(self):
        ms = ['list', 'retrieve']
        if self.action in ms:
            return serializers.Group2SkuDetailSerializer
        return serializers.Group2SkuSerializer

    def create(self, request, *args, **kwargs):
        ret = {'code': 0, 'msg': {}}
        data = request.data.copy().dict()
        # data 是一个querydict类型
        query = eval(data.get('query', {}))
        serializer = self.get_serializer(
            data=query,
            many=isinstance(query, list)
        )
        if serializer.is_valid():
            self.perform_create(serializer)
            ret['msg'] = serializer.data
        else:
            ret['code'] = -1
            ret['msg'] = serializer.errors
        return Response(data=ret, status=200)

    def get_queryset(self):
        import re
        gid = self.request.query_params.get('gid', None)
        if not gid:
            return models.Group2Sku.objects.all()
        if not re.match(r'^[0-9]+$', gid):
            gid = 0
        return models.Group2Sku.objects.filter(group_id=gid)


class Box2SkuViewSet(Group2SkuViewSet):
    """门店sku中间表增删改查， 批量增"""
    # queryset = models.Box2Sku.objects.all()
    filter_class = filters.Box2SkuFilterSet

    def get_serializer_class(self):
        ms = ['list', 'retrieve']
        if self.action in ms:
            return serializers.Box2SkuDetailSerializer
        return serializers.Box2SkuSerializer

    def get_queryset(self):
        import re
        bid = self.request.query_params.get('bid', None)
        if not bid:
            return models.Box2Sku.objects.all()
        if not re.match(r'^[0-9]+$', bid):
            bid = 0
        return models.Box2Sku.objects.filter(box_id=bid)

    def create(self, request, *args, **kwargs):
        ret = {'code': 0, 'msg': {}}
        data = request.data.copy()
        serializer = self.get_serializer(
            data=data,
            many=isinstance(data, list)
        )
        if serializer.is_valid():
            self.perform_create(serializer)
            ret['msg'] = serializer.data
        else:
            ret['code'] = -1
            ret['msg'] = serializer.errors
        return Response(data=ret, status=200)


# 获取门店所有的sku控制
from tools.transfer import get_total_sku_for_box


class Group2PriceViewSet(Group2SkuViewSet):
    """
        店群的商品指导价
    """
    # queryset = models.Group2Price.objects.all()
    filter_class = filters.Group2PriceFilterSet

    def get_serializer_class(self):
        ms = ['list', 'retrieve']
        if self.action in ms:
            return serializers.Group2PriceDetailSerializer
        return serializers.Group2PriceSerializer

    def get_queryset(self):
        import re
        gid = self.request.query_params.get('gid', None)
        if not gid:
            return models.Group2Price.objects.all()
        if not re.match(r'^[0-9]+$', gid):
            gid = 0
        return models.Group2Price.objects.filter(group_id=gid)


class TotalPoints(ListAPIView):
    def get(self, request):
        """获取全部门店以及仓库名和id"""
        ret = {'box': [], 'ware_house': []}
        boxes = models.BoxManage.objects.all()
        ware_houses = models.WareHouse.objects.all()
        for box in boxes:
            obj = {}
            obj['id'], obj['name'] = box.id, box.name
            # print(obj)
            ret['box'].append(obj)
        for ware_house in ware_houses:
            obj = {}
            obj['id'], obj['name'] = ware_house.id, ware_house.name
            # print(obj)
            ret['ware_house'].append(obj)
        return Response(ret)


class TotalSuppliers(APIView):
    def get(self, request):
        """获取全部供应商信息"""
        suppliers = []
        data = {}
        query = models.Supplier.objects.all()
        if not query:
            return JsonResponse(data)
        for obj in query:
            supplier = {}
            supplier['id'], supplier['name'] = obj.id, obj.name
            suppliers.append(supplier)
        data = {'suppliers': suppliers}
        return Response(data)
