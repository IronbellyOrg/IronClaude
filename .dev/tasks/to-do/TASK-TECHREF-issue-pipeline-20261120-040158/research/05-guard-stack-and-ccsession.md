# Research: Guard stack and ccsession
**Investigation type:** Code Tracer + Integration Mapper
**Scope:** hooks/scripts/launch-*.sh, hooks.json, install_hooks.py, install_ccsession.py, ccsession-tag, four design docs, guard and install tests
**Status:** Complete
**Date:** 2026-11-20
---

Snapshot root used for every citation: /home/coder/.cache/ic-snap-20261120/master (abbreviated `SNAP` below). Line numbers are for the 61ac2c2e6 snapshot, re-read from live files. Everything not in the "Observation run" section is READ-ONLY-READING.

## 1. L1 guard: launch-level-guard.sh (808 lines) [READ-ONLY-READING; every line re-read from the snapshot]

Path: SNAP/src/superclaude/hooks/scripts/launch-level-guard.sh

### 1.1 Header, events, exit codes
- Header lines 1-10: "Launch-level guard (L1), IronbellyOrg/IronClaude issue #394"; "Registered on UserPromptSubmit and PreToolUse. Exit 0 allows; exit 2 blocks with a message on stderr; never exit 1, no onFailure." (:4-6). Version marker `# launch-level-guard-version: 1` (:10). Only a session the claim script launched (a valid top-level session_id bound in the store) is governed; every other session is ordinary and never blocked (:6-7).
- Events handled: `case $LL_EVENT` at :275-282: `UserPromptSubmit` -> branch `prompt`; `PreToolUse` -> branch `tool`; any other event name (jq maps it to `OTHER`, :185) -> exit 0 unless positively governed, in which case it falls to the last line (:807-808) = LL-BROKEN exit 2.
- Strict-mode: `set -u -o pipefail`, `set -f` (no globbing), `umask 077`, `LC_ALL=C` (:13-16).
- Exit codes: `ll_deny` (:135-139) prints the message and `exit 2`. `ll_on_exit` EXIT trap (:147-163): rc 0, or rc 2 after a deliberate deny, passes through; any other rc: ordinary session -> `exit 0`; governed -> LL-NOBIND (prompt branch) or LL-BROKEN, exit 2. So the script never exits 1 (the L2 pre-push hook is the one that exits 1, see section 3).
- Store path from three literals LL_S1=.claude, LL_S2=state, LL_S3=launch-level (:20-23) so the script text never contains the joined path; `LL_STORE="${HOME:-}/.claude/state/launch-level"`. The only environment variable read is HOME.

### 1.2 Closed vocabulary of block words (ll_say :36-133)
LL-IMPL, LL-COMMIT, LL-PUSH, LL-PUSH-FORM, LL-PROTECTED, LL-MERGE, LL-GH-WRITE, LL-SUBMIT, LL-REPO, LL-UNKNOWN, LL-MCP, LL-ESCAPE, LL-TURN, LL-TAMPER, LL-SKILL, LL-BIG, LL-NOBIND, and the default LL-BROKEN (case `*)` :110). LL-TAMPER prints the release command `rm "$LL_STORE/sessions/$LL_SID" "$LL_STORE/sessions/$LL_SID.ok"` (:97), and is downgraded to LL-BROKEN when the session id is invalid (:38-40). Two notes: LL-STATE note (:127-129, "launch record was invalid or unreadable, so the strictest level (worktree) applies") and LL-TEXT note (:130-132, the guard does not tell quoted text from commands). The words are printed in the closed form `Blocked:` / `Why:` / `You can:` plus a line `Launch-level guard: this session was started by /sc:issue --claim at level <worktree|worktree (approved)|full|full --submit>` (:115-126).

### 1.3 Binding state machine (prompt branch :314-385)
1. Parse (:182-205): one `jq` call; event, agent_id flag, input-error flag, session id (valid only if `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$`), tool name, skill name, edit path, isolation, then prompt or command text.
2. Empty-store fast exit (:168-173): no `sessions/` directory AND input has no `[sc-launch:` -> exit 0. So with an empty store nothing is ever read further.
3. Governed lookup (:257-273): valid id AND `sessions/<id>` exists (even as symlink) -> `LL_GOVERNED=1`. Level read with `read -N 13` from a regular non-symlink file: `worktree` -> W, `full` -> F, `full-submit` -> FS (each with optional trailing newline); anything else (including symlink/unreadable) -> W plus `LL_NOTE_STATE=1` (:264-269). If level is W and a regular non-symlink `<id>.ok` exists -> WA (:270-272).
4. Subagent prompts (`agent_id` a non-empty string) exit 0 at once: "B5: a subagent prompt never binds or approves" (:315). agent_id is read only on UserPromptSubmit (:199).
5. Marker: strict regex `\[sc-launch:v1:([0-9a-f]{32})\]` anywhere in the prompt (:318); loose marker = prompt starting `[sc-launch:` after whitespace/BOM (:320-330).
6. Usable nonce (:334-337): `pending/` is a directory, not a symlink, owned by the euid (`-O`); `pending/<nonce>` regular non-symlink file.
7. Already governed (:338-362): a supplied usable record is deleted (consumed; the level never changes, B8). Approval (:347-360): only when level is W: first line of the prompt matches `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` -> create `sessions/<sid>.ok` with noclobber, only if `sessions/` is an owned non-symlink directory and `.ok` does not exist. Then exit 0. Approval lasts until a person deletes the files (:361).
8. Not governed, no nonce and no loose marker -> exit 0 (B9, :363-365).
9. A marker is present: `LL_GOVERNED=1` from here (:366) so any later failure is LL-NOBIND; empty session id -> LL-NOBIND (B7, :367); `mkdir -p sessions` and require it owned non-symlink (:368-371); `mv pending/<nonce> sessions/.take-<sid>` (one rename wins the nonce, B11, :372-375); `ll_link_take` (:299-313) reads the taken word, and if it is one of the 3 levels hard-links it to `sessions/<sid>` with `ln` (fails if target exists, so first binding wins), else publishes the word `degraded` (:306); loose marker with no binding publishes `degraded` (B12, :377-379); if a regular `sessions/<sid>` exists -> exit 0 else LL-NOBIND (B13, :381-384).
- Consequence: the pending record's inode equals the session record's inode (hard link); `degraded` is read as level W with the LL-STATE note.

### 1.4 Governed versus ordinary; fail-closed versus fail-open
- Governed means ONLY: valid session id with a `sessions/<id>` entry (:257). Tool branch with no governed record -> exit 0 (:391). Missing or invalid session id on a tool event is "identity loss" -> exit 0 (:386-391, comment :209-217).
- No jq / unparseable JSON (`LL_RC != 0`, :208-238): a tool payload (contains `"tool_name"`) scans every `"session_id":"..."` value for a bound session; if one is found the script falls through to the last line and blocks LL-BROKEN (:218-232; comment :213-214 declares that any bound id in the text counts); a prompt with a `[sc-launch:` marker and no parse -> LL-NOBIND (:233-236); anything else -> exit 0 (:237).
- Input error flag (non-string tool field or NUL, :196-197) on a governed tool call -> LL-BROKEN (:392).
- Default deny: line 807-808 `ll_deny LL-BROKEN` for anything that reaches the end (prompt branch of a governed session never reaches it, it exits at :361).

### 1.5 Level matrix (W, WA, F, FS) and block order (:781-803)
Precedence order at :783: BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL. The first blocked class prints its message.

| Class (word) | W | WA | F | FS | Code line |
|---|---|---|---|---|---|
| IMPL (LL-IMPL) | block | allow | allow | allow | :786, :788 |
| TURN (LL-TURN) | block | allow | allow | allow | :786, :788 |
| COMMIT (LL-COMMIT) | block | block | block | allow | :787, :789 |
| PUSH (LL-PUSH) | block | block | block | allow | :787, :790 |
| SUBMIT (LL-SUBMIT) | block | block | block | allow | :787, :789 |
| SKILL (LL-SKILL, unreadable skill name) | block | block | block | allow | :787, :790 |
| REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG | block at every level including FS | | | | :791-800 |
Any class with no matching cell (including empty level) -> LL-BROKEN (:801).
So: F ("full") cannot commit, push or open a PR; only FS can; nothing at any level can merge, push main/master, or use a free-form `gh api` write.

