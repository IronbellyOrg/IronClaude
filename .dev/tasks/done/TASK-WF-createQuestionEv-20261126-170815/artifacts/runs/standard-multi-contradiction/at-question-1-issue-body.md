<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Bug Summary

An empty description is reported to crash `/sc:issue --create`; the claimed Python crash and logging locations do not exist in this checkout, so the actual failure location needs reproduction. [synthetic run marker: qev-standard-multi-contradiction-182258]

## Environment (OS, version)

- OS: Not known yet
- Version: Not known yet

## Current Behavior

The user reports a crash for an empty description. Static inspection cannot confirm a runtime crash: `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` and `src/superclaude/skills/sc-issue-protocol/scripts/issue_logger.py` are both absent, so this checkout cannot crash or log through those named files. The command instead specifies an empty-description STOP before skill activation. No live slash-command reproduction or log output was supplied or collected in this pass.

## Expected Behavior

Reject an empty `--create` description, or an empty or missing `@path` description file, before Activation with `--create needs a description`, as specified in `src/superclaude/commands/issue.md:51-56`. Do not continue into issue creation for these inputs.

## Steps to Reproduce

1. Proposed reproduction from the report, not executed during this pass: in a Claude Code session with the command installed, enter `/sc:issue --create "" --mode bug --type skill --depth standard`.
2. Capture whether the command gives the documented STOP or a crash, along with the installed version and a sanitized traceback if present. The precise failure location is Not known yet.

## Impact Assessment (Severity, Blast Radius)

- Severity: Not known yet
- Blast Radius: Reported for users invoking `/sc:issue --create` with an empty description; effects beyond this case are Not known yet.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

- `src/superclaude/commands/issue.md:51-56` is the actual command-level empty-description handling: STOP rules precede Activation and cover an empty description and an empty or missing `@path` file.
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:15-18` describes an agent-executed create protocol whose command has already validated the flags; it is not a Python `create_issue.py` entry point. Its helper inventory at lines 33-35 names `origin_repo.py`, `clickup_claim.py` and `orca_worktree.py`, not a create handler or logger. Direct filesystem checks confirmed both user-named scripts are absent.
- `tests/commands/test_issue_command.py:183-191`, `test_stop_rules_come_before_activation`, checks STOP-rule text and ordering, including the empty-description rule; it does not execute a slash command or verify the actual STOP response.
- `tests/skills/test_issue_protocol.py:147-157`, `test_every_named_path_exists_and_every_file_is_named`, checks the skill's declared file inventory against disk.
- Filed flags remain `--mode bug --type skill --depth standard`.
- The pass followed `/sc:analyze` without a depth flag using Glob, Grep and Read. Codegraph MCP and Auggie tools were unavailable in the session; the guarded CLI readiness check found an uninitialized index, so no graph lookups were used. Runtime behavior and performance were not measured.
- Codegraph: index_state=not_initialized, checked_at=2026-11-26T18:24:57Z; degraded: graph:not_initialized. Access: cli. Worktree root: `/tmp/createQuestionEv-scratch/clones/standard-multi-contradiction`.

## Related Issues

Not known yet. The supplied `scout.md` reports no possible-duplicate matches; this does not establish that none exist.

## Priority

High: the rule trigger is “a documented command or gate fails”; Assumption: the reported empty-description crash is reproducible in the installed command, pending verification.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: `/sc:workflow "Reproduce the empty-description /sc:issue --create failure and enforce its pre-Activation STOP" --depth standard --handoff none`, then `/sc:implement <the generated plan path>`, then, when submission is requested, `/sc:pr-submit --monitor 3 --base integration` with the actual head, title and body.

Steps, in order:

- Step 1: Reproduce against the installed command and compare its content to `src/superclaude/commands/issue.md`, especially the STOP rule at line 56. Capture sanitized evidence and the installed version. Do not attribute a failure to the absent `create_issue.py` or `issue_logger.py` or add those files merely to match the report.
- Step 2: Assumption: if reproducible, this is an enforcement or installed-copy mismatch around the existing validation contract, not a proven Python exception. Trace the observed path through `src/superclaude/commands/issue.md` and `src/superclaude/skills/sc-issue-protocol/SKILL.md`; change only the confirmed failing boundary. Update `src/superclaude/skills/sc-issue-protocol/refs/create.md` only if protocol clarification is needed. If the existing STOP works, record the non-reproduction rather than invent a fix.
- Step 3: Strengthen the static command tests in `tests/commands/test_issue_command.py` and retain the inventory checks in `tests/skills/test_issue_protocol.py`; add the manual behavioral checks below because static wording alone is insufficient. After any canonical primitive edits, run `make sync-dev`; do not hand-edit or stage generated `.claude/` mirrors.
- Step 4: Run the regression gates and obtain reviewer verification before submission to IronbellyOrg/IronClaude against integration.

## Test plan

- Tests to add or change: extend `tests/commands/test_issue_command.py::test_stop_rules_come_before_activation` to check the exact `--create needs a description` response and all three documented cases (empty inline description, empty `@path`, missing `@path`) in the pre-Activation rules. Retain `tests/skills/test_issue_protocol.py::test_every_named_path_exists_and_every_file_is_named` so any changed helper references must exist.
- Assumption: there is no demonstrated automated slash-command execution harness for this case in the inspected tests. In a controlled Claude Code session, manually exercise the three invalid-input cases with `--mode bug --type skill --depth standard`; verify the exact STOP message, no traceback, no skill activation, and no GitHub or ClickUp writes. Check a non-empty description reaches normal validation, stopping the controlled run before posting.
- Regression gate: run `uv run pytest tests/commands/test_issue_command.py tests/skills/test_issue_protocol.py`, then the full suite `uv run pytest`, `make lint` and `make verify-sync`; run `make sync-dev` first if canonical primitives changed. These are planned checks, not reported passes from this drafting run.
- How a reviewer verifies: inspect the source diff and installed command for the early STOP boundary, repeat the three invalid-input checks in the controlled session, review sanitized reproduction evidence and confirm the focused tests and full regression gates pass. Confirm that no nonexistent create handler or logger is presented as the root cause without new evidence.

<!-- sc:issue:create template=issue-bug-simple -->
