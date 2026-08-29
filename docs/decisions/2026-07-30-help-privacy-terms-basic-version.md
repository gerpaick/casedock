# 2026-07-30 — Help / Privacy / Terms: basic placeholder version

## Context

The footer in `templates/ui/base.html` has linked to `/help/`, `/privacy/`, `/terms/`
since early stages. Those routes did not exist — every click was a 404. The journey
audit (2026-07-15) flagged this under Poprawka #3 and Stage 10 (Trust Hardening)
captured the full scope as tasks 10.1–10.3.

Gerard wants the dead links killed **now** with basic placeholder content, and to
expand to full legal/help copy only when casedock is close to public launch. This ADR
records what landed, what did not, and the single trigger that should re-open this
work.

## Decision

Land a **partial** Stage 10.1–10.3 now: routes + templates + anonymous access +
footer hard-wired to `{% url %}` (so dead links are structurally impossible). Treat
the copy as an honest draft, not as legal text.

### In scope (landed)

- `src/apps/core/urls.py` — three `TemplateView` routes named `help`, `privacy`,
  `terms`, anonymous-accessible (no `LoginRequiredMixin`).
- `templates/core/{help,privacy,terms}.html` — extend `ui/base.html`, calm casedock
  voice, every page eyebrow-marked `Draft` and dated `Last updated: 2026-07-30`.
- `templates/ui/base.html` — footer links switched from raw paths (`/help/`) to
  `{% url 'help' %}` etc.
- `tests/test_smoke.py` — new `TestTrustPages` covering anonymous + authenticated
  access, key content presence, and footer-link resolution.
- Contact addresses use the existing dev convention `@casedock.local` (matches
  `noreply@casedock.local`, `demo@casedock.local`).

### Out of scope (pending — full Stage 10 acceptance)

These are the **full Stage 10.1–10.3 acceptance items** in `tasks.md`. They are
intentionally deferred and tracked there, not here.

- **Help**: 5 FAQ sourced from `docs/specs/03-workflows.md`, how-to-start /
  how-to-capture / how-to-convert-to-Case as structured guides (current page is a
  4-section starter, not the full FAQ).
- **Privacy**: EU-legal review — hosting region + backup policy confirmed, lawful
  basis stated, retention period stated, DPO/contact-for-requests formalised,
  self-serve export/delete in Settings.
- **Terms**: legal entity, jurisdiction, liability cap, full acceptable
  use.
- **Domains**: `help@casedock.local` and `privacy@casedock.local` → production domain.
  Single update point per template — no settings refactor needed yet.

## Trigger to re-open

Any public announcement or sharing of casedock **must not happen** until the items under "Out of scope"
above are resolved and tasks 10.1–10.3 are flipped `[ ]` → `[x]`. Driving traffic to
a page whose footer points at draft legal copy is the failure mode this ADR exists
to prevent.

## Why TemplateView (no view layer)

The pages have no dynamic state. Adding a view module would be ceremony. If a page
later needs context (e.g. support email pulled from settings, last-updated stamp from
a model), promote it to a real view at that point — not before.

## Alternatives considered

- **Wait until full Stage 10**: rejected — footer 404s are a credibility leak today,
  and every session that ships without fixing them makes the next session more likely
  to forget. A clearly-labelled draft is better than a 404.
- **Single combined `/legal/` page with anchors**: rejected — three short pages match
  user expectations for footer links and make per-page "Last updated" stamps honest.
- **Settings-based support email constant**: rejected as over-engineering — three
  placeholder templates each with one hardcoded email is a single-find-and-replace
  task before launch. Revisit if the count grows.
