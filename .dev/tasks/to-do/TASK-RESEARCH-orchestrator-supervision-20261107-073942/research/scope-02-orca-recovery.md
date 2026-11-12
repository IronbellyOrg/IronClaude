# Scope 02: Orca state, crash-recovery and ccsession
**Scope:** data sources a `/sc:sweep` can read (Orca worker-list, sc-crash-recovery, ccsession --list, return-contract, fixtures)
**Status:** Complete
**Date:** 2026-11-07
---

Tag legend: **CODE-VERIFIED** = confirmed in source, live `--help` output or a captured JSON payload; **CODE-CONTRADICTED** = source or payload shows something else; **UNVERIFIED** = only a doc says so.

Live help was read from the installed binary `orca` -> `/opt/Orca/resources/bin/orca-ide`, version 1.4.245-aidev02.780594c521aa. The inventory doc was written against 1.4.237. Only `--help` commands were run, and no command that changes state. `orca skills get` was not run because the brief allows help commands only. [CODE-VERIFIED: `orca-ide --version` prints `1.4.245-aidev02.780594c521aa`, re-verified 2026-11-07]

## Files read (path, line count)

| Path | Lines | Why |
|---|---|---|
| `.dev/orca-command-refactor/inventory/orca-capabilities.md` | 188 | Orca capability inventory (cites guide text as `[G]`, `[G:recovery]`, `[H:...]`) |
| `orca worker-list --help`, `orca worker-show --help`, `orca worker-read --help`, `orca status --help` (live, 1.4.245) | n/a | flags, paging, scope, agentWait semantics. [CODE-CONTRADICTED as command names, re-verified 2026-11-07: in 1.4.245 `worker-list`, `worker-show` and `worker-read` are subcommands of `orchestration` (`orca orchestration worker-list --help`); top-level `orca worker-list --help` prints "Unknown command: worker-list". The help line numbers cited below are from the `orchestration` forms and hold] |
| `~/.claude/skills/orchestration/SKILL.md` (symlink into `~/.agents/skills`) | 68 | Orca discovery stub; no `references/` dir exists |
| `src/superclaude/skills/sc-crash-recovery/SKILL.md` | 157 | crash-recovery orchestration |
| `src/superclaude/skills/sc-crash-recovery/refs/investigators.md` | 171 | investigator briefs |
| `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md` | 222 | pipeline status signals |
| `src/superclaude/skills/sc-crash-recovery/refs/report-template.md` | 169 | report shape |
| `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` | 170 | bootstrap JSON scan |
| `src/superclaude/skills/sc-crash-recovery/scripts/parse_session_log.py` | 128 | transcript tail parser |
| `src/superclaude/skills/ccsession-tag/ccsession` | 1975 | labelled-session store, `--list`, Orca tab map |
| `src/superclaude/core/WORKER-CONTRACT.md` | 203 | WC-4 return contract |
| `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md` | 56 | workflow package + worker contract |
| `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc16-show-4.json` | 212 | live worker-show capture (working) |
| `.../artifacts/lc17-show-1.json` | ~219 | worker-show capture (failed) |
| `.../artifacts/lc01-show-1.json` | n/a | worker-show capture (succeeded) |
| `.../artifacts/lc01-step7.txt` | n/a | worker-list + worker-release capture |

Line counts re-verified 2026-11-07 with `wc -l` [CODE-VERIFIED]: every count above holds (ccsession 1975, orchestration SKILL.md 68, lc16-show-4.json 212, lc17-show-1.json 219); the two `n/a` captures have lc01-show-1.json 219 and lc01-step7.txt 47 lines.

## Orca worker-list fields a classifier needs (field path, meaning, values, file:line)

Important caveat: no captured worker-list payload with a non-empty `workers` array exists in the repo (see "Sample JSON shapes"). The field paths below come from **worker-show** captures (`result.projection.*`). The inventory says worker-list rows carry the same `projection` (orca-capabilities.md:127, quoting `[G]` 136-142: act on "`projection.attention` categories, `projection.attention.requiresAction`, and literal `projection.nextAction` argv"). That the row shape equals the show shape is **UNVERIFIED**.

### worker-list envelope (CODE-VERIFIED, `lc01-step7.txt`; live help)

[CODE-VERIFIED for every row, re-verified 2026-11-07: lc01-step7.txt:24-46 (`workers: []` :28, `counts` :29-31, `page` :32-37, `scope` :38-41, `_meta.runtimeId` :43-45); `orchestration worker-list --help` lines 21-22 hold the quoted text]

| Field | Meaning | Values seen | Source |
|---|---|---|---|
| `ok` | call succeeded | `true` | lc01-step7.txt |
| `result.workers[]` | rows, newest first, max 100 local | `[]` in the only capture | lc01-step7.txt; `worker-list --help` line 21 |
| `result.counts` | per terminal-state count | `{released: 1}` | lc01-step7.txt |
| `result.page.{limit,total,hasMore,nextCursor}` | paging | `100, 0, false, null` | lc01-step7.txt; help line 21 "Continue with the opaque page.nextCursor value unchanged" |
| `result.scope.{run,source}` | which Run was listed and why | source `flag` / `bound` / `all` | lc01-step7.txt; help line 22 |
| `_meta.runtimeId` | Orca runtime id | string | lc01-step7.txt |

### Per-worker fields (from worker-show `result.*`, CODE-VERIFIED in captures)

