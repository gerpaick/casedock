from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from apps.core.models import User
from apps.inbox.models import get_inbox_to_address_count

from .display import get_display_mode


def ui_preferences(request: HttpRequest) -> dict[str, Any]:
    user = request.user
    inbox_count = get_inbox_to_address_count(user) if isinstance(user, User) else 0
    return {
        "display_mode": get_display_mode(request),
        "inbox_to_address_count": inbox_count,
    }
