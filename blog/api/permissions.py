from rest_framework import permissions


class AuthorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
# use of permissions.SAFE_METHODS is not known
        return request.user == obj.author


# DRF does not know about your objects, so it does not have a way of checking permissions. Therefore, IsAdminUser will always return True. By subclassing IsAdminUser, you can create a method that corresponds to your object.
class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)

#is_staff is to check admin status