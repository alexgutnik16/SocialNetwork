from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import *
from .serializers import *


def get_current_user(request):
    # print('request', request.session.get("user")['userinfo']['nickname'])
    # username = request.session.get("user")['userinfo']['nickname']
    print(request)
    username = 'Alex'
    user = SNUser.objects.get(nickname=username)
    return user


@api_view(['GET'])
def api_get_current_user(request):
    if request.method == 'GET':
        try:
            user = get_current_user(request=request)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response({'data': serializer.data})


@api_view(['GET'])
def get_profile(request, username):
    if request.method == 'GET':
        try:
            user = SNUser.objects.get(nickname=username)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response({'data': serializer.data})


@api_view(['GET', 'POST'])
def get_sub_videos(request):
    if request.method == 'GET':
        user = get_current_user(request=request)
        subscribtions_list = Subscription.objects.filter(subscriber=user)
        sub_to_ids = []
        for subscrption in subscribtions_list.all():
            sub_to_ids.append(subscrption.subscribed_to.id)
        videos = Video.objects.filter(author__in=sub_to_ids)
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


@api_view(['GET', 'POST'])
def get_rec_videos(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query == None:
            query = ''
        videos = Video.objects.filter(heading__icontains=query).order_by('-id')
        serializer = VideoSerializer(videos, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        video = Video()
        video.video = request.FILES.get('video')
        video.heading = request.data['heading']
        video.text = request.data['text']
        video.author = get_current_user(request=request)
        video.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def get_video(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = VideoSerializer(video, many=False)
        return Response({'data': serializer.data})

    elif request.method == 'DELETE':
        user = get_current_user(request=request)
        if user == video.author:
            video.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'POST'])
def get_comments(request, video_id):
    if request.method == 'GET':
        try:
            video = Video.objects.get(id=video_id)
            comments = Comment.objects.filter(video=video)
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


@api_view(['GET', 'DELETE'])
def get_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = CommentSerializer(comment, many=False)
        return Response({'data': serializer.data})

    elif request.method == 'DELETE':
        user = get_current_user(request=request)
        if user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_likes(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
        likes = Like.objects.filter(post=video)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = LikeSerializer(likes, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        like = Like()
        like.post = video
        like.user = get_current_user(request=request)
        like.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def get_like(request, like_id):
    try:
        like = Like.objects.get(id=like_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = LikeSerializer(like, many=False)
        return Response({'data': serializer.data})

    elif request.method == 'DELETE':
        user = get_current_user(request=request)
        if user == like.user:
            like.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_subscribtions(request, username):
    try:
        user = SNUser.objects.get(nickname=username)
        subscriptions = Subscription.objects.filter(subscriber=user)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response({'data': serializer.data})

    if request.method == 'POST':
        if user != get_current_user(request=request):
            subscription = Subscription()
            subscription.subscriber = get_current_user(request=request)
            subscription.subscribed_to = user
            subscription.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_subscribed(request, username):
    try:
        user = SNUser.objects.get(nickname=username)
        subscriptions = Subscription.objects.filter(subscribed_to=user)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response({'data': serializer.data})

    if request.method == 'POST':
        if user != get_current_user(request=request):
            subscription = Subscription()
            subscription.subscriber = get_current_user(request=request)
            subscription.subscribed_to = user
            subscription.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET', 'DELETE'])
def get_subscribtion(request, subscribtion_id):
    try:
        subscription = Subscription.objects.get(id=subscribtion_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscription, many=False)
        return Response({'data': serializer.data})

    elif request.method == 'DELETE':
        user = get_current_user(request=request)
        if user == subscription.subscriber:
            subscription.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_bans(request, username):
    try:
        user = SNUser.objects.get(nickname=username)
        bans = Ban.objects.filter(banned_by=user)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = BanSerializer(bans, many=True)
        return Response({'data': serializer.data})

    if request.method == 'POST':
        if user != get_current_user(request=request):
            ban = Ban()
            ban.banned_by = get_current_user(request=request)
            ban.banned = user
            ban.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def get_ban(request, ban_id):
    try:
        ban = Ban.objects.get(id=ban_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = BanSerializer(ban, many=False)
        return Response({'data': serializer.data})

    elif request.method == 'DELETE':
        user = get_current_user(request=request)
        if user == ban.banned_by:
            ban.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)