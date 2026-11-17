# Diff Analysis: reviewer-card comparison (UC-1 plan audit, wonsol default)

## Metadata
- Generated: 2026-11-17T13:50:00Z
- Variants compared: 3 (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus)
- Total differences found: 17
- Categories: structural (1), content (9), contradictions (3), unique (4), shared assumptions (3)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Card shape and severity labels | 5 findings, 2 blocking, one-line claims | 5 findings, 4 blocking, one-line claims | 9 findings, 2 blocking, one-line claims | Low |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Deleting `review-panel.default.json` breaks golden/exclusion/reflect-profile tests that resolve `"default"` | F1 blocking | F2 blocking | F1 blocking | High |
| C-002 | `tpl` fixture in test_review_panel.py becomes the 3-slot wonsol panel; about 8 tests and 2 CLI tests break | F2 blocking, also test_review_cli.py:52-57,76 | F1 blocking | F2 blocking | High |
| C-003 | Task 1 anchor alias `tier5a` has two models, source says single-model aliases | silent (verified resolve_slot fine) | F3 blocking | silent | Medium |
| C-004 | `default_template_name()` returns a panel (Task 4) vs the pointer value (Task 5) | silent | F4 blocking | F4 minor | Medium |
| C-005 | Removing `@default` / template_id `default` breaks external users | F3 non-blocking | silent | silent | Medium |
| C-006 | User tier-file overrides lack tier5a-c, so the new default fails for them | silent | silent | F3 non-blocking | Medium |
| C-007 | Plugin mirror `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` not covered | F5 minor | silent | silent | Low |
| C-008 | Plan's claim that test_ccsession_tiers.py matched `muse-ember-1.0` is false | F4 minor | silent | F8 minor | Low |
| C-009 | Gateway alias strings `claude-gw-tier5a/5b/5c[1m]` exist nowhere else | F4 minor (note) | silent | F6 minor | Low |

## Contradictions
| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Do the frozen-tier golden values stay valid if the keys are renamed to `classic` | "frozen-tier golden values stay valid" (F1) | silent | renaming changes template_id and template_sha256 inside the values, ending the byte-identity proof (F1) | High |
| X-002 | Is the `default_template_name()` contradiction blocking | silent | blocking (F4) | minor (F4) | Medium |
| X-003 | Is the two-model anchor alias a defect | verified correct against resolve_slot (Verified section) | blocking contradiction with source (F3) | verified correct (Checked and correct) | Medium |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V3 | Pointer-switch test needs `pnl._default` patching, not `default_template_name`; else it cannot guard a return to a hard-coded name (F5) | Medium |
| U-002 | V3 | Smaller option: a `DEFAULT_TEMPLATE` constant loaded through the existing `@` path; duplication of `_PACKAGED_NAME` and `_TEMPLATE_ID` (F7) | Medium |
| U-003 | V3 | Plan never states that template_id continuity splits history (default vs wonsol/classic) in telemetry (F9) | Medium |
| U-004 | V2 | The coverage matrix omits spans of source.md:2, :5, :6 (F5) | Low |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | State: with `distinct_across_slots` true and single-model seat tiers, the `random` pool-exclusion falls back to the same stand-in model without error in `anthropic-only` (pool = candidates when no hard exclusion, panel.py:539-543) | All three accept Task 1/2 acceptance as passable | If a caller passes `strict_distinct` or a hard exclusion, resolve raises ExclusionExhausted instead of two Haiku | UNSTATED (promoted) |
| A-002 | Guard: no consumer outside the listed tests resolves the default by the id `default` (scripts, docs, other skills) | All three searched tests only | A missed consumer breaks at runtime after Task 3 | UNSTATED (promoted) |
| A-003 | Boundary: deleting the old default is desirable rather than keeping `default` as an alias of `classic` | Agreed by omission; only V1 F3 touches it | Changes Task 3 and every golden decision | UNSTATED (promoted) |

## Summary
- Total structural differences: 1
- Total content differences: 9
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy: L1 = S-001, C-007, C-009; L2 = C-001..C-006, C-008, X-002, X-003, U-001..U-004; L3 = X-001, A-001, A-002, A-003
