from django.db import models
from network.models import SNUser


class Chat(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    text = models.TextField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="Chat")
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name="User_from")

    class Meta:
        ordering = ('creation_date',)

    def __str__(self):
        return f'{self.user} to {self.chat}'