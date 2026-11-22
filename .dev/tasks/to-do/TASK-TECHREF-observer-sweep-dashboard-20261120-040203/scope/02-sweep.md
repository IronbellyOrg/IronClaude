# Scope discovery slice 2 of 4: the sweep
**Scope:** src/superclaude/cli/sweep/, commands/sweep.md, skills/sc-sweep-protocol, cli/main.py registration, tests/sweep, tests/commands/test_sweep_command.py, WORKER-CONTRACT.md, HOW-WE-WORK.md, docs/designs/orchestrator-mode.md
**Snapshot:** /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6). All paths below are relative to it.
**Status:** Complete
**Date:** 2026-11-20
---

Notation: `file:line` is from the snapshot. [CODE-VERIFIED] = read in code. UNVERIFIED = stated only by a doc/comment, or never captured.
Key finding up front: `docs/designs/orchestrator-mode.md` (1058 lines) is NOT a general orchestrator doc. It is the Phase 1 architecture design of exactly this sweep (title line 1). It is the design-of-record for the sections below.

## 1. Per-file table

| Path | Lines | Purpose | Key public names |
|---|---|---|---|
| src/superclaude/cli/sweep/__init__.py | 12 | Lazy `__getattr__` export so importing the package runs no seam | `sweep_group` (lines 4-9) |
| src/superclaude/cli/sweep/commands.py | 288 | Click shell: arg checks, bind Run, collect, classify, render, publish (the ONLY write), print JSON | `sweep_group` (214), `run` (242), `_parse_window` (43), `_check_output` (99), `_publish` (153), `_PublishError` (32); consts `DEFAULT_WINDOW="6h"`, `MAX_WINDOW_HOURS=720`, `MAX_SUFFIX=99` (27-29) |
| src/superclaude/cli/sweep/models.py | 278 | Frozen dataclasses + class/state constants; stdlib only | `CLASSES` (50), `PACKAGE_STATES` (62), `SweepContext` (75), `OrcaObservation` (84), `ContractRecord` (116), `TranscriptTail` (129), `TabMapEntry` (144), `SessionRow` (152), `PackageRecord` (186), `WorktreeState` (196), `Classification` (213), `SafeToClose` (222), `SourceCoverage` (229), `SweepInput` (237), `ClassifiedRow` (254), `SweepResult` (262), `report_folders` (29), `JSON_SCHEMA_VERSION=1` (18) |
| src/superclaude/cli/sweep/probes.py | 1477 | Read side: only module that starts a subprocess. Seams, allowlists, budget, disk/git readers, `collect` | `ALLOWED_ORCA` (49), `ALLOWED_GIT` (68), `Budget` (124), `_orca` (266), `_git` (315), `check_orca_argv` (226), `check_git_args` (241), `bind_run` (397), `parse_time` (413), `parse_worker_show` (471), `parse_status` (518), `read_ledger` (639), `read_packages` (713), `read_contract` (781), `read_transcript_tail` (865), `read_tab_map` (898), `read_orca_version` (903), `read_worktree` (1051), `collect` (1322), `BindingError` (104) |
| src/superclaude/cli/sweep/classify.py | 1009 | Pure classifier: rules 1-9, joins, packages, safe-to-close, `classify_all` (no file/process/clock) | `RULES` (345), `classify` (369), `policy_of` (389), `package_state` (423), `mark_shared_packages` (432), `removable` (455), `safe_to_close` (479), `classify_all` (880), `JOIN_PATH="B"` (40) |
| src/superclaude/cli/sweep/report.py | 695 | Pure renderer: Markdown report (12 sections) + JSON v1 | `render` (608), `to_json` (613), `sanitize` (569), `cell` (602), `SECTIONS` (545), `NEXT_INSPECTION` (54), `CHECKED_ORCA_VERSION="1.4.245"` (23) |
| src/superclaude/commands/sweep.md | 70 | `/sc:sweep` command (thin; `allowed-tools: Skill`, line 9); mandates Skill `sc:sweep-protocol` (46-47) | flags table (35-40) |
| src/superclaude/skills/sc-sweep-protocol/SKILL.md | 66 | Runs `superclaude sweep run <args>` once, Reads report, prints counts + path; defines the exempt chat reply | `allowed-tools: Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read` (line 4) |
| src/superclaude/cli/main.py | n/a | Deferred registration at 581-583: `main.add_command(sweep_group, name="sweep")` | |
| tests/sweep/ | 8612 total (8 py files + 21 fixtures) | 323 tests: test_classify 94 (1978 lines), test_probes_allowlist 100 (2397), test_cli_contract 61 (1534), test_report 43 (1465), test_readonly 12 (536), test_git_config_hole 10 (276), test_cli_registration 3 (69), conftest (357) | fixtures/ = captured sanitized Orca JSON (`SOURCES.md`: capture 2026-11-11, Orca 1.4.245-aidev02.9cfecdd30b2a) |
| tests/commands/test_sweep_command.py | 637 | 28 static drift guards on sweep.md, SKILL.md and the `pragmatic` output-style chat-summary exception | e.g. `test_sweep_command_has_no_unattended_mode`, `test_sweep_skill_fallback_only_on_command_not_found`, `test_style_exception_does_not_leak_into_work_discipline` |
| src/superclaude/core/WORKER-CONTRACT.md | 339 | WC-16 (287-289), "The sweep" (110), never-as-worker list (23), WC-10 (46) | |
| src/superclaude/core/HOW-WE-WORK.md | 361 | Routing row (298) and coordinator bullet (359) | |
| docs/designs/orchestrator-mode.md | 1058 | Phase 1 design of this sweep | sections 1-18 + addendum (1056) |

