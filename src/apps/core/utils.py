from __future__ import annotations

from django.http import HttpRequest


def is_htmx_request(request: HttpRequest) -> bool:
    return request.headers.get("HX-Request") == "true"
