---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-design-20261126-042509
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Save edited core files, agents and templates before install --force and update overwrite them (issue 676)

Source: ./source.md
Goal: `superclaude install --force` and `superclaude update` save a core file, agent or template that differs from the shipped one as `<name>.bak.<UTC stamp>` next to it before overwriting it, as they already do for commands, rules and output styles; a save that fails leaves the file untouched and the command exits 1; `install --list` does not count the copies as installed templates; every statement that says these files are overwritten with no copy is corrected; tests prove each behaviour.

## Constraints

- Scope: change only `src/superclaude/cli/install_core.py`, `install_agents.py`, `install_templates.py` (and the docstring of `install_keep.py`), tests under `tests/cli/`, the documentation files named in the tasks, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (the routing-guide copy) and `CHANGELOG.md`. Do not change `src/superclaude/cli/main.py`. Do not change the logic of `backup_if_differs`, `same_content` or `_backup_target`. Add no shared helper function and no code that deletes backups.
- Non-goals: no stale-file notes for agents and templates on a plain `install` (recorded as a follow-up), no change to skill-folder or hook-script copying, no rollback of a failed replacement, no change to `README.md:68` (a 6.0.0 section pinned to `@v6.0.0`), no change to released CHANGELOG entries, `docs/testing/`, `docs/designs/` or `docs/docs-product/`.
- Never edit or stage a path under `.claude/` (those are mirrors made by `make sync-dev`); edit the file under `src/superclaude/` or `plugins/` instead.
- Line numbers in the tasks are as at HEAD 3cf7e2259; locate by the quoted text if an earlier task shifted them.
- The helper contract (unchanged): `backup_if_differs(shipped: Path, target: Path) -> Path | None` in `src/superclaude/cli/install_keep.py` returns `None` when the bytes match, otherwise copies `target` to `<name>.bak.<YYYYmmddTHHMMSSZ>` beside it (a `-2`, `-3` suffix while that name exists) and returns that path; it raises `OSError` when the copy fails, and the caller must then leave `target` untouched.
- Exact strings every installer uses. Saved block, printed only when `backed_up` is non-empty, after the skipped and kept notes and before the failed block: the text `\n💾 Saved {n} changed {noun}(s) before overwriting:` and then one line `   - {backup path}` per saved copy; nouns are `core file`, `agent`, `template`. Failure line, added to `failed`: `<key>: could not save a copy first, left untouched (<error>)`.
- Pattern to copy for the code tasks: `src/superclaude/cli/install_commands.py` lines 54-82 (the backup step with its own `try`/`except OSError`, then the copy `try`) and 108-113 (the saved block).
- Terms: the six backed-up categories are commands, rules, output styles, core files, agents and templates. Skill folders (deleted and re-copied) and hook scripts (`src/superclaude/cli/install_hooks.py:286-287`, a plain `shutil.copy2`) are overwritten with no copy. The word "excluded" names the `agent-memory` folder the template installer never writes.
- Documentation wording kit (use the pieces the task names; keep the wording the same in every file). W-1: "`superclaude install --force` and `superclaude update` overwrite every file they ship. When a command, rule, output-style, core, agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders (deleted and re-copied) and hook scripts get no copy." W-2: "Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either command." W-3: "Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy." W-4: "`could not save a copy first, left untouched`: the installer could not write the `.bak.` copy next to a file, because the folder is not writable or the disk is full. That file is left as it is, the run lists it under the failed files, and `superclaude install --force` or `superclaude update` exits 1. Make the folder writable or free space and run the command again, or move the file aside yourself. A `.bak.` file left behind by a failed save may be incomplete."
- Test conventions: run tests with `uv run pytest`; never `python -m` or bare `pip`. Unit tests live in `tests/cli/test_install_keep.py` (existing helpers `_baks` at line 32 and `_rewrite_keeping_stat` at line 39; existing failed-save tests at lines 144-157 and 202-214 patch `install_keep.shutil.copy2`, which is the same `shutil` module the installers call).

## Phase 1: Core files are saved before a forced overwrite

## Task 1: Save a differing core file before a forced overwrite in install_core_files

In `src/superclaude/cli/install_core.py`, function `install_core_files(target_path, force)` (line 33):

