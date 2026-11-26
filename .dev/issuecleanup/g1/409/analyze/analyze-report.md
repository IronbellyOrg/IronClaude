# Observer dashboard architecture analysis

Template: `.dev/issuecleanup/g1/362/report-template.md` (Analysis template), implementing the loaded `/sc:analyze` report requirements.

## Scope and grounding
Command: `/sc:analyze src/superclaude/cli/observe --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/409/analyze`.

Target: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/`, the smallest package covering the shipped observer. Source and test inspection only; no production source changes and no live observer reads.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:08:14Z; degraded: graph:truncated.

Grounding used the package layout, command/adapter/collector/view outlines, `assert_allowed` body and impact, and `run_once` callees. The `build_view` caller query returned 5 of 90 rows, so it is a truncated lead, not evidence of complete caller coverage. Source excerpts were checked directly. Augment initially failed because its default branch was main; retrying on master succeeded.

## Architecture and metrics
- Structure: 14 Python files in the package, including the fixture initializer; 26 test modules matching `tests/observe/test_*.py` were found. These are inventory counts, not test-pass counts.
- Entry/source selection: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/commands.py:164-196` selects only the synthetic fixture source or the live Orca source and refuses questions without a valid named Run. It does not read the sweep output.
- Collection: adapter -> parsed snapshot -> collector -> pure view -> renderer/export. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/collector.py:28-34` sets a 15-second interval and budget, a 60-second backoff ceiling, and four worker-list calls when the additional question read is enabled. This is configured boundedness, not a measured timing guarantee.
- Question linkage: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/view.py:888-948` joins the selected question's dispatch ID to one collected worker, shows that worker's worktree as evidence only, and otherwise says the scope is unknown. It does not infer all sessions in the worktree are affected.
- Navigation: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/view.py:1246-1300` contains selection, filtering, history, marking, exporting, inspector and quit handling; Enter opens the observer inspector, not an Orca session.
- The existing record regression at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/observe/test_export.py:312-326` asserts that distinctive question payload text is absent from exports. Its presence was inspected; it was not executed in this static pass.

## Severity-rated findings
1. **Medium, incomplete feature scope:** the live adapter admits only its three exact read templates, not a sweep source or GitHub reader (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/adapter.py:135-189`). The worker model has raw task/Run/stage fields but no session-summary, issue/PR-link or named-step model (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/parse.py:109-157`). The outstanding parent criteria need an explicit source contract rather than another renderer patch. This is existing unfinished scope, not a newly discovered runtime defect.
2. **Medium, tracking inaccuracy:** #706 says scale combinations have no tests, but `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/observe/test_render.py:99-118` already tests all 27 size/width combinations. The tests are synthetic rendering checks, not a performance benchmark or a verified orchestrator/session mapping. Correct the backlog description before authoring new scale work; retain any missing scenario-matrix and live-load coverage.
3. **Note, stale parent narrative:** #409's no-code/direction-not-chosen paragraphs predate the enabled guards and merged releases. The current guards at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/commands.py:67-70` contradict that narrative. Its November 20 comment, not the earlier table, records the current closure dependency on #706.

No critical architecture defect was established by this quick static pass. It is not a runtime, security-completeness or live-traffic certification.

## Recommendations and roadmap
Keep the parent open for #706, but size the remaining work from current code, not the stale no-code paragraphs. First obtain the existing owner decisions about source and scope; then add only the approved fields and navigation/disclosure through a confirmed source contract. Reuse the current parser, pure view and read-only adapter boundary.

Audit missing scenario combinations against the existing 27 rendering cases instead of creating the same matrix again. Preserve unknown/partial labels and the screen-only question-payload rule. Remote expansion remains separate in #604 and must not be slipped into the local observer work. The coordinator, not this worker, owns any GitHub corrections.

## Verification limits
- Static quick analysis only: no test execution, benchmark, visual gate, live observer run, remote join or current real-traffic completeness measurement. All such runtime outcomes are UNVERIFIED in this run.
- Current GitHub issue bodies/comments and directly related PR metadata were read using only the authorized issue/pr view/list verbs. Full timeline event enumeration is UNVERIFIED: the installed issue-view JSON field list has no timeline field, and the brief forbids the API route that would enumerate it.
- Negative searches covered the observer Python modules and the observer tests for sweep/GitHub sources, per-session summary/link fields and session-open handling; the concrete model/source/key-handler inspection grounds the absence conclusions. Ordinary `stage_*` values and question payload text are not treated as the requested named workflow or per-session summary.
- Findings concern the implementation gaps and stale tracking statements. No source fix is proposed as completed. No source files, git index, commits, issues or PRs were changed.
- Report editing initially hit the freshness hook because newly written stubs were not registered as Read; both stubs were then Read and edits succeeded through the normal Edit tool. This left no source changes.
