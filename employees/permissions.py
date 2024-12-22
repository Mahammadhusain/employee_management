from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Permission for Super Admin.
    Super Admin can create any type of user.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'


class IsAdmin(BasePermission):
    """
    Permission for Admin.
    Admin can:
    - Create employees, but not super admins or other admins.
    - Perform other actions on users under their supervision.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Super admins can perform all actions
        if request.user.role == 'super_admin':
            return True
        
        # Admin-specific permissions
        if request.user.role == 'admin':
            # Define actions admins are allowed to perform
            if view.action in ['create', 'update', 'partial_update', 'retrieve', 'list']:
                # If it's a create action, restrict it to creating employees only
                if view.action == 'create':
                    # Extract the `role` from the request data
                    role = request.data.get('role')
                    if role in ['super_admin', 'admin']:
                        return False  # Admins cannot create other admins or super admins
                return True

        # Employees do not have any permission
        return False
