from django.contrib import admin
from . models import *
from chat.models import ChatSession, Message
# Register your models here.
admin.site.register(ChatSession)
admin.site.register(Message)
admin.site.register(Item)