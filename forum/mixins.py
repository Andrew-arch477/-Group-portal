from django.core.exceptions import PermissionDenied

class UserIsStaffMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'profile') or user.profile.role not in ['admin', 'moderator']:
            raise PermissionDenied(f"You are not a staff")
        return super().dispatch(request, *args, **kwargs)

class UserIsAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.profile.role != 'admin':
            raise PermissionDenied(f"You are not a admin")
        return super().dispatch(request, *args, **kwargs)