Registration tests: `test_sweep_help_exits_zero`, `test_sweep_run_help_exits_zero`, `test_import_is_lazy_and_runs_no_seam`.

## 2. `superclaude sweep run` surface [CODE-VERIFIED commands.py]

Group `superclaude sweep` has exactly one subcommand, `run` (219). No worker mode, no `--unattended`, no `--json` flag (JSON is always printed).

| Flag | Default | Check |
|---|---|---|
| `--run <id>` (repeatable) | the Run bound to this terminal via `orca-ide orchestration run-current` (264-266) | must `fullmatch` `run_[0-9a-f]{12}` (probes.py:46; commands.py:87-92); duplicates collapse, first-seen order |
| `--window` | `6h` (27) | `[1-9][0-9]{0,3}[hd]`, max 720h/30d (43-52) |
| `--root` | walk up from cwd to first folder holding `.git` (file or folder) (55-84) | must be a dir with `.git` |
| `--output` | `<root>/.dev/sweeps/` | must be that folder or below (a symlinked sweeps folder fails), and must not overlap `<root>/.dev/tasks`, `~/.claude/projects`, `$XDG_STATE_HOME/ccsession/orca-tabs` (254-262, 99-123) |

Exit codes (docstring 1-9; code 279-288):
- 0: report published and JSON printed.
- 1: internal error, stderr `[sweep <stage>] <msg>`, stage in args/bind/collect/classify/render/publish/output (246-276, 287); publish failures print `[sweep publish] ...` lines (282-285).
- 2: usage error (`click.UsageError`) or `BindingError` (no Run bound and none named: "no Run bound: pass --run <id>", probes.py:403).
- Orca unavailable does NOT exit non-zero once a Run id is known: it becomes `unscanned` source rows and the report still publishes (probes.py `_orca_reads` 1114-1192). Only binding needs Orca to succeed (probes.py:404-407).

stdout: one `json.dumps` object (commands.py:277-278) from `report.to_json` (report.py:613-695), `schema_version` 1. Keys: `schema_version, observed_at, collected{start,end}, scope{runs,root,worktrees}, window, orca_available, sources[{name,coverage,age_seconds,unscanned}], rows[{row_id,class,waiting_kind,rule,evidence,notes,policy,person_started,safe_to_close{terminal,worktree,reason}}], worktrees[{path,status_read,uncommitted,unpushed,dev_tasks_unsaved,frozen,packages[{id,location,state}],shared_package_ids,removable,removable_reason}], waiting{a,b}, summary{counts,bound_reached,visible,historical,total,total_is_lower_bound}, report_path`. The #409 "dimensions" (lifecycle, phase, health, ...) are report-only, never JSON keys (models.py:163).
`summary.total_is_lower_bound` is hard-coded True in Phase 1 (classify.py:986-989, a `shortcut:` comment) because remote hosts are never scanned.

