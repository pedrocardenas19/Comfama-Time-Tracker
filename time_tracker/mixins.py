from django.core.exceptions import PermissionDenied

class StaffRequiredMixin:
    """Verify that the current user is staff."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
