# Product Vision

## Working name

**casedock**

Alternate names that match the same direction:
- Builder OS
- Calm Workbench
- Case Studio
- Fizzy for Solo Builders

`casedock` is the chosen product name.

## Product statement

casedock is a calm workbench and personal execution layer for solo technical builders and other overloaded knowledge workers.  
It helps transform incoming work into deliberate, finishable execution.

Its strongest job is to translate raw incoming work into calm structured execution without forcing the user to think inside a noisy external system first.

Instead of treating every input as just another task, the product gives each meaningful piece of work a place to be:
- clarified
- shaped
- documented
- executed
- completed

## Problem

Current work tools cause overload for this user profile because:
- there are too many items visible at once
- too much work arrives without interpretation
- there is weak support for personal thinking and private context
- task systems often optimize for tracking rather than for doing
- enterprise tools make it hard to see “what matters now”
- they make context recovery after interruption expensive (research shows ~23 min to regain focus after a single interruption; see [context-switching research note](../decisions/2026-05-25-context-switching-research.md))
- they create extra executive friction at the moment the user is trying to start

Tools such as ClickUp, Jira, and Asana may still exist around the user for accountability, but they often create pressure, noise, and slowness. Simpler task tools are cleaner, but still too flat and task-centric for complex technical work.

Empirical research confirms that context-switching cost is non-linear: each interruption compounds recovery time and error rate, not merely adds to it (see [context-switching research note](../decisions/2026-05-25-context-switching-research.md)).

The user needs a tool that sits between:
- raw incoming work
- actual focused execution

It should do more than store tasks.
It should reduce ambiguity, preserve context, and make restart friction meaningfully lower.

## Target user

Primary target:
- overloaded solo developer / technical builder, often ADHD-leaning
- works across code, notes, architecture, product thinking, research, debugging
- has mixed workdays: deep work, admin work, quick fixes, ambiguous tasks
- benefits from markdown and text-based context
- wants a calmer system than ClickUp or Jira-style tools
- still needs to keep links to external work systems
- often struggles with overload, task paralysis, context switching fatigue, or restart friction

Secondary target:
- technical IC inside a company toolchain
- receives assigned work through ClickUp, Jira, Asana, or similar systems
- needs private notes and private decomposition outside the official system
- wants a personal execution layer rather than another team dashboard

## Product principles

### 1. Calm before power
The product should feel quiet, intentional, and readable.
More features are acceptable only if they do not increase chaos.

Poor tool usability directly increases cognitive load — this has been measured empirically (see [context-switching research note](../decisions/2026-05-25-context-switching-research.md)). Every unnecessary UI element is not just aesthetic noise; it is measurable mental cost.

### 2. Reduce executive friction
The product should make it easier to begin, resume, and narrow work.

Interruption cost is non-linear: errors and delays compound with each additional context switch (see [context-switching research note](../decisions/2026-05-25-context-switching-research.md)). Lowering friction at the start and resumption points has outsized impact.

### 3. Triage before commitment
Not every incoming task deserves equal attention.
Every item should first be addressed, not automatically absorbed.

### 4. Cases over tasks
Tasks are execution fragments.
A Case is the unit of meaningful work.

### 5. Private thinking matters
Users need working notes, drafts, interpretation, and decomposition that are not visible in external systems.

### 6. Markdown is first-class
This product should fit a text-heavy, spec-first workflow.

### 7. Re-entry must be cheap
The product should help the user resume work without reconstructing context from scratch.

Research indicates ~23 minutes to regain focus after a single interruption (see [context-switching research note](../decisions/2026-05-25-context-switching-research.md)). A Case that preserves spec, decisions, execution state, and private notes in one place is the primary mechanism for making re-entry cheap.

### 8. Daily focus must be explicit
The user should see:
- one main thing
- two secondary things

"Task switching" (suspend, do something else, return) is cognitively more expensive than working on one thing at a time (see [context-switching research note](../decisions/2026-05-25-context-switching-research.md)). Explicit focus is a guardrail against the snowball effect of accumulated interruptions.

### 9. External systems are connected, not dominant
Source systems may provide inputs, but they should not dictate the mental model.

### 10. ADHD-friendly, not medicalized
The product should support overwhelmed brains respectfully without pretending to diagnose, treat, or medically manage ADHD.

## Product promise

When the user opens casedock, they should quickly understand:
- what is active
- what needs to be addressed
- what the next move is
- what they were doing before they stopped
- and they should still feel oriented even if no integration is connected

## What this product is not

- not a full team collaboration suite
- not a full ClickUp replacement in v1
- not a traditional task tracker
- not a timeline-heavy project manager
- not a complex productivity dashboard
- not a medical or therapy product

## Emotional design goal

The user should feel:
- calmer
- clearer
- less trapped by workload
- more able to convert pressure into deliberate action
- less likely to hit shame loops when work feels messy

## Success criteria

A successful product should enable the user to:
- process external work without overwhelm
- process self-created work without needing an external system at all
- keep private context close to the work
- turn ambiguous tasks into structured execution
- maintain a strong “what now?” view
- return to interrupted work without reloading context from scratch
