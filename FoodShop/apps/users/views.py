from django.http import HttpResponse
from rest_framework.views import APIView, Response, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from utils.generate_captcha import GenerateCaptcha
from utils.sms_code import SmsCode
from django_redis import get_redis_connection
from .serializers import SmsCodeSerializer, UserInfoSerializer, UserSerializer, AddressSerializer
from .models import UserProfile, Address
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class GenerateCaptchaView(APIView):
    def get(self, request, uuid):
        generate_captcha = GenerateCaptcha()
        code, image_data = generate_captcha.generate_image_captcha(4)
        conn = get_redis_connection()
        conn.set(str(uuid), code, 180)
        return HttpResponse(image_data, content_type="image/png")


class SmsCodeView(APIView):
    """发送手机验证码"""

    def post(self, request):
        serializer = SmsCodeSerializer(data=request.data)
        if serializer.is_valid():
            conn = get_redis_connection()
            sms_code = SmsCode()
            code, result = sms_code.send_sms(serializer.data['username'], 4)
            if result['return_code'] != '00000':
                return Response({'err': '验证码发送失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            conn.set('sms_mobile_{}'.format(serializer.data['username']), 1, 60)
            conn.set('sms_{}_{}'.format(serializer.data["sms_category"], serializer.data['username']), code, 300)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = UserProfile.objects.get(username=username)
        user.set_password(password)
        user.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save()


class UserInfoViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserInfoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
