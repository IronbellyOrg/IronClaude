# Issue 718 architecture analysis

## Scope
Architecture-only quick static review for issue #718 at checkout a7ae3dd30fcf88aaab655c37e94e58e121c2d863 on 2026-11-24. Target: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills, the narrowest existing source parent of the removed agent-work-report skill and retained closeout integration. Supporting checks covered CLI registration and the separate observer. No source changes, Python execution, tests, installs or GitHub writes.

## Findings
1. **Deferred capability, not completed delivery (P3).** The report skill and tests are absent: Glob for src/superclaude/skills/**/*work*report* and tests/**/*agent_work_report* returned no paths; Grep for agent-work-report across src returned no matches. PR #684 introduced the skill at d7d645dddd42e49a72a734f9c8b6952bcbcb4527; PR #700 removed it at 471f10511c8e2e8176c0e2088720ece03beca317. The November 22 owner comment on #718 parks D1/D2 and declines D3/D4, explicitly without closing the issue.
2. **The report-entry writer remains an integration boundary (P3 while parked).** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-closeout-protocol/refs/settle.md:99 records the absent writer. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh:1037-1039 escalates when its help probe fails rather than editing report files directly. Grep for report-entry in src/superclaude/cli returned no matches. This is a missing integration, not a newly observed runtime failure.
3. **The terminal observer is a separate surface.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/observe/commands.py:22-49 imports its live source, collector, export, render and view components; lines 63-70 enable question and question-link gates. Its existence does not implement #718's report-entry display and daily exclusion. #706 tracks observer links/navigation separately.
4. **Old design sequencing is not current authority.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/releases/backlog/issue-watcher-zero-setup/design-comparison-655.md:3 voids recommendations adopting the living report while retaining #718 as follow-up tracking. Do not restore the old report format or resurrect closed PR #686 on the strength of the original stage list. #719 is an open safety gate for a possible #720 restore; no active vulnerable server is claimed in this checkout.

## Metrics and limits
Two remaining held report requirements (D1 and D2), two requirements not pursued by owner decision (D3 and D4), zero source edits and zero runtime/test runs. Graph readiness was stale (one pending added file), so verification used Glob, Grep and Read. The local unification spec named by #718 is absent in this worktree; its stage-completion claims, archive implementation details, PrivateRepoA deployment and the full GitHub event timeline remain UNVERIFIED. Bounded PR searches are not proof of complete cross-reference coverage. Initial Edit attempts on the report stub were refused by the freshness hook; the required Read was performed before successful edits.

## Recommendations
Keep #718 open as still-relevant, on hold, at P3. Wait for #720's trigger and an owner-approved restore that meets #719; then reuse the coordinator report-entry writer from #716 for D2 instead of introducing a second entry format. Reconfirm scope against the merged design before implementing D1/D2. Do not pursue D3/D4 under this issue unless the owner changes their decision; no broader observer rewrite is requested.

## Grounding
Codegraph: index_state=stale, checked_at=2026-11-24T14:05:19Z; degraded: graph:stale
Access: mcp available, but no graph lookups used after the stale readiness result. Worktree root: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup. Analysis succeeded as a static report; no runtime success or live deployment is claimed.
