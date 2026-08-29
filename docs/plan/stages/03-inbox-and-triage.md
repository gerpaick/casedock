# Stage 3: Inbox and Triage

## Goal

Deliver the intake layer that turns raw pressure into deliberate next actions.

## In Scope

- manual quick capture
- Inbox list and item presentation
- triage actions: Do now, Convert to Case, Park, Waiting
- lightweight completion note for Do now

## Out of Scope

- live ClickUp intake
- write-back to external systems
- advanced filtering

## Prerequisites / Dependencies

- Stage 2 complete
- `docs/specs/03-workflows.md`
- `docs/specs/04-screens-and-ux.md`

## Tasks

- Define the manual capture flow and minimum required input.
- Define Inbox states and display behavior.
- Define what each triage action changes in the model and UI.
- Define the conversion handoff into Case creation.
- Specify empty states and low-noise interaction expectations for Inbox.

## Deliverables

- implementation-ready triage workflow
- documented action outcomes
- documented UI expectations for the Inbox surface

## Acceptance Criteria

- A captured item can be triaged without ambiguity.
- Every triage action has a documented state result.
- Convert to Case is clearly defined as the central path for meaningful work.

## Open Risks or Blocked Questions

- The exact persistence model for Do now completion notes may need a short clarification if implementation exposes multiple reasonable shapes.
