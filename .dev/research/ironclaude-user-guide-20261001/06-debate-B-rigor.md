# Debate B: Default to the Structured Path

**Position:** Structured (task files, research-first, specs, independent QA) is the default; interactive is the exception.
**Evidence base:** files 01-04 in this folder, plus `/Users/cmerritt/GFxAI/IC-Harness/CLAUDE.md`.
**Date:** 2026-10-01
---

## 1. Thesis

This user's most expensive failures are not slow work; they are lost state and drift. 157 resume prompts plus 66 progress pings (P6) and 104 protocol-drift complaints (P5) outnumber the 80 "overengineer" hits (P1) (`04-work-patterns.md` Section 3). Only an on-disk artifact (task file, spec, protocol file, ledger) survives a disconnect or `/compact` (49 typed, `04` Section 1a), and only an independent checker catches drift that the author cannot see. So the default for any multi-step or multi-file work is a written artifact plus a checker, sized to the job. The lean path wins only where nothing needs to survive the session: answers, single-file edits, and live approval loops.

## 2. Decision rules (apply in order; first match wins)

| # | If | Then use | Evidence |
|---|---|---|---|
| R1 | The user asked a question | Answer only. No edits, no skill. | P2 (31 hits), `04` Section 3 |
| R2 | One file, obvious change, fits in this session | Direct edit plus one targeted test. `/sc:task` LIGHT/STANDARD if you want its test run. | Rung 0-2, `02` Part 2 Section 1; P1 |
| R3 | A named on-disk protocol already governs the work (component workflow, grading protocol) | Follow that protocol only; it IS the structured artifact. Add no extra skill. Post-check with `/sc:reflect --mode post` after a revision. | P4, P5, `04` Section 3 |
| R4 | More than 5 edits or more than one file | A written plan before code. This is a project rule, not a preference. | CLAUDE.md Custom Project Rule 6 |
| R4a | ...and scope is known, under about 5 files, within one or two sessions | Simple task file. Master: `/sc:workflow <spec> --depth quick` then `/sc:implement @plan.md` (Template 00, ledger, per-task reviewer, resumable). IC-Harness today: `/task-builder` with `TEMPLATE: 01`, `QA_INTENSITY: lite`, `FINAL_ONLY`, then `/task`. | `02` Sections G.2, G.3, Part 2 Section 2 |
| R4b | ...and 5-20 files or crosses sessions | Full `/task-builder` (Standard, Template 02) then `/task`. | Rung 6, `02` Part 2 Section 1 |
| R4c | ...and 20+ files or several subsystems | Deep tier task file. | Rung 7 |
| R5 | The design or contract is not yet agreed (new tier logic, new grader, new profile scheme) | Short spec file first in `.dev/research/<topic>/`; user approves; then R4a/R4b. Add `/sc:spec-panel @spec --mode critique` when the spec drives more than one PR. | W4, W2 in `04` Section 4; `03` sequence (c) |
| R6 | You do not know what to build or where the code lives | `/tech-research` (Quick unless asked otherwise) then feed its Implementation Plan to `/task-builder`. | Rung 8; `02` Part 2 Section 3 |
| R7 | New product or component needing a formal document | `/prd` then `/tdd`; `/sc:spec-panel` before planning. | Rung 9 |
| R8 | Multi-phase release | `/roadmap` (RF lane, task files per phase at Deep) or `/sc:roadmap` then `/sc:validate-roadmap` then `/sc:tasklist` then sprint. | Rungs 10a, 10b |
| R9 | Something is broken | First pass by hand from code and logs. If the cause is not found in one pass, or it is intermittent or crosses files, `/sc:troubleshoot` (Tier 1 is 1-3 min); `--fix` only for multi-file remediation. | `03` Section 1.1, sequence (a); W5 |
| R10 | Plan exists and a spec resolves | PRE reflect runs (mandatory in task-builder when a spec resolves). After execution, POST reflect. Never disable either without user authorization. | `02` Part 2 Section 4 items 12-13; Custom Project Rule 1 |
| R11 | Two or more credible designs, or a contested decision | `/sc:adversarial --compare` (Mode A) or `/sc:brainstorm --handoff task` when requirements are fuzzy. `/sc:swarm-wizard` only when other model families are wanted. | `03` Section 1.3, sequence (b) |
| R12 | Before commit | Tests, then `/sc:reflect --mode post --no-promote`, then built-in `/code-review`; `/security-review` if auth, secrets, input, or paths changed. | `03` sequence (d) |
| R13 | Before push and PR (push only on explicit request) | `/sc:auggie-review --diff ... --no-post-pr`, then `/sc:pr-submit --monitor 1` or `2`, never 3. | `03` sequence (e), Section 1.4 notes; CLAUDE.md Git Policy |
| R14 | Session lost or resumed | Read the task file or ledger first (it is the source of truth); `sc-crash-recovery` only when you do not know which artifact. | Operational Rules 3, 5; `03` sequence (f) |

## 3. Work types W1-W10 under these rules

