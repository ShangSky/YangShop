from django.contrib import admin
from .models import Goods, GoodsBanner, Category, IndexBanner
admin.site.site_header = admin.site.site_title = admin.site.index_title = '阳哥商城后台管理'


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsBanner)
class GoodsBannerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(IndexBanner)
class IndexBannerAdmin(admin.ModelAdmin):
    pass

