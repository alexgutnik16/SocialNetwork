from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import *
from network.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer()
    user = UserSerializer()
    class Meta:
        model = Message
        fields = '__all__'