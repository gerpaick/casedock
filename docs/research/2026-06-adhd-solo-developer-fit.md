# casedock - ADHD Solo Developer Fit

Date: 2026-06-09
Status: research synthesis, not product contract
Scope: solo technical builders, solo programmers, independent consultants, and ADHD-leaning developers who carry many unfinished technical threads.

This document does not diagnose ADHD, promise treatment, or describe casedock as a medical intervention. It evaluates whether casedock's current product direction has a credible fit with ADHD-adjacent execution problems in solo software work.

Related local docs:

- Academic summary: `docs/research/2025-05-neurodiversity-summary.md`
- Evidence base: `docs/research/2025-05-neurodiversity-evidence-base.md`
- Community synthesis: `docs/research/2026-06-adhd-reddit-community-insights.md`
- ADHD design decision record: `docs/decisions/2026-06-09-adhd-design-principles.md`

Important caveat on Reddit/community evidence:

The local Reddit synthesis should be treated as community research, not as academic evidence and not as independently verified quotation-level evidence. Automated Reddit retrieval was unreliable. Use it for pattern generation, product hypotheses, and language sensitivity; do not use it as hard proof without manual source capture.

---

## Bottom line

casedock has a plausible and unusually coherent fit for ADHD-leaning solo developers, but the fit is narrower than "ADHD productivity app" and stronger than "task manager".

The strongest positioning is:

> Open casedock and know exactly what to do next, without reloading the whole project into your head.

The product should be understood as a personal execution layer for technical work:

- it catches incoming work before it becomes scattered,
- turns fuzzy work into a bounded Case,
- keeps context, decisions, private notes, source links, and execution state together,
- narrows the day to a small visible set,
- and helps the user resume by surfacing one concrete next move.

The most important product implication is that casedock should optimize for start/resume friction, not project-management completeness. The user does not primarily need another place to store tasks. They need a reliable recovery point after interruptions, avoidance, ambiguity, and context loss.

---

## Who this is for

### Primary ICP

Solo technical builders who:

- work across client work, side projects, product development, support, admin, and research;
- have too many partially open threads;
- receive work from many sources such as ClickUp, Jira, GitHub, email, Slack, notes, and memory;
- often know the project is important but cannot quickly answer "what is the next move?";
- lose time re-reading tickets, code, notes, and old decisions before restarting;
- are sensitive to shame, red overdue states, and productivity apps that feel like accountability theater;
- may identify with ADHD, executive dysfunction, neurodivergence, or "my brain works this way", without necessarily wanting a medicalized product.

### Secondary ICP

Neurotypical solo developers with similar constraints:

- context switching,
- client fragmentation,
- fragmented work intake,
- lack of external PM support,
- weak re-entry after interruptions,
- and too many partially documented decisions.

This is important because good ADHD-friendly design often behaves like a curb cut: the same simplification helps many non-ADHD users. The product should not require users to identify as ADHD to understand the value.

### Not the primary ICP

casedock is less likely to fit:

- teams needing shared project management,
- users who primarily want calendar/time-blocking,
- users who want a full life planner,
- users who want gamified habit tracking,
- users who need strict deadlines and external accountability workflows,
- users looking for an AI agent to autonomously decide priorities.

---

## Academic evidence

### 1. ADHD software engineers face real software-specific execution challenges

Liebel, Langlois, and Gama studied software engineers with ADHD and found challenges around task organization, estimation, attention, relationships, and health, while also identifying strengths such as creativity, puzzle-solving, and thinking ahead.

Source: Grischa Liebel, Noah Langlois, Kiev Gama, "Challenges, Strengths, and Strategies of Software Engineers with ADHD: A Case Study", 2023: https://arxiv.org/abs/2312.05029

Product implication:

- casedock should not frame the user as incapable;
- it should support strengths by preserving deep technical context and letting the user re-enter puzzle-solving mode faster;
- it should externalize organization and estimation pressure rather than asking the user to become more disciplined.

### 2. Stack Overflow data supports the interruption/waiting-answer problem

