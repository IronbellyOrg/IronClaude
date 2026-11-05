# Diff Analysis: reviewer-card comparison (UC-1 reflection of the issue 315 plan)

## Metadata
- Generated: 2026-11-05T03:50Z (orchestrator-authored; the diff-analysis step was run inline)
- Variants compared: 3 (variant-1 = reviewer 1 analyzer/sonnet, variant-2 = reviewer 2 qa/haiku, variant-3 = reviewer 3 refactorer/opus)
- Total differences found: 18 (structural 2, content 9, contradictions 3, shared assumptions 4 promoted)
- Categories: structural (2), content (9), contradictions (3), unique (see below), shared assumptions (4)
- Subject under review: the 11-task plan TASK-WF-fixGitHubIssue31-20261105-031410.md against source.md

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card shape | 14 findings, 1 blocking, mechanics-heavy | 5 findings, all minor, coverage-focused, `matrix_gaps: []` | 8 findings plus `scope_additions` list, all minor | Low |
| S-002 | Severity use | uses `blocking` once (F1) and `regression` class | never uses blocking or regression | never uses blocking or regression | Medium |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Where `--auto-name` is dispatched | F12: early fast-path case ccsession:597-628; test texts `--model`, `--claude-args`, `--shim` | silent | F1: same fix; same line ranges | Low (agree) |
| C-002 | Task 5 test list completeness | F6 adds `test_orca_invalid_name_asks_again`, fixes Ctrl+C test prompt; F7 adds CCSESSION_NAME to env exclusion | F2 adds `test_orca_invalid_name_asks_again` | F2 adds the two Enter reopen tests (`_still_asked`, `conversation_is_gone_is_asked`) and notes the "keep as they are" contradiction | Medium |
| C-003 | Auto-name collisions (same minute) | F14: add seconds or random suffix, or reserve with a marker; hook `sync_name` renames the list only, not the resume | F5: add a same-minute test, or pin the hook's `-2` suffix as the guarantee | F8: add random/pid part or atomic topic file; sync_name may hide it but `--name` and list name can differ | Medium |
| C-004 | Lifting Claude `--name`/`-n` | F10 (drift): prefer leaving it in Claude's arguments unless the owner confirms; skip for resume-like or `--session-id` launches | silent | F4 (authorized): keep as reported decision; add two acceptance cases; ask the owner | Medium |
| C-005 | `launch-paths.md` written by test code | silent | criterion treated as fine | F3 (drift): move writing to the executor, tests stay inside tmp_path | Low |
| C-006 | Exit-3 message mechanics | F2 (IFS= and leading tab), F3 (select race), F4 (python drain, size cap), F5 (`--` before text starting with `-`), F13 (INT trap, `rc=$?`) | silent | silent | High (L3) |
| C-007 | Default hint/limit for other `ask_session_name` callers | silent | silent | F5: keep timer, keep old default hint or list it in the Coder handoff | Low |
| C-008 | Plan-author exemptions (print mode, `CCSESSION_AUTOSTART=0`, non-session subcommands) | F9 (drift): non-session positionals such as `mcp`, `doctor`, `--version` must pass through untagged | silent | scope_additions: keep print mode and AUTOSTART=0 | Medium |
| C-009 | Acceptance and doc precision | F11 `=` forms; F8 CCSESSION_NAME unset before exec | F1 timer-default criterion self-contradictory; F3 README `--session-id` row | F6 Task 4 rule wording ambiguous; F7 old tests only updated in Task 5 | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Is an invalid lifted/env name or a failing `--auto-name` (ccsession exits 2, Claude never starts) a plan-blocking regression? | F1: BLOCKING regression; header promises "never ends up at a dead prompt" (ccsession-orca:20-24, ccsession:1649-1653) | not examined | F4: same mechanism for an invalid Claude `--name`, rated MINOR, class authorized, "ask owner" | High |
| X-002 | Does the hook/`sync_name` already protect against same-minute duplicate labels? | F14: renames the saved list only; a label written by another session is still resumed (ccsession:1681-1706) | F5: relies on "the hook's -2 suffix" (cited session-name.sh:10-12, which shows none per the calibrator) | F8: may hide it in the list; Claude's `--name` and the list name can differ | Medium |
| X-003 | Keep or drop the `--name` lift | F10: prefer drop unless owner confirms | silent | F4/scope: keep, ask owner | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | F1 dead-prompt regression analysis (set -e, exit 2) | High |
| U-002 | 1 | F2/F3/F4/F5/F13 shell mechanics of the exit-3 safety net | High |
| U-003 | 1 | F8 CCSESSION_NAME inherited by Claude and nested launches | Medium |
| U-004 | 1 | F9 non-session subcommands get `--name` injected | Medium |
| U-005 | 2 | F1 timer-default criterion cannot detect an unlimited default | Medium |
| U-006 | 2 | F3 README `--session-id` statement missing from Task 9 criterion | Low |
| U-007 | 3 | F5 hint text misdescribes the out-of-scope Coder caller | Low |
| U-008 | 3 | F6/F7 plan wording and task-order notes | Low |
| U-009 | 3 | F3 test code writing outside tmp_path | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|---|---|---|---|---|---|
| A-001 | The plan's overall design (question only with no task/name/resume; auto-name otherwise; 30 s timer; Ctrl+C = 130) is correct | all three | STATED (source.md, owner-approved plan) | none | not promoted |
| A-002 | An auto-named session is recorded in the saved-session list and reopened by name via the SessionStart hook | C-003 findings of all three | UNSTATED | determines whether auto-names pile up and whether collisions resume the wrong session | promoted |
| A-003 | Minor findings can be absorbed by the executor as notes without regenerating the plan (workflow rule: reflect never edits the plan) | all three rate nearly everything minor | UNSTATED | decides whether Task 5 wording defects and the missing fallback are fixed in implementation | promoted |
| A-004 | Every launch Orca makes has well-formed options (values after `--name`, `--session-id`, `--prefill`) | C-004, C-008, F11 | UNSTATED | argument classification in Task 3 | promoted |
| A-005 | A pty test can reproduce a multi-line paste and a Ctrl+C window deterministically | C-006 and Task 7 | UNSTATED | whether the safety-net tests prove anything | promoted |

## Summary
- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 3
- Total unique contributions: 9
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-006, X-001
- Taxonomy tags: L3 (state/guard/boundary/concurrency): C-003, C-006, X-001, X-002, A-002, A-005. L2 (structural): S-002, C-001, C-002, C-004, C-007, C-008, X-003, A-003, A-004. L1 (surface): S-001, C-005, C-009.
- total_diff_points (convergence denominator) = 2 + 9 + 3 + 4 = 18
