<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Evaluate the value, implications and potential unlocks or rethinks of a sub-orchestrator or coordinator mode for the proposed `/sc:orchestrator` command.

## Problem Statement

Work within a worktree can call for aggressive parallel work in separate sessions and greater autonomy, while still requiring coordination and reporting to an orchestrator above.

## User Story

As an orchestrator, I want to evaluate a sub-orchestrator mode that can delegate work below and follow orders and report upward, so that parallel work in a worktree can have greater autonomy.

## Proposed Solution

Analyze the orchestration skill and the specifications and work for the new `/sc:orchestrator`. Evaluate a primitive potentially selected with `--sub`, including how its orchestrator behavior would vary to support delegation below and accountability above. Assess the implications for the existing worker fan-out restriction; do not presume an implementation decision.

## Acceptance Criteria

- [ ] Analyze the orchestration skill and identify relevant specifications and work for the proposed `/sc:orchestrator`, noting any that cannot be located.
- [ ] Evaluate the value, implications, potential unlocks and necessary rethinks of a sub-orchestrator or coordinator mode for parallel work in a worktree.
- [ ] Assess delegation to subordinate agents, reporting and following orders from above, and the implications of WC-13's worker fan-out restriction.
- [ ] Consider `--sub` as a possible interface without assuming that implementation has been approved.

## Out of Scope

Not known yet.

## Components Affected (from `/sc:analyze`)

- `~/.claude/skills/orchestration/SKILL.md`: installed discovery stub for Orca coordination; it directs readers to the version-matched guide supplied by Orca. The skill directory is a symlink to `~/.agents/skills/orchestration`.
- `src/superclaude/core/WORKER-CONTRACT.md` (WC-13): workers may not start or dispatch Orca workers or create tasks; a coordinator decides on further work. Allowing a worker to fan out would require reconsidering this restriction.
- No `/sc:orchestrator` command or matching skill was found in `src/superclaude/commands/`, `src/superclaude/skills/`, `~/.claude/commands/sc/`, or `~/.claude/skills/` during this quick pass. No specification explicitly naming `/sc:orchestrator` was found by text search in `docs/` and `.dev/` beyond this issue draft; relevant work may exist under another name.
- Codegraph and Auggie tools were unavailable in this session; the quick pass used Glob, Grep and Read instead. The full Orca-supplied orchestration guide was not inspected.

## Related Issues/PRs

Possible related issues, not confirmed duplicates: #339, #423, #431.

<!-- sc:issue:create template=issue-feature-simple -->
