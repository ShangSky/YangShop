from .models import IndexBanner, Category, Goods
from .serializers import IndexBannerSerializer, CategorySerializer, GoodsSerializer
from rest_framework import viewsets, mixins, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 20
    page_size_query_param = 'page_size'


class IndexBannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """首页轮播图"""
    queryset = IndexBanner.objects.all()
    serializer_class = IndexBannerSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """商品类别"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GoodsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'desc')
    ordering_fields = ('price', 'sold_num', 'click_num')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