[CODE-VERIFIED for every row except the parts marked UNVERIFIED, re-verified 2026-11-07 against lc16-show-4.json, lc17-show-1.json and lc01-show-1.json. Extra anchors: `dispatch.id` lc17-show-1.json:6, :158; `lastFailure` lc17-show-1.json:23; `assigneePaneKey` lc16-show-4.json:12, `tabId`/`leafId` :169-170; `succeeded`/`completed` stage values lc01-show-1.json:129-130]

| Field path | Meaning | Values seen | file:line |
|---|---|---|---|
| `dispatch.id` (`ctx_*`) | Dispatch id; the `--dispatch` argument for show/read/release | `ctx_5fac5090b848` | lc17-show-1.json (nextAction argv) |
| `dispatch.status` | Dispatch lifecycle | `dispatched`, `failed`, `completed` | lc16-show-4.json:21; lc17-show-1.json:21 |
| `dispatch.lastHeartbeatAt` | last heartbeat (ISO) | `"2026-11-05T20:50:37Z"`, `null` | lc16-show-4.json:29; lc17-show-1.json:29 |
| `dispatch.lastFailure` | JSON **string** holding `{provenance, outcome, messageId, subject, body, filesModified, reportPath, completedAt}` | worker_report provenance | lc17-show-1.json (dispatch block) |
| `dispatch.assigneePaneKey` / terminal `tabId:leafId` | pane identity, a join key to ccsession orca-tabs | string | lc16-show-4.json (dispatch/terminal blocks); join is UNVERIFIED, see Open questions |
| `projection.stage.{worker,dispatch,detail,activity}` | staged state | worker `ready`/`failed`/`succeeded`; dispatch `dispatched`/`failed`/`completed`; detail `input_accepted`/`settled`; activity `working` | lc16-show-4.json:128-133; lc17-show-1.json:128-133 (re-verified 2026-11-07) |
| `projection.outcome` | Task outcome so far | `in_progress`, `succeeded`, `failed` | lc16-show-4.json:134; lc17-show-1.json:134 |
| `projection.liveness.{verdict,reason,observedAt,source}` | fleet liveness verdict | verdict `live` only in captures (docs: `live`/`unverifiable`/`exited`); source `agent_status` | lc16-show-4.json:135-139 (re-verified 2026-11-07); orca-capabilities.md:122 |
| `projection.evidence.{durable,liveStatus,lastObservedAt}` | freshness of the status evidence | `true`, `fresh` | lc16-show-4.json:140-144 (re-verified 2026-11-07) |
| `projection.resource.{state,releaseState,terminalState}` | process/terminal accounting (separate from Task status) | state `user_owned`/`owned`; releaseState `retained`/`not_requested`; terminalState `retained`/`reclaimable`/`active` | lc16-show-4.json:145-151; lc17-show-1.json:145-150 (re-verified 2026-11-07; `resource.state` is at :146 in both) |
| `projection.nextAction.{kind,argv}` | literal next command Orca proposes | `none` + `[]`; `release` + `["orchestration","worker-release","--dispatch","ctx_..."]` | lc16-show-4.json:152-155; lc17-show-1.json:153 |
| `projection.attention.{categories,requiresAction}` | coordinator attention | categories `[]`, `["failure"]`, `["root_completion"]`; requiresAction `true`/`false` | lc16-show-4.json:156-159; lc17-show-1.json:162-165 |
| `terminal.{worktreePath,branch,title,connected,writable,lastOutputAt,preview}` | terminal facts; `preview` is screen text | strings/booleans | lc16-show-4.json:167-175 (re-verified 2026-11-07; `terminal` block :161-181) |
| `terminal.agentWait`, `observation.agentWait` | person-wait evidence (hook / prompt-text / title) | `null` in all captures | lc16-show-4.json:180,185; `worker-show --help` line 16 |
| `observation.{status,exactWorker}` | PTY liveness only | `live`, `true` | lc16-show-4.json:183-184 |
| `terminalResource.retainedReason` | why a terminal is kept | `user_takeover` | lc16-show-4.json:191 (re-verified 2026-11-07; `terminalResource` block starts :187) |

**CODE-CONTRADICTED as a work signal:** `projection.stage.activity` is `"working"` in the failed (lc17-show-1.json:132) and succeeded (lc01-show-1.json:132, re-verified 2026-11-07) captures, both settled workers idle at the prompt. A classifier must not use `activity` to mean "working"; use `outcome`, `dispatch.status`, `liveness.verdict` and `agentWait` instead.

Enum tally across all `lc*-show-*.json` captures: verdict {live}; outcome {in_progress, succeeded, failed}; terminalState {reclaimable, retained, active}; releaseState {not_requested, retained}; nextAction.kind {none, release}; attention.categories {root_completion, failure}. No capture has `unverifiable`, `exited` or a non-null `agentWait`. [CODE-VERIFIED: a grep tally over `lc*-show-*.json` re-run 2026-11-07 gives verdict live 36; outcome in_progress 14, succeeded 17, failed 5; terminalState reclaimable 20, retained 9, active 7; releaseState not_requested 54, retained 18; no non-null `agentWait`]

## Liveness, attention, stall proof and terminal-state rules (file:line, quoted short)