- Extend the import at line 12 to `from .install_keep import backup_if_differs, same_content`.
- Add `backed_up = []` beside `installed`, `skipped` and `failed` (lines 64-66).
- In the loop over `core_files`, between the skip path (`if dest_file.exists() and not force:` ... `continue`, ending at line 73) and the `try:` at line 75, add the backup step: when `dest_file.exists()`, inside its own `try`, call `backup_if_differs(src_file, dest_file)`; append a returned path to `backed_up` as `str(path)`; on `OSError as e` append `f"{src_file.name}: could not save a copy first, left untouched ({e})"` to `failed` and `continue`. The backup call must not sit inside the existing `try`/`except Exception` that wraps `shutil.copy2`, which stays unchanged.
- Print the saved block (see Constraints, noun `core file`) after the whole `if skipped:` block (it ends at line 106) and before `if failed:` (line 108). It must sit outside `if skipped:`: a forced run has no skipped files, so a block inside it would never print.
- In the kept-file note at lines 101-104, change `(run with --force or `superclaude update` to refresh):` to `(run with --force or `superclaude update` to refresh; a differing file is saved as <name>.bak.<time> first):`, the words used at `install_commands.py:101-103`.
- Leave `KNOWN_CORE_FILES`, `_get_core_source`, `list_core_files` and `list_installed_core_files` unchanged. The return stays `success = len(failed) == 0`.

Acceptance criteria:
- `install_core_files(target_path=t, force=True)` over an existing `t/RULES.md` whose bytes differ from the shipped file leaves `t/RULES.md` equal to the shipped bytes, leaves exactly one `t/RULES.md.bak.<stamp>` holding the old bytes, and the returned message contains `Saved 1 changed core file(s) before overwriting:` and that backup path, after the skipped and kept notes and before any `Failed` block.
- The same call with a byte-identical `RULES.md`, or into an empty target, makes no backup and the message has no `Saved`.
- `force=False` writes nothing and makes no backup; for a differing kept file the message contains `a differing file is saved as <name>.bak.<time> first`.
- When the backup copy raises `OSError`, that file's bytes are unchanged, `failed` holds `RULES.md: could not save a copy first, left untouched (<error>)`, the function returns `False`, and the other core files in the same run are still installed.
- `uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py tests/cli/test_bash_inspection_policy.py tests/cli/test_install_failures.py tests/unit/test_cli_install.py -q` passes: these are the existing callers of `install_core_files`, and each runs without force or force-installs into an empty target.

## Task 2: Add the installer-row test scaffold and the core-row tests to tests/cli/test_install_keep.py

Depends on: Task 1

In `tests/cli/test_install_keep.py` add a section parametrized by one row table, the pattern of `_INSTALLERS` in `tests/unit/test_cli_install.py:993-1005`. Each row is a pytest param with an id, the installer function, a target factory (`tmp_path` based), a victim picker and a noun. This task adds only the `core` row: call `install_core_files(target_path=t, force=f)`, target `tmp_path / ".claude"`, victim the first `*.md` in the target, noun `core file`. Write the table so that Tasks 4 and 7 add a row without changing a test.

Add these helpers, local to the section:

- `_victim_baks(victim)` returns `sorted(victim.parent.glob(victim.name + ".bak.*"))`, so a stray file in the folder cannot change a count.
- `_edit(victim)` writes `b"my own edit\n"` and returns the shipped bytes read beforehand.
- `_wrap_copy(monkeypatch, victim, fail_on, error)` replaces `install_keep.shutil.copy2` with a wrapper around the real function; it records every destination and raises `error` when `fail_on(dst)` is true. Provide two predicates: backup-only (`dst.name.startswith(victim.name + ".bak.")`) and replacement-only (`dst == victim`).
- `_freeze_clock(monkeypatch)` replaces `install_keep.datetime` with a stub whose `now(tz)` returns one fixed instant.

Add these tests, each run for every row (add `import errno` and the needed imports):

