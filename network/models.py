from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class SNUser(models.Model):
    nickname = models.CharField(max_length=16)
    mail = models.CharField(max_length=32)

    photo = models.ImageField(upload_to='uploads/avatars/', blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    verified = models.BooleanField(default=False)

    videos = models.ManyToManyField('Video', blank=True)
    subscribtions = models.ManyToManyField('Subscription', blank=True)
    black_list = models.ManyToManyField('Ban', blank=True)
    likes = models.ManyToManyField('Like', blank=True)

    def __str__(self):
        return f'{self.nickname}'


class Video(models.Model):
    video = models.FileField(upload_to='uploads/videos', validators=[
            FileExtensionValidator(
                allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
            )
        ]
    )
    heading = models.CharField(max_length=128)
    text = models.TextField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(SNUser, on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', blank=True, related_name="Comments")
    likes = models.ManyToManyField('Like', blank=True)

    def __str__(self):
        return f'{self.heading}'


class Comment(models.Model):
    text = models.TextField(max_length=512)
    creation_date = models.DateTimeField(auto_now_add=True)

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="Video")
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name="Users")

    def __str__(self):
        return f'{self.text}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name="Subscriber")
    subscribed_to = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name="Subscribed_to")

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.subscribed_to}'


class Ban(models.Model):
    banned_by = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name="Banned_by")
    banned = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name="Banned")
    
    def __str__(self):
        return f'{self.banned_by} banned {self.banned}'


class Like(models.Model):
    post = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="Post")
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name="User")

    def __str__(self):
        return f'{self.user} liked post {self.post}'
