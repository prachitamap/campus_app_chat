from django.db import models
from django.utils import timezone
# Create your models here.
from logs.models import CUser
from products.models import Item

class ChatSession(models.Model):
    seller = models.ForeignKey(CUser, on_delete=models.CASCADE, related_name='seller_chats')
    buyer = models.EmailField(blank=True,null=True)
    items = models.ManyToManyField(Item, related_name='chat_sessions')

    class Meta:
        unique_together = ('buyer', 'seller')

    def __str__(self):
        return f'{self.buyer} - {self.seller.email}'



class Message(models.Model):
    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.EmailField(blank=True,null=True)
    recipient = models.EmailField(blank=True,null=True)
    content=models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)
   
    def __str__(self):
        return f'Message from {self.sender} in chat {self.chat.id}: {self.content}'

        