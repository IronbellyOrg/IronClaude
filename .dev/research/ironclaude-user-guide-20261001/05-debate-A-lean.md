# Debate Position A: Default to the Lightest Approach
**Debater:** A (lean-first)
**Date:** 2026-10-01
**Evidence base:** `01-command-inventory.md` (Sections 6-8), `02-planning-depth-ladder.md` (Part 2), `03-quality-debug-review.md`, `04-work-patterns.md`, `IC-Harness/CLAUDE.md`
**Status:** Complete
---

## 1. Thesis

The user's own record says the heavy path is the exception, not the rule. Of the 10 observed work types, only W6 (batched research) is classified Task-file; the rest are Interactive, Spec-first, or Debug/review (`04-work-patterns.md` Section 4). The top complaints are overengineering (80+ hits), not answering the question (31), and running task-builder or other heavy skills unasked (16+ direct) (`04` Section 3, P1, P2, P4). So the default should be: answer first, then the smallest on-disk artifact that makes the work reviewable, and climb the ladder only when a named trigger fires. Heavy skills are tools for named situations, not a reflex.

## 2. Decision rules (apply in order; stop at the first match)

1. **If the message is a question, answer it and change nothing.** No skill, no agent, no edit. (P2: "Answer it first.")
2. **If the user names a skill or protocol, run exactly that, end to end, and nothing extra.** (P4 resolution in `04` Section 3; CLAUDE.md rule 16.)
3. **If an on-disk workflow protocol already governs this stream (component protocol, grading protocol), follow it; do not add a skill it does not call for.** (P4, P5.)
4. **If it is 1 file and up to 5 edits with an obvious change, edit directly and run one targeted test.** (Rung 0, `02` Part 2 Section 1; CLAUDE.md Custom Rule 6 threshold.) Use `/sc:task` LIGHT/STANDARD only if you want its tier header and affected-test run (`02` rungs 1-2).
5. **If it is security, auth, migration, or crypto, use `/sc:task --compliance strict` at minimum.** Security words always win (`02` rung 3).
6. **If the design is agreed but touches several files, write a short spec file in `.dev/research/<topic>/` with exact file-level changes and acceptance criteria, get approval, then build and test one piece at a time.** This is how W2, W4, W7 actually ran (`04` Section 4). On IronClaude master, the same lane is `/sc:workflow --depth quick` then `/sc:implement @plan.md` (Template 00, one reviewer per task, resumable ledger; `02` G.2, Part 2 Section 2a). Note it is not installed in IC-Harness (`02` G.3).
7. **If the work must survive multiple sessions with audited checkboxes and the scope is known, use a lite task file:** BUILD_REQUEST with `TEMPLATE: 01`, `QA_INTENSITY: lite`, `QA_GATE_REQUIREMENTS: FINAL_ONLY`, then `/task` (`02` Part 2 Section 2b). Keep it to one execution phase, because `/task` adds a 6-agent lens gate on every Phase 2+ regardless of lite (`02` Part 2 Section 4 item 5).
8. **Use full task-builder (Standard/Deep, Template 02) only when:** 5-20+ files across subsystems, unknown structure needing discovery, or unattended multi-hour runs (`02` rungs 6-7).
9. **Use `/tech-research` first only when you do not yet know what to build or where** (`02` rung 8), or the user names it (W6). It defaults to Deep; say "quick" otherwise.
10. **Use `/prd`, `/tdd`, `/roadmap`, or the sc:roadmap to sprint lane only for template-governed documents or multi-phase releases the user asked for** (`02` rungs 9-10). `/roadmap` at Deep/full is 44-48 evaluating agents for 6 phases (`02` Section F).

**Do NOT use a skill when:**
- The user asked a question, a status check, or "brief check" (P2, W10).
- The deliverable is a short doc (CEO summary, onboarding, ClickUp stories, handoff); the user said "do not run a skill for this" (`04` W8).
- The fix is narrow and known; no validators, timers, parsers, or new QA cycles (P1: "Do the surgical fix, test it, report").
- The user is troubleshooting an environment issue and has not asked for `/sc:troubleshoot`; they declined it twice (`04` W5).
- A protocol already governs the work (W1 component consolidation, W7 grading batches).
- Repo operations (push, prune, branch fix): show the plan, wait for go, run git (`04` W9).

## 3. Mapping of the 10 work types

