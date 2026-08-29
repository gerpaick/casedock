from django.urls import path

from .views import FocusQuickActionView, FocusView

app_name = "focus"

urlpatterns = [
    path("", FocusView.as_view(), name="today"),
    path("actions/", FocusQuickActionView.as_view(), name="action"),
]
