---
title: "Design: backup before overwrite for the core, agent and template installers"
issue: 676
type: component
format: spec
status: ready-for-planning
input: .dev/brainstorms/20261126-031739-installer-backups/merged-requirements.md
---

# Design: backup before overwrite for the core, agent and template installers (issue 676)

Grounding: index_state: fresh (checked_at 2026-11-26T04:20:06Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/issue-676); codegraph tools used: codegraph_status, codegraph_files, codegraph_callers (backup_if_differs, install_core_files, install_agents, install_templates, list_installed_templates), codegraph_impact (list_installed_templates), codegraph_search (same_content). Caller rows are leads at their definition line; every call site cited below was confirmed by Read. No graph:* token.

Terms and ids follow the requirements document (`merged-requirements.md`): FR-xxx requirement, TR-xxx test, AC-x acceptance criterion, R-x risk, FU-x follow-up. Line numbers are as at HEAD 3cf7e2259; re-locate by text if edits shift them.

## 1. Overview and design decisions

**Goal.** `superclaude install --force` and `superclaude update` save an edited core file, agent or template as `<name>.bak.<UTC stamp>` before overwriting it, the way commands, rules and output styles already do. The owner decided this (issue summary, "Decided for this work (iteration 3)"). A save that fails leaves the file untouched and the command exits 1.

**Shape of the change.** Three small guarded blocks, one per installer, copied from the pattern in `install_commands.py:65-75`; one filter in `list_installed_templates`; one docstring edit; documentation, CHANGELOG and tests. No new function, no change to `backup_if_differs`, no change to `main.py` (FR-006, AC-2).

| ID | Decision | Why | Requirement |
|---|---|---|---|
| D-1 | Inline block in each installer; no shared function | The keys differ (`src_file.name`, `agent_name`, `rel`); a helper for three sites beside two inline sites leaves two shapes. Extraction is FU-2 | FR-001, Q3 |
| D-2 | The backup call has its own `try/except OSError` placed before the existing generic `try` | The generic `except Exception` would turn a failed save into a plain copy error and lose "left untouched" | FR-061 |
| D-3 | The saved block is printed after the skipped and stale notes and before the failed block; in core it sits outside `if skipped:` | A forced run has no skipped files, so a block inside `if skipped:` never prints | FR-011, FR-040 |
| D-4 | `list_installed_templates` drops names containing `.bak.`; agents and core listings are unchanged | Only the templates lister reads every file (`rglob("*")`); the others already match `*.md` or known names | FR-050, FR-052 |
| D-5 | No stale-file notes for agents and templates on a plain `install` | The owner decision covers backups; those installers have no byte comparison today | Q1, FU-1 |
| D-6 | One "common wording" sentence drives every documentation row | Many files state the old rule; one wording keeps them consistent and gives one grep | requirements section 5 |
| D-7 | Tests use one installer-row table; failure tests fail only the victim's backup | A global copy failure can pass without the guard; the row table adds a fourth installer as one row | TR-001..TR-018 |
| D-8 | A backup that was saved stays on disk and listed even if the replacement then fails | The user keeps the old bytes either way; no rollback is attempted | FR-063 |

## 2. Verified structure and impact

**Components.** All installers live in `src/superclaude/cli/` (15 `install_*.py` files indexed). The ones this change touches or copies from:

| Component | Symbol (signature) | Role today | Change |
|---|---|---|---|
| `install_keep.py` | `same_content(a: Path, b: Path) -> bool` (18); `backup_if_differs(shipped: Path, target: Path) -> Path \| None` (40) | Byte compare; saves `target` as `<name>.bak.<stamp>`, with `-2`.. on a name clash; returns `None` for a match; raises `OSError` when the copy fails | Docstring lines 1-8 only |
| `install_core.py` | `install_core_files(target_path=None, force=False)` (33) | Copies shipped `*.md`; reports kept files that differ | Backup block, saved block, kept-note clause, import |
| `install_agents.py` | `install_agents(target_path=None, force=False)` (15) | Copies shipped `*.md` except `README.md` | Backup block, saved block, import |
| `install_templates.py` | `install_templates(target_path=None, force=False)` (30); `list_installed_templates()` (145) | Copies shipped files, skips `agent-memory` and `__pycache__` | Backup block, saved block, import, listing filter |
| `install_commands.py` | `install_commands` (16) | Already backs up (lines 54-82 and 108-113) | None; it is the model |
| `install_user_setup.py` | `_copy_tree` (87) | Already backs up rules and output styles | None |
| `main.py` | `install` (46), `update` (356) | Call the installers | None |

