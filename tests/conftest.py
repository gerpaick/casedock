from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")


@pytest.fixture
def user_password() -> str:
    return "test-password-123"


@pytest.fixture
def user(db, user_password):
    from apps.core.models import User

    return User.objects.create_user(
        email="testuser@casedock.local",
        password=user_password,
        is_staff=True,
    )


@pytest.fixture
def client(client, user):
    """Authenticated client — all tests get a logged-in client by default."""
    client.force_login(user)
    return client
