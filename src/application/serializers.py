from rest_framework import serializers
from extuser.models import ExtUser

from useractivities.models import Event, Like, Comment

from usermedia.models import Album, Photo

from friendship.models import Friendship

from chat.models import Chat, Message

from useractivities.models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExtUser
        fields = ('pk', 'friends', 'firstname', 'lastname', 'email', 'is_staff')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('creator', 'name', 'content_type')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('title', 'content', 'created_at', 'updated_at', 'content_type', 'object_id')


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'content_type', 'object_id')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = ('user', 'name', 'description', 'created_at')


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('album', 'preview', 'description', 'added_at', 'photo', 'count_likes', 'count_comments')


class FriendshipSerializer(serializers.HyperlinkedModelSerializer):
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
        fields = ('pk', 'user', 'title', 'content', 'created_at', 'updated_at')
