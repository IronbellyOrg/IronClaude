# Architecture analysis: codegraph first-index hook

## Scope and method

Command: `/sc:analyze src/superclaude/hooks/scripts/codegraph-session-start.sh --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/648/analyze`.

Read-only static analysis of the narrowest source responsible for automatic first indexing, plus its registration, user documentation and regression-test inventory. No benchmark, index build, test suite, environment change or source edit was performed.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:36:21Z; degraded: graph:empty

The graph returned no indexed entry for the shell script. Its directory layout returned only one JavaScript file, so shell analysis used direct Read/Grep. No claim of absent callers or tests is based on the empty graph result.

## Findings and metrics

1. **Resource-pressure exposure, Medium follow-up candidate, not an uncompleted measurement.** The startup registration is /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:23-29. The complete 32-line executable hook exits on the off switch (line 11), missing binary (lines 14-19), unsuitable repository (lines 21-22), or existing database (lines 24-25), then starts a detached init (line 31). It contains no workspace-wide lock, concurrency limit or available-memory check. Separate fresh checkouts can therefore each launch an init; source does not establish that doing so is safe on small workspaces.
2. **Documentation mismatch, Medium follow-up candidate.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/user-guide/codegraph.md:28 still says up to about 1 GB for first init. The November 23 results posted on issue #648 report individual IronClaude peaks of 3,744,572-4,172,508 KiB, so this stated memory bound does not describe that tested snapshot. Source commit differences and unreplicated measurements prevent a present-version performance claim.
3. **Measurement deliverable is already posted.** https://github.com/IronbellyOrg/IronClaude/issues/648#issuecomment-7105420783 contains both repositories' 1/3/5/10-build matrix, 38 per-build results, summed peaks, sampled minimum available memory, changing total memory, completion states and timing-based slowdown. https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-7105434345 links it back to the parent. No repair PR is necessary for an issue explicitly requiring no product-code changes.

Static metrics: one shell hook (32 executable/comment lines plus trailing blank), one startup registration, and 12 named regression tests found in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/test_codegraph_session_start_hook.py. The test module says it uses a stub, not real indexing; test execution was not performed.

## Recommendations and limits

Recommend treating #648 as complete measurement work, with owner/coordinator closure rather than a repeated benchmark or product fix. Record resource controls and the inaccurate documentation bound as separate follow-up candidates only; no new issue, source edit or outward action is authorized by this run.

UNVERIFIED: the benchmark's raw process logs, measuring script, nine regression-check results and claimed earlier independent QA were not supplied or rerun here. The report's source commits were PrivateProjectA <private-project-commit> and IronClaude 1a6c8723fe9e6caa85bfffcdb97b2dc434978bf9, not this checkout. Its sum of peaks is not simultaneous aggregate resident memory, and user-perceived slowness was explicitly not measured. This static review does not certify memory safety, repeatability or current performance.