Verma, Cruz, and Liebel analyzed the 2022 Stack Overflow Developer Survey and compared neurodivergent and neurotypical professional engineers. Engineers with ADHD reported more difficulties, including interruptions caused by waiting for answers and less frequent interaction outside their team.

Source: Pragya Verma, Marcos Vinicius Cruz, Grischa Liebel, "Differences between Neurodivergent and Neurotypical Software Engineers: Analyzing the 2022 Stack Overflow Survey", 2025: https://arxiv.org/abs/2506.03840

Product implication:

- "Waiting" should remain a first-class but quiet state.
- Work should not disappear just because it is blocked.
- casedock should preserve the reasoning and next unblock action so that waiting does not become context loss.

### 3. Neurodivergent engineers need regulation of environment and practices, not just personal discipline

Gama et al. propose a socio-technical grounded theory around neurodivergent software engineers with ADHD and autism. Their work emphasizes how cognitive dysfunctions affect software engineering performance and how individual journeys and accommodations regulate that effect.

Source: Kiev Gama, Grischa Liebel, Miguel Goulão, Aline Lacerda, Cristiana Lacerda, "A Socio-Technical Grounded Theory on the Effect of Cognitive Dysfunctions in the Performance of Software Developers with ADHD and Autism", 2024: https://arxiv.org/abs/2411.13950

Product implication:

- casedock should be an accommodation-like work environment, not a discipline tracker.
- The product should adapt the work surface: fewer decisions, visible next action, private notes, neutral revisit prompts.
- The language should avoid "fix yourself" framing.

### 4. Task switching is costly in software development

Shakeri Hossein Abad et al. studied task interruption in software development and found that contextual factors such as interruption type, time of day, task type, and context affect disruptiveness. Their retrospective analysis found self-interruptions can be especially disruptive.

Source: "Task Interruption in Software Development Projects: What Makes some Interruptions More Disruptive than Others?", 2018: https://arxiv.org/abs/1805.05508

Related paper: "Two Sides of the Same Coin: Software Developers' Perceptions of Task Switching and Task Interruption", 2018: https://arxiv.org/abs/1805.05504

Product implication:

- The core unit should not be a task row; it should be a recoverable work context.
- The product should assume the user will be interrupted and should design for resumption, not ideal uninterrupted focus.
- "Where was I?" is a first-class product problem.

### 5. Adult ADHD task management tools often assume the wrong model of self-regulation

Chen, Meng, and Nie argue that adult ADHD task management is not just an individual willpower problem. Existing productivity tools often assume stable self-regulation and linear time. Their study points toward socially and emotionally scaffolded strategies and AI-augmented support.

Source: Jingruo Chen, Yibo Meng, Kexin Nie, "'Not Just Me and My To-Do List': Understanding Challenges of Task Management for Adults with ADHD and the Need for AI-Augmented Social Scaffolds", 2026: https://arxiv.org/abs/2603.17258

Product implication:

- casedock should not depend on the user remembering to maintain a system.
- It should auto-surface the most resume-worthy work.
- AI, if added, should scaffold the user's next step and context recovery, not become autonomous decision-making.

### 6. Assistive technology for adult ADHD is still underdeveloped for positive daily work support

Tan et al.'s scoping review selected 46 papers from 3,538 search results and found that much ADHD technology research is therapeutic/intervention-oriented rather than oriented toward positive everyday support for adults.

Source: Valerie Tan, Luisa Jost, Jens Gerken, Max Pascher, "Preliminary Results of a Scoping Review on Assistive Technologies for Adults with ADHD", 2026: https://arxiv.org/abs/2601.21791

Product implication:

- There is room for non-medical, workplace-oriented support tools.
- casedock should avoid clinical claims while still using evidence-informed design.
- "ADHD-friendly productivity support" is safer and more accurate than "ADHD treatment".

### 7. ADHD-specific developer tools are emerging but not yet validated

Tether is an LLM-powered desktop application proposed for software engineers with ADHD. It combines local activity monitoring, retrieval-augmented generation, and gamification. The paper says target-user evaluation is still future work.

