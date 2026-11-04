# Diff Analysis: reviewer-card comparison

## Metadata
- Generated: 2026-11-04T13:45:00Z
- Variants compared: 3 (variant-1 = reviewer 1, analyzer, sonnet; variant-2 = reviewer 2, qa, haiku alias glm-5.3; variant-3 = reviewer 3, refactorer, opus)
- Subject: pre-execution review of plan .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md (issue #357, bare python hook)
- Focus: correctness, coverage, deviation-classification
- Total differences found: 26
- Categories: structural (2), content (18), contradictions (3), unique (10, overlapping content rows), shared assumptions (3)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Finding count and granularity | 11 findings (2 blocking) | 6 findings (2 blocking) | 11 findings (5 blocking) | Low |
| S-002 | Fix field coverage | 8 of 11 have a fix | 5 of 6 have a fix | 9 of 11 have a fix | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Task 3 breaks tests/hooks/test_freshness_subagent_start_policy.py:102-105 | R1-F1 blocking; narrow assertion to freshness-/counter commands; run tests/hooks | R2-F1 blocking; assert the only Bash registration is block-bare-python.sh; run that file in Task 4 | R3-F1 blocking; narrow to freshness-*; add `uv run pytest tests/hooks tests/cli -q` to Task 4 | Medium (fix approach differs) |
| C-002 | No allowed `;`-chained case in Task 2 | R1-F2 blocking; add several allowed `;` cases | R2-F2 blocking; add one allowed `;` case | absent | Medium |
| C-003 | Heredoc body handling | R1-F5 minor (apostrophes in bodies flip quote state; list as ceiling) | absent | R3-F2 blocking (drop bodies of non-shell heredocs; apostrophe corrupts quote tracking; tests) | High |
| C-004 | Unquoted `#` comments | absent | absent | R3-F3 blocking (strip comments before splitting) | Medium |
| C-005 | Backslash-newline continuation | R1-F4 minor (join before splitting; tests) | absent | R3-F4 blocking (same fix) | Medium |
| C-006 | Command substitution inside double quotes | R1-F5 minor (handle or list as ceiling) | absent | R3-F5 blocking (handle, or document and pin with a test) | High |
| C-007 | Option-taking wrappers, xargs, find -exec, bash -c | R1-F4/F5 minor | R2-F6 minor (document) | R3-F6 minor (skip options or document) | Low |
| C-008 | Fail-open under tokenizer, jq or set -u error | R1-F6 minor | R2-F3 minor (jq-missing branch untested) | R3-F7 minor (exit 2 only on positive jq block result) | Low |
| C-009 | Goal says "the one bare python3 -c in the installed skills" | R1-F8 minor (also template 02 line 965) | R2-F4 minor | absent | Low |
| C-010 | Under-1-second timing assertion | R1-F11 minor | absent | R3-F8 minor (+ jq-missing test guard) | Low |
| C-011 | Task 7 permission mode and live-state checks | absent | absent | R3-F9 minor | Medium |
| C-012 | CHANGELOG task is a scope addition | R1-F9 minor | absent | absent | Low |
| C-013 | Install test passes explicit target, no default-HOME path | R1-F10 minor | absent | absent | Low |
| C-014 | Missing Depends on (Task 5 on 1; Task 6 on 5) | R1-F7 minor | absent | absent | Low |
| C-015 | Constraints line 20 says Task 6 for the live check (is Task 7) | absent | absent | R3-F11 minor | Low |
| C-016 | Splitting at `(` blocks array assignments | absent | absent | R3-F10 minor | Low |
| C-017 | Coverage-matrix misattribution INF-007/INF-010 | absent | R2-F5 minor | absent | Low |
| C-018 | Task 5 `uv run --no-project python` vs Done-when literal | R1-F3 minor refinement | absent | absent | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 3 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Severity of backslash-newline gap | minor (R1-F4: "behaviour is ambiguous") | blocking (R3-F4: the allowed `uv run \<nl> python` form is blocked) | Medium |
| X-002 | Severity of unchecked `$(...)` inside double quotes | minor (R1-F5: "consistent with the issue's quoted-text wording") | blocking (R3-F5: Done-when requires blocking any command that runs bare python) | High |
| X-003 | Severity of heredoc body scanning | minor (R1-F5 mentions heredoc apostrophes as a ceiling) | blocking (R3-F2: blocks text-only heredocs that never execute) | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 3 | `#` comment stripping (C-004) | High |
| U-002 | 3 | Task 7 permission scope and live-state record (C-011) | Medium |
| U-003 | 3 | Array assignment split (C-016) | Low |
| U-004 | 3 | Constraints Task 6/Task 7 mislabel (C-015) | Medium |
| U-005 | 1 | CHANGELOG scope addition (C-012) | Low |
| U-006 | 1 | Default-HOME install test (C-013) | Medium |
| U-007 | 1 | Missing Depends on (C-014) | Low |
| U-008 | 1 | Task 5 refinement vs literal Done-when (C-018) | Medium |
| U-009 | 2 | jq-missing fail-open test (C-008) | Medium |
| U-010 | 2 | Coverage-matrix misattribution (C-017) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-001 (all three: blocking, narrow the test) | Narrowing an existing pinned invariant test is within this plan's scope and needs no owner sign-off | UNSTATED | Yes |
| A-002 | All three phrase fixes as "add to the plan" / "change Task N" | The plan will be edited before execution. (The /sc:workflow protocol forbids editing the plan from reflect findings; findings can only be applied during /sc:implement.) | UNSTATED | Yes |
| A-003 | C-003/C-005/C-006 fixes (all assume jq or awk can host the richer tokenizer) | A jq regex or awk tokenizer can implement heredoc, comment, continuation and nested-substitution handling within the 3 s timeout without Python | UNSTATED | Yes |
| (A-004) | All three | The hook is advisory and fail-open, not a security boundary | STATED (plan Constraints line 21; issue) | No |

## Summary
- Total structural differences: 2
- Total content differences: 18
- Total contradictions: 3
- Total unique contributions: 10
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-003, C-006, X-002, X-003
- Taxonomy: L1 = S-001, S-002, C-009, C-015, C-017; L2 = C-001, C-002, C-011, C-012, C-013, C-014, C-018, A-001, A-002; L3 = C-003, C-004, C-005, C-006, C-007, C-008, C-010, C-016, X-001, X-002, X-003, A-003
- Similarity check: differences well above 10%; debate proceeds.
