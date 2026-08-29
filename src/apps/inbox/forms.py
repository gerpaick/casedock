from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django import forms

from apps.cases.models import CaseClarity, CaseEffort, CaseWorkType

from .models import InboxItem, InboxSourceType

if TYPE_CHECKING:
    from apps.core.models import User

    _InboxItemModelForm = forms.ModelForm[InboxItem]
else:
    _InboxItemModelForm = forms.ModelForm


class InboxCaptureForm(_InboxItemModelForm):
    class Meta:
        model = InboxItem
        fields = ("title", "raw_body", "source_url")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Capture the work as a short title"}),
            "raw_body": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Optional notes, pasted fragment, or rough context",
                }
            ),
            "source_url": forms.URLInput(attrs={"placeholder": "Optional source URL"}),
        }

    def save(self, commit: bool = True, *, user: User | None = None) -> InboxItem:
        instance = super().save(commit=False)
        if user is not None:
            instance.user = user
        instance.source_type = (
            InboxSourceType.URL if self.cleaned_data.get("source_url") else InboxSourceType.MANUAL
        )
        if commit:
            instance.save()
        return instance


class DoNowCompletionForm(_InboxItemModelForm):
    class Meta:
        model = InboxItem
        fields = ("completion_note",)
        widgets = {
            "completion_note": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Optional short completion note",
                }
            )
        }


class ConvertToCaseForm(forms.Form):
    working_title = forms.CharField(max_length=255)
    outcome = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "What should be true when this work is shaped well?",
            }
        ),
    )
    clarity = forms.ChoiceField(choices=CaseClarity.choices)
    next_step = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "The next concrete move",
            }
        ),
    )
    work_type = forms.ChoiceField(choices=CaseWorkType.choices)
    effort = forms.ChoiceField(choices=CaseEffort.choices)
    keep_source_link = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args: Any, inbox_item: InboxItem, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.inbox_item = inbox_item
        self.fields["working_title"].initial = inbox_item.title
        self.fields["outcome"].initial = inbox_item.raw_body
        self.fields["clarity"].initial = CaseClarity.FUZZY
        self.fields["work_type"].initial = CaseWorkType.BUILD
        self.fields["effort"].initial = CaseEffort.MEDIUM
        self.fields["keep_source_link"].initial = bool(
            inbox_item.source_url or inbox_item.source_links.exists()
        )
