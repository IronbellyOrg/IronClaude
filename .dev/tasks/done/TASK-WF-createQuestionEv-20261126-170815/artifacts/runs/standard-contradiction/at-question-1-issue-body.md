<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Bug Summary

An empty description is reported to crash `/sc:issue --create`. The claimed `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` does not exist in this checkout; the actual command contract requires rejecting an empty description before skill activation, so the reported failure needs reproduction against that validation boundary rather than an assumed Python creation script.

## Environment (OS, version)

- OS: Not known yet
- Version: Not known yet for the affected installation. The inspected command declares version `1.1.0` (`src/superclaude/commands/issue.md:3`).

## Current Behavior

The description reports a crash on empty input, but no runtime trace or reproduction was supplied. Static inspection instead finds a STOP rule for an empty description or an empty/missing `@path` file, with the message `--create needs a description`, checked before Activation (`src/superclaude/commands/issue.md:51-56`). This is a behavioral instruction, not evidence that a live invocation obeys it; no live invocation was performed during this pass.

## Expected Behavior

Reject an empty description and an empty or missing `@path` description with `--create needs a description`, before activating `sc:issue-protocol` (`src/superclaude/commands/issue.md:51-56,108-114`). This should not enter create-mode lookup or posting waves.

## Steps to Reproduce

1. Proposed reproduction, not yet verified: in Claude Code invoke `/sc:issue --create "" --mode bug --type skill --depth standard`.
2. Capture the response and whether skill activation or a worker/GitHub call occurs. The documented result is the validation message, not a traceback. The actual crash output and affected installation remain Not known yet.

## Impact Assessment (Severity, Blast Radius)

- Severity: Not known yet; no crash trace or runtime reproduction was supplied.
- Blast Radius: Potentially users invoking create mode with an empty description; actual runtime reach is Not known yet. The documented boundary should prevent entry into create-mode lookup and posting.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

- Standard codebase pass (no `--depth`) followed the installed analyze command using Glob, Grep and Read. Codegraph and Auggie MCP tools are unavailable in this worker. A Codegraph CLI executable was detected, but neither the installed nor project `CODEGRAPH.md` guide was present, so no graph readiness/query command was improvised. Codegraph: index_state=unknown, checked_at=2026-11-26T18:19:15Z; degraded: graph:unresolved. Access: none; worktree_root: `/tmp/createQuestionEv-scratch/clones/standard-contradiction`.
- `src/superclaude/commands/issue.md:51-56,108-114`: empty-input validation precedes the mandatory skill activation. `src/superclaude/skills/sc-issue-protocol/SKILL.md:156` repeats that empty descriptions STOP with usage before Activation. Runtime compliance is unverified.
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:24-50` inventories the package. Its scripts are `origin_repo.py`, `clickup_claim.py` and `orca_worktree.py` (`:33-35`); `create_issue.py` is absent, confirmed by file lookup. Create posting belongs to the orchestrator (`src/superclaude/skills/sc-issue-protocol/refs/create.md:88-99`), not that alleged script.
- `src/superclaude/skills/sc-issue-protocol/refs/create.md:3,11-16`: the slug rule has an `untitled` fallback and Wave 0 persists a description. That fallback is not permission to bypass the command's earlier empty-description STOP rule.
- `tests/commands/test_issue_command.py:183-191` checks that STOP rules precede Activation and mention empty descriptions. It checks Markdown text, not live command behavior. `tests/skills/test_issue_protocol.py:147-157` pins the package inventory; `:186-220` tests a reference slug transformation, including empty input, not command acceptance.
- Static assessment: the reported Python failure location is contradicted by the checkout; no runtime root cause, security exposure or performance defect was established. The actionable quality concern is verifying the pre-activation rejection contract and its regression coverage.

## Related Issues

Not known yet. The supplied scout found no results for `"create_issue.py"` and `"empty description" crash` (`scout.md:28-34`); this does not prove that no related issue exists.

## Priority

High: Assumption: the reported failure is reproducible in an affected installation; the rule trigger is "A documented command or gate fails" because empty-input rejection would be failing, although this checkout's written contract already requires rejection.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: `/sc:troubleshoot` to establish the failing validation boundary, then `/sc:workflow`, then `/sc:implement` for the confirmed change, then `/sc:pr-submit --monitor 3` after the gates pass and submission is authorized.

Assumption: any confirmed defect is in command/protocol validation or installed-copy drift, not a nonexistent `create_issue.py`; do not invent that script or change the supplied `--mode bug --type skill --depth standard` classification.

Steps, in order:

- Step 1: Compare the affected installed `~/.claude/commands/sc/issue.md` and `~/.claude/skills/sc-issue-protocol/SKILL.md` with the project `.claude/commands/sc/issue.md` and `.claude/skills/sc-issue-protocol/SKILL.md` when present. Reproduce empty input and capture the first departure from the STOP rule in `src/superclaude/commands/issue.md:51-56`; do not claim a root cause without that evidence.
- Step 2: If reproduction confirms a validation gap, edit the canonical `src/superclaude/commands/issue.md` STOP instructions and, only where necessary for consistency, `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `refs/create.md` so invalid descriptions stop before workers, lookups or posting. If the source contract is already sufficient and only the installation is stale, correct the installation instead of adding a redundant creation script.
- Step 3: Strengthen `tests/commands/test_issue_command.py` for the exact rejection message and empty/missing `@path` cases; retain the package-inventory and slug-safety checks in `tests/skills/test_issue_protocol.py`. Sync canonical changes with `make sync-dev`, run the regression gates, and attach the controlled reproduction evidence to the eventual PR.

## Test plan

- Tests to add or change: extend `tests/commands/test_issue_command.py::test_stop_rules_come_before_activation` and add a proposed `test_empty_create_rule_names_message_and_file_cases` to pin `--create needs a description`, empty direct input, and empty/missing `@path` rejection. Keep `tests/skills/test_issue_protocol.py::test_every_named_path_exists_and_every_file_is_named` and `test_reference_slug_never_leaves_the_issues_directory` passing. These static tests protect the contract but cannot establish live model compliance.
- Assumption: whitespace-only input should be rejected as empty; make that explicit in the command rule and test it if the reproduction confirms this edge is relevant.
- Regression gate: run `uv run pytest tests/commands/test_issue_command.py tests/skills/test_issue_protocol.py`, then the full suite with `make test`, lint with `make lint`, and `make sync-dev && make verify-sync` after any canonical primitive edits (`Makefile:13-15,48-50,109-136,165-167`). No tests or gates were executed during this static drafting pass.
- How a reviewer verifies: use a controlled Claude Code session to try the empty-string invocation above, whitespace-only input under the stated assumption, an empty `@path` file and a missing `@path` file. Each must emit `--create needs a description` before skill activation, with no workers, GitHub/ClickUp writes or traceback. Compare the affected installed and project copies, inspect the focused test assertions, and confirm the full-suite, lint and sync results. Do not post an issue merely to test invalid-input rejection.

<!-- sc:issue:create template=issue-bug-simple -->
