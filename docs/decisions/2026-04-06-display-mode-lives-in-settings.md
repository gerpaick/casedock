# Display Mode Lives in Settings

Date: 2026-04-06

## Context

`Calm` and `Compact` remain part of the v1 product, but the global top bar was exposing the switch on every screen.
That added interface machinery to surfaces like Inbox and Board where the product should stay more focused on the work itself.

The existing `Settings` screen already had a dedicated display-mode control, so the product did not need a second entry point in shared chrome.

## Decisions

- Display mode remains a global preference stored in session state.
- The `Calm` / `Compact` switch is removed from shared top-level navigation.
- `Settings` is the only place where the user changes display mode in v1.
- Existing compact-mode layout behavior and the `settings/display-mode/` endpoint remain unchanged.

## Why

This keeps the interface aligned with the product direction:

- less chrome on work surfaces
- one clear place for product preferences
- calmer navigation across Inbox, Board, Focus, and Search
