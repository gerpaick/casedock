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

## Tailwind migration — plan sesji

### Zasady cross-session

1. **Każda sesja kończy się działającą apką** — Tailwind i stary `app.css` współistnieją, migrujemy incrementalnie.
2. **Po każdej sesji aktualizuj ten plik** — sekcja "Tailwind — status" poniżej. Zapisz:
   - co zostało zrobione (które komponenty/template'y)
   - co jest do zrobienia (konkretne klasy, pliki)
   - ewentualne problemy lub decyzje podjęte w trakcie
3. **Commit per sesja** — z sensowną wiadomością, np. `tailwind: setup infra`, `tailwind: migrate ui/ templates`.
4. **Jeśli sesja przerywa w połowie** — napisz co zostało niedokończone w sekcji status.
5. **Nie usuwaj `app.css`** dopóki Faza 5 (cleanup) nie jest gotowa.

### Kolejność sesji

#### Sesja 1: Setup infra

**Cel:** Tailwind zainstalowany i kompiluje się, obok istniejącego `app.css`.

**Kroki:**
1. `npm init -y` (jeśli brak `package.json`)
2. `npm install -D tailwindcss @tailwindcss/cli`
3. Stwórz `tailwind.config.js` — zaimportuj palette z `:root` CSS variables (23 zmienne):
   - kolory: `--bg`, `--bg-soft`, `--panel`, `--panel-soft`, `--text`, `--text-soft`, `--muted`, `--line`, `--line-strong`, `--accent`, `--accent-strong`, `--capture-accent`, `--capture-accent-strong`, `--selected`, `--selected-strong`, `--success`, `--danger`
   - fonts: `--font-sans` (IBM Plex Sans), `--font-display` (Iowan Old Style)
   - shadows: `--shadow-soft`, `--shadow-elevated`
4. Stwórz `static/ui/input.css` — `@import "tailwindcss"` + `@theme` z custom palette
5. Build: `npx @tailwindcss/cli -i static/ui/input.css -o static/ui/tailwind.css --watch`
6. W `templates/base.html` dodaj `<link>` do `tailwind.css` **przed** `app.css` (Tailwind ma niższy priorytet, `app.css` override'uje dopóki nie usuniemy)
7. `npm run build:css` w `package.json` scripts
8. Zweryfikuj: apka wygląda identycznie jak przed

**Pliki do stworzenia/zmiany:**
- `package.json` (nowy lub update)
- `tailwind.config.js` (nowy)
- `static/ui/input.css` (nowy)
- `templates/base.html` (dodać link do tailwind.css)
- `.gitignore` — dodaj `static/ui/tailwind.css` (generowany) jeśli nie trackujemy

**Kryteria sukcesu:**
- `npx @tailwindcss/cli` kompiluje bez błędów
- Apka wygląda identycznie z oboma CSS (Tailwind + app.css)
- `uv run pytest` przechodzi

---

#### Sesja 2: Małe komponenty + template'y `ui/`

**Cel:** Migruj małe komponenty i template'y z `apps/ui/`.

**Komponenty do migracji (kolejność):**
1. `.pill`, `.source-chip` — małe inline badge'e
2. `.muted`, `.count-badge` — tekst/badge helper'y
3. `.section-label`, `.eyebrow` — typograficzne label'e
4. `.meta-list`, `.button-row` — prosty layout
5. `.panel`, `.subpanel`, `.soft-row`, `.field` — layout komponenty

**Template'y do migracji:**
- `templates/ui/base.html` — shell, nawigacja, layout
- `templates/ui/board.html` — główny board
- `templates/ui/home.html` — strona domowa
- `templates/ui/search.html` — wyszukiwarka
- `templates/ui/settings.html` — ustawienia

**Metoda:**
- Dla każdej klasy CSS: znajdź definicję w `app.css`, stwórz Tailwind odpowiednik (utility classes lub `@apply` w `input.css` jeśli złożony)
- Zastąp klasę w template
- Sprawdź wizualnie czy wygląda tak samo
- Usuń zmigrowaną regułę z `app.css`

**Kryteria sukcesu:**
- Template'y `ui/` używają Tailwind classes
- Odpowiednie reguły usunięte z `app.css`
- `uv run pytest` przechodzi
- Apka wygląda identycznie

---

#### Sesja 3: Template'y `inbox/`

**Cel:** Migruj komponenty i template'y z `apps/inbox/`.

**Komponenty do migracji:**
- `.inbox-*` — wszystkie inbox-specific styles
- `.capture-*` — capture flow styles
- Pozostałe komponenty używane w inbox template'ach

**Template'y do migracji:**
- `templates/inbox/list.html`
- `templates/inbox/detail.html`
- `templates/inbox/capture.html`
- `templates/inbox/convert.html`
- `templates/inbox/do-now.html`
- `templates/inbox/partials/` — wszystkie partials

**Kryteria sukcesu:**
- Template'y `inbox/` używają Tailwind classes
- Odpowiednie reguły usunięte z `app.css`
- `uv run pytest` przechodzi

---

#### Sesja 4: Template'y `cases/` + `focus/`

**Cel:** Migruj najtrudniejsze template'y.

**Komponenty do migracji:**
- `.case-*` — case workspace styles
- `.focus-*` — focus view styles
- `.board-*` — pozostałe board-specific styles
- Display mode compact overrides (~100 linii)

**Template'y do migracji:**
- `templates/cases/detail.html` — **434 linii**, najtrudniejszy template
- `templates/focus/today.html` — 140 linii

**Kryteria sukcesu:**
- Template'y `cases/` i `focus/` używają Tailwind classes
- Odpowiednie reguły usunięte z `app.css`
- `uv run pytest` przechodzi

---

#### Sesja 5: Cleanup

**Cel:** Usuń `app.css`, zostaw tylko custom CSS tam gdzie Tailwind nie wystarcza.

**Kroki:**
1. Sprawdź co zostało w `app.css` — powinny być tylko:
   - `@keyframes` animations (message-countdown, captureDestinationHint)
   - Tippy.js theme (`.tippy-box[data-theme~="casedock-history"]`)
   - Complex radial-gradient backgrounds
   - `:root` CSS variables (jeśli nie przeniesione w pełni do Tailwind config)
2. Przenieś powyższe do `static/ui/animations.css`
3. Usuń `static/ui/app.css`
4. W `templates/base.html` — usuń link do `app.css`, dodaj link do `animations.css`
5. Napraw testy — ~15 asercji w `test_stage6_surfaces.py` sprawdza konkretne klasy CSS
6. Sprawdź `uv run ruff check .` i `uv run ruff format --check .`
7. Sprawdź `uv run python -m mypy src/`
8. Sprawdź `uv run pytest`

**Kryteria sukcesu:**
- `app.css` usunięty
- `animations.css` zawiera tylko to co Tailwind nie ogarnia
- Wszystkie testy przechodzą
- Lint/type check czysty
- Apka wygląda identycznie

### Co zostaje jako custom CSS

- `@keyframes` animations (message-countdown, captureDestinationHint)
- Tippy.js theme (`.tippy-box[data-theme~="casedock-history"]`)
- Complex radial-gradient backgrounds where Tailwind doesn't map cleanly
- Body background gradient (radial + linear composite)

### Tailwind — status

**Aktualna sesja:** ✅ Sesja 5 COMPLETE — Tailwind migration finished
**Zrobione:**
- ✅ Sesja 1: Setup infra
  - `package.json` — `npm install -D tailwindcss@4.2.4 @tailwindcss/cli@4.2.4`
  - `static/ui/input.css` — `@import "tailwindcss"` + `@theme` z design tokens (18 kolorów, 2 fonty, 2 shadówy)
  - `static/ui/tailwind.css` — generowany (w .gitignore)
  - `templates/ui/base.html` — `<link>` do tailwind.css przed app.css
  - `.gitignore` — dodany `static/ui/tailwind.css`
  - npm scripts: `dev:css` (watch), `build:css` (minify)
  - 74/74 testów przechodzi, ruff czysto
- ✅ Sesja 2: Małe komponenty + template'y `ui/`
  - `input.css` 55→328 linii (+273): `@layer components` z 5 grupami komponentów + compact overrides
  - `app.css` 2129→1872 linii (-257): usunięto zmigrowane reguły
  - Migrowane komponenty: `.pill`, `.source-chip`, `.muted`, `.count-badge`, `.eyebrow`, `.section-label`, `.item-title`, `.meta-list`, `.button-row`, `.panel`, `.subpanel`, `.soft-list`, `.soft-row`, `.field`, `.field-grow`
  - Wszystkie `var(--text)` → `var(--color-ink)` itd. (mapping tokenów w input.css)
  - Template class names bez zmian — testy przechodzą bez modyfikacji
  - 74/74 testów przechodzi, ruff czysto
- ✅ Sesja 3: Template'y `inbox/` + shared components
  - `input.css` 328→1109 linii (+781): Groups 6-16 + compact overrides + `@media (max-width: 700px)` responsive block
  - `app.css` 1872→1120 linii (-752): usunięto zmigrowane reguły
  - Group 6 (Buttons): `.button`, `.button-muted`, `.button-capture`, `.button-quiet`, `.button-subtle`, `.button-link`, `.focus-open-link`
  - Group 7 (Page layout): `.page-head`, `.page-head--stacked`, `.page-head--inbox`, `.page-head__top--inbox`, `.page-head__title-wrap`, `.page-head__action--inbox`, `.page-copy`
  - Group 8 (Section layout): `.section-block`, `.section-grid`, `.card-stack`, `.stack`, `.focus-strip`, `.board-layout`, `.section-head`
  - Group 9 (Inbox stage): `.inbox-stage`, `.inbox-stage__queue`, `.inbox-stage__focus`, `.board-main`, `.board-side`
  - Group 10 (Inbox focus): `.inbox-focus` z `::before` pseudo-element, wszystkie `__` sub-komponenty
  - Group 11 (Queue): `.queue-panel`, `.queue-list`, `.queue-row` z `::before` animowanym accent-barem, `__` sub-komponenty
  - Group 12 (History): `.inbox-history`, `.history-list`, `.history-row`, `.history-tag`, `.history-tag--done`
  - Group 13 (Capture modal): `.capture-modal` z `::backdrop`, `__frame`, `__header`, `.capture-entry-form`, `.capture-page-panel`
  - Group 14 (Form helpers): `.field-error`, `.field-help`, `.field-checkbox`, `.inline-form`, `.section-gap`, `.prose-panel p + p`, `.empty-state`
  - Group 15 (Detail note): `.detail-note`
  - Group 16 (Capture destination hint): `.capture-destination-hint::after` (selector only, @keyframes stay in app.css)
  - Compact overrides: `.stack`, `.page-head`, `.button`, `.capture-modal__frame`, `.inbox-focus`, `.page-copy`, `.detail-note`, `.panel p`
  - Responsive `@media (max-width: 700px)`: inbox + shared layout breakpoints
  - `.panel-form` is a semantic-only class (no CSS definition) — confirmed skipped
  - `.meta-list--inbox` migrated as variant
  - 74/74 testów przechodzi, ruff czysto, Tailwind kompiluje się bez błędów
- ✅ Sesja 4: Board, Focus, Case, Search CSS
  - `input.css` 1109→1879 linii (+770): Groups 17-27 (board/focus/case/search + compact + responsive)
  - `app.css` 1120→371 linii (-749): usunięto wszystkie page-specific reguły
  - Group 17 (Surface stacks): `.surface-stack`, `.surface-stack--*`, `.board-focus-hero`, `.board-active-surface`, `.search-entry`, `.search-results-panel`, `.case-action-panel`, `.case-side-panel`, `.settings-surface`, `__head` variants
  - Group 18 (Board layout): `.board-main-layout`, `.board-right-rail`, `.case-side`, `.board-focus-rail`, `.board-focus-rail__content`
  - Group 19 (Board rows & lists): `.board-group`, `.board-side-panel`, `.focus-setup`, `.focus-current`, `.search-surface`, `.search-empty`, `.board-list`, `.board-history-list`, `.focus-secondary-list`, `.search-list`, `.board-row`, `.board-row__body`, `.board-row__head`, `.board-row__actions`, `.board-history-row`, `.focus-secondary-row`, `.search-row`
  - Group 20 (Board focus cards): `.board-focus-row--three/two/single/empty`, `.board-focus-card--main/secondary`, `.board-focus-card__title` z clamped text + fade gradient, `.board-focus-card__remove`, `.board-focus-card__details`, `@media (hover: none)` touch overrides
  - Group 21 (Board active & rail): `.board-active-row` + sub-components, `.board-rail-panel`, `.board-rail-list`, `.board-rail-row`
  - Group 22 (Focus layout): `.focus-slot`, `.focus-slot--main`, `.focus-shell`, `.focus-current__main`, `.focus-workbench`, `.focus-primary`, `.focus-spotlight` z border/background, `.focus-secondary-row`
  - Group 23 (Search layout): `.search-row`, `.search-row__body`, `.search-form`, `.search-entry` gap override, `.search-results-shell`, `.search-results-panel--primary`
  - Group 24 (Case layout): `.case-entry` + `__primary/summary/metrics/side/grid`, `.case-callout` + `__body`, `.case-metric`, `.case-workbench`, `.case-main`, `.case-section__split`, `.case-section__column`, `.case-section__column--form`
  - Group 25 (Shared elements): `.plain-list`, `.focus-card`/`.board-card`, `.stat-number`, `.board-card__actions`, `.board-row__actions` button widths, `.spec-block`, `.action-menu`, hover states
  - Group 26 (Compact overrides): `.shell`, `.soft-row`, layout gaps, `.board-focus-card--main`, `.board-focus-card__title`, `.focus-spotlight`, `.focus-spotlight__title`, `.case-callout`, `.case-callout__body`
  - Group 27 (Responsive): `.topbar`, `.topbar-actions`, `.nav`, wszystkie multi-column layouts collapsed, `.board-active-row__actions`
  - Token mapping applied (zero `var(--text)` / `var(--muted)` / `var(--accent)` leaks in input.css)
  - 74/74 testów przechodzi, ruff czysto, Tailwind kompiluje się bez błędów
- ✅ Sesja 5: Cleanup — `app.css` removed
  - `input.css` 1879→2239 linii (+360): `@layer base` + Groups 28-32 + keyframes + Tippy theme
  - `app.css` **USUNIĘTY** (371→0 linii)
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
  - 74/74 testów przechodzi, ruff czysto, Tailwind kompiluje się bez błędów
**Do zrobienia:** — nic (Tailwind migration COMPLETE)
**Problemy/decyzje:**
- Tailwind v4 to CSS-first config — brak `tailwind.config.js`, wszystko w `@theme` w CSS
- Nazwy tokenów zmienione vs `:root` żeby uniknąć kolizji z Tailwind namespace'ami:
  `--text → --color-ink`, `--line → --color-rule`, `--bg → --color-base`, `--panel → --color-surface`
- Mapping tokenów udokumentowany w `static/ui/input.css`
- Strategia migracji: przenosimy definicje CSS do `@layer components` w input.css, zachowujemy nazwy klas w template'ach — bezpieczne i stopniowe
- Tailwind tree-shakuje nieużywane tokeny — custom utilities pojawią się w output gdy zaczniemy ich używać w template'ach
- Sesja 3 migrowała shared components — Sesja 4 mogła skupić się na board/focus/case/search
- Sesja 4 przeniosła też `.board-row__actions .button/.button-muted` i `.board-rail-row .detail-note` które w Sesji 3 zostały w app.css
- Sesja 5: plan zakładał że w `app.css` zostaną tylko keyframes + tippy + `:root` — w rzeczywistości zostały też global styles (body, shell, topbar, headings, nav), messages system (144 linie), hero/lede/panel-grid. Wszystko przeniesione do `input.css` jako `@layer base` + Groups 28-32
- Sesja 5: zamiast tworzyć `animations.css`, keyframes i Tippy theme umieszczono bezpośrednio na końcu `input.css` (poza `@layer`) — prostsze, mniej plików

### Szacunek

5 sesji.

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
