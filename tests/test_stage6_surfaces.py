from __future__ import annotations

from django.urls import reverse
from django.utils import timezone

from apps.cases.models import Case, CaseStatus, SpecDocument
from apps.focus.models import FocusAssignment, FocusRole
from apps.inbox.models import InboxItem, InboxItemState


def test_board_home_surfaces_focus_and_stats(client, db, user):
    active_case = Case.objects.create(
        user=user,
        title="Active case",
        status=CaseStatus.ACTIVE,
        next_step="Keep moving.",
    )
    Case.objects.create(
        user=user,
        title="Waiting case",
        status=CaseStatus.WAITING,
        next_step="Wait for feedback.",
    )
    Case.objects.create(
        user=user,
        title="Done case",
        status=CaseStatus.DONE,
        summary="Wrapped up.",
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=active_case,
        role=FocusRole.MAIN,
        order=1,
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b'id="board-page"' in response.content
    assert b"data-board-home" in response.content
    assert b"Daily focus" in response.content
    assert b"data-board-focus-rail" in response.content
    assert b"board-focus-card__remove-form" in response.content
    assert response.content.count(b"board-focus-card__details") == 1
    assert response.context["active_count"] >= 1
    assert response.context["waiting_count"] >= 1
    assert response.context["done_count"] >= 1
    assert b"See all active" in response.content
    assert b"See waiting" in response.content


def test_board_home_renders_htmx_hooks_for_inline_focus_updates(client, db, user):
    case = Case.objects.create(user=user, title="Actionable case", status=CaseStatus.ACTIVE)
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=case,
        role=FocusRole.MAIN,
        order=1,
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert f'hx-post="{reverse("focus:action")}"'.encode() in response.content
    assert b'hx-target="#board-page"' in response.content
    assert b'hx-swap="outerHTML"' in response.content
    assert b'name="surface" value="board"' in response.content
    assert case.title.encode() in response.content


def test_board_focus_row_uses_three_slot_layout_with_two_secondary_cases(client, db, user):
    main_case = Case.objects.create(user=user, title="Main case", status=CaseStatus.ACTIVE)
    secondary_one = Case.objects.create(user=user, title="Secondary one", status=CaseStatus.WAITING)
    secondary_two = Case.objects.create(user=user, title="Secondary two", status=CaseStatus.ACTIVE)
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=secondary_one,
        role=FocusRole.SECONDARY,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=secondary_two,
        role=FocusRole.SECONDARY,
        order=2,
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert response.context["focus_slot_count"] == 3
    assert response.context["board_focus_layout_class"] == "board-focus-row--three"
    assert b"board-focus-row--three" in response.content
    assert b"board-focus-card__title--main" in response.content
    assert response.content.count(b"board-focus-card__title--secondary") == 2
    assert b"board-focus-card__note--main" in response.content
    assert response.content.count(b"board-focus-card__note--secondary") == 2


def test_board_focus_row_uses_two_slot_layout_with_one_secondary_case(client, db, user):
    main_case = Case.objects.create(user=user, title="Main case", status=CaseStatus.ACTIVE)
    secondary_case = Case.objects.create(
        user=user, title="Secondary case", status=CaseStatus.WAITING
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=secondary_case,
        role=FocusRole.SECONDARY,
        order=1,
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert response.context["focus_slot_count"] == 2
    assert response.context["board_focus_layout_class"] == "board-focus-row--two"
    assert b"board-focus-row--two" in response.content
    assert b'<span class="pill">Main</span>' in response.content
    assert b'<span class="pill">Secondary</span>' in response.content
    assert b'<span class="muted">Waiting</span>' in response.content
    assert b"board-focus-card__title--main" in response.content
    assert b"board-focus-card__title--secondary" in response.content
    assert b"board-focus-card__note--main" in response.content
    assert b"board-focus-card__note--secondary" in response.content


def test_primary_nav_shows_inbox_to_address_badge_for_ready_items(client, db, user):
    InboxItem.objects.create(user=user, title="Fresh capture", triage_state=InboxItemState.NEW)
    InboxItem.objects.create(user=user, title="In progress", triage_state=InboxItemState.DOING_NOW)
    InboxItem.objects.create(user=user, title="Waiting", triage_state=InboxItemState.WAITING)
    InboxItem.objects.create(user=user, title="Set aside", triage_state=InboxItemState.PARKED)
    InboxItem.objects.create(user=user, title="Handled", triage_state=InboxItemState.DONE)
    converted_case = Case.objects.create(
        user=user, title="Converted case", status=CaseStatus.ACTIVE
    )
    InboxItem.objects.create(
        user=user,
        title="Converted",
        triage_state=InboxItemState.CONVERTED,
        converted_case=converted_case,
    )

    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert response.context["inbox_to_address_count"] == 4
    assert b'aria-label="Inbox, 4 to address"' in response.content
    assert b'class="count-badge count-badge--nav"' in response.content


def test_primary_nav_hides_inbox_badge_when_nothing_is_to_address(client, db, user):
    InboxItem.objects.create(user=user, title="Already done", triage_state=InboxItemState.DONE)

    response = client.get(reverse("ui:settings"))

    assert response.status_code == 200
    assert response.context["inbox_to_address_count"] == 0
    assert b"count-badge count-badge--nav" not in response.content
    assert b'aria-label="Inbox,' not in response.content


def test_focus_view_post_sets_main_and_secondary_cases(client, db, user):
    main_case = Case.objects.create(user=user, title="Main case", status=CaseStatus.ACTIVE)
    secondary_case = Case.objects.create(
        user=user,
        title="Secondary case",
        status=CaseStatus.WAITING,
    )

    response = client.post(
        reverse("focus:today"),
        {
            "main_case": main_case.pk,
            "secondary_case_one": secondary_case.pk,
            "secondary_case_two": "",
        },
    )

    assert response.status_code == 302
    assignments = FocusAssignment.objects.filter(focus_date=timezone.localdate()).order_by(
        "role", "order"
    )
    assert assignments.count() == 2
    assert assignments[0].case == main_case
    assert assignments[0].role == FocusRole.MAIN
    assert assignments[1].case == secondary_case
    assert assignments[1].role == FocusRole.SECONDARY


def test_focus_view_prefills_existing_assignments(client, db, user):
    main_case = Case.objects.create(user=user, title="Main case", status=CaseStatus.ACTIVE)
    secondary_case = Case.objects.create(
        user=user, title="Secondary case", status=CaseStatus.WAITING
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=secondary_case,
        role=FocusRole.SECONDARY,
        order=1,
    )

    response = client.get(reverse("focus:today"))

    assert response.status_code == 200
    assert b"data-focus-primary" in response.content
    assert b"data-focus-setup" in response.content
    assert b"data-focus-current" in response.content
    assert b"focus-open-link" in response.content
    assert f'value="{main_case.pk}" selected'.encode() in response.content
    assert f'value="{secondary_case.pk}" selected'.encode() in response.content


def test_search_returns_matching_cases_and_inbox_items(client, db, user):
    case = Case.objects.create(
        user=user,
        title="Searchable case",
        status=CaseStatus.ACTIVE,
        summary="Calmer execution path.",
    )
    SpecDocument.objects.create(user=user, case=case, markdown_body="# Context\nSearch anchor")
    InboxItem.objects.create(user=user, title="Searchable inbox note", raw_body="Search anchor")

    response = client.get(reverse("ui:search"), {"q": "Search anchor"})

    assert response.status_code == 200
    assert b"data-search-results" in response.content
    assert b"Case" in response.content
    assert b"Inbox" in response.content
    assert b"Searchable case" in response.content
    assert b"Searchable inbox note" in response.content


def test_settings_page_renders(client, db):
    response = client.get(reverse("ui:settings"))

    assert response.status_code == 200
    assert b"Keep configuration quiet." in response.content
    assert b"Display mode" in response.content
    assert b'name="display_mode"' in response.content


def test_display_mode_controls_render_only_on_settings(client, db):
    board_response = client.get(reverse("ui:home"))
    inbox_response = client.get(reverse("inbox:list"))

    assert board_response.status_code == 200
    assert inbox_response.status_code == 200
    assert b'name="display_mode"' not in board_response.content
    assert b'name="display_mode"' not in inbox_response.content


def test_display_mode_switch_persists_in_session_and_changes_body_class(client, db):
    response = client.post(
        reverse("ui:display_mode"),
        {
            "display_mode": "compact",
            "next": reverse("ui:home"),
        },
        follow=True,
    )

    assert response.status_code == 200
    assert client.session["ui_display_mode"] == "compact"
    assert b"display-mode-compact" in response.content


def test_focus_quick_action_sets_main_from_board_surface(client, db, user):
    case = Case.objects.create(user=user, title="Board focus case", status=CaseStatus.ACTIVE)

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": case.public_id,
            "action": "set_main",
            "next": reverse("ui:home"),
        },
    )

    assert response.status_code == 302
    assignment = FocusAssignment.objects.get(focus_date=timezone.localdate())
    assert assignment.case == case
    assert assignment.role == FocusRole.MAIN


