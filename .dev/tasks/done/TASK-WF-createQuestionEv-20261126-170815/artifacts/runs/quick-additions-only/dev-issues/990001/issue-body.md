<!-- /sc:issue feature template (simple). -->

## Feature Summary

Make `superclaude install` print, as its last line, how many skills it copied. [synthetic run marker: qev-quick-additions-only-180235]

## Problem Statement

Not known yet.

## User Story

Not known yet.

## Proposed Solution

Print the number of skills copied as the final line of `superclaude install`.

## Acceptance Criteria

- [ ] The last line of `superclaude install` reports how many skills it copied.

## Out of Scope

Not known yet.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/cli/main.py`: orchestrates installation and subsequent retirement steps; currently the retirement step produces the last output, with a warning if it raises.
- `src/superclaude/cli/install_skills.py`: tracks installed, skipped, command-served and failed skills; `install_skill.py` copies skill directories.
- `tests/unit/test_cli_install.py`: existing installer and skill installation tests.

Codegraph and Auggie MCP tools were unavailable; the quick pass used Grep and Read.

## Related Issues/PRs

Not known yet; the scout found no possible duplicates.

## Priority

Medium: planned feature.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: `/sc:implement`, then `/sc:pr-submit --monitor 3`.

Steps, in order:

- Step 1: In `src/superclaude/cli/install_skills.py` and `src/superclaude/cli/main.py`, propagate a structured count of successfully copied skills and print it after the retirement steps, preserving installer behavior and exit status.
- Step 2: Update callers and tests for any return-contract change, including `tests/unit/test_cli_install.py`; cover the final output line.

Assumption: The count covers successful copies by the batch skill installer in this invocation, excluding skipped, failed and command-served skills; forced reinstalls count as copies. Report the count even if a later phase fails; `--list` remains a listing rather than an install.

## Test plan

- Tests to add or change: Add CLI output tests in `tests/unit/test_cli_install.py` for fresh copies, zero copies on repeat, forced reinstall, mixed failures and later-phase failure; verify the last line and existing exit behavior. Assumption: mock unrelated installer phases to keep tests isolated.
- Regression gate: `uv run pytest`, `make lint`, and `make verify-sync`.
- How a reviewer verifies: Run the added tests and regression gate; in an isolated test environment run `superclaude install` and repeat it, confirming the last output line matches the successfully copied skill count each time.

<!-- sc:issue:create template=issue-feature-simple -->
