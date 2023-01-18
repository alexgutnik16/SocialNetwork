from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SNUser
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['text', 'creation_date', 'video', 'user']
    

class VideoSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        # fields = '__all__'
        fields = ['id', 'video', 'heading', 'text', 'creation_date', 'author', 'comments', 'likes']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = UserSerializer()
    subscribed_to = UserSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'


class BanSerializer(serializers.ModelSerializer):
    banned_by = UserSerializer()
    banned = UserSerializer()

    class Meta:
        model = Ban
        fields = '__all__'