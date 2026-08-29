# 07 — Example Task Flows

This document shows how real work items move through the app.

The examples intentionally mix manual capture and source-linked intake.
The core workflow should stay useful even when no connector is enabled.

The goal is not to model a generic task manager. The goal is to show how **incoming work** becomes either:

- a quick action handled immediately,
- a structured **Case**,
- or something set aside / waiting on.

This is the practical heart of the system.

---

# Core principles behind the flow

Every incoming item should answer one question first:

> Is this something I should do now, or something I should shape into structured work?

That leads to three main actions from the intake layer:

- **Do now**
- **Convert to Case**
- **Set aside**

Optional additional states:

- **Waiting on**
- **Open source**
- later: **Send update to source system**

---

# Shared UI model

## Intake / To Address panel

Every raw incoming item appears as an **Inbox Item**.

Example card fields:

- title
- source (ClickUp / manual / URL / other)
- due date (if any)
- current source status
- assignee
- short snippet / description
- source link

Example quick actions on each card:

- `Do now`
- `Convert to Case`
- `Set aside`
- `Waiting on`
- `Open source`

## If converted

A new **Case** is created with:

- Overview
- Spec
- Decisions
- Execution
- Private Notes
- Links / Artifacts

## If done immediately

The app opens a lightweight execution panel instead of a full Case.

This panel should support:

- short notes
- quick checklist
- issue log / observations
- promote to Case if needed
- resolution summary

---

# Example 1 — "Implement email authentication"

This is a good example of a task that should usually become a **Case**.

It is larger than a simple action and contains uncertainty.

## Intake state

**Inbox Item**

- Source: ClickUp connector
- Title: `Implement email-based authentication`
- Suggested effort: Deep
- Suggested clarity: Fuzzy
- Recommended action: `Convert to Case`

## User action

The user clicks:

- `Convert to Case`

## Lightweight conversion form

Fields:

- **Working title**: `Email authentication`
- **Desired outcome**: `Users can sign in securely using an email-based flow.`
- **Clarity**: `Fuzzy`
- **Next concrete move**: `Choose auth model for v1.`

## Resulting Case

### Overview

- Title: `Email authentication`
- Status: `Active`
- Type: `Build`
- Effort: `Deep`
- Source: `ClickUp`
- Next move: `Decide auth model`

### Decisions

Initial decision to make:

- Should v1 use magic link, one-time code, or password + email?

Example decision entry:

- **Decision**: Use magic link for v1
- **Why**: Lower implementation friction, simpler UX, avoids password reset complexity in first version
- **Alternatives considered**:
  - One-time code
  - Password + email

### Spec

Example starter markdown:

```md
# Context
We need email-based authentication.

# Outcome
Users can sign in using email.

# Open questions
- magic link or password?
- password reset needed in v1?
- email verification required?
- session handling approach?

# Constraints
- existing user model
- deployment environment
- email sending setup
```

### Execution

Initial execution items:

- choose auth approach
- inspect current user model
- define backend auth flow
- define UI screens
- define failure states
- implement email sending path
- test token expiry and invalid links

## End-of-flow behavior

At any point the user can generate a source-system update, for example:

> Started implementation. Chosen v1 direction: magic link authentication. Now shaping backend flow and email delivery path.

---

# Example 2 — "Add SMTP in ParcelTracker"

This task sits on the border between quick execution and structured work.

That makes it a perfect example of why the app needs both:

- **Do now**
- **Promote to Case**

## Intake state

**Inbox Item**

- Source: manual capture
- Title: `Add SMTP to ParcelTracker`
- Suggested type: `Config / Infrastructure`
- Suggested effort: `Medium`
- Recommended action: `Do now` or `Convert to Case`

## Path A — handled as Do now

The user clicks:

- `Do now`

## Do now panel

Visible sections:

- quick notes
- mini checklist
- current observations
- source link
- `Promote to Case if needed`

Example working checklist:

- confirm SMTP provider
- add env vars
- configure sender identity
- test delivery
- verify failure handling

If the task remains simple, the user completes it directly and records a short result.

Example resolution summary:

> SMTP configured for ParcelTracker. Verified outbound email with test delivery and confirmed basic environment setup.

## Path B — promoted into a Case

If hidden complexity appears, the user clicks:

- `Promote to Case`

This creates:

### Case overview

- Title: `SMTP for ParcelTracker`
- Status: `Active`
- Type: `Config`
- Effort: `Medium`
- Source: `Manual`

### Decision examples

- Which SMTP provider should be used?
- Should credentials differ per environment?
- Do we need templates in v1 or just raw sending?

### Spec example

```md
# Goal
Enable outbound email in ParcelTracker via SMTP.

# Requirements
- environment-based configuration
- verified sender identity
- testable in staging
- production-safe settings

# Questions
- provider?
- auth method?
- TLS / SSL mode?
- default from address?
```

### Execution example

- choose provider
- configure env vars
- wire app mail settings
- send test email
- validate staging
- document production setup

This shows how the system supports light entry and structured escalation.

