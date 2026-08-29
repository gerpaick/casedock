from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import TemplateView

from apps.cases.models import Case, CaseStatus
from apps.cases.services import get_stale_cases
from apps.core.models import User
from apps.focus.models import FocusAssignment, FocusRole
from apps.inbox.models import InboxItem

from .display import DISPLAY_MODE_SESSION_KEY, normalize_display_mode


def build_focus_lookup(*, user: User) -> tuple[list[FocusAssignment], dict[int, str]]:
    assignments = list(
        FocusAssignment.objects.filter(user=user, focus_date=timezone.localdate())
        .select_related("case")
        .order_by("role", "order")
    )
    focus_roles = {assignment.case_id: assignment.role for assignment in assignments}
    return assignments, focus_roles


def attach_focus_roles(cases: list[Case], focus_roles: dict[int, str]) -> list[Case]:
    for case in cases:
        case.focus_role = focus_roles.get(case.pk, "")
    return cases


def build_board_focus_context(assignments: list[FocusAssignment]) -> dict[str, Any]:
    main_assignment = next(
        (assignment for assignment in assignments if assignment.role == FocusRole.MAIN),
        None,
    )
    secondary_assignments = [
        assignment for assignment in assignments if assignment.role == FocusRole.SECONDARY
    ]

    if main_assignment is None:
        layout_class = "board-focus-row--empty"
    elif len(secondary_assignments) >= 2:
        layout_class = "board-focus-row--three"
    elif len(secondary_assignments) == 1:
        layout_class = "board-focus-row--two"
    else:
        layout_class = "board-focus-row--single"

    return {
        "focus_main_assignment": main_assignment,
        "focus_secondary_assignments": secondary_assignments[:2],
        "focus_slot_count": (1 if main_assignment else 0) + len(secondary_assignments[:2]),
        "board_focus_layout_class": layout_class,
    }


def attach_board_actions(
    cases: list[Case],
    *,
    focus_roles: dict[int, str],
    has_main_focus: bool,
    open_secondary_slots: int,
) -> list[Case]:
    for case in cases:
        case.focus_role = focus_roles.get(case.pk, "")
        case.board_action = ""
        case.board_action_label = ""

        if case.focus_role:
            case.board_action = "clear"
            case.board_action_label = "Remove focus"
        elif not has_main_focus:
            case.board_action = "set_main"
            case.board_action_label = "Set main"
        elif open_secondary_slots > 0:
            case.board_action = "add_secondary"
            case.board_action_label = "Add secondary"

    return cases


def build_board_context(request: HttpRequest, *, inline_messages: bool = False) -> dict[str, Any]:
    user = request.user
    assert isinstance(user, User)
    assignments, _focus_roles = build_focus_lookup(user=user)
    focus_context = build_board_focus_context(assignments)
    focus_case_ids = {a.case_id for a in assignments}

    stale_cases = list(
        get_stale_cases(
            user=user,
            exclude_focus_case_ids=focus_case_ids,
        )[:3]
    )
    stale_ack_limit = settings.CASEDOCK_STALE_ACK_LIMIT
    for case in stale_cases:
        case.days_stale = (timezone.now() - case.updated_at).days
        case.can_ack = case.stale_ack_count < stale_ack_limit

    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())

    active_count = Case.objects.filter(user=user, status=CaseStatus.ACTIVE).count()
    waiting_count = Case.objects.filter(user=user, status=CaseStatus.WAITING).count()
    done_count = Case.objects.filter(
        user=user,
        status=CaseStatus.DONE,
        completed_at__date__gte=week_start,
    ).count()

    return {
        "inline_messages": inline_messages,
        "stale_cases": stale_cases,
        "stale_ack_limit": settings.CASEDOCK_STALE_ACK_LIMIT,
        "active_count": active_count,
        "waiting_count": waiting_count,
        "done_count": done_count,
        **focus_context,
    }


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "ui/home.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(build_board_context(self.request))
        return context


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "ui/search.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        assert isinstance(user, User)
        query = self.request.GET.get("q", "").strip()
        case_results: QuerySet[Case] = Case.objects.none()
        inbox_results: QuerySet[InboxItem] = InboxItem.objects.none()

        if query:
            case_results = (
                Case.objects.filter(user=user)
                .prefetch_related("source_links")
                .filter(
                    Q(title__icontains=query)
                    | Q(summary__icontains=query)
                    | Q(next_step__icontains=query)
                    | Q(spec_document__markdown_body__icontains=query)
                    | Q(decisions__body__icontains=query)
                    | Q(decisions__title__icontains=query)
                    | Q(execution_items__title__icontains=query)
                    | Q(execution_items__note__icontains=query)
                )
                .distinct()
                .order_by("-updated_at", "-created_at")[:12]
            )
            inbox_results = (
                InboxItem.objects.filter(
                    user=user,
                )
                .filter(
                    Q(title__icontains=query)
                    | Q(raw_body__icontains=query)
                    | Q(source_url__icontains=query)
                )
                .order_by("-updated_at", "-created_at")[:12]
            )

        context["query"] = query
        context["case_results"] = case_results
        context["inbox_results"] = inbox_results
        return context


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "ui/settings.html"


class DisplayModeUpdateView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
        if not url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
        ):
            next_url = "/"

        display_mode = normalize_display_mode(request.POST.get("display_mode"))
        request.session[DISPLAY_MODE_SESSION_KEY] = display_mode
        messages.success(request, f"Display mode set to {display_mode}.")
        return redirect(next_url)


class ActiveCasesView(LoginRequiredMixin, TemplateView):
    template_name = "ui/active.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        assert isinstance(user, User)
        assignments, focus_roles = build_focus_lookup(user=user)
        active_cases = list(
            Case.objects.filter(user=user, status=CaseStatus.ACTIVE).order_by(
                "-updated_at", "-created_at"
            )
        )
        active_cases = attach_board_actions(
            active_cases,
            focus_roles=focus_roles,
            has_main_focus=any(a.role == FocusRole.MAIN for a in assignments),
            open_secondary_slots=max(
                0, 2 - sum(1 for a in assignments if a.role == FocusRole.SECONDARY)
            ),
        )
        stale_ids = set(get_stale_cases(user=user).values_list("pk", flat=True))
        for case in active_cases:
            case.is_stale = case.pk in stale_ids
        focused = [c for c in active_cases if c.focus_role]
        unfocused_fresh = [c for c in active_cases if not c.focus_role and not c.is_stale]
        stale_cases = [c for c in active_cases if not c.focus_role and c.is_stale]
        for case in stale_cases:
            case.days_stale = (timezone.now() - case.updated_at).days
        context["active_cases"] = focused + unfocused_fresh + stale_cases
        context["active_count"] = len(active_cases)
        return context


class WaitingCasesView(LoginRequiredMixin, TemplateView):
    template_name = "ui/waiting.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        assert isinstance(user, User)
        waiting_cases = list(
            Case.objects.filter(user=user, status=CaseStatus.WAITING)
            .prefetch_related("source_links")
            .order_by("-updated_at", "-created_at")
        )
        context["waiting_cases"] = attach_focus_roles(
            waiting_cases, build_focus_lookup(user=user)[1]
        )
        context["waiting_count"] = len(waiting_cases)
        return context
