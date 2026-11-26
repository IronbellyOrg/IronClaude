# Research: Issue 322 worktree write boundary

- **Topic type:** Issue status review
- **Scope:** Read-only GitHub and source investigation; no implementation
- **Status:** Blocked final acceptance: findings populated, but the independent evidence gate produced no report and the complete GitHub event timeline remains UNVERIFIED.
- **Date:** 2026-11-23
- **Template:** /home/coder/.claude/templates/modularization-template-review/codebase-research_template.md; requested decision fields nested under Findings.

## Findings

### Verdict and evidence
**Verdict: still-relevant.** [CODE-VERIFIED] No fixed worktree write boundary appears in distributed PreToolUse registrations (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:84-135); the current workspace hook is an output-location rule, not a checkout-ownership check (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/reject-workspace-writes.sh:19-39).

GitHub-verified: [issue 322](https://github.com/IronbellyOrg/IronClaude/issues/322) is OPEN and requests design review, not immediate implementation. The owner comment on 2026-11-06 requests removal of stale Serena assumptions and an allowlist for some directories such as /tmp. The current proposal still has three Serena adapter rows, and the 2026-11-17 review says the amendments remain outstanding. Missing implementation alone is not the acceptance criterion for this design-only issue.

Reviewed checkout: a7ae3dd30fcf88aaab655c37e94e58e121c2d863. PR 329 (2f10a0e1e43bee841a4143235a92fc16171c9707) retired Serena; PRs 432, 449, 469 and 541 address other controls, not this boundary. PR 445 (59a43d68754aa9f89b7a138bc23bb12b88965d78) archives observations and explicitly adds no enforcement.

### Real current state
- [CODE-VERIFIED] CONFIGURED, not live-tested in this review: freshness and launch-level checks, agent-presence checks and job identity. None is registered as an immutable whole-session worktree boundary. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:84-135.
- [CODE-VERIFIED] NOT BUILT in the inspected source tree: the proposal's all-tool boundary registration and named boundary entry point. Glob under src and tests found no worktree-boundary-named files; Grep for worktree-write, write-boundary, fixed-scope and confinement found adjacent swarm output handling, not the proposed implementation. Existing workspace policy explicitly permits nonmatching paths: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/reject-workspace-writes.sh:19-39.
- [CODE-VERIFIED] PARTIAL PRIOR ART, not partial completion of issue 322: swarm confine_path checks a selected output directory and acknowledges a symlink-swap limit. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/state.py:65-119. The launch-level hook explicitly leaves ordinary sessions ungoverned: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:2-9.
- [CODE-VERIFIED] Historical evidence exists for adjacent process identity, not filesystem containment. The archived observation report states nothing is enforced and records Monitor/detached-child/supervisor-death gaps: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/done/TASK-WF-planTheRealBound-20261107-080351/artifacts/b-ctx-report.md:3-5,67-77. These are historical observations, not a fresh reproduction.
- [UNVERIFIED] No live isolation backend, immutable scope service, Git broker or all-tool denial/failure matrix was exercised. No stub or functioning implementation of the proposed complete boundary was established.

### Concrete next steps
Recommendations only; no approval, implementation or outward action is implied.

1. Refresh the design against the current hook inventory: remove Serena adapters and replace the obsolete description of four named Serena edit hooks. PR 329 is merged and the current registrations are in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:84-135.
2. Resolve the owner's requested directory allowlist. Distinguish per-session temporary/cache roots from trusted framework state and broad shared /tmp access; the existing freshness hook needs explicit state/log handling (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/freshness-pre-edit.sh:8-14).
3. Re-review the proposal's unresolved platform/backend and human-run-Git-versus-broker choices. Preserve the difference between a limited direct-edit guard and complete arbitrary-process confinement; do not treat launch-level text classification or swarm output checks as substitutes.
4. Once the refreshed design is accepted, create a separate implementation plan with real-tool tests for sibling checkout writes, link/race escapes, nested tools, background processes, protected framework state and fail-closed hook failures. Keep issue 322 as design work unless the owner explicitly expands it.

### Complexity and size
**Complexity: complex. Size: L.** Assessment for the remaining design revision and review, not authorization to build it: the requested policy crosses tool adapters, inherited processes, filesystem aliases, framework service state and shared Git metadata; a short destination matcher cannot settle that contract. Complete implementation would be a separately sized project.

### Priority
**Priority: P1.** Assessment: wrong-checkout writes can corrupt another session's work, so settling the isolation design matters to safe parallel-agent operation. This is not P0: no current production incident or active exploit was reproduced, and no verified issue dependency is blocked by it.

### Dependencies
GitHub-verified: issue 322 has zero formal blockedBy edges and zero blocking edges; closedByPullRequestsReferences is empty. No hard dependency on issue 339 is established. Architecture alignment with its worktree session coordinator is useful, but the 2026-11-17 comment presents parking behind it as an owner choice, not an existing prerequisite. Retirement of Serena is already delivered by PR 329, not an open dependency.

### Related issues
- [Issue 339](https://github.com/IronbellyOrg/IronClaude/issues/339), OPEN: worktree session orchestrator; adjacent ownership/coordination work, not a proven blocker.
- [Issue 394](https://github.com/IronbellyOrg/IronClaude/issues/394), CLOSED: enforcement of claim-launched agent levels, implemented by PR 432; not filesystem isolation.
- [Issue 323](https://github.com/IronbellyOrg/IronClaude/issues/323): Serena/codebase-memory retirement and codegraph migration, identified by merged PR 329. Current issue state UNVERIFIED because this review did not separately fetch it.
- Issues 441 and 442 are referenced in PR 469 as pre-push enforcement and live-observation follow-ups. Their current state and any dependency on issue 322 are UNVERIFIED; they are not asserted to block it.

### Related PRs
All PR states and commits below were read with gh pr view against IronbellyOrg/IronClaude; none closes the proposed write-boundary work.

| PR | Verified state and merge commit | Relationship |
|---|---|---|
| [329](https://github.com/IronbellyOrg/IronClaude/pull/329) | MERGED, 2f10a0e1e43bee841a4143235a92fc16171c9707 | Retired Serena; proves the design inventory needs refresh. |
| [432](https://github.com/IronbellyOrg/IronClaude/pull/432) | MERGED, 3b344dd4e0481a9063d4ac22abb24a9e589614a6 | Launch-level text guard, expressly not universal prevention. |
| [449](https://github.com/IronbellyOrg/IronClaude/pull/449) | MERGED, 24d79b7fa5215d5ad27545386f8cd8b1f63ca9a9 | Requires an agent flag on Orca worktree creation. |
| [469](https://github.com/IronbellyOrg/IronClaude/pull/469) | MERGED, 5f8a1ea2d506fa6a6b8fa5eb335a20140032c64d | Pre-push protection, not local write confinement. |
| [541](https://github.com/IronbellyOrg/IronClaude/pull/541) | MERGED, 0406ef5b01f2e79c88100d32f01df4ebf2395646 | Worktree-instruction test wording only. |
| [445](https://github.com/IronbellyOrg/IronClaude/pull/445) | MERGED, 59a43d68754aa9f89b7a138bc23bb12b88965d78 | Only PR returned by all-state PR search for 322; archives process-identity observations, no enforcement. |

## Gaps
- UNVERIFIED: complete GitHub event timeline, including historical edits/cross-reference events. The permitted gh issue view exposes body, both comments, state, last update, dependency edges and closure references but no timeline event field; no forbidden gh api or browser request was used to fill this gap.
- UNVERIFIED: newly pushed changes not present in checkout a7ae3dd30fcf88aaab655c37e94e58e121c2d863. No fetch/rebase was authorized or performed. Augment search used pushed master as corroboration, while cited files came from this checkout.
- UNVERIFIED: runtime enforcement, deployed client compatibility, link-race containment, OS backend and Git broker. No live containment experiment or full test suite was run during this static review.
- Search scope: complete hook inventory and PreToolUse registrations, project workspace guard, freshness/launch/Orca guard headers, installer integration, swarm path-checking prior art, source/test boundary-name searches, and master semantic search. No source/test filename matching the proposed worktree-boundary component was found. Negative searches support the scoped conclusion, not a claim that every conceivable enforcement mechanism everywhere is absent.
- Recovery notes: initial Augment call failed on default main, then succeeded on master; the unsupported gh field closedByPullRequests was corrected to advertised closedByPullRequestsReferences. Both initial report edits were blocked for missing tracked Read, then applied after the required Reads. No bypass or source edits were used.
- Validation: the runnable report-completeness check passed for all requested fields, no remaining placeholders, and the command contract/handoff. Its uv run invocation also created /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.venv, built the local editable package and installed 27 packages there. This was an unintended local environment side effect outside the report directory, not a source change or shared/global install; it was not deleted because cleanup was not authorized.

## Key Takeaways
Keep issue 322 open as **still-relevant**, refresh its design rather than equating adjacent guards with isolation, and obtain design acceptance before opening implementation work. No implementation, local commit, staging or GitHub mutation was performed. The required quick architecture analysis is /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/322/analyze/analyze-report.md.
