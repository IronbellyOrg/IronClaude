---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-ccsessionHumanVs-20261118-150248
version: "1"
priority: Medium
created_date: "2026-11-18"
---

# ccsession: tell human-saved sessions from agent-saved ones, and keep them for different times

Source: ./source.md
Goal: ccsession records at save time whether a person chose a session name, hides agent-saved sessions in its lists unless asked, moves the installer's Claude Code retention target to 90 days, and gains `--classify`, `--mark` and a dry-run-by-default `--prune`, with a regression test for every rule of the source.

## Constraints

- Shell code in `src/superclaude/skills/ccsession-tag/ccsession`, `ccsession-orca` and `hooks/session-name.sh` stays Bash 3.2 safe (no associative arrays, no `mapfile`, no `${var,,}`), and listing code starts no new process per row: the marker is read with the `read` builtin.
- Every test runs in a temporary HOME (`tmp_path`) and reuses the helpers already in `tests/unit/test_ccsession_tag.py` (`_named_repo`, `_ccs`, `_hook`, `_listed`, `_add_session`, `_transcript`, `_orca_env`, `_orca_tty`, `_retention`, `_user_settings`). Nothing writes to the real `~/.claude` or `~/.local/state`.
- Nothing deletes a transcript or a name except `ccsession --prune --apply`: no environment variable, setting or hook turns it on, and no automatic trigger is added by this plan (the owner has not decided that yet). The prune code is written as plain functions with explicit arguments (projects folder, home, days, apply flag, current session id) so a later automatic trigger can call it unchanged.
- The `--auto-name` label format (`auto_name`, `ccsession` line 674) does not change: `cli/sweep/` recognises it.
- Resolved review follow-ups: the retention limit is read with `retention.py`'s own `managed_value()` and `read_object()` (managed settings, then user, then 30); an invalid `CCSESSION_AGENT_KEEP_DAYS` exits 2 and deletes nothing; the new helper is named `session_keep.py`.
- Edit only under `src/` and `tests/` and the repo-root `CHANGELOG.md`; the synced copies of the skill folder are produced by `make sync-dev`.

## Phase 1: Mark every session when its name is saved

## Task 1: Write the origin marker in `sync_name_locked` and add `ccsession --mark`

Edit `src/superclaude/skills/ccsession-tag/ccsession` (source sections R2.4 and R5.3). Next to `session_saved` (line 387) add `origin_file <list> <session>` (prints `<list>/.origin/<session>`), `read_origin <list> <session>` (prints `human`, `agent` or nothing, using the `read` builtin) and `write_origin <list> <session> <human|agent>` (writes a temporary file inside `<list>/.origin/` and `mv -f`s it into place, creating the folder with `mkdir -p`). In `sync_name_locked` (line 464, called by `sync_name` at line 406 while it holds `lock_list`) apply the R2.4 rule. `sync_name` and `sync_name_locked` take optional arguments given after a literal `--`: `--event <SessionStart|UserPromptSubmit|SessionEnd>`, `--source <startup|resume|clear|compact>` and `--origin <human|agent>`, parsed in the `--sync-name` dispatch (line 746); a marker is written only when `--event` is given, so `rename_dot_labels`, `import_claude_names` and every other caller write none, whatever `CCSESSION_ORIGIN` holds in the environment. There are exactly two writes. New-session write (the only place `agent` is written): `--event SessionStart`, `--source startup` and `--origin` all given and `read_origin` printed nothing: write the `--origin` value. Rename write: `--event UserPromptSubmit` or `SessionEnd` and the name is new for the session, meaning it is not already saved for it in this list (the loop at lines 469 to 476 finds a file of the same session, collision-suffixed files included) and no `<name_to_file name>.txt` or `<name_to_file name>-N.txt` in any list under the projects folder has this session id as its first line (checked only on this path): write `human`, replacing any marker; no `--origin` is needed. Everything else writes nothing (a SessionStart whose source is not `startup`, a name already saved for the session, a call without `--event`): a resume never writes a marker. The "already saved" check must look at the list as it was before this call's own write (the file is written at lines 477 to 482, so test for the session's name file before that write), or every rename would look already saved. The clean-up that removes older names (the `rm -f` loop at lines 483 to 490, `--keep-others`, `--check-others`) never decides a marker. In the fast-path `case` beside `--sync-name` (line 746) add `--mark <name> <agent|human>`: find the name file in this repo's list (`name_key`), read the session id from its first line, and call `write_origin` under `lock_list`; exit 1 when the name does not exist and exit 2 when the value is neither `agent` nor `human`. This command must not call `ensure_names_migrated`.

