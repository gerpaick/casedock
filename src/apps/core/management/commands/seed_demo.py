from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.cases.models import (
    Case,
    CaseStatus,
    PrivateNote,
    SpecDocument,
)
from apps.core.models import User
from apps.decisions.models import Decision
from apps.execution.models import ExecutionItem, ExecutionState
from apps.focus.models import FocusAssignment, FocusRole
from apps.inbox.models import InboxItem, InboxItemState, InboxSourceType
from apps.sources.models import SourceLink, SourceProvider

from .demo_fixtures import (
    DEMO_CASES,
    DEMO_EMAIL,
    DEMO_FOCUS_KEYS,
    DEMO_INBOX_ITEMS,
    DEMO_PASSWORD,
    DEMO_SLUG_PREFIX,
    DEMO_TITLE_PREFIX,
)


class Command(BaseCommand):
    help = "Create a predictable demo dataset for local UI preview."

    @transaction.atomic
    def handle(self, *args: object, **options: object) -> None:
        deleted_counts = flush_demo_records()
        user = ensure_demo_user()
        cases = create_demo_cases(user=user)
        inbox_items = create_demo_inbox_items(user=user, cases=cases)
        create_demo_focus(user=user, cases=cases)

        self.stdout.write(
            self.style.SUCCESS(
                "Demo dataset ready: "
                f"{len(cases)} cases, {len(inbox_items)} inbox items, "
                f"{FocusAssignment.objects.filter(focus_date=timezone.localdate()).count()} "
                "focus slots for today."
            )
        )
        self.stdout.write(
            "Recreated demo records after removing "
            f"{deleted_counts['cases']} cases, {deleted_counts['inbox_items']} inbox items, "
            f"and {deleted_counts['focus_assignments']} focus assignments."
        )
        self.stdout.write(f"Demo login: {user.email} / {DEMO_PASSWORD}")


def flush_demo_records() -> dict[str, int]:
    focus_assignments = FocusAssignment.objects.filter(focus_date=timezone.localdate())
    inbox_items = InboxItem.objects.filter(title__startswith=DEMO_TITLE_PREFIX)
    cases = Case.objects.filter(slug__startswith=DEMO_SLUG_PREFIX)

    deleted_counts = {
        "focus_assignments": focus_assignments.count(),
        "inbox_items": inbox_items.count(),
        "cases": cases.count(),
    }

    focus_assignments.delete()
    inbox_items.delete()
    cases.delete()
    return deleted_counts


def ensure_demo_user() -> User:
    user, _created = User.objects.update_or_create(
        email=DEMO_EMAIL,
        defaults={
            "first_name": "Demo",
            "last_name": "User",
            "is_active": True,
            "is_staff": True,
        },
    )
    user.set_password(DEMO_PASSWORD)
    user.save(update_fields=["password"])
    return user


def create_demo_cases(*, user: User) -> dict[str, Case]:
    cases: dict[str, Case] = {}
    now = timezone.now()

    for index, case_data in enumerate(DEMO_CASES):
        case = Case.objects.create(
            user=user,
            title=case_data["title"],
            summary=case_data["summary"],
            status=case_data["status"],
            clarity=case_data["clarity"],
            work_type=case_data["work_type"],
            effort=case_data["effort"],
            energy=case_data["energy"],
            next_step=case_data["next_step"],
        )
        timestamp = now - timedelta(days=len(DEMO_CASES) - index)
        Case.objects.filter(pk=case.pk).update(created_at=timestamp, updated_at=timestamp)
        if case.status == CaseStatus.DONE:
            completed_at = timestamp + timedelta(hours=6)
            Case.objects.filter(pk=case.pk).update(completed_at=completed_at)
            case.completed_at = completed_at
        case.refresh_from_db()

        SpecDocument.objects.create(
            user=user,
            case=case,
            markdown_body=case_data["spec_markdown"],
        )
        create_case_children(user=user, case=case, case_data=case_data, timestamp=timestamp)
        cases[case_data["key"]] = case

    return cases


