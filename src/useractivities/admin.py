from django.contrib import admin

# Register your models here.
from useractivities.models import Event, Birthday, Meeting, Comment, Like, Post

admin.site.register(Event)
admin.site.register(Birthday)
admin.site.register(Meeting)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)
