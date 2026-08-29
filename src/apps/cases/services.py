from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from django.conf import settings
from django.db.models import F, QuerySet
from django.utils import timezone

from apps.cases.models import Case, CaseStatus

if TYPE_CHECKING:
    from apps.core.models import User


def get_stale_cases(
    *,
    user: User | None = None,
    exclude_focus_case_ids: set[int] | None = None,
) -> QuerySet[Case]:
    threshold = timezone.now() - timedelta(days=settings.CASEDOCK_STALE_PERIOD_DAYS)
    qs = Case.objects.filter(
        status=CaseStatus.ACTIVE,
        updated_at__lt=threshold,
    ).exclude(
        stale_acked_at__gte=timezone.now() - timedelta(hours=24),
    )
    if user is not None:
        qs = qs.filter(user=user)
    if exclude_focus_case_ids:
        qs = qs.exclude(pk__in=exclude_focus_case_ids)
    return qs


def ack_stale_case(case: Case) -> None:
    Case.objects.filter(pk=case.pk).update(
        stale_ack_count=F("stale_ack_count") + 1,
        stale_acked_at=timezone.now(),
    )


def resolve_stale_case(case: Case, action: str) -> None:
    status_map: dict[str, str] = {"done": CaseStatus.DONE, "waiting": CaseStatus.WAITING}
    new_status = status_map.get(action)
    if new_status:
        case.transition_to(new_status)