Source: Aarsh Shah, Cleyton Magalhaes, Kiev Gama, Ronnie de Souza Santos, "Tether: A Personalized Support Assistant for Software Engineers with ADHD", 2025: https://arxiv.org/abs/2509.01946

Product implication:

- The category is becoming legible: ADHD-aware tools for software engineers are no longer speculative.
- casedock should differentiate from Tether-like assistants by being calmer, less surveilling, less gamified, and more explicit about user agency.
- Avoid OS-level monitoring and gamification in v1; they are riskier than a simple user-owned workbench.

---

## Software-developer-specific evidence

The strongest casedock fit appears where ADHD traits intersect with software work mechanics.

### 1. Context is expensive to rebuild

Software work is not just a sequence of visible tasks. A developer needs:

- what was tried,
- what was decided,
- why the code changed,
- what remains uncertain,
- which external issue or message triggered the work,
- which branch/file/test/error matters,
- and what the next concrete move is.

Generic task managers usually store only the task title, status, deadline, and maybe comments. That is not enough for re-entry.

casedock's Case model is valuable because it groups:

- spec context,
- decisions,
- execution items,
- private notes,
- source links,
- status,
- focus assignment.

Fit: high.

Risk: if the Case page opens with too much context before one next action, the product becomes a notebook rather than a resume engine.

### 2. Task switching creates hidden tax

Software developers often switch between:

- coding,
- debugging,
- reviewing,
- waiting for answers,
- writing notes,
- reading docs,
- answering client messages,
- handling deployment/admin work.

For ADHD-leaning users, the self-interruption loop can be especially damaging: a thought appears, the user follows it, the original work context decays, and returning requires a costly reload.

casedock's role is to reduce that reload. The product should not try to prevent all switching. It should make switching survivable.

Fit: high.

Product principle:

> Every Case should answer: what was this, where did I leave it, and what is the first move now?

### 3. External task tools do not map to actual work

A ClickUp/Jira/GitHub issue might say:

- "Fix auth bug",
- "Investigate webhook retries",
- "Add invoice export",
- "Improve onboarding".

But the developer still needs to privately determine:

- what is actually wrong,
- what is in scope,
- what is out of scope,
- what evidence exists,
- what the first probe should be,
- what not to forget.

casedock can win by being the personal interpretation layer between external assignment and real execution.

Fit: very high.

Positioning:

> casedock is not a replacement for ClickUp/Jira/GitHub. It is the private layer where assigned work becomes understandable work.

### 4. Waiting and ambiguity are especially corrosive

Waiting for answers creates a limbo state. The work is not done, but it is not actionable. When the answer arrives, the user has to reconstruct the entire context.

casedock should preserve:

- why the work is waiting,
- what answer is needed,
- what to do when the answer arrives,
- and what was already decided.

Fit: high.

Avoid:

- punitive waiting age,
- red blocked states,
- "late" copy,
- unresolved counters that feel like guilt.

Use:

- neutral "Waiting",
- "Last touched X days ago",
- "Worth revisiting",
- visible first move.

### 5. Estimation is weak fit for v1

The research and local ADHD principles strongly caution against requiring time estimates. ADHD users often struggle with time estimation, and software work has inherent uncertainty.

casedock should not require:

- due dates,
- time estimates,
- story points,
- planned duration,
- urgency scoring.

Fit for required estimation: low.

Fit for lightweight effort labels already present in casedock: moderate, only if optional and not central.

### 6. Reverse todo/accomplishment view has strong emotional fit

ADHD-friendly design should reduce shame and support re-entry. A weekly "Moved forward this week" panel can show evidence of progress without turning it into a streak or leaderboard.

Fit: high.

Constraints:

- no streaks,
- no comparison against last week,
- no red missed-day language,
- no points,
- no "you failed to".

---

## Community research caveats

The local community synthesis identifies useful patterns:

