# casedock

Calm workbench for solo technical builders. Modular Django monolith.
Source of truth: [`docs/specs/`](docs/specs/) — work spec-driven-first.

## Session workflow (read first)

Before any implementation work, follow [`docs/plan/stage-runner.md`](docs/plan/stage-runner.md). Quick summary:

1. Read [`docs/plan/current_stage.md`](docs/plan/current_stage.md) — the snapshot of where you are.
2. Read [`docs/plan/tasks.md`](docs/plan/tasks.md) — the active tracker. Find the first `## Stage N` with an open `[ ]` task.
3. Pick the next `[ ]` task. Implement. Flip `[ ]` → `[x]` only after the relevant `qa-full` subset passes.
4. Update `current_stage.md` before ending the session — non-negotiable for cross-session continuity.

**One stage at a time** (exception: Stage 8 quality-bar is parallel-safe with Stages 9–10). **No new strategic docs without a paired task in `tasks.md`** — „planning is dopamine".

## Commands

```bash
uv run pytest                      # run tests (pytest-django, pythonpath=src)
uv run pytest tests/test_foo.py -k test_bar  # single test
uv run ruff check .                # lint (line-length=100, target py313)
uv run ruff check . --fix          # lint with autofix
uv run ruff format --check .       # check formatting
uv run ruff format .               # apply formatting
uv run python -m mypy src/         # type check (strict mode)
npm run build:css                  # build Tailwind: input.css → tailwind.css (minified)
npm run dev:css                    # Tailwind watch mode during dev
uv run manage.py runserver         # dev server (SQLite local)
uv run manage.py seed_demo         # populate demo data
uv run manage.py makemigrations    # create migrations
uv run manage.py migrate           # apply migrations
```

## Done

A task is done when ALL of the following pass:

1. `uv run ruff check .` — exit 0
2. `uv run ruff format --check .` — exit 0
3. `uv run python -m mypy src/` — exit 0, 0 errors
4. `uv run pytest` — exit 0, all tests pass
5. No new `# type: ignore`, `Any`, or bare `except` in changed files

If CSS changed: also run `npm run build:css` — exit 0.

## Boundaries

### Never

- Add `# type: ignore`, `Any`, or type casts without documented justification
- Suppress errors with bare `except` or empty `except:` blocks
- Delete failing tests to make the suite pass
- Commit secrets, API keys, or `.env` files
- Modify files in `static/vendor/`
- Introduce SPA architecture, frontend framework, or client-side routing
- Make AI autonomous decisions about sync, workflow, or product behavior
- Expose private notes to external systems without explicit user action

### Ask first

- Adding new dependencies (pip or npm)
- Changing database schema (modify models → ask before makemigrations)
- Modifying `docs/specs/` — these are the product contract
- Changing Tailwind design tokens in `input.css`

### Escalation

When stuck after 3 failed fix attempts:

1. STOP editing — do not try more creative workarounds
2. REVERT to last working state (`git checkout` / undo edits)
3. REPORT: what was attempted, what failed, full error output
4. WAIT for user direction

## Tech stack

- **Language**: Python 3.13, type-hint first
- **Framework**: Django 6, Django templates, HTMX
- **JS**: Vanilla JS in `static/ui/app.js` — no Alpine.js, no React
- **CSS**: Tailwind v4, source `static/ui/input.css`, compiled to `static/ui/tailwind.css`
- **DB**: PostgreSQL (prod), SQLite (local dev)
- **Queue**: Redis + Celery (configured, not heavily used yet)
- **Auth**: Email-based login (not username)
- **Linter**: ruff (check + format), configured in `pyproject.toml`
- **Types**: mypy strict, configured in `pyproject.toml`
- **Tests**: pytest + pytest-django, 154 tests

## Project layout

```
src/
  config/             Django settings, URLs, WSGI/ASGI
  apps/
    core/             User model, base models, shared utilities
    inbox/            Inbox capture, triage, conversion to Case
    cases/            Case workspace: spec, status, decisions, execution, notes
    decisions/        Decision model (managed through cases views)
    execution/        ExecutionItem model (managed through cases views)
    focus/            Daily focus: 1 main + 2 secondary
    sources/          SourceLink model for external references
    ui/               Board, search, settings, display mode, layout helpers
    clickup/          Stub — no implementation yet
    ai/               Stub — no implementation yet
templates/            Django templates per app (cases/, focus/, inbox/, ui/, registration/)
tests/                All tests — pytest, NOT inside apps
static/
  ui/                 input.css (Tailwind source), app.js, tailwind.css (compiled)
  vendor/             Third-party assets — DO NOT EDIT
  casedock/           Project-specific static files
```

### Key paths