- `test_forced_install_saves_a_differing_file_then_replaces_it` (TR-001): after installing into the target, edit the victim, install again with `force=True`; the victim equals the shipped bytes, `_victim_baks` holds exactly the edited bytes, and the message contains `Saved 1 changed <noun>` and the backup path.
- `test_forced_install_of_a_matching_or_missing_file_makes_no_backup` (TR-002): a forced run over matching files, and a forced run into an empty target, succeed with no backup and no `Saved`.
- `test_a_second_forced_run_makes_no_further_backup` (TR-003): backup count stays 1.
- `test_plain_install_keeps_the_edit_and_makes_no_backup` (TR-004): bytes kept, no backup; the core message contains `differ from this version`.
- `test_core_kept_note_names_the_bak_naming` (TR-005, core row only): the message of a plain install over an edited victim contains `saved as <name>.bak.<time> first`.
- `test_failed_save_leaves_the_file_untouched` (TR-006), parametrized over `PermissionError("denied")` and `OSError(errno.ENOSPC, "No space left on device")`: use the backup-only predicate; assert the result is not ok, the message contains `<key>: could not save a copy first, left untouched` and the error text, the victim bytes are unchanged, the recorded copies to the victim number zero, and a second edited file in the same target is saved and replaced.
- `test_save_then_failed_replacement_keeps_the_backup` (TR-007): use the replacement-only predicate (the backup copy goes through); assert not ok, the backup holds the edited bytes and its path is in the saved block, and the victim is listed under `❌ Failed`; assert nothing about the victim's bytes.
- `test_backup_names_do_not_collide_on_one_instant` (TR-009): with the frozen clock, edit, force, edit, force; the second backup name ends in `-2` and each backup holds its own edit.
- `test_same_size_same_mtime_edit_is_saved_when_forced` (TR-010): rewrite the victim with `_rewrite_keeping_stat` to the same size and mtime, then force; a backup exists.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_keep.py -q` passes with the new tests present for the `core` row and the existing tests in the file unchanged.
- TR-006 asserts the `left untouched` wording and zero copies to the victim, so a missing `except OSError` guard in Task 1 fails it.
- Adding a row to the table is the only change needed to run every test for another installer (the table is the single place a row is defined).

## Phase 2: Agents are saved before a forced overwrite

## Task 3: Save a differing agent file before a forced overwrite in install_agents

In `src/superclaude/cli/install_agents.py`, function `install_agents(target_path, force)` (line 15):

- Add `from .install_keep import backup_if_differs` after the imports at lines 7-9.
- Add `backed_up = []` beside `installed`, `skipped` and `failed` (lines 43-45).
- In the loop over `agent_files`, between the skip path (ending at line 53) and the `try:` at line 55, add the backup step as in Task 1: when `target_file.exists()`, in its own `try`, call `backup_if_differs(agent_file, target_file)`; append a returned path to `backed_up` as `str(path)`; on `OSError as e` append `f"{agent_name}: could not save a copy first, left untouched ({e})"` to `failed` and `continue` (`agent_name` is the stem set at line 49). The existing `try`/`except Exception` around `shutil.copy2` stays unchanged and does not contain the backup call.
- Print the saved block (noun `agent`) after the skipped block (lines 68-73) and before the failed block (line 75).
- Add no kept-but-different note; leave `list_available_agents`, `list_installed_agents` and `_EXCLUDE_FILES` unchanged.

Acceptance criteria:
- `install_agents(target_path=t, force=True)` over an edited `t/<agent>.md` leaves the shipped bytes in `t/<agent>.md`, exactly one `t/<agent>.md.bak.<stamp>` with the old bytes, and a message containing `Saved 1 changed agent(s) before overwriting:` and the path.
- A byte-identical file, an empty target, and `force=False` make no backup; a failed backup leaves the agent's bytes unchanged, lists `<agent>: could not save a copy first, left untouched (<error>)` under `❌ Failed to install`, returns `False`, and still installs the other agents.
- `list_installed_agents()` does not list `<agent>.md.bak.<stamp>` (it globs `*.md`), and `README.md` stays excluded.
- `uv run pytest tests/cli/test_install_failures.py tests/troubleshoot/test_diagnostic_worker_contract.py tests/unit/test_cli_install.py -q` passes: these are the existing callers of `install_agents` and each force-installs into an empty target or runs without force.

## Task 4: Add the agents row to the installer-row test table

Depends on: Task 2, Task 3

In `tests/cli/test_install_keep.py` add the `agents` row to the table of Task 2: call `install_agents(target_path=t, force=f)` (add `from superclaude.cli.install_agents import install_agents`), target `tmp_path / "agents"`, victim the first `*.md` in that folder, noun `agent`. Do not change any test body except where a row-specific assertion is needed: TR-005 stays core-only, and in `test_plain_install_keeps_the_edit_and_makes_no_backup` the agents message must contain no `differ` text (agents get no kept-but-different note).

Acceptance criteria:
- `uv run pytest tests/cli/test_install_keep.py -q` passes with TR-001 to TR-004, TR-006, TR-007, TR-009 and TR-010 running for the `agents` row.
- The backup of an agent is named `<agent>.md.bak.<stamp>` and is found by `_victim_baks`.
- The `core` row results are unchanged.

## Phase 3: Templates are saved before a forced overwrite and the listing ignores the copies

## Task 5: Save a differing template file before a forced overwrite in install_templates

In `src/superclaude/cli/install_templates.py`, function `install_templates(target_path, force)` (line 30):

- Add `from .install_keep import backup_if_differs` after line 22 (`from typing import List, Tuple`).
- Add `backed_up: List[str] = []` beside `installed`, `skipped` and `failed` (lines 54-56).
- In the loop over the sorted source files, after the excluded-folder skip (`if any(p in _PROTECTED_TARGET_SUBDIRS for p in rel.parts): continue`, lines 67-68), after `dest = target_path / rel` (line 70) and the skip path (`if dest.exists() and not force:` ... `continue`, lines 71-73), and before the `try:` at line 74, add the backup step: when `dest.exists()`, in its own `try`, call `backup_if_differs(src_file, dest)`; append a returned path to `backed_up` as `str(path)`; on `OSError as e` append `f"{rel}: could not save a copy first, left untouched ({e})"` to `failed` and `continue`. The existing `try` (which holds `dest.parent.mkdir` and `shutil.copy2`) and its `except Exception` stay unchanged; no new `mkdir` is needed because a backup exists only when `dest` exists.
- Print the saved block (noun `template`) after the skipped block (lines 86-91) and before the failed block (line 92).
- Add no kept-but-different note.

Acceptance criteria:
- `install_templates(target_path=t, force=True)` over an edited nested template such as `t/workflow/<file>` leaves the shipped bytes in it, exactly one `t/workflow/<file>.bak.<stamp>` in the same subfolder with the old bytes, and a message containing `Saved 1 changed template(s) before overwriting:` and the path.
- A file seeded under `t/agent-memory/` keeps its bytes and gets no backup; a byte-identical template, an empty target and `force=False` make no backup.
- A failed backup leaves the template unchanged, lists `<rel>: could not save a copy first, left untouched (<error>)` under `❌ Failed to install`, returns `False`, and the other templates are still installed.
- `uv run pytest tests/cli/test_install_failures.py tests/unit/test_cli_install.py -q` passes: the existing callers of `install_templates` run without force or force-install into an empty target.

## Task 6: Make list_installed_templates ignore backup files

In `src/superclaude/cli/install_templates.py`, function `list_installed_templates()` (line 145), add one more condition to the comprehension filter (lines 150-156), next to `f.is_file()`, `"__pycache__" not in f.parts` and the `_PROTECTED_TARGET_SUBDIRS` check: `".bak." not in f.name`. Do not filter on the `.md` suffix, because a non-`.md` template ships (`modularization-template-review/synthetic-dnsp-finding.contract`). Leave `list_available_templates()` unchanged.

Acceptance criteria:
- With `Path.home` patched to a temporary folder holding the installed templates plus an extra `workflow/<file>.bak.20261126T000000Z` and a `workflow/<file>.bak.20261126T000000Z-2`, `list_installed_templates()` omits both and its length equals `len(list_available_templates())`.
- A non-`.md` shipped template such as `synthetic-dnsp-finding.contract` is still listed as installed after a normal install.
- `install --list` (`src/superclaude/cli/main.py` lines 143-155, the only caller of `list_installed_templates`) prints `Templates: N available, N installed` with equal N for an isolated home that holds only shipped templates and their backups.
- The consumer inventory still holds: `grep -rnE 'rglob\("\*"\)|glob\("\*"\)|iterdir\(|os\.walk\(' src tests` shows no hit that reads the agents folder, the templates folder or the `~/.claude/` root without a filter, other than `list_installed_templates` with the new condition. Other readers match `*.md`, known names or exact names: `install_agents.py` line 141, `install_core.py` line 171, `doctor.py` line 315, `src/superclaude/cli/recommend/prompts.py` line 135 and `install_retired_files.py` line 201. A grep cannot see a pattern built at runtime or the host's own loader; say so in the task's notes if a new reader turns up.

## Task 7: Add the templates row and the template, listing and shipped-name tests

Depends on: Task 2, Task 4, Task 5, Task 6

In `tests/cli/test_install_keep.py` add the `templates` row to the table: call `install_templates(target_path=t, force=f)` (add the import), target `tmp_path / "templates"`, victim the first file under `workflow/`, noun `template`. In `test_plain_install_keeps_the_edit_and_makes_no_backup` the templates message must contain no `differ` text. Add these tests:

- `test_empty_and_binary_content_is_saved_exactly` (TR-008, templates row): set the victim to `b""`, force, then to bytes containing `\x00` and `\xff`, force; each backup equals those bytes.
- `test_nested_template_backup_and_excluded_folder` (TR-011, templates row): the backup sits in the victim's own subfolder; a file seeded under `<target>/agent-memory/` keeps its bytes and gets no backup after a forced run.
- `test_listings_ignore_backups` (TR-012): patch `Path.home` to `tmp_path` (as `tests/cli/test_how_we_work_install.py:33` does for the core listing); install core files, agents and templates with `force=True` into the home layout, then seed `.bak.` files (one with a `-2` suffix) in `~/.claude/templates/workflow/`, `~/.claude/agents/` and `~/.claude/`; `list_installed_templates()` omits them and equals `list_available_templates()` in length, and `list_installed_agents()` and `list_installed_core_files()` omit theirs.
- `test_no_shipped_template_name_contains_bak` (TR-013): no name in `list_available_templates()` contains `.bak.`.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_keep.py tests/unit/test_cli_install.py tests/cli/test_how_we_work_install.py -q` passes, with TR-001 to TR-004, TR-006, TR-007, TR-009 and TR-010 running for the `templates` row and TR-008, TR-011, TR-012 and TR-013 present.
- TR-012 fails if the filter of Task 6 is removed.

