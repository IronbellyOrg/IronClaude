---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-buildTheRetireSt-20261118-021743
version: "1"
priority: Medium
created_date: "2026-11-18"
---

# Build the retire step: remove commands, skills and agents that 6.0.0 no longer ships

Source: ./source.md
Goal: `superclaude install` and `superclaude update` remove, from `~/.claude/commands/sc/`, `~/.claude/skills/` and `~/.claude/agents/`, only the files IronClaude can prove it wrote (sha256 equal to the file at the `v5.0.0` tag) and whose names 6.0.0 no longer ships; everything else is kept and reported with the reason and the exact removal command.

## Constraints

- Source of truth is `src/superclaude/`; never stage `.claude/` (except `.claude/settings.json`); `.dev/tasks/` is always staged; do not commit `.dev/issues/v6-retire-step/`.
- Never touch the real `~/.claude`: every test uses a throwaway HOME.
- Do not edit `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/` or past `CHANGELOG.md` entries; add no CHANGELOG entry.
- Swarm items are never listed as removed. No agent is removed at this commit, but the mechanism must handle agents.
- The step lives outside `install_commands`, `install_all_skills` and `install_agents`, so tests that pin "installers never delete" (`tests/cli/test_how_we_work_install.py`) keep their meaning.

## Phase 1: Generated data and its generator

## Task 1: Write the generator script

Create `scripts/gen_retired_install_data.py`. It takes `--tag <tag>` (repeatable) and `--check`. For each tag it lists, with `git ls-tree -r`, the files under `src/superclaude/commands/` (names `*.md` except `README.md`), `src/superclaude/agents/` (`*.md` except `README.md` and `__init__.py`) and `src/superclaude/skills/<name>/` (whole folders), compares the names with the same folders in the working tree (`src/superclaude/commands`, `agents`, `skills`, plus the root `skills/` folder that `install_skill.list_available_skills` also scans), keeps the names that are no longer shipped, and takes the sha256 of each file's content at the tag (`git show <tag>:<path>`). It renders `src/superclaude/cli/install_retired_data.py` deterministically (sorted names, sorted paths) and `--check` exits 1 when the file on disk differs from the rendering. Expose pure functions `generate(repo, tags)` and `render(data)` so tests can call them on a throwaway repo.

Acceptance criteria:
- `uv run python scripts/gen_retired_install_data.py --tag v5.0.0 --check` exits 0 after Task 2 and exits 1 when one hash in the data file is altered.
- A repeated run produces byte-identical output.
- The docstring says the next release passes its own previous tag (and may pass several `--tag` values to keep older names), and names the ceiling: only names shipped at a given tag can be retired.

## Task 2: Generate the data module from the v5.0.0 tag

Depends on: Task 1

Run the generator to create `src/superclaude/cli/install_retired_data.py`: header saying it is generated and by which command, `SOURCE_TAGS = ("v5.0.0",)`, `RETIRED_COMMANDS` (name to sha256 tuple), `RETIRED_AGENTS` (empty), `RETIRED_SKILLS` (name to relative path to sha256 tuple). Verify the names with `git ls-tree` first: commands build, cli-portify, improve, index-repo, index, load, review-translation, roadmap, save, spawn, tasklist, validate-roadmap (12); skills sc-cli-portify-protocol, sc-review-translation-protocol, sc-roadmap-protocol, sc-tasklist-protocol, sc-validate-roadmap-protocol (5, 21 files); agents none.

Acceptance criteria:
- The data file lists exactly those 12 commands and 5 skills and no agent; no name from swarm appears.
- Every hash is 64 lowercase hex characters.

## Phase 2: The retire step and its wiring

## Task 3: Add the retire module

Depends on: Task 2

Create `src/superclaude/cli/install_retired_files.py`, modeled on `src/superclaude/cli/install_retired_mcp.py` (module docstring, `Finding`, classify then act, one plain line per item). `run_retire_files_step(commands_dir: Path | None = None) -> dict[str, str]` uses `~/.claude/commands/sc` (or `commands_dir`, the `--target` value), `~/.claude/skills` and `~/.claude/agents`. A command or agent is removed only when it is a regular file (not a symlink) whose sha256 is in the data. A skill folder is removed only when it is a real folder and every entry in it is a regular file listed in the data with a matching hash and no other entry (extra file, extra folder, symlink) exists; removal unlinks the proven files (hash re-read right before) and then `rmdir`s the folders, so a late extra file stops it. Anything else is kept with one line that gives the reason and the exact `rm` or `rm -r` command with the quoted path. Names are used only if they match a simple safe-name pattern and are not currently shipped (`list_available_commands`, `list_available_agents`, `list_available_skills`). Nothing outside the three folders is touched. Per-item `OSError` is printed and recorded, never raised. When nothing is present it prints one "No retired commands, skills or agents present." line; a second run prints that and changes nothing. Missing `~/.claude` is safe.

Acceptance criteria:
- A byte-identical 5.0.0 command, a fully provable skill folder and a provable agent are removed; an edited command, a skill folder with an extra file, a symlink, and an unrelated file next to them are kept and untouched.
- Each kept item prints the reason and the removal command.
- No exception escapes `run_retire_files_step` for permission or missing-folder errors.

## Task 4: Call the step from install and update

Depends on: Task 3

