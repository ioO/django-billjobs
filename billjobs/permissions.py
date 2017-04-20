from rest_framework import permissions

class CustomUserAPIPermission(permissions.BasePermission):
    """
    Define custom permission for UserAPI and UserDetailAPI

    GET : only accessible by admin
    POST: public
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user and request.user.is_staff

        elif request.method == 'POST':
            return True
        return True
