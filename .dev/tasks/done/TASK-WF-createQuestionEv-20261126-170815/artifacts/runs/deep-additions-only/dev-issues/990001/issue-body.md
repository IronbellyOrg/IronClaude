<!-- /sc:issue feature template (complex). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Feature Summary

Make `superclaude install` print, as its last line, how many skills it copied. [synthetic run marker: qev-deep-additions-only-183517]

Codebase pass note: `/sc:analyze --depth deep` was run by following the installed `analyze.md` on `src/superclaude/cli/` (install entrypoint and skill-copy code) and `tests/`. The codegraph MCP tools and `auggie` were not available to the worker (`auggie` is not on the PATH), so the pass used Grep, Glob and Read only.

## Problem Statement

Not known yet

## User Story

Not known yet

## Proposed Solution

After every install step has run, `superclaude install` prints one final line that states the number of skills it copied in this run. Today `install_all_skills()` builds a list of the skills it copied (`installed`) but returns only `(success, message)`, so the count exists only inside the message text and `install` cannot print it on its own.

Assumption: the line reads `Skills copied: <N>` (exact wording was not given). Assumption: "copied" means the skills `install_all_skills()` actually copied into `~/.claude/skills/` in this run, which is the `installed` list; it does not include skills skipped because they already exist (no `--force`), skills served by `/sc:` commands (not installed as skills), or Orca skills installed by `install_user_setup`. Assumption: the line is also printed when the install exits 1, and `0` is printed when no skill was copied.

## Acceptance Criteria

- [ ] The last line of the stdout of `superclaude install` is the skills-copied line, after the step 9 and step 10 retire output.
- [ ] The number equals the number of skills the skills step copied in that run (for example `Skills copied: 0` on a second run without `--force` when every skill already exists).
- [ ] Assumption: with `--force`, the number equals the count of skills the skills step reports as `Installed <N> skills`.
- [ ] `superclaude install --list` is unchanged (it returns before any install step runs).
- [ ] The existing exit-code behaviour of `install` is unchanged.
- [ ] `install_all_skills()` still returns a `(success, message)` pair, so the existing test stubs keep working.

## Out of Scope

Not known yet

## Components Affected (from `/sc:analyze`)

- `src/superclaude/cli/main.py:46` `install` command; `:206` calls `install_all_skills(force=force)`; `:273-283` step 10 (retire stale files) prints the current last output; `:285-296` exit-code block.
- `src/superclaude/cli/install_skills.py:62` `install_all_skills`; `:112-113` appends each copied skill to `installed`; `:119-122` prints `Installed <N> skills`; `:144-150` early return and final message.
- `src/superclaude/cli/install_skill.py:12` `install_skill_command` (the actual copy, `shutil.copytree` at `:52`) and `:115` `list_available_skills`.
- `src/superclaude/cli/main.py:402` `update` command calls the same `install_all_skills(force=True)`; it is affected only if the signature change is not backward compatible.
- Tests that stub or exercise the same path: `tests/cli/test_update_command.py` (`_INSTALLERS` at `:16`, `_stub_installers` at `:74`, install tests from `:128`), `tests/cli/test_install_retired_mcp.py` (`_INSTALLERS` at `:514`, `_stub_framework` at `:526`), `tests/unit/test_cli_install.py` (`:683`, `:713`, `:789`, `_install_skills` at `:942`).

## Related Issues/PRs

No possible duplicates were found: the lookup searches `superclaude install skills count` and `install summary skills copied` returned no results (`scout.md`).

## Success Metrics

Not known yet

## Architecture Impact

One backward-compatible change in the data flow between `install_all_skills()` and `install`: the count of copied skills must reach `install`. The call sites and the test stubs treat the return value as a 2-tuple `(bool, str)` and the stubs are patched on the name `superclaude.cli.install_skills.install_all_skills` (`tests/cli/test_update_command.py:20`, `tests/cli/test_install_retired_mcp.py:518`; their fakes accept `*args, **kwargs`), so the return type is kept and the count travels through a new optional keyword argument that `install_all_skills` fills in (Assumption, see Fix approach).

## Dependencies

Not known yet

## Documentation Needs

`docs/user-guide/commands.md` mentions `superclaude install` (match at line 343); check whether it describes the output and update it if it does. Whether other documents or a changelog need an entry is not known yet.

## Alternatives Considered

- Parse the count out of `skill_message` in `main.py`: rejected as an assumption, because it ties the last line to the message wording (`Installed <N> skills:`) and breaks silently when the wording changes.
- Change `install_all_skills()` to return a 3-tuple or an object: rejected as an assumption, because `update` (`main.py:402`) and several test stubs unpack or return a 2-tuple.
- Count by listing `~/.claude/skills/` after the install (`list_installed_skills()`): rejected as an assumption, because that counts skills that exist, not skills copied in this run.

