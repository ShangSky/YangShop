from django.db import models
from db.base_model import BaseModel


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey('users.UserProfile', verbose_name="用户", on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', verbose_name="商品", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username
