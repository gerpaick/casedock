# Progress & Next Steps

## Done

- Stages 1–6 implemented (74 tests) + auth views (25 tests) = 99 tests passing
- ruff strict configured (B, C4, ERA, F, I, PT, RUF, SIM, T20, UP)
- mypy strict configured with django-stubs
- AGENTS.md updated with quick reference, type safety rules, linting rules
- opencode memory filled (`.opencode/memory/project.md`)
- ruff lint errors fixed (8 → 0)
- all files formatted with ruff format
- curly quotes replaced with straight quotes
- mypy strict: 152 → 0 errors (21 files)
  - all model `save()` methods annotated (`*args: object, **kwargs: object -> None`)
  - managers/forms/views: generic type args via `TYPE_CHECKING` guard
  - `seed_demo.py`: `DEMO_CASES`/`DEMO_INBOX_ITEMS` typed as `list[dict[str, Any]]`
  - `environ` import: added `ignore_missing_imports` override in `pyproject.toml`
  - dynamic attrs on `Case` declared as class-level type annotations
- Auth views implemented (99 tests passing)
  - `src/apps/core/forms.py` — `EmailAuthenticationForm` (email field instead of username)
  - `src/apps/core/urls.py` — login, logout, password-reset flow (Django built-in views)
  - `src/config/settings/base.py` — `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`
  - `LoginRequiredMixin` on all 20 views across ui/, inbox/, cases/, focus/
  - `templates/registration/` — login, password_reset_form/done/confirm/complete
  - `templates/ui/base.html` — nav hidden for anon, logout button for authenticated
  - `tests/test_auth.py` — 25 tests: login/logout, password reset, anon protection, nav visibility
  - `tests/conftest.py` — `user` + authenticated `client` fixtures
- Inbox cleanup + global capture shortcut (2026-07-28, off-stage)
  - **P0-A**: removed unused model fields `raw_metadata_snapshot` + `source_reference` from `InboxItem`; migration `0005_remove_unused_source_fields`; cleaned `demo_fixtures.py` + `seed_demo.py` (CU-DEMO-204 lookup now by `source_type == CLICKUP`); spec `02-domain-model.md` updated with removal note citing ADR 2026-07-17
  - **P0-B**: added Archive as 6th v1 triage action — `InboxTriageActionView.action_to_state["archive"]`, Archive buttons in `detail.html` + `_focus_panel.html`, 4 tests. Validator relaxed to allow `converted_case` in ARCHIVED state (provenance survives cleanup); spec `02-domain-model.md` L71-73 + L45-51 updated
  - **Global capture shortcut**: `c` alone (Gmail/Todoist style) opens capture modal anywhere; new `_global_quick_capture.html` partial in `base.html`; new context processor `inbox_global_capture`; JS handler extends existing keydown listener (skips input/textarea/dialog-open); keyboard help modal lists `c`. ADR `2026-07-28-global-capture-shortcut.md` resolves open question from `2026-05-09-clickup-focus-flow-design-review.md` L413
  - 154 → 161 tests passing; ruff/mypy clean

## In progress

— nothing currently

## Next (priority order)

1. Stage 8: hardening (empty-state polish, error handling audit, release gates)

## Tailwind migration — session plan

### Cross-session rules

1. **Every session ends with a working application** — Tailwind and the old `app.css` coexist;
   migrate incrementally.
2. **Update this file after every session** — use the "Tailwind — status" section below. Record:
   - what was completed (which components/templates)
   - what remains to be done (specific classes and files)
   - any problems or decisions made along the way
3. **One commit per session** — with a meaningful message, such as `tailwind: setup infra` or
   `tailwind: migrate ui/ templates`.
4. **If a session stops halfway through** — record what remains unfinished in the status section.
5. **Do not remove `app.css`** until Phase 5 (cleanup) is complete.

### Session sequence

#### Session 1: Set up infrastructure

**Goal:** Install and compile Tailwind alongside the existing `app.css`.

**Steps:**

