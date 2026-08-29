# Architecture v1

## Architecture goal

The architecture should support a product where:
- incoming work can be captured or imported
- work is triaged into immediate action or structured work
- structured work lives as a Case
- Cases combine thinking and execution
- the core experience remains valuable without integrations
- the system remains calm, understandable, and extensible

The architecture should be:
- modular
- HTML-first
- easy to evolve
- ready for later integrations
- safe for private notes and layered external sync
- supportive of respectful ADHD-friendly workflow design

## Implementation principles

- Work **spec-driven-first**: `docs/specs` defines intended behavior, terminology, and workflow.
- V1 is single-user only, but architecture should remain compatible with a later multi-user model.
- Use email-based authentication in the product UI rather than username-based login.
- Default to Django 6 and `pytest`.
- When implementation exposes a conflict or meaningful gap in the spec, stop and clarify before encoding product behavior.

## Architectural style

## Modular monolith
V1 should be built as a **modular monolith**.

Meaning:
- one deployable application
- shared database
- separated domain modules
- clear boundaries inside the codebase
- no premature distributed architecture

This is the best fit for:
- product discovery
- speed of iteration
- solo development
- refactoring as the model matures

## Initial code boundaries

The initial scaffold should mirror the architectural boundaries directly in code.

Required starting shape:
- `src/config/` for Django project configuration, settings modules, URL wiring, and ASGI/WSGI entrypoints
- `src/apps/core/` for shared cross-cutting concerns only, such as the custom user model, shared base models, timestamps, and non-domain utilities
- `src/apps/ui/` for shared layout, template tags, reusable partials, and design-system-level presentation helpers
- one Django app per documented domain module: `inbox`, `cases`, `decisions`, `execution`, `focus`, `sources`, `clickup`, `ai`

Boundary rules:
- keep product behavior in the owning domain app or in explicit application-layer services close to that domain
- do not create a generic task app or generic workflow engine
- do not move Case-centered behavior into `core` or `ui`
- keep `clickup` and `ai` as extension modules around the core workflow, not as organizing centers for the product
- prefer narrow cross-app dependencies and avoid circular imports between domain modules

## High-level system map

```text
[ Browser ]
    |
    v
[ Django UI layer ]
    |
    +--> Inbox module
    +--> Cases module
    +--> Decisions module
    +--> Execution module
    +--> Focus module
    +--> Sources module
    +--> AI helpers
    |
    v
[ PostgreSQL ]
    |
    +--> Redis / Celery for background work
    |
    +--> external integrations later (ClickUp first, more connectors later)
```

## Main architectural layers

### 1. Presentation layer
Responsible for:
- pages
- partial HTMX updates
- forms
- side panels
- actions
- command-like flows

Examples:
- Inbox view
- Board view
- Case detail page
- Focus view
- conversion modal/panel

### 2. Application layer
Responsible for:
- orchestration of workflows
- converting Inbox Item to Case
- promoting quick work to Case
- marking focus
- recording decisions
- generating source updates

This layer should contain the product behavior, not just raw CRUD.

### 3. Domain layer
Responsible for:
- business meaning of entities
- state transitions
- validation rules
- Case logic
- link rules between source and internal objects
- privacy boundaries for notes

### 4. Infrastructure layer
Responsible for:
- database
- background jobs
- source integrations later
- email sending
- AI API calls
- caching

## Core modules

## 1. `inbox`
Purpose:
manage incoming work before it becomes structured work.

Responsibilities:
- create Inbox Items
- store raw incoming data
- handle triage actions
- support quick actions such as Do now / Convert / Set aside / Waiting on

Main concepts:
- InboxItem
- inbox source reference
- triage state

## 2. `cases`
Purpose:
manage the main work object.

Responsibilities:
- create and update Cases
- render Case overview
- store summary and work metadata
- hold the central lifecycle of meaningful work

Main concepts:
- Case
- CaseStatus
- CaseType
- CaseClarity
- CaseEffort

