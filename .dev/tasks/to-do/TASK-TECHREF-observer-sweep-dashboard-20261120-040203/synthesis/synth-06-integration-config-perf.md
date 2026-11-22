# Synthesis 06: Sections 6-11 (State, Components, Integration, Configuration, Errors, Performance)

Inputs: research 01-06, gapfill GF1-GF5, `gaps-and-questions.md`, `qa/qa-research-consolidated-findings.md` (M-1 to M-17). Code paths are relative to the repo root at origin/master 61ac2c2e6 (`/home/coder/.cache/ic-snap-20261120/master`); design-package paths are under `.dev/design/orca-observer-20261106/` (commit 495eb96d1). Tags: [CODE-VERIFIED] read in code, [UNVERIFIED] kept open, [DESIGN-ONLY] no code. Where a gap-fill file supersedes a statement in files 01-06, the gap-fill is used (GF-1 labels: stalled (proved), fenced, `agent_wait_since`, living-report writer and `orchestrator_repo` are KNOWN LIMIT (cited); DC-01 and DC-02 stay DEFECT-CANDIDATE; remediation tasks not created (read-only brief), flagged for the owner). Facts only; no unification recommendation. Line counts use `wc -l` values (M-4).

---

## 6. State Management

N/A as a client-side store: observer, sweep and agent-work-report (AWR) are CLI and file based tools and the #409 design package is a static renderer. The runtime state that does exist:

| Tool | State | Held where | Reset / lifetime |
|---|---|---|---|
| Observer | `Session` (focus, selected, filter_text, show_historical, baseline, marked, inspector_scroll, selected_question), changed only by `apply_cycle` / `apply_key` | in memory, frozen dataclass (view.py:151-168) | process life; no persisted "last look" (rendering-rules.md:97) |
| Observer | `CycleResult`: one immutable result per cycle, replaced under a lock (collector.py:155-184); states NOT_POLLED, NOT_AVAILABLE, OK, FAILED, PARTIAL | in memory | rows kept across cycles (`reobserved=False`), no cap on the row set (parse.py:723-728; G-04); questions bounded at 1,000 (questions.py:21); both reset on restart |
| Sweep | none between runs; one report file is the only artifact (commands.py:153-208) | disk, `.dev/sweeps/` | by hand (SP-22: the person deletes old reports; design 1:35) |
| AWR | `<state>/run.lock` `{run, kind, started}`, run folder, previous run's `snapshot.json`, `action-log.jsonl`, `priorities.json` | `.dev/coordinator/` of the orchestrator repo | lock older than budget is kept as `stuck` and replaced (run.py:95-131) |
| Design package | none; fixture is deterministic (fixtures.py:1) | n/a | n/a |

Key transitions (observer collector, [CODE-VERIFIED] collector.py:252-321, view.py:456-463):

```
NOT_POLLED --discover finds no Orca--> NOT_AVAILABLE (loop ends for good)
cycle: first page ok --> OK (all pages) | PARTIAL (cap, later-page error, empty page)   wait = 15 s
cycle: first page fails --> FAILED, last good rows kept, wait 15 -> 30 -> 60 -> 60 s
view : OK|PARTIAL, no good poll for >= 45 s (monotonic) --> STALE   (FAILED is never shown as STALE)
```

Cross-store dependencies: none inside a tool. The only shared state names are different files with the same name (`snapshot.json`: observer state dir versus AWR run folder, 02 section 5.3).

## 7. Component Inventory

N/A: these tools have no component tree. The subsystem tables in Section 5 are the inventory.

## 8. API & Integration Points

### 8.1 Orca verb inventory (every Orca call across the tools)

Binary per tool: observer = discovered binary (`_find_orca`: candidates `orca-ide` then `orca` via `shutil.which`, accepted only on exit 0 and a topic named `orca-cli` in `skills list --json`; install_user_setup.py:36, 247-270); sweep = `orca-ide` or unvalidated `$ORCA_CLI_COMMAND`, "never bare orca" (probes.py:43, 214-216); AWR = bare `orca` from PATH (run_cmd list args, 05 section 27); design package = no Orca call (fixtures.py:1). Allowlists: observer 3 argv shapes plus 13 forbidden prefixes (adapter.py:29-50); sweep 10 templates, 7 verbs, `--include-remote` forbidden (probes.py:49-62); AWR has no allowlist.

