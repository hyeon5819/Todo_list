from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User


# 회원 생성 / 수정
class UserSerializer(serializers.ModelSerializer):
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

    def update(self, validated_data, **kwargs):
        print('put요청')
        user = super().create(validated_data, **kwargs)
        password = user.password
        user.set_password(password)
        # user.fullname = kwargs["fullname", ""]            / fullname
        # user.gender = kwargs["gender", ""]                / gender
        # user.age = kwargs["age", ""]                      / age
        # user.introduction = kwargs["introduction", ""]    / introduction
        user.save()
        return user


# 회원 리스트
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# PAYLOAD 커스터마이징
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token
