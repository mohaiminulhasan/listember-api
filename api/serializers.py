from rest_framework import serializers
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ListItem
        fields = ['id', 'text', 'checked', 'created']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class InviteSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = models.Invite
        fields = ['id', 'created', 'sender', 'receiver']