def create_case_children(
    *,
    user: User,
    case: Case,
    case_data: dict[str, Any],
    timestamp: datetime,
) -> None:
    for source_index, source_data in enumerate(case_data["source_links"], start=1):
        link = SourceLink.objects.create(user=user, case=case, **source_data)
        link_time = timestamp + timedelta(minutes=source_index)
        SourceLink.objects.filter(pk=link.pk).update(
            created_at=link_time,
            updated_at=link_time,
            synced_at=link_time,
        )

    for decision_index, decision_data in enumerate(case_data["decisions"], start=1):
        decision = Decision.objects.create(user=user, case=case, **decision_data)
        decision_time = timestamp + timedelta(minutes=decision_index)
        Decision.objects.filter(pk=decision.pk).update(
            created_at=decision_time,
            updated_at=decision_time,
        )

    for note_index, note_data in enumerate(case_data["private_notes"], start=1):
        note = PrivateNote.objects.create(user=user, case=case, **note_data)
        note_time = timestamp + timedelta(minutes=note_index)
        PrivateNote.objects.filter(pk=note.pk).update(
            created_at=note_time,
            updated_at=note_time,
        )

    for item_index, execution_data in enumerate(case_data["execution_items"], start=1):
        item = ExecutionItem.objects.create(user=user, case=case, **execution_data)
        item_time = timestamp + timedelta(minutes=item_index)
        update_fields = {
            "created_at": item_time,
            "updated_at": item_time,
        }
        if item.state == ExecutionState.DONE:
            update_fields["completed_at"] = item_time
        ExecutionItem.objects.filter(pk=item.pk).update(**update_fields)


def create_demo_inbox_items(*, user: User, cases: dict[str, Case]) -> list[InboxItem]:
    inbox_items: list[InboxItem] = []
    now = timezone.now()

    for index, item_data in enumerate(DEMO_INBOX_ITEMS):
        converted_case_key = item_data.get("converted_case_key")
        inbox_item = InboxItem.objects.create(
            user=user,
            title=item_data["title"],
            source_type=item_data["source_type"],
            raw_body=item_data["raw_body"],
            completion_note=item_data["completion_note"],
            source_url=item_data["source_url"],
            triage_state=item_data["triage_state"],
            converted_case=cases[converted_case_key] if converted_case_key else None,
        )
        timestamp = now - timedelta(hours=len(DEMO_INBOX_ITEMS) - index)
        update_fields = {"created_at": timestamp, "updated_at": timestamp}
        if inbox_item.triage_state == InboxItemState.DONE:
            update_fields["updated_at"] = timestamp + timedelta(minutes=5)
        InboxItem.objects.filter(pk=inbox_item.pk).update(**update_fields)
        inbox_item.refresh_from_db()
        inbox_items.append(inbox_item)

    imported_item = next(
        item for item in inbox_items if item.source_type == InboxSourceType.CLICKUP
    )
    SourceLink.objects.create(
        user=user,
        provider=SourceProvider.CLICKUP,
        external_id="CU-DEMO-204",
        external_url="https://app.clickup.com/t/CU-DEMO-204",
        external_title_snapshot="Field mapping sample",
        external_status_snapshot="Open",
        payload_snapshot={"list": "Integrations"},
        inbox_item=imported_item,
    )

    return inbox_items


def create_demo_focus(*, user: User, cases: dict[str, Case]) -> None:
    focus_date = timezone.localdate()
    FocusAssignment.objects.create(
        user=user,
        focus_date=focus_date,
        case=cases[DEMO_FOCUS_KEYS[FocusRole.MAIN]],
        role=FocusRole.MAIN,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=focus_date,
        case=cases[DEMO_FOCUS_KEYS["secondary_1"]],
        role=FocusRole.SECONDARY,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=focus_date,
        case=cases[DEMO_FOCUS_KEYS["secondary_2"]],
        role=FocusRole.SECONDARY,
        order=2,
    )
