# coding=utf-8
from users.models import UserProfile, Role, Permissions
# Permissions_Role
from django.http import JsonResponse, HttpResponse
from users import models
from rest_framework import viewsets
from users import serializers

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import requests, json
from datetime import datetime
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from users.serializers import UserProfileSerializers, SearchUserSerializers
from django.views import View
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()


class GetCaptchaView(View):
    def get(self, request):
        from PIL import Image, ImageDraw, ImageFont
        import random, string, io
        bgcolor = (random.randrange(200, 255), random.randrange(
            200, 255), random.randrange(200, 255))
        width = 110
        height = 40
        im = Image.new('RGB', (width, height), bgcolor)
        draw = ImageDraw.Draw(im)
        for i in range(0, 100):
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)
        str1 = string.digits + string.ascii_uppercase
        rand_str = ''
        for i in range(0, 4):
            rand_str += str1[random.randrange(0, len(str1))]
        font = ImageFont.truetype(
            r'C:\Users\Administrator\Desktop\LIANHUASERVER\static\rest_framework\fonts\fontawesome-webfont.ttf', 36)
        fontcolor = (255, random.randrange(50, 255), random.randrange(50, 255))
        draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
        draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
        draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
        draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
        del draw
        buf = io.BytesIO()
        im.save(buf, 'png')
        img = buf.getvalue()
        buf.close()
        red = HttpResponse(img, 'image/Png')
        red.set_cookie('verifycode', rand_str.lower())
        return red


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SetPagination(PageNumberPagination):
    """
    分页设置
    """
    page_size = 4
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class AllUsers(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.AllUserSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          permissions.DjangoModelPermissionsOrAnonReadOnly)


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = SetPagination
    queryset = models.UserProfile.objects.filter(is_superuser=False)
    serializer_class = serializers.UserProfileSerializers
    filter_class = serializers.UserProfileFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # print(data)
        pwd = data.get('password')
        username = data.get("username")
        if username == '':
            return Response({"msg": "帐号不能为空", "code": 1001})
        if pwd == '':
            return Response({"msg": "密码不能为空", "code": 1002})
        password = make_password(pwd)
        data['password'] = password
        # roles = data.pop('role')
        serialized = serializers.UserProfileSerializers(data=data, context={'request': request})
        if serialized.is_valid():
            self.perform_create(serialized)
            # 插入中间表数据
            return Response({"msg": "创建成功", "code": 0})
        else:
            errors = serialized.errors.copy()
            error_dict = {}
            res = []
            for error in errors:
                if str(errors.get(error)[0]) == "已存在一位使用该名字的用户。":
                    res.append("该帐号已存在")
                else:
                    res.append(str(errors.get(error)[0]))
            error_dict["code"] = 1003
            error_dict['msg'] = res
            return Response(error_dict)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializers
    filter_class = serializers.RoleFilter
    filter_backends = (DjangoFilterBackend,)


class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = models.Permissions.objects.all()
    serializer_class = serializers.PermissionsSerializers
    filter_class = serializers.PermissionsFilter
    filter_backends = (DjangoFilterBackend,)


class AeraViewSet(viewsets.ModelViewSet):
    queryset = models.Aera.objects.all()
    serializer_class = serializers.AeraSerializers


class SearchUserViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = SearchUserSerializers


# 会员
class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MemberSerializer
    queryset = models.MemberProfile.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_class = serializers.MemberFilterSet
    pagination_class = SetPagination