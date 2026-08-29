# Stage 1: Foundation and Project Bootstrap

## Goal

Define the initial repository, tooling, architecture, and delivery rules before any feature work starts.

## In Scope

- repository layout and naming
- Django 6 modular monolith foundation
- HTML-first stack conventions
- environment and settings strategy
- testing and quality defaults
- documentation and decision-note workflow

## Out of Scope

- feature implementation
- production integrations
- non-essential infrastructure automation

## Prerequisites / Dependencies

- `docs/specs/00-prd-v1.md`
- `docs/specs/08-stack.md`
- `docs/specs/09-architecture.md`

## Tasks

- Define the repo skeleton under `src/` and the module boundaries from the architecture spec.
- Lock the default stack: Django templates, HTMX, Alpine.js, Tailwind, PostgreSQL, Redis, Celery.
- Define email-based auth as the only supported login direction for v1.
- Define local/dev/test environment conventions and required tooling.
- Define the baseline test stack around `pytest`.
- Add any missing implementation constraints to `docs/` before scaffolding begins.

## Execution Checklist

### 1.1 Repo and Source of Truth

- [x] Confirm `docs/` is the only source of truth.
- [x] Confirm the canonical reading order in `docs/README.md`.
- [x] Lock the rule that architecture or workflow changes land in `docs/` before code.
- [x] Confirm whether a clarification belongs in `docs/specs/` or `docs/decisions/`.

### 1.2 Project Skeleton Decision

- [x] Approve the target project layout under `src/`.
- [x] Confirm which modules start as separate Django apps.
- [x] Define the required directories in the initial scaffold.
- [x] Lock naming conventions for apps, templates, static assets, tests, and config.

### 1.3 Stack Lock

- [x] Lock the Python runtime direction for v1.
- [x] Lock Django 6 as the framework baseline.
- [x] Lock the UI stack: Django templates, HTMX, Alpine.js, Tailwind.
- [x] Lock the data and async stack: PostgreSQL, Redis, Celery.
- [x] Explicitly record what is out of bounds for v1: SPA, microservices, frontend/backend split, workflow engine.

### 1.4 Auth and Security Defaults

- [x] Confirm email-based authentication as the only v1 login direction.
- [x] Exclude username-centric product flows.
- [x] Record the single-user-now, future-safe-later auth assumption.
- [x] Record the hard rule that private notes never sync without explicit user action.

### 1.5 App Boundaries

- [x] Confirm the core module list: `inbox`, `cases`, `decisions`, `execution`, `focus`, `sources`, `clickup`, `ai`.
- [x] Write a short responsibility statement for each module.
- [x] Record that `Case` is the core object, not a generic task.
- [x] Record that ClickUp and AI are extensions around the core MVP workflow, not the center of the product.

### 1.6 Environment and Config

- [x] Define the minimum supported environments: `local`, `test`, and later `prod`.
- [x] Define the required environment variables for initial bootstrap.
- [x] Define the Django settings strategy.
- [x] Define what is mandatory for local startup versus what can be deferred.

### 1.7 Testing and Quality Defaults

- [x] Lock `pytest` as the default test runner.
- [x] Define the minimum test expectations for new workflows.
- [x] Record that core HTML-first flows and state transitions are the primary coverage target.
- [x] Lock baseline quality tools such as `ruff`, with optional additions clearly marked.
- [x] Define the minimum quality gate required before leaving the foundation stage.

### 1.8 UX and Product Guardrails

- [x] Reconfirm the UI direction: calm, text-first, low-noise.
- [x] Reconfirm support for both `Calm` and `Compact` display modes.
- [x] Record the anti-patterns to avoid: enterprise density, dashboard clutter, gamified microcopy.
- [x] Record HTML-first delivery and small HTMX/Alpine interactions as the default interface model.

### 1.9 Ready-to-Start Gate

- [x] Verify there are no unresolved conflicts between canonical specs.
- [x] Verify Stage 2 can begin without making fresh architecture decisions.
- [x] Mark Stage 1 done only when the project can be scaffolded from `docs/` alone.

## Resolution Notes

Stage 1 is resolved by:
- `docs/README.md` as the source-of-truth and reading-order contract
- `docs/specs/08-stack.md` for runtime, layout, tooling, settings, env, and quality defaults
- `docs/specs/09-architecture.md` for module boundaries and code ownership rules

## Deliverables

- documented project structure
- documented environment assumptions
- documented testing defaults
- confirmed architectural boundaries

## Acceptance Criteria

- An implementer can scaffold the project without making architecture decisions.
- Stack, auth, and testing defaults are unambiguous.
- There is no competing source of truth outside `docs/`.

## Definition of Done

- The starting architecture is unambiguous.
- The stack is locked.
- Module boundaries are documented.
- Auth, privacy, and testing defaults are documented.
- The project can be scaffolded without guesswork.

## Open Risks or Blocked Questions

- Exact local environment bootstrap may need a short decision note if tool choices expand beyond current specs.
