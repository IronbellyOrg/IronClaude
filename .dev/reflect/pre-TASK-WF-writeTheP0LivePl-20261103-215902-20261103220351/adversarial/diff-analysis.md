# Diff Analysis: Tier 2 reviewer-card comparison (sc:reflect UC-1 pre, Wave 4)

## Metadata
- Generated: 2026-11-03T22:40Z
- Mode: A (`--compare R1,R2,R3`), depth standard, focus correctness, coverage, deviation-classification
- Variants compared: 3
  - Variant 1 = `reviewer-cards/reviewer-1-card.yaml` (analyzer, sonnet; calibrated 0.87; R1-06, R1-11 weak)
  - Variant 2 = `reviewer-cards/reviewer-2-card.yaml` (qa, haiku/glm; calibrated 0.86; R2-08 weak)
  - Variant 3 = `reviewer-cards/reviewer-3-card.yaml` (refactorer, opus; calibrated 0.87; R3-03 weak)
  - Reference: Tier 1 card `t1-card.md` (calibrated 0.82), findings F-001..F-017
- Subject: `.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md` (below `plan`)
- Total differences found: 25 diff points (structural 2, content 18, contradictions 1, shared assumptions 4) plus 9 unique contributions
- Weighting rule: calibrated score and per-finding sound/weak only; self_confidence ignored.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card form | YAML, 12 findings, t1_ref + stance | YAML, 9 findings, t1_ref + stance | YAML, 9 findings, t1_ref + stance | Low |
| S-002 | Scope partition | Analyzer slice F-001..F-008 plus 4 new | QA slice F-009..F-014 plus 3 new | Refactorer slice F-015..F-017 plus 6 new (several cross into other slices) | Low |

## Content Differences (shared topics)

| # | Topic | T1 | V1 (R1) | V2 (R2) | V3 (R3) | Severity |
|---|---|---|---|---|---|---|
| C-001 | Archive re-add stages superseded package | F-001 blocking | R1-01 confirm, blocking | - | - | Low (agree) |
| C-002 | FINAL reads intended failures as `issues` | F-002 blocking | R1-02 downgrade, should-fix | - | - | High |
| C-003 | No exit for parked/stalled worker | F-003 blocking | R1-03 downgrade, should-fix | - | R3-08 should-fix (adds failed-start branch) | High |
| C-004 | Step 7 drops `--run` | F-004 should-fix | R1-04 should-fix | - | R3-04 blocking | Medium |
| C-005 | Unverified Orca flags/fields | F-005 should-fix | R1-05 confirm (corrects `--task-title` as recorded) | - | R3-03 says flag risk belongs here | Low |
| C-006 | Branch-remaining name pattern | F-006 should-fix [INFERRED] | R1-06 should-fix (weak) | - | - | Low |
| C-007 | Workflow worker stages `.dev/tasks` | F-007 should-fix | R1-07 should-fix | - | - | Low |
| C-008 | No resume rule | F-008 should-fix | R1-08 should-fix, fix not keyed on artifact files | - | - | Low |
| C-009 | Task 1 "four untracked folders" AC | F-009 should-fix | R1-10 blocking | R2-01 upgrade, blocking | R3-05 blocking | High |
| C-010 | Live-state ACs with no saved evidence | F-010 should-fix | - | R2-02 upgrade, blocking | R3-06 should-fix | High |
| C-011 | Absent `agentWait` vacuous pass | F-011 minor | - | R2-04 minor | - | Low |
| C-012 | `grep -c` exit 1 on pass | F-012 minor | R1-12 (part) minor | R2-05 minor | - | Low |
| C-013 | 240 s wait vs Bash tool timeout | F-013 minor | - | R2-03 upgrade, should-fix | - | Medium |
| C-014 | AC-0.6 transcript read not placed | F-014 minor | - | R2-06 minor | - | Low |
| C-015 | `Worktree:` free-text slot | F-015 minor | - | - | R3-01 minor | Low |
| C-016 | `Depends on:` lines | F-016 minor (change Task 4 to Task 3) | - | - | R3-02 reject | Medium |
| C-017 | Procedure inside Constraints | F-017 should-fix | - | - | R3-03 downgrade, minor (weak) | Medium |
| C-018 | Retry ladder re-runs a one-shot live check | - | R1-09 should-fix | - | R3-09 should-fix | Low (agree) |

