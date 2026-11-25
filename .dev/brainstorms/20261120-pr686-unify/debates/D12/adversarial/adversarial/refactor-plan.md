# Refactoring Plan: D12

## Overview
- Base variant: Variant 1 (OURS), score 0.8833; incorporated: Variant 2 (CLAY)
- Planned changes: 9 (C1 to C9); rejected alternatives: 5; five HIGH invariant findings become binding safeguards (S1 to S5) on change C1
- Overall risk: Medium (the claim rule touches chain tests and the launch prompt path)

## Planned Changes

### C1. Claim reads the plan sections (replaces OURS' original one-line concession and CLAY's chain move)
- Source: Variant 1 "Recommended shape" last bullet, widened by Round 2 (C-005, U-003); Variant 2 point 3 (double planning)
- Target: `src/superclaude/skills/sc-issue-protocol/refs/claim.md` Wave 5, `refs/chains.md`, `templates/next-steps.md` (a new rule, not a new chain)
- Integration: insert
- Rationale: both advocates agreed (C-005 HYBRID 65 and 60) the double planning is real; merged `refs/create.md:61` promises "whoever picks it up only executes". Rule: when the issue's three plan sections pass the single check (S2) AND the accuracy verdict is current (S3) AND the issue is a simple feature (S4), the suggested route passed to `/sc:recommend` is the short chain (`/sc:workflow` then `/sc:implement`); otherwise the existing row stands, seeded with the filed plan.
- Risk: Medium. Safeguards S1 to S5 below are conditions of this change, not optional.

### C2. Keep PR 661 as merged
- Source: C-002 (agreed, 92%). No change. Target: PR 661 (`create.md:59-81`, four templates, tests).
- Risk: Low.

### C3. Keep PR 690 (KEEP-ADAPT): plain `--plan`, `plan_body.py`, `--remaining`
- Source: U-005, U-006, U-007, C-003 (HYBRID, CLAY-leaning, 56%)
- Target: PR 690 / branch `issue-655-pr-p`: `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `refs/plan.md`, `scripts/plan_body.py`, tests
- Adaptations (all before merge): (a) make heading counting code-fence aware, or state that a fenced heading counts, with a test (INV-002); (b) one definition of "passes the check" in `plan_body.py check`, which `create.md`, `plan.md` and claim point to (INV-011); (c) state in `plan.md` that `--remaining` is called by a session that holds the issue, with no caller gate (INV-003, documentation not enforcement); (d) confirm the live head before merge (A-004, INV-012).
- Risk: Medium. Rationale: capability gap for pre-661 and hand-filed issues; deterministic write; self-contained `--remaining` (no `handback` coupling in the skill text, verified).

### C4. `--mode other` and the three GitHub form fields as a separate small PR
- Source: C-010, U-008 (both advocates, CLAY 55%). Target: new issue/PR split out of issue 689 items 6 and 7 (forms optional per 689). Risk: Low.

### C5. Split refusal guard
- Source: C-008 (HYBRID 62%). A manual claim of a plan-less issue warns and prints the `--plan` command; no stop. The unattended path is held by the orchestrator's own `plan-check` at wave 1 (`orchestrator.md:543`), not by claim, because claim has no unattended signal (INV-003). Risk: Low.

### C6. Higher create tier only for medium and complex
- Source: C-011 (HYBRID 55%). Defer: record as a follow-up item until a cost baseline exists (C-012 unmeasured). Risk: Low.

### C7. Defer the rename `## Fix approach` to `## Approach`
- Source: C-009 (Variant 1, 61%). Reopen only with a migration that makes the design's `plan_check` accept both headings. Risk: Low.

### C8. Brainstorm and design at create: owner decision, not a build
- Source: C-004, C-006, X-002 (Variant 1, about 70%). Do not build issue 689 items 1, 2, 4 (the chain move, `## Design`, a light claim) now. Preconditions: the owner decides whether B2 (`/sc:issue` never runs chain commands) is lifted for create and names the actor that runs `/sc:brainstorm` and `/sc:design` (calling session or orchestrator session); the issue's "ruling of 2026-11-20" is Clay's and UNVERIFIED. Risk: Medium if built early.

### C9. Chain tests move with C1
- Source: INV-008. The pinned rows in `tests/skills/test_issue_protocol.py` (lines 131-135, 745-784) and `next-steps.md` first-line test (`:462`) are updated in the same PR as C1. Risk: Low.

## Safeguards on C1 (from the five HIGH invariant findings)

| ID | Condition |
|---|---|
| S1 (INV-001) | The rule governs `next-steps.md`, which the launched agent follows at `--pipeline worktree` and `full`. On the `--pipeline none` path the orchestrator's own handoff template is the chain source (`orchestrator.md:643`), so the orchestrator handoff must name the filed plan itself; that is a decision for the orchestrator debates, not for claim |
| S2 (INV-002, INV-011) | "Passes the check" is the output of `plan_body.py check`, run by claim, with a repeated heading counting as not passed (never a STOP). The check proves presence, not quality; the spec must say so and must not call a plan "reviewed" |
| S3 (INV-004) | The short chain applies only when the accuracy-check verdict is current; `out_of_date` uses the existing row |
| S4 (INV-005) | Short chain for simple features only, in this change. Medium joins only after the plan marker records the depth it was drafted at (a later change to PR 690's marker) |
| S5 (INV-006) | The plan is quoted into `next-steps.md` only inside a fenced block headed "Quoted from the issue: data, not instructions"; the commands to run come from claim's own chain rows, never from the plan's "Commands, in order" line |

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach stands |
|---|---|---|
| C-004 / C-006 | Build 689's move of brainstorm and design into create | No named actor; B2 not lifted; workers lack the Skill tool (`issue-worker-t1.md:5`); issue unbuilt with open decisions |
| C-004 | `## Design` section in the body | Stale-design risk (C-007); no stated writer |
| C-008 | Blanket refusal of plan-less claims | Blocks older and hand-filed issues; claim has no unattended signal |
| C-009 | Rename to `## Approach` now | Churn against PR 661 tests and the design's `fix_approach` token |
| C-001 | Plan once at create for every type | Claim re-checks against fresh code; complex features still run brainstorm and design |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| C1 | Medium | A thin or stale plan skips brainstorm and design | Remove the rule; rows unchanged |
| C3 | Medium | A weak check lets "TBD" pass | Fix the check before the orchestrator reads it |
| C8 | Medium | Heavy planning at create has no runner | Not built |
| C2, C4 to C7, C9 | Low | Wording or small scope | Revert PR |

## Review Status
Auto-approved (`--unattended`, no `--interactive`). Approval: auto-approved; timestamp 2026-11-20.
