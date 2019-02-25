# _*_ coding: utf-8 _*_
# @time     : 2018/12/13
# @Author   : Amir
# @Site     :
# @File     : urls.py
# @Software : PyCharm

from django.urls import path, include, re_path
from rest_framework import routers
from type.views import TypeViewSet, SmallViewSet

from operatorsystem import views
from type.views import TypeViewSet

router = routers.DefaultRouter()

router.register('boxManage', views.BoxManageViewSet, base_name='boxManage')
router.register('goodsType', TypeViewSet, base_name='goodsType')
router.register('SmallType', SmallViewSet, base_name='SmallType')
# router.register('storeGroup', views.StoreGroupViewSet, base_name='storeGroup')
router.register(r'goodsManage', views.GoodsManageViewSet, base_name='goodsManage')
router.register(r'wareHouseManage', views.WareHouseViewSet, base_name='wareHouseManage')
router.register(r'SupplierManage', views.SupplierViewSet, base_name='SupplierManage')
router.register(r'SearchWareHouse', views.SearchWareHouseViewSet, base_name='SearchWareHouse')
router.register(r'SearchBrandCode', views.SearchBrandCodeViewSet, base_name='SearchBrandCode')
router.register(r'UploadImage', views.UploadImageViewSet, base_name='UploadImage')
# 供应商明细管理
router.register(r'supplierGoodsManage', views.SupplierGoodsViewSet, base_name='supplierGoodsManage')
# 公司类型，支付方式
router.register(r'companyType', views.CompanyTypeViewSet, base_name='companyType')
router.register(r'payments', views.PaymentsViewSet, base_name='payments')
router.register(r'brandCode', views.BrandCodeViewSet, base_name='brandCode')

router.register('storeGroup',views.StoreGroupViewSet, base_name='storeGroup')
router.register('group2Sku',views.Group2SkuViewSet, base_name='group2Sku')
router.register('box2Sku', views.Box2SkuViewSet, base_name='box2Sku')
router.register('group2Price', views.Group2PriceViewSet, base_name='group2Price')
urlpatterns = [
    re_path('', include(router.urls)),
    path(r'totalPoints/', views.TotalPoints.as_view()),
    path(r'totalSuppliers/', views.TotalSuppliers.as_view()),
]
