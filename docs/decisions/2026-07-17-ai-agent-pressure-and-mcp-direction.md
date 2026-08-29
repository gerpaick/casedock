# Presja agentów AI vs pierwotna idea casedock + kierunek MCP

Data: 2026-07-17
Status: notatka strategiczna z rozmowy analitycznej — nie kontrakt produktowy
Źródła: `docs/specs/01-product-vision.md`, `docs/research/2026-06-adhd-solo-developer-fit.md`, audyt stanu kodu (2026-07-17), research zewnętrzny (Leantime MCP, wzorzec "Claude Code + CLAUDE.md jako ADHD mode")

---

## Kontekst rozmowy

Analiza całej apki: idea, potrzeby, status. Najważniejsze ustalenia tła:

- **Rdzeń produktu jest dojrzały**: core loop capture → triage → convert → case workspace → focus działa end-to-end, 154 testy, mypy strict, multi-user, konfiguracja deploy (Docker + Caddy). Moduły `clickup` i `ai` to świadome stuby.
- **Wszystko wokół rdzenia nie istnieje**: brak onboardingu i publikacji, martwe linki `/help`, `/privacy`, `/terms`.
- **Największa rozbieżność jest wewnętrzna**: produkt obiecuje "resume engine", a zasada ADHD #1 ("pokaż JEDNĄ następną akcję" / "Just Start") — top finding z własnego researchu, priorytet P0 — ma status *not implemented*.
- Meta-ryzyko behawioralne: dokumenty strategiczne powstają szybciej niż weryfikacja na użytkownikach („planning is dopamine").

---

## ⚡ PIERWOTNA IDEA vs PRESJA ZE STRONY AGENTÓW AI

> **To jest najważniejszy wniosek z tej rozmowy. Czytaj ten blok przy każdej decyzji o pozycjonowaniu i roadmapie.**

### Nowa presja konkurencyjna (nieobecna w dotychczasowych dokumentach)

Po analizach z 2025/2026 wyrósł wzorzec, którego nie ma w `docs/research/`: developerzy z ADHD rozwiązują problem inicjacji zadania i odzyskiwania kontekstu przez **agenty AI + pliki kontekstu** (CLAUDE.md / AGENTS.md, task listy czytane przez agenta co sesję). Powstają teksty typu "Claude Code jako mój ADHD mode". Leantime dodał serwer MCP, żeby AI pytało "co mam teraz robić?" bezpośrednio z projektu.

To uderza w propozycję wartości casedock w wariancie **"resume engine dla kodera"**: jeśli agent kodujący i tak trzyma kontekst projektu, po co osobna apka do odzyskiwania kontekstu?

### Ale pierwotna idea leży na innym terenie

Pierwotny problem, z którego wyrósł casedock:

> Wiele tasków od wielu osób (ClickUp, Todoist, email), kilka projektów + support techniczny. Ilość tworzy chaos — kończy się na **klikaniu i przeglądaniu zamiast planowania**.

To jest problem **chaosu na wejściu (intake + triage)**, nie problem kontekstu w kodzie. I ta część jest **znacznie bardziej odporna na falę agentów AI**, bo:

1. **CLAUDE.md jest per-repo.** Chaos jest *między* projektami: klient A, klient B, support, email, ClickUp. Żaden plik kontekstu w repozytorium nie widzi całego strumienia.
2. **Agent kodujący nie robi triage'u.** Nie odpowie na pytanie "z 40 rzeczy, które dziś wpadły, co ma prawo wejść do mojej pracy, a co parkuję". To jest decyzja, nie kompilacja kontekstu.
3. **Pętla "klikam i przeglądam zamiast planować"** to ADHD-owe unikanie decyzji przez pseudo-aktywność. ClickUp/Todoist ją *pogłębiają* (nieskończona lista do scrollowania); casedock ją *przecina* (przymusowy triage: park / do now / convert / waiting + twardy limit fokusa 1+2). Pierwszym ekranem jest decyzja, nie lista.

Spójne z własnym researchem: fit "incoming work scattered across tools" = *high*; "personal interpretation layer between external assignment and real execution" = *very high*.

### Wniosek pozycjonujący

- **Rdzeń tożsamości**: jeden lejek, przez który przechodzi cały chaos z ClickUpa/Todoista/maila, *zanim* stanie się pracą. Tego agenty AI nie obsługują i długo nie obsłużą — to problem podejmowania decyzji, nie techniczny.
- **Druga noga (nie odwrotnie)**: context recovery / "resume engine" — tu agenty realnie odgryzają wartość, więc ta noga wymaga integracji z agentami (MCP, niżej), a nie konkurowania z nimi.

---

## MCP w casedock — po co, dlaczego, jaka korzyść

### Teza strategiczna

**MCP odwraca zagrożenie w fosę.** Bez MCP casedock i agent AI konkurują o rolę "pamięci zewnętrznej" — agent wygra wygodą. Z MCP casedock staje się **strukturalnym źródłem prawdy, które agent czyta**: cross-projektowym, z cyklem życia (inbox → case → done), z triage'em — czego pliki per-repo nie mają. Im więcej pracy z agentami, tym casedock jest *bardziej* potrzebny, nie mniej.

### Kierunek 1: casedock jako serwer MCP (agent czyta z casedock) — priorytet

Scenariusze użycia:

- **Start sesji kodowania.** Agent woła `get_focus` + `get_case` → dostaje spec Case'a, ostatnie decyzje, pierwszy niedokończony ExecutionItem. Pytanie "co mam teraz robić?" dostaje odpowiedź z *własnego* systemu decyzyjnego usera, nie wymyśloną przez model.
- **Capture bez wychodzenia z terminala.** W trakcie kodowania przychodzi myśl "trzeba ogarnąć backup u klienta X" → agent woła `capture_inbox_item`. Myśl ląduje w lejku, zero zmiany kontekstu. Dla ADHD kluczowe: największy koszt capture to przełączenie do innej apki.
- **Koniec sesji = tanie ponowne wejście.** Agent podsumowuje "co ustaliliśmy i jaki jest następny ruch", user zatwierdza, wpis ląduje jako decyzja/ExecutionItem w Case. Robotę dokumentacyjną (której ADHD-owy mózg nienawidzi) wykonuje agent.

Precedens rynkowy: Leantime MCP server ("what should I work on next?" z live project context).

### Kierunek 2: MCP jako kanał wejściowy (zamiast dedykowanych connectorów)

Roadmapa (Phase 2) zakłada ręcznie pisany connector ClickUp, potem Jira/GitHub. Alternatywa: agent z dostępem MCP do ClickUpa/maila/GitHuba **zasila inbox casedock** przez ten sam `capture_inbox_item`.

- Korzyść: jeden punkt wejścia zamiast N connectorów do utrzymania; każda pozycja i tak przechodzi ludzki triage ("triage before commitment").
- **Ryzyko do pilnowania**: musi pozostać *na żądanie* ("zbierz mi dzisiejsze taski z ClickUpa do inboxa"), nie jako autonomiczny sync w tle — inaczej odtworzy się ten sam chaos, od którego user ucieka, tylko w casedock.

### Granice (zgodne z istniejącymi zasadami produktu — muszą pozostać nienaruszone)

- **"AI nie podejmuje autonomicznych decyzji"** → narzędzia read-mostly. Jedyny zapis: `capture_inbox_item` (przechodzi ludzki triage). Żadnego `set_focus`, `close_case`, `prioritize` przez agenta.
- **"Prywatne notatki nie wychodzą do systemów zewnętrznych bez jawnej akcji usera"** → `PrivateNote` domyślnie NIEwystawione przez MCP; ewentualnie osobna, świadoma zgoda per Case.
- Całość opt-in, token per user.

### Szkic techniczny (na później, nie do natychmiastowej realizacji)

- Naturalne miejsce: stub `src/apps/ai/`.
- Python MCP SDK + autoryzacja tokenem per user.
- 4–5 narzędzi na start: `get_focus`, `list_active_cases`, `get_case`, `get_next_move`, `capture_inbox_item`.
- Mały, dobrze ograniczony zakres — tanie do zbudowania po domknięciu P0.

---

## Rekomendowana kolejność (bez zmian względem audytu journey, z jednym dopiskiem)

1. **Zasada ADHD #1 ("Just Start" / jedna widoczna następna akcja)** — przed każdym nowym feature'em. Bez tego casedock jest archiwum kontekstu, nie silnikiem wznowienia.
2. First-run experience → martwe linki (`/help`, `/privacy`, `/terms`).
3. **MCP (kierunek 1)** — przed connectorem ClickUp z Phase 2; świat poszedł w stronę agentów, nie ręcznych connectorów.
4. Pytanie kontrolne przed każdą sesją: *czy sam przetworzyłem dziś swoją pracę przez casedock?* (metryka sukcesu MVP ze speców: "user zaczyna procesować pracę najpierw w tym systemie").
