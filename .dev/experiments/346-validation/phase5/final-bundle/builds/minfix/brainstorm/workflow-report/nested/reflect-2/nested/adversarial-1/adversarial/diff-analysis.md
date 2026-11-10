# Diff Analysis: reviewer-card Comparison

## Metadata
- Generated: 2026-11-08T18:41:00Z
- Variants compared: 3 (variant-1 = reviewer-1, sonnet/analyzer; variant-2 = reviewer-2, haiku/qa; variant-3 = reviewer-3, opus/refactorer)
- Subject: pre-execution audit findings on plan TASK-WF-spec-20261108-181543.md against its spec source.md
- Focus: correctness, coverage, deviation-classification
- Total differences found: 20
- Categories: structural (2), content (13), contradictions (2), unique (11), shared assumptions (3; promoted 2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Finding count and grain | 7 findings (1 blocking, 6 minor) | 2 findings (1 blocking, 1 minor) | 5 findings (1 blocking, 4 minor) | Low |
| S-002 | Self-audit section | Present, lists checked owner decisions and brief sources | Absent (one "not checked" line) | Present, lists task order and tests not tripped | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|-------|-----------|-----------|-----------|----------|-------|
| C-001 | `tests/recommend/test_routing_refresh.py` breaks when `spec-panel-minfix.md` is added (assertion `shipped - _POST_REFRESH_ADDITIONS == active`) | R1-F1 blocking; fix: run it, allow adding the name or name the blocked outcome | not raised | R3-F1 blocking; fix: add `"spec-panel-minfix"` to the set, run the test, flag as unlisted edit | High | L3 (validation rule) |
| C-002 | Reviewer-side "exit 2 from the reviewer's own call is corrected once and re-run" (source.md:46) missing from the shipped `## Fix Budget` text | not raised | R2-F1 blocking; fix: add the sentence to Task 5 region 4 + pin | not raised | High | L3 (guard on exit codes) |
| C-003 | "check first" tests run in Task 5 instead of the first implementation task (source.md:90) | not raised as a finding; self-audit treats placement as fine | R2-F2 minor; fix: run them at the start of Task 1 too | self-audit: those four tests are not tripped | Low | L2 |
| C-004 | Variant lands at exactly 500 lines, the `lint-architecture` limit | R1-F2 minor; add `wc -l` AC and lint runs | not raised | not raised | Medium | L3 (boundary) |
| C-005 | `check` baseline-hash verification only tested in Task 3 | R1-F3 minor; move to Task 2 | not raised | not raised | Low | L3 (guard) |
| C-006 | gross / net / add-only and the delete exemption undefined | R1-F4 minor; define and test | not raised | not raised | Medium | L3 (count divergence) |
| C-007 | Exact post-edit text of Review Loop bullet 6 not given | R1-F5 minor; write full bullet, pin owner sentence | not raised | not raised | Low | L1 (wording) |
| C-008 | `~/.claude/` precedes `.claude/` pin is ambiguous (bullet 5 names project path first) | not raised | not raised | R3-F2 minor; scope to `## Fix Budget`, lookbehind regex | Medium | L1/L3 -> L3 (validation rule) |
| C-009 | `__pycache__/*.pyc` from importlib may make Task 4's `grep -rn 'src/superclaude'` unpassable and get copied by `cp -rn` | not raised | not raised | R3-F3 minor (calibrator: should be blocking) | High | L3 (guard) |
| C-010 | Pre-run probe needs valid/invalid fixtures; no task creates them | not raised | not raised | R3-F4 minor | Medium | L2 |
| C-011 | New primitive text must avoid write-verb tokens audited by `test_worker_contract.py` | not raised | not raised | R3-F5 minor | Low | L2 |
| C-012 | 40-character quote-match rule and skill-path pin dropped | R1-F6 minor | not raised | not raised | Low | L2 |
| C-013 | Subprocess test does not prove no `superclaude` import | R1-F7 minor | not raised | not raised | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Is the Task 5 placement of the "check first" tests adequate? | Task 5's run list is incomplete (adds `tests/recommend/test_routing_refresh.py`) but placement is not challenged | Placement is wrong: source.md:90 says the first implementation task runs them | Placement holds; the four named tests are not tripped | Medium |
| X-002 | Should `tests/skills/test_model_alias_policy.py` join the regression run? | Yes (R1-F1 fix) | silent | Not tripped by the change (self-audit) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 2 | Reviewer-side exit-2 retry missing from shipped text (C-002) | High |
| U-002 | Variant 1 | 500-line ceiling with arithmetic (C-004) | Medium |
| U-003 | Variant 1 | Undefined count formulas and delete exemption (C-006) | Medium |
| U-004 | Variant 1 | Hash-check bullet placement (C-005) | Low |
| U-005 | Variant 1 | Exact bullet-6 text (C-007) | Low |
| U-006 | Variant 1 | Dropped 40-char quote match and skill pin (C-012) | Low |
| U-007 | Variant 1 | Import-isolation of subprocess test (C-013) | Low |
| U-008 | Variant 3 | Ambiguous path-order pin (C-008) | Medium |
| U-009 | Variant 3 | `__pycache__` breaks grep and install copy (C-009) | High |
| U-010 | Variant 3 | Probe fixtures missing (C-010) | Medium |
| U-011 | Variant 3 | Write-verb audit constraint (C-011) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All three grade the plan only against what its own task acceptance criteria run | The `/sc:implement` executor runs only the tests a task names, never the full suite, so a test the plan omits is a silent breakage | UNSTATED | yes |
| A-002 | V1 and V3 accept the literal `## Fix Budget` block as the authoritative command text; V2 and the T1 card (INF-032) show it omits section 2.1 step 3 requirements | The source.md section 3.2 literal block fully implements section 2.1 | CONTRADICTED | yes (flagged) |
| A-003 | All three use the same grade definition (blocking = wrong/missing deliverable, false claim, or test that cannot pass) | Shared grading rule from the brief | STATED | no |

### Promoted shared-assumption points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Executor runs only task-named tests | all three weigh omitted tests as blocking | High: decides whether C-001 is blocking | open for debate (L3: validation rule) |
| A-002 | The 3.2 literal block fully implements 2.1 | V1/V3 vs V2 + INF-032 | High: decides whether C-002 and INF-032 are plan defects or spec defects | CONTRADICTED, debate attention (L3: guard) |

## Summary
- Total structural differences: 2
- Total content differences: 13
- Total contradictions: 2
- Total unique contributions: 11
- Total shared assumptions surfaced: 3 (UNSTATED: 1, STATED: 1, CONTRADICTED: 1)
- Highest-severity items: C-001, C-002, C-009, A-001, A-002
- Taxonomy coverage: L1 (C-007), L2 (C-003, C-010, C-011, C-012, C-013, S-001, S-002, X-001, X-002), L3 (C-001, C-002, C-004, C-005, C-006, C-008, C-009, A-001, A-002)
- Similarity check: differences are well above 10% of comparable items; debate proceeds.
