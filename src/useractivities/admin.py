from django.contrib import admin

# Register your models here.
from useractivities.models import Comment, Like

admin.site.register(Comment)
admin.site.register(Like)
