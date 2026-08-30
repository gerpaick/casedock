# casedock — Neurodiversity Research Summary

> Research synthesis: how scientific evidence supports the current features and what to consider
> in the future. Full bibliography with links:
> [`2025-05-neurodiversity-evidence-base.md`](./2025-05-neurodiversity-evidence-base.md)

---

## What the research says — in one sentence

casedock addresses a **real, well-documented problem**: more than 10% of developers experience
ADHD or similar patterns of executive dysfunction; standard tools such as Jira, ClickUp, and
Asana create cognitive overload that disproportionately burdens neurodivergent minds; and a
well-designed tool can **eliminate** the performance gap between users with ADHD and
neurotypical users.

---

## How the current features align with the evidence

### 1. Daily Focus (1 main + 2 secondary)

This is not a minimalist aesthetic choice — it is an **evidence-based intervention**.

- **Forster & Lavie (2014)**: restricting the perceptual field to relevant items **eliminates the
  distractibility gap** between people with ADHD and neurotypical people. When the number of
  items is limited, the ADHD brain is no more distracted than the neurotypical brain.
  ([DOI](https://doi.org/10.1037/neu0000020))
- **Le Cunff (2024)**: ADHD positively predicts extraneous cognitive load — visual noise costs
  the ADHD brain more. Showing three items instead of 50 reduces that cost.
  ([DOI](https://doi.org/10.3390/educsci14050516))
- **Kasper (2013)**: working-memory deficits in ADHD make mentally sorting 50 tasks unreliable.
  Three items fall within working-memory capacity.
  ([DOI](https://doi.org/10.1037/a0032371))

### 2. Calm UI / Quiet Chrome

- **Kasatskii (2023)**: a minimalist IDE interface produced a **35% reduction** in perceived
  distraction. Low perceptual load (two panels instead of seven) led to faster coding.
  ([DOI](https://doi.org/10.1007/978-3-031-35017-7_9))
- **Rosenberg (2023, MIT Press)**: an important nuance — cognitive load (decision complexity)
  **harms** people with ADHD, but some perceptual engagement can **help**. "Calm" does not mean
  empty. It means few decisions and little noise, with enough richness to sustain attention.
  ([DOI](https://doi.org/10.1162/netn_a_00341))
- **Weyerhäuser & Piccolo (2026)**: **both groups** (ADHD and neurotypical) benefited from an
  ADHD-friendly redesign — the curb-cut effect. Calm design does not exclude neurotypical users.
  ([DOI](https://doi.org/10.1007/978-3-032-05008-3_59))

### 3. Triage before commitment (Do now / Convert / Park / Waiting)

- **Scientific Reports (2026)**: ADHD involves **delayed goal-directed processing** — the brain
  prepares goals more slowly. When goals must be generated independently (an open task list),
  habitual responses dominate. Four clear, named actions provide an external goal structure
  that bypasses this delay. ([Nature](https://www.nature.com/srep/))
- **Durand (2020)**: people with ADHD **know** how to organize themselves — the problem is
  **persistence**. A tool that maintains the structure for the user is not "training"; it is
  compensation. ([DOI](https://doi.org/10.7717/peerj.9844))
- **Sonuga-Barke (2003, dual pathway)**: task avoidance may result from **delay aversion** (the
  task feels endless or unrewarding), not laziness. Triage creates bounded, named paths, each
  with an endpoint. ([DOI](https://doi.org/10.1016/j.neubiorev.2003.08.005))

### 4. Case as a bounded work unit (Spec + Decisions + Execution + Notes + Links)

- **Leroy (2009)**: **attention residue** — when switching from an unfinished task to a new one,
  some attention remains on the previous task. A Case as a closed unit (start → execution →
  done) reduces this residue. ([DOI](https://doi.org/10.1016/j.obhdp.2009.04.002))
- **Gilbert (2020)**: external reminders allow people with **lower working-memory capacity to
  catch up** with high performers. A Case that externalizes the entire context (decisions, notes,
  and execution state) provides complete cognitive offloading.
  ([DOI](https://doi.org/10.1037/xge0000652))
- **Greenwald (2024)**: scaffolding **eliminated** the comprehension gap between people with ADHD
  and neurotypical people. A Case provides that scaffolding structure.
  ([DOI](https://doi.org/10.1016/j.learninstruc.2024.102051))

### 5. Re-entry support (next step, recent decisions, summary)

- **Mark (2008)**: it takes **23 minutes** to regain focus after an interruption — for
  neurotypical people. It is probably worse for people with ADHD and working-memory deficits.
  ([DOI](https://doi.org/10.1145/1357054.1357072))
- **Koch (2023)**: resumption costs reflect **activation decay** — task goals naturally disappear
  from working memory during an interruption. Visible Case state externalizes those goals.
  ([DOI](https://doi.org/10.3758/s13421-023-01458-8))
- **McDowall (2025)**: a developer with ADHD said literally, *"5 seconds is forever. Whatever I
  was thinking is just gone."* Keeping the next step and recent decisions visible addresses this
  mechanism. ([PDF](https://people.cs.umass.edu/~mendres/papers/GetMeInTheGroove.pdf))

### 6. Private Notes

- **Morris (2015, Microsoft)**: most neurodivergent employees **do not disclose** their diagnosis
  at work for fear of judgment.
  ([PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/neurodiverse_tech_employees_assets2015.pdf))
- **Spiel (2022, CHI)**: technology research more often frames ADHD as a "problem to mitigate"
  than as a valid cognitive style. Private Notes provide a **safe space** — not monitoring,
  sharing, or "fixing." ([DOI](https://doi.org/10.1145/3491102.3517592))
- **"I Work Twice as Hard" (2026)**: neurodivergent employees perform **invisible cognitive
  labor** (masking and compensating). A place for private thinking reduces that burden.
  ([Research Square](https://www.researchsquare.com/))

---

## What to consider — implications for future decisions

### STRONG EVIDENCE: Do more of this

#### 1. Metacognitive feedback loop

**Gilbert (2023)** and a metacognitive training study (2026): a brief metacognitive
intervention (five trials with prediction + feedback) **improved** calibration and reminder
setting.

If casedock eventually tells a user, *"You planned for two hours; it took six,"* that is not a
gimmick. It is **evidence-based metacognitive training** with little code and high impact.

#### 2. Energy/fatigue awareness

**Rosenberg (2023)**: ADHD performance is **differentially sensitive** to cognitive load
depending on the person's state. **AttentionGuard (2026)** models four states — Focused,
Drifting, Hyperfocused, and Fatigued — and adapts the UI.

casedock does not need a mood tracker, but there is evidence for a lightweight **"how are you
today?"** indicator that affects how many Cases are suggested.

#### 3. Completion rituals / shutdown

**Leroy (2009)**: attention residue is stronger when a task is **unfinished**. An explicit
"end-of-day" moment in casedock that closes open Cases could reduce residue and improve the next
day's start.

A Plan → Work → Shutdown rhythm (inspired by Locu) is not cosmetic — it is **attention-residue
management**.

#### 4. "Why this matters" field

In Sonuga-Barke's dual-pathway model, **delay aversion** is lower when a task has **perceived
value**. An optional "why this matters" field on a Case is not bureaucracy — it is **activation
support**.

---

### CAUTION: Potential pitfalls

#### 5. Do not provide too much configuration

**Amazing Marvin** (from the competitor analysis) is a warning: **too much flexibility = another
form of overwhelm.** **Durand (2020)** confirms that the problem is not a lack of strategies but
persistence. More options = more decisions = more executive friction.

Rule: every new toggle or setting must pass this test: **"Does it REDUCE decisions or add
them?"**

#### 6. Cognitive load vs perceptual load — balance

**Rosenberg (2023, MIT Press)** provides a **critical nuance**: cognitive load harms people with
ADHD, but *too little* perceptual engagement may leave spare attention available for
distractions.

casedock should be:

- **Cognitively simple** — few steps, clear actions, and few decisions
- **Perceptually adequate** — not empty; rich enough to engage attention

**"Calm" ≠ "boring".** "Calm" = low decision density, adequate visual texture.

#### 7. Do not add gamification

**Spiel (2022, CHI)**: technology for people with ADHD often frames users as "broken" and tries
to "fix" them through gamified nudges. This is **harmful**.

casedock already has the right instinct: *"no gamified microcopy, no over-enthusiastic tone."*
Keep it that way.

#### 8. Shame-aware design

**"I Work Twice as Hard" (2026)** and a lived-experiences study (2025): workers with ADHD
experience **frustration, stress, and low occupational self-efficacy**.

casedock should avoid:

- Empty states that say "nothing done today!" → shame
- Streak tracking → anxiety
- Time tracking without context → guilt
- Comparisons ("you completed 3 Cases this week; last week it was 7") → shame loop

Instead: *"Breathing room. You're here now."*

#### 9. Integrations as plugins, not identity

**Karr-Wisniewski & Lu (2010)**: **tools themselves can become a source of overload.** If the
ClickUp integration floods the user with 200 tasks, it betrays the entire premise.

Integrations must be:

- **Opt-in** — never enabled by default
- **Triage-first** — external tasks → Inbox → user decides
- **Never automatically promoted** to a Case

---

### TO DO: Concrete next features supported by evidence

#### 10. Weekly view / load awareness

Already planned, now with supporting evidence: users with ADHD are **4.42 times** more likely to
struggle with time management (**McDowall 2025**). A weekly lens externalizes time planning. It
is not a "nice feature" — it is **core executive-function compensation**.

#### 11. AI-assisted triage and Case drafting

**Daley (2025, *Lancet Psychiatry*, 113 RCTs)**: structured psychological interventions work for
adults with ADHD. **Zhu (2026, CHI)**: AI can provide cognitive scaffolding — but as a **draft**,
not autonomous action.

This fits the casedock principle perfectly: *"AI as assistive operator, not spectacle."*

#### 12. Keyboard-first / fast capture

**McDowall (2025)**: developers with ADHD have **3.1 times** more trouble with context switching.
Every second spent moving from capture → triage → Case adds executive friction. Keyboard
shortcuts, a quick-capture modal, and minimal clicks mean less friction, higher compliance, and
greater persistence.

---

## Bottom line

casedock has a **stronger scientific foundation** than most products in this category. Not
because every feature has a random paper behind it, but because its **core design principles**
(calm, structured, bounded, scaffolded) map directly to what the research says about:

1. **Reducing extraneous cognitive load** — Le Cunff 2024
2. **Compensating for working-memory deficits through external offloading** — Gilbert 2020
3. **Eliminating the ADHD–neurotypical performance gap through scaffolding** — Greenwald 2024
4. **Reducing attention residue through bounded work units** — Leroy 2009
5. **Bridging the intention → action gap through structured choices** — Solanto 2011,
   Durand 2020

This is not a "productivity app with an ADHD label." It is an **evidence-based cognitive support
tool** that also happens to be a good task manager. This narrative is stronger than "an
alternative to Todoist."

---

*Full bibliography with 59 entries and 162 links:
[`2025-05-neurodiversity-evidence-base.md`](./2025-05-neurodiversity-evidence-base.md)*

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
