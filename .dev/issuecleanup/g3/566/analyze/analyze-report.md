# Swarm resume architecture analysis

## Scope and method
Command: `/sc:analyze src/superclaude/cli/swarm --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/566/analyze`.

The swarm package is the narrowest shared source directory covering command orchestration, stored job data, preflight, normalization and reduction. Scope is issue #566's resume context, including the later partial-resume gaps recorded in its comments. Static inspection only; no source changes, test execution, provider calls or environment setup.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:09:17Z; degraded: graph:empty, graph:truncated.

The empty lookup was manifest.py, which does not exist in this package; the Manifest type lives in models.py. The initial reducer caller query showed 10 of 48 callers, so it is not used as exhaustive caller evidence. Source and tests are read directly for citations.

## Current architecture
The package contains 36 Python files in the graph inventory. The relevant flow is fresh preflight -> saved Manifest -> worker dispatch -> normalization -> reduction; resume rehydrates the saved job, discovers completed slots, dispatches only remaining slots and reduces the combined results.

Accepted contract context is already persisted before dispatch at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/preflight.py:1852-1878. Resume passes the restored lens, lens source, caller, caller metadata, target and next-command inputs into reduction at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2694-2708. Reduction emits these values rather than dropping them at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/reduce.py:672-698.

The fresh/completed-resume comparison exists at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_resume_context.py:89-119; its resume helper checks skipped=3 and redispatched=0 at lines 80-85. These tests were inspected, not executed in this review.

## Findings and recommendations
1. **Original completed-job loss is addressed in the checkout.** Resume supplies the saved contract context at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2634-2708. This matches merged PR #739, merge commit 3ecf3fee8d7cbf810098ad01807d9c7aa0af8627, rather than the issue's older account of a wholly local fix.
2. **High priority: partial legacy resume still freezes a rendered next command.** At /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2677-2682, a missing accepted template permits a prior rendered command to override even a usable snapshot template. New successful review files can then be absent from the recommendation. Prefer a recoverable saved template; reserve literal fallback for jobs without one.
3. **High priority: resumed provider inputs are still omitted.** Fresh dispatch supplies assembled prompt and worker settings at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:1929-1954; resumed dispatch omits both at lines 2585-2589. Rehydration builds a WorkerSpec using only count at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/preflight.py:2022-2039. Restore accepted nonsecret request/settings, and refuse unsafe or unrecoverable partial jobs before dispatch instead of silently substituting defaults.
4. **Medium priority: resumed normalization lacks accepted provenance arguments.** Fresh normalization supplies recipe arguments, target and checksum at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2105-2119; resume passes only the recipe at lines 2604-2610. Preserve the accepted normalization arguments when retrying failed workers.

These remaining items match the issue's November 20 follow-up scope and the open draft consolidation PR #756. Do not build a competing fix or assume older feature-branch merges delivered these changes to master. Review and validate the consolidation before any owner-authorized submission/merge decision.

## Verification limits
This quick architecture analysis does not execute tests, compile code, call a model or change source. Runtime reproduction on this checkout is UNVERIFIED. Inspected test assertions and GitHub-reported checks are not a locally observed passing run. Live-provider behavior, type checking, the old private probe captures and the full consolidated PR implementation are UNVERIFIED here.

Live GitHub reads found PR #739 merged to master and PR #756 open as a draft with six successful check entries and a reviewer summary reporting two suggestions on f00a199. Those checks do not resolve review suggestions or authorize marking the draft ready. Inline suggestion contents were not available in the allowed `gh pr view` JSON used here and remain UNVERIFIED.

No general security or performance audit is claimed. An Edit was initially blocked because this report had not been Read after its stub was created; the required Read was performed and the same Edit succeeded. No alternate write path was used.
