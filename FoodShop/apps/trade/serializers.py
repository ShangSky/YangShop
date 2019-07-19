from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart, OrderGoods, OrderInfo
from utils.generate_order_num import generate_order_num
from goods.serializers import GoodsSerializer
from utils.alipay_config import alipay
from FoodShop.settings import return_url, notify_url


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goods_num = serializers.IntegerField(min_value=1, error_messages={'blank': "请选择购买数量", 'min_value': "商品数量不饿能小于1", })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all())

    def validate(self, attrs):
        user = attrs["user"]
        goods_num = attrs["goods_num"]
        goods = attrs["goods"]
        shopping_cart = ShoppingCart.objects.filter(user=user, goods=goods)
        if shopping_cart:
            goods_num += shopping_cart[0].goods_num
        if goods_num > goods.stock_num:
            raise serializers.ValidationError("商品数量超过库存")
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        goods_num = validated_data["goods_num"]
        goods = validated_data["goods"]

        shopping_cart = ShoppingCart.objects.filter(user=user, goods=goods)
        if shopping_cart:
            shopping_cart = shopping_cart[0]
            shopping_cart.goods_num += goods_num
            shopping_cart.save()
        else:
            shopping_cart = ShoppingCart.objects.create(**validated_data)
        return shopping_cart

    def update(self, instance, validated_data):
        instance.goods_num = validated_data["goods_num"]
        instance.save()
        return instance


class ShoppingCartListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        depth = 1
        model = ShoppingCart
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGoods
        fields = "__all__"
        read_only_fields = ("order", "rate", "comment")


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_goods = OrderGoodsSerializer(many=True)
    pay_url = serializers.SerializerMethodField(read_only=True)

    def get_pay_url(self, obj):
        order_string = alipay.api_alipay_trade_wap_pay(
            out_trade_no=obj.order_num,
            total_amount=float('{:.2f}'.format(obj.total_price)),
            subject='阳哥商城',
            return_url=return_url,
            notify_url=notify_url
        )
        return 'https://openapi.alipaydev.com/gateway.do?{}'.format(order_string)

    def validate(self, attrs):
        attrs["order_num"] = generate_order_num(attrs["user"].id)
        if not attrs["order_goods"]:
            raise serializers.ValidationError("商品不能为空")
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
        read_only_fields = ("order_num", "trade_num", "total_price", "freight", "pay_status", "pay_time")


class OrderGoodsListSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = OrderGoods
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_goods = OrderGoodsListSerializer(many=True)
    pay_status = serializers.SerializerMethodField()
    pay_url = serializers.SerializerMethodField()

    def get_pay_status(self, obj):
        return obj.get_pay_status_display()

    def get_pay_url(self, obj):
        order_string = alipay.api_alipay_trade_wap_pay(
            out_trade_no=obj.order_num,
            total_amount=float('{:.2f}'.format(obj.total_price)),
            subject='阳哥商城',
            return_url=return_url,
            notify_url=notify_url
        )
        return 'https://openapi.alipaydev.com/gateway.do?{}'.format(order_string)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class GoodsCommentSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(read_only=True)
    rate = serializers.ChoiceField(choices=(1, 2, 3, 4, 5))
    comment = serializers.CharField(required=True, error_messages={"blank": "评论内容不能为空"})

    def validate(self, attrs):
        attrs["is_success"] = True
        return attrs

    class Meta:
        model = OrderGoods
        fields = "__all__"
        read_only_fields = ("order", "goods", "goods_num", "is_success")


class GoodsDetailCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="order.user.nickname")
    avatar = serializers.ImageField(source="order.user.avatar")

    class Meta:
        model = OrderGoods
        fields = ("rate", "comment", "update_time", "nickname", "avatar")
