from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublicIDModel, TimeStampedModel


class FocusRole(models.TextChoices):
    MAIN = "main", "Main"
    SECONDARY = "secondary", "Secondary"


class FocusAssignment(TimeStampedModel, PublicIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="focus_assignments",
    )
    focus_date = models.DateField()
    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="focus_assignments",
    )
    role = models.CharField(max_length=16, choices=FocusRole.choices)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ("-focus_date", "role", "order")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "focus_date", "case"),
                name="uniq_focus_assignment_per_case_per_day",
            ),
            models.UniqueConstraint(
                fields=("user", "focus_date", "role", "order"),
                name="uniq_focus_assignment_slot_per_day",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.focus_date} {self.role} {self.case}"

    def clean(self) -> None:
        super().clean()
        if self.role == FocusRole.MAIN and self.order != 1:
            raise ValidationError({"order": "Main focus must use order 1."})
        if self.role == FocusRole.SECONDARY and self.order not in {1, 2}:
            raise ValidationError({"order": "Secondary focus must use order 1 or 2."})

    def save(self, *args: object, **kwargs: object) -> None:
        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]  # Django save expects specific typed kwargs
