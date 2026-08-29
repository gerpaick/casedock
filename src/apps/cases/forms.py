from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django import forms

from apps.decisions.models import Decision
from apps.execution.models import ExecutionItem, ExecutionState

from .models import CASE_ALLOWED_TRANSITIONS, Case, CaseStatus, PrivateNote, SpecDocument

if TYPE_CHECKING:
    _SpecModelForm = forms.ModelForm[SpecDocument]
    _DecisionModelForm = forms.ModelForm[Decision]
    _ExecutionModelForm = forms.ModelForm[ExecutionItem]
    _PrivateNoteModelForm = forms.ModelForm[PrivateNote]
else:
    _SpecModelForm = forms.ModelForm
    _DecisionModelForm = forms.ModelForm
    _ExecutionModelForm = forms.ModelForm
    _PrivateNoteModelForm = forms.ModelForm


class CaseSpecForm(_SpecModelForm):
    class Meta:
        model = SpecDocument
        fields = ("markdown_body",)
        widgets = {
            "markdown_body": forms.Textarea(
                attrs={
                    "rows": 14,
                    "placeholder": (
                        "Keep context, constraints, and rough shaping close to the Case."
                    ),
                }
            ),
        }


class CaseStatusForm(forms.Form):
    status = forms.ChoiceField()

    def __init__(self, *args: Any, case: Case, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.case = case
        label_map = dict(CaseStatus.choices)
        field_order = [value for value, _label in CaseStatus.choices]
        current_status = CaseStatus(case.status)
        allowed_set = {current_status, *CASE_ALLOWED_TRANSITIONS[current_status]}
        status_field = self.fields["status"]
        if isinstance(status_field, forms.ChoiceField):
            status_field.choices = [
                (value, label_map[value]) for value in field_order if value in allowed_set
            ]
            status_field.initial = case.status


class DecisionForm(_DecisionModelForm):
    class Meta:
        model = Decision
        fields = (
            "body",
            "promoted",
            "title",
            "tag",
            "rationale",
            "alternatives",
            "consequence",
        )
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Capture the choice or constraint in plain language.",
                }
            ),
            "title": forms.TextInput(attrs={"placeholder": "Required only for promoted decisions"}),
            "tag": forms.TextInput(attrs={"placeholder": "Optional tag"}),
            "rationale": forms.Textarea(attrs={"rows": 3, "placeholder": "Why this path?"}),
            "alternatives": forms.Textarea(
                attrs={"rows": 3, "placeholder": "What did you not choose?"}
            ),
            "consequence": forms.Textarea(
                attrs={"rows": 3, "placeholder": "What follows from this?"}
            ),
        }


class ExecutionItemForm(_ExecutionModelForm):
    class Meta:
        model = ExecutionItem
        fields = ("title", "section", "note", "state")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "A concrete next step or check"}),
            "section": forms.TextInput(
                attrs={"placeholder": "Optional group such as setup or rollout"}
            ),
            "note": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional detail"}),
            "state": forms.Select(),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["state"].initial = ExecutionState.TODO


class PrivateNoteForm(_PrivateNoteModelForm):
    class Meta:
        model = PrivateNote
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "User-only thinking. This stays inside casedock.",
                }
            )
        }
