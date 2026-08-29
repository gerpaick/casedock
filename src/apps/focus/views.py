from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from apps.cases.models import Case, CaseStatus
from apps.core.models import User
from apps.core.utils import is_htmx_request
from apps.ui.views import build_board_context

from .forms import FocusSelectionForm
from .models import FocusAssignment, FocusRole
from .services import (
    add_secondary_case_for_day,
    clear_case_from_focus,
    replace_focus_for_day,
    set_main_case_for_day,
)


class FocusView(LoginRequiredMixin, View):
    template_name = "focus/today.html"

    def get_assignments(self) -> QuerySet[FocusAssignment, FocusAssignment]:
        user = self.request.user
        assert isinstance(user, User)
        return FocusAssignment.objects.filter(
            user=user,
            focus_date=timezone.localdate(),
        ).select_related("case")

    def get_context_data(self, *, form: FocusSelectionForm | None = None) -> dict[str, Any]:
        user = self.request.user
        assert isinstance(user, User)
        assignments = list(self.get_assignments().order_by("role", "order"))
        main_assignment = next(
            (assignment for assignment in assignments if assignment.role == FocusRole.MAIN),
            None,
        )
        secondary_assignments = [
            assignment for assignment in assignments if assignment.role == FocusRole.SECONDARY
        ]
        if form is None:
            initial = {
                "main_case": main_assignment.case_id if main_assignment else None,
                "secondary_case_one": (
                    secondary_assignments[0].case_id if len(secondary_assignments) >= 1 else None
                ),
                "secondary_case_two": (
                    secondary_assignments[1].case_id if len(secondary_assignments) >= 2 else None
                ),
            }
            form = FocusSelectionForm(user=user, initial=initial)
        return {
            "focus_date": timezone.localdate(),
            "form": form,
            "main_assignment": main_assignment,
            "secondary_assignments": secondary_assignments,
        }

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, self.get_context_data())

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        form = FocusSelectionForm(request.POST, user=user)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self.get_context_data(form=form),
                status=400,
            )

        secondary_cases = [
            case
            for case in [
                form.cleaned_data["secondary_case_one"],
                form.cleaned_data["secondary_case_two"],
            ]
            if case is not None
        ]
        replace_focus_for_day(
            user=user,
            focus_date=timezone.localdate(),
            main_case=form.cleaned_data["main_case"],
            secondary_cases=secondary_cases,
        )
        messages.success(request, "Today's focus updated.")
        return redirect("focus:today")


class FocusQuickActionView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        case = get_object_or_404(Case, public_id=request.POST.get("case_id"), user=request.user)
        action = request.POST.get("action")
        next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
        if not url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
        ):
            next_url = "/"

        focus_date = timezone.localdate()

        previous_main_case: Case | None = None
        if action == "set_main":
            current_main_assignment = (
                FocusAssignment.objects.filter(
                    user=user,
                    focus_date=focus_date,
                    role=FocusRole.MAIN,
                )
                .select_related("case")
                .first()
            )
            if (
                current_main_assignment
                and current_main_assignment.case.pk != case.pk
                and current_main_assignment.case.status == CaseStatus.ACTIVE
                and current_main_assignment.case.updated_at <= current_main_assignment.created_at
            ):
                previous_main_case = current_main_assignment.case

        try:
            if action == "set_main":
                set_main_case_for_day(user=user, focus_date=focus_date, case=case)
                messages.success(request, "Main focus updated.")
            elif action == "add_secondary":
                add_secondary_case_for_day(user=user, focus_date=focus_date, case=case)
                messages.success(request, "Secondary focus updated.")
            elif action == "clear":
                clear_case_from_focus(user=user, focus_date=focus_date, case=case)
                messages.success(request, "Focus updated.")
            else:
                messages.error(request, "Unknown focus action.")
        except ValidationError as exc:
            messages.error(request, exc.messages[0])

        if is_htmx_request(request) and request.POST.get("surface") == "board":
            ctx = build_board_context(request, inline_messages=True)
            ctx["previous_main_case"] = previous_main_case
            return render(request, "ui/_board_page.html", ctx)

        return redirect(next_url)
