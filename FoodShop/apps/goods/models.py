from django.db import models
from db.base_model import BaseModel


class Category(BaseModel):
    """商品类别"""
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    image = models.ImageField(null=True, blank=True, upload_to='goods/category/', verbose_name='类别图片')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """商品"""
    category = models.ForeignKey(Category, verbose_name='商品类别', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='商品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='销量')
    like_num = models.IntegerField(default=0, verbose_name='收藏数')
    rate = models.IntegerField(default=5, choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), verbose_name='评分')
    stock_num = models.IntegerField(default=0, verbose_name='库存')
    ship_free = models.BooleanField(default=True, verbose_name='是否包邮')
    desc = models.TextField(max_length=500, verbose_name='商品介绍')
    image = models.ImageField(upload_to="goods/goods/", verbose_name='商品图片')

    class Meta:
        ordering = ('id',)
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsBanner(BaseModel):
    """商品轮播图"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='goods_banner', verbose_name='商品')
    image = models.ImageField(upload_to='goods/goods_banner/', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")

    class Meta:
        ordering = ('index',)
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexBanner(BaseModel):
    """首页轮播图"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='goods/index_banner/', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")

    class Meta:
        ordering = ('index',)
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
