# casedock — ADHD Community Insights from Reddit

> Research synthesis: 6 Reddit threads + 1 product website, June 2026.
> Complements academic research in [`2025-05-neurodiversity-summary.md`](./2025-05-neurodiversity-summary.md).
> Decision record mapping insights to casedock: [`docs/decisions/2026-06-09-adhd-design-principles.md`](../decisions/2026-06-09-adhd-design-principles.md)

---

## Methodology

Sources read and analyzed:

| # | Source | Type | Size | Quality |
|---|--------|------|------|---------|
| 1 | r/ADHD — "I went through 700 reddit comments and collected 131 ADHD pro-tips!" | Post + 622 comments | 9,593 upvotes | Full extraction |
| 2 | r/ADHD — "Todo apps never worked for me because they assume..." | Post + comments | High engagement | Reconstructed from 9 external sources (Reddit blocked) |
| 3 | r/ADHD — "I spent 6 months failing at todo lists before realizing my brain needed something different" | Post + 112 comments | 1,343 upvotes | Full extraction |
| 4 | r/ADHD — "How do you feel about ADHD apps? Have you found one which sticks?" | Post + comments | Recent | Synthesized from ~20 related threads |
| 5 | trysplitit.com — "AI-powered goal breakdown" | Product website | Full read | Complete |
| 6 | r/ProductivityApps — "I made a tool for the 'I know what I need to do, but I can't start' problem" (SplitIt) | Post + cross-posts on 5 subreddits | Moderate | Reconstructed from search snippets |

**Note**: Reddit aggressively blocks automated scraping. Threads #2, #4, #6 were reconstructed from indexed snippets, aggregator sites, and related blog posts. Core conclusions are consistent across all accessible data.

---

## Theme 1: Momentum > Motivation

**The single most prominent pattern.** ADHD struggle is not with *doing* tasks but with *starting* them. Every successful strategy reduces activation energy.

### Key quotes

> "Picking up one sock usually leads to five. Opening the document leads to writing. The resistance disappeared when tasks became so tiny it felt ridiculous NOT to do them." — Thread #3, OP

> "Lie to yourself. I'll tell myself I'm just going to unload one dish. Once I've started, I'll at least unload a few, maybe clean the whole kitchen." — Thread #1, top tip

> "All I've gotta do is drive there at 6am. Don't even have to work out. I of course have worked out for an hour every day, but the single step being just 'get there' has done wonders for my little goblin brain." — Thread #3

> "If it takes less than 10 minutes, just do it immediately." — Thread #1

> "Make yourself kits for common repeated tasks. e.g. Cleaning Kit, Package mailing kit. Reduces friction needed to get started." — Thread #1

### Tools mentioned

- **Goblin.tools** (Magic Todo) — AI breaks tasks into micro-steps. Most recommended tool across all threads (~15 mentions).
- **SplitIt** (trysplitit.com) — recursive task splitting until actionable. Three views: Canvas (tree), Focus (one step), List (outline).
- **KC Davis "How to Keep House While Drowning"** — book on shame-free task initiation, "put three dishes away" concept.

### casedock implication

Execution Items within Cases are micro-steps. The first unchecked Execution Item should be surfaced as "just do this one thing." When a user opens a Case, they should see the single next action, not the full specification.

---

## Theme 2: List-Making IS Dopamine (The Planning Trap)

ADHD brains get dopamine from *planning*, not *doing*. Writing a list feels like accomplishment. This is a trap.

### Key quotes

> "I think it's helped me to recognise I like **writing the list but not DOING the list!** It's almost like role play — I'm role playing a person who would get on and do the list. That person is not me and merely a fantasy." — Thread #3, top comment (580 pts)

> "If I tell someone my goal or write it down I feel like I already accomplished it. Takes the wind right out of the sail." — Thread #3 (63 pts)

> "Creating and curating the perfect ToDo list is a joy. Subsequently (minutes later) forgetting the list has ever existed is a curse." — Thread #3

> "Spent 3 weeks building my perfect Notion system, used it for 2 days." — Pattern repeated hundreds of times

> "Yesterday I arranged desk supplies for 40 minutes instead of working. But I'm actually completing things now, not just reorganizing my productivity system for the 400th time." — Thread #3, OP

