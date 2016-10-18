from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from application.serializers import PostSerializer

from useractivities.models import Post

from rest_framework import permissions
from application.permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        qs = super(PostViewSet, self).get_queryset()
        if self.request.query_params.get('user_id'):
            qs = qs.filter(user__id=self.request.query_params.get('user_id'))
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
