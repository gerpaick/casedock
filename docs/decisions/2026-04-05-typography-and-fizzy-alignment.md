# Typography And Fizzy Alignment

Date: 2026-04-05

## Context

The initial UI direction was calm, but it leaned too far into paper-like editorial styling. In practice, that made dense screens feel more text-heavy and less scannable than intended, especially for Inbox and Board.

The product specs and 37signals reference both call for a calmer structure with stronger operational clarity and a visual blend closer to Fizzy in chips, selected states, and readability.

## Decisions

- The shared UI typography shifts to a humane sans direction (`Inter` with system fallbacks).
- The shared visual system moves from beige/brown editorial tones toward a more neutral and blue-led palette.
- Page and section copy should stay shorter and more skimmable on key work surfaces.
- Board, Inbox, and Quick Capture should rely more on hierarchy, spacing, and selected states than on repeated explanatory text.
- Selected and active states should use more than color alone, such as border, weight, or marker treatment.

## Why

This keeps the UI calm while making it easier to scan and act. It also brings the app closer to the intended Basecamp/Fizzy blend:

- calm structure
- stronger readability
- low-noise cards
- confidence without flash