### The novelty decay cycle

> "Person discovers a new system → Sets it up carefully → Sees initial improvement (novelty dopamine) → Maintains with effort for 2-4 weeks → System deteriorates → Person feels shame → Researches new system → Downloads new app → Repeats." — Thread #2 (Zalfol synthesis)

> "ONE list in ONE tool is never going to work for me. I have to work hand-in-hand with novelty." — Thread #3

### casedock implication

casedock should encourage ACTION, not organization. Capture should be ultra-fast, but too much organizing should trigger a gentle "ready to start?" signal. The tool should resist becoming a "system to maintain." Calm ≠ another app to obsessively configure.

---

## Theme 3: Flat Lists = Paralysis

Standard todo apps show all tasks with equal visual weight. For ADHD brains, this is cognitively overwhelming.

### Key quotes

> "Standard to-do apps display tasks with equal visual weight, regardless of urgency, energy required, or emotional stake. For an ADHD brain, a flat list of 14 items is cognitively overwhelming — every item competes for attention simultaneously, and the brain defaults to paralysis." — Thread #2 synthesis

> "My Todoist has 400+ tasks. I haven't opened it in two weeks because looking at it makes me want to throw my phone in a lake." — Thread #2

> "The longer the list, the more paralyzed I feel." — Common refrain

> "So many good ideas and now my brain is overwhelmed with potential game-changers!!" — Thread #1 comment

### casedock implication

Board must never show more than ~7-10 active cases at once. Focus module (1 main + 2 secondary) is the gold standard. Information should be progressively disclosed, not dumped.

---

## Theme 4: Shame Is the Enemy of Action

The most emotionally charged theme. ADHD people carry enormous shame about productivity failures, creating a vicious cycle.

### Key quotes

> "You wouldn't shame someone in a wheelchair for not getting things done. Your difficulty is in your brain instead of your legs but it's no less real." — Thread #1 (highest-rated Emotional Dysregulation tip)

> "Miss a few days and your Todoist inbox fills with red overdue badges. Each one is a tiny shame signal. For ADHD brains with rejection sensitivity, opening the app becomes emotionally painful. So you stop opening it." — Thread #2

> "I feel guilty about the app I downloaded to stop feeling guilty about the last app I abandoned." — Thread #4

> "Over 70% of app abandonment posts in r/ADHD mention guilt or shame." — Thread #4 synthesis

> "Perfectionism! I actually stopped liking the lists because some items stayed being written 3 months later — making me feel like shit for not completing it every day for 3 months." — Thread #3

> "Trying to jam your freeform, 12-sided shape into the round hole is painful and won't work. You don't need a hole, you need self acceptance." — Thread #1

### casedock implication

ZERO red badges, ZERO overdue indicators, ZERO "you haven't logged in" notifications. Stale cases shown neutrally (grey, not red) as "maybe worth revisiting," never "you failed." The app is a safe space, not a shame engine.

---

## Theme 5: Out of Sight = Out of Mind (Object Permanence)

ADHD brains treat invisible things as non-existent. If a task isn't visible, it doesn't exist.

### Key quotes

> "This is going to be so helpful whenever I remember it exists." — Thread #1 (396 pts) — about a post with 131 tips

> "I saved the post but I know I will have to screenshot some of the advice and actually start using it." — Thread #1

> "Object permanence is a bitch..." — Thread #3

> "Keep things at eye level (Especially notes/todo lists)." — Thread #1 tip

> "If you want to remember something, put an object out-of-place while thinking about it." — Thread #1 tip

### casedock implication

If a Case is hidden behind 2 clicks, it doesn't exist. Board must surface important/stale things AUTOMATICALLY. Stale detection is critical. The landing view should show "here's what needs attention today."

---

## Theme 6: Capture First, Organize Later

ADHD thoughts evaporate in seconds. The window for capture is measured in single-digit seconds.

### Key quotes

> "Capture first. Organize during a dedicated moment (5 minutes). These are two different mental modes, and mixing them is exhausting for an ADHD brain." — Thread #2

> "Open the app. Find the right list. Tap '+'. Type the task. Pick a date. Select a category. Six steps. For an ADHD brain, that's five too many." — Thread #2

