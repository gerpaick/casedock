# Quick Capture Modal

Date: 2026-04-05

## Context

The Inbox redesign made triage calmer, but the always-visible quick capture form still carried more visual weight than the action deserved. Capture should feel immediate and pleasant without adding another large panel to the page.

At the same time, casedock remains HTML-first, so quick capture cannot rely exclusively on client-side interaction.

## Decisions

- `Quick capture` becomes a quiet editorial link on the Inbox page instead of a permanently visible form block.
- On `/inbox/`, clicking that link opens a modal with the capture form as a progressive enhancement.
- The link remains a real link and points to a dedicated fallback page for capture.
- The modal and fallback page use the same capture form and copy tone.
- If capture validation fails from the modal path, Inbox re-renders with the modal reopened.
- If capture validation fails from the fallback page, the dedicated page re-renders with errors in place.

## Why

This preserves the HTML-first contract while reducing clutter on the main Inbox surface. It also makes quick capture feel lighter and more intentional, which better matches the calm, ADHD-friendly direction of the product.
