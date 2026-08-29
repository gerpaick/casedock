from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import PublicIDModel, TimeStampedModel


class ExecutionState(models.TextChoices):
    TODO = "todo", "To do"
    DOING = "doing", "Doing"
    DONE = "done", "Done"


class ExecutionItem(TimeStampedModel, PublicIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="execution_items",
    )
    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="execution_items",
    )
    title = models.CharField(max_length=255)
    state = models.CharField(
        max_length=16,
        choices=ExecutionState.choices,
        default=ExecutionState.TODO,
    )
    section = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    note = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("section", "order", "created_at")

    def __str__(self) -> str:
        return self.title

    def save(self, *args: object, **kwargs: object) -> None:
        if self.state == ExecutionState.DONE and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.state != ExecutionState.DONE:
            self.completed_at = None

        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]  # Django save expects specific typed kwargs
