# Context-switching and cognitive load research

Date: 2026-05-25

## Context

casedock's product principles (calm UX, cheap re-entry, explicit focus, reduced executive friction) are grounded in the observation that knowledge workers are overloaded by tool fragmentation, interruptions, and context-switching fatigue. This note collects empirical evidence that supports those principles.

## Sources

### 1. Liu et al. (2023) — Workflow interruption and nurses' mental workload in electronic health record tasks

BMC Nursing, 22(63). Five-month observational study of nurses working with an EHR system.

Key findings:
- 84 minutes of system interaction per shift, ~20 interruptions per hour.
- Cognitive load measured at 44.57/100 on NASA-TLX (the same scale used for pilots and control-room operators).
- Causal chain: more task switching → longer task completion → higher cognitive stress → more errors.
- 68% of errors were caught by the nurses themselves. The remaining 32% propagated further.
- "Task switching" (suspend one task, do another, return) is cognitively more expensive than "concurrent multitasking" (doing two things at once in context).

### 2. Gloria Mark, UC Irvine

Research on interruption and focus recovery in knowledge workers.

Key finding:
- It takes approximately 23 minutes to fully regain focus after an interruption (commonly cited from Mark et al., 2008; updated in later work).

### 3. Hubstaff (2026)

Workforce analytics report.

Key finding:
- Average knowledge worker makes ~1,200 app switches per day.

### 4. General SaaS sprawl data

- Average mid-market company uses ~137 SaaS tools; enterprise companies use 200+.

## Implications for casedock

| Research finding | casedock principle affected |
|---|---|
| 23 min to recover focus after interruption | #7 Re-entry must be cheap |
| Task switching is more expensive than concurrent multitasking | #8 Daily focus must be explicit (narrow the field) |
| Cognitive load increases with poor tool usability | #1 Calm before power |
| Errors compound non-linearly with interruptions | #2 Reduce executive friction |
| Workers scatter across 8+ tools for one process | #9 External systems are connected, not dominant |
| Private context reduces re-processing | #5 Private thinking matters |

The core product promise — that a single Case holds spec, decisions, execution state, and private notes together — is a direct response to the fragmentation problem these studies document. Fewer context switches, lower cognitive load, fewer errors.

## Source article

Aga Binkowska, "Nie przeszkadzaj mi!!! 2871 przerwan na 145 zmian. I to w szpitalu, nie na Slacku." LinkedIn, 2026-05-25. (Summarizes Liu et al. and connects findings to business operations and tool consolidation.)