### 1.6 Classifiers (part 8)
- Skill tool (:398-413): name normalised (first word, lower case, strip one `/`, text after last `:`, strip one `sc-` and one `-protocol`); `implement | task | cleanup` -> IMPL; `pr-submit` -> SUBMIT; `issue` -> ESCAPE; empty -> SKILL. **[STALE DOC]** the design lists implement, task, improve, cleanup, spawn, build; code at :409 has three. See Stale Documentation.
- Bash / Monitor (:414-726): >65536 bytes -> BIG (:419-420); else normalisation NM1a-NM7 (:422-435), then TAMPER tokens (:440, :450-451), ESCAPE words (:452-456: `ccsession*`, tmux, screen, xdotool, ydotool; claude plus a launch flag :452-453, :495), orca verb allow-list (:480-491), G2 rule 2 (:496-537), git (:541-725), gh (:547-663), canonical push (:713-724).
- Edit / Write / NotebookEdit (:727-735): path only after `/+` squeeze; `..` segment -> TAMPER; contents never read.
- Agent / Task (:736-738): only `isolation == remote` -> ESCAPE. Cron*/Schedule* (:739-740) -> TURN. RemoteTrigger, Workflow, SendMessage (:741-742) -> ESCAPE. `mcp__*` (:743-754): suffix after the last `__` containing merge/push/commit/pull_request/create_or_update_file/delete_file/update_ref/create_ref/create_branch -> MERGE (if it contains merge) else MCP, unless it starts list_/get_/search_/read_.
- Tamper tokens on the text or edit path (:760-775): `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git`; #441 lower-cased tokens `.git/hooks`, `hooks/pre-push`, `pre-push.launch-level`, `--no-verify`, `hookspath`, `hook.pre-push` (:766-768); dot-segment tricks after `.claude` (:773-775); `install_hooks` in the text (:440); `superclaude ... install` (:451).
- Orca allow-list (:480-482): `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`; with any glob character in the command the read verbs become ESCAPE (:484); every other orca call is ESCAPE (:489) unless a `--help`/`-h` short call (:488).
- Git (:580-725): `merge|pull` -> MERGE, `push|send-pack|http-push` -> PUSH, `commit|cherry-pick|am|commit-tree` (text) and `commit|cherry-pick|revert|am|commit-tree` (word) -> COMMIT, `update-ref` with HEAD, --stdin or refs/heads/* -> COMMIT (:698-701); `alias.|pushurl|insteadof|hookspath|remote.|url.|include|includeif| set-url` -> UNKNOWN (:587); unknown subcommand -> UNKNOWN (:708). Known read-ish subcommands list at :704. Canonical push regex only allows `git push [-u|--set-upstream] origin <branch>[:<dst>]` (:716); dst master|main -> PROTECTED; dst HEAD or any non-matching form -> PUSHFORM (:717-722).
- gh (:550-663): `gh api` allowed only as one plain GET form (:554-578) else GHWRITE; merge|update-branch|sync -> MERGE (:646); alias|extension|$ -> UNKNOWN (:647); view/list/status/diff/checks/watch/checkout allowed (:649); `pr create|edit|comment|ready`, `issue create|edit|comment` -> SUBMIT (:650); other -> UNKNOWN (:651); `pr create` with no `-R/--repo <value>` -> REPO (:654-663); a word containing `repos/.../merge(s)` -> MERGE, `api.github.com`/`uploads.github.com` -> GHWRITE (:617-620).

### 1.7 G2 rule 2 (bound worker may use `orchestration send|ask` only with no `--to`)
- Code: orca verb pair `orchestration send` / `orchestration ask` sets `LL_SA=1` (:485); decided on the raw command at :496-537. The comment at :496-497 states the rule 1 text of the design is retired and "the commands it classed as TAMPER no longer exist".
- Rule: raw command must be one `orca orchestration send|ask` call of plain words and quoted strings with no expansion (:502-504); no newline; <= 8192 bytes; <= 64 arguments (:506-512); each argument must be an option or an option's value (:517-533). Any option beginning `--to`, `--run`, `--environment` or `--pairing-code` -> ESCAPE (:524); a name that is a prefix of `--to` or `--run` (`--t`, `--r`, `--ru`, `--=`) -> ESCAPE (:527); a bare word, short option or lone `--` -> ESCAPE (:532). `--json` takes no value (:529). Otherwise allowed at every level (class ESCAPE is simply not added).
- This rule is separate from the L1 `ESCAPE` default; at W it still applies to orchestration send/ask, so a bound worker at worktree level may send.

### 1.8 Key Takeaways
- The level is read ONLY from `~/.claude/state/launch-level/sessions/<session_id>` (file), never from env or the ccsession shim.
- Exit 0/2 only; governed sessions fail closed (LL-BROKEN, LL-NOBIND), ordinary sessions and identity loss fail open.
- 18 block words (16 classes in the precedence list at :783, plus LL-NOBIND for a failed binding and the catch-all LL-BROKEN), one level grid at :785-803.
- IMPL list in code is 3 skills (implement, task, cleanup).
- G2 rule 2 is BUILT in the guard; G2 rule 1 is retired in the guard (comment only).

## 2. Job identity: launch-job-identity.sh (582 lines) [READ-ONLY-READING; read in full]

Path: SNAP/src/superclaude/hooks/scripts/launch-job-identity.sh. A bash prologue (:1-54) plus an embedded Python program (heredoc :55-581) run as `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"` (:582). Not a sandbox (:2).

### 2.1 Subcommands (main :541-572)
- no args or `hook` -> `hook()` (the PreToolUse(Bash) adapter, :430-505).
- `execute SESSION TOOL_ID COMMAND` (exactly 4 args) -> `execute()` (:508-538): validates the request, requires the session to be governed, publishes a single-use request file and runs it.
- `identify [PID]` (1-2 args) -> prints one JSON line from `identify(pid)` and returns 0 (:546-553). A non-integer PID gives `{"status": "unknown"}`.
- `prepare SESSION COMMAND [TOOL_USE_ID]` (3-4 args) -> publishes a request, prints its 32-hex token (:554-569).
- `run TOKEN` -> `run()` (:378-414): consumes the request (flock, unlink on read), forks a supervisor.
- Anything else -> ValueError -> stderr `launch job: invalid invocation or unavailable private state`, exit 2 (:572, :575-580).

### 2.2 The command rewrite (hook, :430-505)
- Reads at most 1 MiB + 1 of stdin; over 1 MiB -> return 0 (:433-435); unparseable JSON -> 0 (:436-439); non-object -> 0; `tool_name` a string other than `Bash` -> 0 ("Monitor and other named tools have no adapter", :442-444); invalid `session_id` -> 0 (:445-447); HOME not absolute -> 0; `sessions/<sid>` does not exist (lexists) -> 0 (:451-453).
- Once a session record exists: store ownership and mode checks (`store()` :102-122, `private()` :81-84: owned by euid, no group/other bits; opened O_NOFOLLOW), the record must hold one of the 3 level words (`governed()` :177-186, LEVELS :74), JSON must have no duplicate fields and no non-JSON constants (:459), `hook_event_name == PreToolUse`, size <= 65536 (:462), `agent_id`/`agent_type` strings only (:464-466), `tool_input` an object (:467-469), command <= 32768 bytes and without NUL (:197).
- Rejects a command that names this script followed by `run|hook|execute` (:473-476).
- Preconditions: Linux and `fcntl` (:477), `/proc` stat and boot id (:479-480), pidfd support (:481), prctl subreaper (:482-484), runner script readable (:485), `/bin/bash` executable (:487).
- Output: `hookSpecificOutput.updatedInput` with the command replaced by `shlex.join(['/bin/bash', script, 'execute', sid, tool_use_id or '', original_command])` (:491-497); no `permissionDecision` is set (header :14-15) so the normal permission checks still apply. `additionalContext` tells the model each call is a fresh bash and `cd` does not persist (:497).
- Any failure after the record exists -> stderr `launch job: governed Bash call cannot be wrapped safely`, exit 2 (:500-502). So governed = closed.

### 2.3 Prologue fail modes (:20-54)
- Hook mode with no `$HOME` or no `~/.claude/state/launch-level` -> exit 0 at once (:20-24): ordinary sessions never need UV.
- No `uv` on PATH (:25-54): in hook mode a `jq` fallback checks for an exact top-level Bash payload with a valid session id whose `sessions/<sid>` record is an owned regular non-symlink file under owned non-symlink directories; if jq is absent or any check fails -> exit 0; if all pass -> stderr `launch job: UV is required for this invocation`, exit 2. Non-hook modes without uv -> exit 2 straight away.

### 2.4 State files under ~/.claude/state/launch-level/ read and written here
- `sessions/<sid>`: read only (level word) via `governed()`.
- `requests/<32 hex token>`: written by `publish()` (:164-174; temp name `.<uuid>` O_EXCL, mode 0400 after `fchmod`, hard link to the final name), consumed once by `read_file(..., consume=True)` (:140-159: flock LOCK_EX|LOCK_NB, link count must be 1, then unlink).
- `jobs/<kernel-sid>.json`: written by the supervisor `supervise()` (:307-375), record keys exactly `pid, start, boot, kernel_sid, session_id` (:315-316, validated at :231); removed in the `finally` only when no member process remains (:373-375).
- Directories `requests` and `jobs` are created with mode 0700 by `subdir(..., create=True)` (:125-130).
- `pending/` is NOT touched by this script.

### 2.5 `identify` (:215-260) output values
`{"status": "ordinary"}` (no job record for the process's kernel session id, :228-229); `{"status": "ordinary", "reason": "released"}` (the job record is valid but `sessions/<sid>` is gone, :252-255); `{"status": "governed", "session_id": "<sid>"}` (:256); `{"status": "unknown"}` (store unreadable before the record path is known) or `{"status": "unknown", "reason": "stale|orphaned|foreign|unreadable", "record": "<path>"}` (:257-260). Reasons: orphaned = supervisor missing or zombie (:240, :243); stale = sid or start-time or boot-id mismatch (:246-248); foreign = supervisor not owned by euid (:249-251); unreadable = default (:220).

### 2.6 Declared limits (header :7-18; not tested live here)
Deliberate `setsid` or daemonising escapes selection (:7-8); Monitor and pipelines unsupported (:9); cd does not persist across governed Bash calls (:16-18); rewrite ordering with other hooks "unspecified" (:15); live auto-mode behaviour unverified (:497).

### 2.7 Writes to GitHub
None. No `gh`, `curl` or network call exists in this file (grep `gh |curl|api.github` on the file, see section 12 evidence).

### 2.8 Key Takeaways
- Identity decides governed/ordinary for a PROCESS (git hook), not for a Claude session; it works by rewriting every governed Bash call to run under a supervisor that owns a kernel session whose id is the lookup key.
- Closed for governed (exit 2 on any wrap failure), open for ordinary and for anything it cannot recognise as a bound Bash call.
- State written: `requests/` and `jobs/` only; `sessions/` read only.

## 3. L2 pre-push hook template: launch-level-pre-push.sh (208 lines) [READ-ONLY-READING; read in full]

Path: SNAP/src/superclaude/hooks/scripts/launch-level-pre-push.sh. Shebang `#!/bin/bash -p` (:1); `# launch-level-pre-push-version: 1` (:2). A git hook (event = `git push` run in the hooks directory), not a Claude Code hook.

- Install point: "Installed by the claim as <git-common-dir>/hooks/pre-push next to its data file pre-push.launch-level (line 1: pinned HOME, line 2: pinned uv directory)" (:4-5). Installed by `orca_worktree.py` (section 5.4 below checks `install_l2`); NOT in hooks.json (section 4).
- Data file rules (`l2_data` :29-48): `pre-push.launch-level` beside the hook (`L2_HOOKS=${0%/*}`, :18-19), regular, not a symlink, owned by the euid, mode has no group/other write bit, size <= 8194, exactly two newline-terminated absolute path lines, no NUL.
- Actor (`l2_actor` :52-101): runs `$L2_HOME/.claude/hooks/launch-job-identity.sh identify $$` in `cd /` under `env -i HOME=<pinned> PATH=<uvdir>:/usr/bin:/bin UV_NO_CONFIG=1 timeout 10` with stdin from /dev/null (:65). Missing/unexecutable script -> unknown ("identity script missing"); timeout rc 124 -> unknown ("identity check timed out"); other nonzero -> unknown ("identity check failed"); the single output line is matched against five exact JSON shapes (:82-88): ordinary and ordinary+released -> `ordinary`; governed -> `governed`; plain unknown or unknown+reason+record -> `unknown`; anything else unknown.
- Ordinary -> `exit 0` immediately, stdin never read (:188).
- Reading stdin (`l2_read` :167-185) in 4096-byte chunks, one record per line, `l2_check` (:118-137) names the first failed check (blank line; tab, CR or NUL; fewer than three spaces; empty field; object id not 40 or 64 lowercase hex; object ids of different length; destination not `refs/<x>/<y>`).
- Protected refs: only `refs/heads/main` and `refs/heads/master` (`L2_PROTECTED` :17).
- Outcomes (:187-208): malformed record from a non-ordinary actor -> message `L2-MALFORMED` , exit 2 (:192-195); no protected ref -> exit 0 (:196); governed + protected -> `L2-PROTECTED` exit 1 (:197-200); unknown actor + protected -> `L2-UNKNOWN` exit 1 plus a route text naming `rm '<record>'` only for reason `stale` (:201-208). Pushes to any other ref are allowed for every actor ("pushes to other refs are allowed", :207).
- Exit codes here: 0 allow, 1 refuse protected, 2 refuse malformed stream (header :9-10). This is the only hook in the area that exits 1.
- No file is written and git is never called (:10). Linux only (:11).
- Writes to GitHub: none.

Key Takeaways
- L2 is a second, independent check at the git layer for pushes to main/master only; the feature-branch push control (commit/push/submit classes) lives only in L1.
- Closed vocabulary for L2: L2-PROTECTED, L2-UNKNOWN, L2-MALFORMED.
- Actor information comes from the job-identity selector, never from the environment.

## 4. hooks.json registrations and install_hooks.py [READ-ONLY-READING; both read in full]

### 4.1 src/superclaude/hooks/hooks.json (192 lines)
| Event | Matcher | Command | Timeout | Lines |
|---|---|---|---|---|
| SessionStart | none | `~/.claude/hooks/session-init.sh` | 10 | :3-12 |
| SessionStart | `*` | `freshness-session-start.sh` | 5 | :13-22 |
| SessionStart | `startup` | `codegraph-session-start.sh` | 5 | :23-32 |
| SessionStart | `startup|resume` | `~/.claude/skills/ccsession-tag/hooks/session-start.sh` | 5 | :33-42 |
| UserPromptSubmit | none | `freshness-user-prompt.sh` | 3 | :45-53 |
| UserPromptSubmit | none | `~/.claude/skills/ccsession-tag/hooks/session-name.sh` | 5 | :54-62 |
| UserPromptSubmit | none | `~/.claude/hooks/launch-level-guard.sh` | 5 | :63-71 |
| SessionEnd | none | ccsession-tag `session-name.sh` | 5 | :73-83 |
| PreToolUse | `Edit|Write` | `freshness-pre-edit.sh` | 1 | :85-94 |
| PreToolUse | `Bash` | `block-bare-python.sh` | 3 | :95-104 |
| PreToolUse | `Bash` | `require-orca-worktree-agent.sh` | 3 | :105-114 |
| PreToolUse | `^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)` | `~/.claude/hooks/launch-level-guard.sh` | 5 | :115-124 |
| PreToolUse | `Bash` | `~/.claude/hooks/launch-job-identity.sh` | 5 | :125-134 |
| PostToolUse | `Read`; auggie/augment matcher | `freshness-post-read.sh` (async), `auggie-flag-clear.sh` | 1 | :136-157 |
| SubagentStart | none | `freshness-subagent-start.sh` (1), `node "$HOME/.claude/hooks/pragmatic-subagent.js"` (5) | | :159-178 |
| SubagentStop | none | `freshness-subagent-stop.sh` (async) | 1 | :179-190 |
- The launch-level guard is registered twice (UserPromptSubmit and PreToolUse). The identity hook is registered once (PreToolUse, Bash) and comes AFTER the guard in file order (:125 after :115). No registration has an `onFailure` key (grep in test_launch_level_guard_registration.py pins this; hooks.json text has none).
- `launch-level-pre-push.sh` is NOT registered in hooks.json: grep of hooks.json finds only `launch-level-guard.sh` and `launch-job-identity.sh` (see the table). It is a git hook installed by `install_l2` (section 5.4).
- Plugin copy `plugins/superclaude/hooks/hooks.json` (154 lines): `cmp`/`diff` on the snapshot gives these differences from src: (a) it lacks the ccsession-tag `session-start.sh` SessionStart entry, the ccsession-tag `session-name.sh` UserPromptSubmit entry and the SessionEnd block; (b) it lacks the `pragmatic-subagent.js` SubagentStart entry; (c) its `freshness-subagent-start.sh` entry has `"async": true` (src has not). The three launch-level registrations (UserPromptSubmit guard, PreToolUse guard with the same matcher, PreToolUse identity) are the same text in both. **[STALE DOC]** the scope hint said the plugin copy differs only by ccsession-tag entries; code shows two more differences (b, c) [CODE-CONTRADICTED, verified by `diff` read-only].
- Plugin script copies: `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, `launch-job-identity.sh`, `launch-level-pre-push.sh` all exist and `cmp -s` against the src copies returns identical for all three [OBSERVED-BY-CMP, read-only, run in this session]. These are the only `launch-*` files under `plugins/`.

### 4.2 install_hooks.py (614 lines)
- Module docstring (:1-19): copies scripts to `~/.claude/hooks/`, merges registrations into `~/.claude/settings.json` additively and atomically, backup before write, refuses a malformed target.
- `_FRESHNESS_SCRIPTS` (:42-97) contains `launch-job-identity.sh` (:90), `launch-level-guard.sh` (:93) and `launch-level-pre-push.sh` (:96); the comment on :94-95 says the pre-push script is "installed into a worktree's hooks/pre-push by the Orca launcher, never registered in settings.json". `_LEGACY_SCRIPTS = ["session-init.sh"]` (:98). `_SEED_FILES` has one entry, `auggie-projects.txt.example` -> `auggie-projects.txt` (:104-106), never overwritten.
- `install_hooks(target_path=None, force=False)` (:156-246): Step 1 `_copy_scripts` (:254-293); Step 2 `_merge_settings` (:301-494); Step 3 seed files (:559-590). Returns `(overall, message)` with overall = settings merge ok AND no copy failures (:244-246).
- Skip-if-exists unless force: `if dest_file.exists() and not force: skipped.append(...)` (:282-284); otherwise `shutil.copy2` then `os.chmod(dest, 0o755)` (:286-289). A missing source is a failure line (:278-280).
- Settings merge (:384-474): ownership by command path, not matcher (:405-418). Owned and not force -> skipped as collision (:420-422). Owned and force -> the registration is refreshed in place, keeping any user-only remainder (:424-458). A matcher-only collision keeps the user entry and inserts the framework entry before the first registration owned by a LATER source entry, "so launch-job-identity.sh stays last" (:460-473). Backup `settings.json.bak.<UTC stamp>` before any write (:336-346, `_backup_path` :529-532); malformed or non-object target refused (:348-367); `_atomic_write_json` uses a same-directory temp file and `os.replace` (:510-526).
- Callers: `main.py:219` `install_hooks(force=force)` (install), `main.py:412` `install_hooks(force=True)` (update), and `cli/eval/hook_adapter.py:230` `install_hooks(target_path=settings_path, force=False)` (eval HOME) [CODE-VERIFIED by grep]. So a plain `superclaude install` keeps an older guard on disk; `superclaude update` and `install --force` refresh it. The claim's IR-4 preflight refuses a stale guard lacking `# launch-level-guard-version: 1` and says `run superclaude install --force` (orca_worktree.py:962, :986-988).
- The installer never creates `~/.claude/state/launch-level/`: grep of install_hooks.py has no `launch-level` store path; the store is created by the claim (`publish_pending`, orca_worktree.py:1490-1501) and by the guard (`mkdir -p sessions`, guard :368) and identity (`subdir(..., create=True)`, :125-130).
- The guard also treats text naming `install_hooks` or `superclaude ... install` as TAMPER for a governed session (guard :440, :451), so a governed agent cannot re-run the installer.
- Writes to GitHub: none (no network or `gh` use; grep G6/G7 of the batch found no match for gh/curl/wget in install_hooks.py or install_ccsession.py).

Key Takeaways
- Registration is by `superclaude install` merging hooks.json into `~/.claude/settings.json`; scripts are skipped if they exist unless `force` (update uses force=True).
- The pre-push hook is installed as a script copy only; it is wired into a git clone by the claim, not by settings.
- Plugin hooks.json carries the same three launch-level registrations; plugin script copies are byte-identical.

## 5. ccsession coupling [READ-ONLY-READING unless marked]

### 5.1 install_ccsession.py (161 lines)
`wire_ccsession(home=None) -> (ok, message)` (:11): requires `~/.claude/skills/ccsession-tag/` to exist as a real directory (not a symlink) with `ccsession`, `hooks/session-start.sh`, `ccsession.env.example` regular non-symlink files (:19-31). Symlinks `ccsession` and, if present, `ccsession-orca` into `~/.local/bin` (:33, :41, :61-71; a foreign file at the link path is left alone and reported "unmanaged", :64-68). Seeds `~/.claude/ccsession.env` with mode 0600 using a no-replace `os.link` (:72-88). Runs `unseed-env.py` (:92-99), `retention.py ensure` against `~/.claude/settings.json` (:105-125) and `ccsession --migrate-names` when the wrapper knows it (:131-142) through `subprocess.run` with timeouts of 30 or 60 s. Copies `session-name.sh` beside an older skill (:46-47, :56-57). It registers NO hooks (those come from hooks.json via install_hooks.py). Callers: `main.py:211` (install) and `main.py:406` (update).
- No launch level, no `pending`, `sessions`, `sc-launch` or `launch-level` text exists in the file (grep of `launch-level|sc-launch` found only install_hooks/orca files; install_ccsession.py has none).

### 5.2 The shim carries NO launch level [CODE-VERIFIED]
`grep -rn -E 'launch-level|sc-launch|LAUNCH_LEVEL|launch_level'` over `SNAP/src/superclaude/skills/ccsession-tag` returned zero lines [OBSERVED-BY-GREP, read-only, run in this session]. `ccsession-orca` (263 lines) sets `CCSESSION_ORIGIN=human|agent` (:198-256) and unsets `CCSESSION_NAME` and `CCSESSION_ASK_TIMEOUT` before Claude (:249); it never touches the launch store. The guard reads only HOME (guard :23) and identity reads HOME only (identity :103). So the level travels ONLY by files: `pending/<nonce>` -> prompt marker `[sc-launch:v1:<nonce>]` -> `sessions/<session_id>`.
- ccsession-orca role: Orca's Claude command (header :2-12), classifies the launch (:56-125), honours CCSESSION_NAME (:127-139), asks for a session name only when no task, name or resume is carried and a terminal exists (:141-155), reopens an Orca tab's session (:164-191), computes `origin` (:195-220), derives an auto-name from the task text with `ccsession --auto-name` (:232-236), then `exec ccsession [--name N] --shim --claude-args "$@"` (:259-263). The launch prompt passed by the claim therefore becomes the auto-name seed, which is why the session/tab title starts `sc-launch-v1-<nonce12>-...` (orca_worktree.py:793-797).

### 5.3 What the claim does with the shim (detection only) (orca_worktree.py)
- Constants: `SHIM_MARKERS = ("[ccsession]", "Session name (Enter or Ctrl+C")` (:792); `SHIM_TITLE = re.compile(r"sc-launch-v1-[0-9a-f]{1,12}-\d{4}-\d{6}-[0-9a-f]{4}\b")` (:797); `SHIM_TRIES = 5` (:798); interval env `SC_ORCA_SHIM_INTERVAL`, default 2.0 s (:799-800).
- `behind_ccsession(handle)` (:1564-1583): up to five times it runs `orca terminal read --terminal <handle> --screen --json` and looks for either marker; on a miss it runs `orca terminal show --terminal <handle> --json` and matches the title against SHIM_TITLE (`ccsession_title` :1551-1561); sleeps between tries.
- `cmd_launch` (:1802-1811): if there is no handle or the shim is not seen, adds warning `W-LAUNCH-NOT-CCSESSION` (text "the agent's screen showed no ccsession text" or "the launch result named no terminal"). The launch itself is NOT undone or refused; the warning stays first in the notes (:1825). Remedy text (REMEDY :804-807): "this agent is NOT behind the ccsession shim, or could not be verified; close it. Orca's Claude command must be the ccsession-orca wrapper".
- So the claim DETECTS the shim; it does not set or require the level through it. A launch without the shim still writes `pending/<nonce>` and the marker, so the guard still binds the session (shim and guard are independent).

### 5.4 Who installs L2 and when (orca_worktree.py)
- `install_l2(wt)` (:1386-1442): finds the git common hooks directory, writes `pre-push.launch-level` (data file; `publish_no_replace` mode 0644, :1411) and a private staged copy of `pre-push` (0755) which is self-tested by `_l2_selftest` (:1423) and then hard-linked as `hooks/pre-push` with `os.link` (:1428); an existing `pre-push` is never replaced or deleted (:1403-1404). Returns installed/owned/conflict/unsupported/unavailable.
- Called once, from `cmd_launch` at :1754, after the IR-4 preflight (:1730-1747) and before `publish_pending` (:1761). `l2_status(wt)` (:1048-) is the read-only check that the launch reports (:1755). Warning `W-L2-ABSENT` is raised when state != owned (:1756) but `IR7_REFUSE` is False (:822), so the launch proceeds (:1757-1758 is the dead refusal branch).
- The hook is thus installed by the CLAIM at launch time, not by `superclaude install` (which only copies the template to `~/.claude/hooks/launch-level-pre-push.sh`, install_hooks.py:96) and not by any hook registration.

Key Takeaways
- ccsession coupling is detection-only (screen text or tab title); the shim passes the prompt text through, which is how the marker reaches Claude.
- `W-LAUNCH-NOT-CCSESSION` is a warning, not a refusal.
- `install_l2` is called only from `cmd_launch` (:1754).

## 6. Built-versus-retired ledger (status words: BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED)

"BUILT-ON" below means: the code exists in the snapshot AND it is wired into a path that runs in a normal install (hooks.json registration, installer entry, or a call from the claim). It does not say that a given machine has run `superclaude install`; no machine state is visible in the snapshot.

| Piece | Status | Evidence |
|---|---|---|
| L1 guard (launch-level-guard.sh) | BUILT-ON | Registered on UserPromptSubmit (hooks.json:63-71) and PreToolUse (:115-124); copied by install_hooks.py:93; IR-4 preflight in the claim requires it (orca_worktree.py:955-1045). It governs only a session bound through a claim launch marker; everything else exits 0 (guard :391). |
| Job identity (launch-job-identity.sh) | BUILT-ON | Registered PreToolUse Bash after the guard (hooks.json:125-134); copied by install_hooks.py:90; IR-4 requires its registration (orca_worktree.py:1037-1044). Linux and `uv` needed. |
| L2 pre-push hook (launch-level-pre-push.sh) | BUILT-ON, claim-installed only | Template copied to `~/.claude/hooks/` (install_hooks.py:96); written into a clone's hooks directory by `install_l2` called from `cmd_launch` (orca_worktree.py:1754). Not in hooks.json. Only a claim launch at `worktree` or `full` calls it. |
| G2 rule 2 (bound worker: `orchestration send|ask` only with no `--to`) | BUILT-ON | guard :485, :496-537; plugin copy identical; pinned by test_launch_level_guard_worker.py; WORKER-CONTRACT.md:66 states the rule. OBSERVED allow/deny in the observation run (G2-A..G2-D). Nothing binds a coordinator-started worker (see G1 and Defect Candidates DC-1). |
| G1 (a worker started by a coordinator runs with no marker, so no guard) | NOT BUILT (as a guard); it is the live condition for coordinator-started workers | docs/designs/issue-pipeline-fu1.md:18, :113; docs/designs/orchestrator.md:117 (DQ7: "these workers run with no L1 guard and no L2 pre-push hook"); no caller of `orca_worktree.py pending` (grep, section 12). |
| G2 rule 1 / route A (coordinator writes the worker's `.ok` through a helper such as `release-worker`) | REMOVED | grep for `release-worker|release_worker` over src, tests and plugins: zero hits [OBSERVED-BY-GREP]; `src/superclaude/cli/issue_pipeline/` and `tests/issue_pipeline/` absent [OBSERVED-BY-LS]; guard comment :496-497 "the rule 1 text of that design is retired, the commands it classed as TAMPER no longer exist"; removal recorded in docs/designs/orchestrator.md:991, :1095. The only writer of `<sid>.ok` is the guard's typed-prompt branch (guard :358). |
| G2 route B (signed approval file read by the guard) | NOT BUILT | design only (issue-pipeline-guard-g2.md:24, recommendation route A at :26). grep `signature|signed|hmac|openssl` in the guard and identity scripts: zero hits [OBSERVED-BY-GREP]. |
| FU-1 (first live test runbook for the claim handoff) | REMOVED (its e step commands); record present as text | docs/designs/issue-pipeline-fu1.md:64 runs `uv run superclaude issue-pipeline plan-hash` and `check-approval`; no `issue_pipeline` in cli/main.py (grep zero hits) and the directory is absent. The file carries RECORDED lines a to k dated 2026-11-17 (fu1.md:108-119) and `RUN BY OWNER` (:119); those are the file's own claims, [UNVERIFIED] here. |
| IR-3 (`pipeline.json` written by the claim) | NOT BUILT | design says "IR-3 documentation only: no code writes pipeline.json" (sc-issue-launch-level-hook.md:34, :615); grep `pipeline\.json` over src and plugins (py, sh, md, json): zero hits [OBSERVED-BY-GREP]. |
| IR-4 (enforcement preflight) | BUILT-ON | `enforcement_preflight` (orca_worktree.py:955-1045); refusal `W-ENFORCEMENT-ABSENT` in `cmd_launch` (:1730-1747). |
| IR-7 (refuse the launch when L2 is not owned) | BUILT-OFF (enabled:false equivalent) | `IR7_REFUSE = False` (orca_worktree.py:822, comment "turn on only after the #442 observations pass (owner decision 2026-11-08)"); refusal branch `if IR7_REFUSE and l2_notes:` (:1757-1758) is never taken; warning `W-L2-ABSENT` only; pinned by test_issue_l2_install.py:639-641 `test_ir7_shipped_switch_is_off`. |
| OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX (live observations) | NOT BUILT (never run) | tests/hooks/test_launch_level_observations.py:79-84: `_PENDING` has 12 entries, `test_pending_live_observation` calls `pytest.skip(f"{item}: needs a real governed session and has not been run")`; design sc-issue-launch-level-hook.md:6, :625 "Pending, none run". No code in orca_worktree.py checks an observation record (grep `OB-H|OB-CTX|observation` over claim scripts: only the IR7 comment at :822). The log-only probe and nine synthetic fixtures exist (test lines 32-76, six tests, five of which run). |
| ccsession coupling | BUILT-ON (detection only) | install_ccsession.py (main.py:211, :406); `behind_ccsession` (orca_worktree.py:1564-1583); warning only (:1802-1811). Shim carries no level (section 5.2). |

Key Takeaways
- Live guard code: L1, identity, L2 template, G2 rule 2 all BUILT-ON; only claim launches at `worktree` or `full` ever create a governed session.
- Removed: G2 rule 1 / route A, and everything in `issue_pipeline/`. Not built: route B, IR-3, live observations. Off: IR-7 refusal.

## 7. Writes to GitHub (deliverable c)

**No GitHub write in this area.** Evidence:
- `launch-level-guard.sh`: no line begins with a `gh`, `curl`, `wget`, `git`, `orca` or `uv` command word (grep `^\s*(gh|curl|wget|git|orca|uv)\s` zero hits); `gh` and `git` appear only inside regular expressions and `case` patterns that classify the agent's command. Tools it executes: `jq`, `sed`, `tr`, `cat` (via `$(cat)`), `mkdir`, `mv`, `ln`, `rm`, `printf` (guard :166-205, :291-302, :428-434).
- `launch-job-identity.sh`, `launch-level-pre-push.sh`, `install_hooks.py`, `install_ccsession.py`, `ccsession-orca`, `session-start.sh`: grep for `gh`, `curl`, `wget`, `nc` as a command word gave zero hits; install_ccsession.py imports `subprocess` and uses it only for `unseed-env.py`, `retention.py` and `ccsession --migrate-names` (:94, :108, :133); install_hooks.py imports no network or subprocess module.
- `orca_worktree.py` (the writer side of this area): `run([...])` first words are only `git` and `orca` (grep `run(["...` counts: `git` 4, `orca` 2; a `["gh"` grep found nothing). Its commands touching this area: `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` (:1777-1780), `orca terminal read --terminal <h> --screen --json` (:1568), `orca terminal show --terminal <h> --json` (:1554), `git -C <wt> rev-parse --absolute-git-dir` (:1593). The claim's GitHub and ClickUp writes belong to the claim protocol (research agent 04), not to this area.
- The guard BLOCKS an agent's own GitHub writes (SUBMIT, GHWRITE, MERGE, MCP) below `full --submit`; at `full --submit` it allows `gh pr comment|edit|ready|create --repo`, `issue create|edit|comment` and canonical pushes, but those are the agent's commands, not this area's.

## 8. Triggers (deliverable d)

| Piece | What starts it |
|---|---|
| L1 guard | Claude Code event UserPromptSubmit (every prompt) and PreToolUse for the matcher in hooks.json:116; present only if `superclaude install` merged hooks.json into `~/.claude/settings.json` (install_hooks.py `_merge_settings`) |
| Job identity hook | Claude Code PreToolUse with matcher `Bash` (hooks.json:126). Its `execute` mode is started by the rewritten command it returns; its `identify` mode is started by the L2 pre-push hook (pre-push :65) |
| L2 pre-push hook | git `pre-push` event on `git push` in a clone where `install_l2` placed `hooks/pre-push`; `install_l2` is called by `cmd_launch` (orca_worktree.py:1754) |
| `superclaude install` / `update` | A person runs the CLI: install_hooks via main.py:219 (install, force flag) and main.py:412 (update, force=True); wire_ccsession via main.py:211 and :406; install_hooks also via cli/eval/hook_adapter.py:230 (force=False) |
| ccsession-orca | Orca runs it as the Claude command (person configures Orca Settings > Agents > Claude > Command, ccsession-orca header :7-12); the claim triggers it through `orca agent launch --agent claude` (orca_worktree.py:1777) |
| ccsession hooks | SessionStart (startup, resume), UserPromptSubmit and SessionEnd (hooks.json:33-42, :54-62, :73-83) |
| `publish_pending` | `cmd_launch` (:1761); `pending` subcommand (`cmd_pending` :1515, argparse :1886-1893), which no file in src or plugins calls (section 12) = "no trigger found in snapshot" other than a person or coordinator typing it |
| `behind_ccsession` | `cmd_launch` after a successful `orca agent launch` (:1803) |
| Claim itself | `/sc:issue --claim` Wave 8 (SKILL.md:92) when `--pipeline` is not `none`; the watcher launches the claim with `--pipeline none` (research notes; not re-read here), so the watcher path creates no governed session |

## 9. State stores (deliverable e)

Root: `$HOME/.claude/state/launch-level/` (guard :20-23; claim `PENDING_PARTS` orca_worktree.py:791; identity `store()` :102-122).
| Path pattern | Writer | Readers | Format and mode |
|---|---|---|---|
| `pending/<32 hex nonce>` | `publish_pending` (orca_worktree.py:1488-1512; also `pending --level`) | guard prompt branch (:334-337, `mv` at :374); claim deletes it on launch failure (:1783) | one level word (`worktree`, `full`, `full-submit`), no newline; temp name `.tmp-<nonce>` created O_EXCL 0600 then `os.replace`; directory 0700 |
| `sessions/<session_id>` | guard `ln` hard link of the taken pending record (:299-313, :376) or `ll_publish degraded` (:289-297, :306, :378) | guard (:257-273), identity `governed()` (:177-186), pre-push via `identify` | one word, optional newline (read as 13 bytes); `degraded` is read as W with LL-STATE; mode inherits the pending file (0600 from the claim) or 0600 (ll_publish under umask 077) |
| `sessions/<session_id>.ok` | guard approval branch, noclobber `: >` (:356-359) | guard (:270) | empty; existence = approval; OBSERVED mode 600 |
| `sessions/.take-<session_id>`, `sessions/.tmp-<sid>-<pid>` | guard, temporary | guard | dot names are never valid ids; removed after use (:310, :295) |
| `requests/<32 hex token>` | identity `publish()` (:164-174) via `execute` or `prepare` | identity `run` (:378-385), consumed by unlink under flock | JSON `{session_id, tool_use_id, command}`; mode 0400; directory 0700 |
| `jobs/<kernel session id>.json` | identity supervisor (:307-375) | identity `identify` (:215-260); pre-push through `identify` | JSON with exactly keys `pid, start, boot, kernel_sid, session_id`; mode 0400; directory 0700; removed when no member process remains |
Other stores touched in this area:
- `~/.claude/settings.json` (merged by install_hooks.py; backup `settings.json.bak.<UTC stamp>`; atomic replace).
- `~/.claude/hooks/*.sh` (copied 0755; skipped if present unless force).
- `~/.local/bin/ccsession`, `~/.local/bin/ccsession-orca` (symlinks, install_ccsession.py:61-71); `~/.claude/ccsession.env` (0600, seeded, :72-88).
- `<git common dir>/hooks/pre-push` and `<git common dir>/hooks/pre-push.launch-level` (install_l2: data file 0644 `publish_no_replace` :1411; hook 0755 linked at :1428); the data file holds two absolute path lines, pinned HOME and uv directory.
- `<git dir>/sc-issue-launch-<N>.json` (claim launch mirror, orca_worktree.py:1586-1597), and the `launch` entry in the issue's record (record_launch :1619-1629); belongs to research agent 04.
- Guard permanence: no pruning of `pending/` or `sessions/` (design :627 "Pending launch records are not pruned: a person removes old state files (owner decision O-15)").
- Observation run sandbox (this research only): `research/05-guard-run-sandbox/home/.claude/state/launch-level/{pending,sessions}`.

## 10. Gates (deliverable f): every approval, refusal, cap, kill switch with exit code

| Gate | Exact condition | Word | Exit | Where |
|---|---|---|---|---|
| Typed approval at W | prompt first line matches `^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)`, bound session, level W, no `agent_id`, `.ok` not present | none (writes `.ok`, level W becomes WA) | 0 | guard :347-360 |
| Release (kill switch) | a person deletes `sessions/<sid>` and `sessions/<sid>.ok` | none; `identify` then reports `ordinary` + `released` | n/a | guard message :97; identity :255 |
| IMPL | Skill `implement`, `task` or `cleanup` (normalised) at W | LL-IMPL | 2 | :409, :788 |
| TURN | Cron*/Schedule* tool at W | LL-TURN | 2 | :739-740, :788 |
| SUBMIT | Skill `pr-submit`; `gh pr create|edit|comment|ready`, `gh issue create|edit|comment` below FS | LL-SUBMIT | 2 | :410, :650, :789 |
| COMMIT | git commit-class words below FS | LL-COMMIT | 2 | :585, :697-701, :789 |
| PUSH | git push-class words below FS | LL-PUSH | 2 | :583, :703, :790 |
| SKILL | Skill whose name cannot be read, below FS | LL-SKILL | 2 | :412, :790 |
| PUSHFORM | any push not exactly `git push [-u\|--set-upstream] origin <branch>[:<dst>]`, or dst `HEAD`, at EVERY level | LL-PUSH-FORM | 2 | :716-722, :792 |
| PROTECTED | canonical push whose dst is `master` or `main` (also `refs/heads/` or `heads/` forms) at EVERY level | LL-PROTECTED | 2 | :719-720, :793 |
| MERGE | `git merge|pull`, `gh pr merge|update-branch|sync`, merge endpoints, MCP merge tools, at EVERY level | LL-MERGE | 2 | :581, :646, :617, :751, :794 |
| GHWRITE | `gh api` that is not one plain GET, direct `api.github.com` words, at EVERY level | LL-GH-WRITE | 2 | :554-578, :620, :795 |
| REPO | `gh pr create` without `-R/--repo <value>` at EVERY level | LL-REPO | 2 | :654-663, :791 |
| UNKNOWN | unknown git or gh subcommand, alias/config forms, line continuation inside a word | LL-UNKNOWN | 2 | :426, :587, :647, :651, :708, :796 |
| MCP | `mcp__*` write-like tool name (not merge) | LL-MCP | 2 | :743-754, :797 |
| ESCAPE | `claude` plus a launch flag; `ccsession*`, tmux, screen, xdotool, ydotool; any `orca` verb off the allow-list (and any glob in an allow-listed verb); Agent/Task isolation remote; RemoteTrigger, Workflow, SendMessage; Skill `issue`; G2 rule 2 violations | LL-ESCAPE | 2 | :452-456, :480-491, :524-536, :738, :741, :411, :798 |
| TAMPER | text or edit path naming the store, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, git config files, `.git/hooks`, `hooks/pre-push`, `pre-push.launch-level`, `--no-verify`, `hookspath`, `hook.pre-push`, `install_hooks`, `superclaude ... install`, `..` in an edit path | LL-TAMPER | 2 | :440-451, :735, :760-775, :799 |
| BIG | Bash or Monitor command > 65536 bytes | LL-BIG | 2 | :419-420, :800 |
| NOBIND | marker prompt that cannot be bound (no id, unowned/symlink sessions dir, no jq, no regular session file after the attempt) | LL-NOBIND | 2 | :236, :367, :370, :384, :157 |
| BROKEN | governed session: jq failure on a tool payload with a bound id, input error flag, unknown event, internal error, default deny | LL-BROKEN | 2 | :232, :392, :281, :807-808, :159 |
| Hook time limit | hooks.json `timeout: 5` for guard and identity; a killed hook allows the call (design V8/R2, not testable here) | none | n/a | hooks.json:68, :121, :131 |
| G2 rule 2 caps | raw `orca orchestration send|ask` command <= 8192 bytes, <= 64 arguments, no newline, no `--to*`, `--run*`, `--environment*`, `--pairing-code*` or a prefix of `--to`/`--run` | LL-ESCAPE when violated | 2 | :506-536 |
| Identity wrap failure | governed Bash call that cannot be wrapped | stderr `launch job: governed Bash call cannot be wrapped safely` | 2 | identity :500-502 |
| Identity no UV | bound session, no uv, jq verified binding | stderr `launch job: UV is required for this invocation` | 2 | identity :25-54 |
| Identity bad invocation | any other error | stderr `launch job: invalid invocation or unavailable private state` | 2 | identity :575-580 |
| L2 protected | governed actor, record to `refs/heads/main` or `master` | `L2-PROTECTED` | 1 | pre-push :197-200 |
| L2 unknown | unknown actor, same refs | `L2-UNKNOWN` | 1 | :201-208 |
| L2 malformed | any malformed record, governed or unknown actor | `L2-MALFORMED` | 2 | :192-195 |
| Claim IR-4 refusal | jq/uv/guard commands missing, guard not executable or lacking version line, registrations not firing for the governed tools, `disableAllHooks` true, CLAUDE_CONFIG_DIR mismatch, no Linux process interfaces | `W-ENFORCEMENT-ABSENT` (launch refused, no pending record, no agent) | json `launch_result status failed` | orca_worktree.py:955-1045, :1730-1747 |
| Claim IR-7 | L2 not owned | `W-L2-ABSENT` warning only | launch continues | :1754-1758, :822 |
| Claim shim check | no ccsession screen text or title | `W-LAUNCH-NOT-CCSESSION` warning only | launch continues | :1802-1811 |
| Installer refusals | malformed or non-object `settings.json`; non-dict `hooks`; non-list event | message `refusing to write` | `(False, msg)` | install_hooks.py:348-396 |
Kill switch for the whole guard: none besides a person deleting `sessions/<sid>[.ok]`; `disableAllHooks: true` in a settings file disables every hook (the claim refuses to launch when it sees it, orca_worktree.py:1008-1012).
Exit-code rule (CODE-VERIFIED): L1 guard and identity hook use only 0 and 2 (guard :4-6; identity returns 0 or 2 at :435-502, :580); the L2 git hook uses 0, 1 and 2 (pre-push :9-10).