**Call graph (graph rows; call sites confirmed by Read).**

- `backup_if_differs`: 2 production callers (`_copy_tree`, `install_commands`) plus tests; after this change 5 (AC-1).
- `install_core_files`: `install` (`main.py:180`), `update` (`main.py:383`) and 9 test functions. `install_agents`: `main.py:198`, `396` and 2 test functions. `install_templates`: `main.py:229`, `417` and 1 test function. There are no other production callers, so the behaviour change reaches users only through the two commands.
- `list_installed_templates`: one caller, `install` (`main.py:144`); blast radius 2 symbols (itself and `install`). The count line at `main.py:153-155` is the only visible effect.

**Existing tests that call the three installers (regression watch list).** Each was read; none reaches the new branch, because each force-installs into an empty target or runs without force:

| Test | Call | Why it stays green |
|---|---|---|
| `tests/cli/test_how_we_work_install.py:28`, `80` | `force=True`, empty target; `80` seeds only unshipped retired files | Nothing shipped exists in the target, so no save |
| `tests/cli/test_how_we_work_install.py:54`, `102`, `118` | `force=False` | The skip path is unchanged |
| `tests/cli/test_bash_inspection_policy.py:36` | `force=True`, empty target | As above |
| `tests/cli/test_issue_body_templates.py:27` | `force=False`, empty target | As above |
| `tests/cli/test_install_keep.py:69` | default `force=False` | As above |
| `tests/troubleshoot/test_diagnostic_worker_contract.py:411` | default `force=False`, empty target | As above |
| `tests/unit/test_cli_install.py:916`, `932`, `958` (rows of `_INSTALLERS`, run at `1005`) | `force=True`, empty target | As above; also the model for the new row table |
| `tests/cli/test_update_command.py` stub tests | installers replaced by `_stub_installers` | The real installers are not called |

**Validated names.** Loop variables: core `src_file`, `dest_file`; agents `agent_file`, `target_file`, `agent_name`; templates `src_file`, `rel`, `dest`. Accumulators in all three: `installed`, `skipped`, `failed`. `backed_up` is new. The failure line uses the same key as the installer's existing failure entry.

## 3. Component design

### 3.1 Behaviour per file (the same for core, agents and templates)

| Target exists | `force` | Bytes equal | Backup call | Copy | Result in the report |
|---|---|---|---|---|---|
| no | any | n/a | not called (FR-002) | runs | installed |
| yes | False | n/a | not called (FR-005) | not attempted | skipped; core also names it as kept-but-different when it differs |
| yes | True | yes | returns `None` (FR-003) | runs (rewrites the same bytes) | installed; no saved line |
| yes | True | no | saves the old bytes, returns the path | runs and succeeds | installed; saved line with the path |
| yes | True | no | raises `OSError` | not attempted (FR-060) | failed: `<key>: could not save a copy first, left untouched (<error>)`; not counted installed |
| yes | True | no | saves, returns the path | runs and fails | saved line with the path and a failed line `<key>: <error>`; installer returns False (FR-063) |
| yes | True | unreadable | `same_content` is False, so a save is attempted and fails on the unreadable file | not attempted | failed, as the row above (fails closed) |

The installer returns `success = len(failed) == 0` as today (core 118, agents 85, templates 102). `main.py:285-296` and `449-461` turn a False into exit code 1 (FR-064).

### 3.2 Order of steps inside each loop iteration

