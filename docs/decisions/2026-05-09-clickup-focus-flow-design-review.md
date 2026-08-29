# Design Review: ClickUp Flow, Focus Mechanics, Case List

**Date**: 2026-05-09
**Type**: Product design review — flow analysis, open questions, unresolved gaps
**Context**: Q&A session reviewing how ClickUp integration, inbox triage, daily focus, and case listing should work based on existing specs (`docs/specs/`) and current implementation.

---

## 1. ClickUp → Inbox → Case: confirmed flow

ClickUp tasks **do not** automatically become Cases. They flow through:

```
ClickUp (assigned-to-me, read-only)
        │
        ▼
   Intake Panel  (simplified cards: title, description, due date, status, link)
        │
        │  Manual triage — user decides
        │
   ┌────┼──────────┬────────────┬──────────┐
   ▼    ▼          ▼            ▼          ▼
 Do now  Convert   Set aside   Waiting   Open in
         to Case                         source
   │     │          │            │
   ▼     ▼          ▼            ▼
 done   Case       parked       waiting
        (structured)
```

**Why triage is mandatory** (from `01-product-vision.md`, principle 3):
> "Triage before commitment — Not every incoming task deserves equal attention. Every item should first be addressed, not automatically absorbed."

**Why external tasks don't auto-become Cases** (from `06-clickup-integration.md`):
- The app would inherit external-system chaos
- The user loses the calming effect
- The product becomes a thin integration shell

### Intake Panel card fields

- title
- source (ClickUp / manual / URL / other)
- due date (if any)
- source status snapshot
- assignee snapshot
- short description snippet
- link to source system

### Intake actions

- **Do now** — immediate, lightweight execution panel
- **Convert to Case** — structured work with spec, decisions, execution
- **Set aside** — parked, not relevant now
- **Waiting on** — blocked, waiting for external input
- **Open in source** — view in ClickUp, no action here

---

## 2. Effort / weight on inbox items

**Decision: No effort field at intake.**

Effort (`quick / medium / deep`) is a **Case attribute**, set during conversion — not at inbox intake. Reasons:

- Intake should be zero-friction (principle 2: "Reduce executive friction")
- You don't know the effort until you've interpreted the item — "Implement email auth" could be quick or deep depending on context
- Effort is a **decision**, not input data

The spec examples in `07-example-task-flows.md` do show "Suggested effort: Deep" on intake cards — this could be an AI-assisted suggestion later, but it should never be a required field.

| When | What happens with effort |
|---|---|
| Inbox intake | No effort field. Raw data from source. |
| Convert to Case | User sets effort: quick / medium / deep |
| Do now | No effort needed — just do it |
| AI suggestion (future) | May suggest effort based on description, but as suggestion only |

---

## 3. "Do now" flow — sequential, not batch

**Decision: Do now = do it immediately, on the spot.**

The user does NOT triage all items first and then batch-execute "do now" items. The flow is:

1. Open first inbox item
2. Read it
3. Decide: do now / convert / set aside / waiting
4. If "do now" → lightweight panel opens → work immediately → mark done
5. Back to inbox → next item

This prevents the ADHD paralysis pattern: "I looked at everything but did nothing."

### Safety valve: Promote to Case

If "do now" grows beyond expected scope, the lightweight panel has a **Promote to Case** button. Example: SMTP config starts as "do now", but turns out to require provider selection, env setup, testing — promote to Case mid-work.

---

## 4. Set aside / Waiting — return mechanism (SPEC GAP)

**The spec defines states (`parked`, `waiting`) and transitions, but does NOT define when/how items return to the user's attention.**

This is a gap, especially critical for the target user (ADHD-leaning, overloaded).

### Proposed mechanism

#### Set Aside (`parked`)
- Items don't need time-based return — they're parked because "not now"
- **Visible in collapsed section** on the board (e.g., "Parked (27)") — number visible, items hidden by default
- **Manual return** — user drags/clicks back to triage when ready
- **Weekly review prompt** (future) — once a week, show parked items with "anything to revisit?"
- Based on GTD (Getting Things Done) Weekly Review pattern

