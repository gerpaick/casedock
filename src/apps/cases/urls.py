from django.urls import path

from .views import (
    CaseDecisionCreateView,
    CaseDetailView,
    CaseExecutionCreateView,
    CaseExecutionStateUpdateView,
    CasePrivateNoteCreateView,
    CaseSpecUpdateView,
    CaseStatusUpdateView,
    StaleActionView,
)

app_name = "cases"

urlpatterns = [
    path("<uuid:public_id>/", CaseDetailView.as_view(), name="detail"),
    path("<uuid:public_id>/spec/", CaseSpecUpdateView.as_view(), name="spec_update"),
    path("<uuid:public_id>/status/", CaseStatusUpdateView.as_view(), name="status_update"),
    path("<uuid:public_id>/decisions/", CaseDecisionCreateView.as_view(), name="decision_create"),
    path(
        "<uuid:public_id>/execution/",
        CaseExecutionCreateView.as_view(),
        name="execution_create",
    ),
    path(
        "<uuid:public_id>/execution/<uuid:item_public_id>/state/",
        CaseExecutionStateUpdateView.as_view(),
        name="execution_state_update",
    ),
    path(
        "<uuid:public_id>/private-notes/",
        CasePrivateNoteCreateView.as_view(),
        name="private_note_create",
    ),
    path("<uuid:public_id>/stale/", StaleActionView.as_view(), name="stale_action"),
]
