from __future__ import annotations

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.cases.models import Case, CaseStatus
from apps.inbox.models import InboxItem, InboxItemState
from apps.sources.models import SourceLink, SourceProvider

pytestmark = pytest.mark.django_db


def test_capture_creates_inbox_item(client):
    response = client.post(
        reverse("inbox:capture"),
        {
            "title": "Rough bug thought",
            "raw_body": "Something feels off in the auth flow.",
            "source_url": "",
            "capture_origin": "inbox",
        },
    )

    assert response.status_code == 302
    inbox_item = InboxItem.objects.get()
    assert inbox_item.title == "Rough bug thought"
    assert inbox_item.triage_state == InboxItemState.NEW
    assert response.url == reverse("inbox:list")


def test_capture_preserves_selected_now_item(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Keep this in front",
        triage_state=InboxItemState.DOING_NOW,
    )

    response = client.post(
        reverse("inbox:capture"),
        {
            "title": "Rough bug thought",
            "raw_body": "Something feels off in the auth flow.",
            "source_url": "",
            "capture_origin": "inbox",
            "selected": str(selected_item.public_id),
        },
    )

    assert response.status_code == 302
    assert response.url == f"{reverse('inbox:list')}?selected={selected_item.public_id}"


def test_capture_adds_new_item_to_end_of_queue(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Keep this in front",
        triage_state=InboxItemState.DOING_NOW,
    )
    older_new_item = InboxItem.objects.create(user=user, title="Older queued item")

    client.post(
        reverse("inbox:capture"),
        {
            "title": "Newest captured item",
            "raw_body": "",
            "source_url": "",
            "capture_origin": "inbox",
            "selected": str(selected_item.public_id),
        },
    )

    response = client.get(reverse("inbox:list"), {"selected": selected_item.public_id})

    assert response.status_code == 200
    assert response.context["selected_item"] == selected_item
    assert [item.title for item in response.context["queue_items"]] == [
        older_new_item.title,
        "Newest captured item",
    ]


def test_capture_with_source_url_sets_url_source_type(client):
    client.post(
        reverse("inbox:capture"),
        {
            "title": "Check linked doc",
            "raw_body": "",
            "source_url": "https://example.com/spec",
            "capture_origin": "inbox",
        },
    )

    inbox_item = InboxItem.objects.get()
    assert inbox_item.source_url == "https://example.com/spec"
    assert inbox_item.source_type == "url"


def test_park_action_moves_item_to_parked(client, user):
    inbox_item = InboxItem.objects.create(user=user, title="Park me")

    response = client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {"action": "park"},
    )

    assert response.status_code == 302
    inbox_item.refresh_from_db()
    assert inbox_item.triage_state == InboxItemState.PARKED


def test_park_action_moves_doing_now_item_to_parked(client, user):
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Pause me",
        triage_state=InboxItemState.DOING_NOW,
    )

    response = client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {"action": "park"},
    )

    assert response.status_code == 302
    inbox_item.refresh_from_db()
    assert inbox_item.triage_state == InboxItemState.PARKED


def test_waiting_action_moves_item_to_waiting(client, user):
    inbox_item = InboxItem.objects.create(user=user, title="Wait for info")

    client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {"action": "waiting"},
    )

    inbox_item.refresh_from_db()
    assert inbox_item.triage_state == InboxItemState.WAITING


def test_do_now_start_redirects_to_do_now_page(client, user):
    inbox_item = InboxItem.objects.create(user=user, title="Quick fix")

    response = client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {"action": "do_now"},
    )

    inbox_item.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("inbox:do_now", args=[inbox_item.public_id])
    assert inbox_item.triage_state == InboxItemState.DOING_NOW


def test_do_now_completion_marks_item_done_and_keeps_note(client, user):
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Quick fix",
        triage_state=InboxItemState.DOING_NOW,
    )

    response = client.post(
        reverse("inbox:do_now", args=[inbox_item.public_id]),
        {"completion_note": "Fixed and verified."},
    )

    assert response.status_code == 302
    inbox_item.refresh_from_db()
    assert inbox_item.triage_state == InboxItemState.DONE
    assert inbox_item.completion_note == "Fixed and verified."


