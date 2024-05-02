from django.shortcuts import render
from django.views import View

from . import models


class IndexView(View):

    def get(self, request, *args, **kwargs):