| Rule | Quote | Source | Tag |
|---|---|---|---|
| Three verdicts | "Preserve the verdicts `live` / `unverifiable` / `exited`; contact loss is not process death." | orca-capabilities.md:122 (`[G]` 58-60) | UNVERIFIED (guide text; only `live` seen in captures) |
| Fleet vs PTY | worker-list `projection.liveness` is the fleet verdict; worker-show `observation.status` "is PTY liveness only. A live terminal can still hold a dead or stuck agent." | orca-capabilities.md:122-123 | UNVERIFIED; field names CODE-VERIFIED in lc16-show-4.json:136,183 |
| Show outranks row | for reasons `missing_status`, `host_unavailable`, `capability_unsupported` "a `worker-show` verdict sourced from the execution host ... outranks the row. Only `host_unavailable` is contact loss" | orca-capabilities.md:124 | UNVERIFIED |
| Unverifiable = absence | "`unverifiable` is always absence — `missing_status`, `stale_status`, `restored_unconfirmed`, or a remote worker with no connection ... Absence never authorizes stop, abandon, retry, or release" | orca-capabilities.md:125 | UNVERIFIED |
| Stall proof | "positive proof the agent stopped: `exited` liveness, the worker's own observation of process exit, or a transcript whose final agent turn sent no `worker_done`." | orca-capabilities.md:126 (`[G]` 143-145); also 114 | UNVERIFIED. Gate fix B-05: "final" must be proved, not assumed. Proof is `exited` liveness, a process-exit observation, an observable end-of-turn marker in a `worker-read --source transcript` capture (none captured yet, UNVERIFIED), or Orca reporting the proof; the latest turn read without that evidence is "could not determine". A dispatch fenced by `consumer_fenced` ends without `worker_done` by design (WC-12, `WORKER-CONTRACT.md:60`) and is "fenced", never stalled (research-notes.md Section C rules 2-3) |
| Attention | act on `projection.attention` categories, `requiresAction` and literal `nextAction` argv; "A `none` `nextAction` has no argv to run: read `liveness.reason` and keep waiting" | orca-capabilities.md:127 | field shapes CODE-VERIFIED (lc17-show-1.json:153-165) |
| Person wait is healthy | "Null means Orca looked and found no wait. An absent field means it never looked ... A waiting worker is healthy, not failed." | `worker-show --help` line 16; orca-capabilities.md:129 | CODE-VERIFIED (help text) |
| Heartbeat | heartbeat "proves liveness, not completion" | orca-capabilities.md:130 | UNVERIFIED; whether heartbeat age feeds the verdict is UNVERIFIED (orca-capabilities.md open item 7) |
| Missing heartbeat is absence | coordinator "never stops, retries or releases a worker because a heartbeat is late, and it acts only on Orca's stall proofs" | WORKER-CONTRACT.md:45 (WC-10) | CODE-VERIFIED (repo contract text) |
| Terminal state is separate | `--terminal-state active|reclaimable|retained|release_pending|release_unknown|released`; "reported separately from Task status" | orca-capabilities.md:113; `worker-list --help` lines 3, 19 (re-verified 2026-11-07: the flag list is line 3, the quoted "reported separately from Task status" is line 19) | CODE-VERIFIED (help) |
| Failed start still owns terminal | worker-list "reports that row as `reclaimable`; release it there" | orca-capabilities.md:112 | UNVERIFIED |
| Never release on weak signals | never release on timeout, TUI idle, heartbeat, status, question, escalation or stale completion | orca-capabilities.md:36,111 | UNVERIFIED |
| Coordinator turn guard | do not end the coordinator turn while `worker-list --run <id> --terminal-state reclaimable --json` returns rows | orca-capabilities.md:113 | UNVERIFIED |
| Dispatch-only rows | "Context-only Dispatches created by orchestration dispatch are included as unsupervised with terminal state retained." | `worker-list --help` line 20 | CODE-VERIFIED |

Classifier mapping these rules suggest (derived, not from a source): [UNVERIFIED: a derivation from the rules above; no source states this mapping]

