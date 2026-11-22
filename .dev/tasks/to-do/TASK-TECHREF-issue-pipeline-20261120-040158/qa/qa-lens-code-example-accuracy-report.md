# QA Report - Lens: code-example-accuracy

**QA phase:** lens-code-example-accuracy
**Lens:** code-example-accuracy (quoted commands, argv, exit codes, constants)
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
**Source root:** /home/coder/.cache/ic-snap-20261120/master (read-only)
**Date:** 2026-11-20
**Fix authorization:** false
**Status:** Complete

---

## Verbatim-comparison table, part 1: watcher argv, exit codes, constants, vocabularies

Document line numbers refer to the document under review (2369 lines, read completely in chunks). Source paths are relative to the snapshot root. Every row was opened in the snapshot and compared; the result column is MATCH unless stated.

| # | Item | Document location | Quoted value | Source value (path:line) | Result |
|---|------|-------------------|--------------|--------------------------|--------|
| 1 | Launch argv, 12 elements, order | 5.1.3 (l.811-813), 8.1 (l.1422), 4.5 (l.600) | `<orca> agent launch --agent claude --worktree path:<abs worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json` | `src/superclaude/cli/issue_watch/launch.py:103-116` (orca, agent, launch, --agent, ORCA_AGENT="claude" (:28), --worktree, "path:"+worktree, --surface, terminal, --prompt, prompt, --json = 12) | MATCH |
| 2 | Retry argv 14 elements, `--retry-launch` before `--json` | 8.1 (l.1423) | 14 elements | `launch.py:119-132` (`[*argv[:-1], "--retry-launch", operation_id, argv[-1]]`) | MATCH |
| 3 | Prompt text and pattern | 5.1.3, 8.3 (l.1470) | `/sc:issue --claim <N> --pipeline none`; `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` | `launch.py:33` and `:92` | MATCH |
| 4 | Operation id pattern | 5.1.3, 10.2 | `^[A-Za-z0-9._:-]{1,128}$` | `launch.py:36` | MATCH |
| 5 | Operation-id paths, op-unknown text | 5.1.3 | `OPERATION_ID_PATHS` 42-45, `OP_UNKNOWN_TEXT` 47 = `agent_session_operation_unknown` | `launch.py:42-45, 47` | MATCH |
| 6 | Launch detail vocabulary (8 words) | 5.1.7, 10.2 | ok, spawn_error, timeout, exit_nonzero, non_json, no_operation_id, operation_id_invalid, op_unknown | `launch.py:58-69` | MATCH |
| 7 | Origin literal and orca candidates | 5.1.3, 9.4 | `ironbellyorg/ironclaude` lower-cased; `_ORCA_CLIS` at install_user_setup.py:36 = orca-ide then orca | `launch.py:50, 249`; `install_user_setup.py:36` (`("orca-ide", "orca")`) | MATCH |
| 8 | Origin check argv | 8.1 (l.1420) | `["git","-C",<worktree>,"remote","get-url","origin"]` | `launch.py:244` | MATCH |
| 9 | Orca discovery argv | 8.1 (l.1421) | `[<abs path>,"skills","list","--json"]`, topic `orca-cli` | `launch.py:200, 160` | MATCH |
| 10 | G1 argv | 4.5, 5.1.2, 8.1 | `["gh","api","user","--include"]` | `src/superclaude/cli/issue_watch/github.py:175-177` | MATCH |
| 11 | G2 argv | 4.5, 5.1.2, 8.1 | `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | `github.py:180-198` | MATCH |
| 12 | G3 argv | 4.5, 5.1.2 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>` | `github.py:201-220` | MATCH |
| 13 | G4 argv | 4.5, 5.1.2 | same shape on `/comments` with `MARKER_JQ` | `github.py:223-225` | MATCH |
| 14 | G5 argv | 4.5, 8.1 | `gh api graphql -f query=<EDITS_QUERY> -F number=<N> [-f after=<cursor>]` | `github.py:228-244`, `_cursor_args` `:141-147` returns `["-f", f"after={after}"]` | MATCH |
| 15 | G6 argv | 4.5, 8.1 | `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=<N> ...` | `github.py:228-249` | MATCH |
| 16 | G7 argv | 4.5, 5.1.2 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>` | `github.py:252-262` | MATCH |
| 17 | `"gh"` list literals in github.py | 4.5, 5.1.2, 15.2 | five, at lines 177, 183, 204, 231, 255 | `github.py:177, 183, 204, 231, 255` | MATCH |
| 18 | `--method GET` lines | 4.5 | `P/github.py:206-207, 257-258` | `github.py:206-207, 257-258` | MATCH |
| 19 | REPO literal | 1, 8.1 | `REPO = "IronbellyOrg/IronClaude"` at github.py:37 | `github.py:37` | MATCH |
| 20 | CALL_CAP / RESERVED_CALLS | 5.1.2, 11.1 | 35 (:46), 3 (:49); non-reserved stop at 32 | `github.py:46, 49, 448-454` | MATCH |
| 21 | PAGE_SIZE / PAGE_CAP | 11.1 | 100 (:40), 5 (:43) | `github.py:40, 43` | MATCH |
| 22 | DISCOVERY_BOUND / DISCOVERY_WARN | 11.1 | 100 (:486), 80 (cycle.py:47) | `github.py:486`; `cycle.py:47` | MATCH |
| 23 | RATE_LIMIT_MAX_WAIT_S and rule | 5.1.2, 10.3 | 3600; header wait 1..3600 s else now+3600 `rate_limit_clamped` | `github.py:376, 418-431` | MATCH |
| 24 | classify kinds (8) | 5.1.2, 10.2 | timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed | `github.py:345-371` | MATCH |
| 25 | Cycle constants | 10.1/11.1 | MAX_CANDIDATES 10 (:34), DAY_CAP 6 (:36), GH_TIMEOUT_S 20.0 (:37), PROBE_TIMEOUT_S 10.0 (:38), GIT_TIMEOUT_S 10.0 (:39), LAUNCH_TIMEOUT_S 120.0 (:40), DEADLINE_TOTAL_S 240.0 (:41), GH_FLOOR_S 5.0 (:42), LAUNCH_CUTOFF_S 120.0 (:43), SKEW_WARN_S 60 (:44), HEALTH_AGE_S 900 (:45), STALE_AGE_S 86400 (:46) | `cycle.py:34-47` | MATCH (all 12) |
| 26 | Dead constant | 5.1.7, 11.1 | `MAX_LAUNCHES_PER_CYCLE = 1` at cycle.py:35, no other hit in src/ or tests/ | `grep -rn` over src and tests: one hit, `cycle.py:35`; each of the other 13 constants occurs at least twice in cycle.py | MATCH |
| 27 | `_TOP_KEYS` (8 keys) | 9.1 | schema_version, enabled, labels, project_id, owner_account_id, worktree, approvers_file, state_dir | `cycle.py:58-69` | MATCH |
| 28 | Config constants | 9.1 | `DEFAULT_TRIGGER_LABEL = "issue-watch:trigger"`, `DEFAULT_APPROVAL_LABEL = "issue-watch:approved"`, `_LABEL_MAX` 50, `PVT_[A-Za-z0-9_-]{1,64}`, `[1-9][0-9]{0,19}`, `10**20-1`, 1 MiB, network FS list | `cycle.py:50-52, 55-56, 71-75` | MATCH |
| 29 | `enabled` default | 2.3, 9.1 | `raw.get("enabled", False)` at cycle.py:228; gate `:685-686` | `cycle.py:685-686` (`if not deps.config.enabled and not self.dry_run: raise _Stop("not_enabled")`) | MATCH |
| 30 | Exit precedence | 5.1.1, 10.1 | 2, 6, 7, 5, 3, 4; 75 only as sole condition | `cycle.py:462, 466-477` | MATCH |
| 31 | Step order of a real cycle | 2.1, 4.1, 5.1.1 | enabled, setup, lock, DISABLED, load, G1, origin, sweep, G2, order, candidates | `cycle.py:685-737` | MATCH |
| 32 | Launch-step order and guards | 4.1 step 11, 5.1.1.2 | dry-run return, probe, prompt, re-read, day cap, DISABLED, cut-off, origin, pending save, launch | `cycle.py:1026-1112` | MATCH |
| 33 | S1 halt | 4.1, 5.1.1 | `c.launching = True` (1028); halt (833-834) | `cycle.py:1028, 833-834` | MATCH |
| 34 | Gate words E1..E14 | 5.1.1.1 | already_dispatched, claimed, in_backoff, day_cap, unassigned, assigned_other, marker_unreadable, events_*, edited_after_approval, project_* | `cycle.py:915-961`; `predicates.py:162-271` | MATCH |
| 35 | Marker window 300 s | 4.2, 8.3, 11.1 | `SKEW_TOLERANCE_S = 300` at predicates.py:17; `CLAIM_MARKER` line 14; later of created/updated | `predicates.py:14, 17, 274-296` | MATCH |
| 36 | `REASON_TABLE` size and pairs | 5.1.6, 10.2 | 59 words; 27 cycle (exit 2 x7, 6 x5, 3 x5, 4 x2, 5 x2, 75 x1, 1 x1, 0 x4), 17 skip, 9 entry (7 x4, 0 x5), note `re-approved`, 4 warnings (reset_refused exit 2), `operator_reset` | `audit.py:26-102` | MATCH (counted every row) |
| 37 | `once` exit-code table 0,1,2,3,4,5,6,7,75 and words | 5.1.4, 8.2, 10.1 | each code with its word list | `audit.py:26-102`; `cli.py:34-38, 123-137` | MATCH |
| 38 | CLI exit constants | 10.1 | `_EXIT_UNHEALTHY = 1`, `_EXIT_CRASH = 1`, `_EXIT_CONFIG = 2`, `_EXIT_STORE = 6`, `_EXIT_LOCK_HELD = 75` at cli.py:34-38 | `cli.py:34-38` | MATCH |
| 39 | Verbs and options | 5.1.4, 8.2 | once --dry-run; status --json; check-config; init-state; reset ISSUE (1..999999999) --forfeit-guarantee / --rate-limit; default `~/.config/superclaude/issue-watch.json` | `cli.py:31, 111-348` | MATCH |
| 40 | `once` output lines | 5.1.4 | `cycle: <reason>`, `exit: <code>`, dry-run `probe:`, `would_launch:` | `cli.py:130-136` | MATCH |
| 41 | Registration line | 1, 2.2, 3 | `main.py:577-579` | `main.py:577, 579` | MATCH |
| 42 | `dispatch.json` top-level keys (7) | 5.1.3, 6, 16 | schema_version, created_at, next_permitted_at, last_completed_cycle_at, considered, consumed_log, entries | `record.py:120-130` | MATCH |
| 43 | Entry fields (17), order | 5.1.3, 6 | issue ... last_reason (list in doc) | `record.py:69-88` (17 fields, same order) | MATCH |
| 44 | Entry states (6) | 5.1.3, 6, 10.2, 16 | pending, launched, unknown, failed, abandoned, claimed | `record.py:34-36` | MATCH |
| 45 | Retry constants | 9.4, 11.1 | MAX_ATTEMPTS 3 (:434), BACKOFF 10 min (:437), LEASE 60 min (:440), DAY_CAP_WINDOW 24 h (:443) | `record.py:434-443` | MATCH |
| 46 | Store write, modes | 5.1.3, 6 | sorted, indent 2, ASCII, chmod 0600, dir fsync; init-state dir 0700, lock 0600 | `record.py:370-378, 753-802` | MATCH |
| 47 | `MIGRATIONS` ships empty; file names | 5.1.9, 6 | `MIGRATIONS` empty; `dispatch.json`, `lock`, `DISABLED`, `dry-run.json` | `record.py:247, 281-283, 805` | MATCH |
| 48 | stderr cap, shell False | 5.1 table, 11.1 | 500 bytes, `shell=False`, stdin DEVNULL | `runner.py:15, 88-102` | MATCH |
| 49 | status JSON fields / retry | 5.1.4, 8.1 | HEALTH_AGE_S compare, stale, retry argv for `unknown` | `cycle.py:1296-1335` | MATCH |

## Verbatim-comparison table, part 2: claim flow, guard stack, installers, removed code

| # | Item | Document location | Quoted value | Source value (path:line) | Result |
|---|------|-------------------|--------------|--------------------------|--------|
| 50 | Claim launch argv | 4.3, 5.2, 8.1 | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1776-1779` | MATCH |
| 51 | Worktree create argv | 5.2, 8.1 | `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json` | `orca_worktree.py:684-700` | MATCH |
| 52 | Worktree list argv | 5.2, 8.1 | `orca worktree list --repo path:<main> --limit 500 --json` | `orca_worktree.py:314-327` | MATCH |
| 53 | Preflight argv and rule | 5.2, 8.1 | `orca status --json`, 30 s, `ok` true and `runtime.reachable` true | `orca_worktree.py:210-223` | MATCH |
| 54 | Terminal/git argv in worktree step and shim check | 8.1 | `orca terminal list --worktree path:<wt> --json`; `orca terminal close --terminal <handle> --tab --json`; `orca terminal read --terminal <h> --screen --json`; `orca terminal show --terminal <h> --json`; `git -C <wt> ls-files .dev/issues/<N>`; `git fetch origin`; `git rev-parse --verify <base>`; `git -C <wt> rev-parse --absolute-git-dir` | `orca_worktree.py:592, 619, 1568, 1554, 416, 671-672, 1593` | MATCH |
| 55 | L2 install probes | 8.1 | `git -C <wt> config --get core.hooksPath`; `git rev-parse --path-format=absolute --git-path hooks`; `--git-common-dir` | `orca_worktree.py:1348, 1357, 1361` | MATCH |
| 56 | Timeouts, shim, env names | 5.2, 9.3, 11.1 | DEFAULT 120, PREFLIGHT 30, TERMINAL_READ 15, `SC_ORCA_TIMEOUT`, `SC_ORCA_SHIM_INTERVAL`, SHIM_TRIES 5, interval 2.0, L2 self-test 30 s | `orca_worktree.py:88-91, 798-800, 1078` | MATCH |
| 57 | Shim title regex | 5.2 | `sc-launch-v1-<hex>-<MMDD>-<HHMMSS>-<hex4>` | `orca_worktree.py:797` | MATCH |
| 58 | Warning vocabularies | 5.2, 10.2 | 8 worktree codes in rank order; 4 launch codes with REMEDY | `orca_worktree.py:230-239, 802-817` | MATCH |
| 59 | `IR7_REFUSE = False` and branch | 2.3, 5.2, 9.2 | `:822`, refusal branch `:1757-1758`, `:829-831` | `orca_worktree.py:822, 1757-1758, 829-831` | MATCH |
| 60 | `GOVERNED_TOOLS` count; guard commands; version lines | 5.2, 5.3 | 23 tools (`:841-867`); `cat sed tr mkdir mv ln rm`; `# launch-level-guard-version: 1` | `orca_worktree.py:841-867` (14 + 9 = 23), `:871`, `:839`; `launch-level-guard.sh:10` | MATCH |
| 61 | argparse choices / exit rule | 5.2, 8.2 | prompt, launch: worktree, full; pending: worktree, full, full-submit; `--submit needs --level full` exit 2 | `orca_worktree.py:1873, 1883, 1891, 1900-1901` | MATCH |
| 62 | Pending record | 4.3, 5.2, 6 | `~/.claude/state/launch-level/pending/<32 hex>`, dir 0700, file 0600, `.tmp-<nonce>` then `os.replace` | `orca_worktree.py:791, 1488-1512` | MATCH |
| 63 | L2 install modes | 8.3 | hook 0755 hard link; data file 0644 | `orca_worktree.py:1411, 1421-1428` | MATCH |
| 64 | Reuse lookup keys and basename regex | 5.2 | marker, record, basename `^issue-<N>(-|$)`, branch | `orca_worktree.py:373-411` | MATCH |
| 65 | `worktree.json` mode | 5.2, 6 | atomic, 0644 | `orca_worktree.py:183-200` | MATCH |
| 66 | `issue.md` flags, STOP codes, version | 5.2, 8.2 | seven flags (:36-44), version `1.1.0`, `E-CREATE-ONLY-FLAG` :53, `E-CLAIM-ONLY-FLAG` :57, `E-SUBMIT-NEEDS-FULL` :59, Activation :104-110 | `src/superclaude/commands/issue.md:3, 36-44, 53, 57, 59, 104-110` | MATCH |
| 67 | Claim exact commands C1, C3, C4 | 4.5, 5.2, 8.1 | `gh issue edit <N> --repo <R> --add-assignee @me`; `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`; `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/...` | `refs/claim.md:48, 89-92` | MATCH |
| 68 | Claim reads | 4.5, 8.1 | `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name`; `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author`; `gh pr list --repo <R> --state merged --search "merged:>=<date>" --limit 200 --json number,title,mergedAt,files,url` | `refs/claim.md:18, 27-28` | MATCH |
| 69 | Create path X1-X3, return contract, error table | 4.5, 5.2 | `gh issue create --repo <R> --title "[FEATURE]..."`; `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input ...`; ten claim fields | `SKILL.md:74, 103, 123-134, 152-177` | MATCH |
| 70 | Markers | 4.2, 5.2 | `<!-- sc:issue:claim -->` (claim-comment.md:23), `<!-- sc:issue:accuracy-check -->` (accuracy-check-comment.md:20) | both files, last non-blank line | MATCH |
| 71 | ClickUp PUT | 4.5, 8.1 | `PUT https://api.clickup.com/api/v2/task/{task_id}`, body `{"assignees": {"add": [<user id>]}}`, `clickup_claim.py:232-237`; env `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID`, `CLICKUP_LIST_IDS`, `CLICKUP_MAX_PAGES` default 20 | `clickup_claim.py:37-38, 74, 164-172, 233-236`; result words :52-55, 126, 132, 242 | MATCH |
| 72 | `origin_repo.py` exits | 5.2, 8.2 | 0; 1 `E-NO-ORIGIN`; 3 `E-FOREIGN-REPO`; 4 `E-NOT-AN-ISSUE`; 2 argparse | `origin_repo.py:47-50, 61-63` | MATCH |
| 73 | Worker agent pins | 3.1, 5.2 | t3 `claude-gw-tier2b` + `effort: low` (line 7), t2 `claude-gw-tier2`, t1 `claude-gw-tier1b`; tools `Read, Grep, Glob, Write, Bash` (line 5); model line 6 | `src/superclaude/agents/issue-worker-t{1,2,3}.md:5-7`; `tests/skills/test_model_alias_policy.py:29-33` | MATCH |
| 74 | ccsession tier keys | 13.1.7 | lines 85, 93, 104, 113 | `ccsession-models.json:85, 93, 104, 113` | MATCH |
| 75 | Guard registration events and matcher | 5.3, 8.4 | UserPromptSubmit, PreToolUse matcher string verbatim, PreToolUse `Bash` identity, timeout 5 each (`HJ:63-71, 115-124, 125-134`) | `src/superclaude/hooks/hooks.json:63-71, 115-134` (matcher string identical, character by character) | MATCH |
| 76 | Other hooks.json events | 8.4 | SessionEnd :73-83, Edit\|Write 1 s, Bash 3+3, PostToolUse Read/auggie matcher 1, SubagentStart 1+5, SubagentStop 1 | `hooks.json:73-190` | MATCH |
| 77 | Plugin hooks.json differences | 5.3, 8.4 | lacks ccsession-tag entries and `pragmatic-subagent.js`; `async: true` on `freshness-subagent-start.sh`; 154 lines; three scripts byte-identical | `diff` of the two files; `cmp -s` x3; `wc -l` | MATCH |
| 78 | Typed-approval regex | 5.3, 10.2 | `^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)` | `launch-level-guard.sh:347` | MATCH |
| 79 | Marker regex, 13-byte read, level words | 4.3, 5.3 | `\[sc-launch:v1:([0-9a-f]{32})\]` :318; `read -N 13`; worktree/full/full-submit -> W/F/FS, other -> W + note :264-269 | `launch-level-guard.sh:262-269, 318` | MATCH |
| 80 | Level grid (16 cells) and precedence | 5.3, 10.2 | IMPL/TURN blocked at W only; COMMIT/PUSH/SUBMIT/SKILL blocked W, WA, F, allowed FS; ten classes block everywhere; precedence BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL | `launch-level-guard.sh:783-803` | MATCH |
| 81 | 18 block words | 5.3, 12.1 | LL-IMPL ... LL-BROKEN (16 classes + LL-NOBIND + default LL-BROKEN) | `launch-level-guard.sh:42-106` (17 labelled arms), default `:801, 808` | MATCH |
| 82 | IMPL skills; Skill normalisation | 5.3 | `implement`, `task`, `cleanup` at :409; `pr-submit` SUBMIT; `issue` ESCAPE | `launch-level-guard.sh:398-413` | MATCH |
| 83 | `orca` command word only; allow-list | 5.3, 14 D-25 | `orca)` at :457; allow-list `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`; `LL_SA` :485 | `launch-level-guard.sh:457, 480-491`; zero `orca-ide` in the guard | MATCH |
| 84 | G2 rule 2 limits | 5.3 | 8192 bytes, 64 arguments, `--to`, `--run`, `--environment`, `--pairing-code`, prefix rule, bare word/lone `--` ESCAPE | `launch-level-guard.sh:496-537` (:506-511, :524-533) | MATCH |
| 85 | Guard size limit | 5.3, 11.1 | 65536 bytes (`LL-BIG`) | `launch-level-guard.sh:419` | MATCH |
| 86 | `LL-TAMPER` release command and store literals | 5.3 | `rm "$LL_STORE/sessions/$LL_SID" "$LL_STORE/sessions/$LL_SID.ok"`; three literals :20-23 | `launch-level-guard.sh:20-23, 97` | MATCH |
| 87 | L2 words, exits, protected refs, env | 5.3, 8.1, 10.4 | `L2-PROTECTED` 1, `L2-UNKNOWN` 1, `L2-MALFORMED` 2; `refs/heads/main`, `refs/heads/master` (:17); `env -i HOME=... PATH=<uvdir>:/usr/bin:/bin UV_NO_CONFIG=1 timeout 10`; `#!/bin/bash -p`; only hook that exits 1 | `launch-level-pre-push.sh:1, 9-10, 17, 65, 187-208` | MATCH |
| 88 | Identity hook strings, limits, modes | 5.3, 8.1, 10.2, 11.1 | stderr `launch job: governed Bash call cannot be wrapped safely`, `launch job: UV is required for this invocation`, `launch job: invalid invocation or unavailable private state`; stdin 1 MiB; command 32768 bytes; `identify` shapes and reasons stale/orphaned/foreign/unreadable; record keys pid,start,boot,kernel_sid,session_id; request 0400; `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"` | `launch-job-identity.sh:52, 142, 171, 197, 220-260, 433-434, 501, 579, 582` | MATCH |
| 89 | Installer lines and modes | 5.3, 8.1, 13.1.6 | `_FRESHNESS_SCRIPTS` :42; identity :90, guard :93, pre-push :96; chmod 0755 :288; skip-if-exists :282; `main.py:219` (force flag), `:412` (`force=True`), `:211`, `:406` | `install_hooks.py:42, 90, 93, 96, 282-288`; `main.py:211, 219, 406, 412` | MATCH |
| 90 | ccsession installer timeouts | 8.1 | 30 s, 30 s, 60 s; `~/.local/bin` | `install_ccsession.py:33, 98, 119, 138` | MATCH |
| 91 | ccsession-orca env handling | 9.3 | sets `CCSESSION_ORIGIN` (human/agent), unsets NAME and ASK_TIMEOUT; no launch-level text | `ccsession-orca:183, 198-213, 249-256` | MATCH |
| 92 | Contract rule lines | 5.4 | WC-2 :31, WC-3 :53-58, WC-4 :32, WC-5 :59, WC-6 :72, WC-7 :60, WC-8 :40, WC-9 :41, WC-10 :46, WC-11 :47, WC-12 :61, WC-13 :62, WC-14 :63, WC-15 :64, WC-16 :287-289; sections :9, :27, :49, :68, :299; 339 lines; no WC-17; `grant row` once at :57 | `WORKER-CONTRACT.md` (grep of rule anchors and `##` headings; `wc -l` 339) | MATCH |
| 93 | Removal commit facts | 1, B (intro), 2.3 | 01e7a9e23, PR 682, 2026-11-19 18:02 -0600, message sentence "Nothing ran this code: the issue watcher has enabled: false and never ran live" | `git log -1 01e7a9e23` (`2026-11-19 18:02:35 -0600`, subject `(#682)`) | MATCH |
| 94 | Removed package inventory | B.1 | 10 files, 1,597 lines; per-file lines 5, 62, 416, 74, 395, 90, 161, 66, 301, 27 | `git show 01e7a9e23^:<path> \| wc -l` for each of the 10 paths (sum 1597) | MATCH |
| 95 | Removed verbs, exit constants, line anchors | B.2 | 10 verbs at :61, 76, 96, 108, 117, 134, 161, 179, 200, 335; `_EXIT_REFUSED = 1`, `_EXIT_CONFIG = 2`, `_EXIT_LOCK_HELD = 75` (:29-32); option names and choices (channel label/comment/reply; state started/uncertain; instructed/acked/revoked) | `@01e7a9e23^:src/superclaude/cli/issue_pipeline/cli.py` | MATCH |
| 96 | Removed approval text, hash and rows | B.3 | `approved`; `approved ap-<issue>-plan-<12 hex> plan-sha256=<64 hex>`; `refused:bare`, `refused:mismatch`, `refused:malformed`; 11 plan-hash refusal words in order; 8-byte big-endian length prefixes; states reserved/started/uncertain and recorded/instructed/acked/revoked; file names `adoption-<issue>-<stage>.json`, `approval-<issue>-<stage>-<64 hex>.json`; marker `<!-- sc:stage:plan id=<record id> plan=<64 hex> -->` | `@01e7a9e23^`: `approval_line.py:18-21, 33-62`; `plan_hash.py:24-36, 77-90`; `approval_record.py:43-46, 128-153`; `reads.py:42` | MATCH |
| 97 | `release-worker` | B.4 | `O_WRONLY\|O_CREAT\|O_EXCL\|O_NOFOLLOW`, 0600; refusals `bad-session-id`, `no-store`, `not-bound`, `not-worktree-level`; `already-released` | `@01e7a9e23^:.../release.py:46-62` | MATCH |
| 98 | Removed contract text and guard case | B.5, B.6 | old contract 350 lines; WC-17 at :59; duties :291-300 (adopt :295 ... never :300); old guard 811 lines; TAMPER case words at :441-444 | `git show 01e7a9e23^:...WORKER-CONTRACT.md` (350 lines; lines 59, 291-300), `...launch-level-guard.sh` (811 lines; :441-445) | MATCH |
| 99 | Removed tests and edits | B.8 | 116 tests in 10 files (2,391 lines) + 1 registration test (15 lines); `test_worker_contract.py` 3,181 -> 3,135 lines (+8/-54), 61 -> 59 tests; `test_launch_level_guard_worker.py` 330 -> 300 (-30), 13 -> 11 tests; changelog +4; `cli-groups.md` 10 lines; guard 5 removed/2 added x2 | `git show --numstat 01e7a9e23`; per-file `wc -l` and `grep -c 'def test_'` at `01e7a9e23^` | MATCH |

