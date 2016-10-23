from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user or request.user.is_staff


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'user' in dir(obj):
            return obj.user == request.user
        if 'author' in dir(obj):
            return obj.author == request.user


class IsInChat(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if 'members' in dir(obj):
            return obj.members.filter(id=request.user.id).exists()