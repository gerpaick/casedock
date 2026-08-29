from __future__ import annotations

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from apps.cases.models import Case, CaseStatus
from apps.focus.models import FocusAssignment, FocusRole


def test_active_view_lists_active_cases(client, db, user):
    Case.objects.create(user=user, title="Active case", status=CaseStatus.ACTIVE)
    response = client.get(reverse("ui:active"))
    assert response.status_code == 200
    assert b"Active case" in response.content


def test_active_view_excludes_non_active(client, db, user):
    Case.objects.create(user=user, title="Waiting case", status=CaseStatus.WAITING)
    Case.objects.create(user=user, title="Done case", status=CaseStatus.DONE)
    response = client.get(reverse("ui:active"))
    assert response.status_code == 200
    assert b"Waiting case" not in response.content
    assert b"Done case" not in response.content


def test_active_view_shows_focus_badge(client, db, user):
    case = Case.objects.create(user=user, title="Focused case", status=CaseStatus.ACTIVE)
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=case,
        role=FocusRole.MAIN,
        order=1,
    )
    response = client.get(reverse("ui:active"))
    assert response.status_code == 200
    assert b"Main focus" in response.content


def test_active_view_empty_state(client, db):
    response = client.get(reverse("ui:active"))
    assert response.status_code == 200
    assert b"No active Cases" in response.content


def test_active_view_marks_stale_cases(client, db, user):
    case = Case.objects.create(user=user, title="Old case", status=CaseStatus.ACTIVE)
    old_time = timezone.now() - timedelta(days=30)
    Case.objects.filter(pk=case.pk).update(updated_at=old_time)
    response = client.get(reverse("ui:active"))
    assert response.status_code == 200
    assert b"Stale" in response.content


def test_active_view_sorts_stale_to_bottom(client, db, user):
    stale = Case.objects.create(user=user, title="Stale case", status=CaseStatus.ACTIVE)
    Case.objects.filter(pk=stale.pk).update(updated_at=timezone.now() - timedelta(days=30))
    Case.objects.create(user=user, title="Fresh case", status=CaseStatus.ACTIVE)
    response = client.get(reverse("ui:active"))
    content = response.content.decode()
    stale_pos = content.find("Stale case")
    fresh_pos = content.find("Fresh case")
    assert stale_pos > fresh_pos


def test_active_view_shows_needs_direction(client, db, user):
    Case.objects.create(
        user=user,
        title="Empty case",
        status=CaseStatus.ACTIVE,
        next_step="",
        summary="",
    )
    response = client.get(reverse("ui:active"))
    assert response.status_code == 200
    assert b"Needs direction" in response.content


def test_active_view_shows_next_step_when_present(client, db, user):
    Case.objects.create(
        user=user,
        title="Directed case",
        status=CaseStatus.ACTIVE,
        next_step="Write tests",
    )
    response = client.get(reverse("ui:active"))
    assert response.status_code == 200
    assert b"Write tests" in response.content


def test_waiting_view_lists_waiting_cases(client, db, user):
    Case.objects.create(user=user, title="Waiting case", status=CaseStatus.WAITING)
    response = client.get(reverse("ui:waiting"))
    assert response.status_code == 200
    assert b"Waiting case" in response.content


def test_waiting_view_excludes_non_waiting(client, db, user):
    Case.objects.create(user=user, title="Active case", status=CaseStatus.ACTIVE)
    Case.objects.create(user=user, title="Done case", status=CaseStatus.DONE)
    response = client.get(reverse("ui:waiting"))
    assert response.status_code == 200
    assert b"Active case" not in response.content
    assert b"Done case" not in response.content


def test_waiting_view_empty_state(client, db):
    response = client.get(reverse("ui:waiting"))
    assert response.status_code == 200
    assert b"Nothing is waiting" in response.content
