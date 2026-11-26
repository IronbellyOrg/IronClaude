# Sweep architecture analysis for issue 590

## Scope and method
Command: `/sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/590/analyze`.

Static architecture review of the six Python files in the sweep package, with focused reads of the collector, classifier, CLI entry point and regression tests. Live GitHub issue 590, parent issue 534 and PRs 539/579 were read. The historical report was sampled, not exhaustively counted. No source changes, test execution, live sweep or GitHub mutations were performed.

## Severity-rated findings
1. **P2, incomplete collection at scale.** The list collector makes one worker-list call per Run, notices a full page or `hasMore`, and marks truncation without following a cursor: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/sweep/probes.py:1143-1161`. Its fixed permitted-command forms contain no cursor variant (`:49-60`). The separate 50-detail-read ceiling remains in the budget. Raising that ceiling alone cannot retrieve workers beyond the first list page.
2. **P2, settled status is not separately presented when the result is unread.** The finished classifier requires a settled result contract except for a guard refusal. Its fallback explains the missing contract but still groups the row as unknown. This is a visibility limitation, not proof that the worker is unsafe or dead. The existing test explicitly expects UNKNOWN for a succeeded worker with no contract: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/sweep/test_classify.py:645-654`.
3. **Existing tests pin the limits, not the requested new behavior.** The 60-worker test explicitly expects 50 detail reads and 10 skipped rows: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/sweep/test_probes_allowlist.py:1137-1152`. A replacement must cover both detail-read coverage and list continuation, not merely change the cap constant.

## Architecture and quality metrics
Six Python source files separate command handling, observation models, bounded probes, classification and report rendering. The graph located the CLI and two test-helper callers of collection; source inspection confirmed the CLI constructs the default budget, collects, classifies, then renders and writes the report. The graph's budget impact includes collector helpers and multiple test modules, so changing budget semantics needs matching test updates. Graph counts are navigation evidence, not coverage or correctness measurements.

Historical evidence sampled from `/home/coder/workspaces/IronClaude/.dev/sweeps/20261117-065633-sweep.md`: header at lines 1-9; classification examples at 183-197 and 270-280. The report contains live/in-progress evidence forced into fallback with transcript-start uncertainty, so its zero-working total does not establish that no worker was live. This review does not infer that fixing just the two issue causes will classify every remaining transcript.

Negative evidence: whole-file Grep counts were tried for missing-detail, unread-contract and transcript fallback rows. They include repeated report tables and are not distinct-session counts, so none is used as a measured cause split. Full cause attribution remains UNVERIFIED. The issue's quoted counts remain historical reports, not a reproduced runtime result.

## Security and performance boundaries
The implementation has separate total/per-call time limits and detail-read caps. List continuation and a larger detail-read allowance must preserve bounded work, honest skipped-row coverage and the fixed permitted-command check. The probe already reads candidate contracts named by worker text under its allowed worktree roots; improving discovery is not the same as adding a nonexistent reader. Unknown result evidence must not become authority to close sessions or remove worktrees. No blanket security certification is made by this quick architecture pass. Parent issue 534's accepted buffering and outage-summary limitations are out of scope.

## Recommendations
Keep issue 590 open as still-relevant, medium complexity, size M, priority P2. First measure distinct-session causes in the saved report and have the coordinator reconcile parent issue 534's two owner records about paging versus measuring before choosing. If paging is confirmed, handle first-page continuation, the separate detail cap, fixed command validation, coverage and budget together. Separately resolve settled/asleep wording or bounded contract discovery. Update regression expectations, then obtain a read-only before/after live comparison without changing the five-minute cadence. No implementation is authorized by this report.

## Codegraph
Codegraph: index_state=fresh, checked_at=2026-11-24T13:18:56Z; degraded: none.
Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. Readiness checked once; no index mutation performed. Used grouped package layout, main-file outlines, collection callers/callees and budget impact. Cited findings were confirmed with direct source reads.
