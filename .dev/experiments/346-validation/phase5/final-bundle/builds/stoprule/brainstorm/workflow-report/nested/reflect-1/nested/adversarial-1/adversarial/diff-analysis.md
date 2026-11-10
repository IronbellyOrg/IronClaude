# Diff Analysis: reflect reviewer-card comparison (plan TASK-WF-spec-20261108-181616 vs source.md)

## Metadata
- Generated: 2026-11-08T18:41:00Z
- Variants compared: 3 (V1 = reviewer-1 analyzer/sonnet, V2 = reviewer-2 qa/haiku, V3 = reviewer-3 refactorer/opus); each card carries its blind calibration block
- Total differences found: 39
- Categories: structural (3), content (21), contradictions (4), unique (7), shared assumptions (4)
- Focus: correctness, coverage, deviation-classification
- Produced inline by the orchestrator (mechanical comparison of three YAML finding cards)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Finding granularity | 12 findings, each with id, severity, category, evidence, recommendation | 2 findings plus an adherence summary (35 units, 33 adherent) | 12 findings plus 1 advisory, and an overall verdict field | Medium |
| S-002 | Deviation counts | authorized 1, necessary 1, drift 0, regression 0 (from confirmed A2/A3) | authorized 0, necessary 0, drift 2 | authorized 1, necessary 1, drift 1; not tied to finding ids | Medium |
| S-003 | Verdict surface | no overall verdict; blocking count 3 | no overall verdict; blocking count 2 | explicit `verdict: FAIL`, blocking count 2 | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Task 5 uses Task 6's count function (forward reference) | F2 blocking | not raised | not raised | Medium |
| C-002 | Task 3 `begin` recomputes prior verdict before status/verdict code exists (Tasks 4-5) | F1 blocking | not raised | not raised | Medium |
| C-003 | Task 7 replay needs a sentinel-bearing review-2 prior report | F3 blocking | not raised | not raised | High |
| C-004 | Variant Usage line still advertises `--unattended`, `--report-dir`, `--improve` | F4 minor | not raised | R3-1 blocking | Medium |
| C-005 | Spec test "two claims on one prior counted once" absent | F5 minor | (calibrator note only) | R3-2 blocking | Medium |
| C-006 | Files created after Task 12 never staged | F6 minor | not raised | R3-8 minor | Low |
| C-007 | Task 13 lists Task 14 files before they exist | F7 minor | not raised | R3-9 minor | Low |
| C-008 | Measurement copy from the Arm B base not produced by any task | F12 minor, "not a plan defect" | QA-001 blocking drift | not raised | Medium |
| C-009 | Withdrawn claim's `prior` link not kept for `count` | not raised | QA-002 blocking | not raised | Medium |
| C-010 | Writers of final/verdict lines, source of `brief=`/`grader_model=`, undefined `parent=` | F8 minor | not raised | not raised | Low |
| C-011 | `apply-audit` outcome for `real:true` on an unclaimed seeded hunk | F9 minor | not raised | not raised | Medium |
| C-012 | Task 7 quote-line selection rule | F10 minor | not raised | not raised | Low |
| C-013 | Stdlib import grep only in Task 3; write-verb text in new primitives | F11 minor | not raised | R3-6 minor (src/superclaude scan of stoprule.py and canaries.json; script-relative default rubric path) | Low |
| C-014 | No positive check for FR-8/FR-9 rewrite, bullet 7 suffix, no-unattended sentence | not raised | not raised | R3-3 minor | Medium |
| C-015 | test_review_severity_rule.py scans only tracked files; tests run before staging | not raised | not raised | R3-4 minor | Medium |
| C-016 | Task 12 omits tests/agents, tests/docs, tests/cli | not raised | not raised | R3-5 minor | Low |
| C-017 | Rubric hash test reading a plan artifact breaks after archive | not raised | not raised | R3-7 minor | Low |
| C-018 | Section-5 templates (offline audit, replay gate) outside stated scope | not raised | not raised | R3-10 minor | Low |
| C-019 | finding-grader frontmatter omits `category:` | not raised | not raised | R3-11 minor | Low |
| C-020 | test_routing_refresh.py comment goes stale | not raised | not raised | R3-12 minor | Low |
| C-021 | Integration Patterns examples still call plain `/sc:spec-panel` | not raised | not raised | R3-A1 advisory | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Severity of the Usage-line `--unattended` contradiction (C-004) | minor: doc inconsistency | silent | blocking: the plan forces the contradiction to ship because Task 10's equality test fails any fix | Medium |
| X-002 | Severity of the missing counted-once case (C-005) | minor | silent | blocking: behaviour unspecified and untested | Medium |
| X-003 | Is the measurement copy a plan deliverable (C-008) | no: section 3 omits it; only INSTALL.md wording is unverified | yes: missing deliverable, drift | silent | Medium |
| X-004 | Classification of the plan's declared deviations | Unattended removal = authorized, routing-refresh edit = necessary | both unclassified; findings classed drift | authorized 1, necessary 1, drift 1 (unmapped) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Task-ordering defects F1 and F2 (status/verdict and count code needed before the task that builds it) | High |
| U-002 | V1 | Task 7 replay cannot run without a sentinel-bearing prior report (F3) | High |
| U-003 | V1 | Underspecified writers and audit outcomes inherited from the spec (F8, F9, F10) | Medium |
| U-004 | V2 | Withdrawn carried prior would be counted as new without the `prior` link (QA-002) | Medium |
| U-005 | V3 | Positive wording checks missing; equality test excludes the replaced blocks (R3-3) | Medium |
| U-006 | V3 | Test-run ordering vs git-tracked sweeps and omitted suites (R3-4, R3-5) | Medium |
| U-007 | V3 | Scope and hygiene items (R3-7, R3-10, R3-11, R3-12, R3-A1) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|-----------|------------------|----------------|--------|--------|
| A-001 | "Blocking" means: following the plan exactly as written yields a wrong or missing deliverable, and an implementer may NOT read ahead to later tasks | All three grade ordering and coverage gaps as blocking or minor without stating whether read-ahead is allowed | UNSTATED | Decides whether C-001, C-002, C-004, C-005 are blocking | Promoted [SHARED-ASSUMPTION] |
| A-002 | Owner rulings in the plan's Constraints outrank source.md text (Unattended removal, test edit, brief rulings) | V1 and V3 treat them as authorized; V2 does not mention them | UNSTATED | Decides X-003 and X-004 | Promoted [SHARED-ASSUMPTION] |
| A-003 | The sibling checkouts (`exp346-ab-ctl-r1`, `exp346-p1-logs`) and `/tmp/impl/exp/s1/` will still exist when the plan is executed | All three take Task 7 and Task 14 inputs as available | UNSTATED | Task 7 and Task 14 may block at execution time | Promoted [SHARED-ASSUMPTION] |
| A-004 | The lexical coverage misses INF-003, INF-009 and INF-034 are covered by Tasks 9, 3 and 6 | V1 and V2 state it; V3 does not dispute it | STATED | none | Not promoted |

## Summary
- Total structural differences: 3
- Total content differences: 21
- Total contradictions: 4
- Total unique contributions: 7
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-003
- Taxonomy pre-tag: L1 = S-003, C-019, C-020, C-021; L3 = C-002, C-005, C-009, C-011, X-002, A-001; L2 = all others
- Similarity check: differences are well above 10% of comparable items; debate proceeds
- Convergence denominator: S 3 + C 21 + X 4 + A 3 promoted = 31
