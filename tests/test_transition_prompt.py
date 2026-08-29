from __future__ import annotations

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.cases.models import Case, CaseStatus
from apps.focus.models import FocusAssignment, FocusRole

pytestmark = pytest.mark.django_db


def _make_focus_main(user, case: Case) -> None:
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=case,
        role=FocusRole.MAIN,
        order=1,
    )


def test_transition_prompt_shown_for_untouched_previous_main(client, db, user) -> None:
    old_case = Case.objects.create(user=user, title="Old main", status=CaseStatus.ACTIVE)
    _make_focus_main(user, old_case)
    new_case = Case.objects.create(user=user, title="New main", status=CaseStatus.ACTIVE)

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": new_case.public_id,
            "action": "set_main",
            "surface": "board",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    content = response.content.decode()
    assert "Old main" in content
    assert "hasn't been updated" in content


def test_transition_prompt_not_shown_if_no_previous_main(client, db, user) -> None:
    new_case = Case.objects.create(user=user, title="New main", status=CaseStatus.ACTIVE)

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": new_case.public_id,
            "action": "set_main",
            "surface": "board",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert "hasn't been updated" not in response.content.decode()


def test_transition_prompt_not_shown_if_same_case(client, db, user) -> None:
    case = Case.objects.create(user=user, title="Same case", status=CaseStatus.ACTIVE)
    _make_focus_main(user, case)

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": case.public_id,
            "action": "set_main",
            "surface": "board",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert "hasn't been updated" not in response.content.decode()


def test_transition_prompt_not_shown_if_previous_main_not_active(client, db, user) -> None:
    old_case = Case.objects.create(user=user, title="Old main", status=CaseStatus.WAITING)
    _make_focus_main(user, old_case)
    new_case = Case.objects.create(user=user, title="New main", status=CaseStatus.ACTIVE)

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": new_case.public_id,
            "action": "set_main",
            "surface": "board",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert "hasn't been updated" not in response.content.decode()


def test_transition_prompt_not_shown_if_previous_main_was_edited(client, db, user) -> None:
    old_case = Case.objects.create(user=user, title="Old main", status=CaseStatus.ACTIVE)
    _make_focus_main(user, old_case)
    old_case.next_step = "Updated after focus"
    old_case.save()

    new_case = Case.objects.create(user=user, title="New main", status=CaseStatus.ACTIVE)

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": new_case.public_id,
            "action": "set_main",
            "surface": "board",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert "hasn't been updated" not in response.content.decode()


def test_transition_prompt_dismiss_via_still_working(client, db, user) -> None:
    old_case = Case.objects.create(user=user, title="Old main", status=CaseStatus.ACTIVE)
    _make_focus_main(user, old_case)
    new_case = Case.objects.create(user=user, title="New main", status=CaseStatus.ACTIVE)

    client.post(
        reverse("focus:action"),
        {
            "case_id": new_case.public_id,
            "action": "set_main",
            "surface": "board",
        },
        HTTP_HX_REQUEST="true",
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert "hasn't been updated" not in response.content.decode()
