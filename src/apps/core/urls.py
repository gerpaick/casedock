from __future__ import annotations

from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from .forms import EmailAuthenticationForm
from .views import SignupView

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(form_class=EmailAuthenticationForm),
        name="login",
    ),
    # Public trust pages — basic placeholder content, see ADR 2026-07-30.
    path(
        "help/",
        TemplateView.as_view(template_name="core/help.html"),
        name="help",
    ),
    path(
        "privacy/",
        TemplateView.as_view(template_name="core/privacy.html"),
        name="privacy",
    ),
    path(
        "terms/",
        TemplateView.as_view(template_name="core/terms.html"),
        name="terms",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
