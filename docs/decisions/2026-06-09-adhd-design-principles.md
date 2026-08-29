# Decision: ADHD Design Principles for casedock

> Date: 2026-06-09
> Source: [`docs/research/2026-06-adhd-reddit-community-insights.md`](../research/2026-06-adhd-reddit-community-insights.md)
> Status: Active — these principles guide all future UI/UX decisions

---

## Context

Community research from Reddit (6 threads, 1000+ ADHD users) confirmed and extended academic neurodiversity research. 15 actionable insights were identified and mapped to casedock features.

These principles are NOT just "nice to have for ADHD users." The academic evidence shows ADHD-friendly design benefits ALL users (curb-cut effect, Weyerhaeuser & Piccolo 2026). These principles make casedock better for everyone.

---

## The 15 Principles

### CRITICAL — Core product impact

#### 1. Show ONE next action, not full context

**Insight**: ADHD paralysis comes from seeing a monolithic task. The breakthrough is "pick up one sock" instead of "clean apartment." When a user opens a Case, the first thing they see should be the single next step, not the full spec.

**casedock mapping**: The first unchecked Execution Item should be surfaced as the default view when opening a Case. Full spec/decisions/notes are accessible but NOT the primary visual.

**Status**: Not implemented. Needs UI change in case detail view.

**Evidence**: Thread #3 (1,343 upvotes), Thread #1 (131 tips), Goblin.tools (~15 recommendations), KC Davis "How to Keep House While Drowning."

---

#### 2. Never shame for inactivity

**Insight**: Shame is the #1 reason ADHD users abandon productivity tools. Red overdue badges, "you haven't been here in X days" notifications, streak breaks — these trigger avoidance cycles. Over 70% of r/ADHD app abandonment posts mention guilt/shame.

**casedock mapping**:
- NO red badges or overdue indicators anywhere
- Stale cases shown neutrally (grey, not red) — "maybe worth revisiting"
- No streak tracking, no "you completed X today vs yesterday" comparisons
- Empty states say something warm, not accusatory

**Status**: Partially implemented. Calm design exists. Stale detection planned in board redesign. Must ensure stale indicators are neutral, not punitive.

**Evidence**: Thread #1 (Emotional Dysregulation tips), Thread #2 (shame accumulators), Thread #4 (70% abandonment stat), Spiel 2022 (CHI).

---

#### 3. Limit visible cases on Board

**Insight**: Flat lists of 14+ items cause cognitive overload and paralysis for ADHD brains. Every item competes for attention, brain defaults to inaction.

**casedock mapping**: Board shows max ~7-10 active cases by default. Additional cases are accessible but not visible. Focus module (1 main + 2 secondary) is the gold standard — extend this philosophy to Board level.

**Status**: Partially implemented. Focus module exists with 1+2 structure. Board may need pagination/folding.

**Evidence**: Thread #2 (flat list paralysis), Thread #1 (overwhelm tips), Forster & Lavie 2014 (perceptual load).

---

#### 4. Zero-friction Inbox capture

**Insight**: ADHD thoughts evaporate in seconds. The 5-second capture window is real. If capture requires navigating menus, picking categories, or filling forms — the thought is gone.

**casedock mapping**:
- Inbox capture = one text field, zero required fields
- Brain dump, no categorization at capture time
- Conversion to Case also minimal — no 10-field form
- Organizing is a SEPARATE mental mode from capturing

**Status**: Implemented. Inbox capture works well. Must maintain as features are added.

**Evidence**: Thread #2 (5-second window), Thread #1 (instant capture tips), McDowall 2025 (3.1x context switching trouble).

---

#### 5. Auto-surface important things — don't rely on user memory

**Insight**: ADHD object permanence issue — "out of sight = out of mind." Users save things and never return. The most upvoted comment on a tips post was "This is going to be so helpful whenever I remember it exists."

**casedock mapping**:
- Board landing view shows "here's what needs attention today"
- Stale detection auto-surfaces neglected Cases
- Don't require users to remember to check specific views
- Critical information should be visible without navigation

**Status**: In plan (board redesign includes stale detection). Not yet implemented.

**Evidence**: Thread #1 (396 pt comment about forgetting), Thread #3 ("object permanence is a bitch"), Gilbert 2020 (external reminders).

---

### IMPORTANT — Strengthens product-market fit

#### 6. Micro-steps as core mechanic

**Insight**: Task breakdown until steps are so small they feel ridiculous NOT to do. "Open document" instead of "work on project." Define only the FIRST action, trust momentum.

**casedock mapping**: Execution Items are micro-steps. Consider:
- (a) AI-suggested breakdown of Execution Items
- (b) Auto-suggest "first next action" based on unchecked items
- (c) "Just start" button that shows ONLY the first unchecked item
- (d) Visual indicator of "next step" on Case cards on Board

