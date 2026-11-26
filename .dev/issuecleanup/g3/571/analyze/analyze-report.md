# Issue 571 architecture analysis

## Scope and method
Ran `/sc:analyze src/superclaude --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/571/analyze` on 2026-11-24. This is the narrowest common source directory covering this release's command-line packages, installed commands, skills, agents and core guidance. This is a focused static check of issue 571's removals and upgrade path, not a new full-repository audit.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:17:48Z; degraded: graph:truncated

The grouped layout result was truncated. Targeted outlines, caller/callee and impact lookups plus direct Read/Grep/Glob supplied the relevant source evidence. No source changed.

## Current architecture
- The current package is 6.1.0, not a still-pending 6.0.0 release: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/pyproject.toml:7`.
- The six retired package directories (`prd`, `cleanup_audit`, `cli_portify`, `roadmap`, `tasklist`, `sprint`) and twelve retired command files are absent in targeted Glob searches. The issue's title is obsolete about swarm: it remains deliberately registered alongside reflect, eval, issue-watch, issue-pipeline, sweep, review and observe in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/main.py:557-596`.
- Upgrade retirement is no longer a missing feature. The generated manifest includes the 5.0.0 and 6.0.0 source tags, the twelve 6.0.0 command removals plus `tdd` from 6.1.0, and no retired agents: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_retired_data.py:3-31`.
- The codegraph caller and impact results connect the retirement entry point to both installer entry points and dedicated regression tests. Direct source checks of those call sites and protection branches are recorded below.

## Findings and recommendations
1. **Release implementation is present; do not repeat the removal work.** Both install and update invoke the retirement helper inside a non-fatal error boundary: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/main.py:271-283,425-437`. File classification checks the shipped hashes, and skill classification rejects changed, added, linked or unreadable content: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_retired_files.py:63-81,96-142`. This is evidence of those checks, not a blanket claim of race-free deletion or protection of every installer operation.
2. **Regression checks exist, but were not executed in this review.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/test_install_retired_files.py:300-361` covers an absent install, removal followed by a no-op second run, an edited command, and skill folders with added, changed or linked content. These tests support the implementation inventory, not a new runtime PASS.
3. **The remaining problem is closeout scope and evidence, not an absent architecture.** The live issue's final comments record the release and post-release work as done; its original completion list still requires deployment evidence and a new-repository issue. Resolve that difference explicitly before closing the whole umbrella. Do not revive the withdrawn swarm removal or repeat the separately shipped Part B cleanup.

## Evidence limits
Static source inspection only. No tests, builds, install, update, Python or UV commands were run; no real home, settings, remote branch or GitHub record was changed. Live GitHub reads used only issue view/list and PR view/list on IronbellyOrg/IronClaude. Historical test and install results are attributed to their issue/PR records, not reproduced.

The GitHub release publication and tag target were reported in issue 571, but direct release/tag API reads were outside the allowed command set. The Coder pin, other workspaces' rollout, snapshot fork contents, and completion of every proposal in the eight attached analyses are UNVERIFIED. The first semantic retrieval defaulted to a missing `main` branch; retrying explicitly against `master` succeeded.
