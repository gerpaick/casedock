# MVP and Roadmap

## Product strategy

The MVP should prove one thing first:

> Can this solo-first core help an overloaded user turn incoming or self-created work into calmer, structured, finishable execution without depending on integrations?

Because of that, the MVP must focus on the internal work model, not on external integrations first.
It should validate the translation layer from incoming work to structured execution before it expands into connectors or broader integration surfaces.

## MVP positioning

MVP is:
- personal-use oriented
- single-user in v1
- calm interface
- ADHD-friendly in design posture, without medical framing
- focused on Cases, not task syncing
- valuable with zero live integrations

V1 should optimize for one user only, but the architecture should not block a later move to multi-user accounts and ownership.

## MVP goals

1. Let the user capture raw work.
2. Let the user convert raw work into Cases.
3. Let the user work inside a Case using:
   - spec
   - decisions
   - execution
   - private notes
4. Let the user define daily focus.
5. Let the user see work on a calm board.
6. Preserve enough structure for simple weekly load awareness once the core loop is proven.

## MVP scope

### Included in MVP
- Inbox Item model
- Case model
- Decision model
- markdown Spec
- Execution section
- Private notes
- Board view
- Inbox view
- Focus view
- search basics
- status model: Inbox / Active / Waiting / Done
- metadata: clarity / effort / work type
- source link model without requiring live sync

### Optional in MVP if time allows
- AI helper actions
- simple week view or weekly load surface
- recent activity feed
- case templates

### Explicitly out of MVP
- team collaboration
- multi-user workspaces
- mobile app
- heavy analytics
- time tracking suite
- full ClickUp replacement
- advanced workflow engine
- external sync write-back
- autonomous AI decisions or autonomous workflow changes

## MVP user stories

### Story 1
As a user, I want to quickly capture an idea or incoming task so I do not lose it.

### Story 2
As a user, I want to convert a rough item into a Case so I can think and work with structure.

### Story 3
As a user, I want a markdown spec inside a Case so I can keep context near the work.

### Story 4
As a user, I want to record decisions so I do not lose reasoning.

### Story 5
As a user, I want a practical execution area so I can move the Case forward.

### Story 6
As a user, I want private notes so I can think freely without polluting external systems.

### Story 7
As a user, I want to choose one main and two secondary focus items for the day.

### Story 8
As a user, I want the core workflow to stay useful even when no external task system is connected.

## Immediate post-MVP priorities

These items should be treated as the next product-strengthening layer after the current MVP core, not as speculative someday ideas:

- Weekly Work View or a similarly calm weekly load surface
- richer re-entry support so a Case more clearly shows recent decisions, recent movement, and the next concrete move
- AI-assisted triage, summarization, and Case drafting as explicit draft help
- optional activation helpers such as "why this matters" only if they stay lightweight and do not add workflow drag

## Phase 2

Once MVP proves useful, phase 2 can add source integrations as plugins.

### Strong candidates
- ClickUp read-only intake as the first connector
- source-linked Inbox Items from connector adapters
- “Convert from source” flow
- Jira, GitHub Issues, or Asana only after ClickUp validates the connector model
- Case activity timeline

## Phase 3

### Strong candidates
- heavier AI transforms and next-step support beyond the post-MVP draft helpers
- prepared update generation
- explicit review-based write-back to external systems
- artifact panel
- better search and filtering
- weekly review / heartbeat

## Product maturity path

### Phase 1
Personal calm execution core

### Phase 2
Personal calm workbench with source integrations as plugins

### Phase 3
AI-assisted personal execution layer with explicit reporting flows

### Phase 4
Polished product for overwhelmed solo builders and technical ICs

Scope decisions beyond the proven core loop should follow validated product value.
They should not back-drive MVP workflow scope or force UI changes before the core loop is proven.

## Risk notes

### Risk 1: overbuilding the execution model
Mitigation:
keep it light and always subordinate to the Case.

### Risk 2: recreating ClickUp in disguise
Mitigation:
keep source systems external and linked, not dominant.

### Risk 3: ADHD positioning done badly
Mitigation:
keep the tone respectful, practical, and clearly non-clinical.

### Risk 4: too much philosophy, not enough usability
Mitigation:
keep the default actions extremely practical:
- do now
- convert to Case
- park

### Risk 5: too many metadata fields
Mitigation:
prefer a small number of meaningful attributes.

## MVP success signals

The MVP is successful if the user starts to:
- process work in this system first
- rely on Cases for meaningful work
- feel less overwhelmed than in ClickUp or Jira-style tools
- recover interrupted work faster
- write decisions/specs naturally in the product
- keep using the product even before any live integration is enabled
