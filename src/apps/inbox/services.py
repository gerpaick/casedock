from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction

from apps.cases.models import (
    Case,
    CaseEnergy,
    CaseStatus,
    SpecDocument,
)
from apps.sources.models import SourceLink, SourceProvider

from .models import InboxItem, InboxItemState, InboxSourceType

if TYPE_CHECKING:
    from apps.core.models import User


def build_spec_markdown(
    *,
    inbox_item: InboxItem,
    outcome: str,
    next_step: str,
) -> str:
    context = inbox_item.raw_body.strip() if inbox_item.raw_body else ""
    lines = [
        "# Context",
        context or "Captured from Inbox.",
        "",
        "# Outcome",
        outcome.strip() or "Define the desired outcome.",
        "",
        "# Next Step",
        next_step.strip() or "Choose the first concrete move.",
        "",
        "# Notes",
        "- Source item kept close to the work",
    ]
    return "\n".join(lines)


def map_source_provider(inbox_item: InboxItem) -> str:
    if inbox_item.source_type == InboxSourceType.CLICKUP:
        return SourceProvider.CLICKUP
    if inbox_item.source_type == InboxSourceType.URL:
        return SourceProvider.URL
    if inbox_item.source_type == InboxSourceType.MANUAL:
        return SourceProvider.MANUAL
    return SourceProvider.OTHER


@transaction.atomic
def convert_inbox_item_to_case(
    *,
    user: User,
    inbox_item: InboxItem,
    working_title: str,
    outcome: str,
    clarity: str,
    next_step: str,
    work_type: str,
    effort: str,
    keep_source_link: bool,
) -> Case:
    case = Case.objects.create(
        user=user,
        title=working_title,
        summary=outcome.strip(),
        status=CaseStatus.ACTIVE,
        clarity=clarity,
        work_type=work_type,
        effort=effort,
        energy=CaseEnergy.DEEP if effort == "deep" else CaseEnergy.SHALLOW,
        next_step=next_step.strip(),
    )
    SpecDocument.objects.create(
        user=user,
        case=case,
        markdown_body=build_spec_markdown(
            inbox_item=inbox_item,
            outcome=outcome,
            next_step=next_step,
        ),
    )

    if keep_source_link:
        moved_links = list(inbox_item.source_links.all())
        for source_link in moved_links:
            source_link.case = case
            source_link.inbox_item = None
            source_link.save()

        if inbox_item.source_url and not moved_links:
            SourceLink.objects.create(
                user=user,
                provider=map_source_provider(inbox_item),
                external_url=inbox_item.source_url,
                external_title_snapshot=inbox_item.title,
                inbox_item=None,
                case=case,
            )

    inbox_item.converted_case = case
    inbox_item.triage_state = InboxItemState.CONVERTED
    inbox_item.save()
    return case