def test_convert_creates_case_and_spec_and_marks_item_converted(client, user):
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Implement authentication",
        raw_body="Need to choose the simplest v1 auth shape.",
    )

    response = client.post(
        reverse("inbox:convert", args=[inbox_item.public_id]),
        {
            "working_title": "Email authentication",
            "outcome": "Users can sign in with email.",
            "clarity": "fuzzy",
            "next_step": "Choose auth flow.",
            "work_type": "build",
            "effort": "deep",
            "keep_source_link": "",
        },
    )

    inbox_item.refresh_from_db()
    case = inbox_item.converted_case
    assert response.status_code == 302
    assert case is not None
    assert case.title == "Email authentication"
    assert case.status == CaseStatus.ACTIVE
    assert case.spec_document.markdown_body.startswith("# Context")
    assert inbox_item.triage_state == InboxItemState.CONVERTED


def test_convert_moves_existing_source_link_to_case(client, user):
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Imported task",
        source_type="clickup",
    )
    source_link = SourceLink.objects.create(
        user=user,
        provider=SourceProvider.CLICKUP,
        inbox_item=inbox_item,
        external_id="CU-123",
        external_url="https://app.clickup.com/t/CU-123",
    )

    client.post(
        reverse("inbox:convert", args=[inbox_item.public_id]),
        {
            "working_title": "Imported task",
            "outcome": "",
            "clarity": "clear",
            "next_step": "Start work.",
            "work_type": "build",
            "effort": "medium",
            "keep_source_link": "on",
        },
    )

    source_link.refresh_from_db()
    inbox_item.refresh_from_db()
    assert source_link.case == inbox_item.converted_case
    assert source_link.inbox_item is None


def test_convert_creates_source_link_from_source_url_when_requested(client, user):
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Doc review",
        source_type="url",
        source_url="https://example.com/doc",
    )

    client.post(
        reverse("inbox:convert", args=[inbox_item.public_id]),
        {
            "working_title": "Doc review",
            "outcome": "",
            "clarity": "clear",
            "next_step": "Review the document.",
            "work_type": "research",
            "effort": "quick",
            "keep_source_link": "on",
        },
    )

    case = Case.objects.get()
    source_link = case.source_links.get()
    assert source_link.external_url == "https://example.com/doc"
    assert source_link.provider == SourceProvider.URL


def test_inbox_list_renders_items(client, user):
    InboxItem.objects.create(user=user, title="First item")

    response = client.get(reverse("inbox:list"))

    assert response.status_code == 200
    assert b"Triage what came in." in response.content
    assert b'<p class="eyebrow">Inbox</p>' not in response.content
    assert b"One item in front. The rest in view." not in response.content
    assert b"Drop it here before it drifts away." not in response.content
    assert b"page-head__top--inbox" in response.content
    assert b'id="quick-capture-trigger"' in response.content
    assert b"New Capture" in response.content
    assert b"vendor/tippy.css" in response.content
    assert b"vendor/popper.min.js" in response.content
    assert b"vendor/tippy-bundle.umd.min.js" in response.content


def test_inbox_nav_badge_matches_ready_count_on_inbox_page(client, user):
    InboxItem.objects.create(user=user, title="Fresh capture", triage_state=InboxItemState.NEW)
    InboxItem.objects.create(user=user, title="Doing now", triage_state=InboxItemState.DOING_NOW)
    InboxItem.objects.create(user=user, title="Waiting", triage_state=InboxItemState.WAITING)
    InboxItem.objects.create(user=user, title="Set aside", triage_state=InboxItemState.PARKED)
    InboxItem.objects.create(user=user, title="Done item", triage_state=InboxItemState.DONE)

    response = client.get(reverse("inbox:list"))

    assert response.status_code == 200
    assert response.context["ready_count"] == 4
    assert response.context["inbox_to_address_count"] == response.context["ready_count"]
    assert b'aria-label="Inbox, 4 to address"' in response.content


