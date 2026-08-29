from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, TemplateView

from apps.core.models import User
from apps.core.utils import is_htmx_request

from .context import (
    build_inbox_url,
    coerce_selected_public_id,
    render_inbox_response,
)
from .forms import ConvertToCaseForm, DoNowCompletionForm, InboxCaptureForm
from .models import READY_INBOX_STATES, InboxItem, InboxItemState
from .services import convert_inbox_item_to_case

if TYPE_CHECKING:
    _InboxDetailView = DetailView[InboxItem]
else:
    _InboxDetailView = DetailView


def _render_capture_page(
    request: HttpRequest, *, form: InboxCaptureForm | None = None, status: int = 200
) -> HttpResponse:
    return render(
        request,
        "inbox/capture_page.html",
        {"capture_form": form or InboxCaptureForm()},
        status=status,
    )


class InboxListView(LoginRequiredMixin, TemplateView):
    template_name = "inbox/list.html"

    def get_template_names(self) -> list[str]:
        if is_htmx_request(self.request):
            return ["inbox/_page.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        from .context import build_inbox_context

        context = super().get_context_data(**kwargs)
        capture_form_kwarg = kwargs.get("capture_form")
        selected_public_id_kwarg = kwargs.get("selected_public_id")
        context.update(
            build_inbox_context(
                self.request,
                capture_form=(
                    capture_form_kwarg if isinstance(capture_form_kwarg, InboxCaptureForm) else None
                ),
                selected_public_id=(
                    selected_public_id_kwarg if isinstance(selected_public_id_kwarg, UUID) else None
                ),
                inline_messages=is_htmx_request(self.request),
            )
        )
        return context


class InboxCapturePageView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return _render_capture_page(request)


class InboxCaptureView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        form = InboxCaptureForm(request.POST)
        is_htmx = is_htmx_request(request)
        selected_public_id = coerce_selected_public_id(request.POST.get("selected"))
        capture_landed_in = (
            "queue"
            if InboxItem.objects.filter(user=user, triage_state__in=READY_INBOX_STATES).exists()
            else "now"
        )
        if form.is_valid():
            inbox_item = form.save(user=user)
            messages.success(request, f"Captured '{inbox_item.title}' in Inbox.")
            inbox_url = build_inbox_url(selected_public_id=selected_public_id)
            if is_htmx:
                return render_inbox_response(
                    request,
                    capture_landed_in=capture_landed_in,
                    selected_public_id=selected_public_id,
                    push_url=inbox_url,
                    is_htmx=True,
                )
            return redirect(inbox_url)

        if request.POST.get("capture_origin") == "page":
            return _render_capture_page(request, form=form, status=400)

        return render_inbox_response(
            request,
            capture_form=form,
            selected_public_id=selected_public_id,
            status=200 if is_htmx else 400,
            is_htmx=is_htmx,
        )


class InboxDetailView(LoginRequiredMixin, _InboxDetailView):
    model = InboxItem
    template_name = "inbox/detail.html"
    context_object_name = "inbox_item"

    def get_queryset(self) -> QuerySet[InboxItem, InboxItem]:
        user = self.request.user
        assert isinstance(user, User)
        return InboxItem.objects.filter(user=user)

    def get_object(self, queryset: QuerySet[InboxItem, InboxItem] | None = None) -> InboxItem:
        qs = queryset if queryset is not None else self.get_queryset()
        return get_object_or_404(qs, public_id=self.kwargs["public_id"])


class InboxTriageActionView(LoginRequiredMixin, View):
    action_to_state = {
        "park": InboxItemState.PARKED,
        "waiting": InboxItemState.WAITING,
        "archive": InboxItemState.ARCHIVED,
    }

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        inbox_item = get_object_or_404(InboxItem, public_id=public_id, user=request.user)
        action = request.POST.get("action")
        is_htmx = is_htmx_request(request)

        if action == "do_now":
            if inbox_item.triage_state != InboxItemState.DOING_NOW:
                inbox_item.transition_to(InboxItemState.DOING_NOW)
            return redirect("inbox:do_now", public_id=inbox_item.public_id)

        if action not in self.action_to_state:
            messages.error(request, "Unknown triage action.")
            if is_htmx:
                return render_inbox_response(request, is_htmx=True)
            return redirect("inbox:list")

        target_state = self.action_to_state[action]
        if target_state == InboxItemState.ARCHIVED and inbox_item.converted_case_id is not None:
            # Spec L71-73: only CONVERTED items may keep a converted_case reference.
            # Clear it in the same save as the state change so full_clean() passes.
            inbox_item.transition_to(target_state, save=False)
            inbox_item.converted_case = None
            inbox_item.save(update_fields=["triage_state", "converted_case", "updated_at"])
        else:
            inbox_item.transition_to(target_state)
        if target_state == InboxItemState.ARCHIVED:
            # Archived items exit READY_INBOX_STATES, so they cannot remain the selection.
            messages.success(request, f"Archived '{inbox_item.title}'.")
            selected_public_id: UUID | None = None
        else:
            messages.success(
                request,
                f"Moved '{inbox_item.title}' to {inbox_item.get_triage_state_display()}.",
            )
            selected_public_id = inbox_item.public_id
        next_url = request.POST.get("next")
        if is_htmx:
            return render_inbox_response(
                request,
                selected_public_id=selected_public_id,
                push_url=next_url or build_inbox_url(selected_public_id=selected_public_id),
                is_htmx=True,
            )
        if next_url:
            return redirect(next_url)
        return redirect("inbox:list")


class InboxDoNowView(LoginRequiredMixin, View):
    template_name = "inbox/do_now.html"

    def get(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        inbox_item = get_object_or_404(InboxItem, public_id=public_id, user=request.user)
        form = DoNowCompletionForm(instance=inbox_item)
        return render(
            request,
            self.template_name,
            {"form": form, "inbox_item": inbox_item},
        )

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        inbox_item = get_object_or_404(InboxItem, public_id=public_id, user=request.user)
        form = DoNowCompletionForm(request.POST, instance=inbox_item)
        if form.is_valid():
            inbox_item = form.save(commit=False)
            if inbox_item.triage_state != InboxItemState.DOING_NOW:
                inbox_item.triage_state = InboxItemState.DOING_NOW
            inbox_item.transition_to(InboxItemState.DONE, save=False)
            inbox_item.save()
            messages.success(request, f"Marked '{inbox_item.title}' as done.")
            return redirect("inbox:list")

        return render(
            request,
            self.template_name,
            {"form": form, "inbox_item": inbox_item},
            status=400,
        )


class InboxConvertView(LoginRequiredMixin, View):
    template_name = "inbox/convert.html"

    def get(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        inbox_item = get_object_or_404(InboxItem, public_id=public_id, user=request.user)
        form = ConvertToCaseForm(inbox_item=inbox_item)
        return render(
            request,
            self.template_name,
            {"form": form, "inbox_item": inbox_item},
        )

    def post(self, request: HttpRequest, public_id: UUID) -> HttpResponse:
        user = request.user
        assert isinstance(user, User)
        inbox_item = get_object_or_404(InboxItem, public_id=public_id, user=request.user)
        form = ConvertToCaseForm(request.POST, inbox_item=inbox_item)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "inbox_item": inbox_item},
                status=400,
            )

        case = convert_inbox_item_to_case(
            user=user,
            inbox_item=inbox_item,
            working_title=form.cleaned_data["working_title"],
            outcome=form.cleaned_data["outcome"],
            clarity=form.cleaned_data["clarity"],
            next_step=form.cleaned_data["next_step"],
            work_type=form.cleaned_data["work_type"],
            effort=form.cleaned_data["effort"],
            keep_source_link=form.cleaned_data["keep_source_link"],
        )
        messages.success(request, f"Converted '{inbox_item.title}' into a Case.")
        return HttpResponseRedirect(reverse("cases:detail", args=[case.public_id]))
