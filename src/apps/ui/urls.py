from django.urls import path

from .views import (
    ActiveCasesView,
    DisplayModeUpdateView,
    HomeView,
    SearchView,
    SettingsView,
    WaitingCasesView,
)

app_name = "ui"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("active/", ActiveCasesView.as_view(), name="active"),
    path("waiting/", WaitingCasesView.as_view(), name="waiting"),
    path("search/", SearchView.as_view(), name="search"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("settings/display-mode/", DisplayModeUpdateView.as_view(), name="display_mode"),
]