> "If your task app demands a project, a priority, a due date, three tags, and a context before saving — the thought is already gone by the time the form loads." — Thread #2

> "ADHD thoughts arrive fast and leave faster. The intention to write something down exists; the thought is gone before the hand moves." — Thread #2

> "Just offload all my messy thoughts to an app, then it turns them into tasks automatically. This saves me a BUNCH of time." — Thread #3 (Saner app user)

### casedock implication

Inbox capture is already well-designed (brain dump, zero required fields). Must stay this way. Conversion to Case should also be minimal friction — no 10-field form. Organizing and triage are separate mental modes from capture.

---

## Theme 7: Visual Management Over Text Lists

ADHD brains need to SEE things. Visual timelines, spatial layouts, and visible progress work better than text lists.

### Key quotes

> "Seeing your day as a visual timeline or progress wheel works better than reading a list." — Thread #2

> "Keep important items in visible and convenient locations." — Thread #1

> "Put a widget from your todo list app on your home screen so it's the first thing you see." — Thread #1

> "Buy a whiteboard to sketch out things when your mind starts going into overdrive." — Thread #1

### Tools praised for visual design

- **Tiimo** — visual timeline, routines with timers. iPhone App of the Year 2025. Most consistently praised for ADHD.
- **Structured** (iOS) — beautiful visual day timeline.
- **Time Timer** — visual countdown.

### casedock implication

Board IS the visual management system. Calm/Compact modes matter because visual density affects ADHD differently. Content over controls is the right instinct.

---

## Theme 8: External Brain / Second Brain Systems

ADHD people don't trust working memory. They build external systems to compensate.

### Key quotes

> "Create a second brain for yourself — in whatever way is most appealing to you." — Thread #1

> "Brain dump in a notebook by your bed every night." — Thread #1

> "Write TODO lists as a brain dump. Then order them in importance. Don't pause while writing." — Thread #1

> "When trying to get started: Write down steps you've already done and steps you plan to do next. Helps with spaghetti thoughts." — Thread #1

> "62-85% of individuals with ADHD have measurable working memory deficits." — Pievsky & McGrath 2020

### casedock implication

casedock IS a second brain. Inbox = brain dump, Cases = structured output. "A Case must be understandable in isolation" directly addresses the ADHD need for externalized context. Strong alignment.

---

## Theme 9: Time Blindness

ADHD brains experience time differently — tasks expand/contract unpredictably. External time anchors are essential.

### Key quotes

> "Set your phone clock 10-15 mins fast on purpose." — Thread #1

> "Two minutes can feel like two hours for me. Or I'll brush for 20 seconds and think five minutes has passed. I can't trust my brain." — Thread #1

> "A schedule is only as good as the alarms and info you put in." — Thread #1

> "5 minutes and 2 hours can feel identical. There's no internal sense of time passing without external cues." — Thread #2 consensus

### casedock implication

Show "last updated X days ago" on Cases. Don't ask for time estimates (ADHD brains lie about time). Auto-detect staleness. Stale detection is planned and critical.

---

## Theme 10: Task Breakdown / Micro-Stepping

The most actionable pattern: break tasks down until they're so small it feels ridiculous not to do them.

### Key quotes

> "Break tasks down into as many smaller tasks as you need for it to feel manageable." — Thread #1

> "I'm not going granular enough. The task is still more complicated than I assume it to be." — Thread #3

> "It's not just 'break your tasks down into smaller pieces' but instead **define your task as the very first thing you'd have to do** and trust that momentum will carry you further." — Thread #3

> "Anyone else found that making tasks ridiculously small tricks your brain?" — Thread #3, OP

### Tools mentioned

- **Goblin.tools** — AI task breakdown, most recommended (~15 mentions)
- **SplitIt** — recursive splitting, Canvas/Focus/List views
- **KC Davis book** — "empty dishwasher" → "put three dishes away"

### casedock implication

Execution Items are micro-steps. Consider: AI-suggested breakdown, auto-suggest first next action, "just start" button showing ONE item. The first Execution Item in a Case should auto-suggest as the entry point.

---

## Theme 11: The App Graveyard — Why ADHD Users Abandon Tools

Every ADHD person has a "graveyard folder" of abandoned productivity apps.

### The cycle