Budgets (probes.py:124-143): 50 `worker-show` calls total (split across Runs, 145-169), 90 s total, 10 s per call. Byte limits (marked "proposed", design open item 19): orca/git output 8 MiB, contract/ledger 1 MiB, transcript tail 256 KiB (85-89). `WORKER_LIST_PAGE=100`: a full page sets `truncated` (89, 1160).

## 3. What the sweep reads

### 3a. Orca (probes.py)
Binary is `orca-ide`, or `$ORCA_CLI_COMMAND` when set; never bare `orca` (probes.py:43, 214-216). Every call goes through `_orca` after `check_orca_argv` matches an exact template (226-238; ValueError before any process starts). `subprocess.run`, stdin=DEVNULL, no shell.

`ALLOWED_ORCA` = 10 templates (49-60), 7 verbs. Called in Phase 1:
| Call (after binary) | When | Source |
|---|---|---|
| `orchestration run-current` | only when no `--run` given (bind_run, 397) | plain text, not JSON; no-binding sentence "No Run is bound to this terminal." (93, 254-263) |
| `orchestration worker-list --run <run> --json` | once per Run (1150) | list key `workers`; 100 rows = truncated |
| `orchestration task-list --ready --run <run> --json` | once per Run (1165) | ready Tasks with no Dispatch become rows with `status="ready"` (1251-1261) |
| `orchestration task-list --run <run> --json` | once per Run (1178) | task spec text + result `body` (used for gate policy, report-dir, contract path) |
| `orchestration worker-show --dispatch <ctx_id> --json` | one per valid Dispatch id, capped 50 total / per-Run share (1265-1290) | fields: `dispatch.{id,assigneeHandle,dispatchedAt,completedAt,status}`, `projection.{liveness.verdict,outcome,parent,resource.terminalState,nextAction.kind}`, `terminal.worktreePath`, `observation|terminal.agentWait` (471-515) |
| `worktree ps --json` | once, if Orca still available (1335) | key `worktrees[].path`; `truncated` flag |
Pinned in the allowlist but NOT called: `worktree list --json`, `worktree current --json`, `worktree ps --agent-wait` and `... --agent-wait --json` (the last two allowed by owner ruling R5, 2026-11-08, comment 58-59; design section 18 R5). `--include-remote` is forbidden in any position (62).
First Orca call failing (nonzero exit/invalid response) = `unavailable` (391-393). Marker `runtime_unavailable` only counts as the JSON error code or the whole first stderr line (298).

### 3b. Git (probes.py:68-81, 315-358)
Argv prefix always `git --no-optional-locks -C <path> -c core.fsmonitor=false`, env `GIT_OPTIONAL_LOCKS=0`. Four exact calls per worktree: `status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all`; and three pre-checks that decide whether a git clean/process filter could run a program (issue 547): `config --show-origin --list -z`, `ls-files -z`, `check-attr --stdin -z filter`. If a filter with a command is selected, status is skipped, row `unscanned: git filter could run a program` (967, 1038-1040). Worktree set = the root plus each distinct resolved path from `worktree ps` (1308-1319). Yields uncommitted / unpushed / `.dev/tasks/` unsaved / ahead count / no-upstream (920-964).

### 3c. Files on disk (read-only `open`/`scandir`/`stat`)
- Packages: `<worktree>/.dev/tasks/{to-do,done}/<pkg>/`, `progress.md` for a `FINAL:` line (limit 1 MiB, tail 512 KiB), `.archiving` marker (655-710).
- Worker contract `return-contract.yaml` (`models.CONTRACT_FILE`): found only from paths or `--report-dir/--output-dir/--output` values named in the Task spec or report body (1092-1105); `yaml.safe_load`; fields worker_status, blocked_question, reason, report_path, artifacts, command; file mtime used as wait age (737-778). Must resolve inside a scoped worktree (1414).
- Claude Code transcripts: `~/.claude/projects/<key>/*.jsonl`, key = every non-alphanumeric char of the worktree path -> `-` (1075-1077, 1445-1477). Reads only the last 256 KiB, drops the first partial line; takes `timestamp` and `sessionId` of complete records (786-816). Does not read message content.
- ccsession tab map: `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/*`, 3 lines each: session id, launch dir, Orca terminal handle (870-895). Missing folder = readable and empty.
- Orca version: `/opt/Orca/resources/app.asar.unpacked/out/package.json` (83, 903). Report prints "Orca lock risk: unlikely" only when version prefix equals `1.4.245` (report.py:23, 159-166).
- Not read: `gh`/GitHub, remote hosts (source row `remote hosts` coverage `unknown`, 1381), Orca messages/mailbox ("Messages coverage: partial", report.py:199, 533-536), any screen or terminal content.

### 3d. The eight classes (models.py:50-59; decided in `classify` 369-386, first matching rule wins, `RULES` 345-355)
| Rule | Class | Fires when (classify.py) |
|---|---|---|
| 1 `blocked_contract` (161-188) | waiting on a person (a) | contract `worker_status: blocked`, transcript not unreadable, AND (Orca row settled, or `gate_policy` = report blocked, or Ruling halt code `E-HALT-QA`/`E-NO-RULING`, or no Orca row with a halt code). A live row under "ask the coordinator" declines with a note |
| 2 `orca_exit_proof` (191-208) | stalled (proved) | liveness `exited` AND `worker_done_seen is False` AND `fenced_evidence == "absent"` |
| 3 `fenced` (219-223) | fenced | `fenced_evidence == "present"` |
| 4 `waiting_signal` (226-248) | waiting on a person (a) when `agentWait` non-null; (b) when contract `failed` with a STOP `E-...` code other than `E-RESUME-NEEDED` (frozen plan), or an Orca row `status=="ready"` (ready Task, creator not observable) | |
| 5 `working` (251-269) | working | liveness `live` + outcome `in_progress` + `agentWait` key present and null |
| 6 `finished` (272-292) | finished | report body first line starts `guard refused:`, or Orca outcome in succeeded/partial/failed AND parsed contract worker_status in same set (needs a contract; "partial" adds a note) |
| 7 `idle` (295-311) | idle | person-started, no Orca row, readable transcript, last activity before window start. Printed under "Historical sessions", excluded from `visible` |
| 8 `person_active` (314-327) | person session (active) | person-started, readable, last activity within window |
| 9 `fallback` (330-342) | could not determine | anything else; also forced when the transcript is unreadable (384-385), the join is ambiguous, duplicate Dispatch rows disagree, or a source was unscanned |
`person_started` is decided by transcript joins (`_join_transcripts` 655-683, `_person_origin` 760-779): a transcript is a worker's when it joins a scoped Dispatch row (path A: `session_join` == Claude session id; path B, in force, `JOIN_PATH="B"` line 40: `dispatch.assigneeHandle` == tab-map terminal handle or file name, plus the transcript's earliest timestamp must fall in the Dispatch window, 609-652). By my reading of `_guard` (741-757, `earlier_pane = path_b and bool(rows)`) a no-tab-map-entry transcript can be `person_started True` only when the scoped Runs have no Dispatch rows; with workers present it is None (could not determine). Every True carries note "origin not proved ..." (778). This reading is not tested by me: UNVERIFIED against tests.