## 3. `decisions`
Purpose:
store and evolve decisions made within a Case.

Responsibilities:
- inline decisions
- promoted decisions
- decision history
- decision rationale

Main concepts:
- Decision
- promoted vs inline model
- consequence / alternatives / rationale

## 4. `execution`
Purpose:
track practical forward movement.

Responsibilities:
- execution items
- checklists
- grouped steps
- progress notes

Main concepts:
- ExecutionItem
- execution section/group
- completion state

## 5. `focus`
Purpose:
support daily anti-overwhelm planning.

Responsibilities:
- select 1 main Case
- select 2 secondary Cases
- render focus view
- support quick daily rebalancing

Main concepts:
- FocusAssignment
- focus date
- focus role: main / secondary

## 6. `sources`
Purpose:
abstract external origin systems and connector boundaries.

Responsibilities:
- generic SourceLink records
- generic connector / provider abstractions
- external snapshots
- sync timestamps
- source metadata

Main concepts:
- ExternalSource
- SourceLink
- source payload snapshot

## 7. `clickup`
Purpose:
first optional connector module for phase 2+

Responsibilities:
- auth / API connectivity
- task import
- snapshot refresh
- webhook handling later
- prepared write-back later

Main concepts:
- ClickUp connection
- ClickUp task snapshot
- import job
- sync log

## 8. `ai`
Purpose:
assist, not dominate.

Responsibilities:
- summarize Inbox Items
- propose Case draft
- propose next steps
- extract decisions
- generate update drafts

Main concepts:
- AI job request
- AI result draft
- explicit accept/reject flow

## Core entities and relationships

## InboxItem
Represents raw incoming work.

Suggested fields:
- id
- title
- raw_body
- source_type
- status
- parked flag or state
- waiting flag or state
- created_at
- updated_at

Relationships:
- may have one or more SourceLinks
- may be converted into one Case

## Case
Represents structured work.

Suggested fields:
- id
- title
- summary
- status: Inbox / Active / Waiting / Done
- clarity: clear / fuzzy
- effort: quick / medium / deep
- work_type: build / debug / research / admin / reply
- created_at
- updated_at

Relationships:
- belongs to zero or more SourceLinks
- has one Spec document
- has many Decisions
- has many ExecutionItems
- has many private notes
- may be included in Focus

## SpecDocument
Represents markdown-first work context.

Suggested fields:
- case_id
- markdown_body
- rendered_cache optional
- updated_at

## Decision
Represents reasoning and choice.

Suggested fields:
- case_id
- title
- body
- promoted boolean
- rationale
- alternatives
- consequence
- created_at

## ExecutionItem
Represents a practical step.

Suggested fields:
- case_id
- title
- state
- section
- order
- note
- created_at
- completed_at

## PrivateNote
Represents user-only thoughts.

Suggested fields:
- case_id
- body
- created_at
- updated_at

## SourceLink
Represents external origin linkage.

Suggested fields:
- provider
- external_id
- external_url
- external_title_snapshot
- external_status_snapshot
- payload_snapshot
- synced_at

## FocusAssignment
Represents today's chosen work.

Suggested fields:
- date
- case_id
- role: main / secondary
- order

## Key workflows in architecture terms

## Workflow 1: Capture item
1. User creates a quick item.
2. System stores it as InboxItem.
3. Item appears in Intake view.

## Workflow 2: Import source item
1. External task is fetched or imported.
2. System stores source snapshot.
3. System creates or updates InboxItem linked to that source.

## Workflow 3: Convert Inbox Item to Case
1. User clicks Convert to Case.
2. Conversion form gathers minimal shaping input.
3. Application layer creates Case.
4. System creates SpecDocument.
5. Source links are attached.
6. InboxItem is marked converted or archived.

## Workflow 4: Do now
1. User chooses a quick item.
2. A lightweight work session is opened.
3. User resolves or investigates it.
4. Result is either completed directly or promoted to Case.

