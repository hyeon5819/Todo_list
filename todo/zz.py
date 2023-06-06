# def put(self, request, todo_id, user_id):
#     todo = get_object_or_404(Todo, id=todo_id)

#     # 유저 권한을 위한 확인
#     if request.user == todo.user:
#         serializer = TodoUpdateSerializer(todo, data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             # ↓ 요청 값을 저장한 뒤 완료여부 체크, 완료시간 적용 ↓
#             updated_todo = Todo.objects.get(id=todo_id)

#             # 완료상태가 True인 경우 competion_at 시간을 수정시간과 같게 지정해준다. → datetime or timezone사용
#             if updated_todo.is_complete == True:
#                 updated_todo.completion_at = timezone.now()
#                 updated_todo.save()
#                 serializer_completion_at = TodoSerializer(
#                     updated_todo)
#                 return Response(serializer_completion_at.data, status=status.HTTP_200_OK)

#             # 완료상태가 False인 경우 competion_at 시간을 제거해준다.
#             elif updated_todo.is_complete == False:
#                 updated_todo.completion_at = None
#                 updated_todo.save()
#                 serializer_completion_at = TodoSerializer(
#                     updated_todo)
#                 return Response(serializer_completion_at.data, status=status.HTTP_200_OK)

#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # 유저 본인이 아니면 접근 불가
#     else:
#         return Response({"message": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


class A:
    a = 1

    def hello_a(self):
        print('hello a')


class B:
    b = 2

    def hollo_b(self):
        print('hollo b')


class C(A, B):
    c = 3

    def holle_c(self):
        print('hello c')


temp = C()
print(temp.a)