## Phase 4: Command-level tests for install and update

## Task 8: Add the install --list count and the install-then-update happy-path tests to tests/cli/test_update_command.py

Depends on: Task 1, Task 3, Task 5, Task 6

In `tests/cli/test_update_command.py` (existing fixtures: the autouse `isolated_home_guard` at line 34, which pins HOME and `CLAUDE_CONFIG_DIR` under `tmp_path`; `native_install` at line 188, which runs a real `install --target <home>/.claude/commands/sc` and returns `(home, target)`; the existing real update call at line 240 is `CliRunner().invoke(main, ["update", "--target", str(target)])`) add:

- A test for TR-014: after `native_install`, edit one template under `<home>/.claude/templates/workflow/`, call `install_templates(force=True)` directly (with `Path.home` patched as `native_install` does), then `CliRunner().invoke(main, ["install", "--list"])` with the listings not stubbed; the output contains `Templates: N available, N installed` with equal N and the listing writes no file. The count check holds only in this isolated home.
- A test for TR-015: after `native_install`, edit `<home>/.claude/RULES.md`, one `<home>/.claude/agents/*.md` and one template. Run `install` with no force: exit code 0, the three edits kept, and no `<victim>.bak.*` file. Then run `update --target <target>`: exit code 0 and exactly one `<victim>.bak.*` beside each victim holding the edited bytes. Count with `sorted(victim.parent.glob(victim.name + ".bak.*"))` per victim, never with the folder-wide `_baks(~/.claude)`, because the hook installer writes `settings.json.bak.<stamp>` in `~/.claude/` on every run (`src/superclaude/cli/install_hooks.py:336-346`).

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py -q` passes with both tests present.
- Both tests isolate core files, agents and templates through the pinned HOME, not through `--target` (which redirects only the commands installer, as `test_install_force_target_do_not_redirect` at line 255 pins).
- The existing tests in the file are unchanged.

## Task 9: Add the stub-row and forwarded-flag tests for install --force and update

In `tests/cli/test_update_command.py`, add a recording variant of `_stub_installers` (line 74; the existing `fake` at lines 80-84 ignores keyword arguments) that stores the `force` keyword each fake installer receives. Add a test for TR-016, parametrized over `failing` in `install_core_files`, `install_agents`, `install_templates` and over the command `["install", "--force"]` and `["update"]`: the exit code is 1 and `"<name> result"` appears in the output (the pattern of `test_update_propagates_hook_install_failure` at line 118). Add assertions on the forwarded flag: with `["install"]` the three installers receive `force=False`; with `["install", "--force"]` and `["update"]` they receive `force=True`.

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py -q` passes with the new tests present.
- A change of `main.py` that stopped forwarding the flag (`main.py:180,198,229` for `install`, `383,396,417` for `update`) would fail the forwarded-flag assertions.
- The existing `_stub_installers` helper and its callers are unchanged.

