from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime

from .models import Chat, Message
from .tasks import notify_message_not_read
from .serializers import MessageSerializer, ChatSerializer
from network.models import SNUser, Subscription


def get_current_user(request):
    username = request.session.get("user")['userinfo']['nickname']
    user = SNUser.objects.get(nickname=username)
    return user


@api_view(['GET'])
def chats(request):
    if request.method == 'GET':
        user = get_current_user(request=request)
        joined_chats = Chat.objects.filter(chat_members=user)
        new_chats = Chat.objects.exclude(chat_members=user)
        sub_to = Subscription.objects.filter(subscriber=user)
        
        serializer_joined_chats = ChatSerializer(joined_chats, many=True)
        serializer_new_chats = ChatSerializer(new_chats, many=True)
        serializer_sub_to = ChatSerializer(sub_to, many=True)

        return Response(
            {'data': {
                {'joined_chats': serializer_joined_chats.data},
                {'new_chats': serializer_new_chats.data},
                {'sub_to': serializer_sub_to.data}
            }}
        )


@api_view(['GET'])
def get_lobby(request, name):
    try:
        chat = Chat.objects.get(name=name)
        messages = Message.objects.filter(chat=chat)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        user = get_current_user(request=request)
        other_user_messages = Message.objects.filter(chat=chat).exclude(user=user)
        for message in other_user_messages.all():
            message.is_read = True
            message.save()
        serializer = MessageSerializer(messages, many=True)
        return Response({'data': serializer.data})


@api_view(['GET', 'POST'])
def create_group_chat(request, name):
    if request.method == 'POST':
        user = get_current_user(request=request)
        new_chat = Chat.objects.create(name=name)
        new_chat.save()
        new_chat.chat_members.add(user)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_dm_chat(request, username):
    try:
        user = get_current_user(request=request)
        dm_name = f'{username}_{user.nickname}'
        dm_user = SNUser.objects.get(nickname=username)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        new_chat = Chat.objects.create(name=dm_name)
        new_chat.save()
        new_chat.chat_members.add(user)
        new_chat.chat_members.add(dm_user)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def join_chat(request, name):
    if request.method == 'POST':
        chat = Chat.objects.get(name=name)
        chat_members = chat.chat_members
        user = get_current_user(request=request)
        chat_members.add(user)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def leave_chat(request, name):
    if request.method == 'POST':
        chat = Chat.objects.get(name=name)
        chat_members = chat.chat_members
        user = get_current_user(request=request)
        chat_members.remove(user)
        return Response(status=status.HTTP_200_OK)


# def lobby(request, name):
#     chat = Chat.objects.get(name=name)
#     messages = Message.objects.filter(chat=chat)
#     user = get_current_user(request=request)

#     other_user_messages = Message.objects.filter(chat=chat).exclude(user=user)
#     for message in other_user_messages.all():
#         message.is_read = True
#         message.save()

#     return render(request, 'chat/lobby.html', {'chat': chat, 'messages': messages, 'user': user})

# def chats(request):
#     user = get_current_user(request=request)
#     joined_chats = Chat.objects.filter(chat_members=user)
#     new_chats = Chat.objects.exclude(chat_members=user)
#     sub_to = Subscription.objects.filter(subscriber=user)
    
#     return render(request, 'chat/chats.html', {
#         'chats': joined_chats,
#         'new_chats': new_chats,
#         'sub_to' :sub_to,
#         'user': user
#     })

# def create_group_chat(request, name):
#     user = get_current_user(request=request)
#     new_chat = Chat.objects.create(name=name)
#     new_chat.save()
#     new_chat.chat_members.add(user)
#     return redirect(f'/chat/{name}')

# def create_dm_chat(request, username):
#     user = get_current_user(request=request)
#     dm_name = f'{username}_{user.nickname}'
#     dm_user = SNUser.objects.get(nickname=username)
#     exists = Chat.objects.filter(name=dm_name).exists()
#     if exists:
#         chat = Chat.objects.get(name=dm_name)
#         chat.chat_members.add(user)
#         return redirect(f'/chat/{dm_name}')
#     else:
#         new_chat = Chat.objects.create(name=dm_name)
#         new_chat.save()
#         new_chat.chat_members.add(user)
#         new_chat.chat_members.add(dm_user)
#         return redirect(f'/chat/{dm_name}')

# def join_chat(request, name):
#     chat = Chat.objects.get(name=name)
#     chat_members = chat.chat_members
#     user = get_current_user(request=request)
#     chat_members.add(user)
#     return redirect(f'/chat/{name}/')

# def leave_chat(request, name):
#     chat = Chat.objects.get(name=name)
#     chat_members = chat.chat_members
#     user = get_current_user(request=request)
#     chat_members.remove(user)
#     return redirect(f'/chat/')