---
id: "TASK-RF-merge-prompt-wiring-directive-20260525-160000"
title: "Add wiring-directive to roadmap merge-step LLM prompt"
description: "Follow-up to TASK-RF-20260525-150000 — addresses the merge-step side of the anti-instinct gate failure mode. The Fix B merged refactor landed the gate-side (extractor + coverage check tolerance). This task adds the corresponding directive to the roadmap merge LLM prompt + a regression test asserting the directive's presence, so emitted roadmaps consistently include explicit wiring tasks for spec-level integration mechanisms."
status: "🟡 To Do"
type: "🛠 Code Remediation"
priority: "➡️ Medium"
created_date: "2026-05-25"
updated_date: "2026-05-25"
related_docs:
- path: ".dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/adversarial/merged-output.md"
  description: "§7 — Known follow-up: merge-step prompt blindness. Contains the verbatim directive proposal."
- path: ".dev/tasks/to-do/TASK-RF-20260525-150000/TASK-RF-20260525-150000.md"
  description: "Parent task — landed the gate-side fix; this follow-up addresses the merge-step side."
tags:
- "roadmap-pipeline"
- "merge-prompt"
- "anti-instinct-gate"
- "follow-up"
---

# Add wiring-directive to roadmap merge-step LLM prompt

## Task Overview

This is a follow-up task captured from the §7 section of the Fix B merged
adversarial output (`merged-output.md`). The parent task TASK-RF-20260525-150000
landed the gate side of the anti-instinct gate failure mode — making the
extractor and coverage check more tolerant of valid LLM-generated roadmap
phrasing. It did NOT fix the merge-step side.

The merge step's LLM prompt (in `src/superclaude/cli/roadmap/prompts.py` or
wherever the merge synthesis is templated) does not currently include explicit
guidance that emitted roadmaps must contain explicit wiring tasks for each
integration mechanism in the spec. Without that guidance, repeat roadmap
pipeline runs depend on LLM phrasing luck.

merged-output.md §7 proposes:

> "Every spec-level integration mechanism (dispatch table, registry,
> middleware chain, event binding, DI container) MUST appear in the roadmap
> with an explicit wiring task using one of: create, populate, wire,
> register, configure, set up the [mechanism]."

A proper end-to-end fix would also:

1. Add the directive above to the merge prompt at the right injection point.
2. Add a regression test against the merge step's prompt that asserts the
   directive's presence.

## Resolved Questions

This follow-up was deferred from TASK-RF-20260525-150000 per RQ-2 of that task.
The severity per Round 2.5 invariant probe is **HIGH** for the original failure
mode; **MEDIUM** with the gate-side Fix B applied (the gate is now more
tolerant, so LLM phrasing variance is less likely to trigger failure).

## Status

**Not yet planned — requires a full BUILD_REQUEST + research cycle to produce a complete task file. Use /task-builder when ready to start.**
