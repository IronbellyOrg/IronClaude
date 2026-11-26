# Draft notes

Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.

## New material

- Codebase pass: `/sc:analyze --depth deep` was followed from `~/.claude/commands/sc/analyze.md` on `src/superclaude/cli/` and `tests/` using Grep, Glob and Read only; codegraph MCP tools were not available to the worker and `auggie` is not on the PATH. The installed skill refs and templates under `~/.claude/skills/` were not readable, so the in-checkout copies under `src/superclaude/skills/sc-issue-protocol/` were used.
- Added fact: the `install` command is `src/superclaude/cli/main.py:46`; it calls `install_all_skills(force=force)` at `src/superclaude/cli/main.py:206`; the output that is currently last comes from step 10, `run_retire_files_step` (`src/superclaude/cli/main.py:273-283`, `src/superclaude/cli/install_retired_files.py:269-306`), or from its "Retire step skipped" warning.
- Added fact: `install_all_skills` returns `(success, message)` and the copied skills exist only as the local list `installed` (`src/superclaude/cli/install_skills.py:83`, `:112-113`, `:119-122`); the copy itself is `shutil.copytree` in `src/superclaude/cli/install_skill.py:52`.
- Added fact: `superclaude update` calls the same `install_all_skills(force=True)` (`src/superclaude/cli/main.py:402`); `install --list` returns before any install step (`src/superclaude/cli/main.py:89-174`).
- Added fact: existing tests stub `superclaude.cli.install_skills.install_all_skills` with fakes that return a 2-tuple and accept `*args, **kwargs` (`tests/cli/test_update_command.py:20`, `:74-96`; `tests/cli/test_install_retired_mcp.py:518`, `:526-529`); real-install tests of the function are in `tests/unit/test_cli_install.py:683`, `:713`, `:789`, `:942`.
- Added fact: no possible duplicate issue was found (`scout.md`: searches `superclaude install skills count` and `install summary skills copied` returned no results).
- Added fact: regression-gate commands come from the Makefile (`test` runs `uv run pytest`; `lint` runs `lint-architecture` and `uv run ruff check .`; `verify-sync` at `Makefile:166`); `docs/user-guide/commands.md:343` mentions `superclaude install`.
- Added: Priority Medium, trigger "a planned feature" from the Priority rule set in `refs/create.md`.
- Assumption: the printed line reads `Skills copied: <N>`; the exact wording was not given.
- Assumption: "copied" means the skills `install_all_skills()` copied in this run (the `installed` list); skills skipped because they already exist, skills served by `/sc:` commands, Orca skills from `install_user_setup` and the ccsession skill are not counted.
- Assumption: the line is also printed when `install` exits 1, and prints `0` when nothing was copied (for example a second run without `--force`).
- Assumption: `superclaude update` and `superclaude install --list` are out of scope and do not get the line.
- Assumption: the count reaches `install` through a new optional keyword argument (`counts: dict[str, int] | None = None`) filled by `install_all_skills`, keeping the 2-tuple return so existing stubs and `update` keep working; the parameter name and shape are open to the implementer.
- Assumption: Effort Estimate is 3 hours (one function, one call site, tests, one doc check); by the `refs/claim.md` rubric this is simple, while Complexity is filed as complex because `--depth deep` was given.
- Assumption: a reviewer may check the result with a throwaway `HOME`; the install's codegraph phase may need network access or fail there, and the skills-copied line is still printed because of the "printed when exit 1" assumption above.
- Assumption: the Problem Statement, User Story, Out of Scope, Success Metrics and Dependencies sections stay "Not known yet" because the description and the pass give nothing for them.

## Contradictions

- None
