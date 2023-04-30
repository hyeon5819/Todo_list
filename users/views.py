from rest_framework.generics import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
# 회원가입
class UserView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!", "profile": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 회원 프로필 보기/수정/삭제
class UserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 프로필 페이지
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 프로필 수정 / 자신만 수정 가능
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if user == request.user:
            # email이 요청에 들어오면 제거해주기
            if "email" in request.data:
                del request.data['email']

            # password 변경 요청을 보냈을때
            elif "password" in request.data:
                serializer = UserPasswordSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.update(user, validated_data=request.data)
                    return Response({"message": "비밀번호 변경 완료!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
            elif not "password" in request.data:
                serializer = UserUpdateSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.update(user, validated_data=request.data)
                    return Response({"message": "수정완료!", "profile": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "접근할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            user.delete()
            return Response({"message": "탈퇴 완료."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "접근할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# PAYLOAD 커스터마이징
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
