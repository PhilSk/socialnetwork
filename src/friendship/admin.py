from django.contrib import admin

# Register your models here.
from models import Friendship


class FriendshipInline(admin.StackedInline):
    model = Friendship
    fk_name = 'sender'


admin.site.register(Friendship)
