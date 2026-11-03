# Coder #433: decisions

Issue: IronbellyOrg/Coder#433 (a relaunched Orca tab starts a new session instead of reopening its own).

## D1. Can ccsession alone do it, or does Orca need a change?

**ccsession alone.** Orca gives the relaunched command the same `ORCA_PANE_KEY` it had before the restart (live test and source, see REPORT.md sections 1 and 2), so ccsession can remember which session each tab ran and reopen it. No Orca change is needed. Orca's own resume path does not cover this case (it skips agents whose last state is `done`); changing that would be Orca work and is not needed for this fix.

## D2. What identifies the tab, and where the record lives

- The tab is identified by `ORCA_PANE_KEY` (tab id and pane id, both saved by Orca). A new tab or split pane has a new key, so it has no record and still gets the question.
- One small file per pane: `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/<pane key, ":" written as "_">`, holding three lines: the session id, the folder ccsession was launched in (`pwd -P`), and the `ORCA_TERMINAL_HANDLE` of the terminal it ran in. State, not cache: it must survive a restart; losing it only means the question comes back.
- Written by the ccsession hooks (SessionStart and each prompt, so `/clear` and an in-Claude `/resume` update it) through `ccsession --orca-tab-session <id>`, only for the Claude Code that ccsession launched (the existing launch-owner check), never for a Claude nested inside it.
- Each session id is held by one pane at most: writing a pane's record removes the same id from every other pane's record, under the existing name-list lock. Records whose conversation no longer exists are removed at the same time.

## D3. When the tab's session is reopened without the question

`ccsession-orca` reopens the tab's recorded session only when all of these hold; otherwise it does exactly what it did before:

1. The question would be asked today: a terminal on stdin and stdout, `CCSESSION_AUTOSTART` not `0`, no `--resume`/`-r`/`--continue`/`-c`. So non-interactive launches (supervised workers) are unchanged.
2. Orca passed only options: every argument starts with `-`, and none is `--prefill`, `-p`/`--print`, `--name`/`-n`, `--session-id`, `--fork-session` or `--from-pr`. A prompt, prefill text or option value is a non-option argument, so those launches still ask. Orca's relaunch line in the live test was exactly `--dangerously-skip-permissions`.
3. `ORCA_PANE_KEY` is set, the pane has a record, and `CLAUDECODE` is not set.
4. The record's terminal handle differs from the current `ORCA_TERMINAL_HANDLE`. Orca gives each new terminal process a new handle, so a relaunch differs, while a person running `ccsession-orca` again by hand in the same terminal does not, and gets the question.
5. The record's folder equals `pwd -P`, and the conversation is still saved (`session_saved`).

The session is resumed by its name when this repo's list has a name for that exact session id (`ccsession --name <name>`, so the tab title, label and hooks behave as for a typed name), otherwise by id (`--resume <id>` passed to Claude Code, an untagged resume).

Why not "reopen on any relaunch with a record": a person who opens a new tab must still be asked (new pane key, so no record), and launches carrying a prompt or session choice already say what to start.

## D4. Safety rules (new tabs, prompts, names, --resume, missing transcripts, two tabs, per-worktree list)

| Requirement | How it holds |
|---|---|
| New Claude tab still asked | New tab or split pane: new `ORCA_PANE_KEY`, no record (D3.3). Live: asked after the restart. |
| Prompt, name, `--resume` launches unchanged | D3.1 and D3.2. Live: prompt launch asked, `--resume` passed through without the question. |
| Recorded session gone: fall back, never error | D3.5 (`session_saved`); `--orca-tab-reopen` exits 1 and the question follows. Unit test deletes the transcript. |
| Two tabs never reopen the same session | A session id is held by at most one pane file: each write removes the id from every other pane, under a lock. Live: after `--resume` in another terminal, tab 2 lost the record and was asked after the next restart. |
| Per-worktree session list (IronClaude #350) | The record keeps the launch folder and is used only in that same folder, so a tab never reopens a session from another worktree. Unit test: the same pane asked from another worktree gets nothing. |
| Nested Claude or a `ccsession` inside Claude Code | Only the Claude Code ccsession launched records (existing owner check plus `CCSESSION_LAUNCH_ID`); `--orca-tab-reopen` refuses inside Claude Code (`CLAUDECODE`). |

The record is kept when a session ends: a workspace stop may end Claude Code with its SessionEnd hooks, and clearing the record there would defeat the reopen.
