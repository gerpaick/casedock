# Stage 6: Board, Focus, and Search

## Goal

Deliver the primary navigation surfaces that make the workbench usable day to day.

## In Scope

- Board view
- Focus view
- basic search
- Calm and Compact display modes

## Out of Scope

- advanced saved filters
- analytics dashboards
- command-palette-grade search

## Prerequisites / Dependencies

- Stages 3, 4, and 5 complete
- `docs/specs/04-screens-and-ux.md`
- `docs/specs/05-mvp-and-roadmap.md`

## Tasks

- Define the Board grouping and default information hierarchy.
- Define Focus behavior with exactly 1 main and up to 2 secondary Cases.
- Define the minimum v1 search surface and searchable fields.
- Define how Calm and Compact affect layout density without changing product behavior.
- Specify the minimum navigation structure across Board, Inbox, Focus, Search, and Settings.

## Deliverables

- implementation-ready Board definition
- implementation-ready Focus definition
- implementation-ready basic search definition

## Acceptance Criteria

- The user can see active work without overload.
- The Focus view enforces the documented anti-overwhelm model.
- Search is sufficient for basic retrieval without introducing extra infrastructure.

## Open Risks or Blocked Questions

- If multiple board grouping modes are kept for v1, implementation may need a default-order clarification.