1. Compute the key and target path (unchanged).
2. Skip path: `exists() and not force` records a skip and continues (unchanged, stays first).
3. Backup step (new): when the target exists, call `backup_if_differs(<shipped file>, <target>)` inside its own `try`; a returned path is appended to `backed_up` as `str(path)`; an `OSError` appends the failure line to `failed` and continues to the next file.
4. Copy step (unchanged): the existing `try` with `copy2` and the generic `except` that records `<key>: <error>`.

The backup step must precede the generic `try` and must not sit inside it. In templates the `dest.parent.mkdir` stays inside the copy `try` (a backup exists only when `dest` exists, so its parent exists: FR-031).

### 3.3 Per-installer deltas

| | `install_core.py` | `install_agents.py` | `install_templates.py` |
|---|---|---|---|
| Import | line 12 becomes `backup_if_differs, same_content` | new `from .install_keep import backup_if_differs` after line 9 | new `from .install_keep import backup_if_differs` after line 22 |
| New list | `backed_up = []` beside `installed`, `skipped`, `failed` (64-66) | beside the same three (43-45) | beside the same three (54-56) |
| Backup step goes | between the skip path (ends 73) and the `try` at 75 | between the skip path (ends 53) and the `try` at 55 | after the excluded-folder skip (67-68) and the skip path (71-73), before the `try` at 74 |
| Key in the failure line | `src_file.name` | `agent_name` (the stem, line 49) | `str(rel)` (as line 79 does) |
| Noun | `core file` | `agent` | `template` |
| Saved block goes | after the `if skipped:` block (ends 106), before `if failed:` (108); never inside `if skipped:` | after the skipped block (68-73), before the failed block (75) | after the skipped block (86-91), before the failed block (92) |
| Backup lands | beside the file in the target root | beside the file as `<agent>.md.bak.<stamp>` | beside the file in its own subfolder (`with_name`, `install_keep.py:32`) |
| Also | the kept-note clause (3.4) | none | `list_installed_templates` filter (3.6) |
| Unchanged | `list_installed_core_files` (known names, `*.md`) | `list_installed_agents` (`*.md`, 141) | `list_available_templates`, the `agent-memory` skip, the empty-tree sentinel (97-98) |

### 3.4 Report layout

Block order in every installer: installed, skipped, (core only: kept-but-different note, inside skipped), **saved**, failed, directory line. The saved block is printed only when `backed_up` is non-empty, exactly:

```
\n💾 Saved {n} changed {noun}(s) before overwriting:
   - {backup path}
```

with the nouns `core file`, `agent`, `template` (FR-040). The `✅ Installed` and `⚠️  Skipped` lines do not change; a forced overwrite still counts as installed (FR-042). Example, `update` after the user edited `RULES.md`:

```
✅ Installed 12 core framework files:
   - ...
💾 Saved 1 changed core file(s) before overwriting:
   - /home/u/.claude/RULES.md.bak.20261126T041500Z

📁 Installation directory: /home/u/.claude
```

Example, a failed save:

```
❌ Failed to install 1 files:
   - RULES.md: could not save a copy first, left untouched ([Errno 28] No space left on device)
```

Core's kept-note (lines 101-104) gains the clause used by `install_commands.py:101-103`: `(run with --force or \`superclaude update\` to refresh; a differing file is saved as <name>.bak.<time> first):`. Agents and templates get no kept-but-different note (D-5, FU-1).

### 3.5 Failure semantics

| Failure | Target bytes | Backup on disk | Counted installed | Returned | Exit code |
|---|---|---|---|---|---|
| Save raises `OSError` (folder not writable, disk full, unreadable file) | unchanged | possibly a partial copy (R-3) | no | False | 1 |
| Save works, copy fails | possibly partly written (no rollback) | complete, listed | no | False | 1 |
| Any other file in the same run | processed normally (FR-062) | as per row | yes | unchanged | unchanged |
| Directory at the target path (R-10) | untouched | none | no | False | 1 |

