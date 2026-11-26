# Observer architecture analysis

## Scope
Command: `/sc:analyze src/superclaude/cli/observe/ --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/706/analyze`.

Static architecture review of the observer package, with adjacent tests and guides checked for issue #706. No source, configuration or GitHub changes. No runtime, test, installation or environment-creation commands. Paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`.

## Findings
1. **Medium, source alignment is not implemented.** The observer still has its own adapter and collection pipeline: worker-list and question templates in `src/superclaude/cli/observe/adapter.py:29-32`, and source read, parse and merge in `src/superclaude/cli/observe/collector.py:274-319`. These are not sweep report inputs or shared sweep classification. Item 1 needs an agreed source contract or explicit documented differences, not another parallel collector.
2. **Medium, session explanation fields are not modeled.** `src/superclaude/cli/observe/parse.py:110-157` carries identity, lifecycle, source-reported stage and liveness fields, but no task explanation, done/remaining summary, issue/PR URL or named workflow history. Existing raw stage fields are not the requested named-step display. Adding rendering alone cannot satisfy items 2-4.
3. **Medium, the issue overstates missing scale coverage.** `tests/observe/test_render.py:99-118` already covers 5/8/10 Runs by 50/80/100 rows at three widths: 27 parameter combinations. This is static rendering/count coverage, not proof of 27 live fleet deployments. The full stressed cross-scenario acceptance remains UNVERIFIED; do not recreate the existing size matrix.
4. **Navigation is not implemented, and the read-only boundary matters.** Keys currently select local views, filter, mark, export or quit (`src/superclaude/cli/observe/view.py:1246-1300`); the adapter admits only fixed read templates (`src/superclaude/cli/observe/adapter.py:135-170`). Do not silently add a session-opening command outside that boundary. Issue #727 now records a later two-way direction; it requires architecture/evaluation first and is not an implemented extension of this adapter.
5. **Three narrow guide corrections remain.** Issue #706's November 22 comment adds the report-only parallel-experiment worktree exception, fixture-only FROZEN disclosure and timestamp-collision disclosure. Sources and exact edits are recorded in the companion findings file; none requires completing a new collector first.

## Metrics and limits
Discovery found 14 indexed Python files including the fixture package initializer. The existing render matrix has 27 size/width combinations; separate collector fixtures cover uneven ownership, shared/unmapped worktrees, history, missing fields and duplicate/out-of-order data (`tests/observe/test_collector.py:381-417`). No complexity score, performance measurement, test pass count or live scale result was measured in this run.

Negative evidence: a package-wide search for sweep, GitHub/link, summary and session-opening terms found panel-summary formatting but no shared sweep reader or session-navigation implementation. The Row model and key handler were read to distinguish absence from a search miss. One adjacent sweep search failed with `EACCES: permission denied, posix_spawn 'rg'`; dedicated Glob/Read recovery was used rather than treating that error as absence. GitHub event-timeline completeness and unlisted/unmerged external work are UNVERIFIED.

## Recommendations
Keep #706 open. Reconcile its remaining source and navigation decisions with #727's preliminary architecture/evaluation direction before feature implementation; use the existing observer pipeline and test cases rather than assuming the dashboard is absent. Correct the three guide statements and map cross-scenario coverage before adding tests. Remote fleet stays in #604; no source or GitHub action is authorized by this review.

## Codegraph
Codegraph: index_state=fresh, checked_at=2026-11-24T13:56:24Z; degraded: graph:truncated

Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. Readiness: 0 added, 0 modified, 0 removed; no active init/index process found. Used scoped files, adapter/collector/view outlines, collector callees, build_view callers and Row impact, then native source Reads. build_view callers showed 10 of 90 and therefore are not an exhaustive dependency list; no no-caller claim is made. A graph callee named monotonic resolved into unrelated watcher code, so it was not used as evidence. Local records written by this review do not make graph-derived facts about those records authoritative.