Acceptance criteria:
- New tests in `tests/unit/test_ccsession_tag.py` (a section headed "origin marker") show that `ccsession --sync-name <id> <name> -- --event SessionStart --source startup --origin agent` on a new session writes `.origin/<id>` holding `agent`, with `--origin human` writes `human`, and without `--event` writes no marker file even with `CCSESSION_ORIGIN=agent` in the environment (the import and dot-label paths).
- A table-driven test over event, source and origin (SessionStart with source `startup`, `resume`, `clear`, `compact` and none; UserPromptSubmit; SessionEnd; origin `agent`, `human`, none) shows `agent` is written only for SessionStart, `startup`, `agent`, and `human` only for SessionStart, `startup`, `human` or for a new name at UserPromptSubmit or SessionEnd, with or without `--origin`; a new name at UserPromptSubmit (no older name, or an older name in another repo's list) writes `human` over `agent`; the same name again changes nothing; a collision-suffixed own name in another list is not new; `--check-others` removing a duplicate name alone writes no marker.
- A session that has a name file and no marker (every pre-upgrade session) stays unmarked after a SessionStart with source `resume` and origin `agent` (a worker's `CCSESSION_NAME` equal to its saved name, or `/resume` inside an agent launch).
- `ccsession --mark <name> human` and `--mark <name> agent` change the marker; an unknown name exits 1; a bad value exits 2; the command writes nothing outside the list's `.origin` folder.
- The dependents keep working unchanged: `sync_name` callers in `rename_dot_labels`, `import_claude_names` (lines 514 and 517) and the `--sync-name` dispatch (line 746) still print the saved name; `migrate_names` still copies only `*.txt`; `scan_topics` and `list_sessions` (which glob `*.txt`) print identical output for a list that has an `.origin` folder and one that has not. The existing sync-name, migration and list tests still pass without edits.

## Task 2: Choose and export `CCSESSION_ORIGIN` in `ccsession-orca` and `ccsession`

Depends on: Task 1

Edit `src/superclaude/skills/ccsession-tag/ccsession-orca` (source sections R1 and R2.1). Export `CCSESSION_ORIGIN=human` only when the name came from the question (the `answer` of `ccsession --ask` with exit status 0 and a non-empty value, lines 204 to 207); export `agent` for an auto-name (lines 225 to 229), for `CCSESSION_NAME` (`name_from_env`, lines 195 to 196) and for a Claude `--name` or `-n` in the arguments (`name_carried`); on a resume (`resume_like`, line 58) and on the tab-reopen path (lines 164 to 190) run `unset CCSESSION_ORIGIN` before the `exec`. The export happens before each `exec "$CCSESSION"` (lines 186, 189, 247 and 249). Then edit `src/superclaude/skills/ccsession-tag/ccsession` (source section R2.2, launch path only: this code sits after the fast-path commands, so `--sync-name`, which Claude Code's hooks run with `CLAUDECODE=1` set (verified), never reaches it): directly after `CCSESSION_LAUNCH_ID` is exported (line 2175) set `CCSESSION_ORIGIN` to `agent` when `CLAUDECODE` is set, keep an incoming value that is exactly `human` or `agent`, otherwise use `human` when stdin and stdout are terminals and `agent` when they are not, and export it. The untagged-start branch (line 2182) needs no change.

Acceptance criteria:
- Tests that run `ccsession-orca` with the existing launch helpers (`_orca_tty`, `_orca_no_tty`, `_orca_env`) and a recording fake Claude show the `CCSESSION_ORIGIN` the Claude process receives: `human` for a name typed at the question, `agent` for Enter (auto-name), `agent` for `CCSESSION_NAME`, `agent` for `--name` in the arguments, and unset for `--resume`.
- A `ccsession <topic>` launched on a pseudo-terminal with no `CLAUDECODE` gives `human`; the same launch with `CLAUDECODE=1` or with no terminal gives `agent`; an incoming `CCSESSION_ORIGIN=agent` on a terminal stays `agent`.
- A tab reopen after a restart on a terminal (the existing `_tab_runs` helper) writes no marker and leaves an existing one as it is, because only a SessionStart with source `startup` writes one (checked end to end in Task 3's tests).
- `auto_name` output and the `--auto-name` tests (`_auto_name` helper) are unchanged.

## Task 3: Pass the origin on only for the launch owner in `hooks/session-name.sh`

Depends on: Task 1

Edit `src/superclaude/skills/ccsession-tag/hooks/session-name.sh` (source section R2.3). Directly after the `OWNER` test (the block that sets `OWNER=0` or `OWNER=1` and ends before the `CLAUDE_TOPIC` check) build the option list for `--sync-name`: read `source` from the payload in the `read_payload` Python block (which today reads session id, folder, event, name and reason) as one more NUL-ended field; when `OWNER` is 1 the call near the end of the file (the line that runs `"$_ccs" --sync-name "$SESSION_ID" "$NAME" $_check`) is followed by `-- --event "$EVENT"`, plus `--source "$SOURCE"` at SessionStart, plus `--origin "$CCSESSION_ORIGIN"` only when that variable is exactly `human` or `agent`; when `OWNER` is 0 it passes none of the three, so a Claude started inside a session never takes the outer origin. The literal `--` makes an older `ccsession`, which reads only its fourth argument as its keep flag, ignore the options. `OWNER` is also 1 for a Claude Code that ccsession did not start (no launch id), so a rename there writes `human` without any origin. The hook must not read `CLAUDECODE` (Claude Code sets it for every hook process, verified in the probe note under `.dev/research/ccsession-saved-sessions/`). Add a short comment that says why.

Acceptance criteria:
- Tests that drive the hook with the existing `_hook` helper show: an owner launch (`CCSESSION_LAUNCH_ID` equal to the firing Claude's parent id) with `CCSESSION_ORIGIN=agent` writes an `agent` marker at SessionStart with source `startup` and nothing with source `resume`; a non-owner launch with the same variables writes no marker.
- Every hook test in this task runs once more with `CLAUDECODE=1` in the hook's environment (the real condition) and gives the same result: a new session with origin `agent` still writes `agent`, with origin `human` writes `human`, and a rename at a prompt writes `human`.
- Rename outside ccsession: the hook with no launch id and no `CCSESSION_ORIGIN` (a plain `claude`, its `/resume` picker or the IDE), a new name at UserPromptSubmit over an existing `agent` marker writes `human`; the same name again writes nothing.
- B2: an unmarked saved session resumed by an agent launch (`ccsession-orca` with `CCSESSION_NAME` equal to its saved name), by `/resume` inside an agent launch and by a tab reopen stays unmarked and is still listed.
- B1 route 1: with `CCSESSION_AUTOSTART=0` through `ccsession-orca` (origin `agent` exported, no name, no marker), the hook at `UserPromptSubmit` with `session_title` `my-work` writes `human`.
- B1 route 2: a session saved under an auto-name in repo A's list (marker `agent`), then the hook at `UserPromptSubmit` with `cwd` in repo B's folder and a new title writes `human` in B's list and leaves A's list unchanged; the same title seen again from repo A's folder (already one of the session's names) writes nothing.
- A tab reopen on a terminal (origin `human` computed by `ccsession`) for a session that already has an `agent` marker leaves it `agent`; `/resume` inside a launched session (SessionStart, source `resume`) writes nothing; an `--auto-name` launch followed by `ccsession --mark <name> human` and then another hook call keeps `human`. What `/resume` inside a launched session does at a later prompt or at SessionEnd is a stated limit of the source (R2.4), not a tested guarantee.
- The existing hook tests (name sync at SessionStart, UserPromptSubmit and SessionEnd, Orca tab recording) still pass without edits.

## Phase 2: Findable lists

## Task 4: Hide agent rows in `list_sessions` and add `--agents` to `--list` and `--here`

Depends on: Task 1

Edit `src/superclaude/skills/ccsession-tag/ccsession` (source section R3.1 to R3.6). In `list_sessions` (line 1712), after the row's session id is known (`uuid`, line 1766) call `read_origin "$ws_dir" "$uuid"`; when it prints `agent` and `SHOW_AGENTS` is not 1, count the row in `hidden_n` and `continue` before any `place` or `stat_times` work, so a hidden row is neither listed nor counted in `other_n`. Print the list heading only when a visible row exists. At the end of the function print one dim line `N agent sessions hidden: <command>` (`ccsession --list --agents` for `--list`, `ccsession --here --agents` for `--here`, `type + to list them` for the new-tab question through `LIST_MORE_HINT`-style variable), and when every row of every list is hidden print that line instead of "No labeled sessions yet". Parse `--agents` in the `--list` branch (line 2070) and in the `--here` branch (line 2076), accepted before or after `--all`; `--all` keeps its meaning. Hiding is display only: `ccsession <name>`, `--rm` and `orca_tab_reopen` are not touched.

Acceptance criteria:
- New tests in `tests/unit/test_ccsession_tag.py` using `_add_session`, `_listed` and `_heading` show: with one `agent`, one `human` and one unmarked session, `--list` and `--here` print the human and unmarked rows and the line `1 agent sessions hidden: ccsession --list --agents` (or the `--here` form); `--agents` prints all three and no count line; `--here --all --agents` and `--here --agents --all` give the same output.
- A repo whose only sessions are `agent` prints no heading and the count line instead of "No labeled sessions yet"; a list with no markers prints exactly what it printed before this change (the existing list tests pass without edits).
- A hidden row is not counted in "N more sessions in other worktrees" (a session of another worktree marked `agent` leaves that count unchanged), and `ccsession <hidden name>` still resumes it.
- A timing test with 200 saved names confirms no new process per row (the existing performance test pattern near `_slow_probe`, line 2130, still passes).

## Task 5: Hide agent rows in the new-tab question and accept `+`

Depends on: Task 4

Edit `ask_session_name` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1869; source section R3.2). The inner function `show_saved` (line 1904) calls `list_sessions` with the hidden-count hint `type + to list them`; in the answer loop, directly after the existing `"*"` branch (line 1959) add a `"+"` branch that calls `show_saved` with `SHOW_AGENTS=1` for the worktree view and continues the loop. A name typed as `+` is therefore never a session name, as `*` already is.

Acceptance criteria:
- A pseudo-terminal test with the existing `_ask_on_pty` helper shows: the question lists the human and unmarked sessions, prints `N agent sessions hidden: type + to list them`, and typing `+` lists the agent sessions too and asks again; typing the name of a hidden session still resumes it.
- The existing question tests (name typed, Enter, `*`, paste, timeout) pass without edits.
- `list_sessions` callers stay consistent: `--list` (line 2072), `--here` (lines 2079 and 2081) and `show_saved` all print the same hidden-count line shape.

## Phase 3: Retention target 90

## Task 6: Move `retention.py` from 365 to 90 days and update its tests and text

Edit `src/superclaude/skills/ccsession-tag/retention.py` (source section R4): set `MIN_DAYS = 90` (line 57), rewrite the comment above it (the old reason, "a year keeps a named session through any normal pause", no longer holds), the module docstring (lines 1 to 40) and the advice strings in `check` and `ensure` so they name 90. `ensure` still raises an absent or lower value, keeps any value of 90 or more (a 365 stays 365), never writes where managed settings win and leaves an invalid file alone. Update the callers' text and tests: `src/superclaude/skills/ccsession-tag/install.sh` lines 174 to 177 (comment only), the retention comment in `src/superclaude/cli/install_ccsession.py` lines 100 to 104, `tests/unit/test_ccsession_tag.py` lines 4978 to 5173 and `_quiet_retention` (line 5496), and `tests/unit/test_install_ccsession.py` line 330.

Acceptance criteria:
- The parametrised retention tests expect 90 in place of 365: a missing key and a value of 30 or 89 become 90; 90 stays 90; 365 and 3650 are kept; the creation test expects `{"cleanupPeriodDays": 90}`.
- `check` prints nothing for a value of 90 or more (including a managed 90, as on this machine) and warns below 90 naming the source; `--list` and `--here` warn on stderr only below 90.
- A managed value of 60 is still never overwritten and `ensure` still exits 3 with the managed-file line; the install tests in `tests/unit/test_install_ccsession.py` pass.
- `main` in `retention.py` (its only caller) and its two shell and Python callers (`install.sh` line 177 and `install_ccsession.py` line 107) behave as before apart from the number.

## Phase 4: Existing names and the pruner

## Task 7: Create `session_keep.py` with the shared readers and `classify`, and add `ccsession --classify`

Depends on: Task 1

Create `src/superclaude/skills/ccsession-tag/session_keep.py` (source section R5.2), a standard-library Python 3.10 module in the style of `scan_sessions.py`. It holds plain functions with explicit arguments and no global state: `lists(projects_dir)` (every `<key>/topics` folder, including old per-folder lists), `names(list_dir)` (name file, session id from line 1), `marker(list_dir, session_id)`, `auto_shaped(name)` (true only when the label ends in `-MMDD-HHMMSS-xxxx`, optionally `-N`, with four lowercase hex digits), and `classify(projects_dir, apply)` returning the counts (auto-shaped, left unmarked, already marked) and the names it would mark. A session is marked only when every name saved for it, in every list, is auto-shaped and it has no `human` marker. With `apply` it writes the marker file atomically under the list's `.ccsession-lock` (the same `fcntl.flock` file the shell code uses) and never changes a name or an existing marker; without it, it writes nothing. A command line entry `main(argv)` takes `classify [--apply]` and `<projects_dir>`. In `ccsession` add `--classify [--apply]` beside `--mark` in the fast-path `case`, which runs the helper with `python3` from `CCSESSION_DIR` and does not call `ensure_names_migrated`.

Acceptance criteria:
- New tests in `tests/unit/test_ccsession_tag.py` (or a new `tests/unit/test_session_keep.py` that imports the module by path) show that a dry run of `--classify` leaves a tree snapshot of the whole temporary HOME byte-identical and prints the counts.
- `--classify --apply` marks as `agent` only unmarked names that end in the exact stamp, in every list including an old per-folder list, leaves an already marked name alone, skips a session with a `human` marker and a session that has any non-auto-shaped name in any list (a person's rename), and reports the three counts; running it twice changes nothing the second time.
- A name that merely contains digits (for example `fix-1118-notes`) and a name with an upper-case stamp are not marked.
- `scan_sessions.py` and its callers (`scan_topics`, line 1658) are untouched and their tests pass.

## Task 8: Add `prune` to `session_keep.py`, the `ccsession --prune` command and the list hint

Depends on: Task 7, Task 4, Task 6

Extend `src/superclaude/skills/ccsession-tag/session_keep.py` (source sections 2 and R6). Add `prune(projects_dir, home, days, apply, current_session)` returning a result object (candidates with name, last change, age in days, size and the paths that go; kept sessions with the reason; stale names; the effective Claude Code limit; the limit line). Candidates: sessions that have at least one saved name, whose every name in every list is marked `agent`, and whose newest transcript copy under `<projects_dir>/*/<id>.jsonl` has not changed in more than `days` days. A session named in any list without an `agent` marker is kept and reported as `kept: also saved in <list>`. With `apply`, remove each transcript copy, the folder `<projects_dir>/<folder>/<id>/`, `<home>/.claude/file-history/<id>/`, the session's name files in every list, its marker and an Orca tab record (`<home>/.local/state/ccsession/orca-tabs/*` whose first line is the id), the names, marker and record only after the transcript removal succeeded. Stale names: a name file with no transcript anywhere and a file time older than 2 days; markers with no name file and no transcript; tab records whose conversation is gone. Gates: resolve every path and require it under the projects folder or `file-history` of the same home and not a symlink (else skip and report); skip the session equal to `current_session`; take the effective limit from `retention.managed_value()` then the user settings then 30 (imported from the module beside it) and, when it is at or below `days`, print that Claude Code already deletes at that point and delete no agent session; an invalid `days` (not a whole number of at least 30: the agent limit is floored at 30, so no value can lower it) or an invalid `CCSESSION_AGENT_KEEP_DAYS` makes `--prune` exit 2 and delete nothing (the floor applies to `--prune` only). The output prints the limit line on its own line when `days` is below the effective limit: `LOWERS THE LIMIT: Claude Code keeps sessions N days here; this removes M agent sessions that are between D and N days old (S bytes).` A dry run writes nothing at all. In `ccsession` add `--prune [--apply] [--days N]` beside `--classify` (no `ensure_names_migrated`, `CLAUDE_SESSION_ID` passed as `current_session`) and, in `--list` and `--here` after `retention_warning` (line 1854), one dim line `N agent sessions are older than D days: ccsession --prune shows what would be removed` (D is the valid limit, else 30) produced by a read-only helper call that is skipped silently when `python3` or the helper is missing; a listing never exits 2 and prints no error, whatever `CCSESSION_AGENT_KEEP_DAYS` holds.

Acceptance criteria:
- New tests in `tests/unit/test_session_keep.py` (importing the module by path) and `tests/unit/test_ccsession_tag.py` build a temporary HOME with `_transcript`-style files and set file times with `os.utime`: a dry run leaves a snapshot of the whole HOME byte-identical (no migration stamp) and prints one line per candidate, the totals, the limit line on its own line and `Dry run: nothing was deleted. Run with --apply to delete.`
- `--apply` removes exactly the candidates and their parts; unmarked, `human`, recent (within `days`), symlinked, outside-the-folder and shared-between-lists sessions (`agent` in one list, unmarked or `human` in another) survive with their names; a name file one day old with no transcript survives, one three days old is removed.
- A transcript that cannot be removed (a read-only folder) keeps its name and marker; the running session (`CLAUDE_SESSION_ID`) is skipped; `--days 0`, `--days abc`, `--days 29` and `CCSESSION_AGENT_KEEP_DAYS=abc` or `=29` exit 2 and delete nothing, while `--days 30` and `--days 45` run; with a managed limit of 30 or less the agent part reports that Claude Code already deletes at that point.
- The limit line appears only when `days` is below the effective limit (a user file with 365 prints it; a managed 90 prints it for 30; none when the limit is 30).
- `--list` and `--here` print the older-than hint only when candidates exist and still print exactly what they printed before when none are marked `agent`; with `CCSESSION_AGENT_KEEP_DAYS=29` in the environment `--list`, `--here` and the new-tab question exit 0, print no error and print the hint with 30 or none, while `--prune` exits 2; a session with an `agent` marker, a transcript and no name file is not a candidate.

## Phase 5: Documentation

## Task 9: Document the markers, `--agents`, `--classify`, `--mark`, `--prune` and the 90-day target

Depends on: Task 8

Edit `src/superclaude/skills/ccsession-tag/README.md` (the files table at line 25 gains `session_keep.py`; the section "How long sessions are kept", lines 240 to 262, now says 90, that human sessions get the full limit and that agent sessions are pruned at 30 only by `--prune`; a new section describes who counts as human, the marker file, `--agents`, `--classify`, `--mark`, `--prune` with its dry run, and the three limit lines of source section 2; the troubleshooting row at line 813 mentions `--prune`), `src/superclaude/skills/ccsession-tag/SKILL.md` (one line each for the new commands), the help comment block at the top of `src/superclaude/skills/ccsession-tag/ccsession` (lines 20 to 118: add `--agents`, `--mark`, `--classify` and `--prune`) and `CHANGELOG.md` (one entry under the unreleased heading). No document names a path that does not exist.

Acceptance criteria:
- `ccsession --help` lists `--agents`, `--classify`, `--mark` and `--prune`; the existing help test in `tests/unit/test_ccsession_tag.py` passes, and a new assertion checks the four names.
- The README states in plain words that nothing is deleted unless `ccsession --prune --apply` is run, names the dry-run line, and gives the three limit-change lines of the source section 2 on lines of their own.
- `make sync-dev` followed by `make verify-sync` reports the synced copies of the skill folder in step with `src/superclaude/skills/ccsession-tag/`, including the new `session_keep.py`.
- `grep -rn 'src/superclaude' src/superclaude/skills/ccsession-tag/README.md` shows no new instruction to read a primitive through a `src/superclaude` path.