Two behaviours are new for users and are documented (FR-065, R-14): a folder the user cannot write to, with writable files in it, used to be overwritten in place and now fails; and a full disk now fails at the save instead of at the copy.

### 3.6 Template listing

`list_installed_templates` keeps its three existing conditions (a regular file, no `__pycache__`, no `agent-memory` part) and adds a fourth: the file's base name does not contain `.bak.` (`".bak." not in f.name`). A `.md` test is wrong because a non-`.md` template ships (`modularization-template-review/synthetic-dnsp-finding.contract`). `list_available_templates` does not change; a test pins that no shipped name contains `.bak.` (TR-013) so the filter can never hide a real template. Consumer check (FR-052): the only unfiltered reader of the agents folder, the templates folder or the `~/.claude/` root is `list_installed_templates`; the readers that match `*.md`, known names or exact names are `install_agents.py:141`, `install_core.py:171`, `doctor.py:315`, `recommend/prompts.py:135` and the retire step (`install_retired_files.py:201`).

### 3.7 `install_keep.py` docstring

Replace lines 1-8 with a docstring that names the categories. Proposed text:

> Helpers for installers that keep or overwrite files a user may have edited. `install` keeps an existing file, so a kept file that differs from this version's copy is stale or customized and should be named in the report. `install --force` and `update` overwrite, so the commands, rules, output-styles, core, agent and template installers first save a differing file next to itself (`<name>.bak.<UTC stamp>`, which Claude Code does not load) and skip the overwrite when that save fails. Skill folders and hook scripts do not use this helper: they are overwritten with no copy.

The docstring may grow by a line or two; the check (AC-2) is that the only hunk in `install_keep.py` is the docstring.

## 4. Documentation design

One docs commit carries every row (Q4). Each row reuses a piece of this wording kit, so a grep finds one rule stated one way.

### 4.1 Wording kit

- **W-1 (the rule).** "`superclaude install --force` and `superclaude update` overwrite every file they ship. When a command, rule, output-style, core, agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders (deleted and re-copied) and hook scripts get no copy."
- **W-2 (the advice).** "Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either command." A copy inside `~/.claude/skills/` that holds a `SKILL.md` would load as a skill (R-6).
- **W-3 (the version qualifier).** "Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy." Used only where a page is a 6.0.0 upgrade page (`upgrading.md`).
- **W-4 (the failure entry).** "`could not save a copy first, left untouched`: the installer could not write the `.bak.` copy next to a file, because the folder is not writable or the disk is full. That file is left as it is, the run lists it under the failed files, and `superclaude install --force` or `superclaude update` exits 1. Make the folder writable or free space and run the command again, or move the file aside yourself. A `.bak.` file left behind by a failed save may be incomplete."
- **W-5 (the onboarding card).** Plain sentences with no `/command` and no `--flag` token inside `<code>` beyond what `HOW-WE-WORK.md` states, because `tests/docs/test_onboarding_deck.py:83-87` fails on any token the guide lacks. The card keeps `superclaude update` and names the saved copy as `<name>.bak.<UTC time>`.

### 4.2 File map

