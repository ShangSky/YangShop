from django.db import models
from db.base_model import BaseModel


class ShoppingCart(BaseModel):
    """购物车"""
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE, verbose_name='商品')
    goods_num = models.IntegerField(default=1, verbose_name='商品数量')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "{}({})".format(self.goods.name, self.goods_num)


class OrderInfo(BaseModel):
    """订单"""
    ORDER_STATUS = (
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_CLOSED", "超时关闭"),
        ("TRADE_SUCCESS", "支付成功"),
        ("TRADE_FINISHED", "交易结束"),
    )
    order_num = models.CharField(max_length=100, blank=True, unique=True, verbose_name='订单号')
    trade_num = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='交易号')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    freight = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='运费')
    user = models.ForeignKey('users.UserProfile', verbose_name='所属用户', on_delete=models.CASCADE)
    pay_status = models.CharField(choices=ORDER_STATUS, default="WAIT_BUYER_PAY", max_length=30, verbose_name="交易状态")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    receiver = models.CharField(max_length=20, default="", verbose_name="签收人")
    mobile = models.CharField(max_length=11, verbose_name="联系电话")

    class Meta:
        ordering = ("-create_time",)
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_num


class OrderGoods(BaseModel):
    order = models.ForeignKey(OrderInfo, related_name="order_goods", on_delete=models.CASCADE, verbose_name='订单')
    goods = models.ForeignKey('goods.Goods', verbose_name="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=1, verbose_name="商品数量")
    rate = models.IntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), null=True, blank=True,
                               verbose_name='评分')
    comment = models.TextField(null=True, blank=True, max_length=300, verbose_name='评论内容')
    is_success = models.BooleanField(default=False, verbose_name="是否已评论")

    class Meta:
        ordering = ("-update_time",)
        unique_together = ("order", "goods")
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_num