def test_htmx_focus_quick_action_sets_main_from_board_surface(client, db, user):
    case = Case.objects.create(user=user, title="Board focus case", status=CaseStatus.ACTIVE)

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": case.public_id,
            "action": "set_main",
            "surface": "board",
            "next": reverse("ui:home"),
        },
        HTTP_HX_REQUEST="true",
    )

    assignment = FocusAssignment.objects.get(focus_date=timezone.localdate())
    assert response.status_code == 200
    assert response.context["inline_messages"] is True
    assert response.context["focus_main_assignment"].case == case
    assert assignment.case == case
    assert b'id="board-page"' in response.content
    assert b"Main focus updated." in response.content


def test_focus_quick_action_adds_secondary_and_can_clear_main(client, db, user):
    main_case = Case.objects.create(user=user, title="Main case", status=CaseStatus.ACTIVE)
    secondary_case = Case.objects.create(
        user=user, title="Secondary case", status=CaseStatus.ACTIVE
    )
    other_secondary_case = Case.objects.create(
        user=user,
        title="Other secondary case",
        status=CaseStatus.WAITING,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )

    add_response = client.post(
        reverse("focus:action"),
        {
            "case_id": secondary_case.public_id,
            "action": "add_secondary",
            "next": reverse("ui:home"),
        },
    )
    client.post(
        reverse("focus:action"),
        {
            "case_id": other_secondary_case.public_id,
            "action": "add_secondary",
            "next": reverse("ui:home"),
        },
    )
    clear_response = client.post(
        reverse("focus:action"),
        {
            "case_id": main_case.public_id,
            "action": "clear",
            "next": reverse("ui:home"),
        },
    )

    assert add_response.status_code == 302
    assert clear_response.status_code == 302
    assignments = list(
        FocusAssignment.objects.filter(focus_date=timezone.localdate()).order_by("role", "order")
    )
    assert assignments[0].case == secondary_case
    assert assignments[0].role == FocusRole.MAIN
    assert assignments[1].case == other_secondary_case
    assert assignments[1].role == FocusRole.SECONDARY


