from django.urls import path
from .views import create_chat_session,chat_list,chat_details


urlpatterns = [

    path('chat/', create_chat_session, name='chat-create'),
    path('chat_list/', chat_list, name='chat-list'),
    path('chat_details/', chat_details, name='chat-details'),
]