| Work type | Sequence under these rules | Rule that fires |
|---|---|---|
| W1 Component consolidation | Read the component workflow protocol; build candidate; `artifact-design` HTML side-by-side; present; wait for approval. Optional `/sc:reflect --mode post --no-promote` after a revision. No task-builder. | 3 |
| W2 Skill-eval harness | Short spec file; build and test one grading surface at a time; `/skill-eval <domain> --candidate <gold>`. Lite or Standard task file only for the multi-hour research slice. | 6, then 7/8 for research |
| W3 Persona brain testing | One `persona-agent` question; five-field report; wait for verdict; surgical fix; rerun the same question. | 2, 4 |
| W4 ccsession / IronClaude tiers | Discuss; spec with exact file changes in `.dev/research/<topic>/`; optional `/sc:adversarial` if the user asks for a debate; implement in the worktree; test locally; `/code-review`; push only on request. | 6 |
| W5 Env troubleshooting | Answer from code and logs with a plain-English root cause; change nothing until asked. `/sc:troubleshoot --no-escalate` only if requested. | 1 |
| W6 Batched research | `/tech-research` end to end (user names it), batches of 40, independent QA, fix then proceed. This is the one heavy lane, and it is correct here. | 2, 9 |
| W7 Recruiting grading | Master protocol file with exact steps and scripts; run batches against it; cumulative report; spot-check QA. | 3, 6 |
| W8 Documents | Short deliverable: write directly and present. Formal template-governed doc: the named doc skill at Lightweight unless the user asks for more. | 4/6, 10 |
| W9 Repo operations | Show diff and plan; wait for go; git. | 4 + Git Policy |
| W10 Supervision and recovery | Read the task file or tracker; report done / left / next in under 10 lines; `sc-crash-recovery` (single-project mode) after a real crash. | 1 |

Result: 1 of 10 work types defaults to a heavy skill; 2 more (W2 research slice, W8 formal docs) use one conditionally.

## 4. Where the rigor position is right (concessions)

- **CLAUDE.md Custom Rule 6 binds as written.** ">5 edits or multiple files MUST go through a task file." My rule 6 (spec file then direct build) does not literally satisfy it when the build crosses files. I do not get to reinterpret it (CLAUDE.md rule 6 "Execute Items as Written", Custom Rule 1 "Precedent is not authorization"). Honest position: either (a) the lightest compliant artifact is a one-phase lite Template 01 task file (rule 7 above), or (b) the user amends Rule 6 to accept an approved spec or protocol file with a checklist as satisfying it. W1, W4, and W7 already ran that way with the user's blessing, which is evidence for (b), but the user must make that ruling; I flag it as an open question, not a settled fact.
- **Long unattended runs need task files.** W6 lost work to disconnects and stalls (P6, 157 resume prompts). Checkbox state on disk is the only reliable resume point (`02` Section B; `03` Section 2f).
- **The user once said "when in doubt the regimented skill approach is right" (2026-09-27, `04` P4).** When the right lane is genuinely unclear and the work is large, rigor wins the tie.
- **QA gates are law once a skill runs.** Lean means picking a lighter rung, never stripping gates from a heavy one (Custom Rule 1; `02` Part 2 Section 2b on `QA_GATE_REQUIREMENTS: NONE`).
- **Security-sensitive changes** get STRICT regardless of size (`02` rung 3).

## 5. Expected attacks from Debater B and rebuttals

**Attack 1: "Lean violates Custom Rule 6 and the Canonical Skill Architecture; the repo rules say task files."**
Rebuttal: Rule 6 is a threshold (>5 edits or multiple files), not a default for everything. Below it, direct edits are explicitly allowed (`02` rung 0 cites the same rule). The Canonical Architecture governs how document/task-producing skills are built, not whether every request needs one. Above the threshold I comply with the lightest form (one-phase lite Template 01) and route the spec-file question to the user (Section 4). Meanwhile the cost of the heavy default is measured: 16+ direct complaints about unrequested task-builder runs, and the user rejecting task-builder for W1 and the W2 build (`04` Sections 2, 3).

**Attack 2: "Lean is how errors compound; the QA panels exist because single-agent work was unreliable."**
Rebuttal: The lean lanes keep verification, sized to the work: one targeted test (rule 4), STANDARD affected-test runs or STRICT quality-engineer (`02` rungs 2-3), Template 00's one reviewer per task with cited verdicts and a HALT on non-compliance (`02` G.2), and `/sc:reflect --mode post` as an on-demand independent audit (`03` Section 1.2). What the user complained about is QA added where it bought nothing: "No new verification cycle", "take out every kill timer" (P1), and a lite task file that still triggers 6-agent gates per phase (`02` Part 2 Section 4 item 5, Open Question 1). More agents is not more correctness; 3,731 rf-qa spawns did not prevent P5 protocol drift (`04` Section 1d).

**Attack 3: "Interactive work loses state on disconnects; task files are the only durable record."**
Rebuttal: Durability comes from writing to disk, not from MDTM ceremony. The spec file, the protocol file, the `.dev/implement/<slug>/progress.md` ledger (`02` G.2), and the program tracker (Custom Rule 2) are all on disk and resumable. W1 and W7, the two highest-volume interactive streams, ran under on-disk protocol files. Where a run is genuinely long and unattended (W6), I already concede the task file (Section 4).

## Bottom line

Default ladder for this user: answer, then direct edit with one test, then spec-first, then a one-phase lite task file, and only then full task-builder, tech-research, or roadmap pipelines when a named trigger fires or the user names the skill. Open question for the user: does an approved spec or protocol file with a checklist satisfy Custom Rule 6 for multi-file builds?
