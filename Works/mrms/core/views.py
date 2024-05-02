from django.shortcuts import render
from django.views import View, generic

from . import models


class IndexView(generic.TemplateView):
    pass