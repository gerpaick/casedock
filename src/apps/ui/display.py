from __future__ import annotations

from django.http import HttpRequest

DISPLAY_MODE_SESSION_KEY = "ui_display_mode"
DEFAULT_DISPLAY_MODE = "calm"
VALID_DISPLAY_MODES = {DEFAULT_DISPLAY_MODE, "compact"}


def normalize_display_mode(value: str | None) -> str:
    if value in VALID_DISPLAY_MODES:
        return value
    return DEFAULT_DISPLAY_MODE


def get_display_mode(request: HttpRequest) -> str:
    return normalize_display_mode(request.session.get(DISPLAY_MODE_SESSION_KEY))
