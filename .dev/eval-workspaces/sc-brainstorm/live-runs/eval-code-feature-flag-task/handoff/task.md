# Task Handoff — Add Feature Flag Management to the CLI

## Objective

Implement a small, audit-safe feature flag management layer for the SuperClaude CLI based on the merged brainstorm requirements.

## Source Requirements

- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/eval-code-feature-flag-task/merged-requirements.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/eval-code-feature-flag-task/seed-brief.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/eval-code-feature-flag-task/adversarial/debate-transcript.md`

## Implementation Tasks

1. Add a central source-backed feature flag registry with boolean-only v1 values, stable keys, descriptions, owners, defaults, lifecycle status, and expiry/review metadata.
2. Add a small evaluator/resolver boundary that returns effective values and reports the winning source.
3. Add CLI commands to list flags, show details, enable/disable/unset overrides, and validate registry/override state.
4. Decide and implement supported local override storage without writing to generated `.claude/` mirrors.
5. Add validation that fails on duplicate keys, unknown override keys, malformed override files, invalid values, and expired active flags.
6. Add tests for defaults, override precedence, unknown keys, malformed overrides, expired flags, and CLI command behavior.
7. Preserve existing CLI behavior unless a flag is explicitly overridden.

## Constraints

- Use `src/superclaude/` as the source of truth.
- Do not edit generated `.claude/` mirrors directly.
- Use UV for Python test commands.
- Keep v1 local-only: no remote flag service, network evaluation, or dynamic code loading.

## Open Decisions Before Implementation

1. Project override storage: tracked file, ignored local file, or both.
2. Environment overrides: defer for v1 or support as read-only visible inputs.
3. Lifecycle statuses and expiry grace policy.

## Suggested Validation

- `uv run pytest` for the relevant CLI and registry tests.
- Add focused tests for the new registry/evaluator module and CLI command group before running broader validation.
