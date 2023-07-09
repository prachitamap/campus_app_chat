from rest_framework import serializers
from .models import CUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CUser
        exclude = ['password','secret_key','expiry_time','groups','user_permissions']