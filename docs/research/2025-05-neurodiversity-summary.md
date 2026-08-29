# casedock — Neurodiversity Research Summary

> Syntéza researchu: jak obecne funkcje wspiera dowody naukowe i na co zwrócić uwagę w przyszłości.
> Pełna bibliografia z linkami: [`2025-05-neurodiversity-evidence-base.md`](./2025-05-neurodiversity-evidence-base.md)

---

## Co mówi nauka — w jednym zdaniu

casedock adresuje **realny, dobrze udokumentowany problem**: 10%+ programistów doświadcza ADHD lub podobnych wzorców executive dysfunction, standardowe narzędzia (Jira, ClickUp, Asana) generują cognitive overload który disproportionately obciąża neurodivergent mózgi, a odpowiednio zaprojektowane narzędzie może **wyeliminować** różnicę w wydajności między ADHD a neurotypical użytkownikami.

---

## Jak obecne funkcje wspierają dowody

### 1. Daily Focus (1 main + 2 secondary)

To nie jest minimalistyczny wybór estetyczny — to **evidence-based intervention**.

- **Forster & Lavie (2014)**: ograniczenie pola percepcyjnego do relevant items **eliminuje gap** w distractibility między ADHD a neurotypical. Gdy items są ograniczone, ADHD mózg nie jest już bardziej rozpraszony niż neurotypical. ([DOI](https://doi.org/10.1037/neu0000020))
- **Le Cunff (2024)**: ADHD positively predicts extraneous cognitive load — visual noise kosztuje ADHD mózg więcej. 3 items zamiast 50 = redukcja tego kosztu. ([DOI](https://doi.org/10.3390/educsci14050516))
- **Kasper (2013)**: working memory deficits w ADHD oznaczają że mentalne sortowanie 50 zadań jest niefiabilne. 3 items = w zasięgu WM capacity. ([DOI](https://doi.org/10.1037/a0032371))

### 2. Calm UI / Quiet Chrome

- **Kasatskii (2023)**: **35% redukcja** w perceived distraction z minimalistycznym interfejsem IDE. Low perceptual load (2 panele vs 7) = szybsze kodowanie. ([DOI](https://doi.org/10.1007/978-3-031-35017-7_9))
- **Rosenberg (2023, MIT Press)**: ważna niuans — cognitive load (złożoność decyzji) **szkodzi** ADHD, ale pewne perceptual engagement może **pomagać**. "Calm" nie znaczy puste. Oznacza mało decyzji, mało hałasu, ale wystarczająco bogate żeby utrzymać attention. ([DOI](https://doi.org/10.1162/netn_a_00341))
- **Weyerhäuser & Piccolo (2026)**: **obie grupy** (ADHD i NT) benefited z ADHD-friendly redesign — curb-cut effect. Calm design nie wyklucza NT użytkowników. ([DOI](https://doi.org/10.1007/978-3-032-05008-3_59))

### 3. Triage przed commitment (Do now / Convert / Park / Waiting)

- **Scientific Reports (2026)**: ADHD ma **delayed goal-directed processing** — mózg wolniej przygotowuje cele. Kiedy cele muszą być generowane samodzielnie (otwarta lista zadań), habitual responses dominują. 4 jasne, nazwane akcje to external goal structure — bypassuje to opóźnienie. ([Nature](https://www.nature.com/srep/))
- **Durand (2020)**: osoby z ADHD **wiedzą** jak się organizować — problem jest w **persistence**. Narzędzie które utrzymuje strukturę za użytkownika to nie "trening" — to compensation. ([DOI](https://doi.org/10.7717/peerj.9844))
- **Sonuga-Barke (2003, dual pathway)**: unikanie zadań może wynikać z **delay aversion** (zadanie wydaje się niekończące/nieopłacalne), nie z lenistwa. Triage tworzy bounded, nazwane ścieżki — każda ma koniec. ([DOI](https://doi.org/10.1016/j.neubiorev.2003.08.005))

### 4. Case jako bounded work unit (Spec + Decisions + Execution + Notes + Links)

- **Leroy (2009)**: **attention residue** — przechodząc z nieukończonego zadania na nowe, część uwagi zostaje na poprzednim. Case jako closed unit (start → execution → done) redukuje residue. ([DOI](https://doi.org/10.1016/j.obhdp.2009.04.002))
- **Gilbert (2020)**: external reminders pozwalają osobom z **lower working memory dogonić** high-performers. Case który externalizuje cały context (decyzje, notes, execution state) to pełne cognitive offloading. ([DOI](https://doi.org/10.1037/xge0000652))
- **Greenwald (2024)**: scaffolding **wyeliminował** gap w comprehension między ADHD a NT. Case = scaffolding structure. ([DOI](https://doi.org/10.1016/j.learninstruc.2024.102051))

### 5. Re-entry support (next step, recent decisions, summary)

- **Mark (2008)**: **23 minuty** do ponownego skupienia po przerwaniu — dla neurotypical. Dla ADHD z WM deficits, prawdopodobnie gorzej. ([DOI](https://doi.org/10.1145/1357054.1357072))
- **Koch (2023)**: resumption costs reflect **activation decay** — task goals naturalnie znikają z WM podczas przerwania. Visible Case state externalizuje te goals. ([DOI](https://doi.org/10.3758/s13421-023-01458-8))
- **McDowall (2025)**: ADHD developer dosłownie mówił: *"5 seconds is forever. Whatever I was thinking is just gone."* Next step + recent decisions na wierzchu to odpowiedź na ten mechanizm. ([PDF](https://people.cs.umass.edu/~mendres/papers/GetMeInTheGroove.pdf))

### 6. Private Notes

- **Morris (2015, Microsoft)**: większość ND employees **nie ujawnia** diagnozy w pracy z obawy przed judgment. ([PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/neurodiverse_tech_employees_assets2015.pdf))
- **Spiel (2022, CHI)**: technology research częściej frame'uje ADHD jako "problem do mitigacji" niż jako valid cognitive style. Private notes to **safe space** — nie monitoring, nie sharing, nie "fixing." ([DOI](https://doi.org/10.1145/3491102.3517592))
- **"I Work Twice as Hard" (2026)**: ND pracownicy wykonują **invisible cognitive labor** (masking, compensating). Miejsce na prywatne myślenie redukuje to obciążenie. ([Research Square](https://www.researchsquare.com/))

---

## Na co zwrócić uwagę — co nauka sugeruje do przyszłych decyzji

### MOCNE: Rób więcej tego

#### 1. Metacognitive feedback loop

**Gilbert (2023)** i metacognitive training study (2026): krótka interwencja metacognitive (5 prób z prediction + feedback) **poprawiła** calibration i reminder-setting.

Jeśli casedock w przyszłości pokaże użytkownikowi *"planowałeś 2h, zajęło 6h"* — to nie feature gadżet, to **evidence-based metacognitive training**. Mało kodu, duży impact.

#### 2. Energy/fatigue awareness

**Rosenberg (2023)**: ADHD performance jest **differentially sensitive** do cognitive load w zależności od stanu. **AttentionGuard (2026)** modeluje 4 stany: Focused, Drifting, Hyperfocused, Fatigued — i adaptuje UI.

Casedock nie musi robić mood trackera, ale lekki **"how are you today"** indicator który wpływa na to ile Cases jest suggested — to ma backing.

#### 3. Completion rituals / shutdown

**Leroy (2009)**: attention residue jest silniejsze gdy zadanie jest **nieukończone**. Jeśli casedock ma explicit "end of day" moment który zamyka otwarte Cases — to redukuje residue i improves next-day start.

Plan→Work→Shutdown rhythm (inspirowane Locu) nie jest kosmetyczny — to **attention residue management**.

#### 4. "Why this matters" field

Sonuga-Barke's dual pathway: **delay aversion** jest mniejszy gdy zadanie ma **perceived value**. Opcjonalne pole "dlaczego to ważne" na Case nie jest bureaucracy — to **activation support**.

---

### UWAŻAJ: Potencjalne pułapki

#### 5. Nie za dużo konfiguracji

**Amazing Marvin** (z competitor analysis) to warning: **too much flexibility = another form of overwhelm.** **Durand (2020)** potwierdza: problem nie jest w braku strategii, ale w persistence. Więcej opcji = więcej decisions = więcej executive friction.

Zasada: każdy nowy toggle/setting musi przejść test: **"czy to REDUKUJE decisions, czy je dodaje?"**

#### 6. Cognitive load vs perceptual load — balans

**Rosenberg (2023, MIT Press)** to **critical nuance**: cognitive load szkodzi ADHD, ale *zbyt mało* perceptual engagement może zostawić wolną uwagę na distractors.

Casedock powinien być:
- **Cognitively simple** — mało kroków, jasne akcje, mało decisions
- **Perceptually adequate** — nie pusty, wystarczająco bogaty żeby angażować attention

**"Calm" ≠ "boring".** "Calm" = low decision density, adequate visual texture.

#### 7. Nie rób gamification

**Spiel (2022, CHI)**: technology dla ADHD częściej frame'uje users jako "broken" i próbuje "naprawić" through gamified nudges. To jest **harmful**.

casedock już ma good instinct: *"no gamified microcopy, no over-enthusiastic tone."* Trzymaj się tego.

#### 8. Shame-aware design

**"I Work Twice as Hard" (2026)** i lived experiences study (2025): ADHD workers experience **frustration, stress, low occupational self-efficacy**.

Casedock powinien unikać:
- Empty states które mówią "nothing done today!" → shame
- Streak tracking → anxiety
- Time tracking bez context → guilt
- Porównywania ("you completed 3 cases this week, last week it was 7") → shame loop

Zamiast: *"Breathing room. You're here now."*

#### 9. Integrations jako plugins, nie identity

**Karr-Wisniewski & Lu (2010)**: **tools themselves can become a source of overload.** Jeśli ClickUp integration zalewa użytkownika 200 taskami — to betrays the whole premise.

Integrations muszą być:
- **Opt-in** — nigdy domyślnie włączone
- **Triage-first** — zadania z zewnątrz → Inbox → user decyduje
- **Nigdy nie auto-promote** do Case

---

### DO ZROBIENIA: Concrete next features z backing

#### 10. Weekly view / load awareness

Już w planie, ale z backingiem: ADHD users are **4.42x** bardziej likely to struggle z time management (**McDowall 2025**). Weekly lens = externalized time planning. To nie "nice feature" — to **core EF compensation**.

#### 11. AI-assisted triage i Case drafting

**Daley (2025, *Lancet Psychiatry*, 113 RCTs)**: structured psychological interventions work for adult ADHD. **Zhu (2026, CHI)**: AI może dostarczać cognitive scaffolding — ale jako **draft**, nie autonomous action.

To idealnie pasuje do casedock principle: *"AI as assistive operator, not spectacle."*

#### 12. Keyboard-first / fast capture

**McDowall (2025)**: ADHD devs **3.1x** more trouble z context switching. Każda sekunda capture → triage → case to executive friction. Keyboard shortcuts, quick capture modal, minimal clicks = less friction = higher compliance = more persistence.

---

## Bottom line

casedock jest **lepiej uzasadniony naukowo** niż większość produktów w tej kategorii. Nie dlatego że każdy feature ma random paper — ale dlatego że **core design principles** (calm, structured, bounded, scaffolded) mapują się bezpośrednio na to co research mówi o:

1. **Redukcji extraneous cognitive load** — Le Cunff 2024
2. **Compensating working memory deficits through external offloading** — Gilbert 2020
3. **Eliminating the ADHD-NT performance gap through scaffolding** — Greenwald 2024
4. **Reducing attention residue through bounded work units** — Leroy 2009
5. **Bridging the intention→action gap through structured choices** — Solanto 2011, Durand 2020

To nie jest "productivity app with ADHD label." To jest **evidence-based cognitive support tool** który coincidentally też jest dobrym task managerem. Ta narracja jest silniejsza niż "alternatywa dla Todoist."

---

*Pełna bibliografia z 59 pozycjami i 162 linkami: [`2025-05-neurodiversity-evidence-base.md`](./2025-05-neurodiversity-evidence-base.md)*

---

## Community Research Extension (June 2026)

Academic findings confirmed and extended by community-sourced research from Reddit ADHD communities (6 threads, 1000+ users). Key NEW insights not covered in academic literature:

| Community insight | Novelty |
|-------------------|---------|
| "Planning is dopamine" trap — ADHD users get dopamine from organizing, not doing | Not in clinical papers reviewed |
| App graveyard cycle — novelty decay drives 2-4 week abandonment pattern | Implicit in habituation research, not explicit |
| "Reverse todo" as shame antidote — writing accomplishments reduces avoidance | Novel UX pattern |
| Random task picker removes decision paralysis entirely | Not in clinical literature |
| Nightly "Your Day Tomorrow" email reduces morning paralysis | Novel behavioral intervention |

**Full community research**: [`2026-06-adhd-reddit-community-insights.md`](./2026-06-adhd-reddit-community-insights.md)
**15-point design principles**: [`docs/decisions/2026-06-09-adhd-design-principles.md`](../decisions/2026-06-09-adhd-design-principles.md)
