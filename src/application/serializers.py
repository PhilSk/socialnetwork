from rest_framework import serializers
from extuser.models import ExtUser

from useractivities.models import Event, Like, Comment, Birthday, Meeting

from usermedia.models import Album, Photo

from friendship.models import Friendship

from chat.models import Chat, Message

from useractivities.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtUser
        fields = ('pk', 'avatar', 'friendships', 'firstname', 'lastname', 'email', 'is_staff')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('user', 'name', 'users_to_show', 'content_type')


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
        fields = ('sender', 'receiver')


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
        fields = ('pk', 'user', 'title', 'content', 'created_at', 'updated_at', 'count_likes', 'count_comments')


class BirthdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Birthday
        fields = ('pk', 'user', 'when')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('pk', 'user', 'participants', 'description', 'duration', 'when')


