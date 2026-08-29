from __future__ import annotations

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import SignupForm


class SignupView(View):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form}, status=400)
        user = form.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
