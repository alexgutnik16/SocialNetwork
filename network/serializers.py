from rest_framework import serializers
from .models import *


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('video', 'heading', 'text', 'creation_date', 'author', 'comments', 'likes')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SNUser
        fields = ('nickname', 'photo')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'creation_date', 'video', 'user')