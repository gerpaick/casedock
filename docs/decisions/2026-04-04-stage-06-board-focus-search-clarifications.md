# Stage 6 Clarifications

Date: 2026-04-04

## Context

Stage 6 required implementation-ready definitions for Board, Focus, Search, and the `Calm` / `Compact` display modes. The canonical specs already defined the product direction, but implementation needed a few narrower defaults to avoid inventing behavior case by case.

## Decisions

- Board uses the default v1 grouping recommended in the spec:
  - `Active`
  - `Waiting`
  - `Done recently`
- The Board keeps `Inbox` as a secondary side surface rather than a full mixed board column.
- Focus can be adjusted from two places in v1:
  - the dedicated `Focus` view for full daily rebalancing
  - quick actions on Board and Case pages for `Set main`, `Add secondary`, and `Remove focus`
- `Calm` and `Compact` change layout density only. They do not change workflows, information architecture, or available actions.
- The selected display mode is stored in session state in v1.
- Basic v1 search is intentionally simple and server-rendered.
- Search covers:
  - Case title
  - Case summary
  - Case next step
  - Spec markdown
  - Decision title and body
  - Execution item title and note
  - Inbox title, raw body, and source URL
- Search does not currently introduce saved filters, indexing infrastructure, or advanced search operators.

## Why

These defaults keep Stage 6 aligned with the calm, HTML-first MVP while still making the product usable day to day. They also keep the system from drifting into a heavier dashboard or search product before Stage 7 and Stage 8 are complete.