| File:line | Edit | Wording |
|---|---|---|
| `src/superclaude/core/HOW-WE-WORK.md:3` | Replace "…and keep no backup…Copy any file you changed or added before you run either one" with W-1 and W-2; keep the rest of the line (retire/plugin sentences) | W-1, W-2 |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:3` | Byte-for-byte copy of the edited source file, same commit; `diff` of the two files prints nothing (AC-5, `tests/commands/test_routing_plugin_parity.py:38`) | copy |
| `docs/user-guide/how-we-work.md:3` | Same rule in its own prose | W-1, W-2 |
| `docs/user-guide/flags.md:233` | In the `--force` row: six categories saved first, skill folders re-copied, hook scripts overwritten with no copy | W-1 |
| `docs/reference/troubleshooting.md:159-161` | Replace the "edited core files, agents and skills get no copy" sentence; add the failure entry right after it | W-1, W-2, W-4 |
| `docs/onboarding/ironclaude-onboarding.html:510` | Rewrite the card paragraph | W-5 |
| `docs/getting-started/installation.md:644` | Kept-file naming adds core files (already named by core) | none |
| `docs/getting-started/installation.md:646` | Replace the warning; the `cp` example copies a file added inside a skill folder to a path outside `~/.claude/skills/` | W-1, W-2 |
| `docs/getting-started/upgrading.md:43-56` | Row 1 gains core files, agents and templates with W-3; row 2 becomes skill folders and hook scripts; the `cp` example as above | W-1, W-2, W-3 |
| `docs/getting-started/upgrading.md:99-103` | Add the three kinds | W-1, W-3 |
| `docs/getting-started/upgrading.md:335-364` | Six kinds in the "Saved copies" lead; "Why so many": each forced upgrade saves every changed file and the newest copy may be an older shipped version, so read the copies before restoring; "Not loaded": agents and core files too; "Not covered": skill folders and hook scripts; failure bullet (353-354): "`install --force` or `update` exits 1" plus W-4; the `find` commands below | W-1, W-4 |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1239` | Section 5.6 item 1: name the six categories as saved first, skill folders and hook scripts as written with no backup; keep the marketplace-catalog clause | W-1 |
| Same file, lines 325, 1292, 1581, 1624, 1840, 1841, 1844, 1847 | "…with no backup, apart from the exceptions listed in Section 5.6 item 1" now says only skill folders and hook scripts are overwritten with no backup, and still points to item 1 | short form of W-1 |
| `src/superclaude/cli/install_keep.py:1-8` | Docstring of 3.7 | none |
| `CHANGELOG.md:5` (`[Unreleased]`) | One new entry (4.4) | none |

Not edited: `README.md:68` (under "Upgrading to 6.0.0", pinned to `@v6.0.0`), released CHANGELOG entries, `docs/testing/`, `docs/designs/`, `docs/docs-product/`. The `.claude/` mirrors come from `make sync-dev` and are never staged.

The `find` commands in `upgrading.md` become:

```bash
find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles ~/.claude/agents ~/.claude/templates -name '*.bak.*'
find ~/.claude -maxdepth 1 -name '*.md.bak.*'
```

each with its `-delete` form after "Nothing deletes them". The root search uses `*.md.bak.*`, never `*.bak.*`, because `settings.json.bak.<timestamp>` lives there (R-7). The "Why so many" bullet also says the newest copy is not always your edit (R-11); no page offers an `ls -t … | head -1` restore for these files.

### 4.3 Constraints that bind the edits

- The two routing-guide copies stay identical (AC-5); the level-table block of `src/superclaude/core/CLAUDE.md` is unaffected because line 3 is outside it.
- The onboarding card obeys W-5.
- The documentation grep (AC-4) is line-based and cannot see a phrase wrapped over two lines (`upgrading.md:349-350`); each row of 4.2 is also checked by reading.

### 4.4 CHANGELOG entry (draft)

> ### Installers: core files, agents and templates are saved before `--force` and `update` overwrite them (issue 676)
>
> - `superclaude install --force` and `superclaude update` now save a core file, agent or template that differs from the shipped one as `<name>.bak.<UTC time>` next to it, as they already did for commands, rules and output styles. A save that fails leaves that file as it was, lists it as failed and makes the command exit 1. `install --list` no longer counts these copies as installed templates. Skill folders and hook scripts are still overwritten with no copy. Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy.

## 5. Test design

### 5.1 Unit tests: `tests/cli/test_install_keep.py`

The file already holds the commands and rules tests (109-214) and the helpers `_baks` (32) and `_rewrite_keeping_stat` (39). Add `install_agents` and `install_templates` imports (`install_core_files` is imported). The new section is parametrized by one row table, the pattern of `_INSTALLERS` in `tests/unit/test_cli_install.py:993-1005`:

| Row id | Call | Target (under `tmp_path`) | Victim | Noun in the message |
|---|---|---|---|---|
| `core` | `install_core_files(target_path=t, force=f)` | `.claude` | first `*.md` | `core file` |
| `agents` | `install_agents(target_path=t, force=f)` | `agents` | first `*.md` | `agent` |
| `templates` | `install_templates(target_path=t, force=f)` | `templates` | first file under `workflow/` | `template` |

