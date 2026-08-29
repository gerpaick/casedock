# casedock Docs

`docs/` is the single source of truth for `casedock`.

The repository is intentionally **spec-driven-first**. Product behavior, architecture, workflow boundaries, and implementation sequencing must be documented here before code is added or changed.

## What the product is

**casedock** is a calm, solo-first execution system for overloaded technical builders and other knowledge workers who need a lower-friction path from incoming work to finishable work.

It is not a clone of Todoist.  
It is not a prettier ClickUp.  
It is a **personal execution layer** where incoming work can either be handled immediately or transformed into a structured working object called a **Case**.
Its core job is to act as a translation layer between incoming work pressure and calm, structured execution with strong re-entry support.

A Case can contain:
- decisions
- markdown spec / notes
- execution steps
- private working notes
- links to source systems such as ClickUp

The product must work as a strong solo system with **zero live integrations**. External systems such as ClickUp, Jira, or GitHub should be treated as optional task sources, not as the conceptual center of the app.

## Structure

- `specs/`
  Canonical product and architecture specification for v1.
- `specs/reference/`
  Non-canonical reference material and inspiration documents.
- `plan/`
  The implementation plan, stage breakdown, task lists, dependencies, and acceptance gates.
- `research/`
  ADHD and neurodiversity research, evidence base, and community insights that inform product decisions.
- `decisions/`
  Short decision notes for product-significant clarifications or implementation-driven changes.

## Canonical Reading Order

1. `specs/00-prd-v1.md`
2. `specs/01-product-vision.md`
3. `specs/02-domain-model.md`
4. `specs/03-workflows.md`
5. `specs/04-screens-and-ux.md`
6. `specs/05-mvp-and-roadmap.md`
7. `specs/06-clickup-integration.md`
8. `specs/07-example-task-flows.md`
9. `specs/08-stack.md`
10. `specs/09-architecture.md`
11. `plan/00-master-implementation-plan.md`
12. `research/2025-05-neurodiversity-summary.md`

## Working Rules

- `docs/specs/` is the implementation contract.
- If the docs conflict, stop and resolve the conflict in `docs/` before coding.
- If implementation reveals a missing product decision, add or update a spec or decision note first.
- Reference files under `specs/reference/` may inform the product, but they do not override canonical specs.

## Local Demo Data

For local UI preview, run `uv run python manage.py seed_demo`.

The command recreates the repo's prefixed demo records and refreshes today's Focus
selection with demo Cases, then seeds a complete Board, Inbox, Focus, and Case
workspace dataset so the app can be reviewed without empty states everywhere.

## Product Summary

**casedock** is a calm, ADHD-friendly, solo-first workbench for decisions and execution. It helps users turn incoming work into structured **Cases** that keep context, decisions, execution, private notes, and re-entry support close together without turning the product into another noisy enterprise task manager.
