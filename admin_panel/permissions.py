from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    message = "Only Super Admin can perform this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or getattr(user, "role", None) == "super_admin")
        )