1. `npm init -y` (if `package.json` does not exist)
2. `npm install -D tailwindcss @tailwindcss/cli`
3. Create `tailwind.config.js` — import the palette from the `:root` CSS variables (23
   variables):
   - colors: `--bg`, `--bg-soft`, `--panel`, `--panel-soft`, `--text`, `--text-soft`, `--muted`,
     `--line`, `--line-strong`, `--accent`, `--accent-strong`, `--capture-accent`,
     `--capture-accent-strong`, `--selected`, `--selected-strong`, `--success`, `--danger`
   - fonts: `--font-sans` (IBM Plex Sans), `--font-display` (Iowan Old Style)
   - shadows: `--shadow-soft`, `--shadow-elevated`
4. Create `static/ui/input.css` — `@import "tailwindcss"` + `@theme` with the custom palette
5. Build: `npx @tailwindcss/cli -i static/ui/input.css -o static/ui/tailwind.css --watch`
6. Add a `<link>` to `tailwind.css` in `templates/base.html` **before** `app.css` (Tailwind has
   lower priority, so `app.css` overrides it until removal)
7. Add `npm run build:css` to the scripts in `package.json`
8. Verify that the application looks identical to the previous version

**Files to create or change:**

- `package.json` (new or updated)
- `tailwind.config.js` (new)
- `static/ui/input.css` (new)
- `templates/base.html` (add the link to tailwind.css)
- `.gitignore` — add generated `static/ui/tailwind.css` if it is not tracked

**Success criteria:**

- `npx @tailwindcss/cli` compiles without errors
- The application looks identical with both CSS files (Tailwind + app.css)
- `uv run pytest` passes

---

#### Session 2: Small components + `ui/` templates

**Goal:** Migrate small components and templates from `apps/ui/`.

**Components to migrate (in order):**

1. `.pill`, `.source-chip` — small inline badges
2. `.muted`, `.count-badge` — text/badge helpers
3. `.section-label`, `.eyebrow` — typographic labels
4. `.meta-list`, `.button-row` — simple layout
5. `.panel`, `.subpanel`, `.soft-row`, `.field` — layout components

**Templates to migrate:**

- `templates/ui/base.html` — shell, navigation, layout
- `templates/ui/board.html` — main Board
- `templates/ui/home.html` — home page
- `templates/ui/search.html` — search
- `templates/ui/settings.html` — settings

**Method:**

- For each CSS class, find its definition in `app.css` and create a Tailwind equivalent (utility
  classes, or `@apply` in `input.css` if it is complex)
- Replace the class in the template
- Verify visually that it looks the same
- Remove the migrated rule from `app.css`

**Success criteria:**

- The `ui/` templates use Tailwind classes
- The corresponding rules have been removed from `app.css`
- `uv run pytest` passes
- The application looks identical

---

#### Session 3: `inbox/` templates

**Goal:** Migrate components and templates from `apps/inbox/`.

**Components to migrate:**

- `.inbox-*` — all Inbox-specific styles
- `.capture-*` — capture-flow styles
- Other components used in Inbox templates

**Templates to migrate:**

- `templates/inbox/list.html`
- `templates/inbox/detail.html`
- `templates/inbox/capture.html`
- `templates/inbox/convert.html`
- `templates/inbox/do-now.html`
- `templates/inbox/partials/` — all partials

**Success criteria:**

- The `inbox/` templates use Tailwind classes
- The corresponding rules have been removed from `app.css`
- `uv run pytest` passes

---

#### Session 4: `cases/` + `focus/` templates

**Goal:** Migrate the most complex templates.

**Components to migrate:**

- `.case-*` — Case workspace styles
- `.focus-*` — Focus view styles
- `.board-*` — remaining Board-specific styles
- Compact display-mode overrides (~100 lines)

**Templates to migrate:**

- `templates/cases/detail.html` — **434 lines**, the most complex template
- `templates/focus/today.html` — 140 lines

**Success criteria:**

- The `cases/` and `focus/` templates use Tailwind classes
- The corresponding rules have been removed from `app.css`
- `uv run pytest` passes

---

#### Session 5: Cleanup

**Goal:** Remove `app.css`, leaving custom CSS only where Tailwind is insufficient.

**Steps:**

1. Check what remains in `app.css` — it should contain only:
   - `@keyframes` animations (message-countdown, captureDestinationHint)
   - Tippy.js theme (`.tippy-box[data-theme~="casedock-history"]`)
   - Complex radial-gradient backgrounds
   - `:root` CSS variables (if they have not been fully moved to the Tailwind configuration)
