from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .serializers import TodoCreateSerializer, TodoSerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from todo.models import Todo


# Create your views here.
class TodoView(APIView):
    def get(self, request):
        todo_list = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todo_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        todo = get_object_or_404(Todo, id=request.data['id'])
        if request.user == todo.user:
            serializer = TodoCreateSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        todo = get_object_or_404(Todo, id=request.data['id'])
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
