# Diff Analysis: reviewer-card Comparison (refactor cycle 1)

## Metadata
- Generated: 2026-10-23T03:31:00Z
- Variants compared: 2 (Variant 1 = reviewer-1 card, sonnet, analyzer; Variant 2 = reviewer-2 card, haiku slot grok-4.7, qa)
- Subject: pre-execution review of tasklist TASK-WF-specR1-20261023-031725 against its source.md (spec + cycle-1 review feedback)
- Focus: correctness, coverage, deviation-classification
- Calibration inputs (opus, blind): Variant 1 C=0.84; Variant 2 C=0.76. Calibrator downgrades: R2-2 medium to low (source:39 states the final scope check at directory level). Calibrator-2 independently raised the R1-1 hash-cmp risk.
- Total differences found: 15
- Categories: structural (1), content (6), contradictions (3), unique (9, listed separately), shared assumptions (3)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Finding count | 12 findings, also verifies prior M-01..M-18 | 8 findings, no prior-finding audit | Low | L1 |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity | Level |
|---|-------|--------------------|--------------------|----------|-------|
| C-001 | Task 9 accepts any path under .github/workflows/ (tasklist:184) | R1-4 medium: require the changed set under .github/workflows/ to equal exactly the four named files | R2-2 medium (calibrated low): same fix | Medium | L3 (validation rule) |
| C-002 | Depends on chain vs source:82 | R1-12 low, optional: precondition bullet in Tasks 8/9 that t5/t6/t7 check logs exist and pass | R2-1 medium: re-chain (calibrator's working chain 4->1, 5->4, 6->5, 2->6, 7->2, 8->7, 9->8, Task 3 artifact named in body) | Medium | L2 (dependency) |
| C-003 | -z rename entries (tasklist:37, :178) | R1-6 low: R/C entry yields new and old path lines; old path MISSING if gone | R2-3 low: status, old, new each recorded; new path outside allow-list fails | Low | L3 |
| C-004 | `::warning` literal "advisory" (tasklist:84 vs :96) | R1-7 low: confirm C3, put the word in the instruction | R2-7 low: reject C3 as a defect; check already enforces source:55 | Low | L1 (wording) |
| C-005 | "no `<` placeholder" (tasklist:128) | R1-10 low: reword to zero `<` characters; forbid heredoc PR body | R2-6 low: reword to zero `<` characters | Low | L1 |
| C-006 | Fail-closed push-before-list (C5) | R1-11 low: acceptable, optional note in t6 notes | (not raised; R2 self_audit says C5 matches spec) | Low | L3 (guard) |

## Contradictions

| # | Point of conflict | Variant 1 position | Variant 2 position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Overall readiness | ready_with_notes (self 0.72) | not_ready (self 0.76) | High |
| X-002 | Severity of the dependency-chain issue | low, optional, "Task 9 positive check would catch a premature run" | medium, source:82 not met | Medium |
| X-003 | Is C3 a plan defect | yes (low) | no | Low |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | 1 | R1-1: Task 9 `cmp` of hash files is not exempt for the tooling roots; a rewritten pre-existing file under .dev/reflect/ fails a correct run (tasklist:37, :183-184). Independently confirmed by the reviewer-2 calibrator. | High |
| U-002 | 1 | R1-2: no check that `gh pr list` keeps `--head sync/framework --base master`; the stub prints the count regardless of arguments (tasklist:117, :128-133) | High |
| U-003 | 1 | R1-3: Task 5 has no whole-document comparison for boundary-guard.yml (runs-on, env, checkout, fetch-depth: 0) (tasklist:93-106; boundary-guard.yml:38-48) | Medium |
| U-004 | 1 | R1-5: Decision-line format ambiguous (`files` contains `file`); fix a format and regex (tasklist:48, :52, :145) | Low |
| U-005 | 1 | R1-8: Task 9 states the 3,000 conclusion ahead of Task 3's quote (calibrator: follows source:80, weak) | Low |
| U-006 | 1 | R1-9: leftovers list omits scripts/README.md line 30 (calibrator: a stretch) | Low |
| U-007 | 2 | R2-4: job-name check forbids the substring "required" (tasklist:95) | Low |
| U-008 | 2 | R2-5: Task 7's "do not edit t2" is only checked by the Decision count; an appended note passes (tasklist:140, :147) | Low |
| U-009 | 2 | R2-8: coverage-matrix corrections (missing rows; INF-025, INF-033 best_item wrong) — reflect artifact, not tasklist | Low |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | /sc:implement runs tasks in number order, so the prose rule at tasklist:31 actually holds at execution time | Both treat the Depends chain as a documentation/ordering question, not a runtime hazard | UNSTATED | Medium | Promoted [SHARED-ASSUMPTION] |
| A-002 | A PATH-prepended `git` stub that execs the real git by absolute path works inside the extracted `run:` body (no `command git`, no absolute /usr/bin/git calls in the body) | Both accept the stub design of Task 6 runs (a)-(d) | UNSTATED | Low | Promoted [SHARED-ASSUMPTION] |
| A-003 | No finding is high: with the medium fixes applied the plan meets every spec item | Neither card files a high | UNSTATED | High | Promoted [SHARED-ASSUMPTION] |

## Summary
- Total structural differences: 1
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 9
- Total shared assumptions surfaced: 3 (UNSTATED: 3)
- Highest-severity items: X-001, U-001, U-002, A-003
- Convergence denominator (S + C + X + A): 1 + 6 + 3 + 3 = 13
- Taxonomy coverage: L1 (S-001, C-004, C-005), L2 (C-002, X-001, X-002, A-001, A-003), L3 (C-001, C-003, C-006, A-002); all levels present.
