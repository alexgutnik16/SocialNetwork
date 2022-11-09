from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats, name='chats'),
    path('<str:name>/', views.lobby, name='chat'),
    path('join_chat/<str:name>/', views.add_to_chat, name='join_chat'),
    path('leave_chat/<str:name>/', views.leave_chat, name='leave_chat')
]