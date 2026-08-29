# Source Integrations Concept

ClickUp is the first expected connector, but the model should remain compatible with other source systems later.

## Positioning

Integrations are useful, but they should not define the product core.

The product core is:
- Case
- Decision
- Spec
- Execution
- Focus

Source integrations are **intake and accountability features**.

## Design principle

**External task != Case**

An external task becomes:
- an Inbox Item reference
- then optionally a Case

This distinction must remain clear in both data model and UI.

## Why this matters

If every external task becomes a Case automatically:
- the new app inherits external-system chaos
- the user loses the calming effect
- the product becomes a thin integration shell, which is not the goal

## Recommended v1.5 / phase 2 approach

Start with:
- plugin-style connector boundary
- read-only access
- assigned-to-me tasks only
- intake panel display
- manual conversion to Case

This aligns exactly with user intent:
- still see work tasks
- still stay accountable
- but process them in a better environment

The first connector can be ClickUp, but the flow should stay provider-agnostic at the `sources` layer.

## Intake panel behavior

Show only a simplified representation:
- title
- short description excerpt
- due date if useful
- source status
- link to the source system

### Available actions
- Do now
- Convert to Case
- Set aside
- Waiting on
- Open in source

Not in initial integration:
- editing all provider fields
- heavy bidirectional sync
- full mirrored workspace behavior

## Data model suggestion

### ExternalSource
Generic record for connected systems.

Fields:
- provider
- connection kind / adapter type
- external_id
- external_url
- payload snapshot
- synced_at

### SourceLink
Attached to Inbox Item or Case.

Fields:
- source type
- external title snapshot
- external status snapshot
- assignee snapshot if relevant
- last external update

## Sync rules

### Rule 1
Source data should be refreshable, but not constantly dominant in the UI.

### Rule 2
Cases may outgrow the original source task and should not be flattened back into it.

### Rule 3
Private notes must never sync by default.

## Future integration features

### Phase 3 possible write-back actions
- add comment to the source system
- prepare status update
- change source status
- mark progress externally

### Best write-back design
Keep write-back explicit and review-based.

Example:
1. User completes meaningful work in a Case.
2. App suggests an update.
3. User edits if needed.
4. User sends it to the source system.

This is much safer than invisible sync.

## UX expectations

The user should feel:
- “I still see my work obligations”
- “I do not need to live inside the source system”
- “I can think privately before reporting back”
- “I can convert pressure into structure”

## Anti-patterns to avoid

- full provider clone view
- too many provider fields in cards
- automatic Case creation from everything
- forced bidirectional sync from day one
- sync of private/internal notes

## Final recommendation

Treat ClickUp and later connectors like:
- a port of entry
- a reference system
- a reporting endpoint later

Do not treat it like the conceptual center of the product.