| Tool | Binary | Verb and argv template (after binary) | Purpose | Status | Source |
|---|---|---|---|---|---|
| Observer | discovered | `skills list --json` | discovery, once per `LiveSource` | called (built by `_find_orca`, allowed by exact match) | adapter.py:30, 148-149; install_user_setup.py:258-264 |
| Observer | discovered | `orchestration worker-list --json --limit 100 [--run <id>] [--cursor <c>]` | worker ledger, up to 5 pages | called each cycle | adapter.py:29, 173-183 |
| Observer | discovered | `orchestration check --all --types question --run <id> --json` (8 tokens) | questions of one Run, `--questions` only | called (gate constants True) | adapter.py:32, 186-190, 469-512; commands.py:67, 70 |
| Sweep | orca-ide / env | `orchestration run-current` (plain text, no `--json`) | bind the Run when no `--run` | called | probes.py:50, 399 |
| Sweep | orca-ide / env | `orchestration worker-list --run <run> --json` | worker rows, once per Run | called | probes.py:51, 1150 |
| Sweep | orca-ide / env | `orchestration worker-show --dispatch <ctx_id> --json` | liveness, outcome, `agentWait`, `assigneeHandle` | called, max 50 per sweep | probes.py:52, 1281 |
| Sweep | orca-ide / env | `orchestration task-list --ready --run <run> --json` and `task-list --run <run> --json` | Task rows (ready Tasks, bodies) | called, once per Run each | probes.py:53-54, 1165, 1178 |
| Sweep | orca-ide / env | `worktree ps --json` | worktree paths | called once if Orca still available | probes.py:55, 1335 |
| Sweep | orca-ide / env | `worktree list --json`, `worktree current --json` | none yet | pinned, not called (zero-argv test) | probes.py:56-57; test_probes_allowlist.py:624-638 |
| Sweep | orca-ide / env | `worktree ps --agent-wait [--json]` | prompt-wait listing | pinned (R5, owner 2026-11-08), not called | probes.py:58-59 |
| AWR | bare `orca` | `terminal list [--worktree path:<p>] --json`; `terminal read --terminal <h> --screen --json`; `terminal wait --terminal <h> --for tui-idle --timeout-ms <ms> --json` | find and inspect the coordinator session, session join | called (read) | orca_term.py:24-31, 87-110; sessions.py:291 |
| AWR | bare `orca` | `terminal send --terminal <h> --text <t> [--enter --wait-submit <s>] --json`; `terminal create --worktree path:<ws>` | start and wake the coordinator session | called, WRITE (waker.py only) | orca_term.py:124-133; waker.py:186-189, 297-302 |
| AWR | bare `orca` | `worktree list --json`; `worktree set --worktree path:<repo> --unread --comment <text>` | issue/PR links of a worktree; unread mark as DM fallback | called; first read, second WRITE | sessions.py:309-312; waker.py:88-96 |
| AWR | bare `orca` | `automations list --json`; `automations runs --id <id> --json` | automation run records (names starting `coordinator-`) | called (read) | run.py:160-186 |
| AWR | bare `orca` | `tab list|close|switch|create ...`; `eval --page <id> --expression location.reload()` | open the report page in the Orca browser | called, WRITE (tab) | page.py:354-377 |

