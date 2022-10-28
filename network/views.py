from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import *
from .serializers import *


@login_required
def get_userinfo(request):
    return request.session.get("user")['userinfo']


@login_required
def get_current_user(request):
    username = request.ssession.get("user")['userinfo']['nickname']
    user = SNUser.objects.get(nickname=username)
    return user


@api_view(['GET'], ['POST'])
def get_sub_videos(request):
    if request.method == 'GET':
        videos = []
        user = get_current_user(request=request)
        subscribtions_list = Subscription.objects.filter(subscriber=user)
        for subscrption in subscribtions_list.all():
            for video in subscrption.subscribed_to.videos.all():
                videos.append(video)
        serializer = VideoSerializer(videos, many=True)
        return Response({'data': serializer.data})
    elif request.method == 'POST':
        video = Video()
        video.video = request.data['video']
        video.heading = request.data['heading']
        video.text = request.data['text']
        video.author = get_current_user(request=request)
        video.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'], ['POST'])
def get_rec_videos(request):
    if request.method == 'GET':
        videos = Video.objects.all().order_by('-id')
        serializer = VideoSerializer(videos, many=True)
        return Response({'data': serializer.data})
    elif request.method == 'POST':
        video = Video()
        video.video = request.data['video']
        video.heading = request.data['heading']
        video.text = request.data['text']
        video.author = get_current_user(request=request)
        video.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'], ['POST'], ['DELETE'])
def get_comments(request, video_id):
    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(video=video_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comments, many=True)
        return Response({'data': serializer.data})
    elif request.method == 'POST':
        comment = Comment()
        comment.text = request.data['text']
        comment.video = Video.objects.get(id=video_id)
        comment.user = get_current_user(request=request)
        comment.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'], ['DELETE'])
def like_video(request, video_id):
    if request.method == 'GET':
        try:
            video = Video.objects.get(id=video_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        like = Like()
        like.post = video
        like.user = get_current_user(request=request)
        like.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        try:
            video = Video.objects.get(id=video_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_current_user(request=request)
        try:
            like = Like.objects.get(post=video, user=user)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response(status=status.HTTP_200_OK)
        

@api_view(['GET'])
def user_profile(request, username):
    if request.method == 'GET':
        try:
            user = SNUser.objects.get(nickname=username)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(user)
        return Response({'data': serializer.data})


@api_view(['GET'])
def subscribe(request, username):
    if request.method == 'GET':
        try:
            user = SNUser.objects.get(nickname=username)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        subscription = Subscription()
        subscription.subscriber = get_current_user(request=request)
        subscription.subscribed_to = user
        subscription.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def ban_user(request, username):
    if request.method == 'GET':
        try:
            user = SNUser.objects.get(nickname=username)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        ban = Ban()
        ban.banned_by = get_current_user(request=request)
        ban.banned = user
        ban.save()
        return Response(ban.banned, status.HTTP_200_OK)
