from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^api/get_all_chats/(?P<name>\w+)$', views.chats),
    re_path(r'^api/get_lobby/(?P<name>\w+)$', views.get_lobby),
    re_path(r'^api/create_dm_chat/(?P<username>\w+)$', views.create_dm_chat),
    re_path(r'^api/create_group_chat/(?P<name>\w+)$', views.create_group_chat),
    re_path(r'^api/join_chat/(?P<name>\w+)$', views.join_chat),
    re_path(r'^api/leave_chat/(?P<name>\w+)$', views.leave_chat),
    # path('', views.chats, name='chats'),
    # path('create_group_chat/<str:name>/', views.create_group_chat, name='create_group_chat'),
    # path('<str:name>/', views.lobby, name='chat'),
    # path('create_dm_chat/<str:username>/', views.create_dm_chat, name='create_dm_chat'),
    # path('join_chat/<str:name>/', views.join_chat, name='join_chat'),
    # path('leave_chat/<str:name>/', views.leave_chat, name='leave_chat')
]