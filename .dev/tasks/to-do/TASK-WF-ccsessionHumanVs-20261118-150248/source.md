---
title: "ccsession: tell human-saved sessions from agent-saved ones, and keep them for different times"
status: revised-after-independent-review-2 (agent is written in one place only; a rename needs no origin; a resume never writes a marker; floor applies to --prune only)
adversarial_status: not-run (inline debate; see proposals-and-debate.md)
created: 2026-11-18
inputs:
  - .dev/research/ccsession-saved-sessions/research-retention.md
  - .dev/analysis/ccsession-saved-sessions/analysis.md
  - .dev/brainstorm/ccsession-saved-sessions/proposals-and-debate.md
---

# ccsession: human-saved vs agent-saved sessions

## 1. What this changes, in plain English

1. ccsession records, when a name is saved, whether a person chose it or not.
2. Lists (`--list`, `--here`, and the new-tab question) stop showing agent-saved sessions unless asked (`--agents`). Every session can still be resumed by name.
3. Claude Code's own limit is set to 90 days (the installer's target goes from 365 to 90), so transcripts are kept 90 days broadly.
4. A new command, `ccsession --prune`, removes agent-saved sessions that have not changed in 30 days. It shows what it would remove and removes nothing unless `--apply` is given. Nothing runs it automatically.
5. Two helper commands deal with the sessions already saved: `--classify` (marks the ones whose name is an exact auto-name) and `--mark <name> agent|human`.

## 2. Limit changes (each stated on its own line; the owner decides every removal)

