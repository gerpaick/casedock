from __future__ import annotations

import pytest
from django.urls import reverse

from apps.cases.models import Case, CaseStatus, PrivateNote, SpecDocument
from apps.decisions.models import Decision
from apps.execution.models import ExecutionItem, ExecutionState

pytestmark = pytest.mark.django_db


def test_case_detail_renders_workspace_sections(client, user):
    case = Case.objects.create(
        user=user,
        title="Case workspace",
        summary="Keep the work calm.",
        next_step="Open the case page.",
        status=CaseStatus.ACTIVE,
    )
    SpecDocument.objects.create(user=user, case=case, markdown_body="# Context")
    Decision.objects.create(user=user, case=case, body="Stay HTML-first.")
    ExecutionItem.objects.create(user=user, case=case, title="Ship the workspace")
    PrivateNote.objects.create(user=user, case=case, body="This should stay private.")

    response = client.get(reverse("cases:detail", args=[case.public_id]))

    assert response.status_code == 200
    assert b"data-case-workspace" in response.content
    assert b"data-case-overview" in response.content
    assert b"Decisions" in response.content
    assert b"Execution" in response.content
    assert b"Private" in response.content
    assert b"Stay HTML-first." in response.content
    assert b"This should stay private." in response.content


def test_case_spec_update_saves_markdown(client, user):
    case = Case.objects.create(user=user, title="Spec update")
    SpecDocument.objects.create(user=user, case=case, markdown_body="# Old")

    response = client.post(
        reverse("cases:spec_update", args=[case.public_id]),
        {"markdown_body": "# Updated\n\nSharper scope."},
    )

    assert response.status_code == 302
    case.refresh_from_db()
    assert case.spec_document.markdown_body == "# Updated\n\nSharper scope."


def test_case_status_update_changes_case_state(client, user):
    case = Case.objects.create(user=user, title="Status update", status=CaseStatus.ACTIVE)

    response = client.post(
        reverse("cases:status_update", args=[case.public_id]),
        {"status": CaseStatus.WAITING},
    )

    assert response.status_code == 302
    case.refresh_from_db()
    assert case.status == CaseStatus.WAITING


def test_case_decision_create_supports_promoted_decision(client, user):
    case = Case.objects.create(user=user, title="Decision case")

    response = client.post(
        reverse("cases:decision_create", args=[case.public_id]),
        {
            "body": "We will keep the first version server-rendered.",
            "promoted": "on",
            "title": "Keep HTML-first in v1",
            "tag": "scope",
            "rationale": "The spec makes server-rendered the default.",
            "alternatives": "A more reactive frontend shell.",
            "consequence": "Lower complexity in v1.",
        },
    )

    assert response.status_code == 302
    decision = case.decisions.get()
    assert decision.promoted is True
    assert decision.title == "Keep HTML-first in v1"


def test_case_execution_create_and_state_update_work(client, user):
    case = Case.objects.create(user=user, title="Execution case")

    create_response = client.post(
        reverse("cases:execution_create", args=[case.public_id]),
        {
            "title": "Add the execution section",
            "section": "workspace",
            "note": "Keep it lightweight.",
            "state": ExecutionState.DOING,
        },
    )

    execution_item = case.execution_items.get()
    update_response = client.post(
        reverse("cases:execution_state_update", args=[case.public_id, execution_item.public_id]),
        {"state": ExecutionState.DONE},
    )

    assert create_response.status_code == 302
    assert update_response.status_code == 302
    execution_item.refresh_from_db()
    assert execution_item.state == ExecutionState.DONE
    assert execution_item.completed_at is not None


def test_case_private_note_create_saves_user_only_note(client, user):
    case = Case.objects.create(user=user, title="Private case")

    response = client.post(
        reverse("cases:private_note_create", args=[case.public_id]),
        {"body": "Keep this away from external systems."},
    )

    assert response.status_code == 302
    note = case.private_notes.get()
    assert note.body == "Keep this away from external systems."
