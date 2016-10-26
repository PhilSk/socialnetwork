from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework import viewsets
from application.serializers import FriendshipSerializer
from friendship.models import Friendship


class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
