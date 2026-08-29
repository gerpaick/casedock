"""Cross-user isolation tests.

Verifies that user A cannot read, list, or mutate user B's data through any
HTTP endpoint. Every view must scope by ``request.user``; object lookups must
filter by both ``public_id`` and ``user`` so cross-user access returns 404
instead of leaking data.

These tests use dedicated ``user_a`` / ``user_b`` fixtures (not the single-user
``user`` fixture from conftest) so two distinct accounts coexist in one test.
"""

from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from apps.cases.models import Case, CaseStatus
from apps.core.models import User
from apps.focus.models import FocusAssignment, FocusRole
from apps.inbox.models import InboxItem, InboxItemState

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_a(db) -> User:
    return User.objects.create_user(
        email="alpha@casedock.local",
        password="pw-alpha-123",
    )


@pytest.fixture
def user_b(db) -> User:
    return User.objects.create_user(
        email="beta@casedock.local",
        password="pw-beta-123",
    )


@pytest.fixture
def client_a(client: Client, user_a: User) -> Client:
    client.force_login(user_a)
    return client


def _make_case(user: User, title: str, *, status: str = CaseStatus.ACTIVE) -> Case:
    return Case.objects.create(user=user, title=title, status=status)


def _make_inbox_item(user: User, title: str, *, state: str = InboxItemState.NEW) -> InboxItem:
    return InboxItem.objects.create(user=user, title=title, triage_state=state)


class TestPositiveControl:
    def test_user_can_access_own_case_detail(self, client_a: Client, user_a: User):
        own_case = _make_case(user_a, "Alpha own case")
        response = client_a.get(reverse("cases:detail", args=[own_case.public_id]))
        assert response.status_code == 200
        assert b"Alpha own case" in response.content


class TestCaseIsolation:
    def test_case_detail_404_for_other_users_case(self, client_a: Client, user_b: User):
        other_case = _make_case(user_b, "Beta secret case")
        response = client_a.get(reverse("cases:detail", args=[other_case.public_id]))
        assert response.status_code == 404
        assert b"Beta secret case" not in response.content

    def test_case_status_update_404_for_other_users_case(self, client_a: Client, user_b: User):
        other_case = _make_case(user_b, "Beta status case")
        response = client_a.post(
            reverse("cases:status_update", args=[other_case.public_id]),
            {"status": CaseStatus.WAITING},
        )
        assert response.status_code == 404
        other_case.refresh_from_db()
        assert other_case.status == CaseStatus.ACTIVE

    def test_case_spec_update_404_for_other_users_case(self, client_a: Client, user_b: User):
        other_case = _make_case(user_b, "Beta spec case")
        response = client_a.post(
            reverse("cases:spec_update", args=[other_case.public_id]),
            {"markdown_body": "leaked spec body"},
        )
        assert response.status_code == 404

    def test_case_decision_create_404_for_other_users_case(self, client_a: Client, user_b: User):
        other_case = _make_case(user_b, "Beta decision case")
        response = client_a.post(
            reverse("cases:decision_create", args=[other_case.public_id]),
            {"body": "leaked decision"},
        )
        assert response.status_code == 404
        assert other_case.decisions.count() == 0

    def test_case_execution_create_404_for_other_users_case(self, client_a: Client, user_b: User):
        other_case = _make_case(user_b, "Beta execution case")
        response = client_a.post(
            reverse("cases:execution_create", args=[other_case.public_id]),
            {"title": "leaked step", "state": "todo"},
        )
        assert response.status_code == 404
        assert other_case.execution_items.count() == 0

    def test_case_private_note_create_404_for_other_users_case(
        self, client_a: Client, user_b: User
    ):
        other_case = _make_case(user_b, "Beta note case")
        response = client_a.post(
            reverse("cases:private_note_create", args=[other_case.public_id]),
            {"body": "leaked private note"},
        )
        assert response.status_code == 404
        assert other_case.private_notes.count() == 0


