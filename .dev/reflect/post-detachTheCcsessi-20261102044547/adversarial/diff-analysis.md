# Diff Analysis: reflect reviewer-card comparison

## Metadata

- Generated: 2026-11-02T05:25:00Z
- Variants compared: 2 (variant-1 = reviewer 1, analyzer, sonnet; variant-2 = reviewer 2, qa, haiku alias glm-5.3)
- Total differences found: 17 diff points (2 structural, 11 content, 3 contradictions, 1 promoted shared assumption) plus 8 unique contributions
- Categories: structural (2), content (11), contradictions (3), unique (8), shared assumptions (3 found, 1 promoted)
- Focus: correctness, coverage, deviation-classification
- Calibrated inputs: variant-1 C 0.75 (reviewer-1-calibration.md), variant-2 C 0.76 (reviewer-2-calibration.md)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Level |
|---|---|---|---|---|---|
| S-001 | Section layout | findings table, then "Specific checks" (4 prose checks), "Correctness gaps", "Adherence summary" | per-AC audit table first, then deviations table, "Judgments", "Grounding gaps" | Low | L2 |
| S-002 | AC granularity | summary count only ("13 AC audited, 13 adherent") | one row per AC with a citation (13 rows) | Medium | L2 |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Severity | Level |
|---|---|---|---|---|---|
| C-001 | `isatty()` guard at proxy:863 | necessary, LOW ("accepted, weakly"); rationale: pre-execution F14 and the inline comment | drift, MEDIUM; "no artifact documents" the guard | High | L3 |
| C-002 | extra T1 assertions (getsid :1538; exception-capturing thread, timeout=30) | getsid only: necessary, LOW | getsid plus thread wrapper/timeout: drift, LOW | Medium | L2 |
| C-003 | CHANGELOG heading suffix (:9) | drift (cosmetic), LOW | drift, LOW (folded into R2-F3) | Low | L1 |
| C-004 | CHANGELOG last sentence (:11) | authorized (by reflection F3) | drift (folded into R2-F3) | Medium | L2 |
| C-005 | `make sync-dev` before verify-sync | mentioned under constraints, not a finding | necessary deviation, LOW (R2-F4) | Low | L2 |
| C-006 | tty branch untested | grounding gap (R1-F5) | sub-point of R2-F1 | Medium | L3 |
| C-007 | macOS `os.getsid(<other pid>)` portability | grounding gap (R1-F6) | not raised | Medium | L3 |
| C-008 | verification figure | R1-F7: no "262 passed" found; only 457 | cites verify-logs/pytest-ccsession.stdout.txt:17 "262 passed" and t5-checks.log:11 "457 passed" | Medium | L2 |
| C-009 | `sys.stderr` is None (fd 2 closed) → `isatty()` AttributeError before bind | advisory correctness gap | not raised | Medium | L3 |
| C-010 | CHANGELOG:11 "the shim starts its own session" overstates for a tty start | LOW, in prose checks | sub-point of R2-F1 (soften wording) | Low | L1 |
| C-011 | `bash -n` / lint / live check provenance (implement-leg only) | "rest on the logs" (not verified) | explicit G2 grounding note; T4.AC2 "implement-run only" | Low | L2 |

## Contradictions

| # | Point of conflict | Variant 1 position | Variant 2 position | Impact |
|---|---|---|---|---|
| X-001 | Does a "262 passed" verification exist? | "I found no 262 figure in the logs I read" (R1-F7) | "verify-logs/pytest-ccsession.stdout.txt:17 262 passed" | Medium — R1-F7 inflates the grounding-gap count |
| X-002 | Class of the isatty guard | necessary | drift (MEDIUM) | High — drift counts toward the deviation ledger's blocking classes |
| X-003 | Is the guard documented? | inline comment proxy:859-862 gives the Ctrl-C reason | "no artifact documents a discovered constraint forcing the guard" | Medium — decides drift vs necessary |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | `sys.stderr` None → start-up AttributeError (C-009) | Medium |
| U-002 | 1 | macOS getsid portability; CI ubuntu only (C-007) | Medium |
| U-003 | 1 | subreaper caveat for "not a descendant" (ccsession:801-803) | Medium |
| U-004 | 1 | `pkill -f <copy path>` is a regex, slightly wider than exact-pid (plan:23) | Low |
| U-005 | 2 | per-AC audit table with citations (S-002) | High |
| U-006 | 2 | regression check: no existing test signals the shim by process group (grep killpg/getpgrp) | High |
| U-007 | 2 | `make sync-dev` classified as necessary with environmental reason | Low |
| U-008 | 2 | runtime-surface DEGRADE judged correct; ledger edge wiring nit | Low |

## Shared Assumptions

| # | Agreement source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| — | both accept T1/T2 fail-before/pass-after from logs | implement-leg logs (bash -n, lint, live check, pid snapshots) are truthful | STATED (R1 "Not verified"; R2 G2) | no |
| — | both accept CHANGELOG:11 sentence as accurate | shims already running keep the old behaviour until restarted | STATED (CHANGELOG.md:11) | no |
| A-001 | both find "no regression" and accept the T1 test as a faithful model of Orca's close | Orca's terminal close reaches processes only through the ppid-descendant sweep (plus session/process-group signals), not through a cgroup/scope kill or other mechanism the fix does not cover | UNSTATED (R1 notes the model is plan-sourced; neither verifies Orca's mechanism) | yes |

### Promoted shared assumptions

| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | Orca's close kills by ppid-descendant walk (and possibly session/group), not by cgroup/scope | High if false: the fix would not keep the shim alive in production | [SHARED-ASSUMPTION] for debate (L3: boundary) |

## Summary

- Structural: 2; content: 11; contradictions: 3; unique: 8; shared assumptions surfaced: 3 (UNSTATED 1, STATED 2, CONTRADICTED 0)
- Highest-severity items: C-001, X-002 (High); A-001 (High impact)
- Taxonomy coverage: L1 = {C-003, C-010}; L2 = {S-001, S-002, C-002, C-004, C-005, C-008, C-011, X-001}; L3 = {C-001, C-006, C-007, C-009, X-002, X-003, A-001}
- Similarity check: 17 diff points across 2 short cards — well above the 10% threshold; debate proceeds.