- **LOWERS NO LIMIT BY ITSELF (installer):** `retention.py ensure` goes from "raise to 365" to "raise to 90". It never lowers a value already set (a 365 stays 365) and never writes where managed settings decide (this machine: managed 90). A machine with no value goes from Claude Code's 30 to 90, which keeps more, not less.
- **LOWERS THE AGENT LIMIT, ONLY WHEN THE OWNER RUNS `ccsession --prune --apply`:** on a machine whose Claude Code limit is above 30 (the owner's own workspace: 365), agent-saved sessions between 30 days and that limit are deleted at that moment, and only those. The dry run prints this on its own line first, with the count and size.
- **THE AGENT LIMIT CANNOT BE LOWERED BELOW 30 DAYS:** `--days N` and `CCSESSION_AGENT_KEEP_DAYS` with a value below 30 are refused (exit 2, nothing deleted); a value above 30 only keeps agent sessions longer. So no setting left in `~/.claude/ccsession.env` can make `--prune` delete a session younger than 30 days (independent review M6).
- **DELETES STALE NAMES, ONLY WITH `--apply`:** a saved name whose transcript is gone (older than a 2-day grace) is removed from the list, whatever its origin. The session itself is already gone.
- **Not covered:** transcripts that have no saved name (a `claude -p` run, for example) follow Claude Code's limit (90 after this change, 30 before it). This change deletes none of them.

## 3. Terms

- **Human-saved:** a person typed the name. **Agent-saved:** everything else. **Unmarked:** no record; treated as human everywhere (shown, never pruned), because a wrong "human" costs a row and 60 days, and a wrong "agent" can delete a transcript. Every session saved before this change is unmarked, and so is every session a launch only resumed: a resume never writes a marker.
- **Marker:** the file `<list>/.origin/<session id>` (the list is `~/.claude/projects/<key>/topics/`), one line, `human` or `agent`, written under the list's lock, replaced atomically. The session id is already limited to letters, digits, `_` and `-`.

## 4. Requirements

### R1. Who is human (decided when the name is saved)

| Route | Origin |
|---|---|
| A name typed at the new-tab question (`ccsession --ask` answered, non-empty), for a NEW session | human |
| `ccsession <topic>` / `--name` run on a terminal (stdin and stdout are terminals) with no `CLAUDECODE` in the environment, for a NEW session | human |
| A name a person gives with `/rename`, in a session started by ccsession or not (plain `claude`, its `/resume` picker, the IDE): a name the hook reports at a prompt or at the end of a session that is not already one of that session's saved names in any list (compared by the session id inside the name file, a collision-suffixed `<name>-2.txt` included), whether or not the session had an older name and whatever list that is in (B1) | human (always wins; needs only the hook's `--event`, never an origin) |
| An auto-name (`--auto-name`), including when a person pressed Enter at the question, for a NEW session | agent |
| `CCSESSION_NAME` in the environment; Claude's `--name`/`-n` in the launch arguments, for a NEW session | agent |
| A `ccsession` launch (never `--sync-name`, `--mark`, `--classify` or `--prune`) started inside Claude Code (`CLAUDECODE` set), or with no terminal, for a NEW session | agent |
| Every session saved before this change; any session a launch only resumed (a tab reopen, `ccsession <name>`, a worker's `CCSESSION_NAME` equal to a saved name, `/resume` inside a launch); names imported by `--migrate-names` / `import_claude_names`, names written by `rename_dot_labels`, and any other `sync_name` call that is not the hook's; a session saved by a launch that did not go through ccsession, until a person renames it | no marker (unmarked) |

**Agent is written in exactly one place:** when a launch creates a NEW session (the hook's SessionStart event with `source` `startup`) and the launch's origin is `agent`. Nothing else writes `agent`: a resume never writes any marker, a rename writes only `human`, and `--classify` and `--mark` are the explicit commands (R5).

**Verified fact (2026-11-18, `.dev/research/ccsession-saved-sessions/claudecode-hook-env-probe.md`):** Claude Code sets `CLAUDECODE=1` for hook processes (SessionStart, UserPromptSubmit and SessionEnd were tested, with the launching shell's variable removed; print mode, `claude -p`, on one Claude Code version, recorded in that note). A second probe in the same mode found that the SessionStart payload carries `source` (`startup` for a new session, `resume` for a resumed one; `clear` and `compact` are documented values, not observed) and, with `--name`, the `session_title`. A third probe, an interactive session in a pseudo-terminal, observed that an interactive `/resume` from the picker reports `source: resume` and keeps the resumed session's id (one version, one picker selection; the second probe's persistence setting and a trap that disables transcript saving in a nested interactive `claude` are described in the note). The hook's own `ccsession --sync-name` call therefore always has `CLAUDECODE` set, so the `CLAUDECODE` rule above is a rule about a launch only: it lives in the main script's launch path, which `--sync-name` never reaches because it is a fast-path command that exits first. No rule that reads `CLAUDECODE` may run on the hook path.

### R2. How the origin travels

1. `ccsession-orca` sets `CCSESSION_ORIGIN=human` only when the name came from the question; otherwise `agent` (an auto-name, `CCSESSION_NAME`, a carried `--name`/`-n`, or an untagged start). On a resume or tab reopen it sets none. The value is only ever read by the hook's new-session write (R2.4), so a resume cannot use it.
2. `ccsession` (main script, launch path only, after the fast-path commands): `CLAUDECODE` set forces `agent`; a valid `CCSESSION_ORIGIN` from the environment is kept; otherwise `human` when stdin and stdout are terminals, else `agent`. It exports the result with the launch id it already exports.
3. `hooks/session-name.sh` calls `ccsession --sync-name <id> <name> [--keep-others|--check-others] -- --event <SessionStart|UserPromptSubmit|SessionEnd> [--source <startup|resume|clear|compact>] [--origin <human|agent>]`. The options follow a literal `--`, so an older `ccsession` that reads only the fourth argument as its keep flag ignores them. The hook gives `--event` (and, at SessionStart, `--source` from the payload) whenever it is the owner of the launch (the existing `OWNER=1` test, which is also true for a Claude Code that ccsession did not start, with no launch id); it gives `--origin` only when in addition `CCSESSION_ORIGIN` is `human` or `agent`. When it is not the owner (a Claude started inside a session) it gives none of the three. The hook never reads `CLAUDECODE`.
4. `sync_name_locked` writes a marker, under the lock it already holds, and only when `--event` was given (the hook is the only caller that gives it; `import_claude_names`, `rename_dot_labels` and every other caller write no marker, whatever `CCSESSION_ORIGIN` holds in the environment). There are exactly two writes:
   - **New-session write** (the only place `agent` is written): `--event SessionStart`, `--source startup` and `--origin human|agent` all given: write the `--origin` value when the session has no marker.
   - **Rename write**: `--event UserPromptSubmit` or `SessionEnd` and the name is new for the session, meaning it is not already saved for the session in this list and no `<name>.txt` or `<name>-N.txt` in any list holds this session id (checked only on this path, by the id inside the file): write `human`, replacing any marker (B1). No `--origin` is needed, so a rename in a Claude Code that ccsession did not start is covered.
   - Everything else writes nothing: a SessionStart whose source is `resume`, `clear`, `compact` or missing; a prompt or an end whose name is already one of the session's saved names; every call without `--event`. A resume therefore never writes `agent` or any other marker, and an unmarked session stays unmarked until a person renames it, or `--classify` or `--mark` (R5) acts. The list clean-up that removes older names (`--keep-others`, `--check-others`) never decides a marker.
   - **Known limits, stated not prevented (both end `human`, the safe direction: shown, never pruned):** `/resume` inside a launched session gets the launch's label at SessionStart (existing behaviour), so the resumed session's own old name is "new" for it at a later prompt or at SessionEnd; and `/clear` starts a new session id without a SessionStart (the hook's matcher is `startup|resume`), so its first name at a prompt counts as a rename. Also, a launch whose SessionStart save did not happen (the list lock was busy for 4 seconds, or the hook's folder check failed) has its label arrive first at a prompt, where it is written `human`. The cost is that such an agent session escapes the 30-day limit.
   - **Known limit, unmarked copy (independent review 3, M1):** an agent session whose Claude Code folder moves into another repo gets its name saved in that repo's list with no marker (the name is already one of the session's names in the first list, so neither write applies). That copy is shown and never pruned, which is the safe direction but escapes the 30-day limit. `ccsession --classify --apply` marks it, because every name saved for the session is auto-shaped and none is `human`.
5. The label format of `--auto-name` does not change.

### R3. Listing

1. `--list`, `--here`, `--here --all` and the new-tab question hide rows whose marker is `agent`. `--agents` (accepted after `--list` or `--here`, in any order with `--all`) shows them. `--all` keeps its meaning (every worktree) because it is already taken.
2. Each view that hid rows ends with one dim line: `N agent sessions hidden: <the command that shows them>` (`ccsession --list --agents`, `ccsession --here --agents`, or in the question: `type + to list them`). Typing `+` at the question lists them, as `*` lists every worktree.
3. Hidden rows are not counted in "N more sessions in other worktrees".
4. A list whose rows are all hidden prints no heading; if every row of every list is hidden, the output says so with the same count line instead of "No labeled sessions yet".
5. Hiding is display only: `ccsession <name>`, `--rm` and `--orca-tab-reopen` work on any session.
6. No new process per row: the marker is read with a shell builtin; bash 3.2 safe.

### R4. Retention (`retention.py`)

1. `MIN_DAYS` becomes 90. `ensure` raises an absent or lower value to 90 and keeps any value of 90 or more; managed settings still win; a non-number or invalid file is still left alone.
2. `check` warns only below 90. README "How long sessions are kept" and the install output say 90, and say that human sessions get the full limit and agent sessions are pruned at 30 only by `--prune`.

### R5. Existing names

1. **Unmarked stays human.** The upgrade changes no list and deletes nothing.
2. `ccsession --classify [--apply]`: reads every list; for each unmarked name whose label ends in the auto-name stamp (`-MMDD-HHMMSS-xxxx`, optionally `-N`) reports "would mark agent" (or marks it with `--apply`). It prints how many were auto-shaped, how many stay unmarked, and how many already had a marker. It marks a session only when every name saved for it, in every list, is auto-shaped and it has no `human` marker (a session a person renamed has a non-auto name in some list, so it is skipped; a name a person typed is never marked). It never changes a name or an existing marker, and writes nothing without `--apply`. It stays the only way to mark a session saved before this change as `agent`.
3. `ccsession --mark <name> agent|human`: sets the marker of the session saved under that name in this repo's list; the only command that can lower `human`. Exit 1 when the name does not exist.

### R6. `ccsession --prune [--apply] [--days N]`

N defaults to `CCSESSION_AGENT_KEEP_DAYS`, else 30; a whole number of at least 30. The floor applies to `--prune` only: a smaller or invalid value (from `--days` or the variable) makes `--prune` exit 2 and delete nothing, while `--list`, `--here` and the new-tab question never fail on it (R6.6).

1. **Candidates:** sessions that have at least one saved name (a session with no name is not a saved session; section 2, "Not covered") and whose marker is `agent` in every list that has a name for the session (a session named in any list without an `agent` marker is kept and reported as `kept: also saved in <list>`; F2), and whose newest transcript copy (any project folder) has not changed in more than N days, by file modification time (the clock Claude Code uses).
2. **What goes with a candidate:** every `projects/<folder>/<id>.jsonl`, the folder `projects/<folder>/<id>/`, `file-history/<id>/`, its name file(s) in every list, its marker, and an Orca tab record whose session is that id. Names, marker and tab record are removed only after the transcript was removed.
3. **Stale names:** a name file whose transcript exists nowhere and whose own modification time is more than 2 days old; markers whose session has no name file and no transcript; Orca tab records whose conversation is gone. Any origin.
4. **Output (dry run, the default):** one line per candidate (name, last change, age in days, size), the totals, the limit line (section 2) on its own line, and `Dry run: nothing was deleted. Run with --apply to delete.` A dry run writes nothing at all, not even a migration stamp.
5. **Gates:** (a) only sessions whose every name, in every list, is marked `agent`; unmarked and human never (F2); (b) any copy changed within N days keeps the session; (c) every path is resolved and must lie under the projects folder or `file-history` of the same home and not be a symlink, else it is skipped and reported; (d) the session named by `CLAUDE_SESSION_ID` (the one running the command) is skipped; (e) `--apply` is the only way to delete: no environment variable, setting or hook turns it on; (f) a transcript that could not be removed keeps its name; (g) one lock per list is held while its files change; (h) when Claude Code's own limit is at or below N, the agent part prints that Claude Code already deletes at that point and does nothing.
6. `--list` and `--here` add one dim line when agent sessions are past D days: `N agent sessions are older than D days: ccsession --prune shows what would be removed`, where D is the value of R6 when it is valid and 30 when it is invalid or below 30. A listing never exits 2, never prints an error about it and never fails the question (independent review 2, M3).

### R7. Install and docs

1. The new helper file ships with the skill and is installed beside `ccsession` (the install tests and `superclaude doctor` must pass in a throwaway HOME).
2. README, `--help` text, `SKILL.md` and `CHANGELOG.md` describe the markers, `--agents`, `--classify`, `--mark`, `--prune` and the 90-day target.

## 5. Tests (one per rule, in `tests/unit/`, throwaway HOME only)

- R1/R2: each row of the origin table writes the expected marker (or none); a rename writes `human` over `agent`; a nested launch (`OWNER=0`, `CLAUDECODE` set) makes the hook pass no `--event` and writes no marker; a tab reopen and a resume by name on a terminal write no marker and leave an existing one as it is; `--auto-name` label format unchanged.
- B1 route 1 (untagged launch, then `/rename`): a launch through `ccsession-orca` with `CCSESSION_AUTOSTART=0` (origin `agent` exported, no name, no marker), then the hook at `UserPromptSubmit` with `session_title` `my-work` writes marker `human`; the same with the auto-name having failed and the launch started untagged.
- B1 route 2 (rename after the folder moved to another repo): a session saved under an auto-name in repo A's list (marker `agent`), then the hook at `UserPromptSubmit` with `cwd` in repo B's folder and a new title writes marker `human` in B's list, leaves A's list unchanged, and `ccsession --prune` keeps the session (`kept: also saved in <B's list>`).
- Hook and `CLAUDECODE`: every hook test runs once with `CLAUDECODE=1` set (the real condition, verified): a new session (SessionStart, source `startup`) with `--origin agent` still writes `agent`, one with `--origin human` writes `human`, and a rename at a prompt writes `human`; a `ccsession` launch with `CLAUDECODE=1` still gets `agent`.
- Agent is written in one place (table-driven, review 2 root cause): for every combination of event (SessionStart with source `startup`, `resume`, `clear`, `compact` and with no source; UserPromptSubmit; SessionEnd) and `--origin` (`agent`, `human`, none) on a session without a marker and with a new name, a marker `agent` appears only for SessionStart, source `startup`, origin `agent`; `human` appears only for SessionStart, source `startup`, origin `human`, or for a new name at UserPromptSubmit or SessionEnd; every other combination writes nothing. Run each combination with and without an existing marker: an existing marker changes only to `human` through the rename write.
- B2, resume never marks: an unmarked saved session (a name file, no marker, as every pre-upgrade session is) resumed by an `agent` launch (`ccsession-orca` with `CCSESSION_NAME` equal to its saved name), by `/resume` inside an agent launch (SessionStart, source `resume`), by a tab reopen and by `ccsession <name>` on a terminal, stays unmarked and is still listed.
- B1 round 2, rename outside ccsession: the hook with no launch id (plain `claude`, its `/resume` picker or the IDE; `OWNER=1`), `--event UserPromptSubmit` and no `--origin`, over an existing `agent` marker, a name that is new for the session writes `human`; the same name again writes nothing; a collision-suffixed own name (`<name>-2.txt` in another list holding this session id) is not new.
- `import_claude_names`, `rename_dot_labels` and `--check-others` removing a duplicate name write no marker even with `CCSESSION_ORIGIN=agent` in the environment. Known limits are not asserted away: the test for `/resume` inside a launched session checks only that SessionStart (source `resume`) writes nothing.
- R3: agent rows hidden in all three views, shown with `--agents` (any flag order), count line text, all-hidden output, `+` at the question, hidden rows excluded from the other-worktrees count, resume of a hidden name works.
- R4: the existing retention tests with 90 in place of 365; a value of 365 or 3650 is kept; managed settings still win.
- R5: `--classify` dry run writes nothing; `--apply` marks only exact auto-shaped unmarked names; it skips a session with a `human` marker and a session that has any non-auto-shaped name in any list (a person's rename); `--mark` both ways and its error.
- R6: dry run writes nothing (tree snapshot identical before and after, including no migration stamp); `--apply` removes exactly the candidates and their parts; unmarked, human, recent, symlinked and outside-the-folder cases survive; a session id named in two lists, `agent` in one and unmarked or `human` in the other, keeps its transcript and both names (F2); the 2-day grace; the limit line only when the limit is lowered; a failed removal keeps the name; `--days` validation (`0`, `abc` and `29` exit 2 and delete nothing; `30` and `45` run); `CCSESSION_AGENT_KEEP_DAYS=29` makes `--prune` exit 2 the same way, while `--list`, `--here` and the new-tab question with that value exit 0, print no error, and print the hint with 30 or none; a session with an `agent` marker, a transcript and no name file is not a candidate; the `CLAUDE_SESSION_ID` skip.
- Gate before the PR: the whole suite as CI runs it, before the first edit and after; `make lint`; `uv run ruff format --check src/ tests/`; `make sync-dev` then `make verify-sync`; `git diff --check`; install into a throwaway HOME and `superclaude doctor`.

## 6. Out of scope

Automatic or scheduled pruning; pruning transcripts that have no saved name; any change to Claude Code's settings beyond `retention.py`; a keep store or mtime changes (rejected, see proposals-and-debate.md); any change to the auto-name label.

## 7. Decisions the owner can still reverse

1. Pruning stays manual in this change (recommended). An automatic run would be a separate, later change.
2. A person pressing Enter at the question counts as agent-saved (recommended: no one chose that name; `/rename` or `--mark` promotes it).
3. Stale names of human sessions are removed too, after the 2-day grace (recommended: the label alone cannot resume anything).

## 8. Follow-up candidates (not part of this change; recorded, not fixed)

From the independent reviews of 2026-11-18 (`/home/coder/workspaces/IronFlow/.dev/handoffs/ic-638-independent-spec-review.md` and `...-review-2.md`) and the earlier panel reviews. Resolved by the two revisions: review 1's M1 (`CLAUDECODE` on the hook path), M2 (the origin reaches only the hook's call), M3 (a list clean-up is no longer a rename); review 2's B1 (a rename needs only `--event`), B2 (a resume never writes a marker), M1 (the false `/resume` claim, now a stated limit in R2.4), M3 (the floor applies to `--prune` only), N1 (probe limits), N2 (content check, collision suffix), N3 (argument order after `--`), N4 (a candidate needs a saved name), review 1's N2 and N4. Review 2's M2 (a launch whose SessionStart sync did not happen, and `/clear`) is a stated limit in R2.4, and so is review 3's M1 (an agent session that moves into another repo's folder gets an unmarked copy there, shown and never pruned; remedy `--classify --apply`). Review 3's notes N3 (a name that merely ends in `-N` counts as a session's own; the "already saved" check must look at the list as it was before this call's own write), N4 (renaming in one list to a name the session already has in another leaves the first list's row hidden) and N5 (a rename inside a nested `claude` writes nothing) are recorded here and not fixed. Still open:

- M4: a line sent into a tab by an orchestrator at the name question counts as typed by a person; `--fork-session` starts a new session id with no marker; state the limit in section 3, let an `agent` origin already in a worker's environment win over the question, give a fork the origin of the session it forks.
- M5: the R4 tests that use a managed value of 90 as "below the target" must move to a value below 90 (for example 60).
- M7: tests for R6.3's stale markers and tab records, R6.5(e), (g) and (h), R6.6's dim line, R4.2's threshold and text, and R3.6's process-count test including hidden rows.
- M6 (part): the limit line in R6.4 prints a fixed "30"; print N (R6.6 now prints D).
- N1: section 2's "owner's workspace: 365" example does not hold where managed settings set 90. N3: check the session id of a name file's first line (letters, digits, `_`, `-`) in `--classify` and `--mark`. N5: "LOWERS NO LIMIT BY ITSELF" wording. N6/panel M1 to M3: read the limit with `retention.managed_value()`, an invalid `CCSESSION_AGENT_KEEP_DAYS` exits 2, helper named `session_keep.py` (already in the plan). N7: the question's hint "Enter = auto-named" does not say such a session is hidden and prunable after 30 days.
- From the plan check: no assertion that imported names get no marker (now covered by the "No false promotion" test row), `--rm` and `--orca-tab-reopen` on a hidden session, and the install and `superclaude doctor` runs as task bullets.
