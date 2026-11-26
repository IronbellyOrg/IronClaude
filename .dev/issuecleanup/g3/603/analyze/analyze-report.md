# Architecture analysis: design command

## Scope and method

Command: `/sc:analyze src/superclaude/commands/design.md --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/603/analyze`.

The narrowest target is the design command definition, a Markdown instruction file, not a Python runtime. The related spec-panel command was inspected for the reusable loop. Codegraph readiness was checked once; its commands-directory lookup returned only `__init__.py`, so Markdown claims use direct Read/Grep. No source changes, tests, installs, paid model calls or GitHub writes were performed.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:24:38Z; degraded: none (Markdown is not indexed; source reads are authoritative).

## Findings and impact

1. **Medium, missing integration:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/design.md:30-34` still ends at Document, after the same session's Validate step. It has no independent review/revise/re-review phase. At `:123-125`, unattended success means the design was written and nested invocations are explicitly None. This leaves issue #603's requested final quality gate unimplemented.
2. **Existing grounding is not independent review:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/design.md:51-74` already checks real names, signatures and consumers. It reduces unsupported designs but is part of the producing session and does not fulfill the requested separate review loop.
3. **Reusable policy, not an automatic loop runner:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/commands/spec-panel.md:258-264` defines critique, blocking-only revision, changed-line re-review and a cap of two fixes/three reviews. Line 261 explicitly makes each invocation one review and assigns the loop's state to its caller. Adding only one spec-panel invocation would not satisfy the issue's fix/re-review requirement.

## Recommendations

Keep the issue open. Add a caller-owned review loop after Document, reusing critique and the existing blocking-only reviser rules rather than replacing the review engine. Carry baselines, prior findings and the review count through each review; propagate nested unattended contracts; preserve honest incomplete/escalated outcomes. Decide how a chat-only design is reviewed instead of silently treating an unreviewed design as reviewed. Keep any broader panel/schema redesign outside this issue unless separately approved.

## Metrics and limits

Inspected the 149-line design definition and the existing spec-panel review-loop section. This is a static, quick architecture assessment, not a runtime demonstration of an instruction-following command. Security and performance were not independently audited; no numeric quality score or runtime speed claim is inferred. Markdown has no indexed call graph, so graph caller/callee/impact queries do not apply to this target. The first test-name-filtered search (`tests/*design*`) returned no matches; broader shared contract tests must be checked separately. UNVERIFIED: runtime review behavior and current model/provider availability. A report Edit was initially refused by the freshness hook; a direct Read resolved it before the Edit was retried.