class TestInboxIsolation:
    def test_inbox_detail_404_for_other_users_item(self, client_a: Client, user_b: User):
        other_item = _make_inbox_item(user_b, "Beta inbox secret")
        response = client_a.get(reverse("inbox:detail", args=[other_item.public_id]))
        assert response.status_code == 404
        assert b"Beta inbox secret" not in response.content

    def test_inbox_triage_404_for_other_users_item(self, client_a: Client, user_b: User):
        other_item = _make_inbox_item(user_b, "Beta triage item")
        response = client_a.post(
            reverse("inbox:triage", args=[other_item.public_id]),
            {"action": "park"},
        )
        assert response.status_code == 404
        other_item.refresh_from_db()
        assert other_item.triage_state == InboxItemState.NEW

    def test_inbox_convert_404_for_other_users_item(self, client_a: Client, user_b: User):
        other_item = _make_inbox_item(user_b, "Beta convert item")
        url = reverse("inbox:convert", args=[other_item.public_id])
        get_response = client_a.get(url)
        assert get_response.status_code == 404
        post_response = client_a.post(
            url,
            {
                "working_title": "leaked conversion",
                "clarity": "fuzzy",
                "work_type": "build",
                "effort": "medium",
            },
        )
        assert post_response.status_code == 404
        other_item.refresh_from_db()
        assert other_item.triage_state == InboxItemState.NEW
        assert other_item.converted_case_id is None


class TestSearchIsolation:
    def test_search_excludes_other_users_cases(self, client_a: Client, user_a: User, user_b: User):
        _make_case(user_a, "Alpha common token ZX")
        _make_case(user_b, "Beta common token ZX")
        response = client_a.get(reverse("ui:search"), {"q": "common token ZX"})
        assert response.status_code == 200
        assert b"Alpha common token ZX" in response.content
        assert b"Beta common token ZX" not in response.content


class TestBoardIsolation:
    def test_board_excludes_other_users_cases_and_counts(
        self, client_a: Client, user_a: User, user_b: User
    ):
        _make_case(user_a, "Alpha board case")
        _make_case(user_b, "Beta board case one", status=CaseStatus.ACTIVE)
        _make_case(user_b, "Beta board case two", status=CaseStatus.ACTIVE)

        response = client_a.get(reverse("ui:home"))
        assert response.status_code == 200
        assert b"1 active" in response.content
        assert b"3 active" not in response.content
        assert b"Beta board case one" not in response.content
        assert b"Beta board case two" not in response.content


class TestInboxListIsolation:
    def test_inbox_list_excludes_other_users_items(
        self, client_a: Client, user_a: User, user_b: User
    ):
        _make_inbox_item(user_a, "Alpha queue visible")
        _make_inbox_item(user_b, "Beta queue hidden")

        response = client_a.get(reverse("inbox:list"))
        assert response.status_code == 200
        assert b"Alpha queue visible" in response.content
        assert b"Beta queue hidden" not in response.content


class TestFocusIsolation:
    def test_focus_view_excludes_other_users_assignments(
        self, client_a: Client, user_a: User, user_b: User
    ):
        alpha_case = _make_case(user_a, "Alpha focus case")
        beta_case = _make_case(user_b, "Beta focus case")
        today = timezone.localdate()
        FocusAssignment.objects.create(
            user=user_a,
            focus_date=today,
            case=alpha_case,
            role=FocusRole.MAIN,
            order=1,
        )
        FocusAssignment.objects.create(
            user=user_b,
            focus_date=today,
            case=beta_case,
            role=FocusRole.MAIN,
            order=1,
        )

        response = client_a.get(reverse("focus:today"))
        assert response.status_code == 200
        assert b"Alpha focus case" in response.content
        assert b"Beta focus case" not in response.content

    def test_focus_quick_action_404_for_other_users_case(self, client_a: Client, user_b: User):
        beta_case = _make_case(user_b, "Beta focus target")
        response = client_a.post(
            reverse("focus:action"),
            {"case_id": str(beta_case.public_id), "action": "set_main"},
        )
        assert response.status_code == 404
