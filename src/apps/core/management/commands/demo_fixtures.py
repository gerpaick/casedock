from __future__ import annotations

from typing import Any

from apps.cases.models import (
    CaseClarity,
    CaseEffort,
    CaseEnergy,
    CaseStatus,
    CaseWorkType,
)
from apps.execution.models import ExecutionState
from apps.focus.models import FocusRole
from apps.inbox.models import InboxItemState, InboxSourceType
from apps.sources.models import SourceProvider

DEMO_EMAIL = "demo@casedock.local"
DEMO_PASSWORD = "demo-pass-123"
DEMO_TITLE_PREFIX = "Demo:"
DEMO_SLUG_PREFIX = "demo-"

DEMO_CASES: list[dict[str, Any]] = [
    {
        "key": "auth-stability",
        "title": "Demo: Stabilize email sign-in",
        "summary": ("Tighten the email sign-in path so recovery after interruption stays easy."),
        "status": CaseStatus.ACTIVE,
        "clarity": CaseClarity.CLEAR,
        "work_type": CaseWorkType.DEBUG,
        "effort": CaseEffort.MEDIUM,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "Reproduce the stale session edge case with a short checklist.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "Users can sign in, but the recovery path is brittle after a stale tab.",
                "",
                "# Desired outcome",
                "Make sign-in predictable without adding more ceremony to the v1 flow.",
                "",
                "# Constraints",
                "- Keep the first version email-first",
                "- Do not add a second auth surface",
                "",
                "# Notes",
                "- The issue is small enough to stay inside the monolith",
            ]
        ),
        "decisions": [
            {
                "body": "Keep email magic-link language out of the UI until the flow exists.",
                "promoted": True,
                "title": "Avoid naming an auth flow we have not shipped",
                "tag": "product",
                "rationale": "Users should not infer a capability from placeholder copy.",
                "alternatives": "Mention future auth options in helper text.",
                "consequence": "The sign-in surface stays narrower and calmer.",
            },
            {
                "body": "Log the stale-tab path before touching session storage code.",
                "tag": "debug",
            },
        ],
        "execution_items": [
            {
                "title": "Capture the stale-tab reproduction steps",
                "section": "debug",
                "state": ExecutionState.DOING,
                "order": 1,
                "note": "Keep the path short enough to rerun after each tweak.",
            },
            {
                "title": "Verify flash-message behavior after re-auth",
                "section": "ui",
                "state": ExecutionState.TODO,
                "order": 2,
                "note": "The calm tone should survive the redirect path.",
            },
            {
                "title": "Write a regression test for the failing branch",
                "section": "tests",
                "state": ExecutionState.DONE,
                "order": 3,
                "note": "The first failing expectation already exists in notes.",
            },
        ],
        "private_notes": [
            {
                "body": (
                    "Do not over-engineer the auth fix. A calmer edge-case flow matters "
                    "more than a grand auth abstraction."
                )
            },
            {
                "body": "If the session logic sprawls, stop and collapse the scope again.",
            },
        ],
        "source_links": [
            {
                "provider": SourceProvider.CLICKUP,
                "external_id": "CU-DEMO-101",
                "external_url": "https://app.clickup.com/t/CU-DEMO-101",
                "external_title_snapshot": "Stabilize email sign-in",
                "external_status_snapshot": "In progress",
                "payload_snapshot": {"list": "Core product", "priority": "high"},
            }
        ],
    },
    {
        "key": "onboarding-empty-state",
        "title": "Demo: Shape onboarding empty state",
        "summary": "Make the first-load board feel calm instead of barren.",
        "status": CaseStatus.ACTIVE,
        "clarity": CaseClarity.FUZZY,
        "work_type": CaseWorkType.BUILD,
        "effort": CaseEffort.DEEP,
        "energy": CaseEnergy.DEEP,
        "next_step": "Pick the first two empty-state sentences and remove the rest.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "The empty state should feel like breathing room, not a dead product.",
                "",
                "# Problem",
                "Current placeholders explain too much before the user starts.",
                "",
                "# Implementation idea",
                "- Use one sentence for orientation",
                "- Use one sentence for the next move",
                "- Keep the visual surface spare",
            ]
        ),
        "decisions": [
            {
                "body": "Keep empty states text-first and resist decorative illustrations.",
                "promoted": True,
                "title": "Empty states stay quiet in v1",
                "tag": "ux",
                "rationale": "The product should lower pressure, not demand attention.",
                "alternatives": "A more visually expressive first-run board.",
                "consequence": "Typography carries more of the experience.",
            }
        ],
        "execution_items": [
            {
                "title": "Trim the board empty-state copy",
                "section": "copy",
                "state": ExecutionState.DOING,
                "order": 1,
                "note": "Leave room for the user's own work to become the main signal.",
            },
            {
                "title": "Audit empty states across Inbox and Focus",
                "section": "ui",
                "state": ExecutionState.TODO,
                "order": 2,
                "note": "The tone should stay calm on every screen.",
            },
        ],
        "private_notes": [
            {"body": ("Need to avoid fake optimism in the empty state. Calm beats cheerful.")}
        ],
        "source_links": [
            {
                "provider": SourceProvider.URL,
                "external_url": "https://example.com/notes/onboarding-empty-state",
                "external_title_snapshot": "Onboarding notes",
                "payload_snapshot": {"kind": "research-note"},
            }
        ],
    },
    {
        "key": "inbox-case-walkthrough",
        "title": "Demo: Write inbox-to-case walkthrough",
        "summary": "Document the narrow path from capture to a finishable Case.",
        "status": CaseStatus.ACTIVE,
        "clarity": CaseClarity.CLEAR,
        "work_type": CaseWorkType.RESEARCH,
        "effort": CaseEffort.QUICK,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "Draft the three-step walkthrough directly inside the Case spec.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "Users need one visible example of how Inbox becomes structured work.",
                "",
                "# Desired outcome",
                "A short walkthrough that can be mirrored later in docs or product copy.",
                "",
                "# Notes",
                "- Keep it grounded in current UI labels",
                "- Do not imply background AI automation",
            ]
        ),
        "decisions": [
            {
                "body": "Anchor the walkthrough in existing screen labels only.",
                "tag": "docs",
            }
        ],
        "execution_items": [
            {
                "title": "List the exact transition points from Inbox to Case",
                "section": "outline",
                "state": ExecutionState.TODO,
                "order": 1,
                "note": "Capture, decide, convert, then work from the Case page.",
            }
        ],
        "private_notes": [
            {"body": "This will double as demo content when showing the app locally."}
        ],
        "source_links": [],
    },
    {
        "key": "billing-edge-cases",
        "title": "Demo: Review billing edge cases",
        "summary": "Collect the rough billing concerns before they turn into noise.",
        "status": CaseStatus.ACTIVE,
        "clarity": CaseClarity.FUZZY,
        "work_type": CaseWorkType.ADMIN,
        "effort": CaseEffort.MEDIUM,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "Sort edge cases into now, later, and ignore.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "Billing questions are small individually but costly when scattered.",
                "",
                "# Questions",
                "- Which concerns actually block launch?",
                "- Which ones only need an answer later?",
            ]
        ),
        "decisions": [],
        "execution_items": [
            {
                "title": "Collect all rough billing notes into one list",
                "section": "triage",
                "state": ExecutionState.TODO,
                "order": 1,
                "note": "",
            }
        ],
        "private_notes": [],
        "source_links": [],
    },
    {
        "key": "clickup-mapping",
        "title": "Demo: Wait for ClickUp field mapping",
        "summary": "Keep the integration visible without letting it dominate the app.",
        "status": CaseStatus.WAITING,
        "clarity": CaseClarity.CLEAR,
        "work_type": CaseWorkType.RESEARCH,
        "effort": CaseEffort.MEDIUM,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "Review the connector field inventory once the sample export lands.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "The first ClickUp sync needs a minimal mapping, not a broad import layer.",
                "",
                "# Waiting on",
                "- A sample export with custom fields",
                "- Confirmation of which states matter in v1",
            ]
        ),
        "decisions": [
            {
                "body": "Treat ClickUp as optional input, not the center of the model.",
                "promoted": True,
                "title": "ClickUp remains a feeder system in v1",
                "tag": "integration",
                "rationale": "The Case must stay understandable even without sync access.",
                "alternatives": "Leaning more heavily on mirrored ClickUp state.",
                "consequence": "Imports can stay thinner and easier to reason about.",
            }
        ],
        "execution_items": [
            {
                "title": "Compare the sample export to SourceLink fields",
                "section": "integration",
                "state": ExecutionState.TODO,
                "order": 1,
                "note": "Only map what the product can actually surface in v1.",
            }
        ],
        "private_notes": [{"body": "Avoid sync ambitions creeping into the core Case workflow."}],
        "source_links": [
            {
                "provider": SourceProvider.CLICKUP,
                "external_id": "CU-DEMO-204",
                "external_url": "https://app.clickup.com/t/CU-DEMO-204",
                "external_title_snapshot": "Field mapping sample",
                "external_status_snapshot": "Waiting",
                "payload_snapshot": {"space": "Integrations"},
            }
        ],
    },
    {
        "key": "hosting-follow-up",
        "title": "Demo: Follow up on PostgreSQL hosting decision",
        "summary": "Keep infrastructure choice present without turning it into dashboard noise.",
        "status": CaseStatus.WAITING,
        "clarity": CaseClarity.FUZZY,
        "work_type": CaseWorkType.ADMIN,
        "effort": CaseEffort.QUICK,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "Wait for the final monthly cost comparison before locking the host.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "Hosting is still narrow enough to stay as a small decision record.",
                "",
                "# Desired outcome",
                "Choose the smallest reliable hosting setup that fits v1.",
            ]
        ),
        "decisions": [],
        "execution_items": [
            {
                "title": "Keep the cost comparison in one note",
                "section": "ops",
                "state": ExecutionState.TODO,
                "order": 1,
                "note": "No sprawling procurement workflow.",
            }
        ],
        "private_notes": [],
        "source_links": [
            {
                "provider": SourceProvider.URL,
                "external_url": "https://example.com/hosting/postgres-comparison",
                "external_title_snapshot": "PostgreSQL hosting comparison",
                "payload_snapshot": {"kind": "comparison"},
            }
        ],
    },
    {
        "key": "import-parser-spike",
        "title": "Demo: Archive spike notes for import parser",
        "summary": "The parser spike is done; keep the conclusion close and the noise out.",
        "status": CaseStatus.DONE,
        "clarity": CaseClarity.CLEAR,
        "work_type": CaseWorkType.DEBUG,
        "effort": CaseEffort.MEDIUM,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "No next step. Reopen only if the import shape changes again.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "The parser spike answered the immediate questions about source payload shape.",
                "",
                "# Outcome",
                "We know which fields should stay on SourceLink and which should not.",
            ]
        ),
        "decisions": [
            {
                "body": "Do not store the whole upstream task body on the Case by default.",
                "tag": "data-shape",
            }
        ],
        "execution_items": [
            {
                "title": "Summarize the spike outcome",
                "section": "wrap-up",
                "state": ExecutionState.DONE,
                "order": 1,
                "note": "Keep the conclusion recoverable later.",
            }
        ],
        "private_notes": [],
        "source_links": [],
    },
    {
        "key": "keyboard-shortcuts",
        "title": "Demo: Document keyboard capture shortcuts",
        "summary": "Close the loop on fast capture without growing a large help center.",
        "status": CaseStatus.DONE,
        "clarity": CaseClarity.CLEAR,
        "work_type": CaseWorkType.REPLY,
        "effort": CaseEffort.QUICK,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "No next step. Reopen if the capture flow changes materially.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "Quick capture only matters if it can be explained in one breath.",
                "",
                "# Outcome",
                "The first set of capture hints is now consistent with the current UI.",
            ]
        ),
        "decisions": [],
        "execution_items": [
            {
                "title": "Publish the short shortcut hint",
                "section": "docs",
                "state": ExecutionState.DONE,
                "order": 1,
                "note": "",
            }
        ],
        "private_notes": [],
        "source_links": [],
    },
    {
        "key": "display-mode-polish",
        "title": "Demo: Close loop on calm display mode polish",
        "summary": "Finish the smallest calm/compact polish items and stop there.",
        "status": CaseStatus.DONE,
        "clarity": CaseClarity.FUZZY,
        "work_type": CaseWorkType.BUILD,
        "effort": CaseEffort.QUICK,
        "energy": CaseEnergy.SHALLOW,
        "next_step": "No next step. The current pass is intentionally complete enough.",
        "spec_markdown": "\n".join(
            [
                "# Context",
                "Display mode is valuable only if it stays simple and low-maintenance.",
                "",
                "# Outcome",
                "Compact mode now preserves hierarchy without drifting into density.",
            ]
        ),
        "decisions": [
            {
                "body": "Limit display modes to Calm and Compact in v1.",
                "promoted": True,
                "title": "Keep display mode vocabulary intentionally narrow",
                "tag": "ux",
                "rationale": "More modes add preference overhead without real leverage.",
                "alternatives": "Add several density presets.",
                "consequence": "The UI remains easier to reason about and test.",
            }
        ],
        "execution_items": [
            {
                "title": "Ship the last compact spacing tweak",
                "section": "ui",
                "state": ExecutionState.DONE,
                "order": 1,
                "note": "",
            }
        ],
        "private_notes": [],
        "source_links": [],
    },
]