- Inbox → Case conversion: `src/apps/inbox/services.py → convert_inbox_item_to_case()`
- Focus management: `src/apps/focus/services.py` (5 functions, transactional)
- Board context: `src/apps/ui/views.py → build_board_context()`
- Display mode: `src/apps/ui/display.py → normalize_display_mode()`
- Tailwind source: `static/ui/input.css` — design tokens in `@theme` block

## Code style

### Python

```python
# Good: type annotations on everything, Google-style docstrings on public functions
def convert_inbox_item_to_case(inbox_item: InboxItem, user: User) -> Case:
    """Convert an inbox item into a new case with initial spec."""
    ...

# Good: services layer handles business logic, views are thin
# Bad: business logic in views or templates

# Good: keep functions small, modules focused
# Bad: god objects, files over 300 lines (split them)

# Naming: snake_case everything, PascalCase for classes
# Imports: ruff isort handles ordering (I rule in pyproject.toml)
```

### Templates

- Django templates with HTMX attributes (`hx-get`, `hx-post`, `hx-swap`)
- No Alpine.js, no `x-data`, no `x-show`
- Keep HTMX interactions small and focused

### CSS

- All styles in `static/ui/input.css` using Tailwind v4 `@theme` + `@layer`
- Design tokens: `--color-ink` (text), `--color-base` (bg), `--color-surface` (panels), `--color-rule` (borders)
- Shadows/fonts: `--shadow-soft`, `--shadow-elevated`, `--font-sans`, `--font-display`
- Never edit `tailwind.css` directly — it's compiled output

## Testing

- Tests in `tests/` directory, not inside apps
- Integration tests use Django test client (HTTP requests)
- `conftest.py` sets up Django settings
- Add tests for new domain workflows and state transitions
- Run `uv run pytest` after every meaningful change

## Domain rules

- Core object is the **Case**, not a generic task
- Source data is linked, never dominant
- A Case must be understandable in isolation: private thinking, decisions, spec context, execution state stay together
- Modules: `inbox`, `cases`, `decisions`, `execution`, `focus`, `sources`, `clickup`, `ai` — preserve boundaries per `docs/specs/09-architecture.md`
- Decisions/execution/sources have models only — managed through cases views
- V1 is single-user, but do not hard-code assumptions blocking later multi-user

## UX principles

Calm, text-first, low-noise. Reference: `docs/specs/04-screens-and-ux.md`

- Strong typography, quiet chrome, content over controls
- Support `Calm` and `Compact` display modes
- No enterprise-density patterns, no dashboard clutter, no gamified microcopy
- ClickUp is optional input, not the center of the product

## ADHD design principles

casedock is designed as an evidence-based cognitive support tool. Academic research: `docs/research/2025-05-neurodiversity-summary.md`. Community research: `docs/research/2026-06-adhd-reddit-community-insights.md`. Full 15-point decision record: `docs/decisions/2026-06-09-adhd-design-principles.md`.

**On every UI/UX change, verify against these 5 questions:**

1. Does this ADD decisions or REMOVE them? → Remove wins
2. Could this trigger shame or avoidance? → Red badges, overdue indicators, streak breaks are forbidden
3. Does this rely on user remembering to check? → Auto-surface instead
4. Is the first thing a user sees an ACTION or just INFORMATION? → Action wins
5. Would an ADHD user abandon this after 3 weeks? → Less maintenance = better

**Hard rules (never violate):**

- No red badges, overdue indicators, or "you haven't logged in" notifications
- No gamification (points, XP, streaks, leaderboards, pets)
- No time estimation requirements (ADHD brains can't estimate time reliably)
- Inbox capture must remain one field, zero required fields
- Board must never show more than ~7-10 active cases without folding/hiding

**Key patterns to follow:**

- Surface the FIRST unchecked Execution Item as the "just start" prompt (Principle 1)
- Show "last updated X days ago" instead of asking for due dates (Principle 13)
- Stale detection must be neutral (grey) not punitive (red) (Principle 2)
- Celebrate accomplishments (reverse todo view), not just track backlog (Principle 8)
- Calm ≠ empty/sterile. Subtle animations and satisfying feedback are welcome (Principle 9)

## Docs

- Specs: `docs/specs/01-product-vision.md` through `docs/specs/09-architecture.md`
- Plan: `docs/plan/00-master-implementation-plan.md` (original stage dependencies)
- Plan: `docs/plan/tasks.md` (active tracker — read alongside `current_stage.md`)
- Plan: `docs/plan/stage-runner.md` (workflow rules for `tasks.md`)
- Research: `docs/research/` (ADHD evidence base, community insights, solo-developer fit)
- Decisions: `docs/decisions/2026-07-17-ai-agent-pressure-and-mcp-direction.md` (rationale for Stages 9–12 priority)
- When architecture/UX changes materially: update `docs/` alongside code
