from ast import Delete
from django.shortcuts import render, redirect

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, filters

from .models import Chat, Message
from network.models import SNUser
from .serializers import MessageSerializer


def get_current_user(request):
    username = request.session.get("user")['userinfo']['nickname']
    user = SNUser.objects.get(nickname=username)
    return user


def chats(request):
    user = get_current_user(request=request)
    joined_chats = Chat.objects.filter(chat_members=user)
    new_chats = Chat.objects.exclude(chat_members=user)
    return render(request, 'chat/chats.html', {'chats': joined_chats,  'new_chats': new_chats, 'user': user})


def lobby(request, name):
    chat = Chat.objects.get(name=name)
    messages = Message.objects.filter(chat=chat)
    user = get_current_user(request=request)
    return render(request, 'chat/lobby.html', {'chat': chat, 'messages': messages, 'user': user})


def add_to_chat(request, name):
    chat = Chat.objects.get(name=name)
    chat_members = chat.chat_members
    user = get_current_user(request=request)
    chat_members.add(user)
    return redirect(f'/chat/{name}/')


def leave_chat(request, name):
    chat = Chat.objects.get(name=name)
    chat_members = chat.chat_members
    user = get_current_user(request=request)
    chat_members.remove(user)
    return redirect(f'/chat/')
    

# @api_view(['GET'])
# def get_messages(request, name):
#     if request.method == 'GET':
#         try:
#             chat = Chat.objects.get(name=name)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         messages = Message.objects.filter(chat=chat)
#         serializer = MessageSerializer(messages, many=True)
#         return Response({'data': serializer.data})


