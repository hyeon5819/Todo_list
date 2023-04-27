from django.urls import path
from todo import views

urlpatterns = [
    path('', views.TodoView.as_view(), name='todo'),
]
