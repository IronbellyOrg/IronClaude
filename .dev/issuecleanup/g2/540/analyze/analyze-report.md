# Swarm completion architecture analysis

Template: Analysis template in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/362/report-template.md.

## Scope and grounding
Command: `/sc:analyze src/superclaude/cli/swarm --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/540/analyze`.

This is the narrowest package containing execution, resume, completion policy and marker writing. Static review only; no source changes. Checkout HEAD and cached origin/master both equal `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`; no fetch was performed. Live PR #756 also reports that base commit, but that is not proof of the current remote master tip.

Codegraph: index_state=fresh, checked_at=2026-11-24T02:45:22Z; degraded: graph:truncated

Access: mcp. The run-command callee lookup returned 10 of 31 edges; direct source and full-package text searches covered the completion path instead. Graph rows were leads, not citation evidence.

## Architecture and metrics
The package contains 36 indexed Python files. The normal path dispatches workers, normalizes results, writes a result contract, and marks the state terminal. The reducer returns its contract without emitting a marker (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/reduce.py:677-704).

The completion policy defaults to writing a marker, but its setting is only declared, schema-validated and generated into specs; the execution paths do not consult it. Production-wide search finds one actual call to the shared marker writer, in reflect's ensemble runner, not the swarm command. The kill command has a separate atomic writer for the special killed status (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:3641-3678). No throughput or runtime metrics were measured.

## Severity-rated findings
1. **High, missing executor wiring.** Foreground execution reduces and marks terminal but never writes the promised marker (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2147-2183). The completion setting defaults true (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/models.py:562-573). A marker-only poll can therefore remain waiting; no live consumer hang was reproduced.
2. **Medium, regression expectation encodes the defect.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_e2e_user_guide.py:117-138 asserts that a successful run produces no marker. Updating this expectation is required for the issue's acceptance check, not optional cleanup.
3. **Medium, adjacent completion routes need coverage.** Static inspection shows resume also reduces and marks terminal without invoking the writer, and detached launch invokes the same run command in a child process. These are static findings, not runtime reproductions. Kill completion is distinct and already has its own writer. Existing shared writer uses the atomic helper (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/reduce.py:431-440); introducing a new format or general framework is unnecessary.

## Recommendations and roadmap
Keep #540 open. Reuse the existing atomic marker writer at the executor completion boundary after the contract and terminal-state writes; honor the completion setting and pass the actual contract status/path. Cover both foreground and resume, verify detached delivery separately, preserve kill semantics, and replace the CLI test that asserts absence. Check enabled/disabled policy, terminal status variants and stale markers rather than adding a new general completion framework.

Priority: P1. Complexity: medium. Size: S. No implementation or GitHub action is authorized by this analysis. Related open draft PR #756 touches the resume area and should be coordinated, not credited as a fix without examining and testing that behavior.

## Verification limits
No runtime analysis, tests, detached session, live model call, fix, stage or commit was performed. Foreground omission is source-confirmed; the issue's historical stub reproduction was not repeated. Resume and detached conclusions are static flow tracing only. No actual marker-polling consumer hang is established.

Issue body and all four comments, current assignee/labels, PR searches, and PR #739/#756 metadata were read using only authorized GitHub read commands. Full GitHub timeline events and the current remote master tip are UNVERIFIED under this worker's access limits. The truncated graph callee lookup was supplemented with native text search and source reads. A reducer read beyond EOF was recovered with a bounded read of the actual tail.

Independent review result is recorded in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/540/analyze/qa-review.md.
