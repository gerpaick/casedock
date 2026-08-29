from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublicIDModel, TimeStampedModel


class Decision(TimeStampedModel, PublicIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="decisions",
    )
    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="decisions",
    )
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    tag = models.CharField(max_length=64, blank=True)
    promoted = models.BooleanField(default=False)
    rationale = models.TextField(blank=True)
    alternatives = models.TextField(blank=True)
    consequence = models.TextField(blank=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.title or self.body[:50]

    def clean(self) -> None:
        super().clean()
        if self.promoted and not self.title:
            raise ValidationError({"title": "Promoted decisions require a title."})

    def save(self, *args: object, **kwargs: object) -> None:
        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]  # Django save expects specific typed kwargs
