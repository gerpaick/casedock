from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.core.models import PublicIDModel, TimeStampedModel


class CaseStatus(models.TextChoices):
    INBOX = "inbox", "Inbox"
    ACTIVE = "active", "Active"
    WAITING = "waiting", "Waiting"
    DONE = "done", "Done"


class CaseClarity(models.TextChoices):
    CLEAR = "clear", "Clear"
    FUZZY = "fuzzy", "Fuzzy"


class CaseWorkType(models.TextChoices):
    BUILD = "build", "Build"
    DEBUG = "debug", "Debug"
    RESEARCH = "research", "Research"
    ADMIN = "admin", "Admin"
    REPLY = "reply", "Reply"


class CaseEffort(models.TextChoices):
    QUICK = "quick", "Quick"
    MEDIUM = "medium", "Medium"
    DEEP = "deep", "Deep"


class CaseEnergy(models.TextChoices):
    SHALLOW = "shallow", "Shallow"
    DEEP = "deep", "Deep"


CASE_ALLOWED_TRANSITIONS = {
    CaseStatus.INBOX: {CaseStatus.ACTIVE, CaseStatus.WAITING, CaseStatus.DONE},
    CaseStatus.ACTIVE: {CaseStatus.WAITING, CaseStatus.DONE},
    CaseStatus.WAITING: {CaseStatus.ACTIVE, CaseStatus.DONE},
    CaseStatus.DONE: {CaseStatus.ACTIVE, CaseStatus.WAITING},
}


class Case(TimeStampedModel, PublicIDModel):
    # Dynamic attributes set by view code for template rendering
    focus_role: str
    board_action: str
    board_action_label: str
    days_stale: int
    is_stale: bool
    can_ack: bool

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cases",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    summary = models.TextField(blank=True)
    status = models.CharField(
        max_length=16,
        choices=CaseStatus.choices,
        default=CaseStatus.INBOX,
    )
    clarity = models.CharField(
        max_length=16,
        choices=CaseClarity.choices,
        default=CaseClarity.FUZZY,
    )
    work_type = models.CharField(
        max_length=16,
        choices=CaseWorkType.choices,
        default=CaseWorkType.BUILD,
    )
    effort = models.CharField(
        max_length=16,
        choices=CaseEffort.choices,
        default=CaseEffort.MEDIUM,
    )
    energy = models.CharField(
        max_length=16,
        choices=CaseEnergy.choices,
        default=CaseEnergy.SHALLOW,
    )
    next_step = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    stale_ack_count = models.PositiveSmallIntegerField(default=0)
    stale_acked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-updated_at", "-created_at")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "slug"),
                name="uniq_case_slug_per_user",
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        super().clean()
        if (
            self.status == CaseStatus.DONE
            and self.archived_at
            and self.completed_at
            and self.archived_at < self.completed_at
        ):
            raise ValidationError(
                {"archived_at": "Archived time cannot be earlier than completed time."}
            )

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = self._build_unique_slug()

        if self.status == CaseStatus.DONE and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != CaseStatus.DONE:
            self.completed_at = None

        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]  # Django save expects specific typed kwargs

    def transition_to(self, new_status: str, *, save: bool = True) -> None:
        current_status = CaseStatus(self.status)
        if new_status == current_status:
            return

        allowed_statuses = CASE_ALLOWED_TRANSITIONS[current_status]
        if new_status not in allowed_statuses:
            raise ValidationError(
                {"status": f"Cannot transition case from {current_status} to {new_status}."}
            )

        self.status = new_status
        self.stale_ack_count = 0
        if save:
            self.save(update_fields=["status", "completed_at", "updated_at", "stale_ack_count"])

    def _build_unique_slug(self) -> str:
        base_slug = slugify(self.title)[:240] or "case"
        slug = base_slug
        suffix = 2
        while (
            type(self).objects.filter(user_id=self.user_id, slug=slug).exclude(pk=self.pk).exists()
        ):
            slug = f"{base_slug[: 240 - len(str(suffix)) - 1]}-{suffix}"
            suffix += 1
        return slug

    @property
    def display_hint(self) -> str:
        return self.next_step or self.summary or "No next step yet."


class SpecDocument(TimeStampedModel, PublicIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="spec_documents",
    )
    case = models.OneToOneField(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="spec_document",
    )
    markdown_body = models.TextField(blank=True)
    rendered_cache = models.TextField(blank=True)

    class Meta:
        ordering = ("case_id",)

    def __str__(self) -> str:
        return f"Spec for {self.case}"


class PrivateNote(TimeStampedModel, PublicIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="private_notes",
    )
    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="private_notes",
    )
    body = models.TextField()

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"Private note for {self.case}"