> **Superseded (gate fix B-01, B-02, B-26, 2026-11-07).** The five bullets below were the first draft. The canonical mapping is `research-notes.md` Section C (classes and precedence 1-7) and its safe-to-close dimension; the per-class Orca signals are in `05-orca-row-schema.md` Answer (5). Where this list and Section C disagree, Section C wins (contradiction C14 in research-notes.md). The corrections are:
> - **finished** here is only the Orca half. A worker is finished only when Orca shows `outcome` settled AND a read of its return contract shows `succeeded`, `partial` or `failed` (`WORKER-CONTRACT.md:122-129`); a guard refusal (`:127`) is the only finished row without a contract. `blocked` in the contract is "waiting on a person", not finished (WC-5).
> - **waiting on a person** has two kinds, each with a named source (Section C rule 4): (a) explicit question: a non-null `observation.agentWait` (worker-show only; `worker-show --help` line 16, help CODE-VERIFIED), or `worker_status: blocked` with `blocked_question` in the return contract (WC-4/WC-5), or a pending `ask` (named by #409, but no read path exists for it: `research-notes.md` Section B ask row, "UNKNOWN (no read path, G-B)", so the sweep cannot show it); (b) frozen or blocked by policy (derived): a Ruling halt or a frozen `/sc:implement` plan (`WORKER-CONTRACT.md:133-136`), or a ready Task this coordinator did not create (`:129`, read from `task-list --ready`, `07-gate-gap-fill.md` Section B). #409 counts only (a) as a Request (`495eb96d:.dev/design/orca-observer-20261106/data-dictionary.md:12`); (b) is the policy dimension (`:27`).
> - **stalled** needs the turn proved final (Section C rule 2; see the stall-proof note under the table above).
> - **safe to close** is not a class. It is a separate two-part dimension, both parts REVIEW only and never run: "terminal releasable" (`terminalState` `reclaimable` and `nextAction` `release`, only after the result has been read) and "worktree removable" (all five refusal conditions at `WORKER-CONTRACT.md:108` are false and no freeze applies, `:133-136`). See research-notes.md Section C.

- **working**: verdict `live`, outcome `in_progress`, agentWait null, attention empty.
- **waiting on a person**: agentWait non-null (hook/prompt-text/title), or an `ask` pending. Healthy, not stalled. [Superseded: see the note above; `ask` has no read path]
- **stalled**: only with positive stall proof (verdict `exited` without `worker_done`, or a transcript whose final turn sent no `worker_done`), and never when the transcript or `check` result shows `consumer_fenced` (that row is "fenced"; Section C rule 2, NB-1). `unverifiable` is reported as "could not determine", never "stalled".
- **finished**: outcome `succeeded`/`failed`, `stage.detail` `settled`, attention `root_completion`/`failure`. [Superseded: Orca half only; needs the contract read, see the note above]
- **safe to close**: `terminalState` `reclaimable` and `nextAction.kind` `release`. The sweep is read-only, so it only prints the `nextAction.argv` as a REVIEW action. [Superseded: a two-part REVIEW dimension, not a class, see the note above]

## Failure modes (Orca not running, paging, remote workers, stale data) and how each is reported

| Failure | What Orca returns | Source | Tag | Sweep should report |
|---|---|---|---|---|
| Orca not running | error `runtime_unavailable`, "Orca is not running. Run 'orca open' first." | orca-capabilities.md:39 (`cli-error.js:49-53`) | UNVERIFIED (exit code unknown, open item 9 at :184) | "Orca unavailable" banner; still report on-disk sources (contracts, transcripts); never run `orca open` (that changes state) |
| Access denied | `runtime_access_denied` | `~/.claude/skills/orchestration/SKILL.md:64-66` | UNVERIFIED | report as could-not-determine |
| Bare `orca` outside an Orca terminal | GNOME screen reader may run instead | orchestration SKILL.md:37-39 | UNVERIFIED | call `orca-ide` or the resolved path |
| Outside an Orca terminal | `no_active_sender_terminal` for messaging; `status.caller` omitted | orca-capabilities.md:149,151; `status --help` line 14 | help CODE-VERIFIED | sweep only reads, so pass `--run` explicitly |
| Scope without `--run` | lists the Run bound to the calling terminal, or every Run with no binding; `scope.source` says which | `worker-list --help` line 22; lc01-step7.txt | CODE-VERIFIED | print `scope.source` in the report header. Gate fix B-07: Run IDs for `--run` come from `orca-ide orchestration run-list` (plain read, paged 100 with `--cursor`) or `run-current`; ready Tasks from `task-list --ready`; open gates from `gate-list`. Handler evidence for each is in `07-gate-gap-fill.md` Section B. `inbox` is not used (read-marking UNVERIFIED) |
| Paging | max 100 local rows, newest first; `page.hasMore` + opaque `page.nextCursor`; `--limit 1-100` | `worker-list --help` lines 3, 21 | CODE-VERIFIED | loop on `nextCursor`; report row total vs `page.total`. Gate fix B-08: the row shape is UNVERIFIED (no populated capture), so the conservative default is one `worker-show` per row; worst case is ceil(N/100) list calls plus N show calls (`05-orca-row-schema.md` Answers (1) and (5)) |
| Remote workers | `--on` workers read `unverifiable` until listed with `--include-remote`; remote server chosen by `--pairing-code`/`--environment` | orca-capabilities.md:128; `worker-list --help` lines 10-11, 21 | help CODE-VERIFIED | always pass `--include-remote`; unverifiable remote rows go to "could not determine" |
| Stale data | `evidence.liveStatus` (`fresh` seen), reason `stale_status`, `observedAt` | lc16-show-4.json:140-144 (re-verified 2026-11-07); orca-capabilities.md:125 | field CODE-VERIFIED, `stale_status` UNVERIFIED | print observedAt age; never classify stale as stalled |
| Transcript source switch | `worker-read` cursor pinned to source; restart on `source_changed` | `worker-read --help` line 20 | CODE-VERIFIED | restart read without cursor |
| Executable failure | report the exact error and stop | orchestration SKILL.md:46-47 | UNVERIFIED | copy error verbatim into the report |

## sc-crash-recovery reusable pieces (what each script does, its input/output, allowed-tools, SAFE/REVIEW labels, "could not determine" section, file:line)

### Skill shape

- **allowed-tools** (SKILL.md:4): Read, Glob, Grep, `Bash(ls|find|wc|cat|head|tail|stat *)`, `Bash(git status|diff|log|stash|branch|ls-files *)`, `Bash(~/.claude/skills/sc-crash-recovery/scripts/*)`, `Bash(~/workspace/IronClaude/.claude/skills/sc-crash-recovery/scripts/*)`, Task. [CODE-VERIFIED SKILL.md:4]
  - **CODE-CONTRADICTED** "pure read-only — enforced by allowed-tools" (SKILL.md:13,155): `Bash(git stash *)` allows `git stash push/pop/drop`, which change state. A sweep should allow only `git stash list`.
  - The second script path hardcodes `~/workspace/IronClaude`. The repo is checked out under `~/workspaces/...`, so that allowance does not match here. [CODE-CONTRADICTED for this host: SKILL.md:4 allows `~/workspace/IronClaude/...`, while this checkout is `~/workspaces/worktrees/IronClaude/...`]
- **Arguments** (SKILL.md:25-27): `--all` sweeps `~/workspace/`, `--since` default 72h, optional `<project-path>`. **CODE-CONTRADICTED for this host**: projects and Orca worktrees live under `~/workspaces/` and `~/workspaces/worktrees/...`, so `find ~/workspace -maxdepth 1` (SKILL.md:53) finds none of them. A sweep should take its project list from Orca rows (`terminal.worktreePath`) instead.
- **STOP/WARN rules** (SKILL.md:31-37): STOP on an invalid path; WARN on an untouched project. [CODE-VERIFIED SKILL.md:31-37]
- **Investigators** (SKILL.md:75-81; refs/investigators.md): pipeline-artifacts (:9-41), claude-sessions (:47-70), project-memory (:76-95), git-state (:101-126, all read-only commands incl. `git stash list` at :115), auggie-semantic (:132-151). `--all` waves of 3 projects (investigators.md:171). [CODE-VERIFIED: every range above re-read 2026-11-07 and holds]
- **SAFE/REVIEW**: "Mark each as `SAFE` (idempotent, read-only or trivially reversible) or `REVIEW` (changes state, user should read first)" (SKILL.md:91); examples report-template.md:71-118. Propose, never execute (SKILL.md:93-97). [CODE-VERIFIED SKILL.md:91, :93-97; report-template.md:71-118]
- **"What I could not determine"**: tool-failure table with `unscanned: bootstrap_failed | auggie_unavailable | subagent_failure` (SKILL.md:139-148); "The synthesis report must surface every `unscanned:` marker in a 'What I could not determine' section" (SKILL.md:150); template section report-template.md:127-129. This maps directly onto the sweep's `unverifiable` / Orca-unavailable cases. [CODE-VERIFIED SKILL.md:139-148 (table :143-148), :150; report-template.md:127-129]
- **Running pipeline guard**: "Pipeline still running ... flag explicitly" (SKILL.md:137). [CODE-VERIFIED SKILL.md:137]
- **Conflicts section**: report-template.md:120-125 (do not pick a side; SKILL.md:134). [CODE-VERIFIED report-template.md:120-125; SKILL.md:134]

### scripts/bootstrap_scan.sh (170 lines)

- Input: `bootstrap_scan.sh <project-path> [--since 72h]`. Output: one JSON object on stdout. Missing path: exit 2 with an error JSON on stderr (:21-24). [CODE-VERIFIED bootstrap_scan.sh:21-24]
- Output keys (:143-169): `project, path, since_hours, session_log_dir, session_log_dir_exists, recent_sessions, has_dev, has_docs, has_memory, memory_count, git, sprints, tasks, recent_roadmap_states, recent_manifests, recent_execution_logs, recent_exit_codes, most_recent_mtimes`. [CODE-VERIFIED bootstrap_scan.sh:143-169]
- `recent_sessions` (:65-69, :136): last 3 `*.jsonl` by mtime. [CODE-VERIFIED bootstrap_scan.sh:65-69, :136]
- **Bug 1, CODE-CONTRADICTED encoding** (:31): `ENCODED_CWD="-$(echo "$ABS_PROJECT" | sed 's|^/||; s|/|-|g')"` replaces only `/`. Claude Code replaces every non-alphanumeric character with `-` (ccsession comment at :1301-1302; confirmed by this session's own log dir `-home-coder-workspaces-worktrees-IronClaude-issue-339-orchestrator-mode`). Any path with `.` or `_` gets the wrong session dir and `session_log_dir_exists: false`.
- **Bug 2, git worktrees** (:73): `if [[ -d "$ABS_PROJECT/.git" ]]`. In a git worktree `.git` is a file, so every Orca worktree reports `is_repo` false and git-state is skipped. [CODE-VERIFIED bootstrap_scan.sh:73, `{"is_repo":false}` at :82]
- JSON is built by hand with partial escaping (:136 awk), so a path with `"` or `\` gives malformed JSON (the SKILL.md:145 fallback covers it). [CODE-VERIFIED bootstrap_scan.sh:136; SKILL.md:145]
- Reuse verdict: usable for `.dev/` artifact discovery after the two bugs are fixed; not usable as-is for Orca worktrees. [CODE-VERIFIED basis bootstrap_scan.sh:31, :73; the verdict itself is a judgement]

### scripts/parse_session_log.py (128 lines)

- Input: `<session.jsonl> [--turns N=6] [--max-chars N=600]`. Missing file: `{"error":"not_found","path":...}`, exit 2. [CODE-VERIFIED parse_session_log.py:21-29; the error JSON goes to stdout]
- Skips `isMeta`, `isSidechain` and `file-history-snapshot` events; keeps user/assistant; summarises tool_use input by `file_path|command|description|prompt|query|path|url`; drops turns starting `<local-command-caveat>` or `<system-reminder>`; at most 5 tool calls per turn. [CODE-VERIFIED parse_session_log.py:45-55, :81-84, :91, :111-119; the prefix drop applies to user turns only (:81)]
- Output: `{session_file, total_events, turn_count, returned_turns, turns:[{role, ts, text, tool_calls:[{name,input_summary}]}]}`. [CODE-VERIFIED parse_session_log.py:85-102]
- Limits: reads the whole file into memory (transcripts can be several GB); ignores `custom-title` events. [CODE-VERIFIED parse_session_log.py:31-40 (whole file read), :53-55 (only user/assistant roles kept)]
- Reuse verdict: directly useful for the "final agent turn sent no `worker_done`" stall proof (look for a `worker_done` Bash call in the last assistant turn), once it tails the file instead of reading it whole. Run with `uv run python`. [UNVERIFIED: a reuse judgement; the parser does not itself look for `worker_done`] Gate fix B-05 qualification: the parser can only show the latest assistant turn; it cannot prove that turn is final (it keeps no end-of-turn or process-exit signal, parse_session_log.py:45-55, :85-102). A missing `worker_done` in that turn is stall proof only with separate final-turn proof (research-notes.md Section C rule 2); otherwise the row is "could not determine".

## ccsession --list (output format, store path, file:line)

- Store: `PROJECTS_DIR="$HOME/.claude/projects"` (:144). Labelled sessions are `~/.claude/projects/<name_key>/topics/<name>.txt`, each holding a session uuid; the name key is the origin host/path slug, else the git common dir, else the cwd (:175-222). Name encoding `%25`, `%2F`, `%2E` (:344-361). `.cwd` caches the real folder (:453, :1924-1927). [CODE-VERIFIED ccsession:144, :175-222, :344-361, :453-455, :1920-1927]
- `slugify` (:162-165) replaces only `/`, unlike Claude Code's encoding; only used for ccsession's own keys. [CODE-VERIFIED ccsession:162-165]
- Transcript lookup: `ls -t ~/.claude/projects/*/<uuid>.jsonl | head -1` (:1408-1411). Session home: reads `"cwd"` from the first 256KB and last 1MB of the transcript (:1297-1327). [CODE-VERIFIED ccsession:1408-1411, :1305-1327 (`head -c 262144`, `tail -c 1048576` at :1324)]
- **Output format** (`list_sessions`, :1482-1580): human-readable only, no JSON. Blank line, workspace name heading, then rows `  %-22s  started YYYY-MM-DD HH:MM  last [date ]HH:MM  (dur)  <uuid8>`, or `(transcript missing)` (:1525) / `(times unavailable)`. `--here` adds a "Sessions whose worktree was removed" group and "N more session(s) in other worktrees". Empty: "No labeled sessions in this workspace yet." / "No labeled sessions yet." (:1577-1579). [CODE-VERIFIED ccsession:1482-1581 (rows :1524-1548, groups :1566, :1572); `--here` calls `list_sessions "$(name_key)" worktree` at :1792-1797]
- **CODE-CONTRADICTED as read-only**: `--list` calls `ensure_names_migrated` first (:1787-1788), which runs `rename_dot_labels` (mv) and `migrate_names` (writes files) when the marker `NAMES_MIGRATED="$PROJECTS_DIR/.ccsession-names-by-repo"` (:224) is missing (:285-287). A read-only sweep should read the `topics/*.txt` files directly, not call `ccsession --list`. (re-verified 2026-11-07: ccsession:1787-1788, :224, :285-287)
- **Orca join data** (most useful piece): `ORCA_TABS_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs"` (:564). One file per `ORCA_PANE_KEY` (`:` replaced by `+`) with 3 lines: Claude session id, launch folder, `ORCA_TERMINAL_HANDLE` (:558-605). This maps an Orca pane to a Claude transcript uuid. Title marks live in `${XDG_CACHE_HOME:-~/.cache}/ccsession/orca-titles/$ORCA_TERMINAL_HANDLE` (:524). [CODE-VERIFIED ccsession:564, :566-572, :590, :524]

## Return-contract and on-disk reports (shape, where written)

### Worker contract (WC-4), CODE-VERIFIED as repo contract text

[CODE-VERIFIED for every bullet, re-verified 2026-11-07: WORKER-CONTRACT.md:14, :15, :30-38, :52-57, :58, :161 hold the described text; :161 sits in the worked example at :158-164]

- Where: `<report-dir>/return-contract.yaml`; report-dir is the command's directory-valued `--output`/`--output-dir`, or `--report-dir` (WORKER-CONTRACT.md:15, :31). The coordinator knows the path before dispatch (:31).
- Shape (:32): `worker_contract_version: "1"`, `worker_status: succeeded | partial | failed | blocked`, `command`, `report_path`, `artifacts`, `blocked_question` (when blocked), `reason` (when failed; implement also when blocked).
- Field named `worker_status` because `status` already exists in workflow/adversarial/reflect contracts (:34). Status mapping (:35).
- Written on every outcome, including early stops (:36). Missing report dir: no file, chat-only error (:37). `worker_done --report-path` carries it; "Orca does not check the file, so the coordinator opens it" (:38).
- Outcome mapping (WC-5, :58): `failed`/`blocked`/no contract → `--outcome failed`; `succeeded`/`partial` → `--outcome succeeded`. A sweep therefore must read the YAML to tell `blocked` (waiting on a person/coordinator) from `failed`; Orca shows both as outcome `failed`.
- Blocked gate (WC-2, :30; WC-3, :52-57): `blocked_question` holds the exact question. Example: `.dev/tdd/auth-1/return-contract.yaml` with `worker_status: blocked` (:161).
- Person-mode flag refusal writes `worker_status: failed` with the flag in `reason` (:14); commands: brainstorm.md:155, test.md:104, business-panel.md:100, explain.md:104, adversarial.md:160 (grep hits, not re-read). [CODE-VERIFIED, re-verified 2026-11-07: each of the five lines in `src/superclaude/commands/` reads `worker_status: failed`]

### Workflow package contract

- `.dev/tasks/to-do/<id>/return-contract.yaml`, contract 1.1: `contract_version, status: success|partial|failed, slug, plan_path, source_path, source_origin, strategy, depth, handoff_action, handoff_output_path, reflect_status, reflect_report_path, unresolved` (sc-workflow-protocol/refs/return-contract.md:3-19). May move to `done/` (:33). [CODE-VERIFIED return-contract.md:3-19, :33]
- Worker contract variant under `--unattended`: `worker_status: succeeded | partial | failed` (no `blocked`) (:45-56). [CODE-VERIFIED return-contract.md:49, :45-56]
- Other mapping tables: sc-brainstorm-protocol/SKILL.md:385, sc-graph-protocol (:112), sc-impact-protocol (:100) (grep hits). [CODE-VERIFIED, re-verified 2026-11-07: each line holds a `worker_status` mapping or field]

### Other on-disk progress signals a sweep can read (refs/pipelines.md)

[CODE-VERIFIED for every bullet, re-verified 2026-11-07: sc-crash-recovery/refs/pipelines.md:177-201, :102-116, :52-68, :19, :161-168 hold the described text]

- `TASK-WF-*` packages: `progress.md` lines `T<id>: complete verdict=…`, `FINAL:`, `ARCHIVE:`; in `to-do/` with all tasks complete = archive-blocked; `.archiving` marker = interrupted archive (pipelines.md:177-201).
- Sprint: `results/phase-N-result.json` authoritative, `execution-log.jsonl`, `.sprint-exitcode` (:102-116).
- Roadmap: `.roadmap-state.json` per-step status/attempts (:52-68).
- MDTM: frontmatter `status:` (:19, :161-168).

## Sample JSON shapes found in the repo (paths) or "none found"

Found, all in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/` (799 files):

[CODE-VERIFIED for every bullet, re-verified 2026-11-07: folder holds 799 files; lc16-show-4.json:1-212, lc17-show-1.json:21-23, :152-166, lc01-show-1.json:129-163 and lc01-step7.txt:24-46 hold the described shapes; 88 files match the lc*-worker-start.json, lc*-transcript-*.json and lc*-step7.txt patterns]

- `lc16-show-4.json`: worker-show, live working worker. Envelope `{id, ok, result:{dispatch, worker, projection, terminal, observation, terminalResource}, _meta:{runtimeId}}`.
- `lc17-show-1.json`: worker-show, failed worker with `lastFailure`, `nextAction` release, attention `failure`, `terminalState` reclaimable.
- `lc01-show-1.json`: worker-show, succeeded worker, attention `root_completion`.
- `lc01-step7.txt`: worker-list with `--terminal-state reclaimable` (empty `workers`, `counts:{released:1}`, `page`, `scope:{run, source:"flag"}`) plus a worker-release receipt `{dispatchId, state:"released", processAction:"closed_agent_terminal", archive:{source:"transcript", status:"captured"}, mutation:{requestId, replayed}}`.
- Other `lcNN-show-N.json`, `lcNN-worker-start.json`, `lcNN-transcript-N.json` (worker-read), `lcNN-step7.txt` in the same folder.

None found:

- a worker-list payload with non-empty `workers[]` rows;
- any payload with `liveness.verdict` `unverifiable` or `exited`;
- any payload with non-null `agentWait`;
- an `--include-remote` payload;
- a `runtime_unavailable` error payload.

[CODE-VERIFIED by grep of the artifacts folder 2026-11-07: every `"workers": [` array is empty; no `unverifiable` or `exited` verdict; no non-null `agentWait`; `include-remote` appears only in help and prose text (orca-help.txt, lc09-transcript-1.json:223, lc09 report and retry-prompt files), never in a payload; no `runtime_unavailable` payload]

Unrelated hits for "projection": `tests/swarm/*`, `tests/cli/eval/*`. Related prose: `.dev/issues/339/analysis/analyze-worker-contract.md`, `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/`. [UNVERIFIED: not re-checked 2026-11-07]

## Open questions

1. Does a worker-list row carry the same `projection` object as worker-show? No non-empty row capture exists. (UNVERIFIED) **Answered by `05-orca-row-schema.md` Answer (1) (gate fix B-03, B-08):** still UNVERIFIED with no populated capture; the design default is one `worker-show` per row, worst case ceil(N/100) list calls plus N show calls.
2. What do `liveness.reason` values and `exited` rows look like in 1.4.245? No capture. (UNVERIFIED) **Answered as far as evidence allows by `05-orca-row-schema.md` :125 and Gap 3 at :188 (gate fix B-03):** `liveness.reason` is absent from every captured `live` verdict and its presence on `unverifiable`/`exited` rows is UNVERIFIED; the class does not depend on it, because `unverifiable` is "could not determine" and `exited` is stall proof whatever the reason (research-notes.md Section C rules 2 and 7).
3. Exit code and JSON shape of `runtime_unavailable` (orca-capabilities.md:184). (UNVERIFIED)
4. Does heartbeat age feed the liveness verdict (orca-capabilities.md open item 7)? (UNVERIFIED)
5. Does `dispatch.assigneePaneKey` / terminal `tabId:leafId` equal ccsession's `ORCA_PANE_KEY`? The formats look alike; this would join Orca rows to transcripts via `~/.local/state/ccsession/orca-tabs`. Alternative: `worker-read --source transcript`. (UNVERIFIED) **Answered (gate fix B-09):** CODE-VERIFIED for one worker. `lc16-show-4.json` `assigneePaneKey` with `:` replaced by `+` is the orca-tabs file name, and that file's line 3 equals `assigneeHandle` (`07-gate-gap-fill.md` Section D; research-notes.md C12). Whether the sweep may report person-started sessions at all is an open owner decision (WC-14).
6. Should the sweep fix bootstrap_scan.sh (encoding, worktree `.git` file) or write its own scanner? Both bugs block Orca worktrees. [UNVERIFIED: open decision; the two bugs are CODE-VERIFIED at bootstrap_scan.sh:31, :73, :136]
7. `stage.activity` reads `working` for settled workers. Is that an Orca bug or a field meaning "agent process present"? (CODE-CONTRADICTED as a work signal)
8. Should the sweep allowlist exclude `git stash *` (crash-recovery SKILL.md:4) and avoid `ccsession --list` because of its migration writes? [UNVERIFIED: open decision; basis CODE-VERIFIED at SKILL.md:4 and ccsession:1787-1788, :285-287]
9. Does `--include-remote` cost a network round trip per call, and how should it be bounded under the batching policy? [UNVERIFIED: help text does not say; no remote capture]

## Summary

- Primary source: `orca-ide worker-list --include-remote --json [--run <id>]` with `page.nextCursor` paging; per-worker fields are `projection.{outcome, liveness, resource.terminalState, nextAction, attention}` plus `observation.agentWait` (from worker-show). Field shapes are CODE-VERIFIED from captures; row equality with worker-show is UNVERIFIED. [CODE-CONTRADICTED as a command name, re-verified 2026-11-07: in 1.4.245 the command is `orca-ide orchestration worker-list`; top-level `worker-list` prints "Unknown command: worker-list"]
- Gate fix B-03 (2026-11-07): every Orca verb in this file is run as `orca-ide orchestration <verb>` (for example `orca-ide orchestration worker-list --include-remote --json [--run <id>]`); the bare `orca-ide worker-list` form above is kept only as the original text and is wrong.
- Classification rules (superseded in detail by research-notes.md Section C, gate fix B-01/B-02): `unverifiable` and late heartbeats are absence, reported as "could not determine"; stall needs positive proof with the turn proved final; non-null agentWait means healthy waiting; finished needs the contract read as well as Orca's settled outcome; a fenced dispatch is its own class. Safe to close is a separate two-part REVIEW dimension (terminal releasable: `reclaimable` + `nextAction release`; worktree removable: the five `WORKER-CONTRACT.md:108` conditions false), printed and never run. `stage.activity` must not be used.
- Disk sources: WC-4 `return-contract.yaml` (`worker_status`, `blocked_question`) separates blocked from failed, which Orca alone cannot; `progress.md`, sprint and roadmap state as in crash-recovery refs/pipelines.md.
- Reusable from sc-crash-recovery: SAFE/REVIEW labels, the "What I could not determine" section with `unscanned:` markers, the report template and `parse_session_log.py`. Not reusable as-is: `bootstrap_scan.sh` (two bugs), the `--all` path and the allowed-tools list (`git stash *`, `~/workspace` path).
- ccsession: read `topics/*.txt` and the `orca-tabs` map directly; `ccsession --list` is human-only output and can write.
- Option A4 (extend sc-crash-recovery): no section of this file names it, so no A4 text was added or removed here. The reuse limits it would rest on stay [CODE-CONTRADICTED]: the allowed-tools list holds `git stash *` and a `~/workspace/IronClaude/...` path (SKILL.md:4) that does not match this host's `~/workspaces/worktrees/...` layout, and bootstrap_scan.sh misses Orca worktrees (`.git` is a file, :31, :73) and encodes paths differently from Claude Code (:136).
- Verification (2026-11-07): every file:line citation re-read against current source and captures. Corrected 10 citations in 8 places (lc16/lc17 resource ranges; worker-list help line 3 -> 3, 19; lc16/lc17 stage 127-133 -> 128-133; lc16 liveness 135-140 -> 135-139; lc16 evidence 141-146 -> 140-144 in two tables; lc16 terminal 165-181 -> 167-175; lc16 retainedReason 186-200 -> 191), each marked `(re-verified 2026-11-07)`. Contradicted: 8 (activity signal, `git stash` allowlist, `~/workspace` path, bootstrap encoding, `ccsession --list` writes, Q7, and the two new command-name notes on the help row and this summary). Unverified: 30 lines carry an UNVERIFIED tag (Orca guide text, derivations, open questions and reuse judgements). All other citations re-verified and hold.