def test_inbox_list_uses_single_recent_outcomes_history_stream(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Handle this now",
        triage_state=InboxItemState.DOING_NOW,
    )
    InboxItem.objects.create(user=user, title="Queued next item")
    InboxItem.objects.create(
        user=user,
        title="Need to wait",
        triage_state=InboxItemState.WAITING,
    )
    converted_case = Case.objects.create(user=user, title="Shaped case", status=CaseStatus.ACTIVE)
    InboxItem.objects.create(
        user=user,
        title="Converted idea",
        triage_state=InboxItemState.CONVERTED,
        converted_case=converted_case,
    )
    InboxItem.objects.create(
        user=user,
        title="Done with note",
        triage_state=InboxItemState.DONE,
        completion_note="Fixed and verified.",
    )
    InboxItem.objects.create(
        user=user,
        title="Done without note",
        triage_state=InboxItemState.DONE,
    )

    response = client.get(reverse("inbox:list"), {"selected": selected_item.public_id})

    assert response.status_code == 200
    assert b"Recent outcomes" in response.content
    assert b"count-badge count-badge--queue" in response.content
    assert b"count-badge count-badge--history" in response.content
    assert b"inbox-history__headline" in response.content
    assert b"inbox-history__summary" not in response.content
    assert b"inbox-focus__action-bar" in response.content
    assert b"history-tag" in response.content
    assert b"history-row__title-link" in response.content
    assert b"data-history-tooltip" not in response.content
    assert b"history-row__meta" in response.content
    assert b"Converted" in response.content
    assert b"Done now" in response.content
    assert b"Set aside" in response.content
    assert b"Waiting on" in response.content
    assert b"button button-subtle" in response.content
    assert b"Completed without a note." not in response.content


def test_inbox_history_merges_converted_and_done_items_by_updated_at_and_limits_results(
    client, user
):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Handle this now",
        triage_state=InboxItemState.DOING_NOW,
    )
    base_time = timezone.now()
    rendered_titles: list[str] = []

    for index in range(6):
        if index % 2 == 0:
            converted_case = Case.objects.create(
                user=user,
                title=f"Case {index}",
                status=CaseStatus.ACTIVE,
            )
            inbox_item = InboxItem.objects.create(
                user=user,
                title=f"Converted item {index}",
                triage_state=InboxItemState.CONVERTED,
                converted_case=converted_case,
            )
        else:
            inbox_item = InboxItem.objects.create(
                user=user,
                title=f"Done item {index}",
                triage_state=InboxItemState.DONE,
            )
        timestamp = base_time - timedelta(minutes=index)
        InboxItem.objects.filter(pk=inbox_item.pk).update(updated_at=timestamp)
        rendered_titles.append(inbox_item.title)

    hidden_case = Case.objects.create(user=user, title="Older Case", status=CaseStatus.ACTIVE)
    hidden_item = InboxItem.objects.create(
        user=user,
        title="Older hidden item",
        triage_state=InboxItemState.CONVERTED,
        converted_case=hidden_case,
    )
    InboxItem.objects.filter(pk=hidden_item.pk).update(updated_at=base_time - timedelta(minutes=10))

    response = client.get(reverse("inbox:list"), {"selected": selected_item.public_id})

    assert response.status_code == 200
    assert [item.title for item in response.context["recent_outcomes"]] == rendered_titles
    assert response.context["recent_outcomes_count"] == 7
    assert response.context["recent_outcomes_has_more"] is True
    assert b"Older outcomes stay in history." in response.content
    assert hidden_item.title.encode() not in response.content


