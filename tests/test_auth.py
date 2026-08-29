from __future__ import annotations

import pytest
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.cases.models import Case, CaseStatus
from apps.core.models import User

pytestmark = pytest.mark.django_db


class TestLoginView:
    def test_login_page_renders_for_anonymous(self, db):
        anon = Client()
        response = anon.get(reverse("login"))
        assert response.status_code == 200
        assert b"Sign in" in response.content

    def test_login_with_valid_credentials(self, db, user_password):
        User.objects.create_user(email="login@example.com", password=user_password)
        anon = Client()
        response = anon.post(
            reverse("login"),
            {"username": "login@example.com", "password": user_password},
        )
        assert response.status_code == 302
        assert response.url == "/"

    def test_login_with_wrong_password(self, db):
        User.objects.create_user(email="wrong@example.com", password="correct-pass")
        anon = Client()
        response = anon.post(
            reverse("login"),
            {"username": "wrong@example.com", "password": "wrong-pass"},
        )
        assert response.status_code == 200
        assert b"Please enter a correct" in response.content

    def test_login_with_nonexistent_email(self, db):
        anon = Client()
        response = anon.post(
            reverse("login"),
            {"username": "nobody@example.com", "password": "anything"},
        )
        assert response.status_code == 200
        assert b"Please enter a correct" in response.content

    def test_authenticated_user_can_still_reach_login_page(self, client):
        response = client.get(reverse("login"))
        assert response.status_code == 200
        assert b"Sign in" in response.content

    def test_login_form_uses_email_field(self, db):
        anon = Client()
        response = anon.get(reverse("login"))
        assert response.status_code == 200
        assert b'type="email"' in response.content
        assert b'autocomplete="email"' in response.content
        assert b"autofocus" in response.content


class TestLogoutView:
    def test_logout_redirects_to_login(self, client):
        response = client.post(reverse("logout"))
        assert response.status_code == 302
        assert response.url == reverse("login")

    def test_logout_rejects_get(self, client):
        response = client.get(reverse("logout"))
        assert response.status_code == 405


class TestPasswordReset:
    def test_password_reset_page_renders(self, db):
        anon = Client()
        response = anon.get(reverse("password_reset"))
        assert response.status_code == 200
        assert b"Reset your password" in response.content

    def test_password_reset_sends_email(self, user):
        anon = Client()
        response = anon.post(
            reverse("password_reset"),
            {"email": user.email},
        )
        assert response.status_code == 302
        assert response.url == reverse("password_reset_done")
        assert len(mail.outbox) == 1
        assert user.email in mail.outbox[0].to

    def test_password_reset_done_page_renders(self, db):
        anon = Client()
        response = anon.get(reverse("password_reset_done"))
        assert response.status_code == 200
        assert b"Check your email" in response.content

    def test_password_reset_confirm_with_valid_token(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        anon = Client()
        response = anon.get(reverse("password_reset_confirm", args=[uid, token]))
        assert response.status_code == 302

        confirm_url = response.url
        response = anon.get(confirm_url)
        assert response.status_code == 200
        assert b"Set a new password" in response.content

        new_password = "brand-new-secure-password-456"
        response = anon.post(
            confirm_url,
            {"new_password1": new_password, "new_password2": new_password},
        )
        assert response.status_code == 302
        assert response.url == reverse("password_reset_complete")

        user.refresh_from_db()
        assert user.check_password(new_password)

    def test_password_reset_confirm_with_invalid_token(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        anon = Client()
        response = anon.get(reverse("password_reset_confirm", args=[uid, "invalid-token"]))
        assert response.status_code == 200
        assert b"Link expired" in response.content

    def test_password_reset_complete_page_renders(self, db):
        anon = Client()
        response = anon.get(reverse("password_reset_complete"))
        assert response.status_code == 200
        assert b"Password updated" in response.content


class TestAnonymousAccessProtection:
    @pytest.fixture
    def anon(self):
        return Client()

    def test_homepage_redirects_anonymous(self, anon, db):
        response = anon.get(reverse("ui:home"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_inbox_redirects_anonymous(self, anon, db):
        response = anon.get(reverse("inbox:list"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_focus_redirects_anonymous(self, anon, db):
        response = anon.get(reverse("focus:today"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_search_redirects_anonymous(self, anon, db):
        response = anon.get(reverse("ui:search"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_settings_redirects_anonymous(self, anon, db):
        response = anon.get(reverse("ui:settings"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_case_detail_redirects_anonymous(self, anon, db, user):
        case = Case.objects.create(user=user, title="Protected case", status=CaseStatus.ACTIVE)
        response = anon.get(reverse("cases:detail", args=[case.public_id]))
        assert response.status_code == 302
        assert "/login/" in response.url


class TestNavVisibility:
    def test_base_template_hides_nav_for_anonymous(self, db):
        anon = Client()
        response = anon.get(reverse("login"))
        assert response.status_code == 200
        assert b'aria-label="Primary"' not in response.content
        assert b"casedock" in response.content

    def test_base_template_shows_nav_and_logout_for_authenticated(self, client):
        response = client.get(reverse("ui:home"))
        assert response.status_code == 200
        assert b'aria-label="Primary"' in response.content
        assert b"Sign out" in response.content
        assert b'action="' in response.content


class TestUserModel:
    def test_user_str_returns_email(self, user):
        assert str(user) == "testuser@casedock.local"

    def test_user_can_authenticate(self, db, user, user_password):
        from django.contrib.auth import authenticate

        authenticated = authenticate(email=user.email, password=user_password)
        assert authenticated is not None
        assert authenticated == user

    def test_user_email_is_unique(self, user):
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            User.objects.create_user(email=user.email, password="another-pass")


class TestSignupView:
    SIGNUP_PASSWORD = "secure-signup-pass-9"

    def test_signup_page_renders_form(self, db):
        anon = Client()
        response = anon.get(reverse("signup"))
        assert response.status_code == 200
        assert b"Sign up" in response.content
        assert b'type="email"' in response.content
        assert b'name="password1"' in response.content
        assert b'name="password2"' in response.content

    def test_signup_creates_user_and_logs_in(self, db):
        anon = Client()
        response = anon.post(
            reverse("signup"),
            {
                "email": "newuser@casedock.local",
                "password1": self.SIGNUP_PASSWORD,
                "password2": self.SIGNUP_PASSWORD,
            },
        )
        assert response.status_code == 302
        assert response.url == "/"
        assert User.objects.filter(email="newuser@casedock.local").count() == 1
        created = User.objects.get(email="newuser@casedock.local")
        assert created.check_password(self.SIGNUP_PASSWORD)
        assert response.wsgi_request.user.is_authenticated
        assert response.wsgi_request.user == created

    def test_signup_rejects_duplicate_email(self, db):
        User.objects.create_user(
            email="taken@casedock.local",
            password=self.SIGNUP_PASSWORD,
        )
        anon = Client()
        response = anon.post(
            reverse("signup"),
            {
                "email": "taken@casedock.local",
                "password1": self.SIGNUP_PASSWORD,
                "password2": self.SIGNUP_PASSWORD,
            },
        )
        assert response.status_code == 400
        assert b"already exists" in response.content
        assert User.objects.filter(email="taken@casedock.local").count() == 1

    def test_signup_redirects_to_home_after_success(self, db):
        anon = Client()
        response = anon.post(
            reverse("signup"),
            {
                "email": "redirect@casedock.local",
                "password1": self.SIGNUP_PASSWORD,
                "password2": self.SIGNUP_PASSWORD,
            },
        )
        assert response.status_code == 302
        assert response.url == "/"
