from __future__ import annotations

from .base import *  # noqa: F403
from .base import env

# Production — casedock behind Caddy (TLS terminator) + WhiteNoise.
# Verify with: manage.py check --deploy

DEBUG = False

# WhiteNoiseMiddleware must sit directly after SecurityMiddleware and before
# every other middleware (whitenoise 6.x docs).
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Caddy terminates TLS, forwards over HTTP to gunicorn.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Caddy also does the http→https redirect at the edge; Django must not duplicate it.
SECURE_SSL_REDIRECT = False

# HSTS owned by Caddy (single source of truth for TLS-layer headers).
# HSTS_SECONDS=0 keeps `manage.py check --deploy` quiet while Django stays out
# of HSTS — Caddyfile emits the Strict-Transport-Security header.
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

DATABASES = {
    "default": {
        **env.db("DATABASE_URL"),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }
}

# Caddy owns HSTS and HTTP→HTTPS redirect (single source of truth for TLS-layer
# concerns). Silencing these two deploy checks so `manage.py check --deploy`
# stays clean. If you ever drop Caddy, remove this list and re-enable the
# corresponding settings above.
SILENCED_SYSTEM_CHECKS = [
    "security.W004",  # SECURE_HSTS_SECONDS not set — emitted by Caddy instead
    "security.W008",  # SECURE_SSL_REDIRECT False — Caddy redirects at the edge
]