def test_queue_shows_url_as_source_chip_and_hides_manual_source_labels(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Selected manual item",
        triage_state=InboxItemState.DOING_NOW,
    )
    InboxItem.objects.create(
        user=user,
        title="Linked doc",
        source_type="url",
        source_url="https://example.com/spec",
    )

    response = client.get(reverse("inbox:list"), {"selected": selected_item.public_id})

    assert response.status_code == 200
    assert b'class="source-chip source-chip--inline"' in response.content
    assert b">URL</span>" in response.content
    assert b">Manual</span>" not in response.content


def test_focus_panel_moves_source_type_into_context_chip(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Selected linked item",
        triage_state=InboxItemState.DOING_NOW,
        source_type="url",
        source_url="https://example.com/spec",
        raw_body="Review this linked note before shaping it.",
    )
    InboxItem.objects.create(user=user, title="Queued next")

    response = client.get(reverse("inbox:list"), {"selected": selected_item.public_id})

    assert response.status_code == 200
    assert b"Source linked" in response.content
    assert b'class="source-chip source-chip--context"' in response.content
    assert b'<span class="muted">URL</span>' not in response.content


def test_inbox_detail_uses_source_chip_and_hides_manual_source_label(client, user):
    linked_item = InboxItem.objects.create(
        user=user,
        title="Linked detail",
        source_type="url",
        source_url="https://example.com/spec",
    )
    manual_item = InboxItem.objects.create(user=user, title="Manual detail")

    linked_response = client.get(reverse("inbox:detail", args=[linked_item.public_id]))
    manual_response = client.get(reverse("inbox:detail", args=[manual_item.public_id]))

    assert linked_response.status_code == 200
    assert manual_response.status_code == 200
    assert b'class="source-chip source-chip--detail"' in linked_response.content
    assert b">URL</span>" in linked_response.content
    assert b">Manual</span>" not in manual_response.content


def test_inbox_list_renders_htmx_hooks_for_inline_updates(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Keep this in front",
        triage_state=InboxItemState.DOING_NOW,
    )
    queued_item = InboxItem.objects.create(user=user, title="Queued next")

    response = client.get(reverse("inbox:list"), {"selected": selected_item.public_id})

    assert response.status_code == 200
    assert f'hx-get="/inbox/?selected={queued_item.public_id}"'.encode() in response.content
    assert b'hx-post="/inbox/capture/"' in response.content
    assert f'hx-post="/inbox/items/{selected_item.public_id}/triage/"'.encode() in response.content


