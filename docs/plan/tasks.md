# casedock Tasks — Stage Tracker

Single source of truth for **what's done, what's next, what's blocked**.

Read together with:
- `docs/plan/00-master-implementation-plan.md` — stage dependencies and milestones
- `docs/plan/stages/01-08` — original stage definitions (frozen reference)
- `docs/plan/current_stage.md` — snapshot of active stage (auto-synced)
- `docs/plan/stage-runner.md` — workflow rules for this file
- `docs/decisions/2026-07-17-ai-agent-pressure-and-mcp-direction.md` — rationale for Stages 9–12 priority

## Rules

1. **One stage at a time.** Stage N+1 cannot start until Stage N is `[x]` and the relevant quality checks pass.
2. **Checkboxes are sacred.** Flip `[ ]` → `[x]` only after the task is verifiably done (tests pass, lint clean, artifact on disk).
3. **Stages 1–7 are historical.** Implementation is locked. Listed here for traceability only — see `stages/01-08` for original definitions.
4. **Stages 9–12 supersede Stage 8's original scope.** Stage 8's quality-bar work continues, but the priority order is driven by the 2026-07-17 ADR, not the original hardening list.
5. **Add tasks, don't delete.** If scope changes, mark cancelled `[~]` with a note, do not erase history.
6. **Every completed task leaves an artifact** (code + test, doc update, or ADR entry). No silent `[x]`.

## Legend

- `[ ]` — open
- `[x]` — done, verifiably
- `[~]` — cancelled / superseded (note why)
- `[!]` — blocked (note blocker)

---

## Stage 1–7 — historical (DONE)

| Stage | Name | Status |
|---|---|---|
| 1 | Foundation and project bootstrap | [x] |
| 2 | Core domain model | [x] |
| 3 | Inbox and triage | [x] |
| 4 | Case workspace | [x] |
| 5 | Decisions and execution | [x] |
| 6 | Board, focus, and search | [x] |
| 7 | Sources, clickup, ai boundaries (clickup + ai left as intentional stubs per ADR 2026-07-17) | [x] |

Cross-cutting work that landed between Stage 7 and 2026-07:
- [x] Auth views (login/logout/password-reset) — 25 tests
- [x] Tailwind v4 migration — input.css + tokens, 5 sessions, app.css removed
- [x] Board focus-centric redesign — stale detection, active/waiting views
- [x] Multi-user + public_id — 5-phase migration complete, 15 isolation tests
- [x] SignupView + form + template + tests
- [x] mypy strict 0 errors, ruff clean, 154/154 tests

---

## Stage 8 — Quality bar & hardening (IN PROGRESS, partial)

Depends on: Stages 1–7 (DONE)
Original spec: `docs/plan/stages/08-hardening-and-release-readiness.md`
Continuing scope: tests, type safety, empty-state polish, error handling. The 2026-07 review split the remaining work — the ADHD-impacting pieces moved to Stage 9, the legal/trust pieces to Stage 10. What remains here is the quality bar proper.

