from datetime import datetime
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShoppingCartListSerializer, OrderSerializer, OrderListSerializer, \
    GoodsDetailCommentSerializer, GoodsCommentSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from .filters import OrderGoodsFilter, OrderGoodsListFilter
from rest_framework.pagination import PageNumberPagination
from utils.alipay_config import alipay


class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartListSerializer
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = OrderInfo.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order_goods_list = serializer.validated_data.pop("order_goods")
        total_price = Decimal('0.00')
        for order_goods in order_goods_list:
            total_price += (order_goods["goods_num"] * Decimal(order_goods["goods"].price).quantize(Decimal('0.00')))
        serializer.validated_data["total_price"] = total_price
        order = serializer.save()
        for order_goods in order_goods_list:
            order_goods["goods"].stock_num -= order_goods["goods_num"]
            order_goods["goods"].sold_num += order_goods["goods_num"]
            order_goods["goods"].save()
            ShoppingCart.objects.filter(goods=order_goods["goods"]).delete()
            order_goods["order"] = order
            OrderGoods.objects.create(**order_goods)


class GoodsCommentViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = OrderGoods.objects.filter()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = GoodsCommentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = OrderGoodsFilter

    def get_queryset(self):
        if self.action == "update":
            return OrderGoods.objects.filter(order__pay_status__in=('TRADE_FINISHED', 'TRADE_SUCCESS'), order__user=self.request.user,
                                             is_success=False)
        return OrderGoods.objects.filter(order__pay_status__in=('TRADE_FINISHED', 'TRADE_SUCCESS'), order__user=self.request.user)


class GoodsDetailCommentsPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    max_page_size = 10
    page_size_query_param = 'page_size'


class GoodsDetailCommentViewSet(ListModelMixin, GenericViewSet):
    queryset = OrderGoods.objects.filter(is_success=True)
    serializer_class = GoodsDetailCommentSerializer
    pagination_class = GoodsDetailCommentsPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = OrderGoodsListFilter


class AliPayView(APIView):
    def post(self, request):
        """异步回调"""
        data = {}
        for key, value in request.POST.items():
            data[key] = value
        signature = data.pop("sign", None)
        if alipay.verify(data, signature):
            order_num = data.get('out_trade_no', None)
            trade_num = data.get('trade_no', None)
            trade_status = data.get('trade_status', None)

            order = OrderInfo.objects.filter(order_num=order_num)
            if order:
                order = order[0]
                order.pay_status = trade_status
                order.trade_num = trade_num
                order.pay_time = datetime.now()
                order.save()
                return Response("success")
