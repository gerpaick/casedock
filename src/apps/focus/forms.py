from __future__ import annotations

from typing import Any

from django import forms

from apps.cases.models import Case, CaseStatus
from apps.core.models import User


class FocusSelectionForm(forms.Form):
    main_case = forms.ModelChoiceField(
        queryset=Case.objects.none(),
        empty_label="Choose the main Case",
    )
    secondary_case_one = forms.ModelChoiceField(
        queryset=Case.objects.none(),
        required=False,
        empty_label="Optional secondary Case",
    )
    secondary_case_two = forms.ModelChoiceField(
        queryset=Case.objects.none(),
        required=False,
        empty_label="Optional secondary Case",
    )

    def __init__(self, *args: Any, user: User | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        case_qs = Case.objects.filter(user=user) if user is not None else Case.objects.none()
        candidate_cases = case_qs.filter(
            status__in=[CaseStatus.ACTIVE, CaseStatus.WAITING]
        ).order_by("status", "title")
        for field_name in ("main_case", "secondary_case_one", "secondary_case_two"):
            field = self.fields[field_name]
            if isinstance(field, forms.ModelChoiceField):
                field.queryset = candidate_cases

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        if cleaned_data is None:
            return {}
        selected_cases = [
            cleaned_data.get("main_case"),
            cleaned_data.get("secondary_case_one"),
            cleaned_data.get("secondary_case_two"),
        ]
        selected_ids = [case.pk for case in selected_cases if case is not None]
        if len(selected_ids) != len(set(selected_ids)):
            raise forms.ValidationError("Choose different Cases for each focus slot.")
        return cleaned_data