**Status**: Execution Items exist. AI breakdown and "just start" UI not yet implemented.

**Evidence**: Thread #3 (breakthrough pattern), Goblin.tools (~15 mentions), SplitIt concept.

---

#### 7. Satisfying completion feedback

**Insight**: Checking a box doesn't give enough dopamine for ADHD brains. They need slightly stronger completion signals. BUT — no gamification (which is harmful for ADHD). The balance is satisfying feedback without game mechanics.

**casedock mapping**:
- Progress bar on Case (Execution Items done vs total)
- Satisfying animation on checking off Execution Items
- "You completed 3 things today" end-of-day summary
- NOT: points, XP, streaks, leaderboards, pets

**Status**: Not implemented. Needs CSS/HTMX animation work.

**Evidence**: Thread #2 (dopamine reward loops), Thread #3 (Finch success), Rosenberg 2023 (perceptual engagement ≠ cognitive load).

---

#### 8. Reverse todo / Accomplishment view

**Insight**: ADHD users benefit enormously from seeing what they DID, not just what they haven't done. "Reverse todo lists" (writing accomplishments) reduce shame and build confidence. The top comment (580 pts) recommended adding already-done items to lists.

**casedock mapping**: New view: "What you did this week/month" — auto-generated from completed Cases + Execution Items. Celebrates progress. No mention of backlog or undone items in this view.

**Status**: Not implemented. New feature needed.

**Evidence**: Thread #1 (reverse todo tip), Thread #3 (580 pt comment), "I Work Twice as Hard" 2026 (occupational self-efficacy).

---

#### 9. Calm does not mean under-stimulating

**Insight**: ADHD brains are chronically under-stimulated. Too much minimalism can feel boring/under-stimulating, causing the brain to seek stimulation elsewhere. The balance: cognitively simple + perceptually adequate.

**casedock mapping**: Test with ADHD users specifically. Current calm design may need:
- Subtle animations (not distracting, but alive)
- Satisfying interaction feedback (checkmarks, transitions)
- Rich typography (already strong)
- Not empty/sterile feeling

**Status**: Needs user testing with ADHD population.

**Evidence**: Rosenberg 2023 (MIT Press) — cognitive load hurts, but perceptual engagement helps. Thread #2 (stimulation management).

---

#### 10. "Planning = procrastination" detector

**Insight**: ADHD users hyperfocus on organizing/planning as a form of procrastination. "Spent 3 weeks building Notion, used it 2 days." If a user edits specs for 20+ minutes without completing an Execution Item, they may be stuck in planning mode.

**casedock mapping**: If user edits Case spec/decisions for extended time without checking off Execution Items → gentle nudge: "Ready to start? Your next step is: [first unchecked item]." This is a suggestion, not a warning.

**Status**: Not implemented. Requires session tracking in UI.

**Evidence**: Thread #3 (OP spent 40 min organizing desk supplies), Thread #2 (Notion pattern).

---

### INTERESTING — Future possibilities

#### 11. Body doubling potential

**Insight**: Having someone in the room (even virtually) dramatically improves ADHD task completion. External accountability replaces unreliable internal motivation.

**casedock mapping**: When casedock becomes multi-user, shared focus sessions could be powerful. Even a "working on X" status indicator gives social presence. For V1 single-user: Focus module commitment is self-accountability.

**Status**: Future (multi-user version).

**Evidence**: Thread #1 (body doubling tip), Focusmate (real product success).

---

#### 12. Random task picker for decision paralysis

**Insight**: When ADHD brain can't choose what to do, removing the choice entirely works. "Have a robot pick one task at random from the list. For some reason, I can just START on it."

**casedock mapping**: "Pick for me" button on Board — randomly selects a Case or Focus item. Removes decision paralysis. One button, immediate action suggestion.

**Status**: Not implemented. Simple feature.

**Evidence**: Thread #3 (randomtaskpicker mention, Apple Shortcuts script).

---

#### 13. Time-awareness without time estimation

**Insight**: ADHD brains can't estimate time ("5 minutes can feel like 2 hours"). Don't ask for time estimates. Instead, show elapsed time and staleness automatically.

**casedock mapping**:
- Show "last updated X days ago" on Case cards
- Don't require due dates (ADHD brains lie about deadlines)
- Auto-detect staleness (already planned in board redesign)
- Optional: show how long a Case has been in each status

**Status**: Stale detection in plan. No time estimation requirements currently.

**Evidence**: Thread #1 (time blindness tips), Thread #2 (time estimation failure), Noreika 2017.

---

#### 14. Nightly "Your Day Tomorrow" preview

**Insight**: Waking up to a calm, realistic outline of the day's priorities reduces morning paralysis. One user reported this as the most effective feature of their tool.

