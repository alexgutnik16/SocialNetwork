from django.contrib import admin
from django.urls import re_path
from network import views


urlpatterns = [
    re_path(r'^api/get_profile/(?P<username>\w+)$', views.get_profile),
    re_path(r'^api/get_current_user', views.api_get_current_user),
    re_path(r'^api/get_sub_videos', views.get_sub_videos),
    re_path(r'^api/get_rec_videos', views.get_rec_videos),
    re_path(r'^api/get_video/(?P<video_id>[0-9]+)$', views.get_video),
    re_path(r'^api/get_comments/(?P<video_id>[0-9]+)$', views.get_comments),
    re_path(r'^api/get_comment/(?P<comment_id>[0-9]+)$', views.get_comment),
    re_path(r'^api/get_likes/(?P<video_id>[0-9]+)$', views.get_likes),
    re_path(r'^api/get_like/(?P<like_id>[0-9]+)$', views.get_like),  
    re_path(r'^api/get_subscribtions/(?P<username>\w+)$', views.get_subscribtions),
    re_path(r'^api/get_subscribed/(?P<username>\w+)$', views.get_subscribed),
    re_path(r'^api/get_subscribtion/(?P<subscribtion_id>[0-9]+)$', views.get_subscribtion),
    re_path(r'^api/get_bans/(?P<username>\w+)$', views.get_bans),
    re_path(r'^api/get_ban/(?P<ban_id>[0-9]+)$', views.get_ban),
]