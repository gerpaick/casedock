# Inbox Focus-First UI

Date: 2026-04-05

## Context

The initial Inbox implementation was calm, but still presented too many equivalent actions and cards at once. For casedock's target user, that increased scan load right at the triage step where the product should reduce executive friction.

Stage 6 clarified navigation and density, but the Inbox surface still needed a stronger interaction pattern to support the product promise of turning incoming pressure into deliberate action.

## Decisions

- Inbox now uses a focus-first layout:
  - one `Now addressing` item is shown as the primary surface
  - the rest of ready Inbox items appear as a quieter queue
- The default selected Inbox item follows a fixed priority:
  - `doing_now`
  - `new`
  - `waiting`
  - `parked`
  - newest `updated_at` wins within a state
- Quick capture remains at the top of Inbox, but now keeps only the title field in the first layer.
- `Convert to Case` is the primary CTA on the selected Inbox item.
- `Do now` remains visible as a secondary CTA.
- `Set aside`, `Waiting on`, and `Open source` move into a quieter secondary action group.
- `Converted` and `Done now` remain visible as secondary history sections and should not dominate the main triage flow.

## Why

This keeps the Inbox aligned with the product principles:

- calm before power
- reduce executive friction
- triage before commitment
- ADHD-friendly, not medicalized

The page still shows the full state of the Inbox, but it now guides attention toward one deliberate decision at a time instead of presenting several equally loud options.