Helpers (new, local to the section):

- `_victim_baks(victim)`: `sorted(victim.parent.glob(victim.name + ".bak.*"))`. Per-victim, so a stray file in the folder cannot change a count (R-7, INV-023).
- `_edit(victim)`: writes `b"my own edit\n"` and returns the shipped bytes read beforehand.
- `_wrap_copy(monkeypatch, victim, fail_on, error)`: replaces `install_keep.shutil.copy2` (the same module object the installers call) with a wrapper around the real function. It records every destination, and raises `error` when `fail_on(dst)` is true. Two ready predicates: backup-only (`dst.name.startswith(victim.name + ".bak.")`) and replacement-only (`dst == victim`). Failing only the victim's backup keeps other files processable, so "another file still processed" is checkable (TR-006).
- `_freeze_clock(monkeypatch)`: replaces `install_keep.datetime` with a stub whose `now(tz)` returns one fixed instant (TR-009).

| TR | Test (one function, parametrized over the rows unless noted) | Asserts |
|---|---|---|
| TR-001 | `test_forced_install_saves_a_differing_file_then_replaces_it` | victim bytes equal shipped; `_victim_baks` holds exactly the edited bytes; `Saved 1 changed <noun>` and the path in the message |
| TR-002 | `test_forced_install_of_a_matching_or_missing_file_makes_no_backup` | success; no backup; no `Saved`; includes forcing into an empty target |
| TR-003 | `test_a_second_forced_run_makes_no_further_backup` | backup count stays 1 |
| TR-004 | `test_plain_install_keeps_the_edit_and_makes_no_backup` | bytes kept; no backup; core message has `differ from this version`; agents and templates messages have no `differ` text |
| TR-005 | `test_core_kept_note_names_the_bak_naming` (core only) | message contains `saved as <name>.bak.<time> first` |
| TR-006 | `test_failed_save_leaves_the_file_untouched` (two errors: `PermissionError`, `OSError(errno.ENOSPC, ...)`) | `not ok`; `<key>: could not save a copy first, left untouched` and the error text in the message; victim bytes unchanged; recorded copies to the victim: 0; a second edited file in the same row is saved and replaced |
| TR-007 | `test_save_then_failed_replacement_keeps_the_backup` | `not ok`; backup holds the edited bytes and its path is in the saved block; the victim is under `❌ Failed`; no assertion on the victim's bytes |
| TR-008 | `test_empty_and_binary_content_is_saved_exactly` (templates row) | victim set to `b""`, then to bytes with `\x00` and `\xff`; each backup equals those bytes |
| TR-009 | `test_backup_names_do_not_collide_on_one_instant` | frozen clock; edit, force, edit, force: the second name ends in `-2`; each backup holds its own edit |
| TR-010 | `test_same_size_same_mtime_edit_is_saved_when_forced` | `_rewrite_keeping_stat` on the victim, then force: backup exists (extends 69-78 to forced runs) |
| TR-011 | `test_nested_template_backup_and_excluded_folder` (templates row) | the backup sits in the victim's subfolder; a file under `<target>/agent-memory/` keeps its bytes and gets no backup |
| TR-012 | `test_listings_ignore_backups` | `Path.home` patched to `tmp_path` (as `test_how_we_work_install.py:33`); seed `.bak.` files (one with `-2`) in `templates/workflow/`, `agents/` and the root: `list_installed_templates()` omits them and equals `list_available_templates()` in length; the agents and core listers omit theirs |
| TR-013 | `test_no_shipped_template_name_contains_bak` | no name in `list_available_templates()` contains `.bak.` |
| TR-014 | in `test_update_command.py`, see 5.2 | `install --list` count |

### 5.2 Entry-point tests: `tests/cli/test_update_command.py`

