from django.shortcuts import render, redirect

from .models import Chat, Message
from network.models import SNUser, Subscription


def get_current_user(request):
    username = request.session.get("user")['userinfo']['nickname']
    user = SNUser.objects.get(nickname=username)
    return user


def chats(request):
    user = get_current_user(request=request)
    joined_chats = Chat.objects.filter(chat_members=user)
    new_chats = Chat.objects.exclude(chat_members=user)
    sub_to = Subscription.objects.filter(subscriber=user)
    return render(request, 'chat/chats.html', {
        'chats': joined_chats,
        'new_chats': new_chats,
        'sub_to' :sub_to,
        'user': user
    })


def lobby(request, name):
    chat = Chat.objects.get(name=name)
    messages = Message.objects.filter(chat=chat)
    user = get_current_user(request=request)
    return render(request, 'chat/lobby.html', {'chat': chat, 'messages': messages, 'user': user})


def create_group_chat(request, name):
    user = get_current_user(request=request)
    new_chat = Chat.objects.create(name=name)
    new_chat.save()
    new_chat.chat_members.add(user)
    return redirect(f'/chat/{name}')


def create_dm_chat(request, username):
    user = get_current_user(request=request)
    dm_name = f'{username}_{user.nickname}'
    dm_user = SNUser.objects.get(nickname=username)
    exists = Chat.objects.filter(name=dm_name).exists()
    if exists:
        chat = Chat.objects.get(name=dm_name)
        chat.chat_members.add(user)
        return redirect(f'/chat/{dm_name}')
    else:
        new_chat = Chat.objects.create(name=dm_name)
        new_chat.save()
        new_chat.chat_members.add(user)
        new_chat.chat_members.add(dm_user)
        return redirect(f'/chat/{dm_name}')


def join_chat(request, name):
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