import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async

from .models import Chat, Message
from network.models import SNUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.chat_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.chat_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chat = data['chat']

        await self.save_message(message, chat, username)

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chat': chat,            
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat = event['chat']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat': chat,         
        }))

    @sync_to_async
    def save_message(self, message, chat, username):
        user = SNUser.objects.get(nickname=username)
        chat = Chat.objects.get(name=chat)

        Message.objects.create(
            text=message,
            chat=chat,
            user=user
        )