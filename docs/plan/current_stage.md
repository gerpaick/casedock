# Current Stage — snapshot

> This file is the **resume point** for any new session. Read first, every time.
> Last updated: 2026-07-28

## Active stage

**Stage 8 — Quality bar & hardening** (in progress, parallel-safe)

**Why Stage 8 first and not Stage 9:** Stage 9 (Just Start) is the highest-leverage work, but `8.1` (empty-state audit) and `8.2` (error-handling audit) are prerequisites — Stage 9 adds new empty states and HTMX flows, so the audit must exist first to avoid multiplying unreviewed surface.

If the user wants to start with the ADHD-critical work immediately, swap to Stage 9 and treat 8.1/8.2 as in-line reviews during 9.x tasks. Either ordering is defensible — pick one explicitly.

## Recently shipped (off-stage, 2026-07-28)

- **Inbox cleanup**: removed dead fields (`raw_metadata_snapshot`, `source_reference`); migration `0005_remove_unused_source_fields`. Added Archive as 6th triage action (`action_to_state["archive"]`, buttons in detail + focus panel, validator relaxed to preserve `converted_case` through archive).
- **Global `c` capture shortcut**: modal opens from any authenticated page (new `_global_quick_capture.html` partial in `base.html`, new context processor, JS handler in `app.js` extends existing keydown listener). Resolves open question in `docs/decisions/2026-05-09-clickup-focus-flow-design-review.md` L413. ADR: `docs/decisions/2026-07-28-global-capture-shortcut.md`.
- Tests: 154 → 161 passing. ruff + mypy clean.

## Recently shipped (off-stage, 2026-07-30)

- **Stage 10 partial — Trust pages**: `/help/`, `/privacy/`, `/terms/` now resolve (footer was a 404 since early stages). Three `TemplateView` routes in `apps/core/urls.py`, three templates in `templates/core/`, all anonymous-accessible and eyebrow-marked `Draft`. Footer links switched to `{% url %}` (dead links structurally impossible). `TestTrustPages` in `tests/test_smoke.py` covers anon + auth + footer resolution. Tests: 161 → 166. ADR: `docs/decisions/2026-07-30-help-privacy-terms-basic-version.md`. Stage 10.1–10.4 stay `[ ]` — full FAQ / EU-legal review / production emails pending.

## Currently in flight

- **Nothing.** Stage 8 has no `[x]` tasks yet — the quality-bar work since 2026-07 has been ad-hoc (multi-user migration, signup, isolation tests, inbox cleanup, capture shortcut) and is captured as cross-cutting work under Stage 1–7 historical + Recently shipped section above, not under Stage 8.

## Next task to pick up

Recommended: **`8.1 Empty-state audit`** — list every empty state in Board / Inbox / Focus / Case, verify each offers ONE next action per ADHD principle #4. Output: `docs/plan/empty-state-audit.md` with one row per empty state and a verdict (action / info-only / broken).

Alternative (if user prefers the ADHD hook first): **`9.1 Just-start prompt on Board`** — surface the first unchecked ExecutionItem of the focused Case as a single suggested action. 9.1 unblocks 9.2–9.9 and is the single most-cited research finding in `docs/research/`.

## Blocked / parked

- Stage 7 stubs (`clickup`, `ai`): intentional. Per ADR 2026-07-17, the ClickUp connector is
  deferred indefinitely (MCP direction 2 may subsume it), and `ai` becomes Stage 12 (MCP server).
- All further strategic-doc writing without a paired feature: forbidden — „planning is dopamine".

## Session checklist

Before ending any session that touched tasks.md or current_stage.md:

- [ ] Flip exactly one `[ ]` → `[x]` per task completed in `tasks.md`
- [ ] Run the relevant `qa-full` subset (full suite if Stage completed)
- [ ] Update this file's "Active stage" / "Currently in flight" / "Next task" sections
- [ ] One-line entry in `progress.md` Done section

## Last 3 sessions (high level)

- 2026-07-11 — Multi-user + public_id migration, 5 phases, 15 isolation tests
- 2026-07-17 — Strategic review session, ADR drafted (AI agent pressure + MCP direction)
- 2026-07-28 — Stage-runner setup; Inbox cleanup (P0 dead fields + Archive action + validator fix); global `c` capture shortcut
