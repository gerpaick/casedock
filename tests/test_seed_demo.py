from __future__ import annotations

import pytest
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone

from apps.cases.models import Case, CaseStatus
from apps.core.models import User
from apps.focus.models import FocusAssignment, FocusRole
from apps.inbox.models import InboxItem, InboxItemState

pytestmark = pytest.mark.django_db


def test_seed_demo_creates_predictable_dataset_and_is_idempotent():
    call_command("seed_demo")

    assert User.objects.filter(email="demo@casedock.local").count() == 1
    assert Case.objects.count() == 9
    assert InboxItem.objects.count() == 9
    assert FocusAssignment.objects.count() == 3
    assert Case.objects.filter(status=CaseStatus.ACTIVE).count() == 4
    assert Case.objects.filter(status=CaseStatus.WAITING).count() == 2
    assert Case.objects.filter(status=CaseStatus.DONE).count() == 3

    call_command("seed_demo")

    assert User.objects.filter(email="demo@casedock.local").count() == 1
    assert Case.objects.count() == 9
    assert InboxItem.objects.count() == 9
    assert FocusAssignment.objects.count() == 3


def test_seed_demo_keeps_converted_inbox_items_consistent():
    call_command("seed_demo")

    converted_items = InboxItem.objects.filter(triage_state=InboxItemState.CONVERTED)

    assert converted_items.count() == 2
    assert converted_items.filter(converted_case__isnull=False).count() == 2
    assert (
        InboxItem.objects.exclude(triage_state=InboxItemState.CONVERTED)
        .filter(converted_case__isnull=False)
        .count()
        == 0
    )


def test_seed_demo_populates_board_inbox_focus_and_case_surfaces(client):
    call_command("seed_demo")

    demo_user = User.objects.get(email="demo@casedock.local")
    client.force_login(demo_user)

    home_response = client.get(reverse("ui:home"))
    inbox_response = client.get(reverse("inbox:list"))
    focus_response = client.get(reverse("focus:today"))

    rich_case = Case.objects.get(title="Demo: Stabilize email sign-in")
    case_response = client.get(reverse("cases:detail", args=[rich_case.public_id]))

    assert home_response.status_code == 200
    assert b"Demo: Stabilize email sign-in" in home_response.content
    assert b"See all active" in home_response.content
    assert b"See waiting" in home_response.content

    assert inbox_response.status_code == 200
    assert b"Demo: Reply to vendor about DNS transfer" in inbox_response.content
    assert b"Demo: Convert ClickUp mapping thought into a Case" in inbox_response.content
    assert b"Demo: Restart local worker after env update" in inbox_response.content

    assert focus_response.status_code == 200
    assert b"Demo: Stabilize email sign-in" in focus_response.content
    assert b"Demo: Shape onboarding empty state" in focus_response.content
    assert b"Demo: Write inbox-to-case walkthrough" in focus_response.content

    assert case_response.status_code == 200
    assert b"Avoid naming an auth flow we have not shipped" in case_response.content
    assert b"Capture the stale-tab reproduction steps" in case_response.content
    assert b"Do not over-engineer the auth fix." in case_response.content


def test_seed_demo_sets_focus_for_today():
    call_command("seed_demo")

    assignments = FocusAssignment.objects.filter(focus_date=timezone.localdate())

    assert assignments.count() == 3
    assert assignments.filter(role=FocusRole.MAIN, order=1).count() == 1
    assert assignments.filter(role=FocusRole.SECONDARY).count() == 2
