# coding=utf-8
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
from django.contrib import admin

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers

from extuser.views import UserViewSet
from friendship.views import FriendshipViewSet

from pages.views import custom_login, index

from useractivities.views import PostViewSet, EventViewSet, CommentViewSet, LikeViewSet, BirthdayViewSet, MeetingViewSet, \
    PhotoViewSet, AlbumViewSet

from chat.views import ChatViewSet, MessageViewSet
from django.contrib.auth.views import logout
from django.conf.urls.i18n import i18n_patterns

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'posts', PostViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'friendships', FriendshipViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'birthdays', BirthdayViewSet)
router.register(r'meetings', MeetingViewSet)

urlpatterns = [
    url(r'^accounts/login/$', custom_login, {'template_name': 'pages/login.html'},
        name="login"),
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', logout, {'next_page': 'login'}, name="logout"),
    url(r'^i18n/', include('django.conf.urls.i18n')),  # translate page and redirect back
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

urlpatterns += i18n_patterns(
    url(r'^profile/', include('extuser.urls', namespace="profile"))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
