import django_filters
from .models import OrderGoods


class OrderGoodsFilter(django_filters.rest_framework.FilterSet):
    """订单商品过滤"""

    class Meta:
        model = OrderGoods
        fields = ('is_success',)


class OrderGoodsListFilter(django_filters.rest_framework.FilterSet):
    """评论过滤"""

    class Meta:
        model = OrderGoods
        fields = ('goods',)
