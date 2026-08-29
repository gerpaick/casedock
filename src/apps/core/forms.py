from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm

from .models import User

if TYPE_CHECKING:
    _SignupCreationForm = BaseUserCreationForm[User]
else:
    _SignupCreationForm = BaseUserCreationForm


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True}),
    )


class SignupForm(_SignupCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self) -> str:
        email = str(self.cleaned_data["email"])
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
