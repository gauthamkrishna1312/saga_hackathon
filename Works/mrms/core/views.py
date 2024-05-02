from django.shortcuts import render
from django.views import View



class DoctorProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    user profile page
    """
    template_name = "general/user-profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            "doctor": get_object_or_404(models.Doctor, user=self.request.user)
        })
        return context
