# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('shared/', views.shared, name='shared'),
    path('article/', views.article_info, name='article_info'),
]