## Impact Analysis (Blast Radius, Integration Impact)

- Blast Radius: the stdout of `superclaude install` gains one line at the end. Anything that parses the last line of that output would see a different last line (no such consumer was found in `src/` or `tests/` by Grep; scripts outside the repo are not known yet). `superclaude update` and `superclaude install --list` do not change.
- Integration Impact: the installed `~/.claude` primitives do not change, so no command, skill or agent needs a matching edit. `make verify-sync` is unaffected because nothing under `src/superclaude/{skills,agents,commands,hooks,templates}` is edited.

## Risks & Mitigation

- Risk: a stub in an existing test returns only a 2-tuple and never fills the count. Mitigation: the keyword argument is optional and `install` falls back to `0` when the count is missing; new tests cover both cases.
- Risk: the line is not last because a later step prints after it. Mitigation: print it after the step 10 `try/except` and before the `sys.exit(1)` block, and assert it with `result.output.rstrip().splitlines()[-1]` in a test.
- Risk: the count is read as "skills now installed" instead of "skills copied". Mitigation: label wording `Skills copied` and test the second-run case (`0`).

## Effort Estimate (hours) and Complexity

- Effort Estimate (hours): 3 (Assumption: one function, one call site, tests and one doc check).
- Complexity: complex, set by `--depth deep` as given; by the hours rubric in `refs/claim.md` alone this work would rate simple (one area, under 4 hours).

## Priority

Medium: a planned feature (Medium trigger "a planned feature"); `superclaude install` works today and nothing is blocked or broken.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: `/sc:workflow` (turn this plan into tasks), then `/sc:implement`, then `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` (it opens the PR with `gh pr create --repo IronbellyOrg/IronClaude --base integration`; never against the upstream repository). Python commands use `uv run`.

Steps, in order:

- Step 1: Branch from `integration` in an Orca-created worktree (`orca worktree create --name <name> --base-branch origin/integration --agent claude --prompt "<task>"`), as the project rules require; no source file is touched.
- Step 2: In `src/superclaude/cli/install_skills.py`, add an optional keyword-only parameter to `install_all_skills` (Assumption: `counts: dict[str, int] | None = None`) and, before each return, fill it with at least `{"copied": len(installed)}` (also `skipped`, `served_by_command`, `failed` if cheap). Keep the `(success, message)` return and all existing messages.
- Step 3: In `src/superclaude/cli/main.py`, in `install`, create `skill_counts: dict[str, int] = {}` before step 4 and call `install_all_skills(force=force, counts=skill_counts)` at line 206. After the step 10 `try/except` (line 283) and before the exit-code block (line 285), print `click.echo(f"Skills copied: {skill_counts.get('copied', 0)}")`. Leave the `--list` branch and `update` unchanged.
- Step 4: Add and update tests (see the Test plan) in `tests/unit/test_cli_install.py` and `tests/cli/test_update_command.py`.
- Step 5: Check `docs/user-guide/commands.md` (line 343 mentions `superclaude install`) and update it only if it shows install output.
- Step 6: Run the regression gate of the Test plan, then open the PR with `/sc:pr-submit --monitor 3`; confirm the returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/N`.

## Test plan

- Tests to add or change:
  - `tests/unit/test_cli_install.py`: add a test that `install_all_skills(target_path=tmp, force=True, counts=c)` sets `c["copied"]` to the number of skills actually present in `tmp` (the skills that are not served by a command), and a test that a second call with `force=False` sets `c["copied"] == 0`. Keep the existing tests at `:683`, `:713` and `:789` unchanged.
  - `tests/cli/test_update_command.py`: add a test that `CliRunner().invoke(main, ["install"])` with a stub that fills `counts` makes `result.output.rstrip().splitlines()[-1] == "Skills copied: <N>"`; a test that the same line is still last when a later phase fails and the exit code is 1 (reuse `test_install_codegraph_failure_keeps_framework_work_and_exits_one` setup); a test that the stub which does not fill `counts` prints `Skills copied: 0`; a test that `["install", "--list"]` and `["update"]` do not print the line.
  - Check that the existing `_stub_installers` fake in this file and `_stub_framework` in `tests/cli/test_install_retired_mcp.py` still pass (their fakes take `*args, **kwargs`).
- Regression gate: the full suite `uv run pytest`, lint `make lint` (runs `lint-architecture` and `uv run ruff check .`), formatting `uv run ruff format --check .`, and `make verify-sync`.
- How a reviewer verifies: run `uv run pytest tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py -v` and expect all green; then run `HOME=$(mktemp -d) uv run superclaude install | tail -n 1` and expect `Skills copied: <N>` with N greater than 0, and run the same command a second time and expect `Skills copied: 0`; run `uv run superclaude install --list | tail -n 1` and expect no skills-copied line.

<!-- sc:issue:create template=issue-feature-complex -->
