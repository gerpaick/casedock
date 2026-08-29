from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView

from apps.core.models import User
from apps.core.utils import is_htmx_request
from apps.execution.models import ExecutionItem, ExecutionState
from apps.focus.models import FocusAssignment
from apps.ui.views import build_board_context

from .forms import (
    CaseSpecForm,
    CaseStatusForm,
    DecisionForm,
    ExecutionItemForm,
    PrivateNoteForm,
)
from .models import Case, SpecDocument
from .services import ack_stale_case, resolve_stale_case

if TYPE_CHECKING:
    _CaseDetailView = DetailView[Case]
else:
    _CaseDetailView = DetailView


class CaseDetailView(LoginRequiredMixin, _CaseDetailView):
    model = Case
    template_name = "cases/detail.html"
    context_object_name = "case"

    def get_queryset(self) -> QuerySet[Case, Case]:
        user = self.request.user
        assert isinstance(user, User)
        return (
            Case.objects.filter(user=user)
            .select_related("spec_document")
            .prefetch_related("source_links", "decisions", "execution_items", "private_notes")
            .order_by("-updated_at", "-created_at")
        )

    def get_object(self, queryset: QuerySet[Case, Case] | None = None) -> Case:
        qs = queryset if queryset is not None else self.get_queryset()
        return get_object_or_404(qs, public_id=self.kwargs["public_id"])

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        case = context["case"]
        user = self.request.user
        assert isinstance(user, User)
        spec_document, _ = SpecDocument.objects.get_or_create(case=case, defaults={"user": user})
        execution_items = list(case.execution_items.all())
        focus_assignment = (
            FocusAssignment.objects.filter(
                user=user,
                focus_date=timezone.localdate(),
                case=case,
            )
            .order_by("role", "order")
            .first()
        )

        context["spec_document"] = spec_document
        context["spec_form"] = kwargs.get("spec_form") or CaseSpecForm(instance=spec_document)
        context["status_form"] = kwargs.get("status_form") or CaseStatusForm(case=case)
        context["decision_form"] = kwargs.get("decision_form") or DecisionForm()
        context["execution_form"] = kwargs.get("execution_form") or ExecutionItemForm()
        context["private_note_form"] = kwargs.get("private_note_form") or PrivateNoteForm()
        context["recent_decisions"] = case.decisions.order_by("-created_at")[:5]
        context["execution_items"] = execution_items
        context["open_execution_items"] = [
            item for item in execution_items if item.state != ExecutionState.DONE
        ]
        context["done_execution_items"] = [
            item for item in execution_items if item.state == ExecutionState.DONE
        ]
        context["private_notes"] = case.private_notes.order_by("-created_at")
        context["focus_assignment"] = focus_assignment
        return context


class CaseActionView(LoginRequiredMixin, View):
    form_class = None
    success_message = ""
    error_anchor = ""

    def get_case(self, public_id: UUID) -> Case:
        return get_object_or_404(Case, public_id=public_id, user=self.request.user)

    def get_success_url(self, case: Case) -> str:
        url = reverse("cases:detail", args=[case.public_id])
        if self.error_anchor:
            return f"{url}{self.error_anchor}"
        return url

    def render_detail(
        self, request: HttpRequest, case: Case, *, status: int = 400, **forms: object
    ) -> HttpResponse:
        view = CaseDetailView()
        view.request = request
        view.object = case
        context = view.get_context_data(**forms)
        return render(request, "cases/detail.html", context, status=status)


class CaseSpecUpdateView(CaseActionView):
    error_anchor = "#spec"

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        case = self.get_case(public_id)
        spec_document, _ = SpecDocument.objects.get_or_create(case=case, defaults={"user": user})
        form = CaseSpecForm(request.POST, instance=spec_document)
        if not form.is_valid():
            return self.render_detail(request, case, spec_form=form)

        form.save()
        messages.success(request, "Spec updated.")
        return redirect(self.get_success_url(case))


class CaseStatusUpdateView(CaseActionView):
    error_anchor = "#overview"

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        case = self.get_case(public_id)
        form = CaseStatusForm(request.POST, case=case)
        if not form.is_valid():
            return self.render_detail(request, case, status_form=form)

        new_status = form.cleaned_data["status"]
        case.transition_to(new_status)
        messages.success(request, f"Case moved to {case.get_status_display()}.")
        return redirect(self.get_success_url(case))


class CaseDecisionCreateView(CaseActionView):
    error_anchor = "#decisions"

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        case = self.get_case(public_id)
        form = DecisionForm(request.POST)
        if not form.is_valid():
            return self.render_detail(request, case, decision_form=form)

        decision = form.save(commit=False)
        decision.user = user
        decision.case = case
        decision.save()
        messages.success(request, "Decision captured.")
        return redirect(self.get_success_url(case))


class CaseExecutionCreateView(CaseActionView):
    error_anchor = "#execution"

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        case = self.get_case(public_id)
        form = ExecutionItemForm(request.POST)
        if not form.is_valid():
            return self.render_detail(request, case, execution_form=form)

        execution_item = form.save(commit=False)
        execution_item.user = user
        execution_item.case = case
        execution_item.save()
        messages.success(request, "Execution item added.")
        return redirect(self.get_success_url(case))


class CaseExecutionStateUpdateView(CaseActionView):
    error_anchor = "#execution"

    def post(self, request: HttpRequest, public_id: UUID, item_public_id: UUID) -> HttpResponse:
        case = self.get_case(public_id)
        execution_item = get_object_or_404(
            ExecutionItem, public_id=item_public_id, user=request.user, case=case
        )
        new_state = request.POST.get("state", execution_item.state)
        valid_states = {choice[0] for choice in ExecutionState.choices}
        if new_state not in valid_states:
            messages.error(request, "Unknown execution state.")
            return redirect(self.get_success_url(case))

        execution_item.state = new_state
        execution_item.save()
        messages.success(request, "Execution state updated.")
        return redirect(self.get_success_url(case))


class CasePrivateNoteCreateView(CaseActionView):
    error_anchor = "#private"

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        case = self.get_case(public_id)
        form = PrivateNoteForm(request.POST)
        if not form.is_valid():
            return self.render_detail(request, case, private_note_form=form)

        private_note = form.save(commit=False)
        private_note.user = user
        private_note.case = case
        private_note.save()
        messages.success(request, "Private note saved.")
        return redirect(self.get_success_url(case))


class StaleActionView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        case = get_object_or_404(Case, public_id=public_id, user=request.user)
        action = request.POST.get("action", "")

        if action == "ack":
            if case.stale_ack_count >= settings.CASEDOCK_STALE_ACK_LIMIT:
                messages.error(request, "Ack limit reached. Please resolve this case.")
            else:
                ack_stale_case(case)
                messages.success(request, "Acknowledged. We'll remind you again later.")
        elif action in ("done", "waiting"):
            resolve_stale_case(case, action)
            messages.success(request, f"Case moved to {action}.")
        else:
            messages.error(request, "Unknown action.")

        if is_htmx_request(request):
            return render(
                request,
                "ui/_board_page.html",
                build_board_context(request, inline_messages=True),
            )
        return redirect("ui:home")
