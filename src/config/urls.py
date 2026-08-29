from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cases/", include("apps.cases.urls")),
    path("focus/", include("apps.focus.urls")),
    path("inbox/", include("apps.inbox.urls")),
    path("", include("apps.core.urls")),
    path("", include("apps.ui.urls")),
]
