# _*_ coding: utf-8 _*_
# @time     : 2018/12/13
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm

from approval import views
from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'node', views.NodeViewSet, base_name='node')
router.register(r'process', views.ProcessViewSet, base_name='process')
router.register(r'nodeStatus', views.NodeStatusViewSet, base_name='nodeStatus')
router.register(r'typeProcess', views.TypeProcessViewSet, base_name='typeProcess')
router.register(r'apply', views.ApplyViewSet, base_name='apply')


urlpatterns = [
    re_path(r'^', include(router.urls)),
    # path('setNodePassed/', views.set_node_passed),
    # path('setNodeNopass/', views.set_node_nopass),
    # path('updateTarget/', views.update_target_request),
]