Open tasks:
- [ ] 8.1 Empty-state audit across Board / Inbox / Focus / Case — every empty state offers ONE next action (ADHD principle #4: action wins over information)
- [ ] 8.2 Error-handling audit — 500 pages, form errors, HTMX failure paths render calm copy, not stack traces
- [ ] 8.3 Smoke test for `curl -I` on every public route (anon + auth) — zero unhandled 500s
- [ ] 8.4 Final documentation review: `docs/specs/` vs implementation, conflicts resolved in docs first
- [ ] 8.5 Release-gate checklist written to `docs/plan/release-gates.md`

Stage 8 is parallel-safe: tasks 8.1–8.4 may run alongside Stages 9–10. Stage 8 must be `[x]` before Stage 12 (MCP) starts, because MCP exposes whatever quality bar exists.

Acceptance:
- 5 tasks above `[x]`
- `uv run pytest` green
- `uv run ruff check .` + `uv run ruff format --check .` green
- `uv run python -m mypy src/` 0 errors
- No new `# type: ignore` / `Any` / bare `except`

---

## Stage 9 — Just Start + First-Run Experience (NOT STARTED, P0)

Depends on: Stage 8 in progress (8.1 + 8.2 recommended first)
Source: ADR 2026-07-17 (ADHD principle #1 "show ONE next action" is top research finding, currently *not implemented*).

This stage delivers the single highest-leverage ADHD principle that casedock currently violates. Per the ADR: "Without this, casedock is a context archive, not a resume engine."

Open tasks:
- [ ] 9.1 Board surfaces first unchecked ExecutionItem of the focused Case as a single "Just start" prompt (replaces or augments current focus hero)
- [ ] 9.2 `is_first_visit` flag in `HomeView` / `BoardView` (session-key check) — first-time user sees a guided flow, not an empty board
- [ ] 9.3 `_first_run.html` template — 3 steps: capture InboxItem → convert to Case → set Focus. All inline, no full-page reloads (HTMX)
- [ ] 9.4 Pre-seed 2 demo InboxItems + 1 demo Case per new user on signup (scoped to user, clearly marked "Example", deletable in one click)
- [ ] 9.5 After first Focus setup → redirect to full Board with stale detection acked for demo data
- [ ] 9.6 Welcome email via Resend (already configured) — one short email: "Your first Case is waiting. Open casedock." No marketing, no images
- [ ] 9.7 Focus hero on Board shows the *next action inside the focused Case* — not just the Case title
- [ ] 9.8 Stale-ack UX rework: acking stale must feel like parking, not like guilt (no red, no "overdue", neutral grey)
- [ ] 9.9 Tests: first-visit flow, demo data isolation per user, welcome email mock, just-start prompt visibility, stale-ack copy

Acceptance:
- A brand-new signup reaches their first Case in **<5 minutes** (verifiable by manual click-through or test)
- Board first paint shows ONE suggested action, not a list

Out of scope for Stage 9:
- Reverse todo / accomplishment view (ADHD principle #8 — separate stage)
- Nightly email (separate stage)
- Analytics (not before private beta)

---

## Stage 10 — Trust Hardening (NOT STARTED, P1)

Depends on: Stage 9 started (first-run must be coherent before legal copy is added)
Source: 2026-07 review — "Wire dead links + `/help`, `/privacy`, `/terms` + minimum retention"

Trust leaks are the cheapest fixes with the highest credibility gain — dead links in the footer undermine trust immediately.

Open tasks:
- [ ] 10.1 `/help/` route + `core/help.html` — 5 FAQ (sourced from `docs/specs/03-workflows.md`), how-to-start, how-to-capture, how-to-convert-to-Case, contact `help@casedock.app`
    - _Partial landed 2026-07-30 (ADR `2026-07-30-help-privacy-terms-basic-version.md`): route + template + anon access + 4 starter sections. Still pending: full 5 FAQ, structured how-to guides, production email._
- [ ] 10.2 `/privacy/` route + `core/privacy.html` — EU-legal minimum (cookies, data stored, no third-party sharing, user-controlled deletion)
    - _Partial landed 2026-07-30: route + template + draft sections (account, hosting, tracking, deletion, beta status). Still pending: EU-legal review, hosting region/backup policy confirmation, self-serve export/delete in Settings, production email._
- [ ] 10.3 `/terms/` route + `core/terms.html` — terms of service, beta disclaimer, no-warranty clause
    - _Partial landed 2026-07-30: route + template + draft sections (beta, as-is, account, acceptable use, contact). Still pending: legal entity, jurisdiction, liability cap, production email._
- [ ] 10.4 Remove or wire every dead link in `templates/ui/base.html` (footer, nav) — no compromises
    - _Footer help/privacy/terms wired 2026-07-30 (hardcoded paths → `{% url %}`). Other dead links audited as part of 10.4 still pending._
- [ ] 10.5 Smoke test: every URL referenced in templates resolves to 200 (pytest-django client walk)
- [ ] 10.6 Footer "Built by a solo dev with ADHD" — minimal trust signal, no logos

Acceptance:
- `curl -I /help/`, `/privacy/`, `/terms/` → 200
- Zero 404s from any link rendered in the app shell

---

## Stage 11 — Public Presence (CANCELLED — out of repo scope)

~~11.1–11.9~~ `[~]` — landing page, waitlist, and content publishing were marketing/GTM work and have been moved out of this repository's scope entirely. No waitlist or landing tasks remain in the tracker.

---

## Stage 12 — MCP Server (direction 1) (NOT STARTED, P3)

Depends on: Stage 8 complete (quality bar locked) + Stage 9 complete (Just Start exists — MCP `get_next_move` exposes it)
Source: ADR 2026-07-17 §"MCP in casedock — purpose, rationale, and benefit" — direction 1 (casedock as an MCP server, with the agent reading from casedock)

Stage 12 turns the AI-agent threat into a moat (per ADR): "MCP turns the threat into a moat." The product becomes a structured source of truth that coding agents read — which makes casedock *more* valuable the more someone works with AI agents.

Open tasks:
- [ ] 12.1 `src/apps/ai/` skeleton (currently a stub) — Python MCP SDK, server bootstrap, healthcheck
- [ ] 12.2 Auth: per-user token (generated on Settings page), scope to read-mostly tools. No tokens for anonymous users.
- [ ] 12.3 Tool `get_focus` — returns today's focus slot (1 main + 2 secondary) or "no focus set today"
- [ ] 12.4 Tool `list_active_cases` — returns active Cases for the authenticated user with titles + last-updated + first unchecked ExecutionItem title
- [ ] 12.5 Tool `get_case` — full Case context: spec excerpt, last 3 decisions, first unchecked ExecutionItem, source links (no PrivateNotes unless explicitly shared)
- [ ] 12.6 Tool `get_next_move` — surfaces the same "Just start" prompt that Stage 9 added to the Board, so the agent answers "what should I do now?" from casedock, not from the model
- [ ] 12.7 Tool `capture_inbox_item` — the only write tool. Per ADR: must remain the only one. Captures into inbox for human triage.
- [ ] 12.8 Enforce read-mostly invariant in tests — no tool other than `capture_inbox_item` mutates state
- [ ] 12.9 Enforce PrivateNote isolation in tests — PrivateNotes never returned by any tool unless explicit per-Case opt-in
- [ ] 12.10 Docs: `docs/specs/10-mcp-server.md` — protocol, tools, auth model, security boundaries (becomes the new canonical reference)
- [ ] 12.11 Tests: every tool (happy path + auth fail + cross-user isolation + read-only enforcement)

Acceptance:
- All 5 tools callable from a coding agent (Claude Code, Cursor) with a casedock-issued token
- Zero state mutations outside `capture_inbox_item`
- Zero PrivateNote leaks without explicit opt-in
- Docs locked: spec is the contract, code is the implementation, no drift

Out of scope for Stage 12:
- ClickUp connector (deferred indefinitely per ADR — MCP direction 2 may subsume it)
- Jira / GitHub connectors (same)
- Autonomous sync (forbidden by ADR — must remain on-demand)

---

## Stage 13+ — not yet defined

Likely candidates based on ADHD principles not yet implemented:
- Reverse todo / accomplishment view (ADHD #8)
- Nightly email (review of yesterday + tomorrow's focus)
- Activity feed
- Weekly view

These will be specced in `docs/specs/` first, then broken into tasks here. Do not pre-populate.

---

## Done log

Most recent completed work (full history: see `progress.md` and git log).

- 2026-07-11 — Multi-user + public_id migration, 5 phases complete
- 2026-05-27 — Tailwind v4 migration, 5 sessions complete
- (earlier entries in `progress.md`)

---

## Stage dependency graph

```
1 → 2 → 3 → 4 → 5 → 6 → 7
                            \
                             → 8 (quality bar, parallel-safe with 9–10)
                              \
                               → 9 (Just Start + First-Run, P0)
                                \
                                 → 10 (Trust Hardening, P1)
                                  \
                                   → 12 (MCP Server, P3)
```

Stage 9 unlocks 10 and 12 — everything downstream depends on the core ADHD loop actually working.