Coverage gaps: V2 alone covers the evidence-shape items (C-010 upgrade, C-013, C-014). V3 alone covers the failed-start branch (inside C-003) and the Task 3 evidence copy (U-008). V1 alone covers staging, resume, base-ref resolution.

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact |
|---|---|---|---|---|
| X-001 | When a wrong Orca flag can be corrected | F-005 fix "Fix the procedure text before Task 2 if one is missing; the plan has not been pinned yet" and R1-05 "Correct the procedure text before Task 2 if a flag is absent" | R3-03 "the command is never corrected at run time" | High. `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:43`: "The first `T<id>: start` line is the immutability boundary: afterwards any plan/source hash differing from the latest `PLAN:` line → STOP `E-PLAN-CHANGED`". Task 1's `start` line is written before Task 1 runs, so an edit "before Task 2" halts the run. Position A's fix is an impossible sequence. |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | R1-09 retry ladder moves lc evidence and would re-run a live check (shared with R3-09, so promoted to C-018) | High |
| U-002 | V1 | R1-11 `--base-branch` may resolve to `origin/<branch>`, unpushed commit `8db29f11` (weak) | Low |
| U-003 | V1 | R1-12 step-2 turn may return `worker_done`/`question`; brief needs shell-safe quoting | Low |
| U-004 | V1 | R1-10 Task 1's own `uv run pytest` may add untracked paths | Low |
| U-005 | V2 | R2-07 plan:139 weakens spec:291 with "or state that none did" | Medium |
| U-006 | V2 | R2-08 `--report-path` comparison rule missing (weak) | Low |
| U-007 | V2 | R2-09 spec:303 wants the AC-0.6 excerpt in the phase report | Low |
| U-008 | V3 | R3-07 Task 3 AC needs the plan file copied; body never says so; `--force` removal loses it | Medium |
| U-009 | V3 | R3-02 Task 4 truly depends on Task 2 via plan:35 | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All fixes in all cards | Every fix lands in the plan before `/sc:implement` writes its first `T<id>: start` line (re-pin allowed only before it, managed-workspace.md:43) | UNSTATED | Yes |
| A-002 | C-002, C-009, C-010 severity arguments | The per-task reviewer and the managed FINAL apply AC text literally, including counts and named evidence | UNSTATED | Yes |
| A-003 | C-005, C-006, C-003 | Orca 1.4.237 behaves as `.dev/orca-command-refactor/inventory/orca-capabilities.md` records wherever it records something | UNSTATED | Yes |
| A-004 | F-003, R1-03, R3-08 fixes | The coordinator may `worker-stop` a worker that is parked on a human prompt (non-null `agentWait`) or blocked on an unanswered decision question | CONTRADICTED | Flagged for debate. orca-capabilities.md:114 "Use only after positive proof"; :129 "A waiting worker is healthy, not failed"; :125 "Absence never authorizes stop, abandon, retry, or release"; :111 "Never release because of timeout, ... question, escalation" |

Evidence correction (not a diff point): `reviewer-2-calibration.md` says R2 "misses that Task 5's `git add .dev/tasks` also stages the untracked reflect folder". That is false: the reflect folder is `.dev/reflect/...`, outside `.dev/tasks/`, so `git add .dev/tasks` (plan:139) cannot stage it. The note carries no weight in the debate.

## Summary
- Structural differences: 2
- Content differences: 18
- Contradictions: 1
- Unique contributions: 9
- Shared assumptions surfaced: 4 (UNSTATED 3, STATED 0, CONTRADICTED 1)
- Highest-severity items: C-002, C-003, C-009, C-010, X-001, A-004
- Similarity check: 25 diff points over 30 findings; well above the 10% threshold, debate runs.
