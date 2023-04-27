from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from rest_framework.response import Response


# 회원 생성
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data, **kwargs):  # "fullname", "gender", "age", "introduction"
        user = super().create(validated_data, **kwargs)
        password = user.password
        user.set_password(password)
        # user.fullname = kwargs["fullname", ""]            / fullname
        # user.gender = kwargs["gender", ""]                / gender
        # user.age = kwargs["age", ""]                      / age
        # user.introduction = kwargs["introduction", ""]    / introduction
        user.save()
        return user


# 회원 프로필
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "fullname", "gender",
                  "age", "introduction", "last_login",]


# 회원 정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ["fullname", "gender", "age", "introduction",]
        # exclude = ('email', 'password',)

    def update(self, instance, validated_data):
        print(validated_data)
        if "password" in validated_data:
            user = super().update(instance, validated_data)
            password = user.password
            user.set_password(password)
            user.save()
            return user
        else:
            user = super().update(instance, validated_data)
            user.save()
            return user


# PAYLOAD 커스터마이징
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token