Edit `src/superclaude/cli/main.py`: in `install` add "Step 10" right after the MCP retire step (`main.py:255-267`) and before the exit-code check (`main.py:269-280`), in the same `try/except` shape that prints "Retire step skipped (<ExceptionType>); install is complete." and never touches the exit code; pass `target_path`. In `update` run the same step after user setup and before the MCP notice (`main.py:407-415`), also non-fatal. Add one sentence to the `install` and `update` docstrings (`--help` text). `update.sh` needs no change because it runs `superclaude install --force`.

Acceptance criteria:
- `superclaude install`, `superclaude install --force` and `superclaude update` all run the step; a step that raises still leaves the exit code unchanged (`tests/cli/test_install_retired_mcp.py` exit-code tests still pass).
- `superclaude install --list` and `tests/cli/test_help_examples.py` still pass.

## Phase 3: Launch-level guard follow-up

## Task 5: Remove improve from the guard classifier

Edit `src/superclaude/hooks/scripts/launch-level-guard.sh:409` and its tracked copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh:409` to `implement | task | cleanup)` and drop the trailing comment. In `tests/hooks/test_launch_level_guard.py` remove `"sc:improve"` and its comment from `IMPL_SPELLINGS` (lines 918-920) and add `"sc:improve"` to the look-alike names in `test_lookalike_skill_names_stay_none` (line 936). Leave `_REMOVED_COMMAND_TEXT` alone. Run `make sync-dev` for the `.claude/hooks/` mirror. Evidence for the PR body: the guard sees names only through the `Skill` tool branch and releases only on `/sc:implement` or `/task`; the 5.0.0 `improve.md` has no Skill activation and no skill named `improve` ever shipped, so a kept customized copy reaches the guard the same way `spawn` and `build` already do.

Acceptance criteria:
- `uv run pytest tests/hooks -q` passes and `make verify-sync` is green.
- `grep -rn improve` over both guard scripts prints nothing.

## Phase 4: Tests

## Task 6: Add static, generator and module tests

Depends on: Task 4

Create `tests/cli/test_install_retired_files.py` with: shape checks on `install_retired_data` (every name absent from `src/superclaude/{commands,skills,agents}` and the root `skills/` folder, every hash 64 hex, safe names, no swarm name); generator tests on a throwaway git repo built in `tmp_path` with its own tag (rendering, sorted output, `--check`), which need no `v5.0.0` tag; classifier tests on a throwaway HOME for each keep reason (edited file, extra file in a skill, extra empty folder, symlink, unlisted name, unrelated files). Tests that need the `v5.0.0` tag skip with a clear reason when it is missing.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_retired_files.py -q` passes without the tag present for every test except the tag-dependent ones, which skip with a reason.

## Task 7: Add the upgrade-from-5.0.0 test

Depends on: Task 6

In `tests/cli/test_install_retired_files.py`, build an installed 5.0.0 state in a throwaway HOME from `git archive v5.0.0 src/superclaude/commands src/superclaude/skills src/superclaude/agents` (copy commands except `README.md`, whole skill folders, agents), add a customized copy of one retired command, a retired skill folder with an extra file, an unrelated file in `commands/sc/` and in `skills/`, and run `superclaude install` and `superclaude update` through `CliRunner` with the framework installers and the codegraph phase stubbed as `_stub_framework` does in `tests/cli/test_install_retired_mcp.py`. Assert: the 11 untouched commands and 4 untouched skills are gone while the customized command and the extra-file skill are kept with reason and removal command; unrelated files untouched; kept 6.0.0 items present; a second run changes nothing and prints "No retired"; exit code equals the run without the step (0, and 1 when a stubbed installer fails); a step that raises prints "Retire step skipped" and keeps the exit code. Also a test that the step also honors `--target`.

Acceptance criteria:
- The upgrade test fails on the code before Task 3 and 4 (record both runs in `.dev/issues/v6-retire-step/`) and passes after.
- A manual run: lay the `v5.0.0` files into a throwaway HOME, run `superclaude install`, list what remains under `commands/sc/` and `skills/`, then run `superclaude doctor` with that HOME.

## Phase 5: Documentation

## Task 8: Document the step for users

Depends on: Task 4

Edit `docs/getting-started/upgrading.md` (qualify "The installer never deletes files" near line 229 and add a short 6.0.0 section: what is removed, the proof rule, what is kept and printed, how to remove a kept item, that `install`, `install --force` and `update` run it) and `docs/getting-started/installation.md` (one paragraph near lines 54-70 and the options table near line 283). Do not add a CHANGELOG entry or release notes.

Acceptance criteria:
- Both pages name the 12 commands and 5 skills or point to `install_retired_data.py`, and state that unprovable files are kept.
- `git diff --check` is clean and no historical record is changed.

## Task 9: Document the step for maintainers

Depends on: Task 4

Edit `docs/developer-guide/technical-architecture.md` (install order, add the new step), `docs/developer-guide/release-procedure.md` (release preparation: regenerate the data with `scripts/gen_retired_install_data.py --tag <previous tag>` and commit it) and `docs/developer-guide/codegraph-integration.md` (refresh the `main.py:` line citations at lines 64-67 and 101 that the new step shifts).

Acceptance criteria:
- Every `main.py:NNN` citation in `codegraph-integration.md` points at the code it names after the edit (checked by opening each range).
- The release procedure names the generator command.
