from django.urls import path

from .views import (
    InboxCapturePageView,
    InboxCaptureView,
    InboxConvertView,
    InboxDetailView,
    InboxDoNowView,
    InboxListView,
    InboxTriageActionView,
)

app_name = "inbox"

urlpatterns = [
    path("", InboxListView.as_view(), name="list"),
    path("capture/", InboxCaptureView.as_view(), name="capture"),
    path("capture/new/", InboxCapturePageView.as_view(), name="capture_page"),
    path("items/<uuid:public_id>/", InboxDetailView.as_view(), name="detail"),
    path("items/<uuid:public_id>/triage/", InboxTriageActionView.as_view(), name="triage"),
    path("items/<uuid:public_id>/do-now/", InboxDoNowView.as_view(), name="do_now"),
    path("items/<uuid:public_id>/convert/", InboxConvertView.as_view(), name="convert"),
]
