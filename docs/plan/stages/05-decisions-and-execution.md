# Stage 5: Decisions and Execution

## Goal

Add practical movement inside a Case while avoiding task-manager sprawl.

## In Scope

- inline decisions
- promoted decisions
- lightweight execution items
- simple completion and progress behavior

## Out of Scope

- heavy workflow engines
- dependency graphs
- advanced planning boards inside a Case

## Prerequisites / Dependencies

- Stage 4 complete
- `docs/specs/02-domain-model.md`
- `docs/specs/03-workflows.md`

## Tasks

- Define the difference between inline and promoted decisions.
- Define the minimum fields for promoted decisions.
- Define the allowed execution shapes for v1.
- Define the minimal set of state transitions inside execution.
- Specify UI constraints that keep execution lightweight and subordinate to the Case.

## Deliverables

- implementation-ready decision model behavior
- implementation-ready execution model behavior
- documented constraints that prevent overbuilding

## Acceptance Criteria

- A user can capture meaningful reasoning without creating process overhead.
- Execution supports movement but does not dominate the product.
- Decisions and execution remain tightly coupled to the Case context.

## Open Risks or Blocked Questions

- If grouped execution steps and flat checklist items both remain in scope, implementation may need one follow-up decision to choose the default presentation.
