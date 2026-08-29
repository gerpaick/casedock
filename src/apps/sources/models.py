from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublicIDModel, TimeStampedModel


class SourceProvider(models.TextChoices):
    CLICKUP = "clickup", "ClickUp"
    URL = "url", "URL"
    MANUAL = "manual", "Manual"
    OTHER = "other", "Other"


class SourceLink(TimeStampedModel, PublicIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="source_links",
    )
    provider = models.CharField(max_length=16, choices=SourceProvider.choices)
    external_id = models.CharField(max_length=255, blank=True)
    external_url = models.URLField(blank=True)
    external_title_snapshot = models.CharField(max_length=255, blank=True)
    external_status_snapshot = models.CharField(max_length=255, blank=True)
    payload_snapshot = models.JSONField(default=dict, blank=True)
    synced_at = models.DateTimeField(null=True, blank=True)
    inbox_item = models.ForeignKey(
        "inbox.InboxItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="source_links",
    )
    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="source_links",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        target = self.case or self.inbox_item
        return f"{self.provider} link for {target}"

    def clean(self) -> None:
        super().clean()
        has_case = bool(self.case_id)
        has_inbox_item = bool(self.inbox_item_id)
        if has_case == has_inbox_item:
            raise ValidationError(
                "Source links must target exactly one object: either a case or an inbox item."
            )

    def save(self, *args: object, **kwargs: object) -> None:
        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]  # Django save expects specific typed kwargs