Key Takeaways
- 16 block classes plus LL-NOBIND and LL-BROKEN (18 words, pinned by test_design_table_holds_all_eighteen_ids); 10 classes block at every level including FS.
- Only exit 2 blocks in Claude Code hooks; L2 exit 1 is git's refuse code.

## 11. Test pins (deliverable a)

Counts: `wc -l` and `grep -c -E '^\s*(async )?def test_'` on the snapshot [OBSERVED-BY-GREP, read-only]; parametrized tests make real case counts higher. Test files were read by header, banners, parametrization tables and names; no test was executed (the snapshot is read-only and pytest would write caches).

### 11.1 One row per test file in the assignment
| Path (under SNAP/tests/) | Lines | `def test_` | What it pins | Key test names |
|---|---|---|---|---|
| hooks/test_launch_level_guard.py | 4631 | 162 | Real script run with JSON on stdin and HOME in `tmp_path`; script text (executable, version line, never names the joined store path, `bash -n`); ordinary sessions never blocked; event dispatch and identity loss; EXIT trap fault injection; binding B1-B13 and concurrency; Skill classifier; the hand-written level grid; fail-closed resolution; the 18 message texts against design section 9 (design text read at run time, :72-85); Bash normalisation NM1-NM7; git and gh classifiers; tamper/escape; TURN, MCP, Agent/Task; typed approval; regression corpora; precedence | `test_grid_policy` (:3394), `test_grid_complete` (:3401), `test_grid_level_steps` (:3457), `test_skill_grid_matches_oracle` (:905), `test_impl_name_spellings` (:927), `test_lookalike_skill_names_stay_none` (:936), `test_bind_marker_with_record_binds_level` (:439), `test_bind_nonce_single_use` (:544), `test_trap_in_tool_branch_gives_broken` (:389), `test_apr_matching_prompt_writes_ok_at_w` (:3737), `test_apr_ok_written_only_at_worktree` (:3766), `test_apr_plain_approved_releases_nothing` (:3800), `test_design_table_holds_all_eighteen_ids` (:1712), `test_precedence_order` (:4520), `test_raw_id_scan_declared_limit_blocks_ordinary_with_nested_bound_id` (:1695), `test_nrm_fc7_over_65536_bytes_big` (:2109) |
| hooks/test_launch_level_guard_l2_tokens.py | 160 | 7 | #441 FR-050..052: hook-file edits and Bash tamper tokens (`.git/hooks`, `--no-verify`, `hookspath`, `hook.pre-push`); transport-only forms keep L1 ids (SD-2); combined L1/L2 outcome pins; guard and plugin copy byte-identical | `test_hook_file_edit_is_tamper` (:46), `test_tamper_bash` (:73), `test_transport_only_forms_keep_their_ids` (:94), `test_combined_l2_outcome_is_pinned` (:138), `test_guard_and_plugin_mirror_are_byte_identical` (:149), `test_tamper_message_names_the_pre_push_hook` (:154) |
| hooks/test_launch_level_guard_registration.py | 127 | 7 | Guard registered once per event with timeout 5; not registered elsewhere; no `onFailure`; PreToolUse matcher equals the design string; Bash registrations stay and identity hook stays last; same in both hooks.json trees | `test_guard_registered_once_on_each_event_with_timeout_5` (:45), `test_no_on_failure_key_anywhere` (:64), `test_pretooluse_matcher_equals_the_design_string` (:68), `test_existing_bash_registrations_stay_and_identity_hook_stays_last` (:99), `test_guard_registrations_are_the_same_in_both_trees` (:121) |
| hooks/test_launch_level_guard_with_identity.py | 212 | 5 | Guard and identity hook on one payload (Linux only, skipif at :42): FS allows and identity rewrites only the command; guard must see the original command; W blocks while identity still rewrites; ordinary both silent; a `degraded` record blocks all Bash through the identity hook | `test_full_submit_allowed_command_guard_allows_identity_rewrites_only_command` (:115), `test_guard_must_see_the_original_command_not_the_installed_rewrite` (:135), `test_degraded_word_guard_worktree_with_state_note_identity_blocks_all` (:187) |
| hooks/test_launch_level_guard_worker.py | 300 | 11 | G2 rule 2: marker prompt binds the worker; send/ask allowed with no `--to`; the address check ends inside the hook time limit; other worker/group addressing blocked; other orca verbs blocked; read-only orca forms allowed; still blocked from publishing; chain bind -> ask -> implement blocked -> release -> allowed; forged release is LL-TAMPER | `test_a_bound_worker_may_send_and_ask_its_coordinator` (:74), `test_a_bound_worker_cannot_address_another_worker_or_a_group` (:187), `test_every_other_orca_word_stays_blocked_for_a_bound_worker` (:213), `test_bound_send_ask_implement_blocked_release_implement_allowed` (:249), `test_a_forged_release_from_the_workers_own_session_is_blocked_as_tampering` (:262) |
| hooks/test_launch_job_identity.py | 1530 | 56 (2 classes) | Real Linux sessions: prepare/run/identify, symlink and mode refusals, concurrent consumption, stale/orphaned/foreign records, hook rewrite and no-ticket guarantees, missing uv/jq fallbacks, real-git old-governed-background vs human, `setsid` escape unselected | `test_hook_replaces_whole_input_without_approval_and_executes` (:651), `test_corrupt_or_stale_job_record_is_unknown_not_human` (:362), `test_missing_uv_and_jq_is_unavailable_adaptation_not_positive_identity` (:1133), `test_real_git_deliberate_setsid_escape_is_unselected_not_retained` (:1437), `test_hook_unbound_and_unverifiable_ids_are_silent_without_state_creation` (:686) |
| hooks/test_launch_level_pre_push.py | 1194 | 34 (2 classes) | FR-100 matrix T-01..T-24 with real git and a bare remote: create/update/delete/force/mapped/mixed/empty/fetch-first/sha256/dry-run/linked worktree; stale/orphaned/group-writable/second uid records; invalid data file; hook sha256 pin; `install_l2` placement; FR-101 bypass | `test_t01_create_protected_ref` (:462), `test_t09_fetch_first` (:567), `test_t14_agent_and_human_same_linked_worktree` (:616), `test_t23_hook_sha256_pinned_with_version_line` (:1103), `test_hook_placed_by_install_l2` (:1156), `test_fr101_bypass_reaches_remote_under_governed_actor` (:1182) |
| hooks/test_launch_level_pre_push_records.py | 230 | 8 (1 class) | T-D1..T-D5 record parsing with a stub selector: actor mapping, malformed record, ordinary never reads stdin, last line without newline, no file written | `test_td1_actor_mapping` (:127), `test_td2_malformed_record` (:156), `test_td3_ordinary_does_not_read_stdin` (:164), `test_td5_hook_writes_no_file` (:208) |
| hooks/test_launch_level_observations.py | 84 | 6 | Nine synthetic fixtures; log-only probe tests (five run); ONE test function `test_pending_live_observation` parametrized over `_PENDING` = OB-H1 item 1..9, OB-H2, OB-H3, OB-CTX (12 cases) | `test_fixtures_are_nine_json_objects_with_an_event_name` (:32), `test_probe_appends_exactly_one_line_per_call` (:44), `test_pending_live_observation` (:83). **Why skipped:** its body is `pytest.skip(f"{item}: needs a real governed session and has not been run")` (:84): all 12 cases skip unconditionally because the observations need a real governed Claude session and none was run |
| cli/test_install_hooks.py | 1246 | 37 | Settings merge cases 1-8 (create, empty, preserve, matcher collisions, force refresh, malformed refused, permission denied, backup, atomic); ccsession hook ownership; real hooks.json registrations; launch scripts packaged, listed, executable, mirrored; guard install registers both events and is idempotent; upgrade lands before identity | `test_launch_level_guard_script_is_packaged_listed_executable_and_mirrored` (:1086), `test_launch_level_pre_push_script_is_packaged_listed_executable_and_mirrored` (:1104), `test_launch_level_pre_push_script_sha256_pin` (:1118), `test_launch_level_guard_real_install_registers_both_events_and_is_idempotent` (:1128), `test_launch_level_guard_upgrade_lands_before_launch_identity` (:1190), `test_real_hooks_json_registers_launch_identity_without_replacing_policy` (:897), `test_force_refreshes_subagent_start_from_async_to_sync` (:363) |
| unit/test_install_ccsession.py | 417 | 22 | `wire_ccsession`: symlink and env seeding, refuses unmanaged binary, symlinked skill refused, older skill without ccsession-orca still succeeds, retention setting only raised, name migration | `test_wire_creates_symlink_and_env` (:47), `test_wire_older_skill_without_orca_wrapper_still_succeeds` (:95), `test_wire_refuses_unmanaged_binary` (:197), `test_wire_fails_if_skill_or_example_missing` (:230) |
| unit/test_ccsession_tag.py | 7101 | 277 (1 class) | The ccsession wrapper. Launch-relevant: `CCSESSION_PERMISSIONS=default` drops the bypass (:1519-1684, #390), launch status lines go to stderr (:1493, :1781), ccsession-orca naming, prompt pass-through and tab reopen (:1993-2587), `--auto-name` (:2686). No test in this file mentions `launch-level` or `sc-launch` (grep zero hits), so no test here pins "the shim carries no level"; the word "shim" in most of its test names means the gateway model-alias proxy (local-gateway-alias-proxy.py), not the launch-level path | `test_permissions_default_drops_the_bypass_on_every_launch_line` (:1519), `test_launch_status_lines_are_on_stderr_only` (:1493), `test_orca_prompt_reaches_claude_unchanged_and_is_never_a_label` (:2264), `test_orca_enter_gets_an_auto_name` (:2109), `test_auto_name_without_text_is_the_folder_and_a_stamp` (:2686) |
| unit/test_ccsession_tiers.py | 3821 | 149 (4 classes) | Tier model slots, defaults file, window per tier, version order, stand-in gateways; no launch-level content (grep zero hits) | `test_shipped_data_defines_tier2b_between_tier2_and_tier3` (:208), `test_defaults_file_is_parsed_not_sourced` (:151) |
| core/test_orca_session_launch_guidance.py | 62 | 3 | The "### Orca session launches" paragraph in `core/CLAUDE.md` and `ccsession-tag/README.md`: names Claude (CLI), `ccsession-orca`, `worktree create --agent`, `--surface terminal`; the paragraph is identical in both copies | `test_orca_session_launch_guidance` (:13), `test_appended_paragraph_names_the_owner_roles_and_no_source_path` (:48), `test_appended_paragraph_is_identical_in_both_copies` (:60) |
Claim-side pins used in this area (counted by agent 04 as well): tests/skills/test_issue_l2_install.py (716 lines, 26 tests; `test_ir7_shipped_switch_is_off` :639, `test_hookspath_is_unsupported` :312, `test_l2_status_never_writes` :575); tests/skills/test_issue_orca_worktree.py (2501 lines; `W-LAUNCH-NOT-CCSESSION` pins at :1506, :1595, :1653, :1665, `pending` subcommand pins :2472-2498, pending record published before orca runs :1384); tests/hooks/test_require_orca_worktree_agent_governed.py (56 lines, 1 test, `test_blocks_bare_create_in_a_governed_session` :31).

### 11.2 Level matrix, one test pin per cell
Oracle: `EXPECTED` hand-written table (test_launch_level_guard.py:806-854) and `LEVEL_FILES` (:778-783: W = word `worktree`, WA = `worktree` plus `.ok`, F = `full`, FS = `full-submit`). All 16 cells below are exercised by `test_launch_level_guard.py::test_grid_policy` (:3394, ids `GRID-<CLASS>-<case>-<level>`, built at :3384-3390 from GRID_CASES :3354-3381). Expected value in each cell = the guard's decision. OBSERVED column = this session's run (section "Observation run"): exit 2 with the word, or exit 0.
| Action class | W | WA | F | FS |
|---|---|---|---|---|
| implement (IMPL, Skill `sc:implement`) | block LL-IMPL; pin `test_grid_policy[GRID-IMPL-skill-implement-W]`; OBSERVED exit 2 | allow; pin `...[GRID-IMPL-skill-implement-WA]`; OBSERVED exit 0 | allow; pin `...[GRID-IMPL-skill-implement-F]`; OBSERVED exit 0 | allow; pin `...[GRID-IMPL-skill-implement-FS]`; OBSERVED exit 0 |
| commit (COMMIT, `git commit -m x`) | block LL-COMMIT; pin `...[GRID-COMMIT-git-commit-W]`; OBSERVED exit 2 | block; pin `...[GRID-COMMIT-git-commit-WA]`; OBSERVED exit 2 | block; pin `...[GRID-COMMIT-git-commit-F]`; OBSERVED exit 2 | allow; pin `...[GRID-COMMIT-git-commit-FS]`; OBSERVED exit 0 |
| push (PUSH, `git push -u origin feature`) | block LL-PUSH; pin `...[GRID-PUSH-git-push-canonical-W]`; OBSERVED exit 2 | block; pin `...[GRID-PUSH-git-push-canonical-WA]`; OBSERVED exit 2 | block; pin `...[GRID-PUSH-git-push-canonical-F]`; OBSERVED exit 2 | allow; pin `...[GRID-PUSH-git-push-canonical-FS]`; OBSERVED exit 0 |
| submit (SUBMIT, Skill `sc:pr-submit`; also `gh pr create --repo`) | block LL-SUBMIT; pin `...[GRID-SUBMIT-skill-pr-submit-W]`; OBSERVED exit 2 (with `gh pr comment`) | block; pin `...[GRID-SUBMIT-skill-pr-submit-WA]`; OBSERVED exit 2 | block; pin `...[GRID-SUBMIT-skill-pr-submit-F]`; OBSERVED exit 2 | allow; pin `...[GRID-SUBMIT-skill-pr-submit-FS]`; OBSERVED exit 0 |
Second pins for the same cells: `test_grid_level_steps` ids `GRID-step-W-skill-implement`, `GRID-step-F-git-commit`, `GRID-step-FS-git-push`, ...; WA has no step pin there (W, F, FS only, GRID_STEPS :3423-3446), so WA is pinned only by `test_grid_policy`, `test_skill_grid_matches_oracle` (IMPL/SUBMIT Skill rows, ids by sorted `name` and `level`) and `test_apr_approval_never_unlocks_commit_push_submit` (:3852). Always-blocked classes (REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG) are pinned in all four levels by the same `test_grid_policy` rows; OBSERVED for PROTECTED, MERGE and REPO at FS (section "Observation run").

Key Takeaways
- 16 test files plus claim-side pins cover the area; the main guard file alone has 162 test functions and a hand-written oracle independent of the script.
- The 12 live observations are one skipped function; no test in the ccsession files pins "no launch level".

## 12. Absence and cross-reference evidence (read-only greps and listings run in this session; label OBSERVED-BY-GREP)

| Question | Command (read-only, on SNAP) | Result |
|---|---|---|
| Any caller of the `pending` subcommand or `publish_pending` outside `orca_worktree.py`? | `grep -rn -E 'orca_worktree\.py[^|]*pending\|pending --level\|publish_pending\|cmd_pending' src plugins tests` excluding the script itself | one hit: tests/hooks/test_launch_level_guard.py:165, a docstring ("the way publish_pending does"). No caller in src or plugins. The pins that run it are in tests/skills/test_issue_orca_worktree.py:2472-2498 |
| `release-worker` anywhere in code? | `grep -rln 'release-worker\|release_worker' src tests plugins` | zero files. In docs: docs/designs/orchestrator.md:991, :1095 and issue-pipeline-guard-g2-no-to.md:57 only |
| `src/superclaude/cli/issue_pipeline/`, `tests/issue_pipeline/` | `ls` | "No such file or directory" for both |
| `issue_pipeline` registered in `cli/main.py`? | `grep -n -i 'issue.pipeline' cli/main.py` | zero hits |
| `pipeline.json` written by any code? | `grep -rn 'pipeline\.json' src plugins` (py, sh, md, json) | zero hits |
| Route B signature code? | `grep -n -i 'signature\|signed\|hmac\|openssl'` in guard and identity | zero hits |
| `orca-ide` recognised by the guard? | `grep -n 'orca-ide' launch-level-guard.sh` | zero hits; guard matches basename `orca` only (:457) |
| Where `orca-ide` is used in src | `grep -rln 'orca-ide' src/superclaude` | cli/issue_watch/launch.py, cli/sweep/probes.py (`ORCA_BINARY_DEFAULT = "orca-ide"` :43), cli/install_user_setup.py (`_ORCA_CLIS = ("orca-ide", "orca")` :36) |
| Plugin launch scripts byte-identical? | `cmp -s` src vs `plugins/superclaude/hooks/scripts/<each>` | IDENTICAL for launch-level-guard.sh, launch-job-identity.sh, launch-level-pre-push.sh |
| Plugin hooks.json vs src hooks.json | `diff` | differs: lacks ccsession-tag registrations, lacks `pragmatic-subagent.js` entry, `freshness-subagent-start.sh` has `async: true` in plugin only; launch-level registrations equal |
| Commands in the IMPL list still exist? | `ls src/superclaude/commands/{implement,task,cleanup,improve,spawn,build}.md` | implement, task, cleanup present; improve, spawn, build absent |
| ccsession-tag mentions launch level? | `grep -rn -E 'launch-level\|sc-launch\|LAUNCH_LEVEL\|launch_level' skills/ccsession-tag` | zero hits |
| Callers of `install_l2` | `grep -rn 'install_l2(' src` | only orca_worktree.py:1754 (and its def :1386) |
| Callers of `install_hooks(` / `wire_ccsession(` | `grep -rn` | main.py:219, :412; cli/eval/hook_adapter.py:230; main.py:211, :406 |
| `OB-H`/`OB-CTX` checked by claim code? | `grep -rn -E 'OB-H\|OB-CTX\|observation' skills/sc-issue-protocol/scripts --include='*.py'` | only the comment on `IR7_REFUSE` (orca_worktree.py:822) |

## Observation run

**What was run.** The guard script from its snapshot path, unmodified, against 44 sample payloads, with `env -i HOME=<sandbox> PATH=/usr/bin:/bin` so it saw only the sandbox HOME. Sandbox directory (created inside the task folder): /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/05-guard-run-sandbox/ . Files there: `run-guard-observation.sh` (the exact payload commands, 40 cases), `run-guard-extra.sh` (4 extra cases, command-word recognition), `observation-output.txt` (raw result lines), `out/<case>.stdout|stderr` (captured streams), `home/.claude/state/launch-level/{pending,sessions}` (the store the guard wrote). Script: /home/coder/.cache/ic-snap-20261120/master/src/superclaude/hooks/scripts/launch-level-guard.sh. Runtime: bash 5.2.37, jq 1.7 (both present). No `uv` was needed (the identity hook and `identify` were NOT run: `uv run` would write its interpreter and cache state under the sandbox HOME and the identity checks need a live supervisor process; skipped, see "Not run" below).
**Safety checks (OBSERVED).** `find $SNAP -newer run-guard-observation.sh` returned nothing: no file under the snapshot changed. The real `~/.claude` was never named in any command (HOME was the sandbox on every call). Sessions were bound through the real marker path: pending records were written by the run script (as `publish_pending` would, one word, no newline), then a prompt carrying `[sc-launch:v1:<nonce>]` was fed to the guard. The sandbox session records were mode 644/600 (the 644 are my hand-written pending files created under umask 022 and hard-linked by the guard; the real `publish_pending` writes 0600, orca_worktree.py:1505), a sandbox artifact, not a guard finding.
**Result: all 44 cases matched the reading of the code** (every exit code and class). stdout was empty on every case. Stderr first line is the fixed header `Launch-level guard: this session was started by /sc:issue --claim at level <worktree|worktree (approved)|full|full --submit>.` (`Launch-level guard:` alone when the level is unknown); `Blocked:` is the next line.

| Case | Payload (event, tool, command or prompt) | Exit | Stderr first line / Blocked line (OBSERVED) |
|---|---|---|---|
| S01 | ordinary id `ord-1`, UserPromptSubmit `hello`, store absent | 0 | empty |
| S01b | `ord-1`, Bash `git push origin feature`, store absent | 0 | empty |
| S02 | bind: `gov-w`, prompt `[sc-launch:v1:<nonce>] Read .dev/issues/1/launch-prompt.md` with pending word `worktree` | 0 | empty; sessions/gov-w = `worktree` |
| S02f | bind `gov-f`, pending `full` | 0 | empty; session = `full` |
| S02s | bind `gov-fs`, pending `full-submit` | 0 | empty; session = `full-submit` |
| S02k | bind `worker-w`, pending `worktree` | 0 | empty |
| S02d | bind `gov-d`, pending record holding the word `badword` | 0 | empty; session = `degraded` (ll_link_take :306); pending dir empty afterwards (all five records consumed once) |
| S03 | unbound `ord-2`, Bash `git push origin main`, store non-empty | 0 | empty (ordinary session never blocked) |
| M-IMPL-W | `gov-w` (W), Skill `sc:implement` | 2 | `...level worktree.` / `Blocked: starting /sc:implement, /task or /sc:cleanup (or their skills).` |
| M-COMMIT-W | `gov-w`, Bash `git commit -m x` | 2 | `...level worktree.` / `Blocked: creating a commit ...` |
| M-PUSH-W | `gov-w`, Bash `git push origin feature` | 2 | `...level worktree.` / `Blocked: a git push.` |
| M-SUBMIT-W | `gov-w`, Bash `gh pr comment 5 --repo IronbellyOrg/IronClaude --body-file f.md` | 2 | `...level worktree.` / `Blocked: /sc:pr-submit or a GitHub write ...` |
| S04 | `gov-w`, prompt `/sc:implement x` (typed approval) | 0 | empty; `gov-w.ok` created (mode 600), 1 `.ok` file in sessions |
| M-IMPL-WA | `gov-w` (now WA), Skill `sc:implement` | 0 | empty |
| M-COMMIT-WA | `gov-w`, `git commit -m x` | 2 | `...level worktree (approved).` / `Blocked: creating a commit ...` |
| M-PUSH-WA | `gov-w`, `git push origin feature` | 2 | `...level worktree (approved).` / `Blocked: a git push.` |
| M-SUBMIT-WA | `gov-w`, `gh pr comment 5 ...` | 2 | `...level worktree (approved).` / `Blocked: /sc:pr-submit or a GitHub write ...` |
| M-IMPL-F | `gov-f` (F), Skill `sc:implement` | 0 | empty |
| M-COMMIT-F | `gov-f`, `git commit -m x` | 2 | `...level full.` / `Blocked: creating a commit ...` |
| M-PUSH-F | `gov-f`, `git push origin feature` | 2 | `...level full.` / `Blocked: a git push.` |
| M-SUBMIT-F | `gov-f`, `gh pr comment 5 ...` | 2 | `...level full.` / `Blocked: /sc:pr-submit or a GitHub write ...` |
| M-IMPL-FS | `gov-fs` (FS), Skill `sc:implement` | 0 | empty |
| M-COMMIT-FS | `gov-fs`, `git commit -m x` | 0 | empty |
| M-PUSH-FS | `gov-fs`, `git push origin feature` | 0 | empty |
| M-SUBMIT-FS | `gov-fs`, `gh pr comment 5 ...` | 0 | empty |
| X-PROT-FS | `gov-fs`, `git push origin main` | 2 | `...level full --submit.` / `Blocked: a push to master or main.` |
| X-MERGE-FS | `gov-fs`, `gh pr merge 5 --repo IronbellyOrg/IronClaude` | 2 | `...level full --submit.` / `Blocked: a merge (git merge, git pull, gh pr merge ...` |
| X-REPO-FS | `gov-fs`, `gh pr create --title x --body y` | 2 | `...level full --submit.` / `Blocked: gh pr create without --repo.` |
| G2-A | bound `worker-w` (W), `orca orchestration send --type heartbeat --body hi --json` | 0 | empty (G2 rule 2 allow) |
| G2-B | `worker-w`, `orca orchestration ask --body "may I?" --json` | 0 | empty |
| G2-C | `worker-w`, `orca orchestration send --to run:run_1 --body hi` | 2 | `...level worktree.` / `Blocked: starting or messaging another agent or session ...` (LL-ESCAPE) |
| G2-D | `worker-w`, `orca terminal send --text hi` | 2 | same ESCAPE text |
| D-1 | `gov-d` (degraded record), Skill `sc:implement` | 2 | `...level worktree.` / `Blocked: starting /sc:implement ...` (read as W; the LL-STATE note is a later line) |
| T-1 | `worker-w`, `rm -rf ~/.claude/state/launch-level` | 2 | `...level worktree.` / `Blocked: touching the launch-level state, the Claude Code settings or hooks ...` (LL-TAMPER) |
| L-1 | no `session_id`, Bash `git push origin main` (identity loss) | 0 | empty |
| MAL-1 | not-JSON text containing `"session_id": "ord-3"` and `"tool_name"` (ordinary id) | 0 | empty |
| MAL-2 | not-JSON text containing `"tool_name": "Bash", "session_id": "gov-fs"` (bound id) | 2 | `...level full --submit.` / `Blocked: this action, because the launch-level guard could not run ...` (LL-BROKEN) |
| MAL-3 | not-JSON text containing `[sc-launch:v1:<nonce>]` | 2 | `Launch-level guard:` / `Blocked: this launch prompt.` (LL-NOBIND) |
| EVT-1 | event `Stop` for bound `gov-f` | 2 | `...level full.` / `Blocked: this action, because the launch-level guard could not run ...` (LL-BROKEN) |
| EVT-2 | event `Stop` for ordinary `ord-9` | 0 | empty |
| EXTRA-1 | `worker-w`, `orca terminal send --text hi` | 2 | ESCAPE block |
| EXTRA-2 | `worker-w`, `orca-ide terminal send --text hi` | **0** | empty: the guard does not recognise the word `orca-ide` |
| EXTRA-3 | `worker-w`, `orca-ide orchestration send --to run:run_1 --body hi` | **0** | empty |
| EXTRA-4 | `worker-w`, `/usr/local/bin/orca terminal send --text hi` | 2 | ESCAPE block (basename match) |
Totals: 44 payloads (40 in `run-guard-observation.sh`, 4 in `run-guard-extra.sh`), 16 of them are the level matrix, all 16 matched the matrix of section 1.5.
**Not run (and why).** (1) `launch-job-identity.sh` and the L2 `launch-level-pre-push.sh`: the identity script is launched through `uv run`, which would write interpreter and cache state under the sandbox HOME, and its checks need a live supervisor process in its own kernel session; the pre-push hook needs a git repository with an installed data file and the identity script. Running them could not be done without creating processes and git state outside the declared sandbox rules. They stay READ-ONLY-READING (sections 2 and 3). (2) The OB-H1..3 and OB-CTX live observations need a real governed Claude Code session; not run. (3) The claim (`cmd_launch`), `install_hooks.py` and `install_ccsession.py` were not executed: they write to `~/.claude` and `~/.local/bin`. (4) No pytest run (pytest writes `.pytest_cache`/`__pycache__` under the checkout).
The ordinary-session cases S01, S01b, S03, L-1, MAL-1, EVT-2 confirm FAIL-OPEN for ordinary sessions; D-1, MAL-2, MAL-3, EVT-1 confirm FAIL-CLOSED for governed ones.

## Gaps and Questions

All doc claims that came out [UNVERIFIED] or [CODE-CONTRADICTED], then open questions. Tags: CV = [CODE-VERIFIED], CC = [CODE-CONTRADICTED], UV = [UNVERIFIED].

### Doc claims checked
| # | Claim and doc location | Tag | Code evidence or reason |
|---|---|---|---|
| 1 | IMPL skill set is implement, task, improve, cleanup, spawn, build (sc-issue-launch-level-hook.md:106, :179, :391 O-13; LL-IMPL text :236) | CC | guard :409 `implement \| task \| cleanup`; message text :43 names three; commands `improve`, `spawn`, `build` absent from src/superclaude/commands (ls); test comment test_launch_level_guard.py:77-85 ("6.0.0 removed /sc:spawn, /sc:build and /sc:improve") and `test_lookalike_skill_names_stay_none` lists `sc:improve` as NONE (:934-936) |
| 2 | Row 34: typed `approved` writes `.ok` at W (design :123) | CC | design :189 says plain `approved` was removed (Q39); code accepts only first line `/sc:implement` or `/task` (guard :347); `test_apr_plain_approved_releases_nothing` (:3800). The design contradicts itself; code agrees with :189 |
| 3 | Level grid W/WA/F/FS and class matrix (design :89-98) | CV | guard :783-803; OBSERVED for 16 cells (section "Observation run") |
| 4 | Registrations and matcher equal design section 13 (design :337-346) | CV | hooks.json:116; test_launch_level_guard_registration.py:68 |
| 5 | G2: allow-list lines `:471-474` and TAMPER `:703` (issue-pipeline-guard-g2.md:13, :22) | CC (lines only) | now guard :480-491 and :760-762; behaviour CV |
| 6 | G2-no-to: address block at lines 500-549 (issue-pipeline-guard-g2-no-to.md:7) | CC (lines only) | now :496-537; rule CV: guard :524-531, WORKER-CONTRACT.md:66, `test_a_bound_worker_cannot_address_another_worker_or_a_group` |
| 7 | G2-no-to Task 4: rule WC-17 states the sentence (:48) | CC | WC-17 removed; the sentence sits in a bullet at WORKER-CONTRACT.md:66 (agent 06 owns the contract) |
| 8 | G2 route A: coordinator writes `<worker sid>.ok` through a helper, e.g. `release-worker` (guard-g2.md:22, g2-no-to.md:57) | UV / REMOVED | zero code hits for `release-worker`; removal listed in orchestrator.md:991 |
| 9 | G2 section 3: coordinator calls `orca_worktree.py pending`; "Task 15 puts the marker line into the brief" (guard-g2.md:18) | UV | `pending` exists (orca_worktree.py:1515, :1886-1893) but no caller and no brief builder in src; orchestrator.md:117 says `worker-start` workers have no marker |
| 10 | "A coordinator-started worker is not governed by this guard" (design :23) vs "Before any other issue runs through the flow, the worker must be bound to the guard (G2)" (guard-g2.md:9) | CC between docs | orchestrator.md:117 (DQ7, decided OD1) sides with "not governed"; code binds only claim launches. The guard-g2 text is the older intent |
| 11 | FU-1 e step runs `uv run superclaude issue-pipeline plan-hash` / `check-approval` and cites `src/superclaude/cli/issue_pipeline/plan_hash.py` (fu1.md:64, :66) | CC | `issue_pipeline` absent from cli/main.py; directory absent (ls) |
| 12 | FU-1 RECORDED lines a to k, dated 2026-11-17, "RUN BY OWNER: ironbelly" (fu1.md:108-119) | UV | live results written in the file; the snapshot has no run logs and nothing can re-run them |
| 13 | FU-1 f: under G1 no `sessions/` entry is created and ask/send are not blocked (fu1.md:113) | CV (consistent) / UV (live) | no marker -> unbound -> exit 0 (guard :390-391); OBSERVED for an unbound id (S03). The live worker run itself is UV |
| 14 | IR-3 documentation only (design :34, :351, :615) | CV | grep `pipeline.json`: zero hits |
| 15 | IR-7 refusal switched off (design :6, :34, :516, :615) | CV | `IR7_REFUSE = False` orca_worktree.py:822; test :639 |
| 16 | OB-H1..3 and OB-CTX pending (design :6, :625) | CV | tests skip, 12 params (observations test :79-84) |
| 17 | L2 installed by the claim at launch (design :514) | CV | `install_l2` called at orca_worktree.py:1754; the installer only copies the template (install_hooks.py:96) |
| 18 | L2 behaviour table (design :522-530) | CV | pre-push :187-208 |
| 19 | L2 cost: about 100 ms per push; table :617-623 | UV | measurement not re-run; no test asserts a time (design :617) |
| 20 | Plugin copies byte-identical | CV | `cmp -s` identical for all three scripts; pinned by test_launch_level_guard_l2_tokens.py:149 and test_install_hooks.py:1086-1109 |
| 21 | "The plugin hooks.json differs only by lacking ccsession-tag entries" (scope hint) | CC | `diff`: also lacks the `pragmatic-subagent.js` SubagentStart entry and has `async: true` on `freshness-subagent-start.sh` |
| 22 | "The ccsession shim carries the launch level" | CC | it does not (section 5.2); the level travels by files only |
| 23 | Shim screen text is visible only 1-2 s (orca_worktree.py:793-794) | UV | not observed here |
| 24 | install_hooks.py header cites `.dev/releases/current/freshness-system/phase-4-tasklist.md` (:7) | UV | not opened; irrelevant to behaviour |

### Open questions for the owner
1. Should coordinator-started workers be bound to the guard? Code supports it (`pending` subcommand, marker, G2 rule 2) but nothing calls it; orchestrator.md:117 and :975 record "not governed" with option B (bind) left to the owner (OD1). Until decided, G2 rule 2 only matters for sessions bound by a claim.
2. Should `orca-ide` be a recognised Orca command word in the guard? OBSERVED: a bound session may run any `orca-ide` verb (EXTRA-2, EXTRA-3). docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:83 already lists "the launch-level guard recognizes only the command word `orca`" as a recorded DEFECT with a draft plan.
3. Is the ship gate "no governed claim until OB-H1 item 1, OB-H2, OB-H3 pass" meant to be a code check? Today it is prose (SKILL.md:92, design :625); `cmd_launch` does not check it.
4. A `degraded` session (loose marker with no usable record) is level W for the guard but unusable for the identity hook, which blocks every Bash call of that session (identity :74, :183, :500-502; pinned by test_launch_level_guard_with_identity.py:187). Intended, pinned; confirm it is wanted.
5. `ccsession-orca` is Orca's Claude command; the claim only warns (`W-LAUNCH-NOT-CCSESSION`) when it is absent. If it is absent the guard still binds through the prompt marker, because the marker rides in the prompt, not in the shim. Whether the owner wants the claim to refuse in that case is not stated in any file read.
6. The word "shim" is used for two things: the claim's "ccsession shim" (the wrapper whose `[ccsession]` lines and `sc-launch-v1-...` title it detects, orca_worktree.py:792-797) and ccsession's `--shim` (a local gateway model-alias proxy, local-gateway-alias-proxy.py header). The claim detects the wrapper's text or title only; it does not check that the gateway proxy is running.
7. `session-start.sh` parses the hook JSON with bare `python3 -c` (:20-21); `session-start.sh` fails open (`|| echo ""`, :21-23). Not part of the launch-level path; noted because the owner's rule is UV only.

## Stale Documentation Found
- **[STALE DOC]** docs/designs/sc-issue-launch-level-hook.md :106, :179, :236 (LL-IMPL message), :391 (O-13): IMPL list of six skills; code has three and three commands no longer exist.
- **[STALE DOC]** docs/designs/sc-issue-launch-level-hook.md :123 (row 34 typed `approved`): contradicts :189 and the code.
- **[STALE DOC]** docs/designs/sc-issue-launch-level-hook.md :23 versus docs/designs/issue-pipeline-guard-g2.md :9 (worker must be bound before other issues run): superseded by docs/designs/orchestrator.md:117 (DQ7).
- **[STALE DOC]** docs/designs/issue-pipeline-guard-g2.md: route A / `release-worker` (:22), line references `:471-474` and `:703` (:13, :22), Task 14/15 plan (:45-51), "design note ... No code is changed" status (:3); G2 rule 1 was removed after the note.
- **[STALE DOC]** docs/designs/issue-pipeline-guard-g2-no-to.md: address block "lines 500-549" (:7), Task 4 names WC-17 (:48), `release-worker` (:57); the guard change itself is built.
- **[STALE DOC]** docs/designs/issue-pipeline-fu1.md: the e step commands and the `plan_hash.py` path (:64-66), the "Gates that still apply" and the Plan B task numbering; the runbook's live record is kept as text only.
- scope-5 hint file: the plugin hooks.json difference was incomplete (see claim 21).

## Defect Candidates and Not-Built Capabilities
Per rule C8 (adapted): each row names the capability, the declaring doc, the evidence that it is unreachable, and any recorded decision found in the snapshot. No remediation task was created and nothing was written outside the task folder; the owner decides.
| # | Capability | Declaring doc path and line | Code evidence (unreachable or off) | Recorded decision in the snapshot |
|---|---|---|---|---|
| DC-1 | Binding of coordinator-started workers (`orca_worktree.py pending` plus a marker line in the brief), so that G2 rule 2 governs them | docs/designs/issue-pipeline-guard-g2.md:18 (Task 15 adds `pending` and the marker line); src/superclaude/core/WORKER-CONTRACT.md:66 ("the launch-level guard blocks any `--to` from a bound worker") | `pending` subcommand defined (orca_worktree.py:1515-1523, :1886-1893) and tested (tests/skills/test_issue_orca_worktree.py:2472-2498) but no production caller: grep section 12 finds only a test docstring. The brief builder (`brief.py`) is in the removed package (orchestrator.md:991). G2 rule 2 code (guard :485, :496-537) therefore only runs for sessions bound by a claim launch | docs/designs/orchestrator.md:117 and :129 (DQ7 decided OD1: `worker-start` workers are not governed) and :975, :1002 (binding is option B, left to the owner). So the "not bound" state is a recorded decision; the doc and WORKER-CONTRACT sentence about a "bound worker" still describe a path no code starts |
| DC-2 | IR-7 refusal when L2 is not owned | design :34, :516, :615; orca_worktree.py:818-826 | `IR7_REFUSE = False` (:822); the refusal `return` at :1757-1758 is unreachable while False; pinned `test_ir7_shipped_switch_is_off` | orca_worktree.py:819-822 comment "owner decision OD-3" and "owner decision 2026-11-08": turn on only after the #442 observations pass |
| DC-3 | IR-3 `pipeline.json` | design :34, :351, :615 | grep `pipeline\.json` zero hits in src and plugins | design :34: "Issue #322's source-write boundary and reading `pipeline.json` remain out of scope" |
| DC-4 | Ship gate "no governed claim until OB-H1 item 1, OB-H2, OB-H3 pass" and live observations OB-H1..3, OB-CTX | design :6, :625; SKILL.md:92; refs/claim.md:136 (cited by orchestrator.md:117) | Gate is prose only: `cmd_launch` (:1696-1834) never reads an observation record; the 12 tests `skip` unconditionally (observations test :79-84). A person can run `/sc:issue --claim --pipeline worktree|full` today | design :625 states the gate and "Pending, none run"; no decision says the gate may stay unenforced in code |
| DC-5 | L1 recognition of the Orca CLI under its real binary name `orca-ide` | design :119 (rows 6, 10, 25: `orca terminal send` is ESCAPE) and :175 (orca words ESCAPE unless allow-listed) | guard matches basename `orca` only (:457); OBSERVED exit 0 for `orca-ide terminal send` and `orca-ide orchestration send --to run:run_1` (EXTRA-2, EXTRA-3); `orca-ide` is the default binary in cli/sweep/probes.py:43 and first in cli/install_user_setup.py:36 | none found; SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:83 records it as a DEFECT with a draft plan that "is not a fix" |
| DC-6 | G2 route B (signed approval file) | issue-pipeline-guard-g2.md:24 | grep `signature\|signed\|hmac\|openssl` zero hits in guard and identity | guard-g2.md:26 recommends route A, not B; route A itself is REMOVED (DC-7) |
| DC-7 | G2 rule 1 / route A (`release-worker`, coordinator writes `.ok`) | issue-pipeline-guard-g2.md:22, :45-51 | zero code hits; package and tests deleted (ls); guard comment :496-497 says retired | docs/designs/orchestrator.md:991, :1095, :1002 (rule 1 removed in PR D) |
| DC-8 | FU-1 first live test runbook commands | issue-pipeline-fu1.md:64 | `issue-pipeline` command group absent (cli/main.py zero hits; directory absent) | removal recorded orchestrator.md:991; the runbook text itself was not updated |
| DC-9 | L2 and identity cover only the tested local Bash surface (Monitor, `setsid`, killed supervisor, `git --no-verify` spellings) | design :536-557 (LIM-1..LIM-20) | identity `hook()` returns 0 for any tool other than Bash (:442-444); header :7-9 | design :534 "Limits (OD-1)": declared limits, owner decision OD-1 |
Not defects but worth stating: the guard governs nothing by itself on a machine where no claim launched a session at `worktree` or `full` (every other session exits 0, guard :391), and `--pipeline none` claims (the watcher's launch) create no pending record.

## Summary
The launch-level guard stack is built and wired: the L1 guard (808 lines, exit 0/2 only), the Bash job-identity rewriter and the L2 git pre-push template are registered or installed through hooks.json, `install_hooks.py` and the claim's `install_l2`, with byte-identical plugin copies; the level travels only by files under `~/.claude/state/launch-level/{pending,sessions,requests,jobs}`, never by the ccsession shim, which the claim merely detects (warning `W-LAUNCH-NOT-CCSESSION`). I ran the guard against 44 sample payloads in a sandbox HOME inside the task folder and observed all 16 matrix cells (implement/commit/push/submit at W, WA, F, FS), G2 rule 2, binding, fail-open for ordinary sessions and fail-closed for bound ones; every result matched the code reading. Retired or not built: G2 rule 1 / route A (`release-worker`), route B, IR-3 `pipeline.json` and the live observations OB-H1..3 and OB-CTX (12 skipped tests); IR-7 is built but switched off (`IR7_REFUSE = False`). The main defect candidates are that nothing binds coordinator-started workers (no caller of `orca_worktree.py pending`, a recorded owner decision DQ7), that the ship gate is prose only, and that the guard does not recognise the command word `orca-ide` (observed). The area writes nothing to GitHub.

## Gap-fill c1 B-3 (ERRATUM, supersedes the earlier wording)

Finding B-3: the Key Takeaways of section 11 (the bullet that begins "16 test files plus claim-side pins cover the area") gives a wrong file count. Verdict: [CODE-CONTRADICTED]. The table in section 11.1 has 14 rows (one per assigned test file), and the claim-side paragraph under it names 3 more files, which makes 17 files. The correct statement is: 14 test files in the table plus 3 claim-side pin files, 17 in all. Nothing above this heading was altered; this section replaces the count wherever it is quoted.

Method [OBSERVED-BY-GREP, read-only, snapshot `/home/coder/.cache/ic-snap-20261120/master/tests`, no test executed]: `wc -l <file>` for lines; `grep -c 'def test_' <file>` for the test count asked for by this gap; `grep -c -E '^\s*(async )?def test_' <file>` as a strict cross-check (a line that starts with `def test_`, as used in section 11.1). The two counts differ for one file only (see the note after table A). Parametrized tests expand to more real cases than these function counts.

### A. The 14 test files in the section 11.1 table
| # | Path (under /home/coder/.cache/ic-snap-20261120/master/tests/) | Lines (`wc -l`) | Tests (`grep -c 'def test_'`) | Strict count |
|---|---|---|---|---|
| 1 | hooks/test_launch_level_guard.py | 4631 | 163 | 162 |
| 2 | hooks/test_launch_level_guard_l2_tokens.py | 160 | 7 | 7 |
| 3 | hooks/test_launch_level_guard_registration.py | 127 | 7 | 7 |
| 4 | hooks/test_launch_level_guard_with_identity.py | 212 | 5 | 5 |
| 5 | hooks/test_launch_level_guard_worker.py | 300 | 11 | 11 |
| 6 | hooks/test_launch_job_identity.py | 1530 | 56 | 56 |
| 7 | hooks/test_launch_level_pre_push.py | 1194 | 34 | 34 |
| 8 | hooks/test_launch_level_pre_push_records.py | 230 | 8 | 8 |
| 9 | hooks/test_launch_level_observations.py | 84 | 6 | 6 |
| 10 | cli/test_install_hooks.py | 1246 | 37 | 37 |
| 11 | unit/test_install_ccsession.py | 417 | 22 | 22 |
| 12 | unit/test_ccsession_tag.py | 7101 | 277 | 277 |
| 13 | unit/test_ccsession_tiers.py | 3821 | 149 | 149 |
| 14 | core/test_orca_session_launch_guidance.py | 62 | 3 | 3 |

Note on row 1: the plain `grep -c 'def test_'` gives 163 but the file has 162 test functions. The extra match is line 4615 of hooks/test_launch_level_guard.py, which is the text `"def test_matcher_matches_the_guarded_tools_and_not_the_others(",` inside a string literal (a source snippet), not a test. The 162 in section 11.1 and in the Key Takeaways bullet is correct [CODE-VERIFIED]. All 14 line counts and all other test counts equal the numbers in section 11.1 [CODE-VERIFIED]. Grouping in the 14: guard 5 (rows 1-5), identity 1 (row 6), pre-push 2 (rows 7-8), observations 1 (row 9), install_hooks 1 (row 10), install_ccsession 1 (row 11), ccsession_tag 1 (row 12), ccsession_tiers 1 (row 13), launch_guidance 1 (row 14).

Gap-fill c1 B-3 table A complete

### B. The 3 claim-side pin files named under the section 11.1 table
| # | Path (under /home/coder/.cache/ic-snap-20261120/master/tests/) | Lines (`wc -l`) | Tests (`grep -c 'def test_'`) | Strict count |
|---|---|---|---|---|
| 15 | skills/test_issue_l2_install.py | 716 | 26 | 26 |
| 16 | skills/test_issue_orca_worktree.py | 2501 | 109 | 109 |
| 17 | hooks/test_require_orca_worktree_agent_governed.py | 56 | 1 | 1 |

Path correction [CODE-CONTRADICTED]: the wording of finding B-3 (and any reader who copies it) places the third file under `tests/skills/`. `skills/test_require_orca_worktree_agent_governed.py` does not exist in the snapshot (`[ -f ]` returned missing). The file is `hooks/test_require_orca_worktree_agent_governed.py`, which is the path section 11.1 already gave [CODE-VERIFIED]. Its one test is `test_blocks_bare_create_in_a_governed_session` (:31). The line counts for files 15 and 17 and the test counts for files 15 and 17 equal the numbers in section 11.1 [CODE-VERIFIED]. File 16: section 11.1 gave the line count 2501 [CODE-VERIFIED] but no test count; it is 109. Files 15 to 17 sit under `skills/` and `hooks/` because they pin the claim script (`orca_worktree.py`), not the guard script.

Total of table A plus table B: 17 files, 4631+160+127+212+300+1530+1194+230+84+1246+417+7101+3821+62 = 21115 lines in table A, 716+2501+56 = 3273 lines in table B, 24388 lines in all. Test functions by the plain `grep -c 'def test_'` count: table A 163+7+7+5+11+56+34+8+6+37+22+277+149+3 = 785 (784 by the strict count), table B 26+109+1 = 136, 921 in all by the plain count (920 strict).

Gap-fill c1 B-3 table B complete

### C. Further test files under the snapshot tests tree that touch the guard, identity, pre-push or ccsession-launch behaviour but are in neither list
Search [OBSERVED-BY-GREP over every file under tests/]: (1) `launch-level-guard|launch-level-pre-push|launch-job-identity|launch_level|launch-level|sc-launch|launch_job_identity` gave 16 files: 10 of table A (the 8 guard, identity and pre-push files, test_launch_level_observations.py and test_install_hooks.py), the 3 table B files (test_issue_l2_install.py, test_issue_orca_worktree.py, test_require_orca_worktree_agent_governed.py), the fixture hooks/fixtures/launch_level/live_probe.py, and two files of table C (test_freshness_subagent_start_policy.py, test_worker_contract.py); (2) `ccsession-orca|ccsession_orca|W-LAUNCH-NOT-CCSESSION|CCSESSION_PERMISSIONS|install_ccsession|wire_ccsession` gave 11 files; (3) case-insensitive `ccsession` gave 36 files; (4) `pre-push|pre_push|LL-<word>|orca-ide|install_l2|job-identity|governed session|bound worker` gave 42 files; (5) `hookspath|--no-verify|orca_worktree\.py|launch-level/(pending|sessions|requests|jobs)` gave 13 files; (6) `require-orca-worktree-agent`. The hit lines of each non-listed file were read (or, for the noise files named next, judged from the matching lines). Most of the 42 files in search (4) are noise: tests/pr_submit/* match only on the field name `pre_push_sha` and on `--no-verify` in a pattern list that forbids the flag in pr-submit scripts; tests/sweep/* match on the `orca-ide` command name; tests/issue_watch/conftest.py, test_cli.py and test_cli_e2e.py match on the `orca-ide` stub name. None of these pins the guard, identity, pre-push or ccsession behaviour, so they are not listed as pins. A negative result here means only "no hit for these terms"; it is not a proof that no other test touches the area.

C1. Files that pin one concrete piece of the behaviour (strongest candidates)
| Path (under /home/coder/.cache/ic-snap-20261120/master/tests/) | Lines | Tests (`def test_` at line start) | What it pins that tables A and B do not already carry |
|---|---|---|---|
| hooks/test_freshness_subagent_start_policy.py | 115 | 5 | `test_subagent_start_registration_is_synchronous_without_bash_counter` (:91) asserts that the set of commands registered for PreToolUse with matcher `Bash` in hooks.json is exactly `block-bare-python.sh`, `require-orca-worktree-agent.sh` and `launch-job-identity.sh` (:105-115). It is a second pin, outside test_launch_level_guard_registration.py, that the identity hook is registered for Bash and that no other Bash hook may appear unannounced. It does not name the guard script (the guard has its own matcher). [CODE-VERIFIED] |
| issue_watch/test_launch.py | 952 | 66 | `test_ac8_launch_argv_equals_the_literal_twelve_elements__fr013` (:75): the watcher's launch command is exactly `<orca-ide> agent launch --agent claude --worktree path:<dir> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json` (12 elements); `test_ac8_launch_argv_has_no_extra_flag__fr013_t10` (:102): no `--dangerously-skip-permissions` and no `--permission-mode` is added. This is the launch command of the issue watcher, not of ccsession and not of a governed claim. The prompt carries `--pipeline none`; these tests do not pin the absence of a pending record (the statement in section 12 about that is not pinned by this file). [CODE-VERIFIED for the argv] |

C2. Files that pin the wording of docs that state guard or claim-launch facts (text pins, no script is run)
| Path | Lines | Tests | What it pins |
|---|---|---|---|
| skills/test_issue_protocol.py | 1055 | 62 | `test_st9_final_output_lists_the_launch_results_and_every_launch_code` (:486): `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT` and `W-L2-ABSENT` must appear in both references/claim.md and SKILL.md of the issue protocol skill (:496-502). Also requires the claim wave text `orca_worktree.py" launch --number <N> --source <D> --level <L>` (:475). [CODE-VERIFIED] |
| skills/test_worker_contract.py | 3220 | 59 | The required-text table entry `messages-carry-no-to` (:423-431) requires WORKER-CONTRACT text to say "the launch-level guard blocks any `--to` from a bound worker" (:429). This is the doc pin for G2 rule 2 (section 1.7 above). [CODE-VERIFIED for the table entry; the name of the test function that consumes the table was not read] |

C3. Files that pin ccsession install, update, doctor and launcher-notice behaviour (coupling in section 5, not the launch level)
| Path | Lines | Tests | What it pins |
|---|---|---|---|
| cli/test_update_command.py | 409 | 18 | `test_install_wires_before_hooks_and_templates` (:123); `test_install_and_update_wire_failure_exit_nonzero` (:173, parametrized over command); `test_real_install_launches_ccsession` (:194: symlink `~/.local/bin/ccsession`, `ccsession.env` mode 0600, one SessionStart hook, `ccsession --help` runs); `test_real_update_restores_packaged_ccsession` (:223: modified wrapper restored, env file kept with mode 0640). The ordering lines at :174-179 put `install_hooks` immediately after `wire_ccsession`. [CODE-VERIFIED] |
| unit/test_cli_doctor.py | 363 | 22 | `_check_ccsession` doctor checks: missing wrapper, `ccsession-orca`, hooks, env file or symlink reported (`test_ccsession_doctor_reports_missing` :143); env directory rejected (:150); skill missing (:159); name collision for `ccsession` and `ccsession-orca` (:168-170); placeholder env accepted with a PATH warning (:182). [CODE-VERIFIED] |
| cli/eval/test_doctor_version.py | 225 | 16 | `test_parse_version_takes_claude_before_launcher_stderr` (:197) and `test_real_probe_reads_claude_version_not_the_launcher_notice` (:212): the `[ccsession] Shim already running ...` notice on stderr (issue 389) is not parsed as the Claude version. It is a consumer-side pin of the stderr status-line behaviour pinned from the producer side by test_ccsession_tag.py (:1493). [CODE-VERIFIED] |
| unit/test_cli_install.py | 1057 | 36 | Lists the packaged ccsession-tag files (:168-173) and the scripts list that includes `require-orca-worktree-agent.sh` (:123), read at the hits only. [CODE-VERIFIED for the hit lines; the rest of the file was not read] |

C4. Hit files that are NOT pins of this area (listed so a reader does not count them)
- cli/test_install_retired_files.py (712 lines, 25 tests) and cli/test_install_retired_mcp.py (776 lines, 45 tests): `superclaude.cli.install_ccsession.wire_ccsession` appears only as one entry in a list of installers to stub out (:561 and :519).
- unit/test_session_keep.py (1327 lines, 64 tests): the ccsession session-keep and prune helper (`CCSESSION_AGENT_KEEP_DAYS`, `orca-tabs` folder); not launch behaviour.
- hooks/fixtures/launch_level/live_probe.py (352 lines, 0 tests) and hooks/fixtures/launch_level/ob_h1/* (nine JSON fixtures, a README and log-only-probe.sh): fixtures used by test_launch_level_observations.py, not test files.
- tests/sweep/*, review/test_review_panel_live7.py, skills/test_model_alias_policy.py, skills/test_issue_worker_agents.py, swarm/test_coder_tier_env_2026_10.py, skills/test_agent_work_report.py: mention ccsession only as model-tier data (`ccsession-models.json`), the `orca-tabs` tab map or terminal titles. Not counted (line and test counts not taken; they are not pins of guard, identity, pre-push or launch).
- hooks/test_require_orca_worktree_agent.py (201 lines, 7 tests: `test_blocked` :129, `test_allowed` :137, four fail-open tests :156-186, `test_script_is_executable_and_runs_no_python` :197): the separate `require-orca-worktree-agent.sh` hook, whose governed-session branch is the one test in claim-side file 17. It is the sibling of file 17, is in neither list, and is outside the guard stack proper. [CODE-VERIFIED]

### D. One more pin found inside a table A file (not a new file)
hooks/test_launch_level_guard.py `ESCAPE_BASH` (:3105-3132) lists `ccsession`, `ccsession-orca 'x'` and `/usr/local/bin/ccsession -h` (:3129-3131) among the Bash commands that a governed session may not run (class ESCAPE), next to `claude -p x`, `orca agent launch ...`, `tmux send-keys ...`. So a launch-level test does pin that a governed session cannot start ccsession. The same list is the reason the grep for `ccsession` hits this file five times (:3129, :3130, :3131, :4098, :4386; the last two are `git commit -m "fix(ccsession): ..."` messages that must still classify as ESCAPE-scope edge rows). The earlier statement in row 12 of section 11.1 ("No test in this file mentions launch-level or sc-launch") is about test_ccsession_tag.py and stays correct [CODE-VERIFIED]. Still true after this search: no test anywhere in the tests tree pins "the shim carries no launch level" (search (1) has no hit in any ccsession-named test file).

### E. Corrected Key Takeaways (replaces the first bullet of the Key Takeaways in section 11)
- 17 test files cover the area: 14 in the section 11.1 table (21115 lines, 785 test functions by the plain count, 784 by the strict count) plus 3 claim-side pin files (tests/skills/test_issue_l2_install.py, tests/skills/test_issue_orca_worktree.py, tests/hooks/test_require_orca_worktree_agent_governed.py; 3273 lines, 136 tests). The main guard file alone has 162 test functions and a hand-written oracle independent of the script. Further files that touch the area at smaller depth are in table C (2 launch-pin files, 2 doc-text pin files, 4 ccsession install/doctor/notice files, and the adjacent require-orca-worktree-agent test).

Gap-fill c1 B-3 complete
