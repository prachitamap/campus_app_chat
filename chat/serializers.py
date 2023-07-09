from rest_framework import serializers
from .utils import CustomJSONEncoder
from chat.models import Message,ChatSession

class MessageSerializer(serializers.ModelSerializer):
    content = serializers.JSONField(encoder=CustomJSONEncoder)

    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['chat'] = instance.chat.id
        return representation
    
class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'

