from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.Register, name='register'),
    path('exit/', views.exit, name='exit'),
    path('login/', views.login, name='login'),  
]