| Work type | Rules hit | Sequence |
|---|---|---|
| W1 Component consolidation | R3, R12 | The component workflow protocol file is the structured artifact. Build candidate, HTML side-by-side, present, wait for approval. No task-builder (user rejected it here). `/sc:reflect --mode post` after a multi-consumer fix to catch the P5 drift ("touched sections we have not reached"). Cross-consumer fixes over 5 edits go into a short checklist in the protocol folder per Rule 6. |
| W2 Skill-eval harness | R5, R4a/R4b, R6 | Spec first (user asked for it 2026-08-18). Build one grading surface at a time against a ledger (Template 00 where available, else Template 01 lite). Reuse-first read of the product domain before building (P8; `reuse-auditor`). Multi-hour research parts via `/task-builder` then `/task` with PRE reflect. Then `/skill-eval <domain> --candidate <gold>`. |
| W3 Persona brain testing | R1, R2, R9 | Interactive per question with the five-field report. Fixes: surgical edit plus rerun of the same question. Any fix touching more than one brain file goes to R4a with a ledger, because these runs span sessions. |
| W4 ccsession / IronClaude / tiers | R5, R11, R4a, R12, R13 | Spec with exact file changes, optional `/sc:adversarial` debate, `/sc:spec-panel` when it drives multiple PRs, implement via Template 00 ledger or Template 01 lite, test locally, `/code-review`, `/sc:auggie-review --no-post-pr`, push only on request, `/sc:pr-submit --monitor 1`. |
| W5 Env and tooling troubleshooting | R1, R9 | Answer from code and logs in plain English. Escalate to `/sc:troubleshoot` only if one direct pass fails or the symptom is intermittent; the user declined it twice, so do not lead with it. |
| W6 Batched research | R6, R10, R14 | `/tech-research` end to end, batches with independent QA and fix-then-proceed. Task file checkboxes are what make a 778-item run resumable. Tune cost by tier and QA intensity, not by dropping the gate. |
| W7 Recruiting grading | R5, R3, R14 | One master grading spec (user demand), then each batch runs against it with a cumulative report updated on disk and spot-check QA. |
| W8 Documents | R1/R2, R7 | Short deliverables (CEO summary, ClickUp stories): write directly from the governing template. Formal PRD/TDD/ops guide: the document skill. |
| W9 Repo operations | R2, R13 | Show diff and plan, wait for explicit go, then git. No skill. |
| W10 Supervision and recovery | R14 | Read tracker and task file, report done / left / next, then resume. The structure created by R4-R8 is exactly what makes this step cheap. |

## 4. Where the lean position is right (concessions)

1. **Answer-only and single-file work should never touch a skill.** P1 (80 + 23 + 32 hits) and P2 (31) are real and mostly come from wrapping narrow fixes in machinery. R1 and R2 concede this fully.
2. **Unrequested heavy skills are a protocol violation, not rigor.** P4 (16 direct): running task-builder inside W1 or tech-research for a comparison write-up added drift, not safety. Structure means "the artifact the protocol names", which for W1 and W7 is the protocol file, not task-builder (R3).
3. **Template 01 "lite" is still heavy.** Build runs 3 researchers, a 2-agent research gate, 5 task-file validators, and `/task` still mandates a 6-agent lens gate per phase (`02` Part 2 Section 2b and Section 4 item 5). For a 3-file change that cost is out of proportion; the honest middle rung is master's Template 00 path, which IC-Harness does not have yet (`02` Section G.3).
4. **Debug should start by hand.** W5 questions want a root cause in plain English; Tier 1 troubleshoot is cheap but the user explicitly declined it twice.
5. **Overengineered verification inside a fix (timers, parsers, validators) is not structure.** Structure is the plan and the independent check, not extra code.

## 5. Expected attacks from Debater A and rebuttals

**Attack 1: "The data shows the user hates overengineering; P1 has 80 hits and task-builder is the most-complained-about skill."**
Rebuttal: P1 is about narrow fixes and added machinery, and my R1-R3 already keep those out of structure. Count the other side: resume prompts (157) plus progress pings (66) plus protocol drift (104) is 327 hits for exactly the failures that on-disk artifacts and independent checks prevent (`04` Section 3, P5 and P6). The user also said "when in doubt the regimented skill approach is right" (2026-09-27, `04` P4) and demanded end-to-end skill runs without stopping (P9). The fix for P1 is right-sizing the rung, not dropping the rung.

**Attack 2: "Interactive work under a protocol file (W1, W3, W7) is the user's real mode, so interactive should be the default."**
Rebuttal: Those streams work precisely because a written protocol file exists and the user approves each step. That is structure: a spec-like artifact plus a human gate. The failures in those streams are drift from the protocol (P5: "follow it and only it", "you touched sections we have not reached"), which is what POST reflect and Rule 6 checklists catch. Remove the artifact and W1/W7 become memory-only work that dies on the next disconnect. Interactive is the interaction style; the artifact is still mandatory.

**Attack 3: "Even the lite task file costs 10+ agents and the 6-agent /task floor; that is ruinous for small changes, and W6 already showed cost pain (60 of 778 studios)."**
Rebuttal: Agreed on the numbers (`02` Part 2 Section 2b, Open Question 1), which is why R4a picks the cheapest artifact that still persists and gets checked: Template 00 plus `/sc:implement` keeps a resumable ledger and one reviewer per task with zero planning subagents (`02` Section G.2). Where that is not installed, the right response is to install master (`01` Section 7 gives the path), not to fall back to memory-only work. For W6, the cost complaint was solved by tuning tier and batch size, not by removing QA; Custom Project Rule 1 forbids disabling gates without authorization, and uncaught errors compound across 778 items (Operational Rule 15).

## Open points

- Template 00 is master-only; until IC-Harness adopts it, R4a falls back to Template 01 lite, which is heavier than ideal. UNVERIFIED which way the user wants to go (`02` Part 2 Section 5 item 10).
- Whether `/task` honors lite QA intensity or always enforces 6 agents is unresolved (`02` Part 2 Section 5 item 1); the cost of R4a in IC-Harness depends on it.
