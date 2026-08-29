from __future__ import annotations

from typing import Any
from uuid import UUID

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from apps.core.models import User

from .forms import InboxCaptureForm
from .models import READY_INBOX_STATES, InboxItem, InboxItemState

READY_STATE_PRIORITY: dict[str, int] = {
    InboxItemState.DOING_NOW: 0,
    InboxItemState.NEW: 1,
    InboxItemState.WAITING: 2,
    InboxItemState.PARKED: 3,
}
SECONDARY_SECTION_LIMIT = 6


def rank_ready_items(inbox_items: list[InboxItem]) -> list[InboxItem]:
    return sorted(
        inbox_items,
        key=lambda inbox_item: (
            READY_STATE_PRIORITY[inbox_item.triage_state],
            inbox_item.created_at.timestamp(),
            inbox_item.updated_at.timestamp(),
        ),
    )


def coerce_selected_public_id(raw_value: object) -> UUID | None:
    if isinstance(raw_value, UUID):
        return raw_value
    if isinstance(raw_value, str):
        try:
            return UUID(raw_value)
        except ValueError:
            return None
    return None


def build_inbox_context(
    request: HttpRequest,
    *,
    capture_form: InboxCaptureForm | None = None,
    selected_public_id: UUID | None = None,
    inline_messages: bool = False,
    capture_landed_in: str | None = None,
) -> dict[str, Any]:
    user = request.user
    assert isinstance(user, User)
    inbox_items = InboxItem.objects.filter(user=user).order_by("-updated_at", "-created_at")
    ready_items = rank_ready_items(list(inbox_items.filter(triage_state__in=READY_INBOX_STATES)))
    selected_item = None
    selected_public_id = coerce_selected_public_id(selected_public_id)
    if selected_public_id is None:
        selected_public_id = coerce_selected_public_id(request.GET.get("selected"))
    if selected_public_id is not None:
        selected_item = next(
            (
                inbox_item
                for inbox_item in ready_items
                if inbox_item.public_id == selected_public_id
            ),
            None,
        )
    if selected_item is None and ready_items:
        selected_item = ready_items[0]

    queue_items = [
        inbox_item
        for inbox_item in ready_items
        if selected_item is None or inbox_item.pk != selected_item.pk
    ]

    recent_outcomes = list(
        inbox_items.filter(triage_state__in=(InboxItemState.CONVERTED, InboxItemState.DONE))[
            : SECONDARY_SECTION_LIMIT + 1
        ]
    )
    converted_count = inbox_items.filter(triage_state=InboxItemState.CONVERTED).count()
    done_count = inbox_items.filter(triage_state=InboxItemState.DONE).count()
    return {
        "capture_form": capture_form or InboxCaptureForm(),
        "capture_landed_in": capture_landed_in,
        "capture_modal_open": bool(capture_form and capture_form.errors),
        "inline_messages": inline_messages,
        "selected_item": selected_item,
        "queue_items": queue_items,
        "ready_count": len(ready_items),
        "recent_outcomes": recent_outcomes[:SECONDARY_SECTION_LIMIT],
        "recent_outcomes_count": converted_count + done_count,
        "recent_outcomes_has_more": len(recent_outcomes) > SECONDARY_SECTION_LIMIT,
        "converted_count": converted_count,
        "done_count": done_count,
    }


def build_inbox_url(*, selected_public_id: UUID | None = None) -> str:
    inbox_url = reverse("inbox:list")
    selected_public_id = coerce_selected_public_id(selected_public_id)
    if selected_public_id is not None:
        return f"{inbox_url}?selected={selected_public_id}"
    return inbox_url


def render_inbox_response(
    request: HttpRequest,
    *,
    capture_form: InboxCaptureForm | None = None,
    selected_public_id: UUID | None = None,
    capture_landed_in: str | None = None,
    status: int = 200,
    push_url: str | None = None,
    is_htmx: bool = False,
) -> HttpResponse:
    context = build_inbox_context(
        request,
        capture_form=capture_form,
        selected_public_id=selected_public_id,
        inline_messages=is_htmx,
        capture_landed_in=capture_landed_in,
    )
    template_name = "inbox/_page.html" if is_htmx else "inbox/list.html"
    response = render(request, template_name, context, status=status)
    if is_htmx and push_url:
        response.headers["HX-Push-Url"] = push_url
    return response
