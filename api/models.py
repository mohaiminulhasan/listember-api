import uuid as uuid_lib
from django.db import models
from django.contrib.auth import get_user_model

from .utils import random_string


class List(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)

    def __str__(self) -> str:
        return str(self.uuid)

class ListItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(List, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=255)
    checked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.SET_NULL, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_code = models.CharField(max_length=5, default=random_string)

    def __str__(self) -> str:
        return "{}'s profile".format(self.user)

class Invite(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sender = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='invites_received', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['sender', 'receiver']

    def __str__(self) -> str:
        return '{} -> {}'.format(self.sender, self.receiver)