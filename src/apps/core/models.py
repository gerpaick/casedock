from __future__ import annotations

from typing import ClassVar

import uuid_utils.compat as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublicIDModel(models.Model):
    """Non-enumerable public identifier alongside the int PK for URL routing.

    Uses UUID7 (time-ordered) to keep indexes healthy on PostgreSQL.
    The int PK stays the internal/join key; ``public_id`` is exposed in URLs.
    """

    public_id = models.UUIDField(
        default=uuid.uuid7,
        unique=True,
        db_index=True,
        editable=False,
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    username = None  # type: ignore[assignment]  # django-stubs limitation: standard email-only user pattern
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects: ClassVar[UserManager] = UserManager()  # type: ignore[assignment]  # custom UserManager

    def __str__(self) -> str:
        return self.email
