
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
# from .models import ChatSession

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        # session = ChatSession.objects.get(id=self.session_id)
        # seller = session.seller
        # self.session_group_name = f'chat_{seller.username}'

        self.session_group_name = f'chat_{self.session_id}'    
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
        self.session_group_name,
        self.channel_name
        )

        self.accept()
     
    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.session_group_name,
            self.channel_name
        )

    def receive(self,text_data):
        message = json.loads(text_data)
        content = message.get('content')
        print(content)

        self.send(text_data=json.dumps({
            'type':'chat',
            'content':content
        }))
        async_to_sync(self.channel_layer.group_send)(
            self.session_group_name, 
            {
                'type': 'chat_message',
                'content': content
            }
        )
    def chat_message(self, event):
        content = event['content']
        self.send(text_data=json.dumps({
            'type':'chat',
            'content': content
            }))
