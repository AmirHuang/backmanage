# _*_ coding: utf-8 _*_
# @time     : 2018/12/12
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

from rest_framework import serializers
from users.models import Role, Permissions, UserProfile, Aera, MemberProfile
from django_filters.filterset import FilterSet
import django_filters


class RoleFilter(FilterSet):
    class Meta:
        model = Role
        fields = '__all__'


class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionsFilter(FilterSet):
    class Meta:
        model = Permissions
        fields = '__all__'


class PermissionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class UserProfileFilter(FilterSet):
    first_name = django_filters.CharFilter(name='first_name', lookup_expr='icontains')
    phone = django_filters.CharFilter(name='phone', lookup_expr='icontains')
    is_active = django_filters.CharFilter(name='is_active')
    role = django_filters.CharFilter(name='role')

    class Meta:
        model = UserProfile
        fields = ('first_name', "phone", "is_active", "role")


class AllUserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSerializers(serializers.ModelSerializer):
    # role = RoleSerializers(many=True, read_only=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
        # exclude = ["password"]


class AeraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Aera
        fields = "__all__"


class SearchUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name')


# --------------------------------------
#     lujianxin   2018-09-03  会员
# --------------------------------------

class MemberFilterSet(FilterSet):
    num = django_filters.CharFilter(name='num', lookup_expr='icontains')
    phone = django_filters.CharFilter(name='phone', lookup_expr='icontains')
    regist_source = django_filters.CharFilter(name='regist_source', lookup_expr='icontains')
    wechat_id = django_filters.CharFilter(name='wechat_id', lookup_expr='icontains')
    alipay_id = django_filters.CharFilter(name='alipay_id', lookup_expr='icontains')
    lianhua_id = django_filters.CharFilter(name='lianhua_id', lookup_expr='icontains')
    lianhua_card = django_filters.CharFilter(name='lianhua_card', lookup_expr='icontains')
    user_name = django_filters.CharFilter(name='user_name', lookup_expr='icontains')
    idcard = django_filters.CharFilter(name='idcard', lookup_expr='icontains')

    class Meta:
        model = MemberProfile
        exclude = ['photo']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        exclude = ['photo']