### 3e. Observed vs not observed in Phase 1
- Not observed: stalled (proved) and fenced. `OrcaObservation.worker_done_seen` defaults None and `fenced_evidence` defaults `"unreadable"` (models.py:108-109); a grep of `cli/sweep/` finds no assignment to either outside those defaults and the tests/classify readers, so rules 2 and 3 cannot fire from a real `collect` [CODE-VERIFIED by grep]. The report says so (report.py:42-45, SP24_LINE; sweep.md:16; SKILL.md:26 prints `(not observed in Phase 1)` beside both counts). A decline note `Orca: exited; fenced evidence not readable` attaches when liveness is `exited` (81, 205-208).
- Observed but weak: waiting (a) via `agentWait` non-null: only null was ever captured, non-null meaning UNVERIFIED (models.py:97-99, probes.py:462, design open item 6); its wait time `agent_wait_since` is reserved and never set (models.py:111-112), so such rows have unknown age.
- Observed: working, finished, idle, person session (active), could not determine, waiting (a via blocked contract), waiting (b).

## 4. What it writes, never writes, and who reads it

**Writes (only `commands._publish`, 153-208):** one Markdown file `<root>/.dev/sweeps/<UTC YYYYMMDD-HHMMSS>-sweep.md` (stem from `now`, 155); a clash gets `-2` to `-99` (182); more than 99 = exit 1 "report name space exhausted". Mechanism: `makedirs`, then a dot temp file `.{stem}.{pid}.tmp` created `O_EXCL`, written, `fsync`ed, `os.link`ed to the first free name (never overwrites), temp unlinked (165-208). Failure to unlink after linking = exit 1, report kept, no JSON (202-207). `.dev/sweeps/` is gitignored (snapshot `.gitignore:255-256`: "dated, operator-local, never posted (WC-16)"). No retention or cleanup (design 1: "the person deletes old reports by hand").
**Never writes:** no Orca write verb (allowlist has read verbs only), no git write (4 fixed calls, lock-free), no network, no lock file, no stdin to children, no file under `.dev/tasks`, `~/.claude`, or ccsession folders (`--output` overlap check, commands.py:99-123). Proven by `tests/sweep/test_readonly.py` (e.g. `test_sweep_run_adds_exactly_one_report_and_changes_nothing_else`, `test_a_sweep_starts_no_process_and_records_only_allowlisted_argv`) and `test_git_config_hole.py` (fsmonitor/filter cases).

