# Stage 4: Case Workspace

## Goal

Define the main working surface where a Case becomes understandable, actionable, and recoverable later.

## In Scope

- Case creation from Inbox
- Case overview
- markdown spec area
- private notes area
- links area
- continue-work surface

## Out of Scope

- rich collaboration features
- file attachments or artifacts beyond simple links
- external publishing or sync

## Prerequisites / Dependencies

- Stages 2 and 3 complete
- `docs/specs/02-domain-model.md`
- `docs/specs/04-screens-and-ux.md`

## Tasks

- Define the conversion form inputs and Case defaults.
- Define the required overview fields for every Case.
- Define how the spec is stored and rendered as a markdown-first document.
- Define the private-notes surface as user-only and non-syncing.
- Define the links section and allowed link types for v1.
- Specify what must be visible so the user can resume work without rebuilding context.

## Deliverables

- implementation-ready Case creation workflow
- implementation-ready Case page structure
- documented rules for spec, private notes, and links

## Acceptance Criteria

- A Case page is understandable in isolation.
- The spec, decisions, execution, and private notes each have a clear role.
- The conversion flow produces a useful default Case with minimal friction.

## Open Risks or Blocked Questions

- If implementation pressure pushes too much content into Overview, a decision note may be required to keep section boundaries calm and durable.
