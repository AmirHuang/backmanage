# _*_ coding: utf-8 _*_
# @time     : 2018/12/12
# @Author   : Amir
# @Site     : 
# @File     : baseview.py
# @Software : PyCharm
"""拥有公共方法的基础视图"""

from rest_framework.filters import SearchFilter
from order import models
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class SetPagination(PageNumberPagination):
    """
    分页设置
    """
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


# 获取当天的时间范围
def get_today_range():
    import datetime
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    date_from = datetime.datetime(year, month, day, 0, 0, 0)
    date_to = datetime.datetime(year, month, day, 23, 59, 59)
    return (date_from, date_to)


def make_order_num(model, start, zero=4):
    """
    :param model: 将要查询的model
    :param start: 开时的字母
    :param zero: 日期以后的位数
    :return order_num: 产生的单号
    """
    from time import strftime
    assert isinstance(start, str), '"start" must be string-type.'
    assert isinstance(zero, int) and zero > 0, 'zero must be positive-int.'
    order_num = -1
    today = get_today_range()
    time_str = strftime('%Y%m%d')
    count = model.objects.filter(create_time__range=today).count() + 1
    if count < 10 ** (zero - 1):
        order_num = '{}{}{}'.format(start, time_str, str(count).zfill(zero))
        print('---str(count).zfill(zero):', str(count).zfill(zero))
        print('---order_num:', order_num)
    return order_num


class BaseOrderViewSet(viewsets.ModelViewSet):
    """订单类视图基础"""
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    default_serializer_class = None  # 普通序列器
    detail_serializer_class = None  # 详情序列器

    def get_serializer_class(self):
        ms = ['list', 'retrieve']
        if self.action in ms:
            return self.detail_serializer_class
        return self.default_serializer_class


class BaseMiddleViewSet(BaseOrderViewSet):
    """订单商品中间表基本类"""
    middle_model = None  # 中间表model
    xid = 'oid'  # 接收时的参数名
    order_name_id = None  # 过滤的关键字名称

    def get_queryset(self):
        filter_id = self.request.query_params.get(self.xid)
        if filter_id:
            f = {self.order_name_id: filter_id}
            return self.middle_model.objects.filter(**f)
        return self.middle_model.objects.all()

    def create(self, request, *args, **kwargs):
        ret = {'code': 0, 'msg': {}}
        data = request.data.copy().dict()
        # data 是一个querydict类型
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


if __name__ == '__main__':
    pass
