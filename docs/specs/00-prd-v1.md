# PRD v1

## Product summary

**casedock** is a calm, solo-first execution system for overloaded technical builders, especially ADHD-leaning solo workers and developers. Its job is to turn incoming work and private thinking into deliberate, finishable execution. The core unit is a **Case**, not a generic task.

The product should behave like a translation layer between incoming work pressure and calm structured execution. It should reduce ambiguity before action, keep private shaping close to the work, and make re-entry after interruption cheaper than in broad team tools.

The product must make sense with zero live integrations. External systems such as ClickUp, Jira, Asana, or GitHub Issues are optional task sources, not the product center.

This PRD is the fastest product entry point for an implementation agent. Detailed behavior lives in `01-09`. If this brief and deeper docs diverge, reconcile the product decision explicitly instead of silently choosing one interpretation.

## Target user and problem

The primary user is an overloaded solo technical builder working across code, architecture, debugging, research, notes, and admin work. The product should also fit technical ICs who receive work through larger systems but need a calmer personal execution layer.

Existing work tools create overload because they surface too much raw work, separate thinking from doing, make context recovery expensive, and optimize for tracking instead of execution. This is especially painful for users with ADHD-like overwhelm, context switching fatigue, task paralysis, or executive-friction patterns.

casedock should sit between incoming pressure and focused work. It should help the user triage first, shape meaningful work into Cases, keep private context close to the work, and return to interrupted work without rebuilding context from scratch.

## Core product principles

- calm before power
- reduce executive friction
- triage before commitment
- Cases over tasks
- private thinking matters
- markdown and text are first-class working media
- re-entry support is part of the product value, not a polish detail
- daily focus must be explicit
- external systems are connected, not dominant
- support overwhelmed brains respectfully, without medicalized product behavior

## MVP definition

V1 is **single-user only**. It should optimize for personal use now without blocking a later move to multi-user ownership and accounts.

The MVP must support:
- Inbox capture and intake
- triage actions such as Do now, Convert to Case, Set aside, and Waiting on
- Case pages with spec, decisions, execution, private notes, and links
- a calm board view
- a daily focus view with 1 main and 2 secondary Cases
- simple search and lightweight metadata such as clarity, effort, and work type
- source links without requiring live integrations

V1 succeeds if the user starts handling meaningful work in casedock first, feels less overwhelmed than in ClickUp or Jira-style tools, can resume work with context intact, and still finds the product useful without any connector enabled.

## Explicit non-goals

V1 is not:
- a team collaboration suite
- a multi-user workspace product
- a full ClickUp, Jira, or Asana replacement
- a traditional task manager
- a workflow engine
- a mobile-first product
- a medical or therapeutic ADHD product

## Primary workflows

The core loop is:
1. capture or import incoming work
2. triage it before commitment
3. convert meaningful work into a Case
4. continue the Case through spec, decisions, execution, and private notes
5. choose daily focus explicitly

The most important workflow in v1 is **Inbox Item -> Case -> continued execution**.

## Key engineering constraints

- work spec-driven-first from `docs/specs`
- use Django 6 for the initial implementation
- keep the app HTML-first with Django templates, HTMX, Alpine.js, and Tailwind
- use email-based authentication, not username-based login
- use `pytest` by default and add tests with new workflow and domain logic
- treat private notes as a hard boundary for external sync
- treat AI as draft assistance only, never autonomous product behavior
- keep the core solo workflow valuable before adding live integrations

## Build priority

Build now:
- Inbox, Cases, Decisions, Execution, Focus, Private Notes
- board and Case working surface
- core conversion and continuation workflows
- generic source-link abstraction without live provider sync

Can wait:
- richer re-entry helpers and lightweight work history
- AI triage, summarize, and Case-draft actions
- richer search
- simple week or load-awareness surfaces after the core loop feels strong
- templates and activity views

Later:
- plugin-style source integrations, starting with ClickUp read-only intake
- explicit review-based write-back
- multi-user support

## Open questions

- whether AI helper actions belong in MVP or post-MVP
- whether a magic-link flow is worth adding after the email-and-password bootstrap
