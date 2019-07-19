import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """商品过滤"""
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ('category',)
