# Screens and UX Direction

## UX intent

The product should feel:
- calm
- capable
- text-first
- developer-friendly
- intentionally constrained
- supportive for overload-prone users

Current implementation note:
the current UI direction is being refined, not reset. Strategic documentation may sharpen positioning and later workflow priorities, but it should not be read as a mandate to redesign the current Board, Inbox, Focus, or Case surfaces during the present polish pass.

Visual inspiration:
- Fizzy
- Basecamp
- calm internal tools
- modern markdown-first apps

## UI principles

### 1. No enterprise density by default
Dense layouts can exist as an option, but calm should be the default.

### 2. Strong typography
The product should rely on clean information hierarchy more than on decoration.

### 3. Quiet chrome
Borders, shadows, colors, and badges should be restrained.

### 4. Content over controls
The user should see work, not interface machinery.

### 5. Two display modes
- Calm
- Compact

Both are required.

### 6. Lower executive friction
The UI should help the user begin, resume, and narrow work without adding shame-heavy or high-noise patterns.

## Primary screens

## 1. Home / Board

### Role
Main entry point. This is what the user sees first.

### Primary content
- current focus strip
- active Cases board
- secondary access to Inbox / To Address
- recent done or waiting items

### Recommended layout
Option A:
- top: daily focus
- center: board
- side: intake / recent items

Option B:
- board as full-width center experience
- auxiliary panels open on demand

### Board grouping
Since the main Case status is simple, grouping can be configurable:
- by status
- by work type
- by clarity
- by effort

Default recommendation:
- Active
- Waiting
- Done recently

### Card contents
Each Case card should show:
- title
- one-line summary or next step
- clarity state
- effort type
- source badge
- focus marker if selected today

## 2. Intake / To Address

### Role
A focused place for raw incoming work.

### Purpose
The user should be able to address work pressure without absorbing all of it.

### Card actions
- Do now
- Convert to Case
- Set aside
- Waiting on
- Open source

### Locked v1 Inbox behavior
- Quick capture sits at the top of the Inbox screen.
- The Inbox surface prioritizes items still awaiting triage.
- Converted and quick-completed items remain visible as quieter secondary sections.
- Empty states should read as calm breathing room, not as productivity celebration.

### Why this matters
This screen is especially important once external intake exists.

It lets the user face incoming work in a calmer, more deliberate rhythm.

## 3. Case page

### Role
The main working surface.

### Recommended structure
Tabs or sections:
- Overview
- Spec
- Decisions
- Execution
- Private
- Links

### Overview section
Should contain:
- title
- summary
- status
- next step
- source links
- clarity / effort / type metadata

### Spec section
- markdown editor
- outline if long
- good reading mode
- ability to paste rough notes quickly

### Decisions section
- quick add inline decision
- list of promoted decisions
- timestamps
- lightweight filtering

### Execution section
- checklist / grouped actions
- minimal state transitions
- no task overload

### Private section
- hidden from source systems
- user-only thought space
- personal decomposition
- rough notes
- AI-generated internal drafts

### Links section
- source link such as ClickUp / Jira / GitHub
- docs
- repo paths
- PRs
- commits
- URLs

## 4. Focus view

### Role
A stripped-down execution surface.

### Contents
- main Case
- two secondary Cases
- next step for each
- optional short notes

### Use case
User wants to work without seeing the whole system.

## 5. Quick capture

### Role
Capture without friction.

### Required capabilities
- fast keyboard entry
- minimal required fields
- defaults to Inbox Item
- supports pasted links and fragments

## Navigation model

Recommended top-level navigation:
- Board
- Inbox
- Focus
- Search
- Settings

Secondary navigation inside Case:
- Overview
- Spec
- Decisions
- Execution
- Private
- Links

## Interaction design notes

### Microcopy tone
- calm
- direct
- not gamified
- not over-enthusiastic
- never medicalized or patronizing when speaking to ADHD-friendly use cases

### Empty states
Should feel light and encouraging, not salesy.

### Colors
- neutral base
- subtle accent
- restrained danger states
- excellent dark mode

### Motion
- minimal
- soft
- purpose-driven

## Style translation from Fizzy / 37signals

What to carry over:
- simplicity
- high legibility
- low-noise cards
- confidence without flash
- small number of core views

What to adapt for this product:
- more markdown density
- stronger individual work context
- slightly more “dev cockpit” capability
- optional compact view for high information days
