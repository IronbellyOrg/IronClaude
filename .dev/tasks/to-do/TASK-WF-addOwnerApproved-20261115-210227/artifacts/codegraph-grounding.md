# Codegraph grounding

## Run state

- index_state: fresh (codegraph_status: 0 added, 0 modified, 0 removed; 3464 files indexed)
- checked_at: 2026-11-15T21:02:38Z
- worktree_root: the repository root of this checkout (git rev-parse --show-toplevel)
- projectPath: the same path
- access: mcp (codegraph_search, codegraph_node, codegraph_callers, codegraph_callees, codegraph_impact listed)
- SUPERCLAUDE_CODEGRAPH_PRIMITIVES: unset; no codegraph init or index process running
- tokens: graph:truncated not needed; graph:empty recorded for module-alias callers (see Dependents)

## Resolved symbols

All in SW = .dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet (read in full or by range before citing).

- scaffold/ledgerv1.py: HEAD_LEDGER (line 96), _fenced (123), _heading_between (135), read_ledger (166), transcript_results (290), Corpora (338, find at 361), check_row (395), carries_cb3 (414), check_report (507), summarise (736).
- scaffold/fnd.py: re-exports flat, locate, _blocks_after, _HEAD_FINDINGS from src/superclaude/cli/review/findings.py (read only, not edited). `flat` = " ".join(s.split()); `locate` flattens the text the same way; `_blocks_after` matches the fence info string exactly (label == info).
- analysis/analyze.py: found_fraction (253), group_metrics (365), compliance (1035), ledger_headings (1010), render_report (1144), cmd_all (1257), cmd_compliance (1317), main (1335), COMPLIANCE_LIMIT (1032).
- sweep/cli.py: run_check (121) calls ledgerv1.check_report and ledgerv1.summarise; not in the touch list, so its calls must keep working unchanged.

## Dependents

- read_ledger: codegraph_callers gives check_report, tests/test_ledgerv1.py::test_misplaced_duplicated_truncated_blocks (line 56), ::test_reader_counts_format_errors_dup_unknown_and_verdicts (line 420). resolution: def-line; call sites read in the test file.
- check_report: codegraph_callers gives tests/test_ledgerv1.py helpers run (38) and run_c (495); graph:empty for sweep/cli.py (module-alias call `ledgerv1.check_report(`, found by Grep at sweep/cli.py:141, then read).
- summarise: graph:empty; Grep finds sweep/cli.py:152 only.
- HEAD_LEDGER and _heading_between and _fenced: Grep finds uses only inside scaffold/ledgerv1.py (lines 194, 200, 203).
- Corpora and check_row: Grep finds scaffold/ledgerv1.py:535 and tests/test_ledgerv1.py:327, 361-377.
- compliance(): Grep finds analysis/analyze.py cmd_compliance (1317), tests/test_report.py::test_compliance_go_no_go (301-323, fixture make_compliance has no strict or lenient blocks), tests/test_run_schedule.py::test_spike_compliance_go_and_no_go (556, runs bin/run-spike.sh).
- render_report(): Grep finds analysis/analyze.py cmd_all (1293) and five positional calls in tests/test_report.py (59, 72, 112, 132, 184).
- normalised_verdict: tests/test_ledgerv1.py:435, tests/test_check_flow.py:23 and :102, scaffold/ledgerv1.py (reader, summarise).
- check.json field subset: tests/test_check_flow.py FIELDS_9_4 is a subset check (`<=`), so new keys do not break it.
- tests/test_ledgerv1.py:77-80 pins `reason == "heading_between"` for a heading placed between the ledger block and the findings heading: this is exactly the layout the owner order now forgives, so that assertion changes (strict keeps the old reason).

## Pre-check

Read-only check of the 8 tasks against the code (no new readiness check; index still fresh at the start of the run).

- Files named by tasks that exist: all of SW/scaffold/ledgerv1.py, SW/analysis/analyze.py, SW/sweep/cli.py, SW/bin/run-panel.sh, SW/bin/run-spike.sh, SW/tests/test_ledgerv1.py, test_check_flow.py, test_report.py, test_analyze.py, test_run_schedule.py, SW/tests/fakes/claude, SW/fixtures/runs/make_runs.py, SW/fixtures/plans/p_basic.md, SW/fixtures/reports/{good,bad_json_line,verdict_lowercase,unknown_item,ledger_missing,blocking_no_cb3}.md. Files the plan creates (not yet existing, by design): SW/tests/test_ledger_forgiveness.py, SW/tests/test_forgiveness_report.py, the eight forgive_*.md fixtures, ./artifacts/frozen-before.sha256.
- Symbols that resolve: read_ledger, _fenced, _heading_between, HEAD_LEDGER, Corpora, check_row, check_report, summarise, carries_cb3, scope_from (ledgerv1.py); compliance, render_report, cmd_all, cmd_compliance, found_fraction, COMPLIANCE_LIMIT (analyze.py); make_run and check helpers (test_check_flow.py).
- Dependents named by tasks and confirmed real: sweep/cli.py run_check (lines 141, 152), tests/test_ledgerv1.py (lines 38, 56, 77-80, 327, 361-377, 420, 495), tests/test_check_flow.py (lines 22-23, 66-70, 92-102), tests/test_report.py (59-184 render_report calls, 263-323 compliance), tests/test_run_schedule.py (556-597).
- Dependents of the touched symbols that no task names: tests/test_run_panel_fake.py (runs S5 through the fake claude and reads check output; covered by the full-suite run in Task 8) and analysis/analyze.py `ledger_headings` (counts `## Ledger` in Z0 and K reports, deliberately unchanged). No other caller found by Grep.
- LEDGER_FORGIVENESS reaches `sweep/cli.py check` through the environment the way CHECK_SCOPE does (bin/run-panel.sh line 14, sw_py in bin/common.sh); task 8 states this.
- Tokens: graph:empty (module-alias calls to ledgerv1.check_report and ledgerv1.summarise were found by Grep, not by codegraph_callers).
