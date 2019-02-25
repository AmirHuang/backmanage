# _*_ coding: utf-8 _*_
# @time     : 2018/12/12
# @Author   : Amir
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


from django.urls import path, include, re_path
from rest_framework import routers
from users import views
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.urls import re_path, path
# from users.consumer import search

router = routers.DefaultRouter()


router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'role', views.RoleViewSet, base_name='role')
router.register(r'permissions', views.PermissionsViewSet, base_name='permissions')
# router.register(r'permissions_role', views.PermissionsRoleViewSet, base_name='permissions_role')
router.register(r'area', views.AeraViewSet, base_name='area')
router.register(r'all_user', views.AllUsers, base_name='all_user')
router.register(r'searchUser', views.SearchUserViewSet, base_name='searchUser')
router.register(r'member', views.MemberViewSet, base_name='member')

urlpatterns = [
    path('', include(router.urls)),
    path('getCaptcha/', views.GetCaptchaView.as_view(), name='getCaptcha')

]