## Appendix A line counts (wc -l) and test counts (grep -c 'def test_')

All rows of A.1 to A.4 were recomputed in one pass over the snapshot (48 rows: 21 + 11 + 9 + 7 lines of the tables). Every Lines and Tests value matched, including: test_cycle 4982/237, test_github 2161/141, test_record 2377/147, test_cli 1672/60, test_security_invariants 1013/16, test_no_text 971/22, test_launch 952/66, test_audit 849/46, test_predicates 732/44, conftest 1155/0, guard 4631/163 (162 strict: the extra hit is the string literal at test_launch_level_guard.py:4615), job_identity 1530/56, pre_push 1194/34, test_issue_protocol 1055/62, test_issue_orca_worktree 2501/109, test_worker_contract 3220/59, test_ccsession_tag 7101/277, test_ccsession_tiers 3821/149. Derived totals also match: watcher tests 19,801 lines / 867 functions / 19 fixtures; guard-test set 17 files, 24,388 lines, 921 (920 strict) functions.

Source line counts in Sections 1, 3.1, 5.2, 5.3 (cycle 1406, github 960, record 865, audit 404, launch 370, cli 348, predicates 312, runner 130, `__init__.py` 0, issue.md 117, SKILL.md 197, claim/create/labels/tiers/chains 150/99/67/58/40, orca_worktree 1906, clickup_claim 270, origin_repo 195, launch-prompt 34, claim-comment 23, accuracy-check-comment 20, agents 35 each, guard 808, identity 582, pre-push 208, hooks.json 192 and plugin 154, install_hooks 614, install_ccsession 161, ccsession-orca 263, WORKER-CONTRACT 339, 15 templates, 8 design docs 942/706/509/470/627/51/57/119) all matched `wc -l` / `ls`.

