"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
from extuser.models import ExtUser

# ViewSets define the view behavior.
from application.serializers import UserSerializer

from application.serializers import CommentSerializer

from application.serializers import LikeSerializer

from application.serializers import EventSerializer

from application.serializers import AlbumSerializer

from application.serializers import PhotoSerializer

from application.serializers import FriendshipSerializer
from friendship.views import FriendshipViewSet

from useractivities.models import Event, Comment, Like

from friendship.models import Friendship

from usermedia.models import Photo, Album

from pages.views import custom_login

from useractivities.views import PostViewSet

from chat.views import ChatViewSet, MessageViewSet

from pages.views import IndexView


class UserViewSet(viewsets.ModelViewSet):
    queryset = ExtUser.objects.all()
    serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'posts', PostViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'friendship', FriendshipViewSet)

urlpatterns = [
    url(r'^login/$', custom_login, {'template_name': 'pages/login.html', 'extra_context': {'next': '/'}},
        name="login"),
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^api/', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('^social/', include('social.apps.django_app.urls', namespace='social')),
]
