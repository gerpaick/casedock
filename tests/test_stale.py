from __future__ import annotations

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.cases.models import Case, CaseStatus
from apps.cases.services import ack_stale_case, get_stale_cases, resolve_stale_case
from apps.focus.models import FocusAssignment, FocusRole

pytestmark = pytest.mark.django_db


def _make_stale_case(user, title: str = "Stale case", days_ago: int = 8) -> Case:
    case = Case.objects.create(user=user, title=title, status=CaseStatus.ACTIVE)
    old_time = timezone.now() - timedelta(days=days_ago)
    Case.objects.filter(pk=case.pk).update(updated_at=old_time)
    case.refresh_from_db()
    return case


def test_stale_detection(user):
    case = _make_stale_case(user)

    stale = get_stale_cases()

    assert case.pk in stale.values_list("pk", flat=True)


def test_stale_not_shown_if_acked_recently(user):
    case = _make_stale_case(user)
    ack_stale_case(case)

    stale = get_stale_cases()

    assert case.pk not in stale.values_list("pk", flat=True)


def test_stale_not_shown_for_today_focus_case(user):
    case = _make_stale_case(user)
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.now().date(),
        case=case,
        role=FocusRole.MAIN,
        order=1,
    )

    stale = get_stale_cases(exclude_focus_case_ids={case.pk})

    assert case.pk not in stale.values_list("pk", flat=True)


def test_ack_increments_counter(user):
    case = _make_stale_case(user)

    ack_stale_case(case)
    ack_stale_case(case)
    case.refresh_from_db()

    assert case.stale_ack_count == 2


def test_ack_does_not_bump_updated_at(user):
    case = _make_stale_case(user)
    original_updated_at = case.updated_at

    ack_stale_case(case)
    case.refresh_from_db()

    assert case.updated_at == original_updated_at


def test_resolve_stale_done(user):
    case = _make_stale_case(user)
    Case.objects.filter(pk=case.pk).update(stale_ack_count=3)

    resolve_stale_case(case, "done")
    case.refresh_from_db()

    assert case.status == CaseStatus.DONE
    assert case.stale_ack_count == 0


def test_resolve_stale_waiting(user):
    case = _make_stale_case(user)
    Case.objects.filter(pk=case.pk).update(stale_ack_count=2)

    resolve_stale_case(case, "waiting")
    case.refresh_from_db()

    assert case.status == CaseStatus.WAITING
    assert case.stale_ack_count == 0


def test_transition_resets_ack_count(user):
    case = _make_stale_case(user)
    Case.objects.filter(pk=case.pk).update(stale_ack_count=3)
    case.refresh_from_db()

    case.transition_to(CaseStatus.WAITING)
    case.refresh_from_db()

    assert case.stale_ack_count == 0


def test_stale_only_shows_active_cases(user):
    case = Case.objects.create(user=user, title="Done case", status=CaseStatus.DONE)
    old_time = timezone.now() - timedelta(days=30)
    Case.objects.filter(pk=case.pk).update(updated_at=old_time)

    stale = get_stale_cases()

    assert case.pk not in stale.values_list("pk", flat=True)
