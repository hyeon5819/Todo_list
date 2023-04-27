from rest_framework.generics import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
# 회원가입
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!", "profile": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 회원 리스트
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


# 회원 정보 보기/수정
class UserUpdate(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            serializer = UserListSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "접근할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# PAYLOAD 커스터마이징
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
