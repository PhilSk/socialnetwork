# -*- coding: utf-8 -*-
from rest_framework import serializers
from extuser.models import ExtUser

from useractivities.models import Event, Like, Comment, Birthday, Meeting, Photo, Album, BaseEvent

from friendship.models import Friendship

from chat.models import Chat, Message

from useractivities.models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExtUser
        fields = ('pk', 'avatar', 'friendships', 'firstname', 'lastname', 'email', 'is_staff')


class EventRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `event_object` generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, BaseEvent):
            if isinstance(value, Post):
                serializer = PostSerializer(value)
            if isinstance(value, Meeting):
                serializer = MeetingSerializer(value)
            if isinstance(value, Comment):
                serializer = CommentSerializer(value)
            if isinstance(value, Friendship):
                serializer = FriendshipSerializer(value)
            if isinstance(value, Photo):
                serializer = PhotoSerializer(value)
        else:
            raise Exception('Unexpected type of event object')

        return serializer.data


class EventSerializer(serializers.ModelSerializer):
    content_object = EventRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'user', 'name', 'users_to_show', 'content_type', 'object_id', 'content_object')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'created_at', 'updated_at', 'content_type', 'object_id')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'content_type', 'object_id')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('user', 'name', 'description', 'created_at')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('album', 'preview', 'description', 'added_at', 'photo', 'count_likes', 'count_comments')


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('id', 'sender', 'receiver')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('name', 'members', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('pk', 'author', 'chat', 'text', 'created_at', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Post
        fields = (
            'pk', 'user', 'title', 'content', 'created_at',
            'updated_at', 'attachment', 'count_likes', 'count_comments'
        )


class BirthdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Birthday
        fields = ('pk', 'user', 'when')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('pk', 'user', 'participants', 'description', 'duration', 'when')
