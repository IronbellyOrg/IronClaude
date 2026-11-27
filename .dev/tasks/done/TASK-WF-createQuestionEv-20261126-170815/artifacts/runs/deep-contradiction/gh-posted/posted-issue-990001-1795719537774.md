## Bug Summary

`/sc:issue --create` crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` when the description is empty. The documented behaviour for an empty description is a STOP ("--create needs a description"), and that rule is enforced only by prose and by a phrase-presence test.

## Environment (OS, version)

- OS: Not known yet (the codebase pass ran on Linux 6.8.0-149-generic; the reporter's OS is not stated)
- Version: Not known yet for the reporter. The pass read package version 6.1.0 (`pyproject.toml:7`), branch `qev-run`, commit `862384852`.

## Current Behavior

`/sc:issue --create` crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` when the description is empty. See Codebase Context for what the code and docs say about this path.

## Expected Behavior

An empty `--create` description stops with the message "--create needs a description" and creates no draft directory and no GitHub issue (`src/superclaude/commands/issue.md:56`), instead of crashing.

## Steps to Reproduce

1. Run `/sc:issue --create ""` (an empty description). Not known yet: the exact command line, flags and any `@path` file the reporter used.

## Impact Assessment (Severity, Blast Radius)

- Severity: Not known yet
- Blast Radius: Not known yet

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

Codegraph and auggie were not available to the worker, so the pass used Glob, Grep and Read (depth deep).

- `src/superclaude/commands/issue.md:56`: the STOP rule for an empty `--create` description or an empty or missing `@path` file. It is checked "before Activation", so it lives in the command's prose.
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:98`: create Wave 0 writes `<D>/description.md` from `templates/description.md`. `SKILL.md:156`: the error-handling table repeats the empty-description STOP.
- `src/superclaude/skills/sc-issue-protocol/refs/create.md:3`: the slug rule falls back to `untitled` when nothing is left. `create.md:15-16`: Wave 0 steps 3 and 4 have no explicit empty-description check of their own.
- `src/superclaude/skills/sc-issue-protocol/scripts/`: only `clickup_claim.py`, `origin_repo.py` (`main` at line 177, argparse) and `orca_worktree.py`. None reads the create description, and none is named `create_issue.py`.
- `tests/commands/test_issue_command.py:191`: the only test of the rule; it asserts the phrase "empty `--create` description" appears in the STOP rules text. It does not test any behaviour.
- `tests/skills/test_issue_protocol.py:186-190` and `:210`: `reference_slug("")` returns `untitled`, so an empty description would produce a valid draft directory name if the STOP were skipped.
- The only `create_issue` string in the repo outside `.dev/` is `tests/hooks/test_launch_level_guard.py:3609` (an MCP tool name `mcp__github__create_issue`), unrelated.

## Related Issues

None found. The scout searched `sc:issue create empty description crash` and `create_issue.py` and found no results.

## Frequency

Not known yet

## User Impact

Not known yet

## Business Impact

Not known yet

## Cascading Effects

Not known yet

## Logs and Stack Trace

```text
Not known yet
```

## Attempted Solutions

Not known yet

## Proposed Solution

Not known yet

## For Development Team (Root Cause Analysis)

- Root Cause Analysis: Not known yet. The crash site is `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py`; the documented path for an empty description is a STOP (`src/superclaude/commands/issue.md:56`). The STOP is not enforced by any script or test of behaviour, so an agent that skips it would continue to Wave 0 and write an empty `description.md` with the `untitled` slug (`refs/create.md:3`, `tests/skills/test_issue_protocol.py:190`). This is a lead, not a confirmed cause.

## Priority

High: a documented command fails (`/sc:issue --create` crashes instead of its documented STOP), the "High" trigger of the Priority rule set in `refs/create.md`.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: /sc:troubleshoot (reproduce), then /sc:workflow, then /sc:implement, then /sc:pr-submit --monitor 3.

Steps, in order:

- Step 1: Reproduce and locate the reported crash. Ask the reporter for the exact command, the output and where `create_issue.py` came from (their own checkout or fork?). Run `/sc:issue --create ""` and `/sc:issue --create @<empty file>` in a clean checkout and record what happens. Touches: `src/superclaude/commands/issue.md` (STOP rules, line 56) and `src/superclaude/skills/sc-issue-protocol/` (SKILL.md, refs/create.md, scripts/).
- Step 2: If the STOP holds and no crash exists, correct the report (close as not reproducible, or retitle it). Assumption: the most likely real gap is that whitespace-only descriptions and the `@path` empty or missing case are not named in `refs/create.md` Wave 0. Then add an explicit "empty or whitespace-only description: STOP `--create needs a description`" check as Wave 0 step 0 in `src/superclaude/skills/sc-issue-protocol/refs/create.md` and mirror it in the `SKILL.md` Create mode Wave 0 line (`SKILL.md:98`).
- Step 3: If a real crash is found, fix it at the site found in step 1 (not in a new `create_issue.py`), keeping the script style of `scripts/origin_repo.py` (argparse, exit codes) when a script is the site.
- Step 4: Edit only under `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never stage `.claude/` contents (repo rule); stage only the `src/` side.

## Test plan

- Tests to add or change: in `tests/commands/test_issue_command.py`, extend `test_stop_rules_come_before_activation` (line 191) to also assert the message text "--create needs a description" and the `@path` empty-or-missing wording. In `tests/skills/test_issue_protocol.py`, add a test that `refs/create.md` Wave 0 names the empty or whitespace-only description STOP before `<D>` is created (next to the slug tests at lines 193-221). If step 1 finds a real crash in a script, add a pytest that runs that script with an empty description and asserts a clean non-crash exit.
- Regression gate: `uv run pytest` (full suite), `make lint`, `make verify-sync`.
- How a reviewer verifies: run `uv run pytest tests/commands/test_issue_command.py tests/skills/test_issue_protocol.py -v` and see every test pass, then run `/sc:issue --create ""` and see the STOP "--create needs a description" with no `.dev/issues/draft-*` directory created and no GitHub write.

<!-- sc:issue:create template=issue-bug-complex -->
