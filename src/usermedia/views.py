from django.shortcuts import render

# Create your views here.
from application.serializers import PhotoSerializer, AlbumSerializer
from usermedia.models import Photo, Album
from rest_framework import viewsets


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