This file has the autouse `isolated_home_guard` (HOME and `CLAUDE_CONFIG_DIR` under `tmp_path`, plugins, browser, Orca and codegraph phases stubbed), `_stub_installers` (74-96), `_stub_listings` (153-166) and `native_install` (187-196).

- **TR-014** `install --list` with the listings not stubbed. After `native_install`, edit one template, call `install_templates(force=True)` directly (home patched), then `CliRunner().invoke(main, ["install", "--list"])`: the output contains `Templates: N available, N installed` with equal N, and no file is written. Isolated home only: on a real home user-added templates change the count (AC-3).
- **TR-015** Happy path. After `native_install`, edit `~/.claude/RULES.md`, one agent and one template. `install` (no force): exit 0, edits kept, no `<victim>.bak.*`. `update --target <target>` (the pattern at line 240): exit 0, exactly one `<victim>.bak.*` per victim with the edited bytes. Counted with `_victim_baks`, never `_baks(~/.claude)` (the hook installer writes `settings.json.bak.*` there on every run, `install_hooks.py:336-346`).
- **TR-016** Stub rows. A recording variant of `_stub_installers` stores the `force` keyword each fake receives (the existing fake ignores keywords, 80-84). Parametrize `failing` over `install_core_files`, `install_agents`, `install_templates` and the command over `["install", "--force"]` and `["update"]`: exit 1 and `"<name> result"` in the output. Assert the forwarded flag: `install` passes False; `install --force` and `update` pass True. Isolation comes from the pinned HOME, never from `--target`: `--target` redirects only the commands installer, and `test_install_force_target_do_not_redirect` (255-277) pins that, so core, agents and templates always write under HOME.
- **TR-017** One real failed-save `update`. After `native_install`, edit `RULES.md`; wrap `copy2` so only a destination named `RULES.md.bak.*` raises; run `update --target <target>`. Assert exit 1; the output has `RULES.md: could not save a copy first, left untouched` and exactly one `❌ Failed`; the victim's bytes are unchanged. The hooks phase still writes its `settings.json.bak.*`, so exit 1 can come only from the new guard.
- **TR-018** Unchanged and passing: the tests in the section 2 watch list, plus `tests/commands/test_routing_plugin_parity.py` and `tests/docs/test_onboarding_deck.py`.

### 5.3 Verification commands (AC-1..AC-9)

```bash
uv run pytest tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q
uv run pytest tests/cli tests/unit -q
grep -n "backup_if_differs(" src/superclaude/cli/*.py          # five call sites besides the definition
git diff --stat -- src/superclaude/cli/main.py                  # empty
diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md   # prints nothing
make verify-sync
```

The documentation grep of AC-4 and the consumer grep of AC-6 are run as written in the requirements; their exemptions are listed there.

## 6. Delivery plan

Estimate: about 8 hours (1 policy and scope check done, 3 code and docs, 3 tests, 1 review). Work packages in order; each is one commit on the feature branch (conventional commits), so each is individually revertable. Each installer's row is added to the test table together with its code.

| WP | Content | Files | Depends on | Gate before the next WP |
|---|---|---|---|---|
| WP-1 | Core: backup block, saved block outside `if skipped:`, kept-note clause, import; row table with the `core` row; helpers; TR-001..007, 009, 010 for `core` | `src/superclaude/cli/install_core.py`, `tests/cli/test_install_keep.py` | none | `uv run pytest tests/cli/test_install_keep.py tests/cli/test_how_we_work_install.py -q` |
| WP-2 | Agents: backup block, saved block, import; the `agents` row | `src/superclaude/cli/install_agents.py`, `tests/cli/test_install_keep.py` | WP-1 (helpers, table) | the same two files plus `tests/troubleshoot/test_diagnostic_worker_contract.py` |
| WP-3 | Templates: backup block before the `try`, saved block, import, listing filter; the `templates` row; TR-008, 011, 012, 013 | `src/superclaude/cli/install_templates.py`, `tests/cli/test_install_keep.py` | WP-1 | the same plus `tests/unit/test_cli_install.py` |
| WP-4 | Entry-point tests TR-014..017 | `tests/cli/test_update_command.py` | WP-1..3 | `uv run pytest tests/cli/test_update_command.py -q` |
| WP-5 | Documentation, docstring and CHANGELOG (section 4); the routing-guide copy | the rows of 4.2 | none (can run first) | `tests/commands/test_routing_plugin_parity.py`, `tests/docs/test_onboarding_deck.py`, the AC-4 grep, a reading check of each row |
| WP-6 | Full verification | none | WP-1..5 | AC-1..AC-9 commands (5.3), `make verify-sync`; nothing under `.claude/` staged |

