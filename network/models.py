from django.db import models
from django.contrib.auth.models import User


class SNUser(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to='uploads/avatars/', null=True)
    phone_number = models.CharField(max_length=12)
    videos = models.ManyToManyField('Video', null=True)
    likes = models.ForeignKey('Likes', null=True)

    def __str__(self):
        return f'{self.user.username}'


class Video(models.Model):
    video = models.FileField(upload_to='uploads/videos')
    heading = models.CharField(max_length=128)
    text = models.TextField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(SNUser, on_delete=models.CASCADE)
    likes = models.ManyToManyField('Like', null=True)

    def __str__(self):
        return f'{self.heading}'



class Comment(models.Model):
    text = models.TextField(max_length=512)
    creation_date = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(SNUser, on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(SNUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.subscribed_to}'


class Ban(models.Model):
    banned_by = models.ForeignKey(SNUser, on_delete=models.CASCADE)
    banned = models.ForeignKey(SNUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.banned_by} banned {self.banned}'


class Like(models.Model):
    post = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked post {self.post}'
