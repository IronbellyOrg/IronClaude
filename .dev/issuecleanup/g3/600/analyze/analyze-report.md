# Architecture analysis

## Scope and grounding

Command: `/sc:analyze src/superclaude/core/HOW-WE-WORK.md --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/600/analyze`.
Scope: the routing guide's Auggie review paragraph and routing row, checked against its plugin mirror, regression assertions, fixture and remediation reference. This is static document analysis, not an executed review or test run.
Codegraph: index_state=fresh, checked_at=2026-11-24T13:21:44Z; degraded: none
The graph lists only `__init__.py` under the core directory because Markdown is not indexed; document evidence therefore uses Read/Grep. No source modification was requested or made.

## Findings and metrics

- Issue 600's old route is absent from the current guide. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/HOW-WE-WORK.md:195` explicitly says accepted offers use design then workflow/implement at every depth; its routing row at line 342 says workflow at every depth. There is no remaining issue-600 route defect at these two sites.
- The implementation agrees: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:345-351` uses one chain for every depth and reserves execution for explicit user sign-off. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/auggie-review.md:128-135` describes the same phases.
- The guide mirror is byte-identical: `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exited 0. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/core/test_how_we_work_routing_table.py:799-806` now asserts the all-depth workflow wording, not the removed MDTM claim.
- A separate stale warning remains in the guide at line 195 and row 342: it calls the design-referral destination undeclared, but `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/design.md:23-26` now explicitly supports `--output <file>`, the option Phase A uses at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:346`. This is obsolete guide wording, not a present command defect. Correcting that warning and assertions that require it is a separately scoped documentation follow-up, not an issue-600 prerequisite.
- Checked two guide sites, one mirrored file, the regression assertions and the Auggie review fixture. Found zero issue-600-specific architectural defects requiring a new edit. No performance, security or runtime measurements were taken.

## Recommendations

Recommend closing issue 600 as already addressed, rather than repeating its retired-executor correction. The exact replacement paragraph was introduced by commit `a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6` (merged PR 656); PR 296 had already completed the primitive refactor, and PR 300 added its regression guard. The optional offer-suppression advice does not imply a different deep executor. Separately record the stale design-output warning and its pinning assertions for documentation cleanup, without a source edit or new issue in this run; do not present that warning as a real unsupported handoff.

## Limits

No tests, make targets, installations, Git staging, commits or GitHub writes were run. Test execution and whole-project synchronization are UNVERIFIED in this run; comparing the two guide files does not establish that `make verify-sync` passes. Historical PR test results are reports by their authors, not a fresh test result.
A first PR search for 600 returned unrelated numeric matches; title search and local history identified PRs 296, 300 and 656 instead. A first legacy-marker search used unsupported lookbehind and failed before searching; a retry using a supported boundary expression found no matches in the protocol directory. This search is not a test run.