def test_htmx_queue_selection_returns_partial_fragment(client, user):
    first_item = InboxItem.objects.create(user=user, title="First item")
    selected_item = InboxItem.objects.create(
        user=user,
        title="Move this to front",
        triage_state=InboxItemState.WAITING,
    )

    response = client.get(
        reverse("inbox:list"),
        {"selected": selected_item.public_id},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert response.context["selected_item"] == selected_item
    assert b'id="inbox-page"' in response.content
    assert b"Case work for one." not in response.content
    assert first_item.title.encode() in response.content


def test_htmx_capture_returns_partial_and_pushes_selected_url(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Keep this in front",
        triage_state=InboxItemState.DOING_NOW,
    )

    response = client.post(
        reverse("inbox:capture"),
        {
            "title": "Newest captured item",
            "raw_body": "",
            "source_url": "",
            "capture_origin": "inbox",
            "selected": str(selected_item.public_id),
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert (
        response.headers["HX-Push-Url"]
        == f"{reverse('inbox:list')}?selected={selected_item.public_id}"
    )
    assert response.context["selected_item"] == selected_item
    assert InboxItem.objects.filter(title="Newest captured item").exists()
    assert b'data-capture-landed-in="queue"' in response.content
    assert b'data-capture-destination="queue"' in response.content
    assert b"Captured &#x27;Newest captured item&#x27; in Inbox." in response.content


def test_htmx_capture_to_empty_inbox_marks_now_destination(client):
    response = client.post(
        reverse("inbox:capture"),
        {
            "title": "First capture",
            "raw_body": "",
            "source_url": "",
            "capture_origin": "inbox",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert response.context["selected_item"].title == "First capture"
    assert b'data-capture-landed-in="now"' in response.content
    assert b'data-capture-destination="now"' in response.content


def test_htmx_capture_validation_error_reopens_modal_and_preserves_selection(client, user):
    selected_item = InboxItem.objects.create(
        user=user,
        title="Keep this in front",
        triage_state=InboxItemState.DOING_NOW,
    )
    InboxItem.objects.create(user=user, title="Queued next")

    response = client.post(
        reverse("inbox:capture"),
        {
            "title": "",
            "raw_body": "",
            "source_url": "",
            "capture_origin": "inbox",
            "selected": str(selected_item.public_id),
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert response.context["selected_item"] == selected_item
    assert response.context["capture_modal_open"] is True
    assert b'data-open-on-load="true"' in response.content


def test_htmx_waiting_action_returns_partial_and_pushes_url(client, user):
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Wait for info",
        triage_state=InboxItemState.DOING_NOW,
    )
    queued_item = InboxItem.objects.create(user=user, title="Queued next")

    response = client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {
            "action": "waiting",
            "next": f"{reverse('inbox:list')}?selected={inbox_item.public_id}",
        },
        HTTP_HX_REQUEST="true",
    )

    inbox_item.refresh_from_db()
    assert response.status_code == 200
    assert (
        response.headers["HX-Push-Url"]
        == f"{reverse('inbox:list')}?selected={inbox_item.public_id}"
    )
    assert response.context["selected_item"] == inbox_item
    assert inbox_item.triage_state == InboxItemState.WAITING
    assert queued_item.title.encode() in response.content
    assert reverse("inbox:capture_page").encode() in response.content
    assert b"New Capture" in response.content
    assert b"button-capture" in response.content
    assert b"page-head__top--inbox" in response.content
    assert b"data-inbox-selected" in response.content
    assert b"data-inbox-queue" in response.content
    assert b"Moved &#x27;Wait for info&#x27; to Waiting on." in response.content


def test_capture_page_renders_form(client):
    response = client.get(reverse("inbox:capture_page"))

    assert response.status_code == 200
    assert b"Capture it quickly." in response.content
    assert b'name="capture_origin" value="page"' in response.content


def test_invalid_capture_from_inbox_reopens_modal(client):
    response = client.post(
        reverse("inbox:capture"),
        {
            "title": "",
            "raw_body": "Partial thought",
            "source_url": "",
            "capture_origin": "inbox",
        },
    )

    assert response.status_code == 400
    assert b'data-open-on-load="true"' in response.content
    assert b'value="Partial thought"' not in response.content
    assert b"Partial thought" in response.content


def test_invalid_capture_from_capture_page_stays_on_page(client):
    response = client.post(
        reverse("inbox:capture"),
        {
            "title": "",
            "raw_body": "Still incomplete",
            "source_url": "",
            "capture_origin": "page",
        },
    )

    assert response.status_code == 400
    assert b"Capture it quickly." in response.content
    assert b'data-open-on-load="true"' not in response.content
    assert b"Still incomplete" in response.content


def test_inbox_list_prioritizes_doing_now_item_in_focus_panel(client, user):
    doing_now_item = InboxItem.objects.create(
        user=user,
        title="Finish the tiny fix",
        triage_state=InboxItemState.DOING_NOW,
    )
    queued_item = InboxItem.objects.create(user=user, title="Freshly captured idea")

    response = client.get(reverse("inbox:list"))

    assert response.status_code == 200
    assert reverse("inbox:detail", args=[doing_now_item.public_id]).encode() in response.content
    assert b"Ready to triage" in response.content
    assert f'?selected={queued_item.public_id}"'.encode() in response.content


def test_inbox_list_allows_selecting_a_queue_item(client, user):
    first_item = InboxItem.objects.create(user=user, title="First item")
    second_item = InboxItem.objects.create(user=user, title="Second item")

    response = client.get(reverse("inbox:list"), {"selected": second_item.public_id})

    assert response.status_code == 200
    assert reverse("inbox:detail", args=[second_item.public_id]).encode() in response.content
    assert f'?selected={first_item.public_id}"'.encode() in response.content


def test_inbox_list_keeps_selected_item_out_of_queue(client, user):
    selected_item = InboxItem.objects.create(user=user, title="Selected item")
    queue_item = InboxItem.objects.create(user=user, title="Queue item")

    response = client.get(reverse("inbox:list"), {"selected": selected_item.public_id})

    assert response.status_code == 200
    assert reverse("inbox:detail", args=[selected_item.public_id]).encode() in response.content
    assert f'?selected={queue_item.public_id}"'.encode() in response.content
    assert response.context["selected_item"] == selected_item
    assert list(response.context["queue_items"]) == [queue_item]


def test_archive_action_moves_item_to_archived(client, user):
    inbox_item = InboxItem.objects.create(user=user, title="Archive me")

    response = client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {"action": "archive"},
    )

    assert response.status_code == 302
    assert response.url == reverse("inbox:list")
    inbox_item.refresh_from_db()
    assert inbox_item.triage_state == InboxItemState.ARCHIVED


def test_archive_action_returns_partial_without_selection(client, user):
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Archive me",
        triage_state=InboxItemState.DOING_NOW,
    )
    queued_item = InboxItem.objects.create(user=user, title="Queued next")

    response = client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {"action": "archive"},
        HTTP_HX_REQUEST="true",
    )

    inbox_item.refresh_from_db()
    assert response.status_code == 200
    assert b"data-inbox-page" in response.content
    assert inbox_item.triage_state == InboxItemState.ARCHIVED
    assert response.context["selected_item"] == queued_item
    assert reverse("inbox:detail", args=[queued_item.public_id]).encode() in response.content
    assert response.headers["HX-Push-Url"] == reverse("inbox:list")


def test_archive_action_works_from_converted_state(client, user):
    converted_case = Case.objects.create(
        user=user,
        title="Converted case",
        status=CaseStatus.ACTIVE,
    )
    inbox_item = InboxItem.objects.create(
        user=user,
        title="Already converted",
        triage_state=InboxItemState.CONVERTED,
        converted_case=converted_case,
    )

    response = client.post(
        reverse("inbox:triage", args=[inbox_item.public_id]),
        {"action": "archive"},
    )

    assert response.status_code == 302
    inbox_item.refresh_from_db()
    assert inbox_item.triage_state == InboxItemState.ARCHIVED


def test_archive_button_hidden_when_archived(client, user):
    archived_item = InboxItem.objects.create(
        user=user,
        title="Already archived",
        triage_state=InboxItemState.ARCHIVED,
    )
    active_item = InboxItem.objects.create(user=user, title="Active item")

    archived_response = client.get(reverse("inbox:detail", args=[archived_item.public_id]))
    active_response = client.get(reverse("inbox:detail", args=[active_item.public_id]))

    assert archived_response.status_code == 200
    assert active_response.status_code == 200
    assert b">Archive</button>" not in archived_response.content
    assert b">Archive</button>" in active_response.content


def test_global_capture_modal_present_on_non_inbox_page(client, user):
    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b'id="global-capture-modal"' in response.content
    assert b'id="capture-modal"' not in response.content


def test_global_capture_modal_present_on_inbox_page_alongside_inbox_modal(client, user):
    response = client.get(reverse("inbox:list"))

    assert response.status_code == 200
    assert b'id="capture-modal"' in response.content
    assert b'id="global-capture-modal"' in response.content


def test_keyboard_shortcuts_modal_lists_c(client, user):
    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b'id="keyboard-shortcuts-modal"' in response.content
    assert b"<kbd>c</kbd>" in response.content
    assert b"Capture inbox item (works anywhere)" in response.content
