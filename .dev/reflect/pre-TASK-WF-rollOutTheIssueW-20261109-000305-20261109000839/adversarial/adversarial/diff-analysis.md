# Diff Analysis: reflect reviewer-card Comparison

## Metadata
- Generated: 2026-11-09T00:24:00Z
- Variants compared: 2 (Variant A = variant-1-original.md = reviewer-1, sonnet/analyzer; Variant B = variant-2-original.md = reviewer-2, haiku/qa)
- Input format note: both inputs are YAML reviewer cards (not .md); used as-is after the warning.
- Total differences found: 15 (plus 4 shared assumptions)
- Categories: structural (3), content (4), contradictions (0), unique (8)
- Taxonomy: L1 = S-001, S-002; L2 = S-003, C-001..C-004, A-001, A-002, A-004; L3 = A-003. All three levels covered.

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Self-audit field | Has `self_audit` listing the claims it checked and found sound | No `self_audit`; a `note` with the plan path instead | Low |
| S-002 | Finding ID scheme | Only `F`-IDs (F1, F3, F4, F5) | Mixed: F2 plus QA-02, QA-03, QA-04 | Low |
| S-003 | Severity spread | 1 medium, 3 low | 1 high, 3 medium | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | Plan tasks covered | Task 2 (design doc table AC) and Task 4 (runbook 8.7 / section 16) | Task 1 (capture packaging, secret check) and Task 5 (fixture replacement and tests) | High |
| C-002 | Tier 1 findings confirmed | Confirms T1 F1 and F3 | Confirms T1 F2 | Medium |
| C-003 | Evidence base | Design doc, runbook and audit.py lines | Plan lines, source.md, test_github.py, fixture JSON | Low |
| C-004 | Calibration gap | Self 0.88, calibrated 0.74 (gap 0.14); F3 judged overstated | Self 0.95, calibrated 0.72 (gap 0.23); QA-02 judged high -> medium, bundles 3 claims | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| (none) | No falsifiable claim in one card is denied by the other; the cards review disjoint tasks. | n/a | n/a | n/a |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | F1: Task 2 AC 4 loop over every backticked name in the 4.3 table reports failed/unknown/abandoned (and later once) as misses | High |
| U-002 | A | F3: Task 4 AC 1 `grep -c` gives no expected number (calibrator: overstated, AC implies 2) | Low |
| U-003 | A | F4: runbook section map at setup.md:5 goes stale after 8.7 and section 16 | Low |
| U-004 | A | F5: plan does not locate the "scheduler is the owner's choice" sentence (setup.md:202) | Low |
| U-005 | B | F2: token grep covers only tests/issue_watch/fixtures/, not ./artifacts/captured/ in the always-staged package | Medium |
| U-006 | B | QA-02: plan:108 (one capture per fixture) contradicts plan:110 (uncaptured fixtures stay); every-fixture gate weakened | High |
| U-007 | B | QA-03: include fixture keeps its data in `raw`, not `payload`; replacing `payload` leaves tested data guessed | High |
| U-008 | B | QA-04: test_github.py:566-567 hardcodes the guessed Date timestamp; real capture fails it | Medium |

## Shared Assumptions

| # | Agreement Point | Precondition | Classification | Promoted |
|---|-----------------|--------------|----------------|----------|
| A-001 | Both class every finding `plan-gap` | No finding traces to a source/spec defect (yet QA-02 partly rests on source.md:22 "every" vs source.md:24 "about 12+") | UNSTATED | [SHARED-ASSUMPTION] |
| A-002 | Both cite plan and design line numbers as fixed anchors | Citations stay valid after Task 2 inserts the exit-1 row (calibrator: fixtures cite stale design lines) | UNSTATED | [SHARED-ASSUMPTION] |
| A-003 | Both keep live test, shadow run and cron owner-run, `enabled` false | The enable guard holds until the owner flips it (plan constraints, source) | STATED | no |
| A-004 | Neither card reviews Task 3 | Task 3 (runbook 10.2/14.1 edits) is sound as written (calibrator: argv AC and "byte-identical" range undefined) | UNSTATED | [SHARED-ASSUMPTION] |

## Summary
- Total structural differences: 3
- Total content differences: 4
- Total contradictions: 0
- Total unique contributions: 8
- Total shared assumptions: 4 (3 promoted)
- Highest-severity items: C-001 (disjoint task coverage), U-006 QA-02, U-007 QA-03, U-001 F1
- Difference ratio well above 10%: debate proceeds. Convergence denominator = S + C + X + A = 3 + 4 + 0 + 4 = 11.
