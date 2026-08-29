from __future__ import annotations

from datetime import date

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.cases.models import Case, CaseStatus, SpecDocument
from apps.decisions.models import Decision
from apps.execution.models import ExecutionItem, ExecutionState
from apps.focus.models import FocusAssignment, FocusRole
from apps.inbox.models import InboxItem, InboxItemState
from apps.sources.models import SourceLink, SourceProvider

pytestmark = pytest.mark.django_db


def test_case_generates_unique_slug_and_sets_completed_at_when_done(user):
    first_case = Case.objects.create(user=user, title="Implement auth")
    second_case = Case.objects.create(user=user, title="Implement auth", status=CaseStatus.DONE)

    assert first_case.slug == "implement-auth"
    assert second_case.slug == "implement-auth-2"
    assert second_case.completed_at is not None


def test_case_rejects_invalid_status_transition(user):
    case = Case.objects.create(user=user, title="Core work", status=CaseStatus.ACTIVE)

    with pytest.raises(ValidationError):
        case.transition_to(CaseStatus.INBOX)


def test_case_allows_active_waiting_done_transition_path(user):
    case = Case.objects.create(user=user, title="Core work", status=CaseStatus.INBOX)

    case.transition_to(CaseStatus.ACTIVE)
    case.transition_to(CaseStatus.WAITING)
    case.transition_to(CaseStatus.DONE)

    case.refresh_from_db()
    assert case.status == CaseStatus.DONE
    assert case.completed_at is not None


def test_case_has_one_spec_document(user):
    case = Case.objects.create(user=user, title="Structured work")
    SpecDocument.objects.create(user=user, case=case, markdown_body="# Context")

    with pytest.raises(IntegrityError):
        SpecDocument.objects.create(user=user, case=case, markdown_body="# Duplicate")


def test_inbox_item_requires_case_when_marked_converted(user):
    item = InboxItem(user=user, title="Triage me", triage_state=InboxItemState.CONVERTED)

    with pytest.raises(ValidationError):
        item.full_clean()


def test_inbox_item_rejects_converted_case_reference_for_non_converted_state(user):
    case = Case.objects.create(user=user, title="Converted case")
    item = InboxItem(
        user=user,
        title="Triage me",
        triage_state=InboxItemState.NEW,
        converted_case=case,
    )

    with pytest.raises(ValidationError):
        item.full_clean()


def test_inbox_item_allows_transition_from_doing_now_to_parked(user):
    item = InboxItem.objects.create(
        user=user,
        title="Pause this",
        triage_state=InboxItemState.DOING_NOW,
    )

    item.transition_to(InboxItemState.PARKED)

    item.refresh_from_db()
    assert item.triage_state == InboxItemState.PARKED


def test_decision_requires_title_when_promoted(user):
    case = Case.objects.create(user=user, title="Decision case")
    decision = Decision(user=user, case=case, body="Use Django", promoted=True)

    with pytest.raises(ValidationError):
        decision.full_clean()


def test_execution_item_sets_completion_timestamp_when_done(user):
    case = Case.objects.create(user=user, title="Execution case")
    item = ExecutionItem.objects.create(
        user=user,
        case=case,
        title="Ship it",
        state=ExecutionState.DONE,
    )

    assert item.completed_at is not None


def test_focus_assignment_validates_slots(user):
    case = Case.objects.create(user=user, title="Focus case")
    assignment = FocusAssignment(
        user=user,
        focus_date=date(2026, 4, 4),
        case=case,
        role=FocusRole.SECONDARY,
        order=3,
    )

    with pytest.raises(ValidationError):
        assignment.full_clean()


def test_focus_assignment_enforces_unique_slot_per_day(user):
    first_case = Case.objects.create(user=user, title="Main case")
    second_case = Case.objects.create(user=user, title="Other case")
    FocusAssignment.objects.create(
        user=user,
        focus_date=date(2026, 4, 4),
        case=first_case,
        role=FocusRole.MAIN,
        order=1,
    )

    with pytest.raises(ValidationError):
        FocusAssignment.objects.create(
            user=user,
            focus_date=date(2026, 4, 4),
            case=second_case,
            role=FocusRole.MAIN,
            order=1,
        )


def test_source_link_must_target_exactly_one_object(user):
    case = Case.objects.create(user=user, title="Case target")
    item = InboxItem.objects.create(user=user, title="Inbox target")

    with pytest.raises(ValidationError):
        SourceLink(
            user=user,
            provider=SourceProvider.CLICKUP,
            case=case,
            inbox_item=item,
        ).full_clean()

    with pytest.raises(ValidationError):
        SourceLink(user=user, provider=SourceProvider.CLICKUP).full_clean()


def test_source_link_can_belong_to_case_or_inbox_item(user):
    case = Case.objects.create(user=user, title="Case target")
    item = InboxItem.objects.create(user=user, title="Inbox target")

    case_link = SourceLink.objects.create(user=user, provider=SourceProvider.CLICKUP, case=case)
    inbox_link = SourceLink.objects.create(user=user, provider=SourceProvider.URL, inbox_item=item)

    assert case_link.case == case
    assert case_link.inbox_item is None
    assert inbox_link.inbox_item == item
    assert inbox_link.case is None
