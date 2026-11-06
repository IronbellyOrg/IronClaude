# Explanation: src/superclaude/cli/install_core.py

Level: basic. Format: text. Source read in full (156 lines) on 2026-11-05.

## What this file does

It copies SuperClaude's "core" instruction files (plain `.md` documents such as `CLAUDE.md`, `RULES.md`, `HOW-WE-WORK.md`) from the package into the user's `~/.claude/` folder, where Claude Code reads them at startup. It is one step of `superclaude install` and `superclaude update`.

## The pieces

**`KNOWN_CORE_FILES`** (line 13). A fixed set of 12 file names this version ships. It is used only by `list_installed_core_files`, so that listing `~/.claude/` does not report unrelated `.md` files the user keeps there.

**`install_core_files(target_path=None, force=False)`** (line 31). The main function. It returns a pair: `(True or False, message text)`.
1. Target defaults to `~/.claude`; the folder is created if missing (lines 47-55).
2. It finds the source folder with `_get_core_source()` and lists every `*.md` file in it, sorted (line 57).
3. For each file: if the destination already exists and `force` is off, the file is skipped and left untouched. Otherwise it is copied with `shutil.copy2`, which keeps timestamps (lines 66-77). A copy error is recorded and the loop continues.
4. It builds a report with three optional groups (installed, skipped, failed) and the install directory (lines 79-101).
5. Success is true only when nothing failed (line 103). Skipped files do not count as failure.

**`_get_core_source()`** (line 107). Returns the `core/` folder next to the `cli/` folder, that is `src/superclaude/core/` in a checkout or the installed package's `core/` folder under pipx or pip. Its docstring lists two locations, but the code checks one path and returns it either way; if it is missing, `install_core_files` reports "Core source directory not found".

**`list_core_files()`** (line 129). The names of the `.md` files shipped in the package.

**`list_installed_core_files()`** (line 144). The shipped-name files that are present in `~/.claude/`. It always looks in `~/.claude`, even if `install_core_files` was given a different `target_path`.

## Who uses it

Production callers, in `src/superclaude/cli/main.py` (call lines read and confirmed):
- `install` command, line 178: `install_core_files(force=force)`. Existing files are kept unless the user passes `--force`.
- `update` command, line 365: `install_core_files(force=True)`. Always overwrites.
- The list view, lines 89-90, uses `list_core_files()` and `list_installed_core_files()`.

Tests that pin its behaviour: `tests/cli/test_how_we_work_install.py` (including a check that `KNOWN_CORE_FILES` equals the shipped set, line 44), `tests/cli/test_bash_inspection_policy.py`, `tests/cli/test_issue_body_templates.py`, `tests/unit/test_cli_install.py`.

## Things worth knowing

- Safe by default: a plain install never overwrites a file you edited. Only `update` (or `--force`) does.
- Files in `~/.claude/` that SuperClaude does not ship are never removed or changed.
- Adding a new core `.md` file to `src/superclaude/core/` also requires adding its name to `KNOWN_CORE_FILES`; otherwise it installs but is not listed as installed, and the test at `tests/cli/test_how_we_work_install.py:44` fails.
- A run where every file already exists returns success with only a "skipped" message.

## How this was checked

Source read directly. Codegraph index was fresh (0 pending changes) and gave the caller and callee lists; the `main.py` call lines were then confirmed with a text search. Not run: the install itself (read-only explanation).
