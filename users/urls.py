from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('list/', views.UserList.as_view(), name='user_list'),
    path('update/<int:user_id>/', views.UserUpdate.as_view(), name='user_update'),
    path('api/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
