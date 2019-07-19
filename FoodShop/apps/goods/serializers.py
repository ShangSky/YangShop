from rest_framework import serializers
from .models import Goods, Category, IndexBanner, GoodsBanner


class IndexBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexBanner
        fields = ('image', 'goods')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GoodsBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsBanner
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    goods_banner = GoodsBannerSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'
