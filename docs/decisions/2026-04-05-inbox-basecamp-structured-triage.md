# Inbox Basecamp-Structured Triage

Date: 2026-04-05

## Context

The first Inbox redesign improved prioritization, but the screen still read as a set of similarly weighted cards. That made the page feel softer than intended and forced the user to work too hard to find the next decision.

For casedock, Inbox is not a dashboard. It is a triage surface. The UI therefore needs a stronger answer to "what should I look at first?" while still keeping the rest of the pressure visible.

## Decisions

- Inbox shifts to a Basecamp-first structure:
  - one selected Inbox item becomes the clear workspace
  - the remaining ready items move into a softer structured queue
- Queue items should read as rows, not floating cards.
- The selected workspace remains the only strongly elevated surface on the page.
- Quick capture becomes a utility action near the top of the page instead of a visually loud block.
- Secondary history (`Converted`, `Done now`) remains visible, but in quieter list treatments that do not compete with active triage.
- Copy across Inbox should be trimmed aggressively:
  - keep only text that helps decide the next move
  - remove explanatory copy that only narrates the interface

## Why

This keeps Inbox aligned with the product direction:

- calm before power
- obvious next move
- less chrome, more content
- structured like Basecamp, without copying Basecamp screens directly
