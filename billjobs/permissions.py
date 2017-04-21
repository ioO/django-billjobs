from rest_framework import permissions

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