def test_htmx_focus_quick_action_adds_secondary_from_board_surface(client, db, user):
    main_case = Case.objects.create(user=user, title="Main case", status=CaseStatus.ACTIVE)
    secondary_case = Case.objects.create(
        user=user, title="Secondary case", status=CaseStatus.ACTIVE
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": secondary_case.public_id,
            "action": "add_secondary",
            "surface": "board",
            "next": reverse("ui:home"),
        },
        HTTP_HX_REQUEST="true",
    )

    assignments = list(
        FocusAssignment.objects.filter(focus_date=timezone.localdate()).order_by("role", "order")
    )
    assert response.status_code == 200
    assert response.context["inline_messages"] is True
    assert response.context["focus_slot_count"] == 2
    assert assignments[1].case == secondary_case
    assert assignments[1].role == FocusRole.SECONDARY
    assert b'id="board-page"' in response.content
    assert b"Secondary focus updated." in response.content


def test_htmx_focus_quick_action_clears_focus_from_board_surface(client, db, user):
    main_case = Case.objects.create(user=user, title="Main case", status=CaseStatus.ACTIVE)
    secondary_case = Case.objects.create(
        user=user, title="Secondary case", status=CaseStatus.ACTIVE
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=secondary_case,
        role=FocusRole.SECONDARY,
        order=1,
    )

    response = client.post(
        reverse("focus:action"),
        {
            "case_id": main_case.public_id,
            "action": "clear",
            "surface": "board",
            "next": reverse("ui:home"),
        },
        HTTP_HX_REQUEST="true",
    )

    assignments = list(
        FocusAssignment.objects.filter(focus_date=timezone.localdate()).order_by("role", "order")
    )
    assert response.status_code == 200
    assert response.context["inline_messages"] is True
    assert response.context["focus_main_assignment"].case == secondary_case
    assert assignments[0].case == secondary_case
    assert assignments[0].role == FocusRole.MAIN
    assert b'id="board-page"' in response.content
    assert b"Focus updated." in response.content


def test_board_active_rows_render_lean_focus_actions(client, db, user):
    main_case = Case.objects.create(user=user, title="Main focus", status=CaseStatus.ACTIVE)
    focused_secondary = Case.objects.create(
        user=user, title="Focused secondary", status=CaseStatus.ACTIVE
    )
    Case.objects.create(user=user, title="Can add secondary", status=CaseStatus.ACTIVE)
    Case.objects.create(user=user, title="No action case", status=CaseStatus.ACTIVE)
    waiting_case = Case.objects.create(user=user, title="Waiting case", status=CaseStatus.WAITING)
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=focused_secondary,
        role=FocusRole.SECONDARY,
        order=1,
    )
    FocusAssignment.objects.create(
        user=user,
        focus_date=timezone.localdate(),
        case=waiting_case,
        role=FocusRole.SECONDARY,
        order=2,
    )

    response = client.get(reverse("ui:active"))

    assert response.status_code == 200
    active_cases = {case.title: case for case in response.context["active_cases"]}
    assert active_cases["Main focus"].board_action == "clear"
    assert active_cases["Focused secondary"].board_action == "clear"
    assert active_cases["Can add secondary"].board_action == ""
    assert active_cases["No action case"].board_action == ""
    assert response.content.count(b"Remove focus") >= 2
    assert b"Add secondary" not in response.content


def test_board_active_rows_offer_set_main_when_no_main_focus_exists(client, db, user):
    Case.objects.create(user=user, title="Promote me", status=CaseStatus.ACTIVE)

    response = client.get(reverse("ui:active"))

    assert response.status_code == 200
    active_case = response.context["active_cases"][0]
    assert active_case.board_action == "set_main"
    assert active_case.board_action_label == "Set main"
    assert b"Set main" in response.content
