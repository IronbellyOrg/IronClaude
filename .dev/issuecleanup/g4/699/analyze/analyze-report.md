# Issue 699 claim-worktree architecture analysis

## Scope and method
Ran `/sc:analyze src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/699/analyze` on 2026-11-24. Static scope: the worktree create/copy flow, its policy contract, hook boundary and existing tests. No source edits, installs, tests, agents launched into new worktrees, or GitHub writes.

## Findings and severity
- P2, still open: the create argument list has no agent flag (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:695-710`), deliberately separating creation, copying and launch. This conflicts with the unconditional create-with-agent instruction in `CLAUDE.md:310`; its temporary-checkout exceptions at line 314 do not include claims.
- Partly addressed, not a runtime fix: `src/superclaude/core/WORKER-CONTRACT.md:299` describes copy-first then worker-start and `tests/skills/test_worker_contract.py:431-432` pins the wording. PR 701 merged this clarification as `0a46644576a31f0f62b9629b0f095b213027cdf6`, explicitly leaving issue 699 open.
- The issue's hook uncertainty can now be narrowed by source: `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:60-61` explicitly excludes this script's subprocess; lines 345-349 inspect only the Bash tool command string, while `orca_worktree.py:145-154` invokes subprocess.run. This is a documented coverage limit, not proof of malicious bypass or live enforcement failure.
- Existing coverage already forbids agent flags (`tests/skills/test_issue_orca_worktree.py:283-298,864-886`) and tests closing the first plain tab after copying (lines 899-907,921-935). These are test definitions inspected, not passing tests observed in this run.

## Metrics and limitations
One target Python file; three Python files in its scripts directory. Graph found 18 local callees for cmd_worktree and one callback registration in build_parser; these are navigation leads, not proof that external callers are absent. No runtime metrics collected. Live one-agent count and end-to-end launch success are UNVERIFIED; the brief prohibits creating worktrees or running UV.

## Recommendations
Keep issue 699 open for a narrow documented-exception completion, matching the issue's recorded owner default: reconcile the unconditional policy text with the copy-before-launch exception and retain existing no-agent/copy-order tests. Check or add focused coverage for the full create-copy-one-launch sequence in a later authorized implementation. Do not add --agent to create alone: it would introduce a second launch path before the copy is ready. A future redesign must replace, not supplement, the later launch.

## Codegraph
Codegraph: index_state=fresh, checked_at=2026-11-24T13:53:34Z; degraded: none
Access: mcp. Worktree root: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup. Lookups used file layout, outline, callees, callers and impact; findings were confirmed against Read/Grep source.
