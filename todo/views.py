from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions
from users.models import User
from todo.models import Todo
from datetime import datetime
from django.utils import timezone


# Create your views here.
# Todo 리스트 보기 / 생성
class TodoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 리스트 보기
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            todo_list = Todo.objects.filter(user=user)
            serializer = TodoSerializer(todo_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

    # 할일 생성
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = TodoCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


# Todo detail 수정 / 삭제
class TodoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Todo detail보기
    def get(self, request, todo_id, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            todo = get_object_or_404(Todo, id=todo_id)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정
    def put(self, request, todo_id, user_id):
        todo = get_object_or_404(Todo, id=todo_id)

        # 유저 권한을 위한 확인
        if request.user == todo.user:

            # 완료 여부 요청시
            if 'is_complete' in request. data:

                # 미완료 → 완료시 시간 저장
                if request.data['is_complete'] == True and todo.completion_at == None:
                    request.data['completion_at'] = timezone.now()
                    request.data['created_at'] = timezone.now()
                    serializer = TodoUpdateSerializer(todo, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # 미완료 상태시 완료시간 제거
                elif request.data['is_complete'] == False:
                    request.data['completion_at'] = None
                    serializer = TodoUpdateSerializer(todo, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # 완료상태에서 is_complete == True요청이 추가로 들어오게 되는경우 처음 완료시점시간이 유지되도록 해준다.
                else:
                    serializer = TodoUpdateSerializer(todo, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # is_complete 요청 없이 내용수정만 진행될 때
            else:
                serializer = TodoUpdateSerializer(todo, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 유저 본인이 아니면 접근 불가
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

    # Todo 삭제
    def delete(self, request, todo_id, user_id):
        todo = get_object_or_404(Todo, id=todo_id)

        # 작성자만 삭제 가능하게
        if request.user == todo.user:
            todo.delete()
            return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
