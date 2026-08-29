# casedock MVP Implementation Plan

## Summary

This plan turns the current product spec into an implementation-ready sequence for the v1 MVP. The critical path is:

1. lock documentation and delivery rules
2. build the core domain model
3. deliver the main vertical flow: Inbox Item -> Case -> continued execution
4. add board, focus, and search surfaces
5. harden the product for real daily use

Coding should begin only after this plan and the canonical specs in `docs/specs/` are accepted as the working contract.

## Stage Order and Dependencies

1. `01-foundation-and-project-bootstrap.md`
   Depends on: canonical specs only
2. `02-core-domain-model.md`
   Depends on: Stage 1
3. `03-inbox-and-triage.md`
   Depends on: Stage 2
4. `04-case-workspace.md`
   Depends on: Stages 2 and 3
5. `05-decisions-and-execution.md`
   Depends on: Stage 4
6. `06-board-focus-and-search.md`
   Depends on: Stages 3, 4, and 5
7. `07-sources-clickup-ai-boundaries.md`
   Depends on: Stage 2 and should land before external integrations start
8. `08-hardening-and-release-readiness.md`
   Depends on: Stages 3 through 7

## Milestones

- Milestone A: repository and architecture conventions are fixed
- Milestone B: the domain and state model are implemented without spec gaps
- Milestone C: the main v1 workflow works end to end
- Milestone D: the product has its primary navigation surfaces
- Milestone E: the MVP is stable enough for sustained personal use

## Gates

- No coding before Stage 1 documentation is complete.
- No workflow implementation before Stage 2 domain rules are locked.
- No connector or AI helper work before Stage 7 boundaries are documented.
- Any product-significant ambiguity discovered during implementation must be resolved in `docs/` before implementation continues.

## Expected Deliverables

- A documentation-first repo layout with `docs/` as the sole source of truth.
- A modular Django monolith implementation that stays inside the documented boundaries.
- Tests for core domain transitions and critical HTML-first flows.
- A documented release gate for v1 MVP readiness.
