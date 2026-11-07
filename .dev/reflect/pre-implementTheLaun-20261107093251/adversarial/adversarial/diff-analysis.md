# Diff Analysis: reviewer-card comparison (sc:reflect Tier 2, UC-1)

## Metadata
- Generated: 2026-11-07T09:46:00Z
- Variants compared: 3 (V1 = reviewer 1 analyzer/sonnet, V2 = reviewer 2 qa/haiku, V3 = reviewer 3 refactorer/opus)
- Total differences found: 18
- Categories: structural (3), content (6), contradictions (4), unique (5), shared assumptions (4)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Deviation count and spread | 16 findings, 0 Regression, none HIGH | 9 findings, 4 Regression, 4 HIGH | 11 findings, 2 Regression, 3 HIGH | High |
| S-002 | Severity scale used | HIGH/MEDIUM/LOW plus the non-standard "LOW-MEDIUM" | HIGH/MEDIUM | HIGH/MEDIUM/LOW | Low |
| S-003 | Extra sections beyond the table | Correctness gaps, evidence limits | Per-task acceptance table | Fix list, advisory note A, correctness gap | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 1 B-CTX gate | MEDIUM Drift: only records a verdict; later tasks not conditioned on it | HIGH Regression: turns a stop gate into a report; enforcement tasks are not conditional | Task 1 confirmed first and its evidence files exist; no finding | High |
| C-002 | Task 20 owned-hook and contract marker | MEDIUM Drift: marker undefined; header-only check would contradict IR-4 | HIGH Regression: owned/effective predicate undefined | MEDIUM Drift: marker invented; design defines no format | Medium |
| C-003 | Tasks 19 and 20 L2 status | MEDIUM Drift: status line is dead output after Task 20 refuses | HIGH Regression: Task 19 fixes status absent, Task 20 passing case could print absent | MEDIUM Drift: Task 19 tests describe a state that cannot exist | Medium |
| C-004 | Existing-test fallout of Tasks 18 and 20 | MEDIUM Drift: launch_scene stub fails any real owned-hook check; names three warning tests | not raised | HIGH Regression: about 12 "launched" tests break; lists line numbers | High |
| C-005 | Task 18 effective-registration test | not raised | HIGH Regression: matcher-ineffective registrations pass; no negative cases | not raised | Medium |
| C-006 | Task 21 L2 on a GO verdict | not raised | MEDIUM Drift: L2 dropped even on GO without authorization | not raised | Medium |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Is the refusal of governed launches (IR-7) an unapproved plan choice? | Authorized expansion: the design mandates it (DESIGN:355,514); note in PR body | Task 21 should have built more L2, not less (wants L2 delivered) | Drift HIGH: no owner decision recorded before Task 20 ships it | High |
| X-002 | Severity of the B-CTX gate defect | MEDIUM Drift | HIGH Regression | No defect (Task 1 adherent) | High |
| X-003 | Classification of test breakage and plan gaps | Drift (no Regression anywhere) | Regression for plan gaps although nothing ran | Regression for predicted test failures | Medium |
| X-004 | Does Task 12 order against the identity hook conflict with existing tests? | Necessary deviation, compatible while identity stays last | not raised | Confirmed compatible (hooks.json order, freshness test literal-Bash set) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | IR-3 (pipeline.json documentation only) has no task; Task 22 and issue.md omission; Task 9 superclaude.* forms | Medium |
| U-002 | V2 | Coverage matrix omits three source clauses; T-MSG-4 to T-MSG-6 unassigned; panel F1-F8 definitions unresolvable | High |
| U-003 | V2 | Launch preflight omits the identity adapter runtime prerequisites (UV, Linux interfaces) | Medium |
| U-004 | V3 | enforcement_hook field and the ten-key return-contract test; Task 3 asks for all 18 ids while classifiers are stubs; fixture env leakage (CLAUDE_CONFIG_DIR, PATH/jq) | High |
| U-005 | V3 | Existing opt-in probe live_probe.py ignored by Tasks 1-2; Task 22 skip rule contradicts existing environment skips; upgrade-time hook order (advisory A) | Low |

## Shared Assumptions

| # | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The design (DESIGN:355, 514) is authoritative, so the IR-7 refusal is the intended end state of Task 20 | all three treat Task 20's refusal as the design's rule | High | UNSTATED, promoted |
| A-002 | Predicted test failures and ordering conflicts are correct without running any test | all three reasoned statically; V3 states it, V1 and V2 do not | High | UNSTATED, promoted |
| A-003 | A pre-execution audit may use Regression for plan-versus-existing-code contradictions | all three used the lens the assignment gave | Medium | STATED |
| A-004 | The missing spec-panel and l2-prepush files cannot be recovered from this tree | V1, V2, V3 all report absence | Medium | STATED |

## Summary
- Total structural differences: 3
- Total content differences: 6
- Total contradictions: 4
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: S-001, C-001, C-004, X-001, X-002, U-002, U-004