Suggested messages: `feat(install): save an edited core file before --force and update overwrite it`, the same for agents and templates, `test(install): cover install and update entry points for saved copies`, `docs(install): say which files are saved before --force and update (#676)`.

## 7. Traceability

| Requirements | Design |
|---|---|
| FR-001..006 (common) | 1 (D-1, D-2), 3.1, 3.2, 3.3 |
| FR-010..013 (core), FR-020..021 (agents), FR-030..032 (templates) | 3.3, 3.4 |
| FR-040..042 (report) | 3.4 |
| FR-050..052 (listing, consumers) | 3.6 |
| FR-060..065 (failure) | 3.1, 3.5, 4.1 (W-4) |
| Section 5 documentation rows | 4.1, 4.2, 4.3, 4.4 |
| TR-001..013 | 5.1 |
| TR-014..018 | 5.2 |
| AC-1..AC-13 | 5.3, 6 |
| R-1..R-17 | R-3, 4, 7, 11, 14, 15 are answered in 3.5, 4.1 and 4.2; R-8 is accepted (single-user CLI); R-17 is the WP-6 gate |
| FU-1, FU-2 | 1 (D-1, D-5); not in this change |

## 8. Validation record and open items

**Checked against the code (read at HEAD).** `backup_if_differs` and `same_content` signatures and behaviour (`install_keep.py`); the loop variables, skip paths, `try` blocks and report blocks of the three installers; the pattern in `install_commands.py` and `install_user_setup.py:_copy_tree`; the callers (graph rows plus `main.py:180,198,229,383,396,417`); the exit handling (`main.py:285-296`, `449-461`); the listing and count lines (`main.py:142-155`); the existing tests of the section 2 watch list; the onboarding-deck rule; and the exact documentation lines of 4.2.

**Not verified by this design.**
- That the host does not load `<name>.md.bak.<stamp>` as an agent or core file: the helper's docstring states it and the file name ends in a stamp, not `.md`; no test can prove the host's loader (FR-052).
- That no reader built at runtime globs the agents, templates or `~/.claude/` folders unfiltered; AC-6 repeats the grep for `src/` and `tests/` only.
- That the test suite passes with the change: nothing was run; WP-6 runs it.
- Concurrent installers can pick the same backup name (R-8); accepted and out of scope.

**Correction to the requirements.** TR-016 of `merged-requirements.md` says no test passes `--force` with `--target` ("guarded", `test_update_command.py:255`). Reading that test shows it does combine them, with every installer stubbed, to pin that `--target` redirects only the commands installer. The design keeps the useful part: entry-point tests must isolate core, agents and templates through HOME (the autouse `isolated_home_guard` and `native_install` do), not through `--target`. Use this wording when `/sc:workflow` reads the requirements.

**Open items.** None needs a decision from the owner before implementation. The owner decision in the issue summary authorizes the behaviour change; stale-file notes for agents and templates (FU-1) and extracting one shared function (FU-2) are recorded follow-ups, not part of this change.

## Revision 1

- Replaces package: TASK-WF-design-20261126-042509 (archived under .dev/tasks/archive/TASK-WF-design-20261126-042509/)
- Review report: /home/coder/workspaces/worktrees/IronClaude/issue-676/.dev/reflect/pre-TASK-WF-design-20261126-042509-20261126043230/REPORT.md
- Fix map: ./artifacts/revision-log.md (diff: ./artifacts/plan.diff)
