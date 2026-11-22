# Synthesis 05: Integration, Configuration, Errors, Performance, Test-Pin Matrix

**Sections:** 8, 9, 10, 11, Appendix A
**Status:** Complete
**Date:** 2026-11-20

Conventions for this file. Paths are repository-relative against the 61ac2c2e6 snapshot. `P` = `src/superclaude/cli/issue_watch/`; `SK` = `src/superclaude/skills/sc-issue-protocol/`; `HK` = `src/superclaude/hooks/scripts/`. Status words are only BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. Tags: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED].

---

## 8. API & Integration Points

The pipeline has no HTTP endpoint of its own. Its integration surface is a set of subprocess commands (`gh`, `git`, `orca`, `uv`, `jq`), one ClickUp REST call, files under `~/.claude/state/launch-level/`, and Claude Code hook registrations. The watcher part writes nothing to GitHub: all seven `gh` argv are reads (`P/github.py:107-108`, `:206`, `:257`; greps in research 01 section 13 and research 02 section 7(c)).

### 8.1 External Commands (every `gh`, `orca`, ClickUp and git command)

**Watcher (BUILT-OFF (enabled:false) for real cycles; `once --dry-run` runs the same reads and BUILT-ON).** Every argv runs through `SubprocessRunner.run` with `shell=False`, stdin `DEVNULL`, a mandatory timeout (`P/runner.py:91-101`). Repository literal: `REPO = "IronbellyOrg/IronClaude"` (`P/github.py:37`).

