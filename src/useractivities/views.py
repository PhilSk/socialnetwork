# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from application.serializers import PostSerializer, EventSerializer, CommentSerializer, LikeSerializer, \
    MeetingSerializer, BirthdaySerializer

from useractivities.models import Post, Event, Comment, Like, Meeting, Birthday

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
        serializer.save(user=unicode(self.request.user))


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        qs = super(EventViewSet, self).get_queryset()
        qs = self.request.user.event_set.all()
        return qs


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class BirthdayViewSet(viewsets.ModelViewSet):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer
