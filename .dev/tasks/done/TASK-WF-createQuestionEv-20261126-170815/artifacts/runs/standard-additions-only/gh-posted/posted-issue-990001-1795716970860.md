<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Feature Summary

Make `superclaude install` print how many skills it copied as its last line.

## Problem Statement

The copied-skill count is not available at the end of the command. The batch installer already builds an installed-skills list and includes its length in the skills-phase message (`src/superclaude/cli/install_skills.py:112-122`), but the CLI prints that message before session wiring, hooks, templates, user setup, codegraph and retirement (`src/superclaude/cli/main.py:202-279`). Users must look back through the output to find it.

There is no single fixed last line today: when no retired files are present, the final retirement step prints `No retired commands, skills or agents present.`; other outcomes print kept/removed-item details or restart guidance (`src/superclaude/cli/install_retired_files.py:269-306`). The CLI can also print a retirement-exception warning before its exit-code check (`src/superclaude/cli/main.py:280-296`).

## User Story

Not known yet

## Proposed Solution

Carry the numeric successful-copy count from the skills installer to the CLI, then print it after all subsequent installation and retirement output. Use actual copy outcomes rather than counting the destination directory or parsing the human-readable phase message.

The existing batch installer separates installed, skipped, failed and command-served skills (`src/superclaude/cli/install_skills.py:83-115`); a successful single-skill copy is a completed `shutil.copytree` (`src/superclaude/cli/install_skill.py:50-55`). The count semantics and proposed wording below are labelled assumptions, not additional user-stated requirements.

## Acceptance Criteria

- [ ] The last output line of `superclaude install` states the number of skills copied in that invocation, after all later-phase and retirement output.
- [ ] Under the count-scope assumption in Fix approach, successful new copies and forced reinstalls count; skipped, command-served and failed skills do not. A run with no successful copies reports zero.
- [ ] Under the completion-path assumption in Fix approach, the footer also appears when a phase returns failure and the command reaches its normal exit-code check; existing diagnostics and exit codes remain unchanged.
- [ ] `superclaude install --list` remains a listing operation and does not acquire a copied-skills footer.
- [ ] Automated tests check the final output line, not merely whether a count appears somewhere in the output.

## Out of Scope

Not known yet

## Components Affected (from `/sc:analyze`)

- `src/superclaude/cli/main.py:202-208,271-296`: collect the skills count and emit the footer after retirement, before the exit-code check.
- `src/superclaude/cli/install_skills.py:62-150`: expose the numeric count derived from successful outcomes, including zero-copy paths, while retaining existing call compatibility.
- `src/superclaude/cli/install_skill.py:39-55`: existing skip/force/copy semantics; reference for count tests, not necessarily a source change.
- `src/superclaude/cli/install_retired_files.py:269-306`: existing final-output producer; footer ordering must remain correct for its different outcomes.
- `tests/cli/test_update_command.py:128-143,169-183`: existing CLI invocation, phase-order, list-only and failure coverage to extend.
- `tests/unit/test_cli_install.py:643-727`: existing batch skill-install and command/protocol mapping coverage to extend.
- `tests/cli/test_install_retired_files.py:699-712`: retirement-exception and exit-code regression coverage.

## Related Issues/PRs

Not known yet. The scout's two duplicate searches returned no results (`scout.md:28-30`).

## Priority

Medium: the Priority rule set's planned-feature trigger applies; no command failure, blocked work, security exposure or data loss is established by this request.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: `/sc:workflow` to produce the checked implementation plan, then `/sc:implement` with that plan, then `/sc:pr-submit --monitor 3` after verification, targeting this repo and base branch.

Assumption: the count covers the packaged batch skills copied by `install_all_skills` in this invocation, including successful `--force` replacements, not files within a skill, pre-existing skills, or external Orca-managed skill installation. Orca's separate installer does not currently supply a numeric copy count (`src/superclaude/cli/install_user_setup.py:323-371`).

Assumption: use the stable plain-text footer `Skills copied: N`, where N is the numeric count; the user did not specify exact wording.

Assumption: emit the footer on all completed install paths, including reported phase failures, but not `--list` or unhandled exceptions that abort the command before completion.

Assumption: preserve the existing two-item `(success, message)` interface for batch-installer callers and do not extend this feature to `superclaude update` or `install-skill`.

Steps, in order:

- Step 1: In `src/superclaude/cli/install_skills.py`, expose structured successful-copy accounting to the CLI through a compatible reporting mechanism. Derive it from the installed outcomes, not message text, available-skill totals or directory contents. Cover empty, skipped, command-served, failed and forced-copy cases.
- Step 2: In `src/superclaude/cli/main.py`, retain that count through the remaining phases and print the footer after the final retirement handler and before the existing exit-code check. Keep earlier diagnostics, phase ordering and failure behavior intact; leave the list-only early return unchanged.
- Step 3: Extend `tests/unit/test_cli_install.py` and `tests/cli/test_update_command.py` for the count and final-line contract; retain retirement exception/exit-code coverage in `tests/cli/test_install_retired_files.py`. Run the verification gates before submission.

## Test plan

- Tests to add or change: batch-installer tests in `tests/unit/test_cli_install.py` for known successful counts, a second non-force run yielding zero, forced reinstall counts, empty availability, command-served exclusions, and mixed successful/failed copies. Check that existing two-item callers still work.
- Tests to add or change: CLI tests in `tests/cli/test_update_command.py` using isolated HOME and stubbed external phases. Assert `result.output.splitlines()[-1]` equals the expected `Skills copied: N`; make later phases emit sentinel output to prove the footer remains last. Include zero copies, `--force`, a reported downstream failure, retirement output/exception and `--list` without a footer. Preserve existing exit-code and phase-order assertions.
- Assumption: reviewer verification should use the isolated CLI fixtures rather than running a real install into the reviewer's home, because installation has external setup phases.
- Regression gate: `uv run pytest tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py`, then the full suite `uv run pytest`, `make lint`, and `make verify-sync` must pass. These are future verification requirements; tests were not executed during this read-only drafting pass.
- How a reviewer verifies: run the focused tests and regression gates; inspect captured CLI output for a known successful count and a zero-copy run, confirming the footer is the final line even after retirement messages, failures still exit nonzero where they did before, and `--list` is unchanged.

<!-- sc:issue:create template=issue-feature-simple -->