2. Move the above into `static/ui/animations.css`
3. Remove `static/ui/app.css`
4. In `templates/base.html`, remove the link to `app.css` and add one to `animations.css`
5. Repair the tests — approximately 15 assertions in `test_stage6_surfaces.py` check specific
   CSS classes
6. Run `uv run ruff check .` and `uv run ruff format --check .`
7. Run `uv run python -m mypy src/`
8. Run `uv run pytest`

**Success criteria:**

- `app.css` has been removed
- `animations.css` contains only what Tailwind cannot express cleanly
- All tests pass
- Lint and type checks are clean
- The application looks identical

### What remains as custom CSS

- `@keyframes` animations (message-countdown, captureDestinationHint)
- Tippy.js theme (`.tippy-box[data-theme~="casedock-history"]`)
- Complex radial-gradient backgrounds where Tailwind doesn't map cleanly
- Body background gradient (radial + linear composite)

### Tailwind — status

**Current session:** ✅ Session 5 COMPLETE — Tailwind migration finished
**Completed:**

- ✅ Session 1: Set up infrastructure
  - `package.json` — `npm install -D tailwindcss@4.2.4 @tailwindcss/cli@4.2.4`
  - `static/ui/input.css` — `@import "tailwindcss"` + `@theme` with design tokens (18 colors, 2
    fonts, 2 shadows)
  - `static/ui/tailwind.css` — generated (in .gitignore)
  - `templates/ui/base.html` — `<link>` to tailwind.css before app.css
  - `.gitignore` — added `static/ui/tailwind.css`
  - npm scripts: `dev:css` (watch), `build:css` (minify)
  - 74/74 tests passing, ruff clean
- ✅ Session 2: Small components + `ui/` templates
  - `input.css` 55→328 lines (+273): `@layer components` with five component groups + compact
    overrides
  - `app.css` 2129→1872 lines (-257): removed migrated rules
  - Migrated components: `.pill`, `.source-chip`, `.muted`, `.count-badge`, `.eyebrow`,
    `.section-label`, `.item-title`, `.meta-list`, `.button-row`, `.panel`, `.subpanel`,
    `.soft-list`, `.soft-row`, `.field`, `.field-grow`
  - All `var(--text)` → `var(--color-ink)`, etc. (token mapping in input.css)
  - Template class names unchanged — tests pass without modification
  - 74/74 tests passing, ruff clean
- ✅ Session 3: `inbox/` templates + shared components
  - `input.css` 328→1109 lines (+781): Groups 6-16 + compact overrides +
    `@media (max-width: 700px)` responsive block
  - `app.css` 1872→1120 lines (-752): removed migrated rules
  - Group 6 (Buttons): `.button`, `.button-muted`, `.button-capture`, `.button-quiet`, `.button-subtle`, `.button-link`, `.focus-open-link`
  - Group 7 (Page layout): `.page-head`, `.page-head--stacked`, `.page-head--inbox`, `.page-head__top--inbox`, `.page-head__title-wrap`, `.page-head__action--inbox`, `.page-copy`
  - Group 8 (Section layout): `.section-block`, `.section-grid`, `.card-stack`, `.stack`, `.focus-strip`, `.board-layout`, `.section-head`
  - Group 9 (Inbox stage): `.inbox-stage`, `.inbox-stage__queue`, `.inbox-stage__focus`, `.board-main`, `.board-side`
  - Group 10 (Inbox focus): `.inbox-focus` with a `::before` pseudo-element and all `__`
    subcomponents
  - Group 11 (Queue): `.queue-panel`, `.queue-list`, `.queue-row` with an animated `::before`
    accent bar and `__` subcomponents
  - Group 12 (History): `.inbox-history`, `.history-list`, `.history-row`, `.history-tag`, `.history-tag--done`
  - Group 13 (Capture modal): `.capture-modal` with `::backdrop`, `__frame`, `__header`,
    `.capture-entry-form`, `.capture-page-panel`
  - Group 14 (Form helpers): `.field-error`, `.field-help`, `.field-checkbox`, `.inline-form`, `.section-gap`, `.prose-panel p + p`, `.empty-state`
  - Group 15 (Detail note): `.detail-note`
  - Group 16 (Capture destination hint): `.capture-destination-hint::after` (selector only;
    @keyframes remain in app.css)
  - Compact overrides: `.stack`, `.page-head`, `.button`, `.capture-modal__frame`, `.inbox-focus`, `.page-copy`, `.detail-note`, `.panel p`
  - Responsive `@media (max-width: 700px)`: inbox + shared layout breakpoints
  - `.panel-form` is a semantic-only class (no CSS definition) — confirmed skipped
  - `.meta-list--inbox` migrated as variant
  - 74/74 tests passing, ruff clean, Tailwind compiles without errors
