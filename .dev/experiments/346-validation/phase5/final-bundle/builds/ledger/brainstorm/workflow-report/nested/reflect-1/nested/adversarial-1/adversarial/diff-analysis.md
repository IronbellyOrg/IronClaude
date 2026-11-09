# Diff Analysis: reflect reviewer-card comparison

## Metadata
- Generated: 2026-11-08T18:45:00Z
- Variants compared: 2 (Variant A = variant-1-original.md, reviewer 1, analyzer, sonnet; Variant B = variant-2-original.md, reviewer 2, qa, haiku)
- Subject under review (by both variants): plan `.dev/tasks/to-do/TASK-WF-spec-20261108-181649/TASK-WF-spec-20261108-181649.md` against spec `source.md` in the same folder
- Focus areas: correctness, coverage, deviation-classification
- Total differences found: 23
- Categories: structural (3), content (14), contradictions (3), unique (11), shared assumptions (3)

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card sections | `findings` + `t1_deviation_agreement` (D1-D4) + `self_audit` | `true_gaps` + `lexical_misses_confirmed_covered` + `findings` + `self_audit` | Medium |
| S-002 | Finding granularity | 11 findings (5 blocking, 6 minor) | 4 findings (3 blocking, 1 minor) | Medium |
| S-003 | Reference style | repo-relative refs with short `:line` plan refs | (original) absolute paths; card copy uses short refs | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Byte-identical copy vs no-`src/superclaude` pin (spec-panel.md:220) | A-F1: blocking, class `necessary`; fix by scoping the pin to the loop section or a declared rewrite of line 220 | B-F1: blocking, class `regression`; fix by a recorded narrow exception pinned in Tasks 6-7 | Medium |
| C-002 | Review-1 PASS skips the sweep without "document unchanged" (source.md:28) | A-F5: blocking `drift`; adds undefined k=1 ESCALATE tail (source.md:52) | B-F2: blocking `regression`; adds Task 6 "sweep after every terminal close" inconsistency (plan :125) | Medium |
| C-003 | Absence rules INF-005 (no role flag), INF-058 (no second stop), INF-104 (no event log, no git) | A-F7: not covered, minor `drift`; add grep/`--help` AC | B: covered by Task 1 incorporating spec "Parts"/"Termination"/"CLI outline" (lexical_misses list) | Medium |
| C-004 | New files never scanned by the severity/cap test (git ls-files only) | A-F2: blocking `drift`; add the two assertions to the command test | absent | High |
| C-005 | `tests/recommend/test_routing_refresh.py:647-648` fixed command set | A-F3: blocking `necessary`; add to Task 8, owner decides the fix | absent | High |
| C-006 | Task 2 AC needs `verify`/`close` from Task 3 | A-F4: blocking `drift`; move round-3/E-CAP tests to Task 3 | absent | High |
| C-007 | Sweep route ignores the 5-minute heartbeat condition (source.md:144) | absent | B-F3: blocking `regression`; pin combined spawn+heartbeat condition | Medium |
| C-008 | Bytes per claim not measured (source.md:72) | absent | B-F4: minor `drift` | Low |
| C-009 | E-CAP third-fix-cycle refusal | A-F6: minor `drift` | absent | Low |
| C-010 | Task 9 brief-diff AC is weak (one-line briefs) | A-F8: minor `drift`; reverse-substitute and `cmp` | absent | Low |
| C-011 | Task 11 INSTALL completeness AC trips on pre-existing untracked files | A-F9: minor `necessary` | absent | Medium |
| C-012 | U3/W/O disjointness in Task 4 metrics | A-F10: minor `drift` | absent | Low |
| C-013 | Usage block narrower than body after dropping line 23 | A-F11: minor `authorized` | absent | Low |
| C-014 | Overall verdict | FAIL (self-confidence 0.80, calibrated C 0.78) | FAIL (self-confidence 0.92, calibrated C 0.72) | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Are INF-005/INF-058/INF-104 covered? | "Three spec absence rules are not covered" (A-F7) | "treated Task 1's incorporation of 'Parts', 'Termination' and 'Script CLI outline' as covering INF-005/058/104" (B self_audit; lexical_misses list) | Medium |
| X-002 | Class of the copy/no-path conflict | `class: necessary` (A-F1) | `class: regression` (B-F1) | Medium |
| X-003 | Class of the review-1 PASS omission | `class: drift` (A-F5) | `class: regression` (B-F2) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | A | A-F2: severity/cap scan reads tracked files only, so new files go unchecked | High |
| U-002 | A | A-F3: `test_routing_refresh.py` command-set assertion breaks on a new command | High |
| U-003 | A | A-F4: Task 2 acceptance criteria unreachable before Task 3 | High |
| U-004 | B | B-F3: heartbeat half of the sweep-route condition missing | Medium |
| U-005 | B | B-F4: bytes per claim | Low |
| U-006 | A | A-F6: third-fix-cycle E-CAP | Low |
| U-007 | A | A-F8: brief-diff AC | Low |
| U-008 | A | A-F9: INSTALL completeness AC vs pre-existing untracked files | Medium |
| U-009 | A | A-F10: U3 double count (calibrator marked refuted) | Low |
| U-010 | A | A-F11: Usage narrower than body | Low |
| U-011 | A | t1_deviation_agreement on D1-D4 (D3 reclassified necessary) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | A conflict the plan inherits verbatim from a spec-internal contradiction (source.md:124 vs :125) is a plan defect, not a spec defect needing an owner decision | C-001 (both grade it blocking against the plan) | Medium | UNSTATED, promoted |
| A-002 | Reading a test statically is enough to assert it will fail; neither reviewer ran a test | C-004, C-005 | Medium | UNSTATED, promoted |
| A-003 | The executor follows task text literally and will not resolve an internal conflict itself, so an unresolved conflict in the plan is blocking | C-001, C-002 | Low | UNSTATED, promoted |

STATED assumptions (not promoted): the plan's scope is spec sections 2-4 (both briefs); the plan's `## Constraints` owner decisions override the spec (both briefs).

## Summary
- Total structural differences: 3
- Total content differences: 14
- Total contradictions: 3
- Total unique contributions: 11
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-004, C-005, C-006
- Similarity check: differences 23 of 23 comparable items; not substantially identical, debate proceeds.
- Taxonomy pre-tag: L1 = S-003, C-014; L2 = S-001, S-002, C-005, C-006, C-010, C-011, C-013, X-002, X-003, A-002; L3 = C-001, C-002, C-003, C-004, C-007, C-008, C-009, C-012, X-001, A-001, A-003 (guard/boundary/state terms)
