# Issue 767 findings: Coordinator is compacting conversation too often

Issue: https://github.com/IronbellyOrg/IronClaude/issues/767 (open, no labels, no comments, no linked PR, filed 2026-11-24T17:22:39Z). Analyze run: `.dev/issuecleanup/g7/767/analyze/analyze-report.md` (architecture, quick, `src/superclaude/cli/sweep`).

## Verdict

still-relevant. Nothing in the repo addresses it: no PR references 767 (`closedByPullRequestsReferences` empty) and the last commits touching the sweep code are b46ecc1bd (#579, class fix) and 4d3c0b126 (#539, Phase 1), both before the issue.

Evidence checked in the current checkout (branch ironbelly/Issuecleanup, HEAD a7ae3dd30):
- Full-read rule is still in force: `src/superclaude/skills/sc-sweep-protocol/SKILL.md:25` says to Read the report in chunks of at most 150 lines until `Report complete`; the terminator is emitted at `src/superclaude/cli/sweep/report.py:542`.
- Per-wake trigger is still in force: `src/superclaude/core/WORKER-CONTRACT.md:290` (WC-16) runs `/sc:sweep` and reads its report on every coordinator wake or wait timeout, at most once every 5 minutes. (The issue cites `~/.claude/WORKER-CONTRACT.md:288-290`, the installed copy; the source copy has the same paragraph at line 290.)
- Duplicated rendering is real: unknown rows are emitted in `_could_not_determine` (`report.py:327-350`) and non-idle rows, which include unknown ones, again in `_sessions` (`report.py:405-445`).
- No size control exists: `commands.py:220-238` defines only `--run`, `--window`, `--root`, `--output`; `render` (`report.py:608`) writes every section. `tests/sweep/` has no output-size test (only the show-cap bound line, `tests/sweep/test_report.py:1027`).
- Related causes of the 816 unknown rows are tracked separately in open issue 766 (contract-path regex, transcript-tail rule, 50-show cap); fixing 766 would shrink the report but does not add a budget or remove the full-read rule.

Not verified (UNVERIFIED): the 16 compaction records, the five durations and the report sizes (710 KB to 714 KB) come from the reporter's private session files, which I cannot read. The root cause of compaction (the issue itself calls its hypothesis unproven) and Claude Code's compaction threshold are UNVERIFIED. Issue 574 and 575 both read as closed (574 stateReason COMPLETED); 575 stateReason not read.

## Complexity and size

Complexity medium, size M: the code change is small (a summary or delta output mode in `report.py`/`commands.py`, one changed skill step), but the full-read rule is a safety-relevant policy in two documents plus the installed mirror, and the issue demands a synthetic 800-row regression test and a before/after measurement.

## Priority

P2: it costs the coordinator roughly 22 minutes per five compactions (reporter's numbers, UNVERIFIED), but asserts no crash, data loss or stall, and blocks no other issue.

## Concrete next steps

1. Measure first: reproduce on synthetic data (about 800 unmatched sessions, a few scoped workers) and record report bytes, lines and the Read chunk count as the baseline (issue "Done when" item 4).
2. Decide the design (owner decision): either a summary or scoped output mode (counts, scoped-worker rows, changes since the previous report, with the full report kept on disk) or only removing the duplicate unknown-row rendering in `_sessions`.
3. Change the governing rule explicitly: edit `SKILL.md:25` and WC-16 in `src/superclaude/core/WORKER-CONTRACT.md:290` so the bounded read is stated, keeping FIFO processing, persistence before ack, evidence-based settlement and honest unknown coverage. Edit `src/superclaude/` only, then `make sync-dev` (and the plugin mirror and HOW-WE-WORK-style copies if tests require).
4. Add the regression test in `tests/sweep/` with a documented size budget, also checking that scoped-worker changes remain visible and the full file is still written.
5. Re-run the bounded scenario and report compaction count, durations and supervision correctness against the issue baseline.

## Dependencies

Needs: none hard. Soft: 766 (reduces the unknown-row volume; better done first or alongside, otherwise the baseline moves). Blocks: nothing found.

## Related issues

766 (open, Read workers show as Could not Determine), 574 and 575 (closed evaluations of compaction and tool-output pruning, not fixes), 339 (open, orchestrator, parent of the sweep work), 409 (open, TUI dashboard), 423 (open, orchestrator v2), 755 (open, coordinator Run rule; relevance UNVERIFIED).

## Related PRs

539 (merged, added `superclaude sweep` and `/sc:sweep`), 579 (merged, restored the working class), 708 (merged, user guides for observer and orchestrator mode; content UNVERIFIED). No open PR for this issue.