- ✅ Session 4: Board, Focus, Case, and Search CSS
  - `input.css` 1109→1879 lines (+770): Groups 17-27 (Board/Focus/Case/Search + compact +
    responsive)
  - `app.css` 1120→371 lines (-749): removed all page-specific rules
  - Group 17 (Surface stacks): `.surface-stack`, `.surface-stack--*`, `.board-focus-hero`, `.board-active-surface`, `.search-entry`, `.search-results-panel`, `.case-action-panel`, `.case-side-panel`, `.settings-surface`, `__head` variants
  - Group 18 (Board layout): `.board-main-layout`, `.board-right-rail`, `.case-side`, `.board-focus-rail`, `.board-focus-rail__content`
  - Group 19 (Board rows & lists): `.board-group`, `.board-side-panel`, `.focus-setup`, `.focus-current`, `.search-surface`, `.search-empty`, `.board-list`, `.board-history-list`, `.focus-secondary-list`, `.search-list`, `.board-row`, `.board-row__body`, `.board-row__head`, `.board-row__actions`, `.board-history-row`, `.focus-secondary-row`, `.search-row`
  - Group 20 (Board focus cards): `.board-focus-row--three/two/single/empty`,
    `.board-focus-card--main/secondary`, `.board-focus-card__title` with clamped text + fade
    gradient, `.board-focus-card__remove`, `.board-focus-card__details`, `@media (hover: none)`
    touch overrides
  - Group 21 (Board active & rail): `.board-active-row` + sub-components, `.board-rail-panel`, `.board-rail-list`, `.board-rail-row`
  - Group 22 (Focus layout): `.focus-slot`, `.focus-slot--main`, `.focus-shell`,
    `.focus-current__main`, `.focus-workbench`, `.focus-primary`, `.focus-spotlight` with
    border/background, `.focus-secondary-row`
  - Group 23 (Search layout): `.search-row`, `.search-row__body`, `.search-form`, `.search-entry` gap override, `.search-results-shell`, `.search-results-panel--primary`
  - Group 24 (Case layout): `.case-entry` + `__primary/summary/metrics/side/grid`, `.case-callout` + `__body`, `.case-metric`, `.case-workbench`, `.case-main`, `.case-section__split`, `.case-section__column`, `.case-section__column--form`
  - Group 25 (Shared elements): `.plain-list`, `.focus-card`/`.board-card`, `.stat-number`, `.board-card__actions`, `.board-row__actions` button widths, `.spec-block`, `.action-menu`, hover states
  - Group 26 (Compact overrides): `.shell`, `.soft-row`, layout gaps, `.board-focus-card--main`, `.board-focus-card__title`, `.focus-spotlight`, `.focus-spotlight__title`, `.case-callout`, `.case-callout__body`
  - Group 27 (Responsive): `.topbar`, `.topbar-actions`, `.nav`, all multi-column layouts
    collapsed, `.board-active-row__actions`
  - Token mapping applied (zero `var(--text)` / `var(--muted)` / `var(--accent)` leaks in input.css)
  - 74/74 tests passing, ruff clean, Tailwind compiles without errors
- ✅ Session 5: Cleanup — `app.css` removed
  - `input.css` 1879→2239 lines (+360): `@layer base` + Groups 28-32 + keyframes + Tippy theme
  - `app.css` **REMOVED** (371→0 lines)
  - `@layer base`: body styles (margin, radial-gradient background, font), `.has-modal-open`, heading resets (h1-h4)
  - Group 28 (Shell & brand): `.brand`, `.shell`, `main`
  - Group 29 (Topbar): `.topbar`, `.topbar-brand`, `.topbar-note`, `.topbar-actions`
  - Group 30 (Navigation): `.nav`, `.nav > a/span`, `.is-active`
  - Group 31 (Messages system): `.messages`, `.message`, `.js .message`, `.message__*`, `.message__countdown`, `@media (prefers-reduced-motion)`
  - Group 32 (Hero, lede, panel-grid): `.hero`, `.lede`, `.panel-grid`
  - Keyframes (outside layers): `message-countdown`, `captureDestinationHint`, `captureDestinationHintReduced`
  - Tippy.js theme (outside layers): `.tippy-box[data-theme~="casedock-history"]`
  - `:root` block removed — tokens defined exclusively in `@theme`
  - `* { box-sizing }` removed — Tailwind Preflight handles this
  - Zero old `var()` references remain (all → `--color-*` tokens)
  - `base.html`: removed `app.css` link, only `tailwind.css` loaded
  - 74/74 tests passing, ruff clean, Tailwind compiles without errors

