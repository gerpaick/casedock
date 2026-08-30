# stage-runner — casedock

Adapted from the `stage-runner` pattern used in an earlier solo project to fit casedock's existing `docs/plan/` structure. This is **the** workflow rule for sequencing implementation work.

## When to activate

- User says: "continue," "what next," "what's next," "resume," "start work," or "active stage"
- At the start of any session that will implement code
- Before marking any task `[x]` in `tasks.md`
- Before opening a new spec / feature work

## Workflow

### Step 1 — Read state (parallel)

- `docs/plan/tasks.md` — the active task tracker
- `docs/plan/current_stage.md` — snapshot of current work
- `docs/plan/00-master-implementation-plan.md` — stage dependencies (relevant section only)

### Step 2 — Find the active stage

The active stage is the **first** `## Stage N` section in `tasks.md` that has at least one `[ ]` task. Stages above it must be fully `[x]`.

Special case: **Stage 8 is parallel-safe with Stages 9–10.** This is the only exception to the strict "one stage at a time" rule. Stage 8 quality-bar tasks may be picked up alongside Stage 9/10 work, but Stage 9 must be `[x]` before Stage 10, etc.

If every stage has every task `[x]`: report „Board complete. Waiting for new spec." and stop.

### Step 3 — Verify dependencies

Check the `Depends on:` line of the active stage. Every listed stage must be `[x]` (or explicitly marked parallel-safe). If not, stop and report: „Stage N depends on Stage M which has open tasks. Cannot proceed."

### Step 4 — Present the active stage to the user

Format:

```
## Active Stage: Stage N — <name>

Depends on: <stage IDs or None>
Source: <which ADR / spec drives this stage>

Open tasks:
- [ ] <task 1>
- [ ] <task 2>

Acceptance: <from the stage section>

Relevant quality checks: <which of pytest / ruff / mypy / build:css hit the affected modules>

Current focus: <which task to start with>
```

### Step 5 — Pick the next task

Within the active stage, the next task is the first `[ ]` in document order, unless:
- A task explicitly depends on another task within the same stage that is still `[ ]` — surface that dependency.
- The user names a different task — respect the explicit choice.

### Step 6 — Implement

Hand off to implementation (Sisyphus orchestration + `task()` delegation to `deep` / `unspecified-high` / `quick` categories as appropriate). Load skills: `sdd-workflow` for new modules, `django-htmx-patterns` for template/HTMX work, `qa-full` before stage completion.

When a task completes:
1. Flip `[ ]` → `[x]` in `tasks.md` using `edit` with `replaceAll=false` to flip exactly one checkbox.
2. Run the relevant `qa-full` subset:
   - Single Python file change → focused pytest + `ruff check .`
   - Template / HTMX change → focused pytest + `ruff check .` + manual smoke
   - Settings / migration change → full `qa-full` (pytest + ruff + ruff format + mypy + build:css if touched)
3. Update `current_stage.md` "Currently in flight" / "Next task" sections.

### Step 7 — Stage completion

When every task in the active stage is `[x]`:
1. Run **full** `qa-full`:
   ```
   uv run pytest
   uv run ruff check .
   uv run ruff format --check .
   uv run python -m mypy src/
   ```
   (plus `npm run build:css` if any CSS touched)
2. If everything passes:
   - Update `current_stage.md` "Active stage" to the next stage.
   - Update `current_stage.md` "Last 3 sessions" with the stage completion.
   - Add a one-liner to `progress.md` Done section.
   - Stop. Summarise what was done. Wait for user review.
3. If anything fails: do NOT unlock the next stage. Fix or report.

## Forbidden behaviours

- Starting Stage N+1 before Stage N is `[x]` and `qa-full` passes (except Stage 8 parallel-safe rule).
- Marking `[x]` without running the relevant tests.
- Working on two non-parallel-safe stages in parallel.
- Editing `docs/plan/stages/01-08` — those files are frozen reference. New work goes in `tasks.md`.
- Auto-starting the next stage without user review.
- Writing new strategic docs without a paired task in `tasks.md` („planning is dopamine").

## Sync rule

Every time a task is marked `[x]`, also update `current_stage.md` so the next session resumes cleanly. This is non-negotiable — context loss between sessions is the primary failure mode for solo ADHD-friendly development.

## ADHD principle check (before accepting any task as `[x]`)

For tasks that touch UX, run the 5 verification questions from `docs/decisions/2026-06-09-adhd-design-principles.md`:

1. Does this ADD decisions or REMOVE them? → Remove wins.
2. Could this trigger shame or avoidance? → Red badges, overdue indicators, streak breaks are forbidden.
3. Does this rely on user remembering to check? → Auto-surface instead.
4. Is the first thing a user sees an ACTION or just INFORMATION? → Action wins.
5. Would an ADHD user abandon this after 3 weeks? → Less maintenance = better.

If any answer is wrong, the task is not `[x]` — fix or escalate.

## Parked / superseded work

If the user references work that was deferred (e.g. ClickUp connector pre-2026-07-17 plan):
1. Refuse to start work directly.
2. Cite the ADR that deferred it.
3. Offer to help re-spec it in `docs/specs/` first, if the deferral decision is being revisited.

## File map

| File | Role |
|---|---|
| `docs/plan/tasks.md` | Active tracker — single source of truth for what's done / next |
| `docs/plan/current_stage.md` | Snapshot — read first every session |
| `docs/plan/stage-runner.md` | This file — workflow rules |
| `docs/plan/00-master-implementation-plan.md` | Original stage dependencies (frozen reference) |
| `docs/plan/stages/01-08` | Original stage definitions (frozen reference) |
| `docs/plan/progress.md` | Historical Done log + Tailwind migration history |
