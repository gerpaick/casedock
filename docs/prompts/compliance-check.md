# casedock — Compliance Check Prompt

> Paste this prompt into an LLM with filesystem access (Codex / Claude / Opus).

---

Analyze the casedock application for consistency between its documentation and implementation.

## What to read (order matters)

1. ADHD philosophy and principles:
   - docs/decisions/2026-06-09-adhd-design-principles.md
   - docs/research/2026-06-adhd-reddit-community-insights.md
   - docs/research/2025-05-neurodiversity-summary.md

2. UX specification:
   - docs/specs/04-screens-and-ux.md
   - docs/specs/01-product-vision.md
   - docs/specs/09-architecture.md

3. Key templates (look for violations here):
   - templates/ui/board.html — main Board
   - templates/cases/case_detail.html — Case view
   - templates/cases/partials/active_cases.html — Active list
   - templates/cases/partials/waiting_cases.html — Waiting list
   - templates/focus/focus.html — Daily Focus
   - templates/inbox/inbox.html — Inbox
   - templates/ui/base.html — base layout

4. CSS:
   - static/ui/input.css — design tokens

5. View logic:
   - src/apps/ui/views.py
   - src/apps/ui/display.py
   - src/apps/cases/views.py
   - src/apps/focus/services.py

## What to check

A. **ADHD principles** — does a template violate any of the five verification questions?
   1. Does it add decisions or remove them? (Removing wins.)
   2. Could anything trigger shame or avoidance? (Red badges, overdue indicators, streak breaks.)
   3. Does it rely on the user remembering to check?
   4. Is the first thing an ACTION or merely information?
   5. Would a user with ADHD abandon this after three weeks?

B. **Hard rules** — look for these violations:
   - Red badges or overdue indicators?
   - Gamification?
   - Required time estimates?
   - Does the Inbox have more than one field or require any fields?
   - Does the Board show more than 10 active Cases without folding them?

C. **Specification consistency** — do the templates implement what
   `docs/specs/04-screens-and-ux.md` describes?

D. **CSS token consistency** — do the templates use tokens from `input.css` (`@theme`) or
   hardcoded colors?

E. **Key patterns** — are these implemented?
   - "Just start" prompt = first unchecked ExecutionItem
   - "Last updated X days ago" instead of due dates
   - Stale detection = gray, not red
   - Reverse todo view (celebrate accomplishments)

## Output format

For EACH template file, provide a table:

| Principle/Spec | Status | Problem | Suggested fix |
|---|---|---|---|
| ... | ✅ / ⚠️ / ❌ | ... | ... |

Finish with a summary showing the number of ✅, ⚠️, and ❌ results and a prioritized list of
what to fix.
