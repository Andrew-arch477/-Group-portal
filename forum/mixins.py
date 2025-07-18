from django.core.exceptions import PermissionDenied
from django.utils import timezone

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


class TodayMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context
