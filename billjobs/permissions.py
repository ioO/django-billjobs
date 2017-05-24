from rest_framework import permissions
from rest_framework.compat import is_authenticated

class CustomGroupAPIPermission(permissions.BasePermission):
    """
    Set custom permission for GroupAPI

    * GET   : accessible by admin and user
    * POST  : only accessible by admin
    """

    def has_permission(self, request, view):
        """
        Define permission based on request
        """
        if request.method == 'GET':
            return (
                request.user and
                request.user.is_staff or
                is_authenticated(request.user)
                )
        elif request.method == 'POST':
            return request.user and request.user.is_staff

class CustomGroupDetailAPIPermission(permissions.BasePermission):
    """
    Set custom permission for group detail API

    * GET, UPDATE, DELETE :
        * admin can access all groups instance
        * current user only his groups instance
        * public is forbidden
    """

    def has_permission(self, request, view):
        """
        Give permission for admin or user to access API
        """
        return (
                request.user and
                request.user.is_staff or
                is_authenticated(request.user)
                )

    def has_object_permission(self, request, view, obj):
        """
        Compare User instance in request is equal to User instance in obj
        """
        return request.user.is_staff or obj == request.user

class CustomUserAPIPermission(permissions.BasePermission):
    """
    Set custom permission for UserAPI

    * GET   : only accessible by admin
    * POST  : is public, everyone can create a user
    """

    def has_permission(self, request, view):
        """
        Define permission based on request method
        """
        if request.method == 'GET':
            # admin only
            return request.user and request.user.is_staff

        elif request.method == 'POST':
            # is public
            return True
        # all other methods are accepted to allow 405 response
        return True

class CustomUserDetailAPIPermission(permissions.BasePermission):
    """
    Set custom permission for user detail API

    * GET, PUT, DELETE   :
        * admin can access all users instance
        * current user only his instance
        * public is forbidden
    """
    def has_permission(self, request, view):
        """
        Give permission for admin or user to access API
        """
        return (
                request.user and
                request.user.is_staff or
                is_authenticated(request.user)
                )

    def has_object_permission(self, request, view, obj):
        """
        Compare User instance in request is equal to User instance in obj
        """
        return request.user.is_staff or obj == request.user