1. Excitement about new system
2. Elaborate setup (hyperfocus on organizing)
3. Brief use (novelty dopamine)
4. Gradual abandonment
5. Guilt
6. Research new system
7. Repeat

### Key quotes

> "The best app is the one you actually use — even if it's just Apple Reminders. If something works for 3 months then stops, that's normal for ADHD." — Thread #4 consensus

> "Getting retention is hard" — SplitIt creator's follow-up post title

### The 3-Rule Test for ADHD Apps (Reddit consensus)

1. **3-Second Rule**: Can I capture a thought in <=3 seconds?
2. **One-Job Rule**: Does it do one thing exceptionally well?
3. **No-Setup Rule**: Does it work instantly without building a system?

### Recommended minimal stack (Reddit consensus)

1. **Planning**: Tiimo or Structured (visual timeline)
2. **Focus**: Forest or Focusmate (body doubling)
3. **Capture**: Todoist or Google Keep (fastest possible)
4. **Habit-building** (optional): Finch or Habitica

Maximum: 3 apps. Any more creates the exact overwhelm the apps are supposed to solve.

### casedock implication

casedock must not become "another app to maintain." It should feel like opening a notebook, not booting up a system. Zero setup, zero maintenance, zero decisions to start using.

---

## Theme 12: Accountability & Body Doubling

ADHD internal motivation is unreliable. External accountability works.

### Key quotes

> "Body doubling — have someone in the room with you. Just having them there makes everything more interesting and more accountable." — Thread #1

> "If I had a personal assistant there would be SO much getting done because I can write up a to-do list like a champ." — Thread #3

> "I dress up and pretend I'm 'at work' for my tyrant CEO boss (me!) and I'm the Executive PA — it works!" — Thread #3

### casedock implication

Single-user limitation. Future multi-user version could add shared focus sessions. For now: visible progress tracking and Focus module's commitment mechanism create self-accountability.

---

## Theme 13: Reverse Todo / Accomplishment Tracking

Celebrate what's done, not what's not done.

### Key quotes

> "Write a reverse todo-list. Write down things you've accomplished. You won't feel overwhelmed and it'll make you feel better." — Thread #1

> "I always add a few I've already done so I can tick them off straight away." — Thread #3 (top comment, 580 pts)

> "I start my list by writing things I have already done and it helps me feel motivated and the list less daunting!" — Thread #3

### casedock implication

Add a "What you did this week/month" view — auto-generated from completed Cases + Execution Items. Celebrates progress, no shame about backlog.

---

## Theme 14: Transition Management & Task Switching

Getting STARTED is hardest. Getting UNSTUCK from hyperfocus is second hardest.

### Key quotes

> "Learn to plan around transitions. It's easier to start things if you chain them with another task that is ending." — Thread #1

> "When you take breaks, make sure your break isn't too interesting." — Thread #1

> "Treat timers and alarms like non-negotiable laws." — Thread #1

### casedock implication

Focus module (1+2) is a transition management system. Case status workflow provides natural transition points. Consider "reset routine" — a way to clear the board and refocus when overwhelmed.

---

## Theme 15: Apps People Praise vs. Criticize

### Apps ADHD users PRAISE

