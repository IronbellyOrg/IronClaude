# Issue 665 architecture analysis

## Scope and grounding
Command: `/sc:analyze src/superclaude --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/665/analyze`.

The target is the narrowest common source ancestor of issue-watch, worker-contract core and the former report/orchestrator skills named by issue 665. Inspection within it covers only that issue's architecture, not unrelated package features. The current watcher design, relevant test source and source-change history were also read.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:38:48Z; degraded: graph:truncated

The layout output and the 8-of-27 `_launch` callees were truncated. Graph rows were leads, confirmed through source Reads and Globs. Augment's default-branch query failed (`main` does not exist); the `master` retry succeeded but returned older planning material, not proof of current behavior.

## Severity-rated findings
1. **High, planning correctness:** issue 665 describes follow-up work on a retired architecture. Local rollback commit `471f10511c8e2e8176c0e2088720ece03beca317` (PR 700) deletes the orchestrator design and report skill and restores issue-pipeline. Glob found no former report scripts. Parent issue 655's live closing comment (2026-11-23) says not planned, chooses PR 707 instead and points to issues 716-718. Building the old checklist unchanged would revive a rejected design.
2. **Medium, architectural mismatch:** the current watcher checks human approval and Project state, constructs a fixed claim command and saves pending state before launching. Sources: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/cycle.py:1007-1028,1143-1151,1183-1193` and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch/launch.py:112-156`. This is not PR 686's wake-file registry pipeline; that PR is closed without a merge.
3. **Medium, safety qualification:** PR 684's report server was removed from this checkout by PR 700. That does not establish that an installed copy or the separate PrivateRepoA copy stopped serving files; runtime exposure is UNVERIFIED. The recorded release blocker already has OPEN security successor 719, whose observed acceptance checks gate restoration under OPEN but parked issue 720. The owner's 2026-11-22 comment on 718 holds D1/D2 and says D3/D4 are not pursued; 720 waits for an owner daily-page request or the impending report-entry-writer stage. Neither those open issues nor the rollback prove a fix.
4. **Informational, retained protections:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:59,67` keeps the plan-approval handshake and no-recipient-override rule. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/issue_pipeline/test_brief.py:21-55,63-65` checks the retained stage briefs. Test source was inspected, not executed.

## Metrics and boundaries
One quick architecture pass, four scoped findings, zero source changes and zero test/runtime executions. Codegraph impact for `run_cycle` returned 18 symbols, including production CLI/first-run callers and tests; this is a dependency lead, not complete coverage. Primary issue 665 and its four comments were read, as were descriptions, metadata and returned discussion/review data for PRs 681, 684 and 686. Inline review threads were not separately retrieved; the issue's quotations are the follow-up record used here. The 21 historic defects were not individually reproduced on archived branches.

A shared GitHub rate-limit notice appeared after the lookup wave, although the requested issue results returned. No disallowed `gh api`, retry loop, install, `uv`, environment creation, staging or commit was run. Live deployments, archive contents and PrivateRepoA are UNVERIFIED. The first report Edit attempts were blocked because the newly written stubs had not received a tracked Read; after reading both stubs, edits proceeded through Edit.

## Recommendations
Recommend **not-planned** for issue 665 as scoped to the abandoned issue-655 build, not a claim that all findings were fixed. Before closing, the coordinator should preserve the review record and map surviving findings to the adopted work. The known server finding maps to existing security issue 719, which gates the parked restoration in 720; do not duplicate it or revive the report now. Respect 718's owner disposition: D1/D2 held, D3/D4 not pursued. Other matching work may belong in 716-718, but complete migration remains UNVERIFIED. No GitHub change or restoration is authorized for this worker.
