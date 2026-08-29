from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from .forms import InboxCaptureForm


def inbox_global_capture(request: HttpRequest) -> dict[str, Any]:
    """Provide an empty InboxCaptureForm globally for the global capture modal."""
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {}
    return {"global_capture_form": InboxCaptureForm()}
