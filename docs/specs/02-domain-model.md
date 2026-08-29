# Domain Model

## Overview

The product uses a layered model:

1. **Inbox Item** — raw incoming work
2. **Case** — the main working entity
3. **Decision** — reasoning and chosen direction
4. **Spec** — markdown context and working document
5. **Execution Item** — concrete steps toward completion
6. **Focus Assignment** — today's explicit priorities
7. **Source Link** — connection to an external source system or direct reference URL

## 1. Inbox Item

### Purpose
Represents something that has entered the system but has not yet been fully interpreted.

### Sources
- external task via connector, with ClickUp as the first expected provider
- manual quick capture
- pasted note
- URL
- future sources: Jira, GitHub Issues, email, Slack, clipboard import

### Key attributes
- title
- source type / provider
- raw description
- source URL
- created at
- last updated at
- triage state

> Removed in v1 (2026-07-28): `source_reference` and `raw_metadata_snapshot` were reserved for external-source connectors (ClickUp, Jira, GitHub) that have been deferred indefinitely per ADR `2026-07-17-ai-agent-pressure-and-mcp-direction.md`. They will be re-introduced when a connector lands. The `SourceLink` model remains the canonical way to attach an external reference to an InboxItem or Case in v1.

### Locked v1 source types
- `manual`
- `clickup`
- `url`
- `note`
- `other`

### Triage actions
- Do now
- Convert to Case
- Set aside
- Waiting on
- Open source
- Archive
- Later: send update back

### Locked v1 inbox states
- `new`
- `doing_now`
- `converted`
- `parked`
- `waiting`
- `done`
- `archived`

### Locked inbox transition rules
- `new` can move to `doing_now`, `converted`, `parked`, `waiting`, `done`, or `archived`
- `doing_now` can move to `converted`, `waiting`, `done`, or `archived`
- `converted` can only move to `archived`
- `parked` can move back to `new`, or forward to `doing_now`, `converted`, `waiting`, or `archived`
- `waiting` can move to `new`, `doing_now`, `converted`, `done`, or `archived`
- `done` can only move to `archived`
- `archived` is terminal in v1

### Locked relationship rule
- an Inbox Item may reference at most one converted Case
- only an Inbox Item in `converted` or `archived` state may keep that Case reference (archival preserves the converted-case link from before so provenance survives cleanup)

## 2. Case

### Purpose
A Case is the main unit of real work in the system.

It is where raw incoming work becomes:
- understandable
- actionable
- recoverable later
- linked to decisions and execution
- easier to resume after interruption

### Why Case is the core object
`Case` is preferred over `Bet` because it can gracefully handle:
- small but important items
- medium fuzzy tasks
- larger technical work
- follow-up on external tasks

### Core attributes
- title
- slug / short reference
- summary
- status
- clarity level
- work type
- effort level
- next step
- source badge
- created at
- updated at
- completed at
- archived at

### Status model
Keep status intentionally simple:
- Inbox
- Active
- Waiting
- Done

### Locked case transition rules
- `Inbox` can move to `Active`, `Waiting`, or `Done`
- `Active` can move to `Waiting` or `Done`
- `Waiting` can move to `Active` or `Done`
- `Done` can move back to `Active` or `Waiting`

### Helpful metadata
- `clarity`: clear / fuzzy
- `work_type`: build / debug / research / admin / reply
- `effort`: quick / medium / deep
- `energy`: deep / shallow
- `source_type`: clickup / manual / url / other

### Locked v1 metadata vocabulary
- `clarity`: `clear`, `fuzzy`
- `work_type`: `build`, `debug`, `research`, `admin`, `reply`
- `effort`: `quick`, `medium`, `deep`
- `energy`: `shallow`, `deep`

### Locked relationship rules
- a Case has exactly one Spec document
- a Case may have many Decisions
- a Case may have many Execution Items
- a Case may have many Private Notes
- a Case may have many Source Links

### Lifecycle defaults
- slug is generated from title when the Case is first created
- `completed_at` is recorded when a Case enters `Done`
- `completed_at` is cleared if the Case later leaves `Done`

### User expectations
A Case should tell the user:
- what this is about
- why it matters
- what the current interpretation is
- what happens next

## 3. Decision

### Model choice
Decisions exist in two forms:
- inline decision note inside a Case
- promoted decision record when needed

### Inline decision
Good for:
- quick choices
- local tradeoffs
- light interpretation

Fields:
- text
- timestamp
- optional tag

### Promoted decision
Good for:
- architecture choices
- scope changes
- implementation strategy
- communication-critical reasoning

Fields:
- title
- context
- decision
- why
- alternatives considered
- consequence
- timestamp

### Locked v1 rule
- promoted decisions require a title

## 4. Spec

### Purpose
The spec is the markdown-first working document inside a Case.

It can be:
- tiny
- medium
- a real structured work doc

### Expected sections
Suggested, not mandatory:
- Context
- Problem
- Desired outcome
- Notes
- Constraints
- Edge cases
- Implementation idea
- Questions

## 5. Execution Item

### Purpose
Execution Items are concrete actions inside a Case.

They must remain lightweight.

### Design principle
Avoid rebuilding Jira inside the Case.

### Allowed shapes
- checklist item
- grouped steps
- lightweight lane sections
- status note on current execution state

### Example structure
- To do
- Doing
- Done

Or simply:
- checklist with light state

### Locked v1 execution states
- `todo`
- `doing`
- `done`

### Lifecycle default
- `completed_at` is recorded when an Execution Item enters `done`
- `completed_at` is cleared if it later leaves `done`

## 6. Focus Assignment

### Purpose
Explicitly define the day.

### Model
The user picks:
- 1 main Case
- 2 secondary Cases

This is not a calendar system.
It is a mental load control mechanism.

### Locked v1 assignment rules
- one `main` Focus Assignment per day
- up to two `secondary` Focus Assignments per day
- `main` uses slot order `1`
- `secondary` uses slot order `1` or `2`
- the same Case cannot occupy more than one focus slot on the same day

## 7. Source Link

### Purpose
Connect a Case or Inbox Item to an external system.

### Example: external source
Store:
- provider
- external task ID
- external URL
- source title snapshot
- source status snapshot
- source updated at

ClickUp is the first expected connector, but the data contract should stay compatible with other providers later.

### Locked v1 provider vocabulary
- `clickup`
- `manual`
- `url`
- `other`

### Locked v1 targeting rule
- a Source Link belongs to exactly one target object: either an Inbox Item or a Case
- Source Links do not attach to Private Notes

## Relationship summary

- Inbox Item may convert into one Case
- Case may have many Decisions
- Case has one Spec document
- Case has many Execution Items
- Case may have many Source Links
- Case may be part of Daily Focus

## Design rules

1. Never let raw source data dominate the Case.
2. Keep external references linked, not embedded everywhere.
3. Make the Case page understandable in isolation.
4. Keep state simple and metadata rich.
5. Private Notes remain Case-local and are never modeled as externally synced records.
6. The core model must remain useful even when every item comes from manual capture.
