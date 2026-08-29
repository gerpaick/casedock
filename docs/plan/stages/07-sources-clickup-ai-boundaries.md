# Stage 7: Source Connectors and AI Boundaries

## Goal

Prepare the product for source integrations and AI helpers without letting external systems or AI dominate the MVP.

## In Scope

- generic SourceLink behavior
- source snapshot expectations
- shared connector expectations in `sources`
- future ClickUp extension points as the first adapter
- AI-as-draft constraints
- privacy boundaries for source-linked work

## Out of Scope

- live ClickUp sync
- ClickUp write-back
- autonomous AI actions

## Prerequisites / Dependencies

- Stage 2 complete
- `docs/specs/06-clickup-integration.md`
- `docs/specs/09-architecture.md`

## Tasks

- Define the minimum v1 SourceLink data contract.
- Define how source-linked Inbox Items and Cases remain understandable without the external system.
- Define what connector adapters may do in later phases, with ClickUp as the first provider.
- Define what AI may draft, summarize, or propose and what always requires explicit user acceptance.
- Restate the hard rule that private notes never sync automatically.

## Deliverables

- documented integration boundaries
- documented connector boundary expectations
- implementation-ready SourceLink scope
- documented AI guardrails

## Acceptance Criteria

- Source data is linked, not dominant.
- The connector model remains provider-agnostic at the `sources` boundary.
- Private notes are unambiguously excluded from sync behavior.
- AI is documented as assistive, never autonomous in workflow decisions.

## Open Risks or Blocked Questions

- The eventual shape of AI result acceptance may need a later decision note, but the v1 boundary must remain fixed now.
