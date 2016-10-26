from django.conf.urls import url

from extuser.views import profile

urlpatterns = [
    url(r'^$', profile, name='profile'),
]
