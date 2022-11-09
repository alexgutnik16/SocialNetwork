from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats, name='chats'),
    path('<str:name>/', views.lobby, name='chat')
]