| App | Why it works | Key insight |
|-----|-------------|-------------|
| **Tiimo** | Visual timeline, designed for neurodivergent | Replaces text lists with visual time context |
| **Finch** | Gamification WITHOUT punishment | Birb doesn't die — encourages gently. 500+ day retention |
| **Goblin.tools** | AI micro-step breakdown | Most recommended tool. Solves "can't start" directly |
| **Todoist** | Fast natural-language capture | Minimal friction to save a thought |
| **Forest** | Grow tree by not touching phone | Gentle consequences (tree stops, doesn't die) |
| **Focusmate** | Body doubling with real partner | External accountability replaces internal motivation |
| **Structured** | Visual day timeline | Beautiful, simple, drag-and-drop |

### Apps ADHD users CRITICIZE

| App | Why it fails |
|-----|-------------|
| **Notion** | #1 criticized. Infinite flexibility = infinite setup paralysis. People build systems, never use them |
| **Bullet Journals** | Abandoned after 3 days. Drawing frames gives dopamine, isn't work |
| **TickTick / Amazing Marvin** | Too many features = decision fatigue. Feature discovery as procrastination |
| **Punishment-based apps** | Shame → avoidance → total abandonment. Over 70% of r/ADHD abandonment posts mention guilt |
| **Pomodoro** | Multiple reports of not working for ADHD brains |

### Features that HELP ADHD brains

- Visual timelines (time blindness)
- Immediate rewards / satisfying feedback (dopamine)
- Zero setup friction (thoughts evaporate)
- Gentle/forgiving design (no punishment)
- External accountability (internal motivation unreliable)
- Fast capture (5-second window)
- Task micro-stepping (activation energy reduction)
- Single-purpose apps (decision fatigue prevention)

### Features that HARM ADHD brains

- Endless customization (setup becomes hyperfocus project)
- Punishment for missing (shame → avoidance → abandonment)
- Too many features (decision fatigue)
- List-only views (no time context = no urgency)
- Complex onboarding (thought evaporates before setup completes)
- Maintenance-heavy systems (ADHD brains don't maintain — they abandon)

---

## Appraised: SplitIt (trysplitit.com)

**Concept**: Write a goal → AI breaks into sub-steps → recursively split each step until actionable. Three views: Canvas (tree), Focus (one step), List (nested outline).

**Strengths**:
- Directly addresses "I know what I need to do, but I can't start"
- Focus mode = one step at a time (eliminates overwhelm)
- Context-aware AI (knows full hierarchy when splitting)
- Recursive splitting until "feels silly not to do"

**Risks**:
- Creator's own follow-up: "getting retention is hard" — paradox of ADHD tools
- AI task breakdown easily replicable (ChatGPT, Goblin.tools)
- No dopamine element / satisfying feedback
- Likely another entry in the "app graveyard"

**Assessment**: SplitIt is a feature, not a product. casedock could integrate this pattern (AI breakdown of Execution Items) without being a separate app to maintain.

---

## Meta-Patterns: Design Implications for Software

### Pattern: "This is going to be so helpful whenever I remember it exists" (396 pts)

Systems must surface relevant content automatically. Don't rely on users remembering to check.

### Pattern: Reading/saving ≠ Doing

Users confuse collecting information with taking action. The app should prompt action, not just store information.

### Pattern: "There is no TL;DR. I'm amazed I was able to read through the entire thing."

ADHD users struggle with long-form content. Progressive disclosure, bite-sized views, scannable layouts.

### Pattern: "Too many options = paralysis"

Limit visible choices. Don't show everything at once.

### Pattern: Organizing IS procrastination

If a user is organizing for 20+ minutes without completing an action item, they're procrastinating. Consider gentle nudge: "Ready to start? Your next step is: [first unchecked item]."

---

## Research Cross-Reference

This community-sourced research confirms and extends the academic findings in:

- [`2025-05-neurodiversity-summary.md`](./2025-05-neurodiversity-summary.md) — academic evidence base
- [`2025-05-neurodiversity-evidence-base.md`](./2025-05-neurodiversity-evidence-base.md) — full bibliography (59 sources)

Key overlaps:
| Academic finding | Community confirmation |
|-----------------|----------------------|
| Working memory deficits (Kasper 2013) | "Brain dump" pattern, external brain systems |
| Cognitive load sensitivity (Le Cunff 2024) | "Flat lists = paralysis" consensus |
| Attention residue (Leroy 2009) | "Can't switch tasks" lived experience |
| Perceptual load vs cognitive load (Rosenberg 2023) | "Calm ≠ boring" discussion |
| Delay aversion (Sonuga-Barke 2003) | "Why this matters" as activation support |

Key NEW insights (not in academic research):
| Community insight | Novelty |
|-------------------|---------|
| "Planning is dopamine" trap | Not addressed in academic papers reviewed |
| App graveyard cycle with novelty decay | Implicit in habituation research, not explicit |
| "Reverse todo" as shame antidote | Novel UX pattern |
| Random task picker for decision paralysis | Not in clinical literature |
| Nightly "Your Day Tomorrow" email | Novel behavioral intervention |

---

*Research conducted: June 2026. 6 primary sources, ~30 secondary sources (blog syntheses, app reviews, aggregator sites).*
