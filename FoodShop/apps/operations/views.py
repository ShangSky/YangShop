from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UserFav
from .serializers import UserFavSerializer, UserFavListSerializer


class UserFavViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    """用户收藏"""
    queryset = UserFav.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavListSerializer
        else:
            return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.like_num -= 1
        goods.save()
        instance.delete()
