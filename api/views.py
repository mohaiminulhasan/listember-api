from django.db import transaction
from api.models import ListItem, Profile
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Invite, List, ListItem
from . import serializers

User = get_user_model()

# Create your views here.
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        now = datetime.now()
        then = datetime(1970, 1, 1)
        auth_validity_time = 60 * 60 # in seconds
        time_in_seconds = round((now-then).total_seconds() + auth_validity_time)

        return Response({
            'message': 'Login success!',
            'token': token.key,
            'expiresAt': time_in_seconds,
            'userInfo': {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
        })

@api_view()
@permission_classes([permissions.IsAuthenticated])
def init(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.email_verified:
        # send_mail(
        #     'Listember - Verify Email',
        #     'Hi {}\n\nPlease use the following code to verify your email:\n659386\nRegards,\nThe Listember Team'.format(request.user.username),
        #     'noreply@listember.com',
        #     ['hasan.mohaiminul@gmail.com'],
        #     fail_silently=False
        # )
        return Response({ 'result': 'verify_email' })
    elif not profile.list:
        return Response({ 'result': 'invite' })
    else:
        # objs = ListItem.objects.filter(list=request.user.profile.list)
        # serializer = serializers.ListItemSerializer(objs, many=True)
        return Response({ 'result': 'error' })

class ListItemView(generics.ListAPIView):
    queryset = ListItem.objects.all()
    serializer_class = serializers.ListItemSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def verify_email(request):
    p = Profile.objects.get(user=request.user)
    code = request.data['code']
    if code == p.email_code:
        p.email_verified = True
        p.save()
        return Response({ 'result': 'OK' }, status = 200)
    return Response({ 'result': 'Invalid code' }, status = 404)

@api_view()
@permission_classes([permissions.IsAuthenticated])
def check_sent_invite(request):
    try:
        i = Invite.objects.get(sender=request.user)
        msg = 'You\'ve invited {}'.format(i.receiver.email)
    except Invite.DoesNotExist:
        msg = 'not_found'
    finally:
        return Response({ 'result': msg })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_invite(request):
    email = request.data['email']

    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        u = None
        msg = 'No users found with this email address'
        return Response({ 'result': msg, 'error': 1 })
    else:
        Invite.objects.create(sender=request.user, receiver=u)
        msg = 'Invite sent to {}'.format(u.username)
        return Response({ 'result': msg, 'error': 0 })

class DeleteInvite(generics.DestroyAPIView):
    queryset = Invite.objects.all()
    serializer_class = serializers.InviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        filter = {'sender': self.request.user}
        obj = get_object_or_404(queryset, **filter)
        return obj

class ReceivedInvites(generics.ListAPIView):
    queryset = Invite.objects.all()
    serializer_class = serializers.InviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        objs = Invite.objects.filter(receiver=self.request.user)
        return objs


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic
def accept_invite(request):
    sender = User.objects.get(id=request.data['sender_id'])
    receiver = request.user

    l = List.objects.create()
    receiver.profile.list = l
    receiver.profile.save()
    if (sender.profile.list is None):
        sender.profile.list = l
        sender.profile.save()

    invite = Invite.objects.get(sender=sender)
    invite.delete()
    return Response({ 'result': 'OK' })


class RejectInvite(generics.DestroyAPIView):
    queryset = Invite.objects.all()
    serializer_class = serializers.InviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        filter = {'sender': User.objects.get(id=self.request.data['sender_id'])}
        obj = get_object_or_404(queryset, **filter)
        return obj

class ListAddItemView(generics.CreateAPIView):
    queryset = ListItem.objects.all()
    serializer_class = serializers.ListItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(list=self.request.user.profile.list)

class ListItemDeleteView(generics.DestroyAPIView):
    queryset = ListItem.objects.all()
    serializer_class = serializers.ListItemSerializer
    permission_classes = [permissions.IsAuthenticated]