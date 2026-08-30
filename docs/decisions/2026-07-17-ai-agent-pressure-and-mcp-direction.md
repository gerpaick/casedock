# AI agent pressure vs the original casedock concept + MCP direction

Date: 2026-07-17
Status: strategic note from an analytical discussion — not a product contract
Sources: `docs/specs/01-product-vision.md`,
`docs/research/2026-06-adhd-solo-developer-fit.md`, codebase audit (2026-07-17), and external
research (Leantime MCP, the "Claude Code + CLAUDE.md as ADHD mode" pattern)

---

## Discussion context

Analysis of the whole application: concept, needs, and status. Key background findings:

- **The product core is mature**: the capture → triage → convert → Case workspace → focus loop
  works end-to-end, with 154 tests, strict mypy, multi-user support, and deployment configuration
  (Docker + Caddy). The `clickup` and `ai` modules are intentional stubs.
- **Everything around the core is missing**: there is no onboarding or public presence, and the
  `/help`, `/privacy`, and `/terms` links are dead.
- **The biggest mismatch is internal**: the product promises a "resume engine," while ADHD
  principle #1 ("show ONE next action" / "Just Start") — the top finding from the project's own
  research and a P0 priority — is *not implemented*.
- Behavioral meta-risk: strategic documents are created faster than ideas are tested with users
  ("planning is dopamine").

---

## ⚡ THE ORIGINAL CONCEPT VS PRESSURE FROM AI AGENTS

> **This is the most important conclusion from this discussion. Read this section whenever
> making a positioning or roadmap decision.**

### New competitive pressure (absent from the existing documents)

The 2025/2026 analysis revealed a pattern absent from `docs/research/`: developers with ADHD
are solving task-initiation and context-recovery problems with **AI agents + context files**
(CLAUDE.md / AGENTS.md and task lists that an agent reads each session). Articles describe
"Claude Code as my ADHD mode." Leantime added an MCP server so AI can ask "what should I work
on now?" directly from the project.

This challenges the **"resume engine for a developer"** version of casedock's value proposition:
if a coding agent already retains project context, why use a separate app to recover it?

### But the original concept occupies different ground

The original problem from which casedock emerged:

> Many tasks from many people (ClickUp, Todoist, email), several projects, and technical support.
> The volume creates chaos that results in **clicking and browsing instead of planning**.

This is a problem of **inbound chaos (intake + triage)**, not a problem of context in code. This
part is **far more resilient to the wave of AI agents**, because:

1. **CLAUDE.md is per repository.** The chaos exists *between* projects: client A, client B,
   support, email, and ClickUp. No repository context file sees the whole stream.
2. **A coding agent does not perform triage.** It will not answer, "Of the 40 things that arrived
   today, which ones are allowed into my work and which ones should I park?" That is a decision,
   not context compilation.
3. **The "clicking and browsing instead of planning" loop** is ADHD-driven decision avoidance
   through pseudo-activity. ClickUp and Todoist *deepen* it with an endless scrolling list;
   casedock *breaks* it with mandatory triage (park / do now / convert / waiting) and a hard 1+2
   focus limit. The first screen presents a decision, not a list.

This is consistent with the project's research: fit for "incoming work scattered across tools"
= *high*; fit for a "personal interpretation layer between external assignment and real
execution" = *very high*.

### Positioning conclusion

- **Core identity**: one funnel through which all the chaos from ClickUp, Todoist, and email
  passes *before* it becomes work. AI agents do not handle this and will not for a long time —
  this is a decision-making problem, not a technical one.
- **The second pillar (not the other way around)**: context recovery / "resume engine." Agents
  genuinely erode value here, so this pillar needs integration with agents (MCP, below), not
  competition against them.

---

## MCP in casedock — purpose, rationale, and benefit

### Strategic thesis

**MCP turns the threat into a moat.** Without MCP, casedock and an AI agent compete for the role
of "external memory," and the agent wins on convenience. With MCP, casedock becomes **a
structured source of truth that the agent reads**: cross-project, with a lifecycle (inbox → Case
→ done) and triage that per-repository files do not provide. The more someone works with agents,
the *more* they need casedock, not less.

### Direction 1: casedock as an MCP server (the agent reads from casedock) — priority

Usage scenarios:

- **Start of a coding session.** The agent calls `get_focus` + `get_case` and receives the Case
  spec, recent decisions, and the first incomplete ExecutionItem. The question "what should I do
  now?" is answered by the user's *own* decision system, not invented by the model.
- **Capture without leaving the terminal.** While coding, the thought "I need to sort out the
  backup for client X" appears, so the agent calls `capture_inbox_item`. The thought enters the
  funnel with no context switch. This is critical for ADHD: the greatest capture cost is
  switching to another app.
- **End of session = low-cost re-entry.** The agent summarizes "what we decided and what the next
  move is"; the user approves it; and the entry becomes a Decision or ExecutionItem in the Case.
  The agent handles the documentation work that an ADHD brain hates.

Market precedent: Leantime MCP server ("what should I work on next?" with live project context).

### Direction 2: MCP as an intake channel (instead of dedicated connectors)

The roadmap (Phase 2) assumes a custom-built ClickUp connector followed by Jira and GitHub. An
alternative is for an agent with MCP access to ClickUp, email, and GitHub to **feed the casedock
Inbox** through the same `capture_inbox_item` tool.

- Benefit: one intake point instead of N connectors to maintain; every item still passes through
  human triage ("triage before commitment").
- **Risk to manage**: it must remain *on demand* ("collect today's ClickUp tasks in my Inbox"),
  not an autonomous background sync. Otherwise, the same chaos the user is escaping will be
  recreated inside casedock.

### Boundaries (consistent with existing product principles — must remain intact)

- **"AI does not make autonomous decisions"** → tools are read-mostly. The only write operation
  is `capture_inbox_item`, which passes through human triage. No agent-driven `set_focus`,
  `close_case`, or `prioritize`.
- **"Private notes do not leave for external systems without an explicit user action"** →
  `PrivateNote` is NOT exposed through MCP by default; a separate, informed opt-in may be added
  per Case.
- The entire feature is opt-in, with one token per user.

### Technical outline (for later, not immediate implementation)

- Natural location: the `src/apps/ai/` stub.
- Python MCP SDK + per-user token authentication.
- Four or five initial tools: `get_focus`, `list_active_cases`, `get_case`, `get_next_move`, and
  `capture_inbox_item`.
- Small, well-bounded scope that is inexpensive to build after P0 is complete.

---

## Recommended sequence (unchanged from the journey audit, with one addition)

1. **ADHD principle #1 ("Just Start" / one visible next action)** — before every new feature.
   Without it, casedock is a context archive, not a resume engine.
2. First-run experience → dead links (`/help`, `/privacy`, `/terms`).
3. **MCP (direction 1)** — before the ClickUp connector from Phase 2; the world has moved toward
   agents, not custom-built connectors.
4. A checkpoint question before every session: *Did I process my own work through casedock
   today?* (the MVP success metric from the specs: "the user starts processing work in this
   system first").