- task initiation is the key pain, not merely task storage;
- planning can become a dopamine trap;
- flat lists create paralysis;
- shame destroys return behavior;
- capture must be one-field fast;
- out-of-sight work disappears;
- reverse todo/accomplishment framing may reduce avoidance.

However:

- not all Reddit claims were directly verified;
- some quotations in the local file should not be used externally without manual source capture;
- community patterns should generate hypotheses, not final product truth;
- they should be cross-checked against user interviews and behavioral data.

Practical use:

- safe for internal product thinking;
- safe for UX heuristics;
- not safe for marketing as "research proves Reddit users say...";
- not safe for academic-style citation unless manually verified.

---

## Product fit matrix

| User pain | Evidence strength | Current casedock fit | Gap | Priority |
|---|---:|---:|---|---:|
| Context loss after interruption | High | High | First visible action must be stronger | P0 |
| Task initiation paralysis | High | Medium | Case detail should lead with first unfinished ExecutionItem | P0 |
| Too many active threads | High | Medium | Active list should fold after about 7-10 Cases | P0 |
| Incoming work scattered across tools | High | High | Integrations must remain opt-in and triage-first | P1 |
| Waiting for answers destroys momentum | Medium-high | Medium | Waiting state needs clearer re-entry prompt | P1 |
| Shame from overdue/red states | High | Medium-high | Replace stale language with neutral revisit language | P0 |
| Planning trap/list maintenance | Medium-high | Medium | Avoid configuration, complex metadata, and list grooming | P1 |
| Need for private thinking space | Medium-high | High | Keep private notes local/user-controlled by default | P1 |
| Desire for AI scaffolding | Emerging | Low | Add only after manual flow is excellent | P2 |
| Medical/therapeutic ADHD support | Low fit | Low | Do not pursue | Reject |

---

## What casedock already gets right

### 1. Case as the core object

This is the most important strategic choice. "Case" is broader than "task" and more bounded than "project". It can hold ambiguity without becoming a life-management system.

For ADHD solo developers, this is useful because the work unit is rarely just a checkbox. It is a cluster of context, decisions, and partial execution.

### 2. Inbox before Case

Inbox lets the user capture before organizing. This matches the ADHD-friendly principle that capture and organization are different cognitive modes.

The current direction is strong if capture remains:

- one main field,
- zero required metadata beyond title,
- no due date,
- no required category,
- no forced project selection.

### 3. Daily Focus: one main, two secondary

This is one of the strongest product choices. It constrains the visual field and reduces daily decision load.

The principle should remain:

- one main Case,
- up to two supporting Cases,
- no gamified score,
- no "you failed yesterday",
- no large dashboard.

### 4. Private notes

Private notes are not a minor feature. They allow the user to keep messy reasoning, uncertainty, and emotional context without exposing it to external systems.

For developers who work in client/team tools, this can be a major differentiator:

> The external tracker gets the professional artifact. casedock gets the private thinking that makes the work possible.

### 5. Source links as supporting context

Source links should stay linked but not dominant. ClickUp/Jira/GitHub/email should be inputs, not the product center.

---

## Biggest gaps

### Gap 1: The first visible thing must be an action

The current strategic risk is that casedock can become a beautiful context archive. That is useful, but insufficient for ADHD fit.

When a user opens a Case, the first question is not:

> What is all the context?

It is:

> What can I do now?

Then, if needed:

> What context do I need to do it?

Research-backed recommendation:

- Surface the first unfinished ExecutionItem as "Just Start".
- Put "Mark done" and "Open context" near it.
- If no ExecutionItem exists, show one action: "Define first move".
- Keep the full execution list lower on the page.

### Gap 2: Active work must be folded

The board should never become a full active backlog. Flat lists with 14+ items undermine the product's ADHD promise.

Recommendation:

- Board: Focus + max 3 revisit candidates + navigation links.
- Active view: sorted and folded after 7-10 visible Cases.
- Sorting: focus first, actionable/fresh next, revisit-later last.

### Gap 3: "Stale" language is risky

The stale concept is useful. The word "stale" is product-internal and can read as blame when surfaced.