**Report layout (report.py `SECTIONS` 545-558; `render` joins with blank lines, ends `Report complete`):**
1. Header block (no `##` heading): `READ ONLY . observed ... . collected ... (not an atomic runtime snapshot)`, Scope (Runs, worktrees, sessions shown/total, window), Orca binary, Sources, `Messages coverage: partial`, Orca lock-risk line, untracked-paths note, optional banners (worktrees not discovered, show cap/time budget reached, 100-row page) (182-211).
2. `## Source coverage` (table Source/Coverage/Age/Unscanned)
3. `## Waiting on a person (a)` (ID, Age, Question, Requested by, Decision owner, Affected, Evidence; "Requested by"/"Decision owner" always "unknown"; footer "Seen is not resolved / Answered: could not determine")
4. `## Waiting on a person (b)` (frozen plans, then `### Ready Tasks needing ownership review`)
5. `## Could not determine`
6. `## Retained problems` (interrupted archive, package in both to-do/ and done/, package active in several worktrees, WC-13 violation, bound reached)
7. `## Sessions (<shown>/<total>)` (per row: ID, ten #409 dimensions, Class, Rule, Evidence, Safe to close terminal/worktree, Notes, Next inspection)
8. `## Worktrees` (Uncommitted, Unpushed, .dev/tasks unsaved, package states, Removable + reason)
9. `## Historical sessions` (idle)
10. `## Shift Brief` (distinct count needing a person or undetermined)
11. `## What I could not determine`
12. Footer: `Inspection only.`, one line per source, `Report complete`.
All cell text goes through `sanitize` (strips ESC/CSI/OSC, control and bidi chars, neutralises `| < > [ ]`) and is cut at 200 chars (report.py:569-605). `Safe to close` never prints `yes` in Phase 1 (report.py:46-49; classify.py:479-504); `Removable` is `no` with a reason or `could not determine`, never `yes` (455-476).
Dimensions Phase/Approval/Admission/Evidence packet are never set by `classify_all` (SessionRow defaults `unknown`, models.py:164-173); Tests/review prints `unavailable` (report.py:401).

**Consumers.** (1) `/sc:sweep`'s skill: parses stdout JSON for only `report_path` + `summary`, Reads the report in <=150-line chunks to `Report complete`, prints counts and path (SKILL.md:23-29). (2) The coordinator, per WC-16: "reads its report before it acts" (WORKER-CONTRACT.md:289). (3) A person. A grep of `src/superclaude` finds no other code reading `.dev/sweeps` or importing `cli.sweep` (only `cli/main.py` registration); `commands/closeout.md:99` and `HOW-WE-WORK.md:298` merely name `/sc:sweep`. Whether any dashboard consumes the report: out of this slice, none found here.

## 5. How WC-16 binds the coordinator

WC-16 text (WORKER-CONTRACT.md:287-289), summarised:
- Cadence: on every coordinator wake or wait timeout, at most once per 5 minutes, run "The sweep." (line 110) unchanged AND, in the same pass, run `/sc:sweep` and read its report before acting. Keep that pass scheduled while work remains. "Phase 1 adds this duty, not a scheduler."
- Relation to the liveness sweep: `/sc:sweep` is "an added read": not a replacement, not a second pass; it does NOT update heartbeat records and does NOT run `worktree ps --agent-wait`; its reads are not L1 probes and do not count against the L1 cap. HOW-WE-WORK.md:359 repeats this.
- The liveness sweep (line 110) = one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`), one `stat` per worker contract path (WC-11), updating each worker's heartbeat record (arrival time, progress token, declared window); costly probes only for triggered workers. States S0-S11 and ladder L0-L5 (lines 116-157) key off heartbeats, `agentWait` (S4), transcript age and contract stat. The sweep CLI uses none of heartbeats; it reads `agentWait` from `worker-show`, not from `worktree ps --agent-wait` (which it never calls). So a pass makes two independent `worker-list` reads (coordinator's own and the CLI's).
- WC-10 binding: "The `/sc:sweep` classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine. A missing heartbeat is absence, never death." (WC-16 text; WC-10 itself is WORKER-CONTRACT.md:46). Stall proofs per line 157: `exited`, process exit, or a final agent turn with no `worker_done`; nudges/heartbeats/repeated reads/context exhaustion are never proofs.
- Must NOT: `/sc:sweep` "recommends nothing: no stop, retry, release, merge or removal"; the coordinator decides and acts under WC-6 etc.; report is "a dated local file; it is never posted"; person-started sessions "are never messaged"; the coordinator "never stops watching on its own" and re-arms an expired Orca wait.
- Escalate to the person, not act alone, on: failed/blocked result it cannot retry under WC-6, partial result judged unusable, a third brief-guard refusal, a ready Task it did not create (ownership review), a frozen plan, a fan-in with fewer than 2 admitted inputs. The coordinator records each admission/rejection in its run notes; the sweep does not observe them.
- Never-as-worker (WORKER-CONTRACT.md:23): `/sc:sweep` is on the list with `/sc:agent, /sc:closeout, /sc:git, /sc:help, /sc:issue, /sc:pm, /sc:swarm-wizard` (+ `/sc:pr-submit` while D3 stands): never dispatched as a worker, no `--unattended`. sweep.md:42 "There is no worker mode and no flag for one"; test `test_sweep_command_has_no_unattended_mode`.
- Chat format: SKILL.md:33-51 defines an "exempt reply" (counts and path only, no DONE/NEXT table) for a session with an explicit coordinator assignment; mirrored in `output-styles/pragmatic.md:23` (not read in full here).
- Related doc nit: sweep.md:22 says the coordinator runs it "inside its liveness sweep pass, at most once every 5 minutes".

## 6. Built vs only designed

BUILT on master (all files above exist and are registered; 323 + 28 tests): `sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-16, never-as-worker entry, HOW-WE-WORK rows, `.gitignore` rule.
Designed or declared but not live (all labelled "Phase 1" limits):
- stalled (proved) and fenced: classifier rules exist, no producer of `worker_done_seen` / `fenced_evidence` (3e).
- `Safe to close` and `Removable` can never be `yes` (report.py:46-49; classify.py:476, 479): `REASON_NOT_OBSERVABLE = "report read, open PR and unmerged commits not observable"` (classify.py:88-91).
- Ready-Task creator not observable (design open item 7); "Requested by"/"Decision owner" columns always `unknown`; "Answered" always `could not determine`.
- Remote hosts not scanned (`total_is_lower_bound` hard-coded True); Orca messages/mailbox not read.
- `agent_wait_since` reserved, never set; non-null `agentWait` meaning UNVERIFIED.
- Allowlisted but uncalled: `worktree list`, `worktree current`, `worktree ps --agent-wait` (x2).
- Phase 2 `/sc:close` (design line 217: "gets its own package, seam and allowlist; nothing in this package grows a write verb"); `commands/closeout.md` exists (name only seen in grep, not read: UNVERIFIED relation). No scheduler (WC-16), no retention.
- Doc staleness: design line 27 "`src/superclaude/cli/sweep/` does not exist yet" is [CODE-CONTRADICTED] (it exists, 5 modules). Design section 17 lists 23 open items, some since closed (item 6 marked resolved 2026-11-16 inline; the 1.0a capture is in tests/sweep/fixtures/SOURCES.md); which others remain open is UNVERIFIED. Design line 7 "third review did not pass cleanly" is history; blockers R3-B1..B3 are stated closed.
- No TODO/FIXME markers in `cli/sweep/` (grep); known limits are written as `shortcut:` comments (probes.py:271-273, 342, 1003; classify.py:986) and "Known gap" (classify.py:693-695: a worker-list row with no Dispatch id is dropped and can hide an incomplete list; UNVERIFIED whether real Orca emits such rows).
- `subprocess.run` buffers whole output; 8 MiB limit checked after exit (owner ruling 2026-11-12 D-01, probes.py:271-273).

## 7. Proposed deep-investigation assignments (2 research agents)

**Agent A: classifier and join semantics ("what does each row mean").**
Files: `cli/sweep/classify.py` (esp. 155-402 rules, 609-780 joins/guard, 880-1009), `models.py`, `tests/sweep/test_classify.py` (94 tests), `tests/sweep/fixtures/` (captured worker-show/tab-map JSON), design sections 7.2 and 12-14 in `docs/designs/orchestrator-mode.md`.
Why: the eight classes, the D9/path-B person_started narrowing, the guard cases, the contract-to-row mapping (`_contract_for`) and the could-not-determine forcing are the least obvious logic and the most likely thing a tech reference gets wrong. Questions to settle: exactly when `person_started` can be True; which fixture proves each rule; whether any producer for `worker_done_seen`/`fenced_evidence` exists on any other branch.

**Agent B: read-side, safety and coordinator integration ("what touches the world, who relies on it").**
Files: `cli/sweep/probes.py` (allowlists, `_orca`, `_git`, `Budget`, `collect`), `commands.py` (`_publish`, exit paths), `tests/sweep/test_probes_allowlist.py`, `test_readonly.py`, `test_git_config_hole.py`, `test_cli_contract.py`, `WORKER-CONTRACT.md` (lines 20-30, 96-160, 287-289), `HOW-WE-WORK.md:298,359`, `commands/sweep.md`, `skills/sc-sweep-protocol/SKILL.md`, `output-styles/pragmatic.md` (sweep exception), `tests/commands/test_sweep_command.py`, `.gitignore:255-256`.
Why: documents the exact Orca/git/disk calls, budgets, failure-to-unscanned behaviour and publication atomicity, then the WC-16 coordinator contract (cadence, non-duplication with the heartbeat sweep, escalation list) and the chat-summary exemption. Questions to settle: what the live coordinator skill/worker docs actually do with the report (any code consumer, e.g. dashboard or issue-watch, UNVERIFIED so far); whether `orca-ide` vs `orca` naming in WC-16 text matters to users; which design open items (section 17) are still open.
End of slice 2.
