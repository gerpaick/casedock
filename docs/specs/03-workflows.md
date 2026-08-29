# Core Workflows

## Overview

The system should feel natural in everyday use.  
The workflow must support:
- quick action
- deeper shaping
- continued execution
- external accountability later through optional connectors

## Workflow 1 — Manual capture

### Goal
Allow the user to quickly store something without committing to work yet.

### Flow
1. User creates a quick item.
2. The item enters Inbox as an Inbox Item.
3. Later, the user triages it.

### Locked v1 capture input
- required: title
- optional: raw note or pasted fragment
- optional: source URL

### Locked v1 result
- captured items enter Inbox in `new` state
- if a source URL is provided, the item is treated as URL-backed input

### Good for
- rough idea
- bug thought
- reminder
- copied link
- note from a meeting

## Workflow 2 — Intake from external source

### Goal
Bring visible work pressure into a calmer environment.

### Flow
1. External task is shown in the Intake / To Address panel.
2. User sees a simplified card.
3. User chooses one of the actions:
   - Do now
   - Convert to Case
   - Set aside
   - Waiting on
   - Open in source

### Design principle
An external task is not yet “accepted” as structured work until the user triages it.

### v1.5 connector note
The first supported adapter may be ClickUp, but the workflow should stay generic enough for later Jira, Asana, GitHub Issues, or similar source systems.

## Workflow 3 — Do now

### Goal
Let quick items be handled immediately without over-structuring them.

### Flow
1. User opens Inbox Item or external-source intake card.
2. Chooses `Do now`.
3. Completes the action.
4. Optionally records a small completion note.
5. Later phases may allow sending a short update back to the source system.

### Locked v1 state result
- choosing `Do now` moves the Inbox Item to `doing_now`
- finishing the work moves the Inbox Item to `done`
- the optional completion note is stored on the Inbox Item in v1

### When to use
- tiny fixes
- small admin actions
- quick replies
- obvious, low-ambiguity tasks

## Workflow 4 — Convert to Case

### Goal
Turn fuzzy or meaningful work into a structured object.

### Conversion prompt
Keep the form intentionally light.

Suggested fields:
- working title
- outcome
- clear or fuzzy?
- next concrete step
- work type
- deep / medium / quick
- keep source link

### Result
System creates a Case with:
- title
- summary
- default markdown spec
- decision section
- execution section
- private notes area
- source link if applicable

### Locked v1 state result
- the new Case starts in `Active`
- the Inbox Item moves to `converted`
- the Inbox Item stores a reference to the created Case
- if the user keeps the source link, existing Source Links move to the Case
- if the Inbox Item only has a direct source URL, v1 creates one Case-level Source Link during conversion

### Why this matters
This is the central transformation of the product:
raw pressure becomes deliberate work.

## Workflow 5 — Continue a Case

### Goal
Help the user return to ongoing work without rebuilding context.

### On opening a Case, user should see
- current state
- summary
- next step
- recent decisions
- execution progress
- private notes

### Continue actions
- update spec
- add or promote a decision
- execute steps
- change status
- set as focus item

## Workflow 6 — Make a decision

### Goal
Capture choices without creating heavy process overhead.

### Inline path
User adds a quick decision line directly in the Case.

### Promote path
User turns it into a richer decision entry when it matters.

### Example triggers
- architecture choice
- “we will not do X in v1”
- narrowed scope
- implementation route selected

## Workflow 7 — Execution inside a Case

### Goal
Give a practical place for the work itself.

### Supported modes
- checklist
- light step groups
- simple doing/done sections

### Design warning
Do not let execution become a second giant task manager.

The Case execution area exists to support movement, not bureaucracy.

## Workflow 8 — Daily Focus

### Goal
Protect the day from overload.

### Model
User selects:
- one main Case
- two secondary Cases

### Benefits
- lowers mental spread
- makes priorities explicit
- improves start-of-day clarity

## Workflow 9 — Set Aside / Waiting On

### Goal
Keep work visible without keeping it mentally active.

### Set aside
For things not relevant now.

### Waiting on
For things blocked by:
- someone else
- pending info
- external response
- dependency

### Locked v1 state result
- `Set aside` moves the Inbox Item to `parked`
- `Waiting on` moves the Inbox Item to `waiting`

## Workflow 10 — External reporting later

### Goal
Maintain compatibility with workplace systems without forcing them into the whole UX.

### Later flow
1. User finishes meaningful work in the Case.
2. System prepares a compact update.
3. User reviews it.
4. System sends or helps send it to the source system.

This is explicitly not part of v1 core, but it should be anticipated in the design.