---

# Example 3 — "Add new F03 system"

This is not really a task.
It is a **larger, fuzzy work item**.

This should almost always become a structured Case.

## Intake state

**Inbox Item**

- Source: Jira connector
- Title: `Add new F03 system`
- Suggested clarity: `Low`
- Suggested effort: `Deep`
- Recommended action: `Convert to Case`

## User action

The user clicks:

- `Convert to Case`

## Conversion framing

The app can gently ask:

- What is F03 exactly?
- Is it a module, workflow, integration, or system mode?
- What does “done” actually mean?
- Is this replacing something or extending something?

## Resulting Case

### Overview

- Title: `F03 system`
- Status: `Active`
- Type: `System`
- Effort: `Deep`
- Clarity: `Fuzzy`
- Next move: `Define F03 scope and impact`

### Spec example

```md
# Context
We need to add a new F03 system.

# What we know
- likely touches multiple parts of the application
- probably has both business and technical implications

# What is unclear
- scope
- data model
- UI implications
- integration points
- rollout expectations

# Desired outcome
A clear definition of F03 and a workable implementation path.
```

### Decision examples

Early decisions may be framing decisions, not implementation decisions:

- Is F03 a module or an operating mode?
- Is this a replacement or an addition?
- Is this MVP or full rollout?
- Which existing parts are affected?

### Execution in the early stage

Execution here starts as discovery:

- define business scope
- identify touched areas of the app
- map dependencies
- document implementation shape
- split into execution chunks

This is exactly where the system creates value.

A generic task app would leave this as one scary line item.

CaseDock turns it into:

- a named area of work
- a visible uncertainty space
- a decision trail
- a clear next move
- a reusable working context

---

# Example 4 — "Printer not working on POS4"

This is an ideal example of an operational incident or support/debug task.

These tasks need to be:

- quick to enter,
- easy to act on,
- not forced into a heavy process,
- but still easy to escalate when needed.

## Intake state

**Inbox Item**

- Source: ClickUp connector
- Title: `Printer not working on POS4`
- Suggested type: `Debug / Ops`
- Suggested urgency: `High`
- Recommended action: `Do now`

## User action

The user clicks:

- `Do now`

## Do now incident panel

Visible sections:

- quick incident notes
- observations
- small troubleshooting checklist
- source link
- `Promote to Case if needed`

Example quick checklist:

- verify printer power and connection
- verify POS4 sees the printer
- test print from operating system
- test print from app
- inspect queue / spooler
- record exact error

## Path A — resolved quickly

If the issue is resolved in one pass, the user records a short summary and stops there.

Example resolution:

> Issue reproduced on POS4. Printer was visible but incorrectly mapped in the application configuration. Updated mapping and verified successful test print.

No full Case required.

## Path B — escalated into a Case

If the issue grows, the user clicks:

- `Promote to Case`

### Resulting Case

#### Overview

- Title: `POS4 printer failure`
- Status: `Active`
- Type: `Debug`
- Effort: `Medium`
- Source: `ClickUp`

#### Decision examples

- Is this local to POS4 or part of a broader printing issue?
- Do we need a quick workaround or a permanent fix?
- Is this application config, OS config, or hardware mapping?

#### Spec / Notes example

```md
# Observed behavior
Printer on POS4 does not print from the app.

# What was tested
- power OK
- OS print test OK
- app print fails

# Hypotheses
- wrong printer mapping
- application config mismatch
- print handler issue
```

#### Execution example

- compare POS4 with working POS
- inspect app printer config
- inspect print handler logs
- reproduce with controlled test
- apply fix
- verify successful print

---

# Cross-example summary

These four examples show the intended logic of the system.

## Small and clear
Use **Do now**.

Example:

- printer issue that can be resolved immediately

## Medium and uncertain
Start with **Do now** if appropriate, but allow **Promote to Case**.

Example:

- SMTP setup that turns out to require provider, environment, or rollout decisions

## Large or fuzzy
Use **Convert to Case** from the start.

Examples:

- email authentication
- new F03 system

---

# Practical triage rule

## Use “Do now” when

- the task is small
- the task is clear
- it can likely be completed in one working session
- it does not require major decision-making

## Use “Convert to Case” when

- the task is unclear
- the task is larger than a quick action
- it requires decisions
- it needs lasting context
- it may return later
- it has risk, ambiguity, or multiple moving parts

---

# Minimal UI language for these flows

## Inbox Item actions

- Do now
- Convert to Case
- Set aside
- Waiting on
- Open source

## Case sections

- Overview
- Spec
- Decisions
- Execution
- Private Notes
- Links

## End-of-work actions

- Draft source update
- Copy summary
- Mark done locally
- later: Sync to source system

---

# Why this matters

The point of the app is not to store tasks.

The point is to create a system where every piece of incoming work can be handled in the right mode:

- immediate action,
- structured shaping,
- or parking / waiting.

That is what turns a stressful task feed into a calmer system for **decisions and execution**, especially when the user is overload-prone and needs a clearer next move.