**To do:** — nothing (Tailwind migration COMPLETE)

**Problems/decisions:**

- Tailwind v4 uses CSS-first configuration — there is no `tailwind.config.js`; everything lives
  in `@theme` in CSS
- Token names changed from their `:root` versions to avoid collisions with Tailwind namespaces:
  `--text → --color-ink`, `--line → --color-rule`, `--bg → --color-base`, `--panel → --color-surface`
- The token mapping is documented in `static/ui/input.css`
- Migration strategy: move CSS definitions into `@layer components` in input.css while keeping
  class names unchanged in templates — safe and incremental
- Tailwind tree-shakes unused tokens — custom utilities will appear in the output once templates
  begin using them
- Session 3 migrated shared components, allowing Session 4 to focus on Board/Focus/Case/Search
- Session 4 also moved `.board-row__actions .button/.button-muted` and
  `.board-rail-row .detail-note`, which remained in app.css after Session 3
- Session 5: the plan assumed that only keyframes, Tippy, and `:root` would remain in `app.css`;
  in practice, global styles (body, shell, topbar, headings, navigation), the messages system
  (144 lines), and hero/lede/panel-grid remained too. Everything moved into `input.css` as
  `@layer base` + Groups 28-32
- Session 5: instead of creating `animations.css`, the keyframes and Tippy theme were placed
  directly at the end of `input.css` (outside `@layer`) — simpler, with fewer files

### Estimate

Five sessions.

## Last updated

2026-05-27

## Board focus-centric redesign

### What was done

- **Stale detection**: Cases untouched for 7+ days surface as "stale" on the Board with action buttons (Done, Move to waiting, Still active). Stale cases are acked (up to configurable limit) without status change.
- **Active/Waiting views**: Dedicated pages at `/active/` and `/waiting/` listing all active and waiting cases respectively. Accessible from Board bottom links and topbar.
- **Board redesign**: Single-column focus-centric layout. Focus hero at top, stale alerts below, bottom links to Active/Waiting views. Old two-column layout with inbox rail removed.
- **Topbar "Active" link**: Navigation link added between Board and Inbox for quick access to active cases.

### Files changed

- `templates/ui/base.html` — added "Active" nav link
- `templates/ui/_board_page.html` — redesigned board template (stale section, bottom links)
- `templates/ui/active.html` — new active cases page
- `templates/ui/waiting.html` — new waiting cases page
- `static/ui/input.css` — new CSS for stale section, bottom links, transition prompt; dead CSS removed (board-main-layout, board-active-surface, board-right-rail, board-rail-panel, board-focus-rail, board-focus-rail__content)

### Dead CSS removed

- `.board-main-layout` — old two-column board layout
- `.board-active-surface`, `.board-active-surface__head`, `.board-active-surface__empty` — unused surface wrapper
- `.board-right-rail` — old board right rail
- `.board-rail-panel`, `.board-rail-panel--inbox` — old rail panel
- `.board-focus-rail`, `.board-focus-rail__content` — old focus rail grid

### New CSS classes

- Group 21b: `.board-stale-section`, `.board-stale-row`, `.board-stale-row__body`, `.board-stale-row__actions`
- Group 21c: `.board-bottom-row`, `.board-bottom-links`, `.board-bottom-link`
- Group 21d: `.board-transition-prompt`, `.board-transition-prompt__actions`
- Responsive: `.board-stale-row`, `.board-stale-row__actions` mobile breakpoints

### Regression

- 131 tests passing
- ruff check/format clean
- mypy strict clean
- Django system check clean
- CSS rebuilds via `npm run build:css`
