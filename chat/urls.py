from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats, name='chats'),
    path('<str:name>/', views.lobby, name='chat'),
    path('create_dm_chat/<str:username>/', views.create_dm_chat, name='create_dm_chat'),
    path('create_group_chat/<str:name>/', views.create_group_chat, name='create_group_chat'),
    path('join_chat/<str:name>/', views.join_chat, name='join_chat'),
    path('leave_chat/<str:name>/', views.leave_chat, name='leave_chat')
]