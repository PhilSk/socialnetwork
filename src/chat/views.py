from django.shortcuts import render


# Create your views here.
from rest_framework import viewsets
from chat.models import Chat

from application.serializers import ChatSerializer, MessageSerializer

from chat.models import Message

from rest_framework import permissions
from application.permissions import IsOwner, IsInChat


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated, IsInChat]

    def get_queryset(self):
        qs = super(ChatViewSet, self).get_queryset()
        if self.request.query_params.get('user_id'):
            qs = qs.filter(members=self.request.query_params.get('user_id'))
        return qs


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        qs = super(MessageViewSet, self).get_queryset()
        if self.request.query_params.get('user_id'):
            qs = qs.filter(author=self.request.query_params.get('user_id'))
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