## Task 10: Add the real failed-save update test and run the full install-related test set

Depends on: Task 1, Task 8

In `tests/cli/test_update_command.py` add the test for TR-017: after `native_install`, edit `<home>/.claude/RULES.md`; replace `shutil.copy2` with a wrapper around the real function that raises `OSError` only when the destination name starts with `RULES.md.bak.`; run `CliRunner().invoke(main, ["update", "--target", str(target)])`. Assert exit code 1; the output contains `RULES.md: could not save a copy first, left untouched`; the output contains exactly one `❌ Failed`; the victim's bytes are unchanged. Because only the victim's backup is failed, the hooks phase still writes its own `settings.json.bak.<stamp>`, so exit code 1 can come only from the new guard.

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py -q` passes with the test present.
- `uv run pytest tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q` passes.
- `uv run pytest tests/cli tests/unit -q` passes.

## Phase 5: Documentation, docstring and changelog

## Task 11: Update the install_keep.py module docstring to name the covered and uncovered categories

In `src/superclaude/cli/install_keep.py` replace the module docstring at lines 1-8 with: "Helpers for installers that keep or overwrite files a user may have edited. `install` keeps an existing file, so a kept file that differs from this version's copy is stale or customized and should be named in the report. `install --force` and `update` overwrite, so the commands, rules, output-styles, core, agent and template installers first save a differing file next to itself (`<name>.bak.<UTC stamp>`, which Claude Code does not load) and skip the overwrite when that save fails. Skill folders and hook scripts do not use this helper: they are overwritten with no copy." Wrap it as a normal triple-quoted docstring in the file's existing style.

Acceptance criteria:
- `git diff -- src/superclaude/cli/install_keep.py` shows one hunk, the docstring; `same_content`, `_backup_target`, `backup_if_differs` and the imports are unchanged.
- `uv run pytest tests/cli/test_install_keep.py -q` passes.

## Task 12: Correct the routing guide sentence and copy it to the plugin twin

In `src/superclaude/core/HOW-WE-WORK.md` line 3, replace the sentence that starts "`superclaude install --force` and `superclaude update` both overwrite every file they ship, including an edited `~/.claude/CLAUDE.md`, and keep no backup." through "...Copy any file you changed or added before you run either one." (this includes the sentence about deleting and re-copying each shipped skill folder) with W-1 followed by W-2 from the Constraints. Keep the rest of line 3 (the text before it about `superclaude install --force` refreshing the guide, and the text after it starting "Plugin installs ship only some of these commands and skills") exactly as it is. Then make `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` a byte-for-byte copy of the edited source file (for example with `cp`). Change nothing in the level-table block, the routing-table block or any other line.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- `git diff -- src/superclaude/core/HOW-WE-WORK.md` shows only line 3 changed; the text "keep no backup" no longer appears in either file.
- `uv run pytest tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/cli/test_how_we_work_install.py tests/commands/test_worktrees_command.py -q` passes (the last one reads both copies of the guide and asserts that other sentences are absent).

## Task 13: Correct the user guide pages docs/user-guide/how-we-work.md and docs/user-guide/flags.md

Depends on: Task 12

- In `docs/user-guide/how-we-work.md` line 3, the sentence "...a command, rule or output-style file that differs from the shipped one is first saved as `<name>.bak.<UTC time>`; an edited core file such as `~/.claude/CLAUDE.md`, an agent or a skill is overwritten with no copy. They also delete and re-copy each shipped skill folder in `~/.claude/skills/`, so any file you add..." becomes the same rule as W-1 and W-2 in its own prose: the six backed-up categories are saved first, skill folders and hook scripts get no copy, and the advice names skill files and hook scripts.
- In `docs/user-guide/flags.md` line 233 (the `--force` row), replace "it saves a differing command, rule or output-style file as `<name>.bak.<UTC time>` first, overwrites edited core files and agents without a copy, and re-copies skill folders" with W-1 in the row's compact style: the six categories are saved first, skill folders are re-copied, and hook scripts are overwritten with no copy.

Acceptance criteria:
- Neither file says that core files, agents or templates are overwritten with no copy; both name skill folders and hook scripts as the files that get no copy.
- The `--force` table row in `flags.md` still has its other cells and column count unchanged.
- `grep -nE "no copy|without a copy|no backup" docs/user-guide/how-we-work.md docs/user-guide/flags.md` prints only lines about skill folders or hook scripts.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/commands/test_worktrees_command.py -q` passes: the first pins another sentence in `docs/user-guide/flags.md` (the pr-submit late re-sync sentence), so only the `--force` row may change there.