DEMO_INBOX_ITEMS: list[dict[str, Any]] = [
    {
        "title": "Demo: Reply to vendor about DNS transfer",
        "source_type": InboxSourceType.MANUAL,
        "raw_body": (
            "Short reply needed. Confirm the transfer window and whether downtime is "
            "expected during the switch."
        ),
        "triage_state": InboxItemState.DOING_NOW,
        "source_url": "",
        "completion_note": "",
    },
    {
        "title": "Demo: Investigate flaky sync screenshot",
        "source_type": InboxSourceType.URL,
        "raw_body": "A screenshot suggests the sync status badge got stuck after refresh.",
        "triage_state": InboxItemState.NEW,
        "source_url": "https://example.com/support/flaky-sync-screenshot",
        "completion_note": "",
    },
    {
        "title": "Demo: Parking-lot idea for git activity heatmap",
        "source_type": InboxSourceType.NOTE,
        "raw_body": (
            "Interesting, but probably too dashboard-like for v1. Keep it parked until "
            "the core workflow is clearly stronger."
        ),
        "triage_state": InboxItemState.PARKED,
        "source_url": "",
        "completion_note": "",
    },
    {
        "title": "Demo: Waiting for user quote on landing copy",
        "source_type": InboxSourceType.OTHER,
        "raw_body": "Need the exact wording before touching the calm/productive tension.",
        "triage_state": InboxItemState.WAITING,
        "source_url": "",
        "completion_note": "",
    },
    {
        "title": "Demo: Rough note about AI prompt guardrails",
        "source_type": InboxSourceType.NOTE,
        "raw_body": (
            "Need a tighter boundary statement: AI can draft, summarize, and suggest, "
            "but it should never silently move work."
        ),
        "triage_state": InboxItemState.NEW,
        "source_url": "",
        "completion_note": "",
    },
    {
        "title": "Demo: Convert ClickUp mapping thought into a Case",
        "source_type": InboxSourceType.CLICKUP,
        "raw_body": "Imported from ClickUp when the field-mapping question first surfaced.",
        "triage_state": InboxItemState.CONVERTED,
        "source_url": "https://app.clickup.com/t/CU-DEMO-204",
        "completion_note": "",
        "converted_case_key": "clickup-mapping",
    },
    {
        "title": "Demo: Turn hosting note into a tracked Case",
        "source_type": InboxSourceType.URL,
        "raw_body": "The hosting question needed somewhere calmer than a browser tab pile.",
        "triage_state": InboxItemState.CONVERTED,
        "source_url": "https://example.com/hosting/postgres-comparison",
        "completion_note": "",
        "converted_case_key": "hosting-follow-up",
    },
    {
        "title": "Demo: Restart local worker after env update",
        "source_type": InboxSourceType.MANUAL,
        "raw_body": "Tiny maintenance task. No Case needed.",
        "triage_state": InboxItemState.DONE,
        "source_url": "",
        "completion_note": "Worker restarted and queue recovered.",
    },
    {
        "title": "Demo: Send contract PDF to accountant",
        "source_type": InboxSourceType.MANUAL,
        "raw_body": "One-off admin follow-up handled directly from Inbox.",
        "triage_state": InboxItemState.DONE,
        "source_url": "",
        "completion_note": "Sent from the archive and confirmed receipt.",
    },
]

DEMO_FOCUS_KEYS = {
    FocusRole.MAIN: "auth-stability",
    "secondary_1": "onboarding-empty-state",
    "secondary_2": "inbox-case-walkthrough",
}
