from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from FoodShop.settings import MEDIA_ROOT
from rest_framework import routers
from goods.views import IndexBannerViewSet, CategoryViewSet, GoodsViewSet
from users.views import GenerateCaptchaView, SmsCodeView, UserViewSet, AddressViewSet, UserInfoViewSet
from operations.views import UserFavViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet, GoodsCommentViewSet, GoodsDetailCommentViewSet, AliPayView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls
router = routers.DefaultRouter()
router.register(r'api/index_banner', IndexBannerViewSet)
router.register(r'api/category', CategoryViewSet)
router.register(r'api/goods', GoodsViewSet)
router.register(r'api/user_info', UserInfoViewSet)
router.register(r'api/user', UserViewSet)
router.register(r'api/user_fav', UserFavViewSet)
router.register(r'api/user_address', AddressViewSet)
router.register(r'api/shopping_cart', ShoppingCartViewSet)
router.register(r'api/order', OrderViewSet)
router.register(r'api/goods_comment', GoodsCommentViewSet)
router.register(r'api/goods_detail_comment', GoodsDetailCommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/<uuid:uuid>', GenerateCaptchaView.as_view()),
    path('api/sms_code/', SmsCodeView.as_view()),
    path('api/pay/', AliPayView.as_view()),
    path('', include(router.urls)),
    path('api/docs/', include_docs_urls(title='阳哥商城')),
    path('api/login/', obtain_jwt_token),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path('api-auth/', include('rest_framework.urls'))
]
