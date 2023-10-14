from rest_framework import permissions


class IsSuperuserOrOwner(permissions.BasePermission):
    message = 'You must be the admin or owner of this object.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.creator == request.user
