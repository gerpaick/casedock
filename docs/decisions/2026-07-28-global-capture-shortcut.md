# Global `c` Capture Shortcut

Date: 2026-07-28

## Context

Quick capture previously only existed on `/inbox/`. From anywhere else in casedock (Board, Focus, a Case workspace), capturing a thought meant navigating away from the page the user was working in. That round-trip is exactly the kind of friction the ADHD 3-Second Rule warns against: if capture takes longer than three seconds, the thought is likely to be lost (`docs/research/2026-06-adhd-reddit-community-insights.md`, Theme 6 — "Capture First, Organize Later", and the 3-Second Rule in the same file).

This resolves an open question left in `docs/decisions/2026-05-09-clickup-focus-flow-design-review.md` (L413): _"Should there be a global quick-capture shortcut available from any page?"_ — answer: yes, with a single-key shortcut.

## Decision

- Pressing `c` alone (no modifiers, not while typing, no dialog already open) opens a capture modal from any authenticated page.
- On `/inbox/`, `c` opens the existing `#capture-modal` so the Inbox HTMX flow (auto-clear-on-swap, focus return, queue ordering) stays intact.
- On any other authenticated page, `c` opens a new `#global-capture-modal` rendered in `templates/ui/base.html`. That modal uses the same `_capture_form.html` with `capture_origin="page"` — a plain POST that already exists. On success the server redirects to `/inbox/`; on validation error it redirects to `/inbox/capture/new/` so the user sees the standalone form with errors in place.
- If neither modal is present in the DOM (e.g. a minimal error page), `c` falls back to navigating to `/inbox/capture/new/`.
- The shortcuts help modal lists `c` → "Capture inbox item (works anywhere)".

## Alternatives considered

- **`Ctrl/Cmd+/` then `c` (two-step)** — rejected. Two-step chords are undiscoverable and slower, which is the opposite of what the 3-Second Rule demands. The shortcuts panel is a reference, not a gate.
- **`Shift+C` chord** — rejected. Slower than a single key and easier to fumble. Gmail, Todoist, and Linear all use bare `c`; matching that prior art reduces learning cost.
- **Lift the Inbox modal into `base.html`** — rejected. The Inbox modal relies on HTMX swapping `#inbox-page` after each capture, which auto-clears the form and preserves the current focus selection. A globally included Inbox modal would either break that swap behavior or duplicate the form logic. Keeping two modals (one HTMX, one plain POST) preserves each flow's invariants.

## Why

This keeps casedock aligned with its core capture principles:

- capture is the front door, not a side feature
- one key, no decisions, no modifiers to remember
- the Inbox HTMX flow is preserved exactly — no regression on the calm triage surface
- the fallback path keeps the contract honest: capture never silently fails

## Status

Implemented.

## Follow-up

When Stage 12 MCP lands the `capture_inbox_item` tool, the global modal becomes the human-side mirror of the programmatic capture path — both funnel into the same plain-POST endpoint with `capture_origin="page"`. The keyboard shortcut and the MCP tool should be treated as one capture contract viewed from two surfaces.
