# Architecture analysis: installed hook coverage

## Scope and method
Command: `/sc:analyze src/superclaude/cli/eval/coverage.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/562/analyze`.

The narrow target is the hook coverage gate. Static inspection followed its two production callers (doctor and run), the declaration-based matcher mapping, integration-test assertions, and the installed skill's empty-HOME guidance. No source changes, Python execution, installation, or inference were performed.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:05:56Z; degraded: none. Access: mcp. Worktree: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup. Graph rows were used as leads, then checked against source; fixture-only callers were excluded from production claims.

## Findings and severity
- **Policy question, P3 advisory:** selected-suite coupling is present, not an inferred bug. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:1798-1829 applies eval-ID selection first and then calls the coverage gate with only those specs. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/coverage.py:321-335 requires each checked installed matcher to have a matching spec in that sequence. An unrelated suite can therefore be rejected before its workers start. The no-MCP capability-skip flag is processed later at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:1837-1842; it does not skip this gate.
- **Workflow evidence, not approval:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-cli-eval-protocol/refs/eval-contracts.md:54-62 documents the empty-HOME workaround. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/coverage.py:300-304 returns an empty passing coverage result if the settings file is missing; existing but unreadable, malformed JSON or non-mapping top-level settings return a parse error at :305-319 instead. The workaround removes installed matcher registrations from this check; it does not demonstrate those hooks are tested separately.
- **No implementation recommendation under the hold:** live issue #562 explicitly remains open and parked under the November 18 owner direction. No source defect that answers this policy choice is established by the review.

## Metrics and other domains
- Target: one Python policy module; production integration: two commands share it (doctor and run). No source edits or new abstractions were needed.
- The filter is bounded to the known MCP prefix families, not every hook entry: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/coverage.py:193-203. Coverage is calculated from declared expected tool calls, not observed runtime tool execution: :232-264.
- The rejection regression exists at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/eval/test_coverage_gate_integration.py:238-266. Its source asserts failure and the missing pattern; tests were not executed, so no test-pass claim is made.
- Security, performance and full quality audits were not requested. No runtime timings or installed-hook coverage percentages were measured. The issue's historical 16-of-17 rejection count was not recomputed.

## Recommendations
Keep the existing gate unchanged and the issue parked. When the owner resumes the eval harness, resolve the per-selected-suite policy and accepted isolated testing workflow before planning any behavior change; separately retain installed-hook coverage and corrupt-settings rejection. Neither the documented empty-HOME workaround nor the sibling diagnostic/directory defects establish that the coverage refusal is wrong.

## Limits
Read-only analysis of local checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` plus live issue and pull-request reads on 2026-11-24. No fetch, Python/UV execution, tests, eval runs, model calls, package installation, or GitHub mutation. Live project-board values, old retained runtime captures, full-install replay and empty-HOME execution remain UNVERIFIED. A PR-number search for 562 returned no matches; a broader coverage/eval search is not an exhaustive proof of absence. The project-local analyze command copy was absent; the installed copy passed the worker guard. One attempted report Edit was blocked because a newly written stub had not been explicitly Read; the stub was then Read and the same Edit succeeded, with no bypass.
