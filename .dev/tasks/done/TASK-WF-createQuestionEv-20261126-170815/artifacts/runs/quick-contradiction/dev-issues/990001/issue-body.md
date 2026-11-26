<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Bug Summary

`/sc:issue --create` crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` when the description is empty. [synthetic run marker: qev-quick-contradiction-180724]

## Environment (OS, version)

- OS: Not known yet
- Version: Not known yet

## Current Behavior

The reporter says the command crashes with an empty description; the crash has not been reproduced in this pass.

## Expected Behavior

The command's STOP rule says an empty description should stop with `--create needs a description` (`src/superclaude/commands/issue.md:56`).

## Steps to Reproduce

1. Run `/sc:issue --create ""`.

## Impact Assessment (Severity, Blast Radius)

- Severity: Not known yet
- Blast Radius: Not known yet

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

- `src/superclaude/commands/issue.md:51-56` defines a pre-activation STOP for empty descriptions; `src/superclaude/commands/issue.md:108-114` invokes the issue protocol skill after those checks.
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:156` likewise specifies stopping before activation; `src/superclaude/skills/sc-issue-protocol/refs/create.md:11-16` describes the create-mode prerequisites.
- `tests/commands/test_issue_command.py:183-191` checks the STOP rule's presence in command text, not a live empty-input execution.
- Codegraph MCP and Auggie tools were unavailable; the quick pass used Glob, Grep and Read.

## Related Issues

Not known yet

## Priority

High: Assumption: the reported crash is reproducible; a documented command fails (High trigger).

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: `/sc:troubleshoot`, then `/sc:implement`, then `/sc:pr-submit --monitor 3`.

Steps, in order:

- Step 1: Reproduce the reported empty-input failure and locate its actual execution path; inspect `src/superclaude/commands/issue.md` and `src/superclaude/skills/sc-issue-protocol/SKILL.md` before choosing a fix.
- Step 2: Assumption: if validation fails in practice, fix the responsible command or protocol component to honor the existing STOP rule; add coverage in `tests/commands/test_issue_command.py` or the appropriate execution test.

## Test plan

- Tests to add or change: Assumption: add an empty-description execution regression at the actual entry point once identified; verify the stated STOP message and no issue creation. Keep the existing command-rule test.
- Regression gate: `uv run pytest`, `make lint`, and `make verify-sync` must pass.
- How a reviewer verifies: run the regression test and the gates above; reproduce `/sc:issue --create ""` in a controlled session and confirm the STOP message without creating an issue.

<!-- sc:issue:create template=issue-bug-simple -->
