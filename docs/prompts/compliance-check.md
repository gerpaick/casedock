# casedock — Compliance Check Prompt

> Wklej ten prompt do LLM z dostępem do filesystem (Codex / Claude / Opus).

---

Przeanalizuj aplikację casedock pod kątem spójności między dokumentacją a implementacją.

## Co przeczytać (kolejność ma znaczenie):

1. Filozofia i zasady ADHD:
   - docs/decisions/2026-06-09-adhd-design-principles.md
   - docs/research/2026-06-adhd-reddit-community-insights.md
   - docs/research/2025-05-neurodiversity-summary.md

2. Specyfikacja UX:
   - docs/specs/04-screens-and-ux.md
   - docs/specs/01-product-vision.md
   - docs/specs/09-architecture.md

3. Kluczowe szablony (tu szukaj naruszeń):
   - templates/ui/board.html — Board główny
   - templates/cases/case_detail.html — widok Case'a
   - templates/cases/partials/active_cases.html — lista Active
   - templates/cases/partials/waiting_cases.html — lista Waiting
   - templates/focus/focus.html — Daily Focus
   - templates/inbox/inbox.html — Inbox
   - templates/ui/base.html — layout bazowy

4. CSS:
   - static/ui/input.css — tokeny designu

5. Logika widoków:
   - src/apps/ui/views.py
   - src/apps/ui/display.py
   - src/apps/cases/views.py
   - src/apps/focus/services.py

## Co sprawdzić:

A. **Zasady ADHD** — czy szablon łamie którąś z 5 pytań weryfikacyjnych?
   1. Dodaje decyzje czy je usuwa? (usuwanie wygrywa)
   2. Czy coś może wywołać wstyd/unikanie? (czerwone badge, overdue, streak break)
   3. Czy polega na tym, że user pamięta sprawdzić?
   4. Czy pierwsza rzecz to AKCJA czy informacja?
   5. Czy użytkownik ADHD porzuci to po 3 tygodniach?

B. **Hard rules** — naruszenia:
   - Czerwone badge / overdue indicators?
   - Gamifikacja?
   - Wymaganie estymacji czasu?
   - Inbox ma więcej niż jedno pole / wymaga wymaganych pól?
   - Board pokazuje >10 aktywnych case'ów bez folding?

C. **Spójność ze specyfikacją** — czy szablony realizują to co opisano w docs/specs/04-screens-and-ux.md?

D. **Spójność tokenów CSS** — czy szablony używają tokenów z input.css (@theme) czy hardcoded colors?

E. **Key patterns** — czy są zaimplementowane:
   - "Just start" prompt = pierwszy unchecked ExecutionItem
   - "Last updated X days ago" zamiast due dates
   - Stale detection = szary, nie czerwony
   - Reverse todo view (celebrate accomplishments)

## Format wyniku:

Dla KAŻDEGO pliku szablonu wypisz tabelę:

| Zasada/Spec | Status | Problem | Sugestia fixu |
|---|---|---|---|
| ... | ✅ / ⚠️ / ❌ | ... | ... |

Na koniec podsumowanie: ile ✅, ile ⚠️, ile ❌ i lista priorytetowa co naprawić.
