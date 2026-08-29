from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublicIDModel, TimeStampedModel, User


class InboxSourceType(models.TextChoices):
    MANUAL = "manual", "Manual"
    CLICKUP = "clickup", "ClickUp"
    URL = "url", "URL"
    NOTE = "note", "Note"
    OTHER = "other", "Other"


class InboxItemState(models.TextChoices):
    NEW = "new", "New"
    DOING_NOW = "doing_now", "Doing now"
    CONVERTED = "converted", "Converted"
    PARKED = "parked", "Set aside"
    WAITING = "waiting", "Waiting on"
    DONE = "done", "Done"
    ARCHIVED = "archived", "Archived"


READY_INBOX_STATES = (
    InboxItemState.DOING_NOW,
    InboxItemState.NEW,
    InboxItemState.WAITING,
    InboxItemState.PARKED,
)


INBOX_ALLOWED_TRANSITIONS = {
    InboxItemState.NEW: {
        InboxItemState.DOING_NOW,
        InboxItemState.CONVERTED,
        InboxItemState.PARKED,
        InboxItemState.WAITING,
        InboxItemState.DONE,
        InboxItemState.ARCHIVED,
    },
    InboxItemState.DOING_NOW: {
        InboxItemState.CONVERTED,
        InboxItemState.PARKED,
        InboxItemState.WAITING,
        InboxItemState.DONE,
        InboxItemState.ARCHIVED,
    },
    InboxItemState.CONVERTED: {InboxItemState.ARCHIVED},
    InboxItemState.PARKED: {
        InboxItemState.NEW,
        InboxItemState.DOING_NOW,
        InboxItemState.CONVERTED,
        InboxItemState.WAITING,
        InboxItemState.ARCHIVED,
    },
    InboxItemState.WAITING: {
        InboxItemState.NEW,
        InboxItemState.DOING_NOW,
        InboxItemState.CONVERTED,
        InboxItemState.DONE,
        InboxItemState.ARCHIVED,
    },
    InboxItemState.DONE: {InboxItemState.ARCHIVED},
    InboxItemState.ARCHIVED: set(),
}


class InboxItem(TimeStampedModel, PublicIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inbox_items",
    )
    title = models.CharField(max_length=255)
    source_type = models.CharField(
        max_length=16,
        choices=InboxSourceType.choices,
        default=InboxSourceType.MANUAL,
    )
    raw_body = models.TextField(blank=True)
    completion_note = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    triage_state = models.CharField(
        max_length=16,
        choices=InboxItemState.choices,
        default=InboxItemState.NEW,
    )
    converted_case = models.OneToOneField(
        "cases.Case",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_inbox_item",
    )

    class Meta:
        ordering = ("-updated_at", "-created_at")

    def __str__(self) -> str:
        return self.title

    @property
    def visible_source_type_label(self) -> str:
        if self.source_type == InboxSourceType.MANUAL:
            return ""
        return self.get_source_type_display()

    def clean(self) -> None:
        super().clean()
        if self.triage_state == InboxItemState.CONVERTED and not self.converted_case_id:
            raise ValidationError({"converted_case": "Converted inbox items must point to a case."})
        if (
            self.triage_state not in (InboxItemState.CONVERTED, InboxItemState.ARCHIVED)
            and self.converted_case_id
        ):
            raise ValidationError(
                {
                    "triage_state": (
                        "Only converted (or archived-after-conversion) inbox items can keep "
                        "a converted case reference."
                    )
                }
            )

    def save(self, *args: object, **kwargs: object) -> None:
        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]  # Django save expects specific typed kwargs

    def transition_to(self, new_state: str, *, save: bool = True) -> None:
        current_state = InboxItemState(self.triage_state)
        if new_state == current_state:
            return

        allowed_states = INBOX_ALLOWED_TRANSITIONS[current_state]
        if new_state not in allowed_states:
            raise ValidationError(
                {
                    "triage_state": (
                        f"Cannot transition inbox item from {current_state} to {new_state}."
                    )
                }
            )

        self.triage_state = new_state
        if save:
            self.save(update_fields=["triage_state", "updated_at"])


def get_inbox_to_address_count(user: User) -> int:
    return InboxItem.objects.filter(user=user, triage_state__in=READY_INBOX_STATES).count()