Orchestrator design set against these three [DESIGN-ONLY]: the design (`docs/designs/orchestrator.md`, merged by PR #681, "holds no implementation code", DESIGN:3) names about 30 distinct Orca verb forms (GF-3 rows 1-34). The `superclaude orchestrator` package and `sc-orchestrator-protocol` skill are absent from the snapshot. The binary the design would use is not stated in the research. "Match" = token-for-token with an existing allowlist.

| Verb family | Observer (3) | Sweep (10) | AWR | Orchestrator design (DESIGN line) |
|---|---|---|---|---|
| skills | `skills list --json` | none | none | `skills get orchestration [--reference f]` (9, 515, 534, 726) |
| run-current / run-create / run-use / run-show | forbidden (run-use, run-create) | `run-current` without `--json` | none | `run-current --json`, `run-create --objective`, `run-use --id`, `run-show --id` (98, 534, 661, 1262) |
| worker-list | `--json --limit 100 [--run][--cursor]` | `--run <run> --json` | none | `--json` (572), `--run <id> --json` (744), `--run <id> --terminal-state reclaimable --json` (628) |
| worker-show | none | `--dispatch <id> --json` (match) | none | same argv (565, 744, 1278) |
| worker-read / task-list | none | task-list `--run` (match), `--ready --run`; no worker-read | none | `worker-read --dispatch <id> --source transcript --limit <=200` (572, 745); `task-list --run <id> --json` (1304) |
| worker-start, request-show, release/retain, stop/abandon/reset, task-create, gates | none (`dispatch`, `reset` etc. forbidden) | none | none | worker-start (565, 726), `--retry-request` (1279), request-show (567), release/retain (628), task-create (565), gate-create/resolve (572); stop/abandon/reset listed as refused (759, 1117) |
| check / send / reply | `check --all --types question ...` only; `--ack --wait --peek` forbidden | none | none | `check --wait --types worker_done,escalation,question,status --timeout-ms 240000`, `--ack`, `--peek` (572, 748, 1263); `send` (112, 572, 1263); `reply` (572) |
| terminal | none | none | list, read, wait, send, create | list (744), read (573), send incl. `--interrupt` via `escalate` (573, 749), wait (748), close (710, 762) |
| worktree | none | `ps --json` called; `list`, `current`, `ps --agent-wait` pinned | list, set | `show --worktree issue:<N>` (474), `current --json` (565; match with pinned template), `set --unread --comment` (112, 666), `ps` without `--json` (1129), `rm` refused |
| other | none | none | automations, tab, eval | `project setup-clone` (114), `reference add|find` (474, 565), `automations list|show|runs` read-only (348, 762); `ccsession` is not an Orca verb |

Counts: 4 designed argv match a sweep template (worker-show, `worker-list --run`, `task-list --run`, pinned `worktree current --json`); none match an observer template; every write or consuming verb of the design is forbidden in the observer or outside the sweep allowlist (GF-3 section 3). Built today in the same area: `issue_watch` builds a 12-element `orca agent launch` argv (launch.py:95-131); PR A (#686, open) makes the poll wake instead of launch.

### 8.2 Internal Integration Points

| Integration | Direction | Mechanism | Description |
|---|---|---|---|
| WC-16 coordinator binding (sweep) | coordinator to sweep | prose duty, no code | WORKER-CONTRACT.md:287-289: on every wake or wait timeout, at most once per 5 minutes, run "The sweep." (WC:110) and `/sc:sweep`, read the report before acting. Chain: `commands/sweep.md:47` invokes skill `sc:sweep-protocol`, whose steps 1-2 run `superclaude sweep run`, registered at cli/main.py:581-583. No scheduler (sweep.md:22 "Nothing starts it automatically"), no throttle, no check that the report is read [CODE-VERIFIED absence]. The sweep issues its own `worker-list` and never runs `worktree ps --agent-wait`; it reads `agentWait` from `worker-show`, a different source from the coordinator's listing (04 s6.1) |
| `.dev/sweeps` consumers | sweep to disk | file | Writer only (commands.py:100-132, 240). No Python module, hook or script reads a published report back; readers are the skill's Read step (SKILL.md:25) and a person or coordinator. Ignored by `.gitignore:255-256` (absent from the stale checkout, SD-14) |
| Observer snapshot consumers | observer to disk | file | None found: nothing in `src/superclaude/{commands,skills,agents,core,hooks}` names the observer or its snapshot; only tests read it (02 s5.3; G-09) |
| Observer and sweep to each other | none | none | no import or reference either way (grep, 06 s8.3); "observer reads the sweep JSON" is a proposal in the live issue 409 body only (alignment item 1, undecided) |
| Orchestrator design to sweep / observer | none | none | design never mentions `/sc:sweep`, WC-16, observer or `.dev/sweeps` (grep, GF-3 s2); sweep and observer code never mention the orchestrator, poll or entry files. Whether WC-16 binds a script-started orchestrator is [UNVERIFIED] (U-35) |
| AWR to coordinator run folders | AWR to `.dev/coordinator/runs/<run>/` | files | 15 steps, 16 scripts; gate = 7 checks plus a sha256 chain (`overview.md`, `script-checks.md`, `report.html`, `summary.md`) (run.py:204-368) |
| Living-report entry files | designed writer to AWR | JSON files `.dev/coordinator/orchestrated/<owner>__<repo>__<n>.json` | Reader built: `exclude.py`, `run.py refresh`, `render.entry(filed=)` (merged PR #684). Writer `superclaude orchestrator report-entry` has no code (KNOWN LIMIT sequenced to PR B, no PR open; label flips if the owner says the PR split is not a scope decision, G-35). Only entry-file write in the snapshot: `move_to_closed` (run.py:483). `sc-closeout-protocol` `settle.sh:1037-1042` probes the verb and ends `ENTRY escalated why=surface_absent` |
| `orchestrator_repo` route | AWR reads poll config | `~/.config/superclaude/issue-watch.json` | KNOWN LIMIT sequenced to PR A (#686, open): master poll rejects the key (cycle.py:216-220), so only `$AWR_ROOT` works; CODE-CONTRADICTED tag on SKILL.md:14 stands until PR A merges (CC-02). Who sets the key: [UNVERIFIED] |
| Design package to observer | none in code | names and intent only | "no code, import or vendored file" (ARCHITECTURE-SPINE.md:172); all 10 same-named fixtures differ by `cmp`; palette: all 8 colours equal (theme.py:59-69 vs canvas.py:7); 3 of 20 designs partly implemented (06 s4) |

Who reads what, who writes what:

| Artifact | Written by | Read by |
|---|---|---|
| `.dev/tasks/{to-do,done}`, `~/.claude/projects/<key>`, `<state>/ccsession/orca-tabs`, Orca `package.json` | other tools | sweep (read only) |
| `~/.config/orca/agent-hooks/last-status.json`, `~/.claude/projects/*/<id>.jsonl`, `/proc/<pid>/environ` | Orca, Claude, OS | AWR `sessions.py`, `orca_term.py` |
| `runs/<id>/*`, `report.html`, `wakes/*.json`, `action-log.jsonl`, `priorities.json`, `settings.json` | AWR scripts (`prefs.py` writes priorities and log rows) | AWR scripts; `page.py` serves the whole `.dev/coordinator/` folder on 127.0.0.1:8765 (G-22) |
| design-package `exports/`, `manifest.json`, `gallery.html`, `portfolio.pdf` | `render.py` | people; `tests/test_designs.py` (manifest, exports, PDF header); not the observer |

File formats and schemas written:

| Format | Contents |
|---|---|
| Observer snapshot v1 | `schemaVersion` 1, closed (`additionalProperties:false`), additive-only policy, "PROPOSED, not an Orca contract"; root keys schemaVersion, producer, cycle, generatedAt, source, page, scope, counts, rows (+ optional collection, questions); 20 of the 31 parsed worker attributes; `UNKNOWN` string for unsupplied values; questions group has ids, times, counts and `closureEvidence:"unavailable"`, never subject or body; 0600 atomic replace; one fixed name, no history (snapshot.schema.json:3-9; export.py:20, 141-274) |
| Sweep Markdown | 12 sections (two without `##`), ends "Report complete"; `<stem>.md`, `<stem>-2.md` ... `-99.md` (report.py:545-558; commands.py:29) |
| Sweep JSON v1 | 12 keys: schema_version, observed_at, collected, scope, window, orca_available, sources, rows, worktrees, waiting, summary, report_path; no `orca_binary`, `orca_version` or the ten dimensions (report.py:613-695; C7) |
| AWR run folder | `run.json`, `*.json` per source, `overview.md`, `script-checks.md`, `report.html` (meta `overview-sha256`), `notes.json`, `summary.md`, `complete.json` or `abandoned.json` (05 s23); entry-file contract at common.py:133-151 |
| Design package | per design x width (160/116/80) six files `.txt .ascii.txt .ansi .svg .png .mono.png`; `contact-sheet.png`, `portfolio.pdf`, `manifest.json` `{synthetic, as_of, batch, widths, concepts[], fixture_sha256}`, `gallery.html`, `fixture.json`, `scenarios/*.json` (render.py:41-124; fixtures.py:114-122) |

### 8.3 External Service Dependencies

| Service | Purpose | Failure Mode | Fallback |
|---|---|---|---|
| Orca CLI | all three tools | observer: no validated Orca gives `NOT_AVAILABLE` and the loop ends; call failures give FAILED or PARTIAL (section 10). Sweep: first-call failure becomes `unavailable`, later Orca reads are skipped as `unscanned`. AWR: `automations` failure writes `{"read": false, ...}`; terminal list truncated means "not read" | observer keeps last good rows; sweep still publishes (exit 0) unless binding fails with no `--run` (exit 2); AWR continues without that source |
| GitHub, orgs `IronbellyOrg` and `IronbellyGroup`, plus Projects | AWR only (`gh repo/issue/pr/project/search`, `gh api timeline`; read-only; no `--repo` flag because both orgs are swept) | per-repo errors go to `coverage.json` / `source_errors`, never fatal; `gh` close lookups: only "HTTP 404/410/Could not resolve" mean closed | items of unread repos are carried, not closed (compare.py:108-118, 166-169). Observer, sweep and design package read no GitHub or ClickUp (grep, 06 s8.2) |
| ClickUp REST (`https://api.clickup.com/api`) | AWR reads tasks, comments, chat; only write is the self-DM | no `CLICKUP_API_TOKEN` raises `ClickUpError`; GET retried up to 3 times on 5xx; POST never retried; 429 waits up to 65 s; at most 6 attempts | `waker.notify` falls back to an Orca unread mark and comment, then records the failure (waker.py:81-99) |
| git | sweep: 4 allowlisted shapes, 2-4 calls per worktree; AWR: `git -C <path> remote get-url origin` (10 s) | `GitCallFailed` gives `unscanned` / unknown, never clean | worktree rows marked unknown |
| Local page server and browser | AWR `page.py`: detached `python -m http.server 8765 --bind 127.0.0.1 --directory .dev/coordinator` | server not answering after about 10 s | none recorded; report template loads Google Fonts when opened (G-23) |

## 9. Configuration & Environment

### 9.1 Configuration Files

| File | Purpose | Key Settings |
|---|---|---|
| `src/superclaude/skills/agent-work-report/config.json` | AWR behaviour | 14 keys: person, person_name, orgs, excluded_repos, timezone, daily_run_local, report_days, missed_run_dm_local, time_budget_minutes, session_tag, automation_prefix, clickup_user_id, clickup_email, priority_labels. Values recorded: person `clayphi`, orgs `IronbellyOrg` and `IronbellyGroup`, excluded_repos empty, timezone America/Chicago, daily_run_local 07, missed_run_dm_local 09, time_budget_minutes daily 120 / hourly 10, automation_prefix `coordinator-`; other values not recorded in research. `session_tag` read at waker.py:175, 273, 362; `person_name` at classify.py:35, 62; no read of `clickup_email` or `clickup_user_id` found (a fuller grep is needed before calling them unused; G-48). No `workspace` key (test at test_agent_work_report.py:3005) |
| `~/.config/superclaude/issue-watch.json` | poll config; AWR reads `orchestrator_repo` (absolute path to a repo holding `repos.yaml`) | master poll rejects any key outside `_TOP_KEYS` (cycle.py:58-69, 216-220); PR A branch accepts it. Who writes the file: [UNVERIFIED] |
| `.dev/coordinator/settings.json`, `priorities.json` | AWR state written by `clickup.py` and `prefs.py` | clickup_user_id, clickup_workspaces, clickup_dm_channel; per-item priority overrides (clickup.py:558-563, 610-612; prefs.py:35-47) |
| `src/superclaude/cli/observe/snapshot.schema.json` | output contract, not a setting | schemaVersion const 1; closed schema (snapshot.schema.json:3-9) |
| `.dev/design/orca-observer-20261106/requirements.txt` | package renderer dependencies | `Pillow==13.0.0`, `wcwidth==0.9.4`; font path `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` read at import (render.py:16-18; existence on this host [UNVERIFIED], U-27) |
| `.gitignore:255-256` | keeps sweep reports untracked | `.dev/sweeps/` |

Observer and sweep have no configuration file; they take flags and environment only.

### 9.2 Environment Variables

| Variable | Purpose | Default | Required |
|---|---|---|---|
| `ORCA_CLI_COMMAND` | sweep binary name; value unvalidated (probes.py:214-216) | `orca-ide` | No |
| `XDG_STATE_HOME` | observer state dir `<it>/superclaude/observe` when absolute (export.py:236-244); sweep ccsession tab map `<it or ~/.local/state>/ccsession/orca-tabs` (probes.py:871) | `~/.local/state` | No |
| `NO_COLOR`, `COLORTERM`, `TERM` | observer colour policy: `NO_COLOR` non-empty disables colour; truecolor/24bit, `*256color`, else standard; dumb gives none (terminal.py:92-116). Design `--show` tests only presence of `NO_COLOR` (render.py:129) | unset | No |
| `AWR_ROOT` | AWR orchestrator repo root, else `orchestrator_repo` of the poll config (common.py:28-51) | unset | Yes, unless the poll config key is usable (it is not on master) |
| `AWR_HOOK_FILE`, `AWR_PROJECTS` | AWR overrides for Orca's hook file and `~/.claude/projects` | `~/.config/orca/agent-hooks/last-status.json`, `~/.claude/projects` | No |
| `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` | ClickUp reads and the DM | unset | token Yes for ClickUp; workspace id No (SKILL.md:37) |
| `ORCA_TERMINAL_HANDLE`, `CLAUDE_TOPIC` | read from `/proc/<pid>/environ` of `claude` processes to map terminals to sessions (orca_term.py:34-58) | n/a | n/a |
| `GIT_OPTIONAL_LOCKS=0` | set by the sweep in every git child env, with `--no-optional-locks` and `-c core.fsmonitor=false` (probes.py:331-340) | set by code | n/a |

### 9.3 Feature Flags (CLI flags and gate constants)

| Flag | Description | Default | Impact When Toggled |
|---|---|---|---|
| observer `--once`, `--width {160,116,80}`, `--ascii`, `--fixture <name>`, `--snapshot <file>`, `--run <id>`, `--questions` | one click group, seven flags | defaults, exit codes and rules in 5.2 (command surface and exit codes) | `--questions` needs `--run` and a live source (exit 2 otherwise); fixture runs write no snapshot unless `--snapshot` is given |
| `QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED` (commands.py:67, 70) | gates for the question read and the Decision Desk link | both `True` on 61ac2c2e6; tests pin True only with a cited record (test_commands.py:754-779) | False: `--questions` exits 1 with no Orca call, not even discovery |
| sweep `run --run`, `--window`, `--root`, `--output` | Run ids (repeatable); look-back; checkout root; output folder | bound Run (`run-current`); `6h` (`[1-9][0-9]{0,3}[hd]`, max 720h or 30d); folder holding `.git`; `<root>/.dev/sweeps/` | output must stay under `.dev/sweeps` and not overlap input folders (exit 2) |
| sweep gate constants | `JOIN_PATH = "B"` (classify.py:40); `CHECKED_ORCA_VERSION = "1.4.245"` (report.py:23); `JSON_SCHEMA_VERSION = 1` (models.py:18) | as stated | JOIN_PATH only changes the guard cases; version mismatch prints lock risk UNVERIFIED; bump policy not stated in code (U-30) |
| AWR `run.py open daily\|hourly\|on-demand`, `waker.py morning\|hourly\|check-missed`, `check.py --links`, `page.py --open`, `refresh [--run]` | run kinds and modes | n/a | `check.py` without `--links` cannot pass the gate; `hourly` waker mode is a recorded skip (waker.py:216-220) |
| design `render.py --batch {1,2}`, `--show <slug>`, `--width N` | layout set and output folder; print one screen; its width | 1; none; 116 | `--width` ignored in export mode; batch 2 writes `agent-focus/` and rewrites ROOT `fixture.json` and `scenarios/` (render.py:42-43, 127-130) |

## 10. Error Handling & Edge Cases

### 10.1 Error Handling Patterns

| Error Category | Handling Pattern | User Experience | Recovery |
|---|---|---|---|
| Observer: `timeout`, `overrun`, `output-cap`, `spawn-error`, `exit:<n>`, `json`, `shape` (adapter.py:196-305, 409-444; parse.py:369-380) | cycle `FAILED` if on page 1, `PARTIAL` after; 10 s per call, 8 MiB (process group killed), 2 KiB stderr kept, stderr sanitized | header shows state and code; last good rows kept; `FAILED` outranks STALE | wait doubles 15, 30, 60 s; any cycle parsing a page resets to 15 s |
| Observer: `cursor-rejected`, `cursor-stalled`, `empty-page` (adapter.py:447-466) | `PARTIAL`, pages kept; `capped=True` at 5 calls | coverage shows PARTIAL or MISMATCH | next cycle |
| Observer: `not-found` (no Orca validated) | `NOT_AVAILABLE`, one result, polling thread ends (collector.py:252-270, 345-351) | "worker-list NOT AVAILABLE (no Orca CLI validated)" | restart observer |
| Observer: `consumer-fenced`, `no-active-terminal` (Orca error envelope, even at exit 0; code names [UNVERIFIED] against a live Orca) | question source `FAILED`; ledger, retained questions and backoff untouched (collector.py:290) | instruction line; read only works from the terminal holding the Run | run from that terminal; a good read recovers |
| Observer exits | 0 quit, Ctrl-C, `--once` read (a failed read is a view state, not an exit code); 1 snapshot write failure, render failure, gate False; 2 usage, `--questions` refusals, win32, no TTY; 129 SIGHUP, 143 SIGTERM (commands.py:195-269, 364-387; keys.py:115-125) | stderr text, no traceback | fix invocation |
| Sweep Orca failures | `OrcaResult.kind` ok / no_binding / unavailable / call_failed; timeout, missing binary, `runtime_unavailable`, first-call failure give `unavailable`; over 8 MiB or non-zero exit gives `call_failed` (probes.py:254-312, 369-394) | `unscanned` source rows; "What I could not determine" section; class `could not determine` | exit 0 anyway |
| Sweep git, disk, join failures | every failure maps to `unscanned` or None, never to clean or empty; unreadable transcript, ambiguous join, duplicate Dispatch rows force `could not determine` (probes.py:1021-1048; classify.py:358-366, 908-914) | notes cell names the cause | none by the tool |
| Sweep exits and publish | 0 published and JSON printed; 2 `click.UsageError` or `BindingError`; 1 `_PublishError` or any other exception, `[sweep <stage>] <msg>` (commands.py:279-288); temp file `O_EXCL`, `os.link` never overwrites, own temp removed on failure | stderr only; stdout JSON only on exit 0 | rerun; names to `-99` |
| AWR run lock and gate | open run younger than budget: skip record and `sys.exit(3)`; gate needs 7 PASS rows plus matching sha256 chain, `BLOCKED: <why>` exit 1; `clickup.py dm` re-runs the whole gate and writes `clickup-dm.json {sent:false}` when blocked; `run.py close` re-checks only `passed()` (CC-04) | stderr; no DM | fix the checks; `abandon` releases the lock |
| AWR source failures | each source degrades to `read:false`, `errors` or carried items; waker outcomes SENT / HOLD / DM_NEEDED / SKIPPED, 15 retries for `morning` only | DM to Clay on DM_NEEDED | next automation run |

### 10.2 Known Edge Cases

| Scenario | Current Behavior | Notes |
|---|---|---|
| `check --all` re-lists a handled question | listed as open while Orca returns it; "seen is not resolved" | non-consumption verified for the owner-bound reader only; non-owner read [UNVERIFIED] (U-01); burst over 100 rows may lose questions |
| Transcript tail over 256 KiB joined by path B | row forced to `could not determine` (classify.py:619-628) | five exited workers (2026-11-12 record) all exceeded it; real frequency [UNVERIFIED] (U-12) |
| Live sweeps in practice | 180 rows all `could not determine` (2026-11-12 record); issue #590: 264 sessions, 263 `could not determine`, 1 waiting | causes named: show cap 50, no contract read; recorded, not re-run [UNVERIFIED] |
| `os.link` unsupported or 99 names taken | `[sweep publish] cannot link report`, exit 1, no fallback | open item 14 |
| Entry-file reads | symlinked folder or file refused, bad JSON skipped with note, `javascript:` and `data:` URLs dropped | common.py:188-208 |
| Two exports in one second (observer) | same record file name | whole-second timestamp; records never pruned (export.py:247-250) |
| Sweep Phase 1 limits, fixture replay of the question ledger (DC-02), entry writer, `prefs.py answer <orca://session url>` (DC-01), nested `counts`, odd `topics` reply | see 14.1, 14.2 and 14.5 | not restated here |

### 10.3 Graceful Degradation

| Failure | Impact | Degraded Experience |
|---|---|---|
| Orca call failing, observer | no new rows | last good rows stay on screen and the source shows FAILED (FAILED outranks STALE); STALE shows only when the last result was OK or PARTIAL and 45 s old; question panel has its own FAILED / STALE state |
| Orca unreachable, sweep | no Orca rows | report still published; counts and "could not determine" from disk and git reads |
| GitHub or ClickUp read fails, AWR | missing items | items carried from the previous run, run-log "Not checked" lines; DM only after the gate |

## 11. Performance Characteristics

### 11.1 Performance Profile

Only measured or code-stated values; the research ran no code and measured no tool latency itself.

| Metric | Value | Measurement Method | Notes |
|---|---|---|---|
| Live worker-list sample | 100 rows per page, `total` 428, `hasMore` true; `nextAction.kind` none 86 / release 14; liveness exited 63 / unverifiable 35 / live 2 | recorded golden sample (golden-success.json; test_golden_contract.py:43-58) | no worker-list latency found; `PER_CALL_TIMEOUT` comment still says UNVERIFIED (SD-02) |
| Message read latency | about 0.2 s per call | recorded probe in RESEARCH-REPORT (not re-run) | [UNVERIFIED] here |
| Question traffic | 41 questions over about 66 h, at most 6 in one hour; synthetic steady load 181 sent and 181 retained; burst about 30 of about 415 lost | release-gates.md (QUESTION-LINK, QUESTION-OBSERVATION) | recorded results, not re-tested (U-05) |
| Sweep full-sweep fixture | 9 Orca argv: 1 worker-list, 2 task-list, 5 worker-show, 1 `worktree ps` | test_probes_allowlist.py:609-619 | argv count only, no timing; tests pin timeouts finishing under 120 s |
| Live sweep outcomes | 180 rows (5 Orca plus 175 transcript) all `could not determine`; issue #590 run: 264 sessions (recorded, not re-run [UNVERIFIED]) | task-package record 2026-11-12; issue #590 | outcome, not duration |
| AWR run budget | target "about 5 minutes and well under 1M new tokens"; time budget 120 min daily | SKILL.md:10, 97 | a target, not a measurement; no AWR timing recorded |
| Design package | `gallery.html` 15,653,280 B and `agent-focus/gallery.html` 13,952,741 B; 406 files, ZIP 14,438,526 B; 360 export files | `ls -l`, manifest | sizes read from disk; artifacts never regenerated (U-24, U-28) |

### 11.2 Performance-Critical Code (caps, budgets, intervals, timeouts)

| Area | Value | Why It Matters | Location |
|---|---|---|---|
| Observer poll | interval 15 s, cycle budget 15 s, backoff cap 60 s, join timeout 5 s; spacing is cycle time plus wait (observation) | per observer process; several observers multiply Orca load (HELP) | collector.py:28-34, 345-351 |
| Observer call caps | 5 calls per cycle (4 worker-list plus 1 message call with questions); 10 s per call; 8 MiB stdout; 2 KiB stderr; kill grace 2 s; cursor at most 2,048 bytes | bounds one cycle at 500 rows (400 with questions) | adapter.py:55-63; collector.py:32-34 |
| Observer view | STALE at 45 s monotonic; key read 0.1 s; redraw at least every 0.5 s; question retention 1,000; question window 100 rows; warnings 50 | freshness and memory bounds | view.py:33-35; commands.py:57-60; questions.py:21-22; parse.py:403-405 |
| Sweep budget | 50 worker-shows, 90 s total, 10 s per call; show cap shared across Runs; 4 byte limits marked "proposed" (DESIGN 17 item 19); Budget defaults carry no decision record (U-14) | the #590 reporter names the 50 cap as one of two causes of `could not determine` rows (cause split not measured); issue #534 comments record an owner decision of 2026-11-17 to page past the cap (read to 400 characters per comment) | probes.py:85-89, 127-208 |
| Sweep size limits | output 8 MiB (checked after the child exits, buffered; "shortcut", owner ruling 2026-11-12 D-01); contract and ledger 1 MiB; ledger search last 512 KiB; transcript tail 256 KiB; worker-list page 100; window max 720 h; cell 200 chars; names up to `-99` | memory and read bounds | probes.py:85-89, 270-290; report.py:24; commands.py:29 |
| Sweep git | 2 to 4 calls per worktree; filter pre-check before status; status skipped when a filter driver could run | safety and cost | probes.py:995-1048 |
| AWR timeouts and waits | `run_cmd` 120 s; `orca_term` default 60 s; `gh view` 30 s; git 10 s; `FRESH_OUTPUT_SECONDS` 60; wake retries 15 x 120 s = 30 min; shell wait 30 s; start wait 120 s; run-opened wait 120 s; idle waits 90 s and 30 s; page server wait about 10 s | coordinator wake path | common.py:103-113; orca_term.py:14-21; waker.py:39-42, 203-210, 278-300 |
| AWR collection limits | `gh` lists 1000; 8 repo threads; 6 activity threads; 8 events per item; first session read 24 h and 30 MB; ClickUp 200 task pages, 400 comment calls, 30 active days, 10 min overlap; max 6 attempts | cost of a daily run | collect.py:267-270; activity.py:225; sessions.py:48-49; clickup.py:40-44 |
| Design package | `exports()` writes 10 x 3 x 6 = 180 files per batch; `build_gallery` renders 19 scenarios x 10 designs x 3 widths = 570 frame pairs (1,140 Canvas builds) (derived from code, not run) | gallery size | render.py:41-124 |

### 11.3 Asset Management

| Asset Type | Count | Total Size | Loading Strategy | Location |
|---|---|---|---|---|
| Observer fixtures | 19 (10 variants, 8 golden, `question-cap-100`) | not recorded | loaded by name via `--fixture` | `src/superclaude/cli/observe/fixtures/` |
| Sweep fixtures | 20 `captured-*.json` plus `SOURCES.md` | not recorded | test only | `tests/sweep/fixtures/` |
| AWR run folders | one per run | not recorded | kept; offsets let transcripts be read incrementally | `.dev/coordinator/runs/` |
| Design package | 406 files, 20 designs, 18 scenarios, 360 exports, 2 galleries, 2 PDFs | ZIP 14,438,526 B | offline, self-contained gallery; same content on master via PR #503 | `.dev/design/orca-observer-20261106/` |

Extension and test tasks for these sections: see Section 13.

