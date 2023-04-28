from django.urls import path
from todo import views

urlpatterns = [
    path('<int:user_id>/', views.TodoView.as_view(),
         name='todo'),        # Todo 리스트 보기, 생성
    path('<int:user_id>/<int:todo_id>/', views.TodoDetailView.as_view(),
         name='todo_detail'),                               # Todo detail 보기, 수정, 완료, 삭제
]