Test names with line numbers cited in 5.2, 5.3, 12, 13 (about 50 names, for example `test_grid_policy` :3394, `test_grid_complete` :3401, `test_grid_level_steps` :3457, `test_precedence_order` :4520, `test_design_table_holds_all_eighteen_ids` :1712, `test_apr_*` :3737/:3800/:3852, worker-test :74/:187/:213/:262, `test_ir7_shipped_switch_is_off` :639, `test_reasons_pin_59_names` :214, clickup :277/:311/:548) all exist at the cited lines.

## Section 13 skeleton check

| Skeleton | Names used | Result |
|---|---|---|
| 13.1.1 reason word | `REASON_TABLE` (`audit.py:26`), `REASONS` (:104), `_Stop(reason, stamp)` (`cycle.py:503`), `self._cond` (:587), `_stopped` (:590), `exit_for` (:480), `resolve_exit` (:466); entry shape `"name": ("<kind>", <exit>)` | exist, signatures consistent |
| 13.1.2 config key | `_TOP_KEYS` (:58), `Config` (:97), `load_config` (:195), `raw.get(...)` pattern | exist |
| 13.1.3 `gh` call | `argv_*` pattern, `_issue_arg` :111, `_page_arg` :118, `_cursor_args` :141, `_trigger_arg` :150, `_login_arg` :168, `_call` :557, `classify` :345 | exist |
| 13.1.4 pipeline level | `BLOCK_MARKER` (`orca_worktree.py:743`), `render_prompt` :746, choices at :1873/:1883/:1891, guard case arms :264-269 and :785-803 | exist; case-arm shape matches |
| 13.1.5 guard class | precedence list :783, grid :785-803, `LL-BROKEN` default :801 | exist |
| 13.1.6 hook registration | `_FRESHNESS_SCRIPTS`, hooks.json PreToolUse group shape (`matcher`, `hooks[{type, command, timeout}]`) | exist, shape matches |
| 13.1.7 worker tier | frontmatter keys, `WORKERS` dict shape `("claude-gw-<tier>", "<tier>")` (`test_issue_worker_agents.py:21-26`), `ISSUE_WORKER_PINS`, `TIER_TEXT_ALLOWED` | exist, shape matches |
| 13.1.8 contract rule | `RULE_PHRASES` (`test_worker_contract.py:25`), `_check_never_as_worker` :734, `WRITE_VERB_RE` :1863, `test_contract_states_rule` :877 | exist |

