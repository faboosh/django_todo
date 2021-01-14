"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views
from todo import views

urlpatterns = format_suffix_patterns([
    path('api/todolists/', views.TodoLists.as_view(), name='todo-lists'),
    path('api/todolists/<int:pk>/', views.TodoListDetail.as_view()),
    path('api/todolists/<int:list_pk>/todos/', views.Todos.as_view(), name='todos'),
    path('api/todolists/<int:list_pk>/todos/<int:pk>/', views.TodoDetail.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterUser.as_view(), name='register'),
])

urlpatterns += [
    path('admin/', admin.site.urls),
]