## Task 14: Rewrite the onboarding deck card at docs/onboarding/ironclaude-onboarding.html:510

Depends on: Task 12

At line 510 the card `<div class="card"><h3><code>superclaude update</code> overwrites</h3><p>It overwrites every file it ships, including an edited <code>~/.claude/CLAUDE.md</code>, keeps no backup, and deletes and re-copies each shipped skill folder...` becomes plain sentences with the W-1 rule: every file it ships is overwritten; a command, rule, output-style, core, agent or template file that differs is first saved as `<name>.bak.<UTC time>`; skill folders are deleted and re-copied and hook scripts are overwritten with no copy, so copy any skill file or hook script you changed or added before you run it. Keep `superclaude update` in the heading `<code>`; do not put a `/command` or `--flag` token inside a `<code>` element unless `src/superclaude/core/HOW-WE-WORK.md` states that same token, because `tests/docs/test_onboarding_deck.py` (lines 83-87) fails on any token the guide lacks.

Acceptance criteria:
- `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
- The card names the saved copy as `<name>.bak.<UTC time>` and names skill folders and hook scripts as the files with no copy; the words "keeps no backup" no longer appear in the file.
- The rest of the HTML file is unchanged.

## Task 15: Correct docs/reference/troubleshooting.md and add the failed-save entry

Depends on: Task 12

At lines 159-161 (under "Reset Installation") replace "It saves a differing command, rule or output-style file as `<name>.bak.<UTC time>` first; edited core files, agents and skills get no copy, so copy those first." with W-1 and W-2. Directly after that paragraph add a short entry that uses W-4 verbatim (the message, the cause, the fix, the exit code 1 and the note that a `.bak.` copy left by a failed save may be incomplete). Leave the sentence "There is no uninstall command." and the rest of the file unchanged.

Acceptance criteria:
- The paragraph no longer says edited core files or agents get no copy; it names skill folders and hook scripts.
- The new entry contains the exact message `could not save a copy first, left untouched` and states that `superclaude install --force` and `superclaude update` exit 1.
- No restore command in the file uses `ls -t ... | head -1` for these backup files.

## Task 16: Correct docs/getting-started/installation.md lines 644 and 646

Depends on: Task 12

- Line 644: the sentence that says a plain `superclaude install` "names each kept command, rule and output-style file that differs from this version" also names core files (the core installer already does, `src/superclaude/cli/install_core.py:95-106`). Agents and templates are not added.
- Line 646, the "Warning" paragraph: replace the text "Core files such as `~/.claude/CLAUDE.md` and `~/.claude/RULES.md`, agents and skills are overwritten with no copy, and each shipped skill folder ... is deleted and re-copied, so any file you added inside one is lost. If you edited or added any of those files, copy them first (for example `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine`), then re-apply your changes after the upgrade." with W-1 and W-2, and change the `cp` example so it copies a file added inside a skill folder to a path outside `~/.claude/skills/`. Keep the rest of the paragraph (the codegraph phase, exit code 1 note and the link to the saved-copies section) unchanged.

Acceptance criteria:
- Line 646 names skill folders and hook scripts as the files overwritten with no copy and contains no `cp` example that targets `CLAUDE.md`.
- The link `upgrading.md#saved-copies-of-changed-files` is unchanged and still resolves to the section edited in Task 18.
- No other line of `installation.md` changes.

