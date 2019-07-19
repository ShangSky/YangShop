from rest_framework import serializers
from django_redis import get_redis_connection
from .models import UserProfile, Address
import re


class SmsCodeSerializer(serializers.Serializer):
    """发送验证码校验"""
    captcha = serializers.CharField(
        min_length=4,
        max_length=4,
        error_messages={
            "blank": "请输入验证码",
            "min_length": "验证码为4位",
            "max_length": "验证码为4位",
        }
    )
    uuid = serializers.CharField()
    sms_category = serializers.ChoiceField(choices=("register", "password"))
    username = serializers.CharField(error_messages={"blank": "请输入手机号"})

    def validate(self, attrs):
        conn = get_redis_connection()
        true_code = conn.get(attrs['uuid'])
        if not true_code:
            raise serializers.ValidationError("验证码过期")

        if true_code.decode().lower() != attrs['captcha'].lower():
            raise serializers.ValidationError("验证码错误")

        if not re.match(r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$', attrs['username']):
            raise serializers.ValidationError("手机号非法")

        if attrs["sms_category"] == "register":
            if UserProfile.objects.filter(username=attrs["username"]):
                raise serializers.ValidationError("该账号已被注册")
        else:
            if not UserProfile.objects.filter(username=attrs["username"]):
                raise serializers.ValidationError("该账号不存在")

        if conn.get('sms_mobile_{}'.format(attrs['username'])):
            raise serializers.ValidationError("请60s后发送验证码")

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """注册和修改密码"""
    username = serializers.CharField(error_messages={"blank": "请输入手机号"})
    code = serializers.CharField(
        write_only=True,
        min_length=4,
        max_length=4,
        label='验证码',
        error_messages={
            "blank": "请输入验证码",
            "min_length": "验证码为4位",
            "max_length": "验证码为4位",
        }
    )
    re_password = serializers.CharField(
        required=True,
        write_only=True,
        label='确认密码',
        min_length=6,
        max_length=14,
        error_messages={
            "blank": "请输入密码",
            "required": "请输入密码",
            "min_length": "密码最少为6位",
            "max_length": "密码最多为14位",
        }
    )

    def validate(self, attrs):
        if self.context["request"].method == "POST":
            if UserProfile.objects.filter(username=attrs["username"]):
                raise serializers.ValidationError("该账号已被注册")
        else:
            if not UserProfile.objects.filter(username=attrs["username"]):
                raise serializers.ValidationError("该账号不存在")

        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError('两次密码不一致')

        conn = get_redis_connection()
        sms_category = "password"
        if self.context["request"].method == "POST":
            sms_category = "register"
        true_code = conn.get('sms_{}_{}'.format(sms_category, attrs['username']))

        if not true_code:
            raise serializers.ValidationError('验证码过期')

        if true_code.decode() != attrs['code']:
            raise serializers.ValidationError('验证码错误')
        return attrs

    def create(self, validated_data):
        return UserProfile.objects.create_user(validated_data['username'], password=validated_data['password'])

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 're_password', 'code')
        extra_kwargs = {'password': {'write_only': True}}


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'nickname', 'gender', 'email', 'username', 'desc')
        read_only_fields = ('username',)


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_mobile(self, mobile):
        if not re.match(r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$', mobile):
            raise serializers.ValidationError("手机号非法")
        return mobile

    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {
            'name': {'error_messages': {"blank": "请输入姓名"}},
            'mobile': {'error_messages': {"blank": "请输入手机号"}},
            'province': {'error_messages': {"blank": "请输入省份"}},
            'city': {'error_messages': {"blank": "请输入城市"}},
            'area': {'error_messages': {"blank": "请输入地区"}},
            'detail_address': {'error_messages': {"blank": "请输入详细地址"}},
        }
