from __future__ import annotations

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.cases.models import Case, CaseStatus
from apps.focus.models import FocusAssignment, FocusRole

pytestmark = pytest.mark.django_db


def _make_stale_case(user, title: str = "Stale case", days_ago: int = 8) -> Case:
    case = Case.objects.create(user=user, title=title, status=CaseStatus.ACTIVE)
    old_time = timezone.now() - timedelta(days=days_ago)
    Case.objects.filter(pk=case.pk).update(updated_at=old_time)
    case.refresh_from_db()
    return case


def test_board_shows_focus_hero(client, db, user):
    case = Case.objects.create(user=user, title="Hero case", status=CaseStatus.ACTIVE)
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=case,
        role=FocusRole.MAIN,
        order=1,
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b"Daily focus" in response.content
    assert b"Hero case" in response.content
    assert b"data-board-focus-rail" in response.content


def test_board_shows_stale_alert_when_stale_cases_exist(client, db, user):
    _make_stale_case(user, title="Old and stale")

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b"Stale Cases" in response.content
    assert b"Old and stale" in response.content
    assert b"Untouched for" in response.content


def test_board_no_stale_alert_when_clean(client, db, user):
    Case.objects.create(user=user, title="Fresh case", status=CaseStatus.ACTIVE)

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b"Stale Cases" not in response.content


def test_board_excludes_stale_for_today_focus_cases(client, db, user):
    case = _make_stale_case(user, title="Focused stale")
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=case,
        role=FocusRole.MAIN,
        order=1,
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b"Stale Cases" not in response.content


def test_board_shows_stats(client, db, user):
    Case.objects.create(user=user, title="A1", status=CaseStatus.ACTIVE)
    Case.objects.create(user=user, title="A2", status=CaseStatus.ACTIVE)
    Case.objects.create(user=user, title="W1", status=CaseStatus.WAITING)
    done = Case.objects.create(user=user, title="D1", status=CaseStatus.DONE)
    Case.objects.filter(pk=done.pk).update(
        completed_at=timezone.now(),
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert response.context["active_count"] == 2
    assert response.context["waiting_count"] == 1
    assert response.context["done_count"] >= 1


def test_board_links_to_active_and_waiting(client, db):
    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert reverse("ui:active").encode() in response.content
    assert reverse("ui:waiting").encode() in response.content
    assert b"See all active" in response.content
    assert b"See waiting" in response.content


def test_stale_ack_via_htmx(client, db, user):
    case = _make_stale_case(user)

    response = client.post(
        reverse("cases:stale_action", args=[case.public_id]),
        {"action": "ack"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert b'id="board-page"' in response.content
    case.refresh_from_db()
    assert case.stale_ack_count == 1
    assert b"Acknowledged" in response.content


def test_stale_ack_blocked_at_limit(client, db, user):
    case = _make_stale_case(user)
    Case.objects.filter(pk=case.pk).update(stale_ack_count=3)
    case.refresh_from_db()

    response = client.post(
        reverse("cases:stale_action", args=[case.public_id]),
        {"action": "ack"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert b"Ack limit reached" in response.content
    case.refresh_from_db()
    assert case.stale_ack_count == 3


def test_stale_resolve_done_via_htmx(client, db, user):
    case = _make_stale_case(user)

    response = client.post(
        reverse("cases:stale_action", args=[case.public_id]),
        {"action": "done"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    case.refresh_from_db()
    assert case.status == CaseStatus.DONE
    assert b"Case moved to done" in response.content


def test_stale_resolve_waiting_via_htmx(client, db, user):
    case = _make_stale_case(user)

    response = client.post(
        reverse("cases:stale_action", args=[case.public_id]),
        {"action": "waiting"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    case.refresh_from_db()
    assert case.status == CaseStatus.WAITING
    assert b"Case moved to waiting" in response.content
