# Inbox Recent Outcomes History

Date: 2026-04-07

## Context

Inbox already used a focus-first triage layout, but its lower history area still rendered `Converted` and `Done now` as two separate sections with similar visual weight.
That made the bottom of the screen read like a second dashboard instead of a quiet proof that work had been handled.

## Decisions

- Inbox history now appears as one `Recent outcomes` stream instead of two side-by-side sections.
- The stream mixes `converted` and `done` items by recency using `updated_at`.
- Each history row shows only:
  - outcome type
  - title
  - relative time
- `Converted` items link forward into the Case workspace.
- `Done now` items remain passive history entries in v1.
- The history block stays visible on `/inbox/`, but in a quieter treatment than the active triage surfaces.

## Why

This keeps Inbox aligned with the product direction:

- one decision in front
- calm before power
- history as orientation, not competition
- visible proof of progress without extra scan load