Recommendation:

- User-facing label: "Worth revisiting".
- Supporting copy: "Last touched X days ago."
- Visual style: neutral grey/quiet, never red.

### Gap 4: Conversion flow should not front-load metadata

Inbox-to-Case conversion should ask for:

- title,
- outcome,
- first move.

Advanced fields such as clarity, work type, and effort can exist, but they should not be required as the primary path.

### Gap 5: Completion needs a calm feedback loop

The product should help the user see movement without creating a scoreboard.

Recommendation:

- "Moved forward this week" panel.
- Show completed Cases and completed ExecutionItems.
- No streaks.
- No comparisons.
- No points.

---

## Product implications

### Core promise

Use this internally:

> Open casedock and know exactly what to do next, without reloading the whole project into your head.

Shorter positioning variants:

- "Know what to do next when you come back."
- "A calm execution layer for too many technical threads."
- "Turn scattered work into one next move."
- "For solo developers with too many threads open."

Avoid:

- "ADHD treatment"
- "cure procrastination"
- "fix executive dysfunction"
- "never miss a task again"
- "AI project manager"
- "replace Jira"

### Product identity

casedock should be:

- personal,
- calm,
- private,
- technical-work aware,
- context-preserving,
- action-first.

casedock should not be:

- a generic todo app,
- an enterprise PM platform,
- a medical app,
- a gamified habit tracker,
- an autonomous AI agent,
- a full life planner.

### UX decision rule

For each UI feature:

1. Does it reduce the number of decisions?
2. Does it make the next move more visible?
3. Does it preserve context for re-entry?
4. Does it avoid shame and guilt?
5. Does it require maintenance after novelty fades?

If a feature fails 1, 2, and 5, it is probably not a fit.

---

## Rejected directions

### 1. Full ADHD life planner

Reason to reject:

- too broad,
- crowded category,
- weaker developer-specific differentiation,
- higher emotional/medical expectation,
- more likely to require routines, habits, mood, calendar, medication, and personal life workflows.

### 2. Task manager with ADHD branding

Reason to reject:

- generic task apps already exist,
- many have stronger mobile/calendar ecosystems,
- free/open-source competition is strong,
- ADHD branding without workflow difference is shallow.

### 3. Heavy gamification

Reason to reject:

- shame risk,
- novelty decay risk,
- local ADHD design principles forbid points, XP, streaks, leaderboards, and similar mechanics,
- Tether already explores gamified support; casedock can differentiate by being calmer.

### 4. Time-estimation-first planning

Reason to reject:

- ADHD users often struggle with time estimation;
- software work is inherently uncertain;
- estimates can become friction and shame;
- better to support first move, context, and progress evidence.

### 5. Autonomous AI workflow decisions

Reason to reject:

- product boundary says AI must not make autonomous sync/workflow/product decisions;
- privacy and trust risks are high;
- user agency is core to casedock;
- AI is better as a drafting/scaffolding layer.

### 6. Integration-first positioning

Reason to reject:

- ClickUp/Jira/GitHub are inputs, not the identity;
- integration-first invites feature-count comparison;
- the unique value is private context recovery and execution shaping.

---

## Competitive interpretation

### Amazing Marvin

Amazing Marvin validates personal productivity tools that acknowledge different working styles instead of forcing a single methodology.

Source: https://amazingmarvin.com/pricing/

Implication:

- a strong, opinionated product philosophy can carry a tool in this category;
- simplicity fits ADHD-friendly positioning;
- casedock should not compete by feature count with Marvin.

### Leantime

Leantime explicitly positions around neurodivergent work management. Its product philosophy argues that a single all-inclusive offer avoids cognitive overhead and feature-table decision load.

Source: https://leantime.io/pricing/

Implication:

- reducing plan-like decision load can be part of the product design;
- casedock can borrow the simplicity, but not the team/project-management scope.

### Lunatask

Lunatask is a privacy-focused personal productivity app with a simple, low-cost offer.

Source: https://lunatask.app/pricing

