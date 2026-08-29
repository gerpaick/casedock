# casedock

Calm workbench for solo technical builders.

casedock is a personal execution layer for overloaded developers. Incoming work lands in one inbox, gets triaged once, and either becomes a structured **Case** — with its spec, decisions, private notes, source links, and execution state in one place — or is parked without noise. A daily focus keeps the day down to a small, visible set.

It is not another task manager. It optimizes for one thing: **knowing exactly what to do next without reloading the whole project into your head.**

## The core loop

1. **Capture** — one field, zero required fields. Global `c` shortcut from any page.
2. **Triage** — every item gets decided once: *do now / convert to Case / set aside / waiting / archive*. Decided items leave your head.
3. **Case** — a bounded working object: spec, decisions, execution items, private notes, source links. Understandable in isolation, weeks later.
4. **Focus** — 1 main + 2 secondary per day. The board surfaces the first unchecked execution item as the "just start" prompt.

## Design principles

casedock is ADHD-informed by design — evidence-based, not gamified:

- Remove decisions instead of adding them; the first thing you see is an action, not information
- No red badges, overdue indicators, or streaks — stale work is marked neutrally
- No time estimation, no gamification, no "you haven't logged in" nags
- The board never shows more than ~7–10 active cases without folding

The full 15-point decision record lives in [`docs/decisions/2026-06-09-adhd-design-principles.md`](docs/decisions/2026-06-09-adhd-design-principles.md), backed by research in [`docs/research/`](docs/research/).

## Stack

- **Python 3.13**, type-hint first (mypy strict)
- **Django 6** — modular monolith, server-rendered templates
- **HTMX** + vanilla JS — no SPA framework, no client-side routing
- **Tailwind CSS v4** — tokens in `static/ui/input.css`
- **PostgreSQL** (prod) / **SQLite** (local dev)
- **pytest**, **ruff**, **mypy** — the quality gate

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and Node (for CSS build).

```bash
uv sync
uv run manage.py migrate
npm install && npm run build:css
uv run manage.py runserver
```

Optional — populate a demo workspace (Board, Inbox, Focus, Cases):

```bash
uv run manage.py seed_demo
```

## Quality gate

```bash
uv run pytest                  # 166 tests
uv run ruff check .
uv run ruff format --check .
uv run python -m mypy src/
```

## Project layout

```
src/
  config/             Django settings, URLs
  apps/
    core/             User model, base models
    inbox/            Capture and triage
    cases/            Case workspace
    decisions/        Decision model (managed through cases views)
    execution/        ExecutionItem model
    focus/            Daily focus: 1 main + 2 secondary
    sources/          SourceLink model
    ui/               Board, search, settings
    clickup/, ai/     Intentional stubs — see docs/decisions/
templates/            Django templates per app
tests/                pytest suite (not inside apps)
static/ui/            Tailwind source + compiled CSS
docs/                 Specs, plan, decisions, ADHD research
```

## Documentation

- [`docs/specs/`](docs/specs/) — product and architecture specification (the contract)
- [`docs/plan/`](docs/plan/) — implementation plan and stage tracker
- [`docs/decisions/`](docs/decisions/) — decision records
- [`docs/research/`](docs/research/) — ADHD and neurodiversity research with sources

## Status

Work in progress, single-user. Current stage: **Stage 8 — quality bar & hardening**. The active-stage snapshot lives in [`docs/plan/current_stage.md`](docs/plan/current_stage.md); the full task tracker is [`docs/plan/tasks.md`](docs/plan/tasks.md).

ClickUp integration and AI features are intentional stubs — nothing ships until the core loop is right.

## License

[Apache-2.0](LICENSE)
