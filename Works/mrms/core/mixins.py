from django.core.exceptions import PermissionDenied


class RoleRequiredMixin:
    role = None

    def dispatch(self, request, *args, **kwargs):
        if self.role == self.request.user.role:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("you are not authorized")