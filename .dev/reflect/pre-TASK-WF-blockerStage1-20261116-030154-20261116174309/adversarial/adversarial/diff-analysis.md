# Diff Analysis: reviewer-card comparison (stage 1 plan re-review)

## Metadata
- Generated: 2026-11-16 (orchestrator-authored, inline; analytical agent not spawned)
- Variants compared: 3 (V1 = reviewer 1 analyzer/sonnet, V2 = reviewer 2 qa/haiku, V3 = reviewer 3 refactorer/opus), files `variant-N-original.md`
- Plan under review: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (`PLAN:n`); spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (`SPEC:n`)
- Total differences found: 22 diff points
- Categories: structural (2), content (12), contradictions (4), unique (6), shared assumptions (4)
- Taxonomy auto-tags (L3 over L2 over L1): L1 = S-001, S-002, C-006, C-012; L2 = C-002, C-003, C-004, C-005, C-009, C-010, C-011; L3 = C-001, C-007, C-008, X-001..X-004 where a state or guard term applies, A-001, A-002, A-003, A-004

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card layout | Verdict, First-review findings (F1-F9), Findings (6), Checked sound, confidence | same sections, absolute paths in F-lines, 5 findings | same sections plus a trailing "Not checked" paragraph, 6 findings | Low |
| S-002 | Finding numbering and grade counts | R1-F1..F6: 1 blocking, 5 non-blocking | R2-F1..F5: 3 blocking, 2 non-blocking | R3-F1..F6: 1 blocking, 5 non-blocking | Low |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity |
|---|---|---|---|---|---|
| C-001 | Task 7 grep line (`PLAN:125`) lists `.pyc` files (`grep -rln "follow_ups" src/superclaude/cli/review`) | R1-F1 BLOCKING; pycache glob evidence; fix `--include='*.py'` | R2-F1 BLOCKING; "independently confirmed" bytecode exists; fix: restrict to source files | R3-F1 BLOCKING; pycache glob evidence; fix `--include='*.py'` | High (agreed) |
| C-002 | Scale-map `labels` grammar has no family key and cannot hold conditional outcomes; Tasks 9 and 12 read it | R1-F2 non-blocking, plus multi-path `defining file` cell separator | silent (marks F5 fixed) | R3-F2 non-blocking | Medium |
| C-003 | REQ-09 (SPEC:396 cross-run matching) not in any task | R1-F3 non-blocking | silent | R3-F3 non-blocking; adds that no other stage plan owns it | Medium |
| C-004 | Task 8 does not say how `origin_repo.py` (a script, not a package) is called or faked | R1-F5 non-blocking | silent | R3-F5 non-blocking | Low |
| C-005 | Task 4 copy of SPEC:485 `.dev/pr-monitor/` versus Task 5 folder-wide grep (`PLAN:97`) | R1-F6 non-blocking | silent | R3-F4 non-blocking | Low |
| C-006 | `verify` named at `PLAN:184`; real command name is `verify-citations` (`verify_cmd.py:76`) | noted as nit inside F8 line | R2-F5 non-blocking | R3-F6 item | Low (agreed) |
| C-007 | Task 10 enables M with a required-item list only; SPEC:512 says code confirms the item is absent by name first | silent | R2-F2 BLOCKING | silent | High |
| C-008 | Task 10 returns "S, W and D always"; SPEC:516 says D needs decision-basis excerpts, SPEC:522 Option Q consumer lookup | silent | R2-F3 BLOCKING | silent | High |
| C-009 | Task 12 writes a `classifier` value into ledger rows, but the follow-ups Items table holds only Medium and needs-decision rows; no row-update call in Task 7 | R1-F4 non-blocking | silent | silent | Medium |
| C-010 | Task 1 order: SKILL.md is created before the owner-go and stage-0-summary acceptance checks run | "Task 1's first acceptance line correctly halts the run" (sound) | prerequisites not mistaken (sound) | R3-F6 sub-item: entry gate runs after the work, leaves a file behind | Low |
| C-011 | Coverage matrix of this review omits merged-spec rows and two source.md spans | silent | R2-F4 non-blocking | silent | Low |
| C-012 | Cosmetic items: stray ", ;" at `PLAN:223`; "installed-only rows checked for pointer order only" is a no-op; `PLAN:52` phrase cancels itself | silent | silent | R3-F6 sub-items | Low |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Is Task 1's gate order a defect? | sound ("correctly halts") | sound | defect (non-blocking): file created before the gate runs | Low |
| X-002 | Is first-review F5 fixed? | "partly fixed" (family key, conditional, separator missing) | "fixed" | "fixed" in F-list, same gap as R3-F2 | Medium |
| X-003 | V1 header sentence "All nine first-review fixes are in the live plan" versus its own list (F1 grep fails, F5 partly) | internal inconsistency | n/a | n/a | Low |
| X-004 | V2 states "No files were changed and no tests or commands were run" yet R2-F1 says it "independently confirmed" bytecode exists | n/a | internal inconsistency (evidence quality of R2-F1) | n/a | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | R1-F4 (classifier column target row; update call) | Medium |
| U-002 | V2 | R2-F2 (M presence check) | High if real |
| U-003 | V2 | R2-F3 (D decision-basis input / Option Q) | High if real |
| U-004 | V2 | R2-F4 (review coverage matrix limits) | Low |
| U-005 | V3 | R3-F6 cosmetic and ordering items, "Not checked" disclosure | Low |
| U-006 | V1 | packaging check (wheel includes `src/**`, so packaged refs resolve) listed as sound | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | `.pyc` files embed the plain text `follow_ups`, so `grep -rl` lists them (no variant ran grep; V1 and V3 say so) | C-001 | the blocking grade rests on it | UNSTATED (orchestrator batch c01: `grep -rln "ledger"` lists 10 `.pyc` files) |
| A-002 | An executor runs Task 7's pytest before the grep, with bytecode writing on (`PYTHONDONTWRITEBYTECODE` unset) | C-001 | whether the check fails in practice | UNSTATED |
| A-003 | A check that cannot be met as literally written is blocking even when the repair is one flag and an executor could silently adapt (precedent: first-review F1) | C-001 | grade of C-001 | UNSTATED |
| A-004 | The plan's scope for the classifier supplier is the spec's stage 1 exit tests (V1, V3 implicit) versus the whole of SPEC section 7.2 "Needs from code" (V2 implicit) | C-007, C-008 | grade of C-007 and C-008 | UNSTATED (contested) |

## Summary
- Total structural differences: 2
- Total content differences: 12
- Total contradictions: 4
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 4, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-007, C-008
- Similarity: not substantially identical (the three cards differ on 8 of 12 content points); debate proceeds
