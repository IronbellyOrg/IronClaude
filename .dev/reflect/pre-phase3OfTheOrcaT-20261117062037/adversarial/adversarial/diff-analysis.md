# Diff Analysis: reviewer-card Comparison (UC-1 pre-execution review of the phase 3 plan)

## Metadata
- Generated: 2026-11-17T06:31Z
- Variants compared: 3 (variant-1 analyzer/sonnet, variant-2 qa/haiku, variant-3 refactorer/opus)
- Variants: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/reflect/pre-phase3OfTheOrcaT-20261117062037/adversarial/adversarial/variant-{1,2,3}-original.md
- Plan under review: .dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md
- Total differences found: 3 structural, 15 content, 4 contradictions, 10 unique contributions, 6 shared assumptions
- Verified facts (orchestrator, Grep this run): `Collector(` is constructed at commands.py:218 and commands.py:350 and nowhere else in src/superclaude/cli/observe/; view.py:914 selects `KEYS_LINE if panel is None else QUESTIONS_KEYS_LINE`; export.py:131-134 and :195 export `dispatchId` for every worker row.

## Structural Differences
| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Finding count and BLOCKING count | 8 findings, 1 BLOCKING | 4 findings, 3 BLOCKING | 12 findings, 1 BLOCKING | Medium |
| S-002 | Self-reported confidence | 0.65 | 0.97 | 0.80 | Low |
| S-003 | `checked` section | lists confirmed-correct items | lists per-INF coverage reasoning | lists reads and an explicit "not checked" | Low |

## Content Differences
Tag = taxonomy level (L1 surface, L2 structural, L3 state mechanics).

| # | Topic | V1 | V2 | V3 | Level | Severity |
|---|-------|----|----|----|-------|----------|
| C-001 | The `--once` path (`run_once`, commands.py:218) never gets `link=` | F1 BLOCKING | F2 BLOCKING | F1 BLOCKING | L2 | High |
| C-002 | `QUESTIONS_KEYS_LINE` change alters link-off behaviour (view.py:78-81, 914) | F3 MEDIUM Regression | F3 BLOCKING Regression | F3 MEDIUM Regression | L2 | High |
| C-003 | Task 6 "no dispatch id in the snapshot" contradicts exported `rows[].dispatchId` | F6 MEDIUM | F1 BLOCKING Regression | F5 MEDIUM Drift | L2 | High |
| C-004 | Source of the "link on" state is undefined; gating `n`/`p` on `view.desk` cannot make the first selection | F2 MEDIUM | not raised (INF-008 "partial") | F2 MEDIUM | L3 | Medium |
| C-005 | Selection has no data path into `_panel_lines`; desk height can collapse the whole question list (render.py:304-323, 369-395) | F4 MEDIUM | not raised | F12 NOTE (selected flag, marker `>` already means truncated) | L3 | Medium |
| C-006 | Join must use typed `row.raw.dispatch_id`; the id pattern admits `unknown`; export `q.dispatch_id or "unknown"` | F5 MEDIUM | not raised | F11 NOTE | L3 | Medium |
| C-007 | Task 3 says "module docstring (lines 87-95)"; it is the HELP string with a pinned sentence (test_commands.py:739-742) | F8 NOTE | not raised | F7 MEDIUM Regression | L2 | Medium |
| C-008 | No reason string for a present-but-invalid `dispatchId` | F7 NOTE | not raised | not raised | L1 | Low |
| C-009 | No acceptance assertions for desk missing values or stale/as-of note | not raised | F4 MEDIUM | not raised | L3 | Medium |
| C-010 | Task 4 is too large; split into 4a and 4b | not raised | not raised | F4 MEDIUM Drift | L2 | Medium |
| C-011 | ARCHITECTURE-SPINE.md AD-18 says Stage C adds `links.py` and a field group; no task amends it | not raised | not raised | F6 MEDIUM Drift | L2 | Medium |
| C-012 | Planned `question_message` builder duplicates `make_question_rows` (conftest.py:239-271) and omits `body`/`to_handle` | not raised | not raised | F8 MEDIUM Drift | L2 | Medium |
| C-013 | rendering-rules.md lines 21, 24, 43 stay stale (global keys, evicted selection note, "two-column is R3") | not raised | not raised | F9 MEDIUM Gap | L2 | Medium |
| C-014 | Post-link default (B or C) re-confirm not recorded | not raised | not raised | F10 NOTE | L1 | Low |
| C-015 | INF-009 (argv log unchanged) check | "no acceptance check; existing tests only" | "not wholly untested; a link-enabled argv assertion would strengthen" | "only a constraint" | L2 | Medium |

## Contradictions
| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Severity of the keys-line defect (C-002) | MEDIUM | BLOCKING | MEDIUM | Medium: decides whether the plan must be revised before execution |
| X-002 | Severity of the snapshot dispatch-id check (C-003) | MEDIUM | BLOCKING | MEDIUM | Medium: same |
| X-003 | Is INF-009 untested? | untested (existing tests only) | not wholly untested | constraint only | Low |
| X-004 | Is the stacked-block narrowing of C (INF-007) a deviation? | not raised | partially covered | Necessary (C is undefined in rendering-rules.md:8), but spec line 43 stays stale | Low |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Order the desk height before the list so the desk is dropped, never the list (C-005) | High |
| U-002 | V1 | Typed join on `row.raw.dispatch_id`, skip UNKNOWN (C-006) | High |
| U-003 | V1 | Reason string for invalid `dispatchId` (C-008) | Low |
| U-004 | V2 | Desk missing-value and stale/as-of assertions (C-009) | Medium |
| U-005 | V2 | Byte-for-byte link-off screen comparison with questions on at all three widths | High |
| U-006 | V3 | Split Task 4 (C-010) | Medium |
| U-007 | V3 | Amend ARCHITECTURE-SPINE AD-18 (C-011) | Medium |
| U-008 | V3 | Reuse `make_question_rows` (C-012) | Medium |
| U-009 | V3 | Update rendering-rules.md lines 21, 24, 43 and the evicted-selection note (C-013) | Medium |
| U-010 | V3 | Record the post-link default (C-014) | Low |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|-------|-----------|------------------|----------------|----------|
| A-001 | The two Collector sites (commands.py:218, :350) are the only places `link` must be wired | C-001 (all three) | UNSTATED, verified true by Grep | Yes |
| A-002 | `n` and `p` are free keys in every focus mode | all three accept the key design | UNSTATED (apply_key handles ctrl_c, up/k, down/j, d/u, q, e, m, escape, enter, `/`, h; filter focus routes all text to `_filter_key`) | Yes |
| A-003 | A plan executor follows plan text literally, so every ambiguity becomes wrong code | all three grade by "executor would produce" | UNSTATED | Yes |
| A-004 | The stacked block is an acceptable reading of "Decision Desk composition (C)" | no variant objects | UNSTATED (rendering-rules.md:8 leaves C's contents undefined) | Yes |
| A-005 | `RowView` and `Row` carry what the join needs (`dispatch_id`, `worktree_id`) | all three | STATED | No |
| A-006 | Plan-versus-code findings are reliable without running tests | all three ran no tests | UNSTATED | Yes |

## Summary
- Total structural differences: 3
- Total content differences: 15
- Total contradictions: 4
- Total unique contributions: 10
- Total shared assumptions surfaced: 6 (UNSTATED: 5, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003
