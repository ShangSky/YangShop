from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        instance = super(UserFavSerializer, self).create(validated_data)
        goods = instance.goods
        goods.like_num += 1
        goods.save()
        return instance

    class Meta:
        model = UserFav
        fields = ('user', 'goods')
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='你已收藏该商品'
            )
        ]


class UserFavListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        depth = 2
        fields = ('user', 'goods')