## Task 17: Correct the backup table and the upgrade steps in docs/getting-started/upgrading.md (lines 43-56 and 99-103)

Depends on: Task 12

- Lines 43-56 (Step 1 "Back up files you edited"): the two-row table becomes: row one lists commands (`commands/sc/`), rules (`rules/`), output styles (`output-styles/`), core files, agents (`agents/`) and templates (`templates/`) as saved next to the file as `<name>.bak.<UTC time>` before the overwrite, with W-3 stating that 6.1.0 and earlier overwrite core files, agents and templates with no copy; row two lists skill folders (`skills/`, deleted and copied again, so a file added inside one is lost) and hook scripts as overwritten with no copy. The `settings.json` row is unchanged. The `cp` example that copies `CLAUDE.md` and `RULES.md` and the sentence "Copy anything you changed in the second row first" change to W-2 with an example that copies a file from a skill folder to a path outside `~/.claude/skills/`.
- Lines 99-103 ("What the upgrade does", step 1): "A command, rule or output-style file that differs from the shipped one is saved as `<name>.bak.<UTC time>` first." lists the six categories and carries W-3.

Acceptance criteria:
- `upgrading.md` lines 43-56 and 99-103 no longer say that core files or agents are overwritten with no copy for this version, and keep the 6.1.0 qualifier.
- The page title (line 1, 6.0.0) and the `@v6.0.0` pin (lines 65-66) are unchanged.
- The table keeps its two columns and the `settings.json` row.

## Task 18: Correct the "Saved copies of changed files" section of docs/getting-started/upgrading.md (lines 335-364)

Depends on: Task 17

Edit the section that starts "### Saved copies of changed files":

