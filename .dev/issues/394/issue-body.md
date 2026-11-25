<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Add a hook that enforces the permitted launch level in sessions started by `/sc:issue --claim --pipeline`. It must prevent the agent and its subagents from crossing the allowed boundary without relying on prompt instructions alone.

## Problem Statement

The planned claim pipeline uses instructions in a launch prompt to stop agents at the appropriate boundary. An agent running with permission prompts off can ignore those instructions and perform implementation or submission actions that were not authorized.

## User Story

As a person claiming an issue, I want the launched agent's actions limited to the chosen level, so that work does not proceed or get submitted without authorization.

## Proposed Solution

Add a hook that reads launch state the agent cannot edit, identifies claim-launched sessions, and blocks disallowed actions across relevant tools and subagents. Account for human approval, nested subagents, state tampering, worktree renames, re-claims, shell wrappers around git, and hook speed.

The `/sc:issue --pipeline` feature is a separate, not-yet-implemented dependency being built in parallel. Its specification proposes `pipeline.json` as an input and permits moving it to a location the agent cannot edit.

## Acceptance Criteria

- [ ] In claim-launched sessions, the default `worktree` level stops at an approved plan and blocks `/sc:implement` and `/task` until a human approves; it also blocks `git commit`, `git push`, and `/sc:pr-submit` unless submission is allowed.
- [ ] The `full` level allows implementation but blocks commit, push, and `/sc:pr-submit` without `--submit`; `full --submit` allows those submission actions subject to the restrictions below.
- [ ] A human can approve implementation by typing the command or replying `approved`, and the hook distinguishes human commands from agent-issued commands.
- [ ] The hook applies only to claim-launched sessions, leaving ordinary sessions unchanged; it covers Bash, Skill and Task tool calls and nested subagents.
- [ ] The hook reads the level from state the agent cannot edit and fails closed for claim-launched sessions when required state is missing or unreadable; tests cover attempted tampering, worktree renames and re-claims.
- [ ] No level permits a merge or a push to `master` or `main`, including through shell wrappers around git.
- [ ] Every block explains in plain words why the action was blocked.
- [ ] Automated tests cover allowed and blocked actions at each level, approval, session isolation, nested subagents, missing or unreadable state, shell wrappers and the listed edge cases. Hook speed is evaluated.

## Out of Scope

Designing the claim feature itself, the ccsession shim, or agent launching.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/hooks/hooks.json` and `src/superclaude/hooks/scripts/block-bare-python.sh`: existing hook registration and Bash blocking example; the new hook source belongs under `src/superclaude/hooks/` and is synced to `.claude/` by `make sync-dev`.
- `.claude/settings.json`: project hook registrations; the only tracked file under `.claude/`.
- `src/superclaude/skills/sc-issue-protocol/refs/claim.md` and `src/superclaude/commands/issue.md`: claim protocol and command surface, subject to the parallel pipeline feature.
- `tests/hooks/test_block_bare_python.py`: existing hook test example.

## Related Issues/PRs

- [#322](https://github.com/IronbellyOrg/IronClaude/issues/322): open design review for a worktree write boundary across tools and agents.
- [#357](https://github.com/IronbellyOrg/IronClaude/issues/357): closed issue for a PreToolUse hook replacing a text-only rule.
- [#339](https://github.com/IronbellyOrg/IronClaude/issues/339): open issue for session orchestration in a worktree.
- [#315](https://github.com/IronbellyOrg/IronClaude/issues/315): open issue for agent-spawned worktree sessions stuck at the ccsession Session Name prompt; claim launches Claude behind the shim.

None is a true duplicate.

<!-- sc:issue:create template=issue-feature-simple -->