Implication:

- casedock's differentiation is developer-specific context recovery, not generic planning features.

### Tiimo

Tiimo validates neurodivergent-friendly visual planning as a mainstream category. Its official site emphasizes visual planning, executive functioning support, and AI task breakdown.

Source: https://www.tiimoapp.com/

Implication:

- the category has consumer pull;
- casedock should avoid becoming a daily-life visual planner;
- its niche is technical work context, not routines.

### Super Productivity

Super Productivity is free, open source, local-first, and developer-friendly. It includes tasks, time tracking, focus tools, integrations, offline privacy, and keyboard-first workflows.

Source: https://super-productivity.com/ and https://super-productivity.com/pricing/

Implication:

- casedock cannot win on generic developer task features;
- it must win on Case/context recovery, private shaping, and lower cognitive friction.

---

## Falsifiable hypotheses

These should be tested before expanding scope.

### H1: Case context recovery is more valuable than task storage

Signal:

- users return to casedock after an interruption and say it helped them restart faster;
- users create fewer but richer Cases than generic tasks;
- users mention "I knew where I left off" unprompted.

Failure signal:

- users treat it as another backlog;
- Cases become stale archives;
- users still go back to ClickUp/GitHub/email to understand what to do.

### H2: First unfinished ExecutionItem is the right primary prompt

Signal:

- users mark execution items done from the Case page;
- users create first moves during conversion;
- users say "Just Start" reduces resistance.

Failure signal:

- users ignore ExecutionItems and only use spec/private notes;
- first moves become vague ("work on it");
- users want a different next-action source.

### H3: Board folding reduces avoidance

Signal:

- users open board more often;
- users do not ask for "show everything" as default;
- users move through focus/revisit surfaces without scanning a long list.

Failure signal:

- users feel hidden work is unsafe;
- users create duplicate Cases because folded work is invisible;
- users need stronger search or resurfacing.

### H4: Context recovery is the core differentiator

Signal:

- users describe casedock as the place they go to resume work, not to store tasks;
- willingness to keep using it is tied to fewer restarts, not task count;
- users compare casedock to losing half an hour reloading context, not to Todoist.

Failure signal:

- users treat it as interchangeable with free task managers;
- users cannot name a painful enough problem.

---

## Validation questions for interviews

Use these with solo developers who identify with ADHD/executive-friction patterns. Do not ask first whether they want an ADHD app. Ask about work behavior.

1. Tell me about the last time you returned to a technical task after a few days away. What did you have to re-read?
2. Where does incoming work arrive for you right now?
3. What do you do when a task is too vague to start?
4. What is the difference between a task you can start immediately and one you avoid?
5. What do you store privately that would never go back into ClickUp/Jira/GitHub?
6. How many active technical threads can you keep visible before you stop looking?
7. What does your current system do when something waits on another person?
8. What productivity app did you stop using after a few weeks? Why?
9. When you finish something, where does that evidence go?
10. If casedock saved you one restart per week, what would that change for you?

Strong-fit answers:

- "I had to read everything again."
- "The ticket was not the real work."
- "I knew it mattered but not where to begin."
- "I needed one first move."
- "I keep private notes because the external tracker is too public."
- "Long lists make me close the app."

Weak-fit answers:

- "I just need a better calendar."
- "My project manager already keeps everything clear."
- "I mostly need team dashboards."
- "I want automatic prioritization without deciding."
- "I want gamification/streaks."

---

## Research conclusion

casedock's product-market fit is plausible if the product stays narrow:

> solo technical work, private context recovery, one visible next move.

The strongest evidence supports:

- bounded work objects,
- low decision density,
- visible next action,
- context preservation,
- neutral revisit prompts,
- private notes,
- triage-first intake,
- no shame mechanics.

The weakest directions are:

- generic todo features,
- full life planning,
- complex metadata,
- gamification,
- time estimation,
- integration-first positioning,
- autonomous AI.

The product should move from "calm workbench" toward "calm start/resume engine" without losing the quiet, text-first identity.