**casedock mapping**: Email digest or morning view: "Here are your 1-3 things for today" based on Focus module. Calm, no guilt, just "here's what you committed to."

**Status**: Not implemented. Requires email infrastructure or dedicated landing view.

**Evidence**: Thread #3 (NotForgot user), Thread #2 (nightly planning pattern).

---

#### 15. Novelty via subtle variation, not replacement

**Insight**: ADHD brains habituate to systems after 2-4 weeks. The novelty decay cycle drives app abandonment. But rotating between entirely different tools is wasteful. The solution: subtle variation within one tool.

**casedock mapping**:
- Calm and Compact modes already provide two "looks"
- Consider: seasonal/minimal theme variations
- Progress indicators that change over time
- Weekly layout tweaks (not user-configured — automatic)
- Key: variation should be effortless, not another thing to manage

**Status**: Two display modes exist. More variation possible.

**Evidence**: Thread #2 (novelty decay cycle), Thread #3 ("rotate tools" comment).

---

## Alignment Summary

| Principle | casedock Feature | Status |
|-----------|-----------------|--------|
| 1. Show one next action | Case detail view | Needs implementation |
| 2. No shame for inactivity | Calm design, stale detection | Partial |
| 3. Limit visible cases | Focus module, Board design | Partial |
| 4. Zero-friction capture | Inbox | Implemented |
| 5. Auto-surface important things | Board landing, stale detection | In plan |
| 6. Micro-steps as core mechanic | Execution Items | Partial (AI breakdown not done) |
| 7. Satisfying completion feedback | Check-off UX | Needs implementation |
| 8. Accomplishment view | — | Needs implementation |
| 9. Calm but not under-stimulating | Current UI | Needs ADHD user testing |
| 10. Planning = procrastination detector | — | Needs implementation |
| 11. Body doubling | — | Future (multi-user) |
| 12. Random task picker | — | Simple feature, not started |
| 13. Time-awareness without estimation | Stale detection | In plan |
| 14. Nightly preview | — | Needs implementation |
| 15. Novelty via variation | Display modes | Partial |

---

## Rules for Future Sessions

When implementing any UI/UX change in casedock, verify against these principles:

1. **Does this ADD decisions or REMOVE them?** (Principles 1, 3, 4, 6)
2. **Could this trigger shame or avoidance?** (Principles 2, 8)
3. **Does this rely on user remembering?** (Principles 5, 13)
4. **Is the first thing a user sees an ACTION or INFORMATION?** (Principles 1, 6, 10)
5. **Would an ADHD user abandon this after 3 weeks?** (Principles 9, 15)

If any answer is concerning, reconsider the approach.

---

## Inversion as Design Method

The five verification questions above are not ad hoc heuristics — they are an application of **inversion**, a decision-making technique that asks "what would cause failure?" instead of "how do we achieve success?"

casedock's design uses **negative inversion** systematically:

- "Could this trigger shame?" → eliminate shame sources (Principle 2)
- "Would an ADHD user abandon this after 3 weeks?" → eliminate abandonment drivers (Principles 9, 15)
- "Does this ADD decisions?" → eliminate decision fatigue (Principles 1, 3, 4, 6)
- The hard rules ("no red badges, no gamification, no time estimation") are a failure-mode elimination list, not a feature list

This works because failure modes in productivity tools are finite and concrete, while success paths are infinite and abstract. Eliminating 3-4 specific failure modes delivers more value than chasing an ideal.

### Caveat: inversion and the rumination risk

Negative inversion is safe when applied to **product design** — we are evaluating the tool, not ourselves. But it becomes risky when surfaced as a **user-facing feature** for ADHD users.

Asking an ADHD user "what will make today a failure?" can trigger **rumination** — a well-documented ADHD pattern where negative scenarios are cognitively sticky and hard to disengage from. Negativity bias combined with attention-shifting difficulty makes failure-focused prompts potentially harmful for exactly the population casedock serves.

**Design rule**: if inversion is surfaced to users (e.g., a daily prompt or reflection view), use **positive inversion** ("imagine the day went well — what had to be true?") or frame negative inversion with agency language ("what can you set aside today?" instead of "what will go wrong?"). Same cognitive operation, different emotional frame.

The framing matters more than the technique. "Porażka" (failure) triggers shame. "Odrzucam" (I set aside) triggers agency. Both achieve the same reduction — but only one is safe for ADHD users.

---

*Related: [`docs/research/2026-06-adhd-reddit-community-insights.md`](../research/2026-06-adhd-reddit-community-insights.md) — full research data*
*Related: [`docs/research/2025-05-neurodiversity-summary.md`](../research/2025-05-neurodiversity-summary.md) — academic evidence base*
