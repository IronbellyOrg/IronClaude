# Worker lock architecture analysis

Template: analysis structure from /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/362/report-template.md.

## Scope and grounding
Command: `/sc:analyze src/superclaude/core/WORKER-CONTRACT.md --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/446/analyze`.

Target is the single canonical worker-contract file, the narrowest source path covering issue #446. Supporting checks cover the existing contract tests, the routing guide and its plugin copy, and the supervised-orchestration technical reference. This is static analysis only, not an implementation.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:11:51Z; degraded: none

Access: mcp. Markdown is not indexed; the grouped core-directory query returned only its Python initializer. Markdown conclusions therefore use Read/Grep, not graph call edges.

## Architecture and metrics
The worker reads the installed contract and follows its procedural limits. The canonical WC-9 text at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:41-45 governs git writes and still specifies a blocked report on seeing the lock. This is a contract wording and regression-pin change, not a new service, scheduler, or lock manager.

Scope metrics: one normative lock sentence; zero `index.lock` occurrences in its contract-test file; one matching restatement in the technical reference. The routing guide and its plugin copy have no index-lock rule. Existing contract tests use phrase pins and negative mutation tests, suitable for the added schedule and safety requirements. Other worktree-cleanup lock references concern a separate cleanup safety boundary.

## Severity-rated findings
**Medium: the worker still blocks on a transient lock.** The normative sentence at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/core/WORKER-CONTRACT.md:45 contains neither retry nor lock age. This leaves the precise improvement requested by issue #446 unimplemented; a transient lock can cause a worker to stop instead of continuing once it disappears. Live collision frequency is UNVERIFIED.

**Medium: no dedicated contract regression pin for the new behavior.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_worker_contract.py:124 pins only the heading for WC-9. A whole-file search finds no `index.lock`. A passing existing suite would not demonstrate the requested retry behavior.

No security or performance defect is asserted from this limited static review. The important safety invariant for the eventual edit is preserving the lock and reporting a persistent lock, not removing it.

## Recommendations and roadmap
Keep issue #446 open. Make the already-defined 1+2+3+4 second retry a small contract-and-test change, preserve the prohibition on deleting/moving/editing a lock, report persistent lock path plus modification-time age, and align the technical-reference restatement. Use existing regression-pin conventions; do not add a new framework or extend waits to cover long hooks. Run the sync, lint and contract-test checks named by the issue during that implementation, not as evidence that the still-missing feature already works.

## Verification limits
No source edits, test runs, live lock experiments, sync commands, commits or GitHub writes were performed. Current Git/Orca lock timing and frequency remain UNVERIFIED; the earlier investigation was read as historical evidence. Codegraph cannot index this Markdown target, so no caller/impact result is claimed. This report assesses the issue's narrow contract gap, not every orchestration concern. The optional graph limitations did not prevent completing the static analysis.
