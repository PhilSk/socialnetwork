from django.shortcuts import render

# Create your views here.
from application.serializers import UserSerializer
from extuser.models import ExtUser
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = ExtUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        serializer.save(sender=serializer.data.receiver, receiver=self.request.user)


def profile(request):
    return render(request, 'extuser/profile.html')