- The lead names the six categories: command, rule, output-style, core file, agent and template.
- "Why so many": every forced upgrade saves each file whose shipped bytes changed, edited or not, and the newest copy may be an older shipped version rather than your edit, so read the copies before restoring.
- "Not loaded": the copy ends in a time stamp, not in `.md`, so Claude Code does not load it as a command, agent or core file.
- "Not covered": skill folders and hook scripts are overwritten without a copy (the sentence that wraps over two lines near line 349 is rewritten).
- "If a copy cannot be saved": `superclaude install --force` or `superclaude update` prints that file as a failure and exits 1 (it currently says only `superclaude install`); add the cause and fix from W-4.
- "Nothing deletes them": the two `find` commands become `find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles ~/.claude/agents ~/.claude/templates -name '*.bak.*'` and `find ~/.claude -maxdepth 1 -name '*.md.bak.*'`, each with its `-delete` form. The root search uses `*.md.bak.*`, never `*.bak.*`, because `settings.json.bak.<timestamp>` lives there and is a separate file the installer writes on every run.

Acceptance criteria:
- The section names the six categories, says skill folders and hook scripts are not covered, and has no `ls -t ... | head -1` restore advice.
- The `find` commands match the two shown above, with the `-maxdepth 1 -name '*.md.bak.*'` form for the `~/.claude` root and no `*.bak.*` search of the root.
- The heading "Saved copies of changed files" is unchanged, so the anchor `#saved-copies-of-changed-files` still works.

## Task 19: Correct the no-backup statements in the supervised-orchestration architecture reference

Depends on: Task 12, Task 13, Task 14, Task 15, Task 16, Task 17, Task 18

In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`:

- Section 5.6 item 1, at line 1239 (the paragraph that says the installers overwrite files "in place and delete and re-copy each installed skill directory, with no backup (`install_core.py:70-75`, `install_commands.py:55-61`, `install_agents.py:51-56`, `install_templates...`"): name the six categories as saved first as `<name>.bak.<UTC time>` and name only skill folders and hook scripts as written with no backup; keep the marketplace-catalog clause ("One more file is written with no backup and without `force`: the pinned catalog...") and the clause about deleting an installed skill folder.
- At the lines that say "...overwrite the shipped files they copy with no backup, apart from the exceptions listed in Section 5.6 item 1" (lines 325, 1292, 1581, 1624, 1840, 1841, 1844 and 1847; the wording differs slightly in each), change the claim to say that only skill folders and hook scripts are overwritten with no backup, and keep the pointer to Section 5.6 item 1.
- Do not edit lines 196 and 1321 (they say "no copy the worker reads", which is unrelated).

Acceptance criteria:
- `grep -rnE "no copy|no backup|keeps? no backup|without a copy" docs src/superclaude/core plugins`, ignoring paths under `docs/testing/`, `docs/designs/` and `docs/docs-product/`, leaves only these hits: lines that name skill folders, hook scripts or the marketplace catalog as written with no copy or backup; architecture reference lines 196 and 1321 and the catalog clause at line 1239; and `plugins/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py:5`. The grep reads one line at a time, so also read each documentation row of Tasks 13 to 18 for a phrase wrapped over two lines.
- `git diff --stat` shows no change to `README.md` or to released CHANGELOG entries.

## Task 20: Add the CHANGELOG entry and confirm the whole change is limited to its scope

Depends on: Task 10, Task 19

In `CHANGELOG.md`, under `## [Unreleased]` (line 5), add one entry above the existing first entry, in the file's style (a `###` heading naming the change and issue, then a bullet): heading "Installers: core files, agents and templates are saved before `--force` and `update` overwrite them (issue 676)"; bullet "`superclaude install --force` and `superclaude update` now save a core file, agent or template that differs from the shipped one as `<name>.bak.<UTC time>` next to it, as they already did for commands, rules and output styles. A save that fails leaves that file as it was, lists it as failed and makes the command exit 1. `install --list` no longer counts these copies as installed templates. Skill folders and hook scripts are still overwritten with no copy. Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy."

Acceptance criteria:
- The `[Unreleased]` section has exactly this one new entry and no released entry changed.
- `grep -n "backup_if_differs(" src/superclaude/cli/*.py` shows exactly five call sites besides the definition: `install_commands.py`, `install_user_setup.py`, `install_core.py`, `install_agents.py` and `install_templates.py`.
- `git diff --stat` shows no change to `src/superclaude/cli/main.py`, and `git diff -- src/superclaude/cli/install_keep.py` shows only the docstring hunk.
- The changed files are only the three installers, `install_keep.py`, `tests/cli/test_install_keep.py`, `tests/cli/test_update_command.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `CHANGELOG.md` and the documentation files named in Tasks 13 to 19; no path under `.claude/` is staged.
- `uv run pytest tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q` and `uv run pytest tests/cli tests/unit -q` pass, `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/commands/test_worktrees_command.py -q` passes (both read `CHANGELOG.md` or the guide copies and pin text other than this entry), and `make verify-sync` passes.