| Piece | Command (exact argv or command line) | R/W | Actor | File:line |
|---|---|---|---|---|
| G1 login | `["gh","api","user","--include"]` | Read | watcher | `P/github.py:175-177`; call `P/cycle.py:755` |
| G2 discovery | `["gh","issue","list","--repo","IronbellyOrg/IronClaude","--state","open","--label",<trigger>,"--assignee",<login>,"--json","number,labels,assignees,state","-L","100"]` | Read | watcher | `P/github.py:180-198`; `P/cycle.py:796` |
| G3 events (G3' = reserved) | `["gh","api","--method","GET","repos/IronbellyOrg/IronClaude/issues/<N>/events","-F","per_page=100","-F","page=<P>","--jq",EVENTS_JQ]` | Read | watcher | `P/github.py:201-220`; `P/cycle.py:907, 944, 996` |
| G4 claim-marker comments | same shape on `.../issues/<N>/comments` with `--jq MARKER_JQ` (body reduced to a boolean) | Read | watcher | `P/github.py:223-225`; `P/cycle.py:905, 926, 942` |
| G5 edits | `["gh","api","graphql","-f","query=<EDITS_QUERY>","-F","number=<N>"]` plus `["-f","after=<cursor>"]` from page 2 | Read (GraphQL query; POST by design) | watcher | `P/github.py:228-244`; `P/cycle.py:948` |
| G6 project items (G6' = reserved) | `["gh","api","graphql","-f","query=<PROJECT_ITEMS_QUERY>","-F","number=<N>"]` plus optional cursor | Read | watcher | `P/github.py:228-249`; `P/cycle.py:957, 1013` |
| G7 re-read | `["gh","api","--method","GET","repos/IronbellyOrg/IronClaude/issues/<N>","--jq",REREAD_JQ]` | Read | watcher | `P/github.py:252-262`; `P/cycle.py:983` |
| Origin check | `["git","-C",<worktree>,"remote","get-url","origin"]` | Read | watcher | `P/launch.py:244`; `P/cycle.py:721, 1074` |
| Orca discovery | `[<abs path of orca-ide, then orca>,"skills","list","--json"]`; accepted only if topic `orca-cli` is listed | Read (local; the doc's "no runtime contact" claim is [UNVERIFIED]) | watcher | `P/launch.py:163-203`; `P/cycle.py:1048` |
| The one Orca launch (12 elements) | `<orca> agent launch --agent claude --worktree path:<abs worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json`, run with `cwd=<worktree>` | Write (starts a Claude session) | watcher | `P/launch.py:95-116, 358-370`; `P/cycle.py:1099` |
| Retry argv (printed only) | the launch argv with `--retry-launch <op-id>` before `--json` (14 elements) | none (printed by `status`; nothing runs it; automatic retry NOT BUILT) | `status` | `P/launch.py:119-132`; `P/cycle.py:1308-1312` |

**Claim (`/sc:issue --claim`; every write is made by the orchestrating model, workers are read-only).** `<R>` comes from `origin_repo.py` only (`SK/SKILL.md:72-73`).

| Piece | Command | R/W | Actor | File:line |
|---|---|---|---|---|
| C1 assign | `gh issue edit <N> --repo <R> --add-assignee @me` | Write | orchestrator, Wave 3 | `SK/refs/claim.md:48`; `SK/SKILL.md:74` |
| C2 ClickUp assign | `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"`; the one non-GET request is `PUT https://api.clickup.com/api/v2/task/{task_id}` body `{"assignees": {"add": [<user id>]}}` | Write (only if one task matches) | orchestrator runs script | `SK/scripts/clickup_claim.py:232-237`; `SK/refs/claim.md:50` |
| C3 / C3' accuracy comment | `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`, or `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | Write | orchestrator, Wave 6 | `SK/refs/claim.md:89, 91` |
| C4 / C4' claim comment (ends with the marker) | `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md`, or the same `gh api -X PATCH` form | Write | orchestrator, Wave 6 | `SK/refs/claim.md:92` |
| Claim reads | `git remote get-url origin`; `gh auth status`; `orca status --json`; `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name`; `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author`; `gh api user -q .login`; `gh pr list --repo <R> --state merged --search "merged:>=<date>" --limit 200 --json number,title,mergedAt,files,url`; `git fetch origin` (the only worker git write); `git log --since=<createdAt> --name-only origin/<B>`; ClickUp `GET /user`, `GET /team/{ws}/task?page&subtasks=true&include_markdown_description=true[&list_ids[]]` | Read | origin_repo.py, orchestrator, T3 worker, clickup_claim.py | `SK/scripts/origin_repo.py:159-164`; `SK/refs/claim.md:16-29`; `clickup_claim.py:176, 185-191` |
| Create path X1-X3 (not the claim) | `gh issue create --repo <R> --title "[FEATURE\|BUG] <title>" --body-file ... [--label ...] [--type ...]`; `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`; `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md` | Write | orchestrator, Wave 5 | `SK/refs/create.md:92-96`; `SK/SKILL.md:103` |
| Worktree step | `git rev-parse --path-format=absolute --git-common-dir`; `orca worktree list --repo path:<main> --limit 500 --json`; `git fetch origin`; `git rev-parse --verify <base>`; `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json` (no `--agent`, no `--issue`, no `--pr`); `git -C <wt> ls-files .dev/issues/<N>`; `orca terminal list --worktree path:<wt> --json`; `orca terminal close --terminal <handle> --tab --json` | Write (create, close first tab) | `orca_worktree.py worktree` | `SK/scripts/orca_worktree.py:287-291, 314-350, 684-700, 568-622` |
| Preflight | `orca status --json` (30 s); passes only with `ok` true and `runtime.reachable` true | Read | `orca_worktree.py preflight` | `orca_worktree.py:210-223` |
| Governed launch | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` (no `--model`, `--effort` or link flag) | Write | `orca_worktree.py launch` | `orca_worktree.py:1776-1779` |
| Shim check | `orca terminal read --terminal <h> --screen --json` then `orca terminal show --terminal <h> --json`, up to 5 tries, 2.0 s apart | Read | `orca_worktree.py launch` | `orca_worktree.py:1564-1583, 1551-1561` |
| L2 install probes | `git -C <wt> config --get core.hooksPath`; `git rev-parse --path-format=absolute --git-path hooks`; `git -C <wt> rev-parse --absolute-git-dir` (mirror file) | Read | `install_l2`, `record_launch` | `orca_worktree.py:1348-1350, 1356-1367, 1593` |

**Guard stack and installers.**

| Piece | Command / invocation | R/W | Actor | File:line |
|---|---|---|---|---|
| L1 guard | Claude Code hook `~/.claude/hooks/launch-level-guard.sh` (stdin JSON; tools used: `jq`, `sed`, `tr`, `cat`, `mkdir`, `mv`, `ln`, `rm`); exit 0 or 2 only | Write (session files under `sessions/`) | Claude Code | `HK/launch-level-guard.sh:4-6, 291-313` |
| Job identity | `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"`; modes `hook`, `execute SESSION TOOL_ID COMMAND`, `identify [PID]`, `prepare SESSION COMMAND [TOOL_USE_ID]`, `run TOKEN`; a governed Bash command is rewritten to `/bin/bash <script> execute <sid> <tool_use_id> <command>` | Write (`requests/`, `jobs/`) | Claude Code hook; L2 | `HK/launch-job-identity.sh:541-582, 491-497` |
| L2 pre-push | git `pre-push` hook; asks `$L2_HOME/.claude/hooks/launch-job-identity.sh identify $$` under `cd /` and `env -i HOME=<pinned> PATH=<uvdir>:/usr/bin:/bin UV_NO_CONFIG=1 timeout 10`; exit 0, 1 or 2 | none (writes no file, calls no git) | git | `HK/launch-level-pre-push.sh:52-101, 187-208` |
| Hook installer | `superclaude install` / `update`: `install_hooks()` copies scripts to `~/.claude/hooks/` (0755) and merges `hooks.json` into `~/.claude/settings.json` (backup `settings.json.bak.<UTC stamp>`) | Write | person | `src/superclaude/cli/install_hooks.py:156-246`; callers `main.py:219, 412` |
| ccsession installer | `wire_ccsession()` symlinks `ccsession`, `ccsession-orca` into `~/.local/bin`; runs `unseed-env.py`, `retention.py ensure`, `ccsession --migrate-names` (30 or 60 s timeouts) | Write | person | `src/superclaude/cli/install_ccsession.py:11-142`; callers `main.py:211, 406` |

### 8.2 CLI Surface

| Verb | Options | Exit codes | Evidence |
|---|---|---|---|
| `superclaude issue-watch once` | `--dry-run`, `--config PATH` (default `~/.config/superclaude/issue-watch.json`) | 0, 1, 2, 3, 4, 5, 6, 7, 75 (Section 10.1) | `P/cli.py:111-137`; registered `src/superclaude/cli/main.py:577-579` |
| `issue-watch status` | `--json`, `--config`; no platform check | 0 healthy; 1 unhealthy; 2 config; 6 store | `P/cli.py:164-182` |
| `issue-watch check-config` | `--config`; static check only (no `gh`, no Orca, no origin, no store) | 0 valid; 2 invalid | `P/cli.py:185-198` |
| `issue-watch init-state` | `--config` | 0 created; 2 config; 6 exists or unwritable | `P/cli.py:201-214` |
| `issue-watch reset` | optional `ISSUE` (1..999999999), `--forfeit-guarantee`, `--rate-limit`, `--config`; needs `ISSUE --forfeit-guarantee` or `--rate-limit`, not both | 0; 2 usage or refused; 6; 75 | `P/cli.py:282-348` |
| `/sc:issue` | `--claim <N\|#N\|url>`, `--create`, `--depth`, `--mode`, `--type` (create only), `--pipeline worktree\|full\|none`, `--submit` (only with explicit `--pipeline full`); no repo, dry-run or preview option | STOP codes (Section 10.2) | `src/superclaude/commands/issue.md:36-59` |
| `--pipeline` levels | `none` ends after Wave 6 (no worktree, no agent); `worktree` stops at the plan boundary until a typed `/sc:implement` or `/task` line; `full` runs every step with no commit, push or PR; `full --submit` adds commit, push, `/sc:pr-submit --monitor 3` | n/a | `SK/refs/claim.md:81-96`; `SK/templates/launch-prompt.md:20-34` |
| `orca_worktree.py` | `preflight`; `worktree --repo --number --base --source`; `prompt --template --level worktree\|full [--submit] ... --out`; `launch --number --source --level worktree\|full [--submit]`; `pending --level worktree\|full\|full-submit` | 0 for every runtime outcome (one JSON object); 2 for argparse errors incl. `--submit needs --level full` | `orca_worktree.py:11-12, 1857-1902` |
| `origin_repo.py` | `--claim <arg>` prints `{"repo","number"}` | 0; 1 `E-NO-ORIGIN`; 2 argparse; 3 `E-FOREIGN-REPO`; 4 `E-NOT-AN-ISSUE` | `SK/scripts/origin_repo.py:45-50, 177-191` |
| `clickup_claim.py` | `--issue-url`, `--issue-number`, `--repo` | 0 with one JSON object; 2 bad arguments only | `SK/scripts/clickup_claim.py:245-259` |

### 8.3 Hand-off Contracts Between Pieces

| Contract | Producer | Consumer | Format | Evidence |
|---|---|---|---|---|
| Launch prompt | watcher `build_claim_prompt(n)` | the launched Claude session running `/sc:issue` | exactly `/sc:issue --claim <N> --pipeline none`; `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`; level `none` and agent `claude` hard-coded | `P/launch.py:33, 84-92`; `issue.md:48`; pinned `tests/issue_watch/test_security_invariants.py:936-1009` |
| Claim marker | claim session (comment ending `<!-- sc:issue:claim -->`) | watcher G4 `marker_in_window` (window: marker time at or after `pending_at` minus 300 s, else after `approved_at`) | hidden comment line; G4 reduces the body to a boolean | `P/predicates.py:14, 17, 274-296`; `SK/templates/claim-comment.md:23`; `tests/issue_watch/test_marker_contract.py` |
| Governed launch prompt | `orca_worktree.py launch` | L1 guard on the agent's first `UserPromptSubmit` | `[sc-launch:v1:<32 hex nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it.`; regex `\[sc-launch:v1:([0-9a-f]{32})\]` | `orca_worktree.py:1779`; `HK/launch-level-guard.sh:318` |
| Launch-level files | `publish_pending` (`launch` or `pending`) then the guard | guard, identity hook, L2 hook | `~/.claude/state/launch-level/pending/<nonce>` holds one word `worktree`, `full` or `full-submit` (file 0600, dirs 0700); guard renames it to `sessions/.take-<sid>` and hard-links `sessions/<sid>`; `sessions/<sid>.ok` (empty) = approval at level `worktree` | `orca_worktree.py:791, 1488-1512, 1759-1761`; guard `:299-313, 347-360, 372-376` |
| Identity records | identity hook (`execute`/`prepare`, supervisor) | identity `run`; L2 via `identify` | `requests/<32 hex>` JSON (0400, single use); `jobs/<kernel-sid>.json` with keys `pid, start, boot, kernel_sid, session_id`; `identify` prints one of five JSON shapes | `HK/launch-job-identity.sh:140-174, 215-260, 307-375`; `HK/launch-level-pre-push.sh:82-88` |
| L2 install | `install_l2` in `cmd_launch` | git, `l2_status` | `<git-common-dir>/hooks/pre-push` (0755, hard link) plus data file `pre-push.launch-level` (0644; line 1 `HOME`, line 2 `uv` directory); never replaces an existing entry | `orca_worktree.py:1386-1442, 1754` |
| Launch record | `record_launch` | `cmd_worktree`, `cmd_launch`, `cmd_prompt` | `<D>/worktree.json` `{"path","status","launch":{"level","submit","at"}}` plus mirror `<wt git dir>/sc-issue-launch-<N>.json` | `orca_worktree.py:507-524, 1586-1643` |
| Worker output | `issue-worker-t1/t2/t3` | orchestrator | worker returns only the paths it wrote under `.dev/issues/<N>/`; one retry on empty | `SK/SKILL.md:66`; `src/superclaude/agents/issue-worker-t*.md:35` |
| Config cross-consumer | operator file `~/.config/superclaude/issue-watch.json` | `agent-work-report` skill expects key `orchestrator_repo` | the watcher loader rejects that key (`config_invalid`, exit 2): the two consumers contradict each other [CODE-CONTRADICTED]; see Section 14 | `P/cycle.py:58-69, 216-220`; `skills/agent-work-report/scripts/common.py:22-40` |
| Coordinator hand-off after a `--pipeline none` claim | nothing in the snapshot | a person-opened coordinator (prose only) | NOT BUILT; contract text was removed; no code calls `orca_worktree.py worktree` or `worker-start` for a claimed issue; see Section 14 | `issue.md:85`; `SK/refs/claim.md:96`; `src/superclaude/core/WORKER-CONTRACT.md` (no "Issue pipeline duties") |
| Binding a coordinator-started worker (`orca_worktree.py pending`) | the verb exists; no production caller | L1 guard G2 rule 2 | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON; no production caller found; see Section 14 | `orca_worktree.py:1515-1523, 1886-1893`; test callers `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498` |

### 8.4 Hook Registrations (`src/superclaude/hooks/hooks.json`, 192 lines)

| Event | Matcher | Command | Timeout (s) | Lines |
|---|---|---|---|---|
| SessionStart | none / `*` / `startup` / `startup\|resume` | `session-init.sh` (10); `freshness-session-start.sh` (5); `codegraph-session-start.sh` (5); ccsession-tag `session-start.sh` (5) | 10, 5, 5, 5 | `:3-42` |
| UserPromptSubmit | none | `freshness-user-prompt.sh` (3); ccsession-tag `session-name.sh` (5); `~/.claude/hooks/launch-level-guard.sh` (5) | 3, 5, 5 | `:45-71` |
| SessionEnd | none | ccsession-tag `session-name.sh` | 5 | `:73-83` |
| PreToolUse | `Edit\|Write` | `freshness-pre-edit.sh` | 1 | `:85-94` |
| PreToolUse | `Bash` | `block-bare-python.sh`; `require-orca-worktree-agent.sh` | 3, 3 | `:95-114` |
| PreToolUse | `^(Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Monitor\|Workflow\|RemoteTrigger\|SendMessage\|Cron[A-Za-z]*\|Schedule[A-Za-z]*)$\|^mcp__.*(merge\|push\|commit\|pull_request\|create_or_update_file\|delete_file\|update_ref\|create_ref\|create_branch)` | `~/.claude/hooks/launch-level-guard.sh` | 5 | `:115-124` |
| PreToolUse | `Bash` | `~/.claude/hooks/launch-job-identity.sh` (after the guard in file order) | 5 | `:125-134` |
| PostToolUse | `Read`; auggie/augment matcher | `freshness-post-read.sh` (async); `auggie-flag-clear.sh` | 1 | `:136-157` |
| SubagentStart / SubagentStop | none | `freshness-subagent-start.sh`, `pragmatic-subagent.js`; `freshness-subagent-stop.sh` (async) | 1, 5, 1 | `:159-190` |

No registration has an `onFailure` key (pinned by `tests/hooks/test_launch_level_guard_registration.py:64`). `launch-level-pre-push.sh` is not in `hooks.json`; the claim installs it as a git hook (Section 8.3). The plugin copy `plugins/superclaude/hooks/hooks.json` (154 lines) carries the same three launch-level registrations; it also lacks the ccsession-tag entries and the `pragmatic-subagent.js` entry, and has `async: true` on `freshness-subagent-start.sh` [CODE-VERIFIED by diff; research 05 section 4.1]. The three launch-level scripts are byte-identical in both trees.

### 8.5 External Service Dependencies

| Service | Purpose | Failure mode | Fallback |
|---|---|---|---|
| GitHub via `gh` (login, `read:project` scope) | discovery, approval replay, re-read | unauthenticated, missing scope, rate limit, 5xx, non-JSON map to `gh_auth_failed`, `project_read_failed`, `rate_limited`, `gh_timeout`, `gh_non_json` (exit 3 or 5) | fail closed: skip or stop; no write happens. All 19 reply fixtures are assumed shapes [UNVERIFIED] |
| Orca CLI (`orca-ide`, then `orca`) | the only way to start a session | not found: `orca_not_found` (exit 2); unusable launch reply: `launch_unknown` (exit 7) | never auto-retried; `status` prints a retry command |
| ClickUp API | optional assignment mirror | any error becomes a non-fatal JSON `error` reason | claim continues; exit 2 (bad arguments) stops but keeps the GitHub assignment (`SK/refs/claim.md:51`) |
| `uv`, `jq`, `/proc`, `pidfd_open` | guard and identity hooks | governed session: fail closed (exit 2); ordinary session: fail open (exit 0) | claim IR-4 preflight refuses a launch when they are absent (`W-ENFORCEMENT-ABSENT`) |

---

## 9. Configuration & Environment

### 9.1 Watcher Configuration File (`~/.config/superclaude/issue-watch.json`, or `--config PATH`)

The loader is strict: any key outside `_TOP_KEYS` is `config_invalid` (exit 2), error details never echo file values, and no sample file ships in the snapshot (Glob `**/issue-watch*.json` is empty). Only the eight top-level keys below exist (`P/cycle.py:58-69`).

| Key or setting | Where defined | Default | Valid values | Purpose | Evidence |
|---|---|---|---|---|---|
| `schema_version` | `Config` loader | none (required) | integer `1` (`true` and `1.0` fail) | file format version | `P/cycle.py:222-226` |
| `enabled` | `Config.enabled` | `false` (`raw.get("enabled", False)`) | JSON boolean | gate for real cycles; `once --dry-run` ignores it | `P/cycle.py:228-230, 685-686` |
| `labels.trigger` | `Config.trigger_label` | `issue-watch:trigger` (`DEFAULT_TRIGGER_LABEL`) | 1..50 chars, no control character, no comma, no double quote, no leading `-` | label that selects issues in G2 | `P/cycle.py:55, 71, 127-139, 240-241` |
| `labels.approval` | `Config.approval_label` | `issue-watch:approved` (`DEFAULT_APPROVAL_LABEL`) | same rules; must differ from `labels.trigger` | label whose add-event is the human approval | `P/cycle.py:56, 242-243` |
| `project_id` | `Config.project_id` | none (required) | `PVT_[A-Za-z0-9_-]{1,64}` | the one GitHub Project the issue must sit in (Status `Backlog`) | `P/cycle.py:72, 245-249` |
| `owner_account_id` | `Config.owner_account_id` | absent = no pin | integer 1..10**20-1 | pins the G1 account id; mismatch is `account_id_mismatch` | `P/cycle.py:74, 251-255, 768-769` |
| `worktree` | `Config.worktree` | none (required) | absolute path (no `~` expansion) to an existing directory whose `origin` is `IronbellyOrg/IronClaude` | `--worktree path:` and `cwd` of the Orca launch | `P/cycle.py:118-124, 257-259, 371-377` |
| `approvers_file` | `Config.approvers_file` | none in code (runbook example `~/.config/superclaude/issue-watch-approvers.txt`) | absolute path; regular file, euid-owned, no group/other write bit, at most 1 MiB, UTF-8, one decimal id per line (`[1-9][0-9]{0,19}`), `#` comments only at line start, at least one id | allow-list of approver account ids | `P/cycle.py:75, 298-361` |
| `state_dir` | `Config.state_dir` | `$XDG_STATE_HOME/superclaude/issue-watch`, else `~/.local/state/superclaude/issue-watch` | absolute path; a network filesystem (`nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p`) is refused; unreadable `/proc/self/mountinfo` skips the check | holds `dispatch.json`, `lock`, `DISABLED`, `audit.jsonl*`, `dry-run.json` | `P/cycle.py:50-52, 187-192, 261-272` |

`check-config` is a static check only and succeeds without `gh`, Orca, a correct origin or an initialised store (`P/cycle.py:371-377`).

### 9.2 Claim, Guard and Install Settings

| Key or setting | Where defined | Default | Valid values | Purpose | Evidence |
|---|---|---|---|---|---|
| `--pipeline` default-level rule | model-applied prose, not code | explicit value wins; unreadable type, complexity or hours gives `worktree`; bug gives `full`; simple or medium feature of 16 h or less gives `full`; complex feature or over 16 h gives `worktree` | `worktree`, `full`, `none` | picks how far the launched agent runs; prints `Level: <L> (explicit)` or `(default: <reason>)` | `SK/refs/claim.md:81`; `issue.md:43`; pinned as text only by `tests/skills/test_issue_protocol.py:774, 791` |
| `--pipeline` for the watcher | `P/launch.py:33, 92` | always `none` | not configurable | watcher launches stop after the claim comments | `issue.md:48` |
| `--submit` | `issue.md:44` | off | only with explicit `--pipeline full`; otherwise `E-SUBMIT-NEEDS-FULL` (script exit 2) | adds commit, push and `/sc:pr-submit --monitor 3` | `orca_worktree.py:1900-1901` |
| `superclaude install` hooks | `install_hooks(force=False)` | existing scripts in `~/.claude/hooks/` are skipped | `--force` refreshes; `update` uses `force=True` | a plain install keeps an older guard on disk; IR-4 refuses a guard lacking `# launch-level-guard-version: 1` | `install_hooks.py:282-289`; `main.py:219, 412`; `orca_worktree.py:986-988` |
| Settings merge | `_merge_settings` | additive, ownership by command path, backup before write, malformed target refused | n/a | registers the three launch-level hooks | `install_hooks.py:301-494` |
| IR-7 refusal | `IR7_REFUSE` | `False` (BUILT-OFF: refusal branch never runs) | boolean constant | would refuse a launch when the L2 hook is not owned | `orca_worktree.py:822, 1757-1758`; pinned `tests/skills/test_issue_l2_install.py:639` |
| L2 protected refs | `L2_PROTECTED` | `refs/heads/main`, `refs/heads/master` | fixed | refused for governed and unknown actors (exit 1) | `HK/launch-level-pre-push.sh:17` |

### 9.3 Environment Variables, Paths and Kill Switch

| Variable or path | Where read | Default | Valid values | Purpose | Evidence |
|---|---|---|---|---|---|
| `HOME` | watcher default `state_dir`; guard (the only env var it reads); identity; claim | none (no `HOME`: "state_dir has no default") | absolute path | locates `~/.claude/state/launch-level/` and `~/.config/` | `P/cycle.py:187-192`; `HK/launch-level-guard.sh:23` |
| `XDG_STATE_HOME` | `_default_state_dir` | unset, then `~/.local/state` | absolute (a relative value is `config_invalid`) | state directory root | `P/cycle.py:187-192, 261-268` |
| `CLAUDE_CONFIG_DIR` | IR-4 preflight | unset | unset or resolving to `$HOME/.claude` | claim refuses a launch otherwise (`W-ENFORCEMENT-ABSENT`) | `orca_worktree.py:989-997` |
| `SC_ORCA_TIMEOUT` | `_timeout` | `DEFAULT_TIMEOUT=120` s (preflight 30, terminal read 15) | number of seconds | per-command Orca timeout override | `orca_worktree.py:88-91, 120` |
| `SC_ORCA_SHIM_INTERVAL` | shim check | 2.0 s (`SHIM_TRIES = 5`) | number of seconds | wait between shim reads | `orca_worktree.py:798-800` |
| `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` | `clickup_claim.py` | none; missing gives `skipped` (`no_token`, `no_workspace`) | strings | ClickUp auth (token only in the `Authorization` header) | `clickup_claim.py:109, 166, 169` |
| `CLICKUP_LIST_IDS`, `CLICKUP_MAX_PAGES` | `clickup_claim.py` | none; `20` (`DEFAULT_MAX_PAGES`); invalid values fall back to 20 | list ids; positive integer | narrows search; page cap | `clickup_claim.py:74, 88-94` |
| `CCSESSION_PERMISSIONS=default` | ccsession wrapper | unset (permission bypass applies) | `default` drops the bypass | launch-line permission mode (issue 390) | `tests/unit/test_ccsession_tag.py:1519-1684` |
| `CCSESSION_ORIGIN`, `CCSESSION_NAME`, `CCSESSION_ASK_TIMEOUT` | `ccsession-orca` | set or unset by the shim, not by the operator | `human`, `agent` | shim naming; carries no launch level | `skills/ccsession-tag/ccsession-orca:198-256, 249` |
| `AWR_ROOT` | `agent-work-report` | unset | path | only a workaround when `orchestrator_repo` is absent from the shared config | `skills/agent-work-report/scripts/common.py:22-40` |
| `<state_dir>/DISABLED` | cycle start and again before the launch | absent | any file, symlink or dangling symlink (`os.path.lexists`) | kill switch (`disabled`, `disabled_mid_cycle`, exit 0) | `P/record.py:421-423`; `P/cycle.py:712-713, 1063-1064` |
| `~/.claude/state/launch-level/{pending,sessions,requests,jobs}` | claim, guard, identity | absent until first launch; never pruned (owner decision O-15) | modes 0700 dirs, 0600/0400 files | launch-level stores (Section 8.3) | `orca_worktree.py:791`; guard `:20-23`; identity `:102-130`; `docs/designs/sc-issue-launch-level-hook.md:627` |
| `<git-common-dir>/hooks/pre-push`, `pre-push.launch-level` | `install_l2` | absent | see Section 8.3 | L2 hook and its pinned `HOME` and `uv` directory | `orca_worktree.py:1079, 1386-1442` |
| `.dev/issues/<N>/` | claim | absent | markdown and JSON artefacts; never staged or committed | claim output folder | `issue.md:80, 100` |
| Scheduler for `once` | not found in snapshot | none | n/a | runbook text names `0 */5 * * * *`; no timer, cron, systemd or workflow file exists (NOT BUILT) | `docs/designs/issue-watcher-setup.md:288`; research 03 section F.2 |

### 9.4 What Is NOT Configurable

| Fixed behaviour | Evidence |
|---|---|
| Every numeric limit of the cycle (candidates, day cap, timeouts, deadline, warn and health ages) is a module constant: "module constants, not operator knobs" | `P/cycle.py:33-47` |
| Repository is the literal `IronbellyOrg/IronClaude`; origin must equal `ironbellyorg/ironclaude` (lower-cased) | `P/github.py:37`; `P/launch.py:50` |
| Orca agent `claude`; surface `terminal`; no permission flag, no model flag; 12-element argv | `P/launch.py:26-28, 95-116` |
| Launch prompt and pipeline level `none` | `P/launch.py:33, 84-92` |
| Retry counts: `MAX_ATTEMPTS = 3`, backoff 10 min, lease 60 min, 24 h day-cap window | `P/record.py:434-443` |
| Launch-level words (`worktree`, `full`, `full-submit`), the 23 governed tool names and the L1 level grid | `orca_worktree.py:841-867`; guard `:781-803` |
| Worker tier pins live in agent frontmatter line 6; the skill never passes `model` | `SK/SKILL.md:54-64`; `src/superclaude/agents/issue-worker-t*.md:6` |
| `--retry-launch` is never run by code; a cron entry is never installed by code | `P/cycle.py:1308-1312`; `docs/designs/issue-watcher-setup.md:288` |

---

## 10. Error Handling & Edge Cases

### 10.1 Exit-Code Tables

**`issue-watch once` (resolved by `resolve_exit`).** The code of a reason is `audit.REASON_TABLE[reason][1]` (`P/cycle.py:480-482`). Precedence when several conditions exist: 2, 6, 7, 5, 3, 4 (`_PRECEDENCE`, `P/cycle.py:462`); 75 only when it is the sole non-zero condition; otherwise 0 (`P/cycle.py:466-477`). Exit-code constants in the CLI: `_EXIT_UNHEALTHY = 1`, `_EXIT_CRASH = 1`, `_EXIT_CONFIG = 2`, `_EXIT_STORE = 6`, `_EXIT_LOCK_HELD = 75` (`P/cli.py:34-38`); codes 3, 4, 5, 7 come only from the cycle.

| Exit | Condition | Reasons | Evidence |
|---|---|---|---|
| 0 | cycle finished or deliberate no-op | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled`, every skip reason, `attempts_exhausted`, `launched`, `claimed`, `pending_orphan`, `claim_not_observed` | `P/audit.py:26-102` |
| 1 | `once`: an unexpected `Exception` out of the cycle (stderr line carries the class name only); `status`: unhealthy | `cycle_crashed` (written to stderr only) | `P/cli.py:123-129, 164-182`; `P/audit.py:57` |
| 2 | config or environment | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch`; also `reset_refused` | `P/cycle.py:195-377, 722, 769, 1052` |
| 3 | GitHub read failure | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` | `P/github.py:489-496`; `P/cycle.py:764-765, 842-843` |
| 4 | incomplete discovery | `truncated` (100 or more results), `discovery_duplicate` | `P/github.py:823-830` |
| 5 | rate limit | `rate_limited` (header wait 1..3600 s), `rate_limit_clamped` (3600 s) | `P/github.py:418-431`; `P/cycle.py:663-668, 748-750` |
| 6 | state store | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` | `P/record.py:347-401`; `P/cycle.py:605, 1125-1126` |
| 7 | launch-step failure | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` | `P/cycle.py:1021, 1108, 1111` |
| 75 | another run holds the lock, or the lock path was replaced after `flock` | `lock_held` | `P/record.py:403-414`; `P/cycle.py:698-699` |

The doc claim that exit 7 can combine with 5 or 3 is not reachable through the cycle because a launch-step outcome halts the loop (`P/cycle.py:833-834`); only 7 with 6 is reachable [CODE-CONTRADICTED, `docs/designs/issue-watcher.md:173`]. Other verbs: `check-config` 0 or 2; `init-state` 0, 2 or 6; `reset` 0, 2, 6 or 75; `status` 0, 1, 2 or 6 (`P/cli.py:185-348`).

### 10.2 Closed Vocabularies

| Vocabulary | Members | Evidence |
|---|---|---|
| `REASON_TABLE` cycle-kind (27) | exit 2: `config_invalid, approvers_invalid, platform_unsupported, worktree_invalid, origin_mismatch, orca_not_found, account_id_mismatch`; exit 6: `store_invalid, store_missing, lock_missing, lock_invalid, state_dir_unwritable`; exit 3: `login_invalid, gh_auth_failed, gh_timeout, gh_non_json, project_read_failed`; exit 4: `truncated, discovery_duplicate`; exit 5: `rate_limited, rate_limit_clamped`; exit 75: `lock_held`; exit 1: `cycle_crashed`; exit 0: `disabled, disabled_mid_cycle, not_enabled, cycle_complete` | `P/audit.py:26-102`; pinned literally `tests/issue_watch/test_audit.py:214, 223` |
| skip-kind (17, exit 0) | `not_approved, approval_before_trigger, approval_before_init, events_incomplete, events_unreadable, edited_after_approval, project_mismatch, project_unreadable, unassigned, assigned_other, already_dispatched, in_backoff, day_cap, budget_exhausted` (never stamped in `considered`), `revalidation_failed, marker_unreadable, edits_unreadable` | research 01 section 8.2 |
| entry-kind (9) | `prompt_invalid`(7), `revalidation_transient`(7), `spawn_error`(7), `launch_unknown`(7), `attempts_exhausted`(0), `pending_orphan`(0), `claim_not_observed`(0), `launched`(0), `claimed`(0) | `P/audit.py:84-91` |
| note, warning, operator | note `re-approved`; warnings `discovery_count` (80 or more), `clock_skew` (over 60 s), `dry_run_shadow_reset`, `reset_refused`(2); `operator_reset` | `P/cycle.py:660, 731, 775, 807`; `P/cli.py:244-250` |
| Total | 27 + 17 + 9 + 1 + 4 + 1 = 59; five words never leave `run_cycle`: `config_invalid`, `platform_unsupported`, `cycle_crashed`, `reset_refused`, `operator_reset` | research 01 section 8.4-8.5 |
| `gh` reply kinds | `Reply.kind`: `timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed`; `Read.kind` adds `incomplete, budget_exhausted, truncated, discovery_duplicate`; stderr and GraphQL strings in `GH_ERROR_SIGNS` are [UNVERIFIED] | `P/github.py:267-277, 345-371, 481-496` |
| Launch outcomes | kinds `launched, unknown, spawn_error`; details `ok, spawn_error, timeout, exit_nonzero, non_json, no_operation_id, operation_id_invalid, op_unknown` (set but read nowhere); id pattern `^[A-Za-z0-9._:-]{1,128}$` | `P/launch.py:36, 56-70, 326-349` |
| Entry states | `pending, launched, unknown, failed, abandoned, claimed`; `claimed` is terminal | `P/record.py:34-36, 654-686` |
| Claim STOP codes | `E-CREATE-ONLY-FLAG, E-CLAIM-ONLY-FLAG, E-SUBMIT-NEEDS-FULL, E-NO-ORIGIN(exit 1), E-FOREIGN-REPO(3), E-NOT-AN-ISSUE(4), E-GH-AUTH, E-ORCA-REQUIRED, E-WORKER-NO-OUTPUT, E-TIER-UNAVAILABLE, E-ASSIGN-FAILED, E-POST-FAILED, E-CREATE-FAILED`; closed or assigned issue prints a no-write message | `issue.md:50-59`; `SK/SKILL.md:152-177`; `origin_repo.py:45-50` |
| Claim worktree warnings (8) | `W-ORCA-LIST-FAILED, W-ORIGIN-BASE-MISSING, W-WORKTREE-CREATE-FAILED, W-WORKTREE-AMBIGUOUS, W-WORKTREE-STALE, W-WORKTREE-COPY-FAILED, W-ORIGIN-BASE-STALE, W-FIRST-TAB-LEFT` (never STOP; status stays `success`) | `orca_worktree.py:230-239` |
| Claim launch warnings (4) and statuses | `W-LAUNCH-FAILED, W-LAUNCH-NOT-CCSESSION, W-ENFORCEMENT-ABSENT, W-L2-ABSENT`; statuses `launched, already_launched, failed`; `W-LAUNCH-NOT-CCSESSION` leaves the agent running | `orca_worktree.py:802-817, 1823-1831` |
| ClickUp results | `skipped` (`no_token`, `no_workspace`), `not_found`, `ambiguous`, `already_assigned`, `assigned`, `error` (`auth`, `rate_limited`, `page_cap`, `http_<code>`, `network`, `bad_response`, `unexpected`) | `clickup_claim.py:117-242` |
| L1 guard words (18) | `LL-IMPL, LL-COMMIT, LL-PUSH, LL-PUSH-FORM, LL-PROTECTED, LL-MERGE, LL-GH-WRITE, LL-SUBMIT, LL-REPO, LL-UNKNOWN, LL-MCP, LL-ESCAPE, LL-TURN, LL-TAMPER, LL-SKILL, LL-BIG, LL-NOBIND, LL-BROKEN`; block order BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL; ten classes block at every level including `full --submit` | `HK/launch-level-guard.sh:36-133, 783-803`; `tests/hooks/test_launch_level_guard.py:1712` |
| L2 and identity words | `L2-PROTECTED`, `L2-UNKNOWN`, `L2-MALFORMED`; identity stderr `launch job: governed Bash call cannot be wrapped safely`, `launch job: UV is required for this invocation`, `launch job: invalid invocation or unavailable private state`; `identify` statuses `ordinary` (with optional `released`), `governed`, `unknown` (reasons `stale, orphaned, foreign, unreadable`) | `HK/launch-level-pre-push.sh:187-208`; `HK/launch-job-identity.sh:215-260, 500-580` |

Level grid (`worktree` W, W approved, `full` F, `full --submit` FS): IMPL and TURN blocked at W only; COMMIT, PUSH, SUBMIT, SKILL blocked at W, WA and F and allowed at FS (`HK/launch-level-guard.sh:785-803`). Approval at W is a typed first prompt line matching `^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)`; a first line `/sc:task` is not accepted although `templates/launch-prompt.md:23` names it [CODE-CONTRADICTED].

### 10.3 Recovery and Fail-Safe Behaviour

| Mechanism | Behaviour | Evidence |
|---|---|---|
| Write-ahead `pending` | `mark_pending` then `_save()` (atomic temp file, fsync, `os.replace`, chmod 0600, directory fsync) before `orca agent launch`; if the save crosses the 120 s cut-off the previous document is restored | `P/cycle.py:1091-1098`; `P/record.py:370-378` |
| Crash points C1-C5 | C1 before the pending save: store untouched. C2 during the atomic replace: old file kept. C3 after the pending save: swept as `pending_orphan`, never launched. C4 after the spawn: swept, never launched again. C5 after the outcome save: only audit lines are lost. Across 6 runs the launcher is called at most once | `tests/issue_watch/test_crash_injection.py:1-11` |
| Sweep | `pending` found at cycle start gives `abandoned` / `pending_orphan`; `launched` past its 60 min lease gives `abandoned` / `claim_not_observed`; a later marker hit moves an entry with `pending_at` to `claimed` | `P/record.py:627-651`; `P/cycle.py:922-931` |
| At-most-once | `pending`, `launched`, `unknown`, `abandoned`, `claimed` are never relaunched; only `reset N --forfeit-guarantee` removes `abandoned` or `unknown` (the day-cap count is kept) | `P/record.py:706-720` |
| Stuck entries | `unknown` and `abandoned` with `pending_at` cost at least one G4 call per cycle while the issue stays discovered; whether that is acceptable is an open question (see Section 14) | `P/cycle.py:922-931` |
| Lock and `flock` | non-blocking `LOCK_EX\|LOCK_NB` on a pre-created 0600 `lock` file (`O_NOFOLLOW`, euid-owned, regular); inode re-checked after locking; held or replaced gives exit 75 with no rotation; missing or unsafe gives exit 6 | `P/record.py:380-419`; `tests/issue_watch/test_concurrency.py` |
| Kill switches | `enabled` false (exit 0, no lock, no call); `DISABLED` file checked inside the lock and again before the launch; neither stamps the health marker, so `status` reports unhealthy while disabled | `P/cycle.py:685-686, 712-713, 1063-1064, 1138-1139` |
| Rate limit | G1 with a usable header: wait 1..3600 s stored in `next_permitted_at`; no header (G2 and every per-issue read): clamp `now + 3600 s`; next cycles stop `rate_limited` while `now < next_permitted_at`; a dry-run never persists it | `P/github.py:418-431`; `P/cycle.py:663-668, 748-750` |
| Budget and deadline | a refused call is `budget_exhausted` (skip, not stamped, no exit); G1 or G2 starved by the deadline is `gh_timeout` (exit 3) | `P/github.py:557-589`; `P/cycle.py:418-431` |
| Dry-run isolation | all reads run; no `dispatch.json` write; no probe, re-read or launch; shadow file `dry-run.json`; a bad shadow is reset with a warning | `P/cycle.py:1029-1035, 1146-1162`; `P/record.py:831-865` |
| Audit output | decision lines then one cycle line, atomic one-`os.write` append; on `OSError` or `state_dir_unwritable` only a five-key stderr JSON line; config or platform failures before the cycle are stderr only | `P/audit.py:130-139, 381-404`; `P/cycle.py:1176-1211`; `P/cli.py:77-91` |
| Malformed or hostile replies | every typed read returns a `Read` and never raises; a wrong assumed shape reads as `non_json`, `failed` or `no_operation_id`, which fail closed (skip, or `unknown`); an unreadable launch reply is never retried | `P/github.py:467-477`; `P/launch.py:326-349` |
| Guard fail-closed versus fail-open | governed session: `LL-BROKEN`/`LL-NOBIND` (exit 2) on jq failure with a bound id, input error, unknown event, trap on non-zero exit, wrap failure; ordinary session, missing or invalid session id on a tool event, empty store, subagent prompts: exit 0 | `HK/launch-level-guard.sh:147-163, 168-173, 208-238, 386-392` |
| Claim refusals | `already_launched` without an Orca call; stale launch prompt, IR-4 failure or unwritable record: `failed` with no agent; failed launch removes the pending record; recorded-write failure adds "do not re-run the claim" text | `orca_worktree.py:1704-1775, 1815-1821` |
| Re-run idempotence | marked comments (`<!-- sc:issue:claim -->`, `<!-- sc:issue:accuracy-check -->`) are edited, not duplicated; a failed post stops with `E-POST-FAILED` and files stay | `SK/refs/claim.md:88-93` |

### 10.4 Guard Exit Codes

| Hook | Exit codes | Rule | Evidence |
|---|---|---|---|
| L1 guard (`launch-level-guard.sh`) | 0 allow, 2 block with message on stderr; never 1 and no `onFailure`; the EXIT trap maps any other status to 0 (ordinary) or 2 (governed) | Claude Code blocks only on exit 2 | `HK/launch-level-guard.sh:4-6, 135-163` |
| Job identity (`launch-job-identity.sh`) | 0 or 2 only | exit 2 for any wrap failure on a bound session, missing `uv` with a verified binding, or invalid invocation | `HK/launch-job-identity.sh:435-502, 575-580` |
| L2 pre-push (`launch-level-pre-push.sh`) | 0 allow; 1 refuse (`L2-PROTECTED`, `L2-UNKNOWN`); 2 refuse malformed stream (`L2-MALFORMED`) | the only hook in the stack that exits 1 (git's refuse code); pushes to non-protected refs are allowed for every actor | `HK/launch-level-pre-push.sh:9-10, 187-208` |
| Claim scripts | `orca_worktree.py` 0 (one JSON object) or 2 (argparse); `origin_repo.py` 0, 1, 2, 3, 4; `clickup_claim.py` 0 or 2 | runtime outcomes ride in JSON, not exit codes | `orca_worktree.py:11-12`; `origin_repo.py:45-50`; `clickup_claim.py:245-259` |

---

## 11. Performance Characteristics

No measured latency exists in the snapshot (no benchmark, no recorded timing); the section lists the budgets, deadlines and caps the code enforces. The one timing statement in the docs, "L2 costs about 100 ms per push" (`docs/designs/sc-issue-launch-level-hook.md:617-623`), was not re-run and no test asserts a time [UNVERIFIED].

### 11.1 Budgets, Deadlines and Caps

| Name | Value | Where | Effect |
|---|---|---|---|
| `gh` calls per cycle | 35 per-issue calls (`CALL_CAP`), the last 3 (`RESERVED_CALLS`) usable only by G7, G3', G6'; G1 and G2 counted apart; ceiling 37, idle cycle 2 (plus one `git` origin call) | `P/github.py:46, 49, 448-463`; `P/cycle.py:580-585` | non-reserved reads stop at 32; a refused call is a `budget_exhausted` skip |
| `PAGE_SIZE`, `PAGE_CAP` | 100 per page, 5 pages per paged read | `P/github.py:40, 43` | a fifth full page returns `incomplete` |
| `MAX_CANDIDATES` | 10 | `P/cycle.py:34, 736` | at most 10 issues examined per cycle; with one page per read about 8 can run the whole chain (design `k = min(10, 8)`) |
| `MAX_LAUNCHES_PER_CYCLE` | 1; defined but never read (dead constant); the limit works through `_Cand.launching` and `halt` | `P/cycle.py:35, 833-834` | see Section 14 |
| `DAY_CAP` | 6 launches in a rolling 24 h (`DAY_CAP_WINDOW`) | `P/cycle.py:36, 867-876`; `P/record.py:443` | `day_cap` skip, tested twice (examine and launch step) |
| `DISCOVERY_BOUND`, `DISCOVERY_WARN` | 100, 80 | `P/github.py:486`; `P/cycle.py:47, 806` | 100 or more results: `truncated`, exit 4; 80 or more: warning `discovery_count` |
| `GH_TIMEOUT_S` | 20.0 s per `gh` call | `P/cycle.py:37, 578, 582` | timeout reply kind `timeout` |
| `PROBE_TIMEOUT_S` | 10.0 s per Orca probe | `P/cycle.py:38, 1036, 1044` | no time: `budget_exhausted` skip |
| `GIT_TIMEOUT_S` | 10.0 s | `P/cycle.py:39, 716, 1071` | no time at start: `gh_timeout`, exit 3 |
| `LAUNCH_TIMEOUT_S` | 120.0 s | `P/cycle.py:40, 1099` | timeout gives `unknown` / `timeout` |
| `DEADLINE_TOTAL_S` | 240.0 s per cycle | `P/cycle.py:41, 405` | cycle budget (sized for a 5 minute cadence) |
| `GH_FLOOR_S` | 5.0 s | `P/cycle.py:42, 425` | fewer than 5 s left: no call starts |
| `LAUNCH_CUTOFF_S` | 120.0 s elapsed | `P/cycle.py:43, 431, 1069-1079, 1095-1098` | checked before and after the git call and after the pending save; past it: `budget_exhausted`, no launch |
| `SKEW_WARN_S` | 60 s | `P/cycle.py:44, 774` | warning line `clock_skew`; `clock_skew_s` is written on every cycle line whose `Date` header parsed |
| `SKEW_TOLERANCE_S` | 300 s (claim-marker window, not the warning) | `P/predicates.py:17, 295` | marker counts if at or after `pending_at` minus 300 s. The design row "skew tolerance 300 s" (`docs/designs/issue-watcher.md:827`) names this value [CODE-VERIFIED; the label is ambiguous, the number is right] |
| `HEALTH_AGE_S` | 900 s | `P/cycle.py:45, 1327` | `status` healthy only if the last stop-free exit-0 cycle is at most 900 s old (status report only) |
| `STALE_AGE_S` | 86400 s | `P/cycle.py:46, 1259` | `unknown`, or `abandoned`/`pending_orphan`, older than 24 h is listed as stale (status report only) |
| `RATE_LIMIT_MAX_WAIT_S` | 3600 s | `P/github.py:376`; `P/cycle.py:488` | longest header wait and the clamp |
| `MAX_ATTEMPTS`, `BACKOFF`, `LEASE` | 3, 10 min, 60 min | `P/record.py:434-440` | third pre-launch failure abandons; failed entries wait 10 min; a launched entry needs a marker within 60 min |
| Audit rotation | 5 MiB (`ROTATE_BYTES`), 4 rotated files (`_ROTATIONS`) | `P/audit.py:106-107, 141-156` | rotation only with the lock held; the previous `.4` is overwritten |
| stderr cap | 500 bytes (`STDERR_CAP_BYTES`), cut on a character boundary; stdout not capped | `P/runner.py:15, 57-64` | bounded memory and no text leakage |
| Approvers file size cap | 1 MiB (`_APPROVERS_MAX_BYTES`) | `P/cycle.py:75, 341-349` | larger file: `approvers_invalid` |
| Claim command timeouts | `DEFAULT_TIMEOUT` 120 s, `PREFLIGHT_TIMEOUT` 30 s, `TERMINAL_READ_TIMEOUT` 15 s (override `SC_ORCA_TIMEOUT`); shim check 5 tries x 2.0 s; L2 self-test 30 s | `orca_worktree.py:88-91, 798-800, 1078, 1178` | `run()` never raises; a timeout is a failed result |
| ClickUp caps | `CLICKUP_MAX_PAGES` 20; one retry of a 429 after `Retry-After` | `clickup_claim.py:74, 88-94, 119-123` | page cap gives `page_cap` and never assigns |
| Worker caps | one retry of an empty worker file; one T1 to T2 fallback; T2 and T3 none | `SK/SKILL.md:64-66` | `E-WORKER-NO-OUTPUT`, `E-TIER-UNAVAILABLE` |
| Hook limits | guard and identity hook timeout 5 s; L2 identity lookup `timeout 10`; guard `LL-BIG` above 65536 bytes; G2 rule 2 at most 8192 bytes and 64 arguments; identity stdin at most 1 MiB, command at most 32768 bytes | `hooks.json:68, 121, 131`; `HK/launch-level-guard.sh:419-420, 506-512`; `HK/launch-job-identity.sh:197, 433-435`; `HK/launch-level-pre-push.sh:65` | a killed hook allows the call (design V8/R2, not testable here) |

### 11.2 Performance-Critical Code

| Area | Optimization | Why it matters | Location |
|---|---|---|---|
| GitHub reads | projections (`--jq`) keep bodies out; a marker body is reduced to a boolean | bounded output and no text leakage | `P/github.py:54-67` |
| Idle cycle | exits after G1 and G2 when no trigger issue exists | 2 calls per idle cycle (`tests/issue_watch/test_cli_e2e.py:299`) | `P/cycle.py:794-808` |
| Guard empty-store fast exit | no `sessions/` directory and no `[sc-launch:` in the input: exit 0 before any parse | ordinary sessions pay almost nothing per hook event | `HK/launch-level-guard.sh:168-173` |
| Identity prologue | hook mode with no `~/.claude/state/launch-level` exits 0 before starting `uv` | ordinary sessions never need `uv` | `HK/launch-job-identity.sh:20-24` |
| L2 hook | ordinary actor exits 0 without reading stdin | most pushes cost one identity lookup only | `HK/launch-level-pre-push.sh:188` |

---

## Appendix A: Test-Pin Matrix

Counts: Lines = `wc -l`; Tests = count of `def test_` (the strict count is given where the plain `grep -c` differs); a parametrized function counts once, so collected cases are higher. No test was executed in this research: "pins" means what the test asserts when read, not a pass result. All tests below use fakes, stubs or temporary homes; none calls the real GitHub (`gh`) or Orca, and the pre-push and L2-install tests run real `git` against temporary local repositories and a local bare remote, so they prove self-consistency with assumed reply shapes, not agreement with the live tools.

### A.1 `tests/issue_watch/` (watcher)

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/issue_watch/conftest.py` | 1155 | 0 (fixtures) | test support | `FakeClock`, `FakeRunner`, `CrashingStore` (`CRASH_POINTS = (None,"C1","C3","C4","C5")`), `FailingStore`, `FakeLauncher`, `GhWorld`; `make_config` builds an ENABLED config (`:352`) so the `enabled:false` path is pinned only by `test_cycle.py:1607, 1623` |
| `tests/issue_watch/test_cycle.py` | 4982 | 237 | decision engine | `load_config` rules and defaults, `validate_approvers`, `resolve_exit` over every pair and subset, `Deadline` constants 240/5/120, idle cycle = 2 `gh` calls, `not_enabled` and `DISABLED` = 0 calls, S1 halt (one launch step per cycle), durable `pending`, 32+3 budget, 50-cycle at-most-once, dry-run isolation; no test references `MAX_LAUNCHES_PER_CYCLE` |
| `tests/issue_watch/test_github.py` | 2161 | 141 | watcher I/O | the seven argv written out literally, `--method GET` on REST and none on GraphQL, no mutation or upstream repo in any argv, `classify` rows, rate-limit wait and clamp, `CallBudget` 32/35, paging 99/100/101 and page cap 5, discovery bound 100, hostile values never reach an argv; pins the 19 fixtures are labelled and each is read (`:575-597`) |
| `tests/issue_watch/test_record.py` | 2377 | 147 | dispatch record | store schema (7 keys, 17-field entries), `store_invalid` cases, save is sorted/ASCII/0600/fsync, lock cases, DISABLED, T-1..T-13 one case each and every other pair raises `TransitionError`, half-open windows, day cap, `init_state` modes, dry-run shadow; key lists are literal, not read from the module |
| `tests/issue_watch/test_cli.py` | 1672 | 60 | operator surface | exactly five verbs, shared `--config`, `check-config`, `once` exit code = cycle code, crash gives exit 1 with class name only, `status` JSON fields and exit follows age, `init-state`, every `reset` rule (usage errors before config, refusals, day-cap kept, exit 75 and 6) |
| `tests/issue_watch/test_security_invariants.py` | 1013 | 16 | prompt and argv safety | only `/sc:issue --claim <n> --pipeline none` reaches `--prompt` (2000 seeded draws, 31 attack strings); every argv is an allowed form; GraphQL constants read-only; launch argv is exactly 12 elements |
| `tests/issue_watch/test_no_text.py` | 971 | 22 | no GitHub text stored | a canary title/label/login never reaches state files, argv, prompt or output; audit keys are a closed set; 500-byte stderr cap; crash line names the class only |
| `tests/issue_watch/test_launch.py` | 952 | 66 | launch and origin | `build_claim_prompt` int 1..999999999; `launch_argv` literal 12 elements; agent `claude`; `retry_argv`; Orca probe order and relative-path skip; origin parse tables and `check_origin`; outcome table (op-unknown wins over a valid reply); only the launch passes `cwd` |
| `tests/issue_watch/test_audit.py` | 849 | 46 | audit log | the 59 reason names and every `(kind, exit)` pair pinned literally; `line()` rejections; one-`os.write` append, 0600; rotation at 5 MiB keeping four files; exit-75 path never rotates; stderr fallback has five keys |
| `tests/issue_watch/test_predicates.py` | 732 | 44 | pure predicates | `approval_of` rows, `unchanged_since`, `is_intended_owner`, `project_check`, `marker_in_window` (skew floor, `pending_at` wins), `eligibility_order`, `parse_utc`, `valid_operation_id`; every predicate reason is in the audit table |
| `tests/issue_watch/test_cli_e2e.py` | 443 | 4 | end to end (PATH stubs) | real process: idle cycle = exactly 2 `gh` calls and stdout `cycle: cycle_complete`/`exit: 0`; one launch through `orca-ide` with the literal argv; `pending` already on disk at launch time; a second `once` launches nothing |
| `tests/issue_watch/test_slo_helper.py` | 421 | 14 | SLO reducer | `slo_numbers`: nearest-rank p95, 7-day exit-0 share excluding `disabled`, `not_enabled` and dry-run, claimed-within-lease share, stale count; the reducer has no production caller |
| `tests/issue_watch/test_module_boundaries.py` | 413 | 13 | architecture | exactly nine modules, per-module import allow-list, `fcntl` and `swarm.atomic` imported inside functions, exactly four Protocol classes |
| `tests/issue_watch/test_crash_injection.py` | 373 | 6 | crash safety | crash at C1-C5 then five more cycles: launcher called at most once, a recorded call leaves `launches` 1 |
| `tests/issue_watch/test_find_orca_parity.py` | 288 | 10 | Orca discovery | `launch.find_orca` equals `install_user_setup._find_orca` on the same probe replies; rejects where the original raises |
| `tests/issue_watch/test_concurrency.py` | 275 | 6 | locking | two real processes on one store give one launch and one `lock_held`; symlinked, directory or missing lock gives exit 6; replaced-after-`flock` gives exit 75 |
| `tests/issue_watch/test_no_shell.py` | 266 | 9 | no shell | AST scan: no `shell=` other than False, no `os.system`/`os.popen`, `import subprocess` only in `runner.py` |
| `tests/issue_watch/test_runner.py` | 226 | 16 | subprocess runner | `TypeError` for non-list argv, `shell=False`, `cwd` only when given, stderr cut to 500 bytes on a character boundary, timeout and spawn error shapes |
| `tests/issue_watch/test_origin_parity.py` | 179 | 7 | origin parsing | `launch.parse_origin` equals `origin_repo.parse_origin_url`; only `check_origin` compares lower-cased with `ironbellyorg/ironclaude` |
| `tests/issue_watch/test_marker_contract.py` | 53 | 3 | claim marker | `CLAIM_MARKER` literal present in both `src/` copies (`refs/claim.md`, `templates/claim-comment.md`), the template's last non-blank line is the marker, `MARKER_JQ` embeds it |
| `tests/issue_watch/fixtures/_assumed_shape/` | 19 files, 12,059 bytes | n/a | reply fixtures | all 19 carry `_assumed_shape: true`; all reply shapes are still assumed and no live-test record exists; count and "every file is read by a test" pinned by `test_github.py:575-597` |

### A.2 `tests/hooks/` (guard stack)

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/hooks/test_launch_level_guard.py` | 4631 | 162 (163 by plain grep: the extra hit is a string literal at `:4615`) | L1 guard | real script run with JSON on stdin; binding B1-B13 and single-use nonce; the hand-written level grid (`test_grid_policy`); IMPL spellings and look-alikes stay NONE; the 18 words (`:1712`); typed approval writes `.ok` only at `worktree` and plain `approved` releases nothing; precedence; `LL-BIG` above 65536 bytes |
| `tests/hooks/test_launch_level_guard_l2_tokens.py` | 160 | 7 | L1 tamper tokens | hook-file edits and `.git/hooks`, `--no-verify`, `hookspath`, `hook.pre-push` are TAMPER; guard and plugin copy byte-identical |
| `tests/hooks/test_launch_level_guard_registration.py` | 127 | 7 | hook registration | guard registered once per event with timeout 5, no `onFailure`, matcher equals the design string, identity hook stays last, both `hooks.json` trees agree |
| `tests/hooks/test_launch_level_guard_with_identity.py` | 212 | 5 | guard plus identity | `full --submit` allowed and identity replaces only the command; guard sees the original command; a `degraded` record blocks all Bash through identity |
| `tests/hooks/test_launch_level_guard_worker.py` | 300 | 11 | G2 rule 2 | a marker prompt binds a worker; `orchestration send`/`ask` allowed only without `--to`; other workers, groups and orca verbs blocked; forged release is TAMPER; a test caller of `orca_worktree.py pending` (`:287`; the other is `tests/skills/test_issue_orca_worktree.py:2472-2498`) |
| `tests/hooks/test_launch_job_identity.py` | 1530 | 56 | job identity | prepare/run/identify on real Linux sessions, refusals, stale/orphaned/foreign records, hook command replacement, missing `uv`/`jq` fallbacks, `setsid` escape unselected |
| `tests/hooks/test_launch_level_pre_push.py` | 1194 | 34 | L2 pre-push | matrix T-01..T-24 with real git and a bare remote (create/update/delete/force/mixed/linked worktree), invalid data file, hook sha256 pin, `install_l2` placement, bypass FR-101 |
| `tests/hooks/test_launch_level_pre_push_records.py` | 230 | 8 | L2 record parsing | actor mapping, malformed record, ordinary never reads stdin, no file written |
| `tests/hooks/test_launch_level_observations.py` | 84 | 6 (5 run) | live observations | nine synthetic fixtures and log-only probe; `test_pending_live_observation` (12 cases OB-H1..3, OB-CTX) skips unconditionally: the live observations were never run |
| `tests/hooks/test_require_orca_worktree_agent_governed.py` (added: claim-side pin of the governed branch) | 56 | 1 | worktree-agent hook | a bare worktree create is blocked in a governed session |
| `tests/hooks/test_freshness_subagent_start_policy.py` (added: second registration pin) | 115 | 5 | hook registration | the `Bash` PreToolUse set is exactly `block-bare-python.sh`, `require-orca-worktree-agent.sh`, `launch-job-identity.sh` |

### A.3 `tests/skills/` (claim)

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/skills/test_issue_protocol.py` | 1055 | 62 | claim protocol text | two-way file inventory, Wave ordering (preflight Wave 0, worktree after posts), four launch-prompt blocks, every worktree warning code has a remedy, `none` creates no worktree, ten return fields, default-level text (`:774, :791`), fork safety (`--repo` on every `gh` mention), one allowed `orgs/` read, coordinator paragraph identical in three files |
| `tests/skills/test_issue_orca_worktree.py` | 2501 | 109 | `orca_worktree.py` | fake `orca` on PATH: preflight, lookup keys, exact create argv and no forbidden flag, copy rules, first-tab close, prompt rendering, exact launch argv (LA1), record privacy, shim detection, IR-4 refusal, IR-7 warns and launches, `pending` verb (`:2472-2498`) |
| `tests/skills/test_issue_l2_install.py` | 716 | 26 | L2 install | `install_l2`/`l2_status` on real git: fresh and repeat install, forged entry never owned, `core.hooksPath` unsupported, self-test failure links nothing, `IR7_REFUSE is False` (`:639`) |
| `tests/skills/test_issue_repo_resolution.py` | 291 | 18 | `origin_repo.py` | origin forms, `E-NO-ORIGIN` exit 1, foreign URL exit 3, `/pull/` URL exit 4, only `origin` read, stdlib only |
| `tests/skills/test_issue_worker_agents.py` | 559 | 24 | worker agents | `model:` pins `claude-gw-tier2b` (t3), `claude-gw-tier2` (t2), `claude-gw-tier1b` (t1), t3 `effort: low`, tools exactly `Read, Grep, Glob, Write, Bash`, read-only GitHub rule |
| `tests/skills/test_issue_t1_fallback.py` | 69 | 8 | tier fallback | T1 to T2 fallback text, STOP when not served, no alias fallback, none for T3 or T2 |
| `tests/skills/test_worker_contract.py` | 3220 | 59 | coordinator text | WC-2..WC-16 required text, never-as-worker list (includes `/sc:issue`), write-verb audit that classifies the issue skill and agents, the surviving no-`--to` bullet (`:3216-3220`); no WC-17 or issue-pipeline pin; the doc figure "739 tests" is [UNVERIFIED] |
| `tests/skills/test_clickup_claim.py` (added: pins the only ClickUp write) | 569 | 29 (41 collected cases) | `clickup_claim.py` | fake server accepts only `GET /user`, `GET /team/<ws>/task`, `PUT /task/<id>`; one PUT with `{"assignees":{"add":[4242]}}`; ambiguous, already-assigned and page-capped searches never write; 429 retried once; invalid `CLICKUP_MAX_PAGES` falls back to 20; token never printed |
| `tests/skills/test_model_alias_policy.py` (added: pins worker tier ids) | 249 | 11 (13 collected cases) | model alias policy | `ISSUE_WORKER_PINS` (`:29-33`) must equal each worker `model:`; `claude-gw-tier` text only in allowed paths; issue chains pass no `--models`; the other seven tests are repository-wide alias policy |

### A.4 Other Directories

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/commands/test_issue_command.py` | 212 | 15 | `/sc:issue` front | version `1.1.0`, exactly seven flags, no repo/dry-run/preview option, STOP rules, `E-SUBMIT-NEEDS-FULL`, default-level text with the watcher explicit (`:182`) |
| `tests/cli/test_issue_body_templates.py` | 97 | 5 | create-mode bodies | handoff and backlog body files ship flat with four headings; `/sc:issue` is the only issue primitive (not a claim test) |
| `tests/cli/test_install_hooks.py` | 1246 | 37 | hook installer | merge cases 1-8, force refresh, backup, launch scripts packaged, executable and mirrored, guard registers both events idempotently, upgrade lands before identity, pre-push sha256 pin |
| `tests/unit/test_install_ccsession.py` | 417 | 22 | ccsession install | symlink and env seeding, refuses an unmanaged binary or symlinked skill, older skill without `ccsession-orca` still succeeds |
| `tests/unit/test_ccsession_tag.py` | 7101 | 277 | ccsession wrapper | `CCSESSION_PERMISSIONS=default` drops the bypass (`:1519-1684`), status lines on stderr, prompt passes through unchanged; no test pins "the shim carries no launch level" |
| `tests/unit/test_ccsession_tiers.py` | 3821 | 149 | tier slots | tier model slots and defaults (incl. `tier2b`); no launch-level content |
| `tests/core/test_orca_session_launch_guidance.py` | 62 | 3 | session guidance | the "Orca session launches" paragraph names Claude (CLI), `ccsession-orca`, `worktree create --agent`, `--surface terminal`; identical in both copies |

Total: 48 rows (A.1 21, A.2 11, A.3 9, A.4 7): 44 are the files named for this appendix (the 20 watcher files plus the fixture directory, 9 hooks, 7 skills, 1 command, 2 cli, 3 unit, 1 core) and 4 are added because research shows they pin pipeline behaviour (`test_require_orca_worktree_agent_governed.py`, `test_freshness_subagent_start_policy.py`, `test_clickup_claim.py`, `test_model_alias_policy.py`). Tests that pinned the removed `issue_pipeline` package are listed in Appendix B.
