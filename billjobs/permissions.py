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
        elif request.method in ('POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS',
                'HEAD'):
            return request.user and request.user.is_staff

        return False

class CustomGroupDetailAPIPermission(permissions.BasePermission):
    """
    Set custom permission for group detail API

    * GET :
        * admin can access all groups instance
        * current user only his groups instances
        * public is forbidden
    * UPDATE, DELETE :
        * admin can access all groups instance
        * current user and public is forbidden
    """

    def has_permission(self, request, view):
        """
        Define permissions base on request.method
        """
        if request.method == 'GET':
            return (
                    request.user and
                    request.user.is_staff or
                    is_authenticated(request.user)
                    )
        elif request.method in ('POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS',
                'HEAD'):
            return request.user and request.user.is_staff

        return False

    def has_object_permission(self, request, view, obj):
        """
        User instance in request is member of the group in obj instance
        Allow object access only for GET method for user
        """
        if request.method == 'GET':
            for group in request.user.groups.all():
                if group.id == obj.id:
                    return True
        return request.user.is_staff

class CustomUserAPIPermission(permissions.BasePermission):
    """
    Set custom permission for UserAPI

    * GET   : accessible by admin and authenticated users
    * POST  : is public, everyone can create a user
    * PUT, DELETE, PATCH, OPTIONS, HEAD : accessible by admin
    """

    def has_permission(self, request, view):
        """
        Define permission based on request method
        """
        if request.method == 'GET':
            return (
                request.user and
                request.user.is_staff or
                is_authenticated(request.user)
                )

        elif request.method == 'POST':
            # is public
            return True
        # other HTTP method allowed to admin, others get 401/403
        return request.user and request.user.is_staff

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
        if request.method in ('GET', 'PUT', 'DELETE'):
            return (
                request.user and
                request.user.is_staff or
                is_authenticated(request.user)
                )
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """
        Compare User instance in request is equal to User instance in obj
        """
        return request.user.is_staff or obj == request.user
