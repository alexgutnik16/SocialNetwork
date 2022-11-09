from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SNUser
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Video
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class BanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ban
        fields = '__all__'