#### Waiting On (`waiting`)
- Items are time-sensitive — waiting for someone/something
- **Visible in expanded section** on the board with staleness indicator
- **Auto-staleness signal**: after 3 days → yellow highlight, after 7 days → red highlight. Visual only, not push notification
- **Manual return** — when response arrives, click to move back to `new`
- Optional field: "waiting for..." (free text, describing what's blocking)

#### Board layout proposal

```
┌──────────────────────────────────────────────┐
│  TODAY'S FOCUS                                │
│    1 main + 2 secondary                       │
├──────────────────────────────────────────────┤
│  INBOX (new)          12 items                │
│  WAITING (stale)       3 items  ← yellow      │
│  PARKED               27 items  ← collapsed   │
└──────────────────────────────────────────────┘
```

---

## 5. Focus mechanics — closing main, auto-promotion

### Current implementation (`focus/services.py`)

`clear_case_from_focus()` already handles auto-promotion:

| Situation | What happens |
|---|---|
| Close main, 2 secondary exist | Secondary #1 → main, Secondary #2 → sole secondary. Slot freed. |
| Close main, 1 secondary exists | Secondary → main. Empty secondary slot. |
| Close main, no secondary | Focus becomes empty. All assignments deleted. |
| Close secondary | Main stays. One secondary remains. Slot freed. |

### UX concern

Auto-promotion should be **visible** — toast/flash message: "SMTP config promoted to main focus." Otherwise the user may not notice the change.

When focus becomes empty (all cases done), show a prompt to pick next main focus from active cases.

### Focus is per-day, resets each morning

`FocusAssignment` has `focus_date`. Next day = new focus. This is consistent with "explicit daily focus" philosophy. Could add "carry forward yesterday's focus" option later.

---

## 6. Focus — no auto-fill of secondary slots

**Decision: Empty secondary slots stay empty. No automatic insertion of cases from inbox/active list.**

Reason: Focus means "I consciously choose to work on this." If the system auto-fills, focus becomes just another filtered list, not a deliberate decision.

An empty slot is **intentional space**: "You have room, choose consciously."

---

## 7. Focus — multiple rounds per day

**Decision: User can set focus again mid-day. No special mechanism needed.**

`replace_focus_for_day()` replaces all assignments for a given date. Flow:

```
8:00   Set focus #1
         Main:  Email auth
         Sec:   Fix printer, SMTP config

12:00  All 3 done → set focus #2
         Main:  F03 system
         Sec:   Deploy staging, Update docs
```

Focus is "what I'm working on now", not "what I swear to work on today."

---

## 8. Case list — sorting and metadata

### Current sorting

Board sorts by **`-updated_at, -created_at`** — most recently touched on top.

No manual sort, no drag-and-drop, no priority field. This is by design — Case is not a prioritized task. Prioritization is handled by Focus.

### Metadata available at creation

| Field | Values | Purpose |
|---|---|---|
| `effort` | quick / medium / deep | How big is this chunk of work |
| `clarity` | clear / fuzzy | Do you know what to do |
| `work_type` | build / debug / research / admin / reply | What kind of work |
| `energy` | shallow / deep | What type of focus it requires |

These don't sort the list but could enable filtering (e.g., "show only quick + clear when I have low energy").

### Missing: `due_date` on Case

Due date from ClickUp is visible in Intake Panel but **lost after conversion to Case**. Options:

1. **Add `due_date` field to Case** (recommended) — simple, useful, naturally enables sort-by-urgency
2. **Show due date from SourceLink on Case card** — no schema change, but requires extra query
3. **Don't add** — due date lives in source system, click to check

**Recommendation**: Option 1. `due_date` is too useful to hide in SourceLink. It also naturally leads to urgency-based sorting.

---

## 9. Open questions

### Critical (affects v1.5 ClickUp integration)

- [ ] **Intake Panel UI**: How exactly should the intake panel look? Separate page, sidebar, or section on board?
- [ ] **ClickUp sync trigger**: Manual pull (button) vs scheduled pull (cron) vs webhook? Spec says "assigned-to-me, read-only" but doesn't specify pull mechanism.
- [ ] **Source data snapshot**: When and how often do SourceLink snapshots refresh? On pull? On user action?
- [ ] **"Waiting for..." field**: Should `waiting` state on InboxItem have a free-text "waiting for..." field? Useful but not in spec.
- [ ] **Due date on Case**: Should Case model get a `due_date` field? Strong recommendation to add it.

### Important (affects UX quality)

- [ ] **Weekly review prompt**: Should parked items get a weekly re-surfacing prompt? GTD-inspired, good for target user.
- [ ] **Staleness thresholds**: What are the right thresholds for waiting items? 3 days yellow / 7 days red proposed — needs validation.
- [ ] **Auto-promotion notification**: When secondary auto-promotes to main focus, should there be a visible notification (toast/flash)?
- [ ] **Empty focus prompt**: When focus is completely empty, what exactly does the user see? List of active cases to pick from?
- [ ] **Filtering by metadata**: Should board allow filtering by effort/clarity/work_type/energy? Useful for "low energy mode" scenarios.

### Future (phase 3+)

- [ ] **Write-back to ClickUp**: Explicit, review-based update flow described in spec — needs detailed design.
- [ ] **AI-suggested effort**: Spec examples show "Suggested effort: Deep" on intake cards. What's the mechanism?
- [ ] **Carry forward focus**: Should user be able to carry yesterday's focus to today?
- [ ] **Multi-provider**: Spec mentions Jira, Asana, GitHub Issues — how generic should the connector boundary be?
- [ ] **"Waiting for..." nudges**: Auto-suggest sending a reminder after staleness threshold.

---

## 10. Design decisions summary

| Topic | Decision | Rationale |
|---|---|---|
| ClickUp → auto-Case | **No** | External task ≠ Case. Triage first. |
| Effort at intake | **No** | Effort is a decision made during conversion, not input data. |
| Do now = batch? | **No** | Sequential — open, decide, do, close. Prevents ADHD paralysis. |
| Set aside return | **Manual + weekly review** | Time doesn't apply to "not now" items. |
| Waiting return | **Auto-staleness signal** | Time matters — visual indicator when stale. |
| Auto-fill focus slots | **No** | Focus is explicit choice, not auto-populated. |
| Multiple focus/day | **Yes** | Focus = "what now", not "what today, sworn". |
| Due date on Case | **Recommended: yes** | Too useful to hide in SourceLink. |
| Case list sorting | **By updated_at** | No manual priority — Focus handles prioritization. |

---

## 11. Triage adoption — why users should invest the effort

### Core objection: „I already have tasks in ClickUp, why do this again?"

The key misunderstanding: triage in casedock is NOT the same activity as organizing tasks in ClickUp/Jira/Todoist.

| In ClickUp/Jira | In casedock |
|---|---|
| Organize for **tracking** — statuses, assignees, priorities, lists, folders, tags | Organize for **doing** — what does this mean for me and what will I do about it |
| Managerial perspective: "where is this, who owns it" | Execution perspective: "do I act now, shape it, or ignore it" |
| No interpretation required — just file it | Interpretation IS the value — each item gets a personal decision |

ClickUp answers: "This task is In Progress, High priority, assigned to me."
casedock answers: "This takes 15 minutes and I can close it now" or "This is unclear, I need to think before starting."

The second answer requires thinking. That thinking IS the value, not its absence.

### The hidden cost of NOT triaging

Someone with 47 tasks in ClickUp who doesn't triage is still making decisions — just badly:

- **On the fly**, during work, at the worst possible moment
- **Repeatedly** — reviewing the same list daily, re-deciding what's important every time
- **With anxiety** — 47 items = constant low-grade "I should be doing something about these"

| Cost of no triage | Example |
|---|---|
| Context switching tax | Open ClickUp, see 47 tasks, close it. Nothing done but you're tired. |
| Re-deciding | Every morning you scan the same list and pick the same 3 things. That's the same decision made 5 times. |
| Paralysis | Too much to process = do nothing. |
| Sunk attention | You keep looking at tasks you won't touch for a week, but every glance costs attention. |

Triage in casedock is a **one-time investment**: process an item once, decide once, and it disappears from view until needed. Instead of deciding daily over the same list, you decide once and move on.

### How to explain it — by audience

**For someone coming from ClickUp/Jira:**
> "How many times a day do you open ClickUp, look at the list, and nothing comes of it? Triage in casedock costs 30 seconds per item, but after triage you NEVER look at that item again until you choose to. Closed? Gone. Set aside? Invisible. Waiting? System reminds you. Your head is empty instead of full of 47 things."

**For someone with ADHD / overload:**
> "You don't have to organize everything. You just decide about one item at a time: do it now, turn it into a project, or set it aside. This isn't organizing — it's **unloading**. Every item that leaves your inbox is one less thing living in your head on standby."

**For someone who says „this is a waste of time":**
> "Right now: 47 tasks, 5 min/day scanning, nothing done after 3 days = 15 minutes wasted.
> After triage: 30 minutes once, then 0 minutes scanning because you know what you're doing = net savings from day 4."

### Critical framing distinction

Don't say: **„Organize your tasks"** (sounds like homework, feels like admin).
Say: **„Get this out of your head"** (sounds like relief, feels like progress).

Triage is not organizing — it's **unloading**. Every item that leaves inbox with a decision is one less thing occupying mental standby. That's the value.

### UX implication: triage must feel rewarding

The product should make the act of clearing inbox feel good:
- Inbox counter going from 12 → 0 = dopamine hit
- Contrast with ClickUp, where the list never shrinks because new tasks constantly flow in
- Visual progress: cleared items disappear, not just change status
- Empty inbox state should feel like accomplishment, not „nothing to do"

This means the inbox counter and the visual feedback of items leaving are not cosmetic — they are core to adoption.

---

## 12. Additional open questions from triage value discussion

### Adoption & onboarding

- [ ] **First-run experience**: When a user connects ClickUp and sees 47 items for the first time, how do we prevent immediate overwhelm? Batch show? Progressive reveal? Guided triage for first 5 items?
- [ ] **Triage fatigue**: What if someone has 100+ items from ClickUp? Should there be a „triage session" mode that shows items in batches (e.g., 10 at a time)?
- [ ] **Inbox zero moment**: How should the UI celebrate / acknowledge an empty inbox? This is psychologically important for adoption.
- [ ] **Metrics for triage value**: Should the app show „time saved" or „decisions made" stats? Could reinforce the value of triage.
- [ ] **Partial triage**: What if someone only triages 5 out of 12 items and closes inbox? Should items remain in `new` or should we prompt?
- [ ] **Re-onboarding after break**: If someone hasn't used casedock for 2 weeks and has 30 new ClickUp items, how do we ease them back in?

### Product positioning

- [ ] **Framing in UI copy**: Audit all inbox/triage-related labels for „organizing" language vs „unloading" language. The framing matters.
- [ ] **Onboarding explanation**: Should first-time triage include a one-line explanation of WHY? („Each item you process leaves your head. Decide once, move on.")
- [ ] **Empty state messaging**: When inbox is empty, what does the message say? „All clear" (achievement) vs „No items" (dead) — framing matters.

---

## 13. Does casedock make sense without external integrations?

### Short answer: Yes. Integration is an accelerant, not a prerequisite.

The strongest adoption hook IS integration ("connect ClickUp and stop living inside it"), but the core product value — converting chaos into structured execution — does not depend on where the chaos comes from.

### Two user segments, same problem

| | With integration (ClickUp/Jira user) | Without integration (solo builder) |
|---|---|---|
| **Where chaos comes from** | Outside — assigned tasks from team/system | Inside — own ideas, half-thoughts, noticed things |
| **Pain** | "47 tasks and I don't know where to start" | "15 things in my head and I'm doing none of them" |
| **casedock value** | Converts someone else's chaos into your structure | Converts your internal chaos into structure |
| **Manual capture role** | Supplement (things not in ClickUp) | Primary intake |

A solo builder doesn't need ClickUp to be overwhelmed. They have:
- ideas that come up during work
- bugs they noticed but didn't log
- things they want to investigate
- half-started projects
- things deferred for weeks

For them, **manual capture → triage → case** IS the full product. Not a supplement — the entire workflow.

### What the spec says

- `01-product-vision.md`: "they should still feel oriented even if no integration is connected"
- `07-example-task-flows.md`: "The core workflow should stay useful even when no connector is enabled"
- `02-domain-model.md`: "The core model must remain useful even when every item comes from manual capture"
- Example 2 in `07-example-task-flows.md` is specifically a manual capture scenario ("Add SMTP to ParcelTracker")

### Manual capture must be zero-friction

For the no-integration user, capture is the front door. It must feel like relief, not admin:

- One field (title) → enter → done. Not a form, not categorization.
- Framing: **"capture it and come back later"** / **"don't think now, throw it in inbox"**
- This is the GTD capture habit — collect everything in one place without filtering
- Value: you stop carrying it in your head

### Integration is the gateway, not the destination

| Statement | Accuracy |
|---|---|
| "casedock needs ClickUp to be useful" | **False** — core loop works with manual capture alone |
| "ClickUp integration drives adoption" | **True** — strongest hook for the largest segment |
| "Manual capture is just a supplement" | **False** — for solo builders it's the primary intake |
| "Product should work fully without any integration" | **True** — integration is an accelerant, not a prerequisite |

### Implications for product development

- v1 must be complete with manual capture alone — this is already the case
- Integration should be positioned as "level up", not "turn on"
- Onboarding should demonstrate value with manual capture FIRST, then offer integration as enhancement
- The capture UX (title-only, one field, instant) is as important as the integration UX

---

## 14. Additional open questions from integration value discussion

- [ ] **Capture friction audit**: Is the current manual capture flow truly one-field-and-done? Or does it ask too much upfront?
- [ ] **Onboarding sequence**: Should onboarding show manual capture value BEFORE offering integration? ("Try with your own items first → want more? Connect ClickUp")
- [ ] **Capture everywhere**: Should there be a global quick-capture shortcut available from any page? (e.g., keyboard shortcut, floating button)
- [ ] **Segment-specific onboarding**: Should first-run experience differ for "I use ClickUp" vs "I don't use any task manager" users?
- [ ] **Integration as progressive enhancement**: How to communicate that integration is optional without making it seem unimportant?

---

## 15. Bidirectional connectors — write-back strategy

### The problem

Without write-back, a connector is incomplete — the user still has to go to ClickUp/Jira to close tasks. This undermines the "stop living in ClickUp" value prop.

But full automatic bidirectional sync is dangerous:
- Tasks are shared — your "done" is not their "done"
- Statuses don't map 1:1 (casedock: active/waiting/done vs ClickUp: open/in progress/review/closed + custom)
- ClickUp has data casedock doesn't (custom fields, time tracking, other people's comments)
- Auto-close sends notifications to the whole team — unintended consequences

### Write-back spectrum

| Level | What you can do | Is it enough? |
|---|---|---|
| **Read only** | See tasks, triage, work in casedock | **Half a product** — still must go to ClickUp to close |
| **Read + deep link** | Click straight to specific task in source | **Pragmatic v1.5** — avoid the chaos, go direct |
| **Read + review-based write-back** | Draft update → user reviews → sends to source | **Optimal phase 3** — full control, zero surprises |
| **Full bidirectional sync** | Auto-sync both directions | **Overkill** — complexity, conflicts, illusion of control |

Sweet spot: **level 3** (explicit, review-based write-back) for phase 3. But **level 2** (deep links) is sufficient and valuable for v1.5.

### What each connector must know about its service

Connectors are not universal adapters — each has service-specific logic:

| Layer | What the connector must handle |
|---|---|
| **Ingest** | Pull assigned-to-me tasks with right fields (title, description, due date, status, assignee, url) |
| **Status mapping** | Bidirectional status mapping (casedock `done` → ClickUp `closed`? `resolved`? `ready for review`?) |
| **Draft update** | Generate update appropriate for the service (ClickUp = comment + status change, GitHub = issue comment + close, Jira = transition + comment) |
| **Push** | Send updated data via service API |
| **Snapshot refresh** | Refresh source data without overwriting local work (private notes, decisions, spec — never overwritten) |

The **interface** (intake → triage → case → draft update → send) is universal. The **implementation** per service is specific.

---

## 16. v1.5 pragmatic solution: deep links + local checkbox

Until write-back is built (phase 3), the user avoids ClickUp chaos through **direct links to specific tasks**.

### How it works

SourceLink already stores `external_url` on Cases. When a Case is marked `done`:

```
┌─────────────────────────────────────────┐
│  ✓ Case completed                        │
│                                           │
│  This case is linked to a ClickUp task.   │
│  [Open task in ClickUp →]                 │
│                                           │
│  ☐ Done — I've updated the source task    │
└─────────────────────────────────────────┘
```

1. **Link** — one click, opens the specific task in ClickUp (not the list, not the dashboard — one task)
2. **Checkbox** — "I've updated the source" — local flag so user doesn't have to remember whether they already closed it in ClickUp

The user never sees the full ClickUp task list. They go directly to one task, do what's needed, come back.

### Why this is sufficient for v1.5

| Problem | Solution |
|---|---|
| Don't want to see all of ClickUp | Deep link → specific task |
| Don't want to remember if I closed it | Checkbox "updated source" on Case |
| Don't want to manually find the task | Link is already in SourceLink |
| Want to close several in a row | Queue: after checking "updated source" → show next unclosed case with source link |

**Minimal overhead, maximum relief.** No API integration needed for write-back, just a URL and a local boolean.

### What's already implemented

- `SourceLink` model has `external_url` — link to task in external system
- Intake Panel has **"Open in source"** action
- Case view has source links section

### What needs adding for v1.5

- Source link visibility on Case completion (prompt to close in source)
- Local boolean field on SourceLink or Case: `source_updated` (defaults to false, user checks when done)
- Visual indicator on Case list: Case is done but source not updated yet (e.g., subtle badge)

---

## 17. Additional open questions from connector/write-back discussion

- [ ] **Source update prompt timing**: When should the "update source" prompt appear? Immediately on Case `done`? On next board visit? As a separate "pending source updates" section?
- [ ] **Batch source updates**: Should there be a "pending source updates" view where user can process multiple completed cases at once? (open first → close → next → next)
- [ ] **Source update tracking**: Should `source_updated` be a field on SourceLink, Case, or a separate model? Implications for multiple source links on one Case.
- [ ] **Per-connector status mapping config**: Should users be able to configure how casedock statuses map to ClickUp statuses? Or should the connector have sensible defaults?
- [ ] **Connector permission scope**: What API scopes/permissions does each connector need? Read-only for v1.5, write for phase 3 — how to handle auth?
- [ ] **Stale source data indicator**: When source task has been updated (e.g., someone commented, changed priority) but casedock doesn't know yet — how to signal this?

---

## 18. Case decomposition — when a Case is too big

### The problem

Some Cases start as one thing but reveal themselves to be collections of independent, meaningful work items. "Implement email authentication" is actually: choose approach + build backend + build UI + write tests. Each has its own decisions, spec, and execution. One Case can't hold this without becoming a mini-Jira.

The spec warns: "Do not let execution become a second giant task manager." But the spec also doesn't address decomposition explicitly.

### Three options considered

| Option | Description | Pros | Cons |
|---|---|---|---|
| **Flat decomposition** | User manually creates separate Cases, links them in markdown | Zero model changes | No structure, links get lost, no progress tracking |
| **Parent Case hierarchy** | `parent_case` FK on Case, parent = umbrella, children = sub-Cases | Formal relationship, progress visible | Complexity: focus on sub or parent? Decisions at which level? Sub-sub-cases? |
| **Decompose action (lightweight)** | "Decompose" action on Case creates related Cases, original becomes umbrella dashboard | Structured but not over-engineered. Focus stays on leaf Cases. | Requires new relationship model |

### Recommended: Option 3 — Decompose action

#### How it works

1. User creates Case: "Email auth" → active, fuzzy
2. Starts working, realizes it's enormous
3. Clicks **"Decompose"**
4. Enters list of sub-Case titles:
   - "Choose auth approach"
   - "Build backend flow"
   - "Build auth UI"
   - "Write integration tests"
5. System creates 4 separate Cases, each with:
   - Source link back to parent
   - Default spec seeded with parent context
6. "Email auth" becomes **umbrella** — not a workspace, a dashboard
7. User picks focus on individual (leaf) Cases
8. As each sub-Case completes → umbrella updates progress
9. All sub-Cases done → umbrella auto-completes

#### Umbrella Case view

```
┌─────────────────────────────────────────────┐
│  CASE: "Implement email authentication"      │
│  Status: umbrella                            │
│                                              │
│  Related Cases:                              │
│    ✓ Choose auth approach        [done]      │
│    → Build backend flow          [active]    │
│    ○ Build auth UI               [inbox]     │
│    ○ Write integration tests     [inbox]     │
│                                              │
│  Progress: 1/4 done                          │
│                                              │
│  [Open any sub-case →]                       │
└─────────────────────────────────────────────┘
```

#### Rules

| Rule | Why |
|---|---|
| **Umbrella is not a workspace** | No execution items, no focus slot. Only a dashboard showing child Case progress |
| **Decompose is optional** | Small/medium Cases live without it. Decompose only when the user feels it's too big |
| **Max 1 level of nesting** | No sub-sub-cases. If a sub-Case is too big → decompose it, it becomes umbrella, its children are siblings |
| **Focus works on leaf Cases** | Daily focus picks specific Cases, never umbrellas |
| **Decisions live at Case level** | Each Case has its own decisions. Umbrella can have high-level decisions ("using magic link") |
| **Auto-complete umbrella** | When all child Cases are `done`, umbrella auto-transitions to `done` |
| **User decides decomposition** | Never automatic. The user must feel the size and choose how to split |

#### What NOT to do

- ❌ Epic → Story → Task → Subtask hierarchy (this IS the Jira chaos we're escaping)
- ❌ Multi-level nesting (unbounded hierarchy = unbounded complexity)
- ❌ Automatic decomposition (user must decide what the pieces are)
- ❌ Execution items on umbrella (umbrella is a dashboard, not a workspace)

### Model implications

Current Case model needs:

- Optional `parent_case` FK (self-referential, nullable) — or separate `CaseRelation` model
- Status awareness: umbrella Cases have different behavior than leaf Cases
- Progress computation: count children by status

Two approaches to the relationship model:

| Approach | Description | Tradeoff |
|---|---|---|
| `parent_case` FK on Case | Simple, direct | One parent only (good — enforces max 1 level), but mixed concerns in model |
| `CaseRelation` M2M through model | `parent`, `child`, `order` | More flexible, cleaner separation, but over-engineered for 1-level hierarchy |

**Recommendation**: `parent_case` FK. Simple, enforces single parent, easy to query. Add `CaseRole` choices: `leaf` (default) vs `umbrella`.

### When does decomposition naturally happen

- During **Convert to Case** — user realizes the inbox item is bigger than expected
- During **work on Case** — execution reveals hidden complexity
- During **spec writing** — markdown outline makes the real scope visible
- During **decision-making** — a decision opens multiple independent work streams

The product should make decomposition feel natural, not like a planning ceremony. It's an **emergent action**, not a planned one.

---

## 19. Additional open questions from case decomposition discussion

### Data model

- [ ] **Parent FK vs through model**: Confirm `parent_case` FK on Case vs separate `CaseRelation` model. FK is simpler but through model is cleaner if we ever need ordering or metadata on the relationship.
- [ ] **Umbrella status model**: Should umbrella have the same status choices as leaf Cases? Or simplified (only `active` / `done`)? Umbrella probably shouldn't be `waiting` — that's a leaf-level concern.
- [ ] **CaseRole field**: Should Case have a `role` field (`leaf` / `umbrella`)? Or is it inferred from having children? Explicit is clearer but another field to maintain.
- [ ] **Circular reference protection**: How to prevent Case A being parent of Case B which is parent of Case A? DB constraint + clean() validation?
- [ ] **Decompose and re-compose**: Can a user merge child Cases back into the parent? Undo decomposition? What happens to work done in children?

### UX

- [ ] **Decompose UI**: What does the "Decompose" form look like? Simple textarea with one title per line? Or more structured with effort/clarity per sub-Case?
- [ ] **Umbrella on the board**: How do umbrellas appear on the board? Different card style? Collapsed (just title + progress bar)? Or hidden entirely (only leaf Cases on board)?
- [ ] **Focus with umbrellas**: Should umbrellas be selectable as focus items? (Recommendation: no — focus on leaf Cases only)
- [ ] **Umbrella spec**: Should umbrella have its own spec/decisions? Or just link to children? High-level context (project overview, constraints) probably belongs in umbrella spec.
- [ ] **Decompose from execution**: Should user be able to promote an Execution Item into a full Case? (e.g., "this step is way bigger than I thought → make it a Case")
- [ ] **Umbrella private notes**: Should umbrella have private notes separate from children? Probably yes — project-level private thinking.

### Product

- [ ] **When to suggest decomposition**: Should the app ever prompt "this Case seems large — want to decompose?" Based on what signal? Number of execution items? Age? Spec length?
- [ ] **Decomposition and ClickUp**: If a ClickUp task becomes an umbrella Case with children, what happens to the SourceLink? Does each child get a SourceLink to the same task? Or only the umbrella?
- [ ] **Reporting**: Should umbrella show aggregate info from children? Total effort estimate, combined execution progress, decision count?
- [ ] **Decompose as workflow**: Should decomposition be documented as Workflow 11 in `docs/specs/03-workflows.md`?

---

## 20. Additional open questions (connectors + public repo)

### Connector priority

- [ ] **ClickUp vs Todoist as first connector**: ClickUp is spec'd and has stronger „escape from chaos" narrative. Todoist is simpler API and broader user base. Which first?
- [ ] **Connector scope for launch**: What's the minimum viable connector? Read-only + deep links? Or needs some write-back to be compelling?
- [ ] **Connector auth UX**: How does the user connect ClickUp? OAuth? API token? Where in the UI?

### GitHub / README

- [ ] **README structure**: What sections? Problem, screenshots, stack, quick start, contributing, roadmap?
- [ ] **Demo data**: Should `seed_demo` produce a convincing demo state for screenshots?
- [ ] **Contribution guidelines**: Open to contributions from day one? Or „feedback welcome, code later"?

> Sections 20, 22–24 of this review originally covered launch strategy (forum lists, announcement sequencing, post drafts), landing-page concepts, A/B testing, and launch analytics. That business/GTM content was removed before the project was published — the product ships as a plain app for solo developers, and marketing decisions live outside this repository.

---

## 25. Remaining topics worth addressing

### 25.1 AI — assistant, not decider

The `ai/` module is a stub. Spec says: „AI may summarize, draft, and propose next steps, but it must not make meaningful product, workflow, or sync decisions autonomously."

Concrete use cases:

| Use case | When | User action |
|---|---|---|
| **Draft spec** | After Inbox → Case conversion | AI proposes starter spec from task description → user edits/accepts |
| **Suggest next step** | On opening a Case | AI reads spec + decisions + execution → suggests „your next move is..." → user decides |
| **Summarize case** | Returning after absence | AI summarizes what happened since last visit |
| **Draft source update** | On Case completion | AI writes update draft for ClickUp → user reviews → sends |
| **Suggest decomposition** | Large Case detected | AI asks „want to break this into pieces?" → user decides how |

**Rule**: every AI output is a **draft requiring explicit accept**. Never auto-apply.

### 25.2 Onboarding — empty product is terrifying

First login → empty board, zero cases, zero inbox. What now?

- **Guided first steps**: „Capture your first item" → „Convert to Case" → „Set focus" — 3-step walkthrough
- **Demo data option**: on first login — „Load sample data to explore?" (with option to clear later)
- **Empty state messages**: not „No cases" but „What are you working on? Capture your first item."

Empty states ARE the UX, not an afterthought. This is the first impression.

### 25.3 Data export as the trust baseline

casedock ships as a plain app for solo developers — no hosted/paid split is planned in-repo. User trust comes from data ownership, not from business-model choices (see 25.8 below).

### 25.4 Deployment — how people will run it

Target user is overloaded — deployment must be minimal effort:

- **Docker Compose** — one `docker compose up` and it runs
- **`.env` template** — clear what needs configuring
- **One-click deploy** — Render / Railway / Fly.io button in README
- **SQLite by default** — zero database config on start (already the case)

Fewer steps to „it works" = more people try it.

### 25.5 Keyboard shortcuts

Target user is a developer. Developers hate mice. Minimum:

| Shortcut | Action |
|---|---|
| `n` | New inbox item (quick capture) |
| `/` | Search |
| `Esc` | Close modal / back |
| `j` / `k` | Next/previous item (vim-style) |

Not needed for launch, but worth having in backlog. Difference between „useful" and „delightful".

### 25.6 Mobile — not an app, but don't ignore

No mobile app. But overloaded user checks phone on the tram, couch, queue. Two things must work on mobile:

- **Quick capture** — open, type title, enter. Done.
- **Focus view** — see what I'm working on today. View only.

The rest (triage, spec editing, execution) is desktop-only and that's OK.

### 25.7 Dead Case cleanup

Closed Cases never disappear. After a year: 200+ done Cases cluttering the system.

- **Archive** — done → archived, only appears in search
- **Auto-archive** — after 30 days in `done`, auto-transition to `archived`
- **Hard delete** — optional, for things you don't want in the system

Spec has `archived_at` on Case model but no auto-archive mechanism.

### 25.8 Data export

„What if I want to leave casedock?" — basic respect for user's data:

- **Export Cases as Markdown** — each Case = one .md file with frontmatter (metadata) + spec + decisions + notes
- **Export inbox items as JSON** — simple dump
- Not needed for launch, but builds trust. Important for OSS credibility.

### Priority timeline

| Topic | When |
|---|---|
| AI helpers | Phase 3 (after connectors) |
| Onboarding / empty states | **Before release** — first impression |
| Docker / one-click deploy | **Before release** — so people can try |
| Keyboard shortcuts | Post-release, v2 |
| Mobile capture | Post-release, v2 |
| Dead Case cleanup | When users accumulate history |
| Data export | Post-release, signal of trust |

---

## 26. Additional open questions from remaining topics

### AI

- [ ] **AI provider**: Which LLM provider? OpenAI API? Local model? Provider-agnostic adapter?
- [ ] **AI scope for v1**: Which AI feature ships first? Draft spec? Next step suggestion?
- [ ] **AI cost**: Who pays for API calls? User's own key, or bundled?
- [ ] **AI trust**: How to make AI suggestions feel helpful, not intrusive? Visual distinction between AI-generated and user-written content?

### Onboarding

- [ ] **Onboarding flow design**: Step-by-step wizard? Tooltip tour? Just good empty states?
- [ ] **Demo data content**: What Cases/Inbox Items should demo data contain? Realistic examples from `07-example-task-flows.md`?
- [ ] **Skip onboarding**: Should experienced users be able to skip? How?

### Licensing

- [ ] **Licensing**: Which OSS license? MIT? AGPL (prevents cloud reselling)? BSL?

### Deployment

- [ ] **Docker image**: Official Docker Hub image? GitHub Container Registry?
- [ ] **Minimum requirements**: What are the minimum system requirements? RAM, disk, CPU?
- [ ] **Upgrade path**: How do users upgrade between versions? Database migrations? Breaking changes?

### Mobile

- [ ] **PWA**: Should casedock be installable as PWA? Service worker for offline quick capture?
- [ ] **Responsive audit**: Current responsive state of templates — what needs fixing for mobile capture?

### Data

- [ ] **Export format**: Markdown with YAML frontmatter? Pure markdown? JSON?
- [ ] **Import**: Should users be able to import from other tools? (ClickUp export, Todoist export, plain markdown)
- [ ] **Auto-archive timing**: 30 days in `done` → `archived`? Configurable?

---

## References

- `docs/specs/01-product-vision.md` — product principles (triage before commitment, explicit focus)
- `docs/specs/02-domain-model.md` — Case, InboxItem, FocusAssignment models
- `docs/specs/03-workflows.md` — all 10 workflows including Do now, Convert, Focus
- `docs/specs/06-clickup-integration.md` — ClickUp connector design principles
- `docs/specs/07-example-task-flows.md` — 4 concrete examples of flow
- `docs/specs/09-architecture.md` — module boundaries
- `src/apps/focus/services.py` — focus management implementation
- `src/apps/cases/models.py` — Case model with metadata fields
- `src/apps/ui/views.py` — board context and sorting
