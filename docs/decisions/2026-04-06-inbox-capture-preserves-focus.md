# Inbox Capture Preserves Current Focus

Date: 2026-04-06

## Context

Inbox already used a focus-first structure with one active `Now` item and a quieter `Queue`.
Manual capture still broke that rhythm because a newly captured item immediately replaced the current focus.

For casedock, capture should reduce the risk of losing work without hijacking the triage decision already in front of the user.

## Decisions

- `New Capture` no longer auto-selects the newly created Inbox item.
- If Inbox already has a selected `Now` item, capture returns to that same item.
- If Inbox was empty, the newly captured item becomes the only ready item and therefore appears in `Now`.
- Within the same ready-state priority, older items stay ahead of newer ones so fresh captures land at the bottom of `Queue`.

## Why

This keeps Inbox aligned with the product direction:

- capture without interruption
- one decision in front
- queue as quiet pressure, not attention theft