## Findings

Result: no MISMATCH was found in any quoted argv, command, exit code, constant value, field name, state name, reason word, guard word, hook event, level-matrix cell, count or skeleton signature. Zero BLOCKING findings. The notes below are MINOR only.

| ID | Severity | Location | Quoted value | Source value (path:line) | Required fix |
|----|----------|----------|--------------|--------------------------|--------------|
| CEA-1 | MINOR | Section 5.4, "Who starts a worker after a claim" (document l.1358) | `"was removed in issue 655 ... and until [its replacement] lands no contract rule says who starts that worker"` | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268` reads "(the section "Issue pipeline duties") were removed in issue 655, PR D; the orchestrator design replaces them, and until it lands no contract rule says who starts that worker" | Optional: keep the quotation marks exact ("were removed", "until it lands") or drop the quotation marks. The meaning is faithful; only a prose quote is altered, no code value. |
| CEA-2 | MINOR | Section 8.4 table, SessionStart row (l.1486) | `:3-42` | `src/superclaude/hooks/hooks.json:3-43` (the SessionStart array closes on line 43) | Optional: write `:3-43`. |
| CEA-3 | MINOR | Section 5.1.2 / 14.3.1 U-2 | `GH_ERROR_SIGNS` `267-277` and `P/github.py:267-278` | `github.py:269-277` is the table; 267-268 is the lead comment and 278 the docstring | None needed: both ranges contain the table; the two citations differ from each other by one line. |
| CEA-4 | MINOR | Section 1 key statistics (l.210) and Appendix A.1 | "20 files in `tests/issue_watch/` (19 test modules plus `conftest.py`)" | the directory also holds an empty `tests/issue_watch/__init__.py` (0 lines), so `ls` shows 21 `.py` files; the 19,801-line and 867-test totals are unaffected | None needed: the stated parenthesis is accurate; mention `__init__.py` only if a file count of the directory is wanted. |
| CEA-5 | MINOR | Section 2.2 cycle row (l.295) | `_Cycle` (:485-1222) | `class _Cycle` starts at `cycle.py:541`; `:485` is the "Part 2" comment above `_Skip`/`_Stop`; `run_cycle` ends near :1222 | None needed: a section range, not a symbol line. |

## Checks performed

| Measure | Count |
|---|---|
| Rows in the verbatim-comparison tables above (each row groups several quoted values, all opened in the snapshot) | 99 |
| Individual quoted values compared (argv elements, constants, words, line anchors counted separately inside those rows) | about 400 |
| Quoted argv lists compared | 33 (launch argv, retry argv, G1-G7, origin check, orca discovery, claim launch, worktree create/list, preflight, terminal list/close/show/read, git ls-files/fetch/verify/absolute-git-dir/config/git-path/git-common-dir, `uv run` identity exec, L2 identity env line, pending, plus removed-code argv forms) |
| Exit-code tables compared | 9 (`once` 0/1/2/3/4/5/6/7/75; status/check-config/init-state/reset; claim scripts 0/1/2/3/4; guard 0/2; L2 0/1/2; identity 0/2; removed package 1/2/75; `issue-watch` precedence 2,6,7,5,3,4; `orca_worktree.py` 0/2) |
| Constant tables compared | 5 (cycle 12 timings and caps; github 5 caps; record 4 retry constants; orca_worktree timeouts; audit rotation and runner cap) |
| Vocabularies compared word by word | 8 (59 `REASON_TABLE` words with kinds and exits; 18 `LL-*` words; 8+4 `W-*` codes; 13 STOP codes; 6 entry states; 17 entry fields; 7 store keys; 12 ClickUp result words) |
| Files with `wc -l` checked | about 45 source files, 48 Appendix A test rows, 10 removed files |
| Files with `def test_` count checked | 48 (Appendix A) plus 11 removed test files |
| Test function names with cited line numbers checked | about 50 |
| Section 13 skeletons checked against real names and signatures | 8 of 8 |
| Removed-code facts read with read-only `git show` / `git log` / `git ls-tree` at `01e7a9e23^` | 9 files, 3 listings, 2 commit stats |
| Files written outside the report | 0; nothing under the snapshot was written |

Tool engagement: Read: 33 | Grep: 14 | Glob: 0 | Bash: 14 (all read-only: `wc -l`, `grep -c`, `ls`, `sed -n`, `cmp -s`, `diff`, read-only `git show`/`git log`/`git ls-tree`). No web research (tavily_search: 0, tavily_extract: 0, fallbacks: 0). One Grep call failed once with an environment error (`posix_spawn rg` EACCES) and was replaced by an equivalent Bash `grep`.

Confidence: Verified: 99 of 99 table rows plus all Appendix A, source line-count, test-name and skeleton checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% of the items opened. Items not opened: the `swarm/atomic.py` internals and every runtime claim marked [UNVERIFIED] in the document (live `gh` and Orca replies, PR numbers #447 and #448, the "44 sample payloads" observation run, which is a research-folder artefact, not a snapshot file); these are outside the lens (they are not quoted code values) and the document labels them [UNVERIFIED] itself.

Self-audit: I can point to the table rows above and the tool calls behind them. The document is unusually accurate; the likely reasons are that every quoted value was copied from a read of the snapshot and that the assembler reconciled the research errata (for example the guard-worker test delta -30 versus -56 and the SKEW_TOLERANCE_S label). The only deviations found are the five MINOR notes, none of which changes a code value.

## Verdict: PASS

Status: Complete


