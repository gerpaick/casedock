# Stage 2: Core Domain Model

## Goal

Lock the v1 data model and state rules so workflow implementation does not invent behavior on the fly.

## In Scope

- Inbox Item
- Case
- Decision
- Spec document
- Execution Item
- Focus Assignment
- Source Link
- status and metadata model
- privacy boundaries

## Out of Scope

- full ClickUp sync
- AI workflow execution
- advanced analytics

## Prerequisites / Dependencies

- Stage 1 complete
- `docs/specs/02-domain-model.md`
- `docs/specs/09-architecture.md`

## Tasks

- Define model fields and relationships for all MVP entities.
- Lock status transitions for Inbox and Case states.
- Lock metadata vocabulary for clarity, work type, effort, and related v1 attributes.
- Define the conversion relationship from Inbox Item to Case.
- Define the privacy boundary for private notes and any external-source records.
- Document future-ready assumptions that keep later multi-user support possible.

## Deliverables

- implementation-ready entity definitions
- documented state transitions
- documented privacy and ownership assumptions

## Acceptance Criteria

- The core objects and relationships can be implemented without guessing.
- State transitions are simple, explicit, and testable.
- Private notes are clearly separated from source-linked data.

## Open Risks or Blocked Questions

- If spec, private notes, and overview content overlap too much, a follow-up decision note may be needed to clarify ownership of those fields.
