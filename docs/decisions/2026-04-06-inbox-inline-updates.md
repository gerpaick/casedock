# Inbox Inline Updates Preserve Triage Context

Date: 2026-04-06

## Context

Inbox already used a focus-first layout, but selecting an item from `Queue` or capturing a new item still caused a full page reload.
That reset scroll to the top and broke the calm, continuous triage rhythm the screen is meant to support.

The product stack already prefers HTML-first interactions with partial updates over heavier client-side state.

## Decisions

- Inbox selection from `Queue` now updates in place instead of reloading the full page.
- Quick capture from the Inbox modal now refreshes the Inbox fragment in place on success.
- `Set aside` and `Waiting on` from the selected Inbox item now refresh the Inbox fragment in place.
- Full-page links and form submissions remain valid fallbacks when HTMX is unavailable.
- The selected item remains represented in the URL with `?selected=...` during inline updates.

## Why

This keeps Inbox aligned with the product direction:

- one decision in front
- less visual interruption
- calmer handling of incoming work
- HTML-first before custom client state
