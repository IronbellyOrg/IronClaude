<!-- /sc:issue bug template (complex). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Bug Summary

`superclaude install` never reports how many skills it copied: its last line is whatever the final retire step prints (or the codegraph/retire warning), and no line anywhere gives a skills total. The user asks that the command print, as its last line, how many skills it copied. [synthetic run marker: qev-deep-flag-preserved-190117]

## Environment (OS, version)

- OS: Not known yet (the reporter's OS is not given). Code read on Linux 6.8.0-149-generic.
- Version: Not known yet for the reporter. Code read at package version 6.1.0 (`pyproject.toml:7`), branch `qev-run`, commit `862384852`.

## Current Behavior

Running `superclaude install` echoes the output of `install_all_skills` in Step 4 (`src/superclaude/cli/main.py:202-208`) and then runs the remaining steps (ccsession wiring, hooks, templates, user setup, codegraph, retire steps). Nothing after Step 4 prints a skills total, and nothing prints a count as the last line:

- The skills block prints `✅ Installed N skills:` only when at least one skill was installed (`src/superclaude/cli/install_skills.py:119-122`); when none were, there is no count line at all, and the early returns print only `No skills available to install` (`install_skills.py:80-81`) or `No skills to install` (`install_skills.py:144-145`).
- The last output of a successful run is the Step 10 retire step (`main.py:271-283`, output from `run_retire_files_step`, for example `   No retired commands, skills or agents present.` at `src/superclaude/cli/install_retired_files.py:280`), or the retire-skipped warning at `main.py:281-283`.
- When any step fails, the command ends with `sys.exit(1)` at `main.py:285-296`, again with no count line.

## Expected Behavior

`superclaude install` prints, as its final line of output, how many skills it copied, on every path that reaches the end of the command:

- After the Step 10 retire step and any warning it prints (`main.py:271-283`).
- Also when the run ends in `sys.exit(1)` (`main.py:285-296`): the count line is printed before the exit.
- "Copied" means the installed bucket of `install_all_skills` (`install_skills.py:83`, appended at `:113`, reported at `:119`). Skills skipped because they already exist (without `--force`), skills served by `/sc:` commands and skills that failed are not counted.
- When nothing is installed (including the early returns at `install_skills.py:80-81` and `:144-145`), the line still prints `0`.

## Steps to Reproduce

1. In a checkout, run `uv run superclaude install` (use a throwaway `HOME`, because the codegraph phase downloads a binary and registers an MCP server).
2. Look at the last line of the output: it is the Step 10 retire output, not a skills count.
3. Search the output for a skills total: only `✅ Installed N skills:` (first run) or `⚠️  Skipped N existing skills` (rerun without `--force`) appear, in the middle of the output, and never as the last line.

## Impact Assessment (Severity, Blast Radius)

- Severity: low. Output only; no file, exit code or installed content is wrong. (Assumption: the reporter has not stated a severity.)
- Blast Radius: the `install` command in `src/superclaude/cli/main.py` and the batch skill installer `src/superclaude/cli/install_skills.py`. `superclaude update` (`main.py:356-461`) shares `install_all_skills` (`main.py:402`) and must keep its current output unless the maintainer decides otherwise.

## Error Messages

```text
Not known yet (no error is reported: the command runs to the end and prints no skills count)
```

## Codebase Context (from `/sc:analyze`)

Pass: `/sc:analyze --depth deep` by following `~/.claude/commands/sc/analyze.md`, on Grep, Glob and Read (codegraph and auggie were not available to the worker).

- `src/superclaude/cli/main.py:46` `install(target, force, list_only)`. `--list` returns early at `:174` and prints per-category "available/installed" counts only (`:138-140` for skills); it never reaches the install steps.
- `main.py:202-208` Step 4: `skill_success, skill_message = install_all_skills(force=force)`, then `click.echo(skill_message)`. Only the `(bool, str)` pair is consumed.
- `main.py:241-255` Step 8 codegraph (a failure message goes to stderr, `:255`); `:257-269` Step 9 retire MCP; `:271-283` Step 10 retire files (non-fatal, prints a warning on exception); `:285-296` exit check ending in `sys.exit(1)`.
- `main.py:356-461` `update` also calls `install_all_skills(force=True)` at `:402` and has its own exit check at `:449-461`.
- `src/superclaude/cli/install_skills.py:62-64` `install_all_skills(target_path=None, force=False) -> Tuple[bool, str]`. Buckets: `installed`, `skipped`, `failed`, `served_by_command` (`:83-86`); served-by-command skills are never installed (and a stale install is removed, `:90-98`); existing skills without `--force` are skipped (`:102-104`); `installed.append` / `failed.append` at `:112-115`.
- `install_skills.py:144-145`: `if not installed and not skipped and not served_by_command: return True, "No skills to install"`. This branch also fires when every skill failed, so the failure text built at `:139-142` is dropped and success is reported as True (see draft-notes.md; out of scope here, but it decides what "0" means on that path).
- Callers that depend on the `(bool, str)` shape: `tests/unit/test_cli_doctor.py:78` (`skills_ok, _ = ...`), `tests/troubleshoot/test_diagnostic_worker_contract.py:419` (`ok, message = ...`), `tests/unit/test_cli_install.py:688,721,792,948`.
- Test stubs of `install_all_skills` return a 2-tuple and accept any kwargs: `tests/cli/test_update_command.py:16-25,74-96`, `tests/cli/test_install_retired_mcp.py:514-534`; real skills are installed in `tests/cli/test_install_retired_files.py:560-576` and `tests/cli/test_update_command.py:187-196`.
- Existing install-output tests check order and exit codes, not the final line or a skills total: `tests/cli/test_update_command.py:128-143,280-333`, `tests/cli/test_install_retired_mcp.py:552-560`, `tests/cli/test_install_retired_files.py:603-712`. A search of `tests/` finds no assertion on a skills total or on the last line of `install` output.

## Related Issues

None found: the scout lookup for `superclaude install skills count` returned no possible duplicates (`scout.md`).

## Frequency

Always: no code path of `install` prints a skills total, so every run is affected.

## User Impact

The user cannot read, from the end of the `install` output, how many skills were copied; they have to scroll back through the per-step output (which is only printed when at least one skill was installed) or run `superclaude install --list`.

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

Print one final line, `Skills copied: N` (wording is an assumption), from `install()` after the Step 10 retire step and before the exit check, so it comes last on the success path and on the `sys.exit(1)` path. Get `N` from the installed bucket of `install_all_skills` without changing its `(bool, str)` return: add an optional keyword out-parameter (for example `counts: dict[str, int] | None = None`) that `install_all_skills` fills on every return path, and have `install()` pass a dict and read `installed` with a default of 0 (so stubs that do not fill it print 0). Leave `update` and `install --list` unchanged. Details are in Fix approach.

## For Development Team (Root Cause Analysis)

- Root Cause Analysis: `install_all_skills` returns only `(success, message)` (`install_skills.py:62-64,149-150`); the installed count exists only as `len(installed)` inside the message text (`:119-120`) and is lost to the caller. `install()` echoes that message mid-run (`main.py:206-208`) and has no later statement that prints a total; the command's tail is the retire step (`main.py:271-283`) and the exit check (`main.py:285-296`).

## Priority

Medium: degraded behaviour with a workaround (trigger of the Medium level in the Priority rule set of `refs/create.md`): the count is not shown, but `superclaude install --list` (`main.py:138-140`) or the `- <name>` lines of the Step 4 output give the same information; nothing fails, loses data or blocks other work, so High and Urgent do not apply.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: `integration`.

Commands, in order: `/sc:workflow` (turn this plan into a task plan), then `/sc:implement` (steps 1 to 4 below), then `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` (opens the PR with `gh pr create --repo IronbellyOrg/IronClaude --base integration`, waits for the Augment and Codex reviews, fixes confirmed findings).

Steps, in order:

- Step 1: expose the installed count without breaking the `(bool, str)` contract. In `src/superclaude/cli/install_skills.py` add an optional keyword parameter to `install_all_skills` (for example `counts: dict[str, int] | None = None`) and fill `installed`, `skipped`, `failed` and `served_by_command` on every return path, including the early returns at `:80-81` (all zero) and `:144-145` (installed is 0 there by construction). Update the docstring (`:65-74`). Do not change the return type: `tests/unit/test_cli_doctor.py:78`, `tests/troubleshoot/test_diagnostic_worker_contract.py:419` and the test stubs rely on the 2-tuple.
- Step 2: print the final line in `src/superclaude/cli/main.py` `install()`: create the dict before Step 4 (`:202`), pass it as `counts=` at `:206`, and after the Step 10 try/except (`:283`) and before the exit check (`:285`) `click.echo(f"Skills copied: {counts.get('installed', 0)}")`. Because the echo comes before `sys.exit(1)` (`:296`), it is last on the failure path too. Do not touch `--list` (`:88-174`) or `update` (`:356-461`) unless the maintainer decides otherwise.
- Step 3: add and change the tests listed in the Test plan (`tests/cli/test_update_command.py`, `tests/unit/test_cli_install.py`).
- Step 4: if the install output is documented, add the new last line to `docs/getting-started/installation.md` (section "What's Installed", `:337`); otherwise skip.
- Step 5: run the regression gate from the Test plan, then open the PR. Before pushing: `git remote get-url origin` must print the IronbellyOrg/IronClaude URL, `git fetch origin && git log HEAD..origin/integration` and rebase onto `origin/integration` if it has commits the branch lacks. Run Python only through `uv run`. Edit only `src/` and `tests/`; never stage `.claude/` mirrors (no `git add .claude/...`, no `git add -f`; no primitive is edited here, so `make sync-dev` is not needed).

## Test plan

- Tests to add or change:
  - `tests/cli/test_update_command.py` (stubbed installers, next to `test_install_runs_codegraph_phase_after_user_setup_before_retire` at `:280`): `test_install_prints_skills_copied_as_last_line` (stub `install_all_skills` to fill `counts["installed"] = 3`; assert the last non-empty line of `result.stdout` is `Skills copied: 3` and exit code 0); `test_install_skills_copied_is_last_line_after_failure` (`failing="install_codegraph_mcp"`, exit code 1, last line still the count); the same with the retire step raising (as in `tests/cli/test_install_retired_files.py:706-712`) to prove the line follows the retire warning; `test_install_skills_copied_zero_when_stub_reports_nothing` (stub leaves `counts` empty, last line `Skills copied: 0`); `test_update_and_list_do_not_print_skills_copied` (`update` and `install --list` output has no `Skills copied:` line).
  - `tests/unit/test_cli_install.py` (next to `:683-723`): count cases for `install_all_skills(target_path=tmp_path, force=True, counts=counts)`: `counts["installed"]` equals the number of available skills that are not `_has_corresponding_command` (same computation as `_install_skills` at `:942-955`); a second call with `force=False` gives `installed == 0` and `skipped == <previous installed>`; `served_by_command` skills are not in `installed`; with `install_skill_command` monkeypatched to fail for one skill that skill is in `failed`, not `installed`; with `list_available_skills` monkeypatched to return `[]` both early returns (`:80-81`, `:144-145`) leave `installed == 0`; the returned `(bool, str)` is unchanged.
  - One real-install check in `tests/cli/test_update_command.py` using the `native_install` fixture (`:187-196`): the last line of the real output equals `Skills copied: <expected>` where `<expected>` is computed from the source skills minus command-backed ones.
- Regression gate (all must pass): `uv run pytest` (full suite; at minimum `tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py tests/cli/test_install_retired_files.py tests/unit/test_cli_install.py tests/unit/test_cli_doctor.py tests/troubleshoot/test_diagnostic_worker_contract.py`), `make lint`, `make verify-sync`.
- How a reviewer verifies: run `uv run pytest tests/cli/test_update_command.py tests/unit/test_cli_install.py -v` and see the new tests pass and fail on the pre-change code; then, with `HOME` pointing at a throwaway directory, run `uv run superclaude install 2>&1 | tail -n 1` and expect `Skills copied: N` where N equals the `N` in `✅ Installed N skills:`; run it again without `--force` and expect `Skills copied: 0`; check that `uv run superclaude update 2>&1 | tail -n 1` and `uv run superclaude install --list | tail -n 1` do not end in `Skills copied:`. The real run downloads the codegraph binary, so prefer the CliRunner tests when offline.

<!-- sc:issue:create template=issue-bug-complex -->