## Workflow 5: Promote quick work to Case
1. User starts in Do now mode.
2. Complexity grows.
3. User promotes work to Case.
4. Existing notes/checklist are preserved and transferred.

## Workflow 6: Record decision
1. User adds a small decision inline.
2. If needed, user promotes it to a fuller Decision record.
3. Decision becomes part of Case history.

## Workflow 7: Build daily focus
1. User selects 1 main Case.
2. User selects 2 secondary Cases.
3. Focus view surfaces only these items.

## State model

## InboxItem state
Suggested states:
- new
- doing_now
- converted
- parked
- waiting
- done
- archived

This can later be simplified or normalized depending on implementation taste.

## Case state
Chosen product model:
- Inbox
- Active
- Waiting
- Done

This should remain intentionally small.

Other useful attributes should not be forced into status:
- clarity
- effort
- work type
- source presence
- focus role

## UI architecture

## Primary views
- Home Board
- Intake / To Address
- Case detail
- Focus view
- later: source connector panel

## UI pattern recommendations
- page shell is server-rendered
- boards update via HTMX partials
- side panels use partial templates
- conversion flow uses small modal or side sheet
- markdown editor remains simple in v1
- avoid over-animated UI

## Permissions and privacy

V1 is single-user, but privacy boundaries still matter and later multi-user boundaries should stay possible.

Rules:
- private notes never sync externally by default
- AI outputs based on private notes should be user-reviewed before external posting
- source snapshots are references, not the primary thinking layer

This matters especially for future external write-back.

## Integration architecture

## V1
No active integration required.
Use generic source model only.
The core Case workflow must stay complete and useful with manual capture alone.

## V1.5 / Phase 2
Add plugin-style source adapters:
- shared connector contract in `sources`
- ClickUp as the first read-only adapter
- connection settings
- manual sync
- assigned-to-me import
- task snapshot storage
- InboxItem generation

## Phase 3
Add write-back:
- comment draft
- explicit comment send
- optional status update
- webhook refresh

This should remain explicit and review-based rather than automatic.

## AI architecture

AI should be treated like a drafting subsystem.

Pattern:
1. User requests an AI action.
2. Action is executed synchronously or via background job.
3. Result is stored as a suggestion.
4. User accepts, edits, or discards.

Never:
- auto-overwrite Case content silently
- auto-post to an external source
- auto-promote raw notes without confirmation

## Background jobs

Jobs likely needed soon:
- source import
- source refresh
- webhook processing
- AI transforms
- markdown render cache refresh if used
- search indexing later
- outbound email tasks later

These should go through Celery.

## Observability and operations

Even in v1, add basic operational structure:
- structured application logs
- job failure logging
- sync error history for integrations later
- admin visibility into InboxItem / Case conversion

This prevents invisible failures once connectors or AI arrive.

## Testing strategy

Recommended layers:
- `pytest` for all automated test layers
- unit tests for state transitions and conversion logic
- integration tests for key workflows
- request tests for core views
- background job tests for import and AI helpers later

Priority test targets:
- Inbox Item -> Case conversion
- Do now -> promote to Case
- decision promotion
- focus assignment rules
- private note visibility rules

## Recommended first implementation order

### Step 1
Core models:
- InboxItem
- Case
- SpecDocument
- Decision
- ExecutionItem
- PrivateNote
- FocusAssignment

### Step 2
Core views:
- Board
- Intake
- Case detail
- Focus

### Step 3
Core workflows:
- capture item
- convert to Case
- do now
- promote to Case
- add decision
- add execution item

### Step 4
Refine UX:
- calm mode
- compact mode
- quick actions
- card summaries

### Step 5
Add source abstraction and connector contract

### Step 6
Add ClickUp connector

## Final architectural recommendation

Build v1 as a **modular Django monolith** centered around:
- Inbox
- Case
- Decision
- Spec
- Execution
- Focus

Keep the architecture:
- simple
- calm
- explicit
- markdown-friendly
- source-aware but not source-dominated

This is the architecture most aligned with the product vision.
