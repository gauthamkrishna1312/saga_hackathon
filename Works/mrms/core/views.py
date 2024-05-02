from django.shortcuts import render
from django.views import View, generic

from . import models


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "patients": models.Customer.objects.all(),
            "doctors": models.Doctor.objects.all(),
            "hospitals": models.Hospital.objects.all(),
        })
        return context