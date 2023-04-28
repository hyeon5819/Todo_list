from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from todo.models import Todo


# Create your views here.
# Todo 리스트 보기 / 생성
class TodoView(APIView):
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
            serializer = TodoUpdateSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()

                # ↓ 요청 값을 저장한 뒤 완료여부 체크, 완료시간 적용 ↓
                updated_todo = Todo.objects.get(id=todo_id)

                # 완료상태가 True인 경우 competion_at 시간을 수정시간과 같게 지정해준다.
                if updated_todo.is_complete == True:
                    updated_todo.completion_at = updated_todo.updated_at
                    updated_todo.save()
                    serializer_completion_at = TodoSerializer(
                        updated_todo)
                    return Response(serializer_completion_at.data, status=status.HTTP_200_OK)

                # 완료상태가 False인 경우 competion_at 시간을 제거해준다.
                elif updated_todo.is_complete == False:
                    updated_todo.completion_at = None
                    updated_todo.save()
                    serializer_completion_at = TodoSerializer(
                        updated_todo)
                    return Response(serializer_completion_at.data, status=status.HTTP_200_OK)
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
