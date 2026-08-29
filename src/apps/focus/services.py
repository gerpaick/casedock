from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.cases.models import Case

from .models import FocusAssignment, FocusRole

if TYPE_CHECKING:
    from apps.core.models import User


@transaction.atomic
def replace_focus_for_day(
    *,
    user: User,
    focus_date: date,
    main_case: Case,
    secondary_cases: list[Case],
) -> None:
    FocusAssignment.objects.filter(user=user, focus_date=focus_date).delete()
    FocusAssignment.objects.create(
        user=user,
        focus_date=focus_date,
        case=main_case,
        role=FocusRole.MAIN,
        order=1,
    )
    for order, case in enumerate(secondary_cases, start=1):
        FocusAssignment.objects.create(
            user=user,
            focus_date=focus_date,
            case=case,
            role=FocusRole.SECONDARY,
            order=order,
        )


def get_focus_cases_for_day(*, user: User, focus_date: date) -> tuple[Case | None, list[Case]]:
    assignments = list(
        FocusAssignment.objects.filter(user=user, focus_date=focus_date)
        .select_related("case")
        .order_by("role", "order")
    )
    main_case = next(
        (assignment.case for assignment in assignments if assignment.role == FocusRole.MAIN),
        None,
    )
    secondary_cases = [
        assignment.case for assignment in assignments if assignment.role == FocusRole.SECONDARY
    ]
    return main_case, secondary_cases


def set_main_case_for_day(*, user: User, focus_date: date, case: Case) -> None:
    _main_case, secondary_cases = get_focus_cases_for_day(user=user, focus_date=focus_date)
    preserved_secondary_cases = [
        secondary_case for secondary_case in secondary_cases if secondary_case.pk != case.pk
    ][:2]
    replace_focus_for_day(
        user=user,
        focus_date=focus_date,
        main_case=case,
        secondary_cases=preserved_secondary_cases,
    )


def add_secondary_case_for_day(*, user: User, focus_date: date, case: Case) -> None:
    main_case, secondary_cases = get_focus_cases_for_day(user=user, focus_date=focus_date)
    if main_case is None:
        raise ValidationError("Choose a main Case first.")
    if main_case.pk == case.pk:
        return
    if any(secondary_case.pk == case.pk for secondary_case in secondary_cases):
        return
    if len(secondary_cases) >= 2:
        raise ValidationError("Focus already has two secondary Cases. Open Focus to rebalance it.")

    replace_focus_for_day(
        user=user,
        focus_date=focus_date,
        main_case=main_case,
        secondary_cases=[*secondary_cases, case],
    )


def clear_case_from_focus(*, user: User, focus_date: date, case: Case) -> None:
    main_case, secondary_cases = get_focus_cases_for_day(user=user, focus_date=focus_date)
    remaining_secondary_cases = [
        secondary_case for secondary_case in secondary_cases if secondary_case.pk != case.pk
    ]

    if main_case and main_case.pk == case.pk:
        if remaining_secondary_cases:
            replace_focus_for_day(
                user=user,
                focus_date=focus_date,
                main_case=remaining_secondary_cases[0],
                secondary_cases=remaining_secondary_cases[1:3],
            )
            return
        FocusAssignment.objects.filter(user=user, focus_date=focus_date).delete()
        return

    if main_case is not None:
        replace_focus_for_day(
            user=user,
            focus_date=focus_date,
            main_case=main_case,
            secondary_cases=remaining_secondary_cases,
        )
