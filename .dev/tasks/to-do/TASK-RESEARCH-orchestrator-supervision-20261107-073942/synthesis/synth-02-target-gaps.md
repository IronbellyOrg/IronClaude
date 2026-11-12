# Synthesis 02: Target State and Gap Analysis (Orchestrator mode, #339 Phase 1)

**Task:** TASK-RESEARCH-orchestrator-supervision-20261107-073942 (Phase 5, checklist item 210)
**Date:** 2026-11-07
**Sections:** `## 3. Target State`, `## 4. Gap Analysis`
**Inputs read (offset/limit reads only):** `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `gaps-and-questions.md`, `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md`. Also read for context: `research/research-notes.md` Section C (`:186-221`, the canonical class vocabulary that every assigned file cites) and `qa/qa-nb4-fix-log.md`.
**State of the inputs at synthesis:** NB-4 is fixed. The `scope-03:99` default Orca read allowlist now includes `orchestration task-list`, `run-list`, `run-current` and `gate-list`, and `inbox` stays forbidden (`qa/qa-nb4-fix-log.md` edits 1-2). `gaps-and-questions.md:26` marks GQ-03 resolved, and its summary line `:125` reads Open 75 / Resolved 25 with no open blocking QA finding.
**Tag convention:** [CODE-VERIFIED] claims are stated as current architecture. [CODE-CONTRADICTED] claims are corrected in place. [UNVERIFIED] claims are marked "-> Open Questions" and are never stated as fact. Web findings are marked **External context** and give their URLs.

---

## 3. Target State

### 3.1 Desired behavior

- **One read-only, coordinator-only command.** `/sc:sweep` is the command file `src/superclaude/commands/sweep.md` (`name: sweep`), backed by the skill `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (`name: sc:sweep-protocol`) and a Python CLI group `superclaude sweep` (option A1). Source: `research-notes.md:157`; naming per `scope-03:129`. Today neither `commands/sweep.md` nor any `sweep`/`close` command exists [CODE-VERIFIED] (`scope-01:74`, `scope-03:129`).
- **How the skill calls the CLI.** It calls the installed entry point `superclaude sweep ...` on PATH first. Inside a dev checkout, when `command -v superclaude` finds nothing, it falls back to `uv run superclaude sweep ...`. `allowed-tools` lists both `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)` (B-19, NB-3; `scope-03:208-209`). Precedent: `sc-reflect-protocol/SKILL.md:63-64` [CODE-VERIFIED].
- **Code split.** A pure classifier module with no subprocess calls, plus one subprocess-owning module whose Orca calls all go through a single `_orca(*args)` seam modelled on `reflect/config.py:64-78`. Precedent: `reflect/contract.py:7` and `scope-03:210` [CODE-VERIFIED for the precedent].
- **Data sources.** Only the sources below, all read-only (`research-notes.md` Section B; `scope-03:99` after NB-4):

| Source | Feeds | Read form |
|---|---|---|
| `orca-ide orchestration worker-list --include-remote --json --run <id>`, paged on `page.nextCursor` (max 100 per page) | Dispatch ids and the envelope only (G-A) | plain read |
| `orca-ide orchestration worker-show --dispatch <id> --json` (one call per row) | `projection.{outcome, liveness, resource.terminalState, nextAction}`, `observation.agentWait`, `terminal.worktreePath`, `parent` | plain read; `lc16-show-4.json:127-185` [CODE-VERIFIED] |
| `orca-ide orchestration worker-read --source transcript` | latest turn; stall proof only when the turn is proved final | plain read |
| `orca-ide orchestration task-list --ready` / `--run <id>` | waiting on a person, kind (b): a foreign ready Task | plain read, `task-handlers.js:32-44` [CODE-VERIFIED] |
| `orca-ide orchestration run-list`, `run-current` | Run ids, Owner column | plain read, `run-handlers.js:28-48` [CODE-VERIFIED] |
| `orca-ide orchestration gate-list` | Approval candidate (the value mapping is [UNVERIFIED] -> Open Questions, GQ-34) | plain read, `gate-handlers.js:26-37` [CODE-VERIFIED] |
| `worktree ps` **without** `--agent-wait` | peer and person-started sessions | plain read |
| `<report-dir>/return-contract.yaml` (WC-4) | `worker_status`, `blocked_question`, `report_path` | file read |
| `.dev/tasks/*/progress.md`, sprint `results/`, `.roadmap-state.json`, MDTM frontmatter | unfinished ledgers (refusal condition 4) | file read |
| `git -C <worktree>` limited to status, log, branch and rev-parse | the five refusal conditions at `WORKER-CONTRACT.md:108` | read-only git |
| `~/.local/state/ccsession/orca-tabs/<tabId>+<leafId>`, `~/.claude/projects/<key>/topics/*.txt`, transcript `*.jsonl` (read by tailing) | pane-key to transcript join; idle for person-started sessions | file read; join [CODE-VERIFIED] for lc16 only (C12) |

- **Classification.** Each session gets exactly one class, decided by the precedence in `research-notes.md` Section C (`:190-202`); the first rule that matches wins:

```
 per session
   |
   1 contract read first -- worker_status: blocked -----------> waiting on a person (a)
   2 exited / exit observed / turn PROVED final, no worker_done,
     no consumer_fenced evidence ------------------------------> stalled (proved)
   3 consumer_fenced evidence (WC-12) -------------------------> fenced
   4 non-null agentWait | frozen plan | Ruling halt |
     foreign ready Task (task-list --ready) -------------------> waiting on a person (a)/(b)
   5 live + in_progress + agentWait null ----------------------> working
   6 settled + contract read (succeeded|partial|failed),
     or a "guard refused:" body --------------------------------> finished
   7 everything else (unverifiable, agentWait absent, stale,
     Orca down, late heartbeat only, turn not proved final,
     row truncated at 100) -------------------------------------> could not determine
   person-started session, no Task, no activity in window ----> idle
```

| Class | Rule | Maps the issue's term | Never derived from |
|---|---|---|---|
| waiting on a person | 1 or 4: (a) explicit question, or (b) frozen or blocked by policy | needs-person | a pending `ask` (no read path, G-B) |
| working | 5 | (healthy) | `stage.activity` [CODE-CONTRADICTED] |
| stalled (proved) | 2: positive stop proof only | stuck | a late heartbeat (WC-10), `unverifiable` |
| finished | 6: Orca settled **and** contract read | finished | Orca `outcome` alone (WC-5 shows blocked as `failed`) |
| could not determine | 7 | timed out (reported as absence, never death) | - |
| idle | person-started sessions only | idle | any Orca row |
| fenced | 3 | (none; ends without `worker_done` by design) | - |

- **Contradiction: six classes or seven.** The research question lists six classes. Section C, the canonical vocabulary (C14, B-28; `research-notes.md:188`), defines seven: it adds **fenced** (rule 3). The stronger evidence is Section C, because it rests on WC-12 (`WORKER-CONTRACT.md:60`) [CODE-VERIFIED]: a fenced worker ends without `worker_done` by design, so it must be neither stalled nor finished. Target: keep fenced as its own row. If the owner holds to six classes, fenced must fold into "could not determine", never into stalled -> Open Questions.
- **Safe to close is a separate dimension, never a class.** It is a per-row REVIEW recommendation in two independent parts, printed and never executed (B-02, GQ-68; `research-notes.md:216-219`):
  - **Terminal releasable:** `resource.terminalState` is `reclaimable` and `nextAction` is `release`, and the session's result has already been read.
  - **Worktree removable:** all five refusal conditions at `WORKER-CONTRACT.md:108` are false (no unmerged commits, no open PR, no uncommitted changes, no unfinished `/sc:implement` ledger, no unread report), and no freeze applies (`:133-136`).
  - A class is never derived from `resource.terminalState` (`research-notes.md:204`).
- **Window.** The default window is 6 h and bounds session-log and artifact **activity only**. An open Orca Task, a pending question or an unread report is listed whatever its age, so "kept until answered" holds (`research-notes.md:221`; N-41). The 72 h default belongs to crash-recovery (`sc-crash-recovery/SKILL.md:26`) and is not adopted. The owner decision is still open: GQ-61.
- **Report.** The sweep writes one dated static Markdown file on the #409 layout, pinned to commit `495eb96d` (#409 is unmerged; GQ-35). The file is local only and never posted (git ownership, `WORKER-CONTRACT.md:112`, `:114`). It goes under `.dev/` (WC-11, `:46`); the exact directory is an owner decision (GQ-10). The skeleton is DERIVED (`scope-04:268-308`):

```
# Orchestrator sweep: <worktree-tree root>
READ ONLY . observed <real UTC time>          <- #409 hardcodes its clock (canvas.py:73-77)
Scope: owners / sessions / mapped worktrees
Sources: <source> <coverage> <age> | ...      <- "Messages coverage: partial" (G-B)
## Waiting on a person: explicit questions (a)   oldest first; unknown age in a labelled group
## Waiting on a person: frozen or blocked by policy (b)   no question text, ever
## Retained problems   failed / stale / policy frozen; plus stalled (proved), could not determine
## Sessions (<shown>/<total>)   10 #409 dimensions + derived Class + safe-to-close REVIEW
## Worktrees (<shown>/<total>)
## Historical sessions
Inspection only. ...                             <- footer (canvas.py:81)
```

- **Report rules** (`scope-04:316-351`; External context below):
  - Dimensions stay independent columns, and the class is one extra derived column that never overwrites a dimension.
  - Unknown values print "unknown"; missing results print "not observed".
  - The waiting list is sorted oldest first by the time since the wait began, the question's "original age" (`scope-04:87`) (#409 documents the sort but its code does not sort: C6). Rows with an unknown age go in a labelled group, never at age 0.
  - Every bounded list prints `<shown>/<total>` (#409's wide views omit it: C7). A source truncated at 100 rows prints "at least 100 (truncated at 100), total could not determine".
  - "Answered: could not determine" and "Seen is not resolved".
- **WC-14 coordinator-loop rule.** Add a new `### WC-14. Coordinator loop` to `src/superclaude/core/WORKER-CONTRACT.md`. Insert it after the fan-in rule ends at `:156` and before `### Worked example` at `:158`, or else after `:129` and before `:131` (`scope-01:78`) [CODE-VERIFIED insertion points]. It states:
  1. **G1:** the coordinator keeps polling until every Task it created is settled and read. Cite the owner order of 2026-11-05 (N-30).
  2. **G2:** an expired wait is re-armed, never treated as done.
  3. **G3:** the periodic read-only sweep and its cadence.
  4. **G4:** the session classes, by reference to WC-10, WC-6 and `:108`.
  5. **G5:** one list of the "tell the person" triggers at `:126`, `:127`, `:129`, `:134` and `:156`, with each item kept in the report until answered.
  6. **G6:** whether person-started sessions are reported at all (owner decision).
  7. **G7:** the report is a dated local file under `.dev/`, never posted.
  8. The sweep performs none of the actions at `:74` (stop/cancel), `:107` (merge/remove) or WC-6 (new Task); it only recommends them (`scope-01:86`).

  WC-14 should contain no runnable code spans (`_check_repo_setup_gated`, `test_worker_contract.py:446`). "WC-14" is a working name; WC-14 versus amending WC-1 is open (GQ-11).
- **Recommendations only.** A resume recommendation for an Orca worker is phrased as "new Task" (WC-6, `WORKER-CONTRACT.md:70`, `:73`) and is never offered on `unverifiable`. A non-null worker-show `parent` is reported as a WC-13 violation for review (`:39`, `:61`).
- **Orca unavailable.** The sweep prints an "Orca unavailable" banner, falls back to reading contracts only, and never runs `orca open` (`scope-02` failure-mode table; `orca-capabilities.md:39`).

### 3.2 Success criteria

| # | Criterion | How it is checked | Source |
|---|---|---|---|
| SC-1 | No local write except the report | Patch the forbidden entry points with `side_effect=AssertionError(...)`; run inside `CliRunner.isolated_filesystem()` | `tests/cli/reflect/test_contract_status_cli.py:44-66` pattern (`scope-03:99`) [CODE-VERIFIED] |
| SC-2 | No Orca call outside the allowlist | Patch the `_orca(*args)` seam and assert every argv against the default allowlist. The test fails on `check` (while the probe is unsettled), `--ack`, `--wait`, `--unread`, `--format`, `reply`, `ask`, `send`, `inbox` or `worktree ps --agent-wait` | `scope-03:99` (NB-2, NB-4) |
| SC-3 | Argv uses the full verb form | Every pinned argv is `orca-ide orchestration <verb>` | C13 [CODE-VERIFIED]; GQ-85 |
| SC-4 | Classification is deterministic and follows the precedence | Unit tests with mocked rows, one per rule 1-7 plus idle, including fenced-with-exited, `agentWait` null vs absent, and guard-refused | `research-notes.md:190-202`; seed brief "mock-testable" (`research-notes.md:229`) |
| SC-5 | Absence never reads as death | A late heartbeat, `unverifiable` or a missing row gives could not determine; no test path yields stalled without stop proof | WC-10 `WORKER-CONTRACT.md:45` [CODE-VERIFIED] |
| SC-6 | Every class has a report home | The Sessions table Class column carries every class; stalled (proved) and could not determine also appear under Retained problems | `scope-04:332` |
| SC-7 | Kept until answered | A fixture with an open Task older than 6 h is still listed | `research-notes.md:221`; N-41 |
| SC-8 | Honest counts | `<shown>/<total>` on every list; a 100-row result prints "truncated at 100" as could not determine | `scope-04:292`; GQ-48 |
| SC-9 | Real observation time in the header; "Messages coverage: partial" | Static check on the rendered report | `scope-04:270`, `:276`; web-02 recommendation 1 |
| SC-10 | CLI registered | `main.add_command(sweep_group, name="sweep")` after the pattern at `main.py:559-561`; a `CliRunner` `--help` test | `scope-03:135`, `:141` [CODE-VERIFIED] |
| SC-11 | Routing registries updated | `_POST_REFRESH_ADDITIONS` gains `"sweep"` (`test_routing_refresh.py:33`); HOW-WE-WORK "Other commands" row (`:318-337`, ASCII only); `_OTHER_COMMANDS` gains `"sc:sweep"` (`test_how_we_work_routing_table.py:27-40`); plugin byte copy (`test_routing_plugin_parity.py:38`), unless GQ-24 places sweep in the excluded set | `scope-03:136-139` [CODE-VERIFIED] |
| SC-12 | Contract tests pin WC-14 | `RULE_PHRASES` gains a WC-14 entry (`test_worker_contract.py`, under the comment at `:163`); `/sc:sweep` joins `NEVER_AS_WORKER` (`:245-254`, 8 entries; the test name says "all seven", N-34) and the phrase at `:86-92` | `scope-01` test-pinning section |
| SC-13 | `make lint` passes | lint-architecture Checks 1, 2, 3/4, 6, 8, 9 and 11 (`Makefile:362-489`); the SKILL.md `name:` ends in `-protocol`; no contract constants re-declared under `cli/` | `scope-03:143-150` [CODE-VERIFIED] |
| SC-14 | Suite-wide scans pass | `test_model_alias_policy.py:81-100`; `test_graph_command.py:219-225`; the AC-0.9 write-verb audit over `AUDIT_ROOTS` (`test_worker_contract.py:1090-1094`); no `## Unattended mode` section | `scope-03:152-157` [CODE-VERIFIED] |
| SC-15 | `make verify-sync` clean | `src/superclaude/` edited first, then `make sync-dev` | CLAUDE.md component sync; `scope-03:163` |
| SC-16 | PATH form works under pipx | Run `superclaude sweep --help` once from a project that is not a uv project; a static test pins bare form first and both forms in `allowed-tools` | `scope-03:208` (GQ-25; [UNVERIFIED] until run -> Open Questions) |

### 3.3 Constraints

| Constraint | Rule | Evidence |
|---|---|---|
| Read-only | No stop, cancel, merge, remove, Task creation, `orca open`, `check` (any mode, until the probe settles Gaps 1, 2 and 18), `inbox`, `--agent-wait`, `ccsession --list` (it writes: `ensure_names_migrated`, `ccsession:285-287`), or `git stash` beyond `list` | `scope-03:99`; `research-notes.md:178-182`; `06:158-175` |
| Coordinator-only | `/sc:sweep` is never run as a worker; it joins the never-as-worker list at `WORKER-CONTRACT.md:23` | `scope-01:80` (G3) |
| WC-10 | A missing heartbeat is absence, never death; the coordinator acts only on Orca's stall proofs | `WORKER-CONTRACT.md:45` [CODE-VERIFIED] |
| WC-6 | A retry is a new Task, never `--retry-of`, and never on `unverifiable`. `[G:recovery]` row 9 conflicts with this; WC-6 wins (GQ-98) | `WORKER-CONTRACT.md:70`, `:73`, `:74` [CODE-VERIFIED] |
| WC-12 | A fenced worker ends without `worker_done`; rule 2 excludes fenced evidence | `WORKER-CONTRACT.md:60` [CODE-VERIFIED] |
| WC-3 / WC-5 | A worker blocked in `ask` sends no heartbeat; Orca shows blocked and failed alike as `failed`, so the contract is read first | `WORKER-CONTRACT.md:54-58` [CODE-VERIFIED] |
| WC-13 | No fan-out; a non-null `parent` is a violation to report | `WORKER-CONTRACT.md:39`, `:61` |
| WC-11 and git ownership | The report is a local file under `.dev/`; a post is an outward action needing the person's instruction | `WORKER-CONTRACT.md:46`, `:112`, `:114` [CODE-VERIFIED] |
| Freeze and cleanup refusal | A frozen plan is "waiting on a person", never safe to close; the five refusal conditions gate "worktree removable" | `WORKER-CONTRACT.md:108`, `:133-136` [CODE-VERIFIED] |
| No new store, extend the contract | No new protocol or database; the report is the only output | `research-notes.md:229` (seed brief `:53-59`) |
| Signals excluded | `stage.activity` (stays "working" after settlement, C5), `resource.terminalState` as a class input, heartbeat age as stall proof | `lc17-show-1.json:132`; `research-notes.md:204` |
| Later phases, recorded only | `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay (GQ-66) are out of Phase 1 | research question |
| Option A4 rejected | Extending `sc-crash-recovery` is [CODE-CONTRADICTED]: `Bash(git stash *)` in allowed-tools (`SKILL.md:4`), `~/workspace/` paths where this host uses `~/workspaces/` (`:25-27`), 72 h default, and `bootstrap_scan.sh` bugs at `:31` (encoding), `:73` (`.git` is a file in a worktree) and `:136` (JSON escaping). Its SAFE/REVIEW vocabulary and report shape may be reused without its scripts | `research-notes.md:160-162`; `scope-02:131-146` |

**External context (supports the constraints; the codebase rules govern):**

| Finding | Effect on the target | URL |
|---|---|---|
| Kubernetes `Ready=Unknown` is distinct from `False`; OTP restarts on an exit signal; Pekko's phi detector says a suspect can come back. All independently support WC-10 (web-01 findings 1-2) | could not determine is a first-class class | https://kubernetes.io/docs/reference/node/node-status/ ; https://www.erlang.org/doc/system/sup_princ.html ; https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html |
| gRPC `UNKNOWN` vs `SERVICE_UNKNOWN`; Nagios UNKNOWN as a broken check (web-01 recommendation 1) | Split could-not-determine causes: evidence absent vs source unreadable | https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto ; https://nagios-plugins.org/doc/guidelines.html |
| Camunda excludes waiting for outside input from time budgets (web-01 finding 4) | Waiting on a person is healthy; exclude person-wait time from activity ages and the 6 h activity window (the waiting list still sorts on time since the wait began) | https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ |
| Harmonograf labels a progress-free run "stuck" (web-01 D3) | Heuristics are a note column only, never the stalled class | https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md |
| Kubernetes eviction after Unknown; liveness probe restarts (web-01 D1, D4) | Rejected for Phase 1 (WC-10; no action) | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ ; https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ |
| Icinga 2 UNKNOWN = "could not determine the service's state"; a probe timeout reports UNKNOWN (web-02) | A probe timeout maps to could not determine | https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/ |
| Statuspage keeps component state, incident lifecycle and impact as separate fields (web-02) | Safe to close stays a separate dimension | https://support.atlassian.com/statuspage/docs/top-level-status-and-incident-impact-calculations |
| Grafana lets missing data map to firing or OK, and an evicted series can look resolved (web-02) | **Contradicts WC-10; rejected.** A row that drops out of a listing is never "finished" | https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ |
| Kanban Work Item Age; `gh issue list` "Showing 30 of 624" (web-02) | Oldest first with an unknown-age group; `shown/total`, with an "at least N" form when the total is unknown (an extension of #409) | https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf ; https://github.com/cli/cli/issues/12196 |
| I-PASS action list with owner, "watcher" state and if-then contingency; PagerDuty "next update" (web-02) | Optional text-only "what to check next" line per waiting item; the header gives the observation time | https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html ; https://docs.pagerduty.com/ops-guides/incident-response-guide/incident-commander |

Excluded from the target, with reason: phi-accrual and progress-counter scores (web-01 recommendation 6: Orca exposes no heartbeat history, GQ-17); OTP-style restart budgets (web-01 recommendation 5: later phase only).

---

## 4. Gap Analysis

### 4.1 Severity rules

| Rule | Statement |
|---|---|
| R-1 Source severity | A row keeps the severity its source gives. G1-G7 follow N-32. B- and NB- findings are Important. Open questions that the sources call non-blocking are Minor (`gaps-and-questions.md:20`). |
| R-2 Unwired in-scope capability | **An in-scope Phase 1 capability that is designed but not wired into code, contract text, tests and registries is a defect rated Critical.** It is never retired as "future work" unless a scope decision is cited. The rule applies to the `/sc:sweep` command, skill and CLI (G3), the Section C classifier (G4), WC-14 and its clauses (G1, G2, G5), the static report writer, the read-only proof tests and the registries. For these rows R-2 wins over R-1: the row is rated Critical until wired, and the source severity is kept in the Severity cell for reference. G7 is not in this list: the report location is an owner decision (GQ-10), and the writer it governs is the separate Static report writer row. It does not apply to items the research question puts in later phases: `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay. Those are recorded only, and the research question is their cited scope decision. |
| R-3 Rows without a source severity | [CODE-CONTRADICTED] and [STALE DOC] rows have no source severity. They are rated **Important** when the wrong claim would change the Phase 1 design or a test (for example the read-only claims C3 and scope-02:165), and **Minor** when they are wording, line numbers or counts. Each row states its basis. |

### 4.2 Core gaps (G-A, G-B, G1-G7, and the Phase 1 build)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| G-A (GQ-01): `worker-list` row schema | No populated row has been captured (`lc01-step7.txt:28` is `[]`), so the row's fields are [UNVERIFIED] (C10). `agentWait` is not inside `projection` (`lc16-show-4.json:180,185`) [CODE-VERIFIED] | Use only the list envelope and the Dispatch id, then call `worker-show --dispatch <id> --json` once per row. Page on `page.nextCursor`. Worst case is ceil(N/100) list calls plus N show calls (05 `:165`, Gap 1 `:186`) | Critical | Open, partly answered. Closes only with a live `worker-list --run <id> --json` capture -> Open Questions. N-29 suggests downgrading once the fallback is accepted. The call count versus the batching policy is GQ-99. |
| G-B (GQ-02): no non-consuming read of pending questions | Every `check` mode goes through `callOrchestrationMutation` (`message-check-handler.js:30`). `inbox` read-marking is [UNVERIFIED] (06 Gap 4 `:161`). No read path exists (C11) | "Waiting on a person" (a) comes from the contract fallbacks only: WC-3 `blocked_question`, a non-null `agentWait`, and the frozen-plan test at `WORKER-CONTRACT.md:133-136`. The header prints "Messages coverage: partial", and every question shows "Answered: could not determine" (06 `:77`) | Critical | Open but answered for the design. Related Orca unknowns: GQ-43, GQ-44, GQ-47, GQ-48, GQ-56, GQ-57, GQ-59 (section 4.4). |
| G1 (GQ-04): no keep-polling rule | `WORKER-CONTRACT.md` has no rule that the coordinator keeps polling (`scope-01:78`) | WC-14 clause 1. It cites the owner order of 2026-11-05 in the memory note `coordinator-never-stop-polling.md` (N-30) | Critical | R-1 (N-32) and R-2. scope-01 marks the source [UNVERIFIED]; N-30 says the note is readable. |
| G2 (GQ-05): no re-arm rule | No current text (`scope-01:79`) | WC-14 clause 2: an expired wait is re-armed, never treated as done | Critical (R-2, unwired; source severity Important, N-32) | In scope as a WC-14 clause. |
| G3 (GQ-06): no periodic sweep | No `commands/sweep.md`, no `sc-sweep-protocol` skill and no `sweep` CLI group exist (`scope-01:74`, `scope-03:129`) [CODE-VERIFIED] | Option A1: `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, a `superclaude sweep` Click group registered after `main.py:559-561`, and the cadence stated in WC-14 clause 3 | Critical | This is the feature itself. A2 is not deterministic. A3 cannot import package code. A4 is rejected (section 3.3). |
| G4 (GQ-07): no classification vocabulary | Resolved on paper: `research-notes.md` Section C (`:188-204`) is the one canonical vocabulary (C14, B-01, B-28). No code implements it | A pure classifier module with no subprocess calls that applies rules 1-7 and idle in precedence order, with unit tests per rule (SC-4) | Critical (R-2, unwired) | The source gap is resolved, but the capability is not built. Six classes versus seven: section 4.8. |
| G5 (GQ-08): no rule for when to tell the person | The triggers are spread across `WORKER-CONTRACT.md:126`, `:127`, `:129`, `:134` and `:156` (`scope-01:82`) | WC-14 clause 5: one list, with each item kept in the report until answered | Critical (R-2, unwired; source severity Important, N-32) | Design decision for the plan. |
| G6 (GQ-09): person-started sessions | No rule. The evidence route (pane-key join) is [CODE-VERIFIED] for one worker, lc16 (C12) | An owner decision on whether to report them at all. If yes, `idle` applies only to these sessions | Important (N-32) | Retiring G6 needs the owner's decision cited (R-2). Overlaps AMBIGUITY 8 and GQ-18. |
| G7 (GQ-10): report location | No source fixes a location | A dated local file under `.dev/` (WC-11 `:46`), never posted (`:112`, `:114`). The exact directory is an owner decision | Important (N-32; R-1, outside R-2's list) | The writer itself is Critical (next row); only the directory is a decision. |
| Static report writer | The #409 layout exists only at unmerged commit `495eb96d` (GQ-35), and it hardcodes its clock (`canvas.py:73-77`). No static writer exists | A writer for the skeleton in section 3.1: real observation time, waiting kinds (a) and (b), Retained problems, Sessions with 10 dimensions plus a derived Class column, Worktrees, Historical, the footer, and `shown/total` | Critical (R-2) | Column sources are at `scope-04:336-351`. Layout questions are GQ-29 to GQ-35. |
| Read-only proof tests | No sweep tests exist. Patterns exist: `test_contract_status_cli.py:44-66` and the `reflect/config.py:64-78` seam | SC-1 (no local write), SC-2 (`_orca(*args)` argv allowlist), SC-3 (full verb form) | Critical (R-2) | Designed in B-13/NB-2/NB-4 (`scope-03:99`). Without these tests the read-only claim is unproven. |
| Registries and suite gates | No sweep entry is registered (`scope-03:129`) | SC-10 to SC-15: `main.py`, `_POST_REFRESH_ADDITIONS`, HOW-WE-WORK "Other commands", `_OTHER_COMMANDS`, plugin byte copy, commands.md UTILITIES, `NEVER_AS_WORKER`, `RULE_PHRASES`, lint-architecture, `make verify-sync` | Critical (R-2) | Placement choices are GQ-12, GQ-24 and GQ-28. `NEVER_AS_WORKER` has 8 entries but its test is named for seven (N-34). |

### 4.3 The four known non-critical gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| K1 (GQ-18): pane-key to transcript join | [CODE-VERIFIED] for lc16. Replacing `:` with `+` in `assigneePaneKey` gives the orca-tabs file name, and that file's line 3 is the `assigneeHandle` (`lc16-show-4.json:11-12`) | Used only if G6 is approved | Important (`research-notes.md:273`) | One worker only, so the plan checks a second worker -> Open Questions. |
| K2 (GQ-19): fix `bootstrap_scan.sh` or write a new scanner | `sc-crash-recovery/scripts/bootstrap_scan.sh` has bugs at `:31` (encoding), `:73` (treats `.git` as a directory, which fails in a worktree) and `:136` (JSON escaping) | Write new read-only Python in the sweep CLI. Running `bootstrap_scan.sh` as it is stays excluded (`research-notes.md` Section B) | Important | A plan decision. A4 is [CODE-CONTRADICTED], so nothing builds on it. |
| K3 (GQ-25): `uv run superclaude` outside a uv project | Decision B-19 is made: PATH form first, `uv run` fallback, both forms in `allowed-tools` | SC-16: a runtime check from a non-uv project plus a static test of the order | Important | Pipx PATH behaviour is [UNVERIFIED] -> Open Questions. |
| K4 (GQ-23): lazy or eager start of the Orca client | Both patterns exist: lazy `__getattr__` at `recommend/__init__.py:12-20` and eager imports at `reflect/__init__.py:17-30` | Lazy, as `scope-03` OQ1 recommends | Important | A plan decision. The seam location is GQ-27. |

### 4.4 Other open gaps (Orca behaviour, plan and owner decisions, #409 layout, wording)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| GQ-37: `unverifiable` and `exited` never captured | Their meanings and the six reason codes come from guide text only (`[G:recovery]` 34-38, 58-59) | Rules 2 and 7 are tested against a live stalled-row capture | Important | N-29. -> Open Questions. |
| GQ-58: null `agentWait`, help versus guide | `[H:worker-show]:16` reads "looked and found no wait"; `[G:recovery]:58-61` reads "same absence seen again" (06 `:144` is CC by help) | null = no wait observed, which is valid for working and never stall proof; absent = could not determine | Important | B-10. Contradiction in section 4.8. |
| GQ-40: nested workers (C15) | Guide `[G]` 130-131 says workers start helpers; `orca-capabilities.md:97-102` says depth 1 forbids it | The sweep reports a non-null `parent` (`lc16-show-4.json:115`) as a WC-13 violation for review | Important | Orca behaviour is [UNVERIFIED]; the sweep-side rule is settled. |
| GQ-43: does plain `check` mark rows read | Every check goes through `callOrchestrationMutation` (`message-check-handler.js:30`) | Plain `check` is forbidden | Important | [UNVERIFIED]. |
| GQ-44, GQ-57 and GQ-59: `check --peek` / `--all` side effects; `ackMessageIds`; runtime probe | Not side-effect-free by construction: older runtimes ignore `--peek` (`:17`), and both modes can trigger `compatibilityAck` (`:58-71`). No read-only version verb was found | Default is contracts only. `check --peek` / `--all` become a separate addition, gated on a probe | Important | `scope-03:99` (NB-2). |
| GQ-48 and GQ-56: enumeration past 100 rows; `check --all` `run:<id>` rows | `--all` and Run `--peek` cap at 100 with no cursor (`[H:check]:37`); older runtimes keep the newest 100 (`message-check-handler.js:82-83`) | A 100-row result reports "could not determine: message listing truncated at 100" | Important | B-18. |
| GQ-60: where the logic lives (AMBIGUITY 1) | Open, leaning A1 | A1 (section 3.1) | Important | A4 [CODE-CONTRADICTED] (`research-notes.md:160`). |
| GQ-61: window 6 h or 72 h (AMBIGUITY 2) | Open owner decision | 6 h default bounding activity only; open Tasks, questions and unread reports are always listed | Important | N-41. The research question fixes 6 h, but the owner decision is still recorded as open. |
| GQ-63: `pragmatic` DONE/NEXT "No exceptions" | `pragmatic.md:22`, `:53` give no exception mechanism; `launch-job-identity.sh` sets no environment variable | Owner decision on how a sweep report is exempted, if at all | Important | B-04 is resolved as evidence; the decision stays open. |
| GQ-21: exclude `git stash *` and `ccsession --list` | crash-recovery allows `Bash(git stash *)` (`SKILL.md:4`), and `ccsession --list` writes (`ensure_names_migrated`) | Both are excluded from the sweep's allowed-tools and code | Important | C3 and scope-02:165. |
| GQ-15, GQ-16, GQ-17, GQ-22, GQ-36, GQ-38, GQ-39, GQ-41: Orca field and shape unknowns | `liveness.reason` values, `runtime_unavailable` shape, whether heartbeat age feeds liveness, the cost of `--include-remote`, the non-null `agentWait` shape, `page.hasMore` past 100 rows, `counts` keys and the capture CLI version are all [UNVERIFIED] | The classifier treats each unknown as could not determine, never as stalled | Minor | -> Open Questions. |
| GQ-46, GQ-47, GQ-49 to GQ-54, GQ-64, GQ-65: Orca read and identity unknowns | `inbox` read-marking, `reply` effect, `--dispatch-capability`, peer `ask --to run:<id>`, whether the `--agent-wait` probe writes, `agentWait` while blocked in `ask`, missing `caller`, cross-host joins, whether `identify` writes, `task-list` / `gate-list` caps: all [UNVERIFIED] | `inbox` and `--agent-wait` stay forbidden. "Answered: could not determine". Unknown caps print `shown/total` or "at least N" | Minor | N-35: a pending `ask` waits on the coordinator, not a person. |
| GQ-11, GQ-12, GQ-14, GQ-24, GQ-26, GQ-27, GQ-28: rule id and registry placement | WC-14 versus WC-1; never-as-worker test changes; whether a test requires help or HOW-WE-WORK registration; "Other commands" versus the excluded set (also the routing-table option, N-37); how `allowed-tools` patterns combine; probe module location; whether a test pins UTILITIES | Decided in the plan, with each decision cited | Minor | GQ-14, GQ-26 and GQ-28 are [UNVERIFIED]. |
| GQ-29 to GQ-35: #409 layout | Sort tie-break, closure evidence, per-source coverage, scope line, omission bound, Approval label and its `gate-list` mapping ([UNVERIFIED]), pinning to unmerged `495eb96d` | Plan decisions inside the skeleton in section 3.1 | Minor | C6 and C7 apply. |
| GQ-62, GQ-66, GQ-67, GQ-100: sequencing and owner clarifications | PR #422 sequencing; meaning of "management server"; worktree-first versus trigger-based placement (CR-01 unread); APPROVED.md texts unverified | Owner decisions. The management-server relay is a later phase, recorded only | Minor | R-2 does not apply because these are outside Phase 1 or are decisions. |
| GQ-84: fenced exclusion with an unreadable transcript | Rule 2 fires before rule 7 | The plan states: exited, no `worker_done` and an unreadable transcript give could not determine | Minor | Not a WC-10 break. |
| GQ-85: mixed verb forms at `scope-03:99` | Bare `worker-list` next to full `orchestration <verb>` | Every pinned argv is `orca-ide orchestration <verb>` (C13) | Minor | `qa-nb4-fix-log.md:41`. |
| GQ-86 to GQ-95, GQ-97: wording and citation residuals | `--unread` versus `--unread --peek` wording; `scope-01:64` "class"; 06 `:57-58` tags; stale 06 `:187`; `filterLegacyPeekResult` runs on every peek; `scope-04:290` and `:320`; "needs a human" at `research-notes.md:225` and `scope-04:356`; G-A versus G-B at `research-notes.md:175`, `:196`; MISSING list at `:241-242`; a default stated as fact at `05:165` and `scope-01:142`; small citations | The canonical terms from Section C apply in the final report | Minor | No design effect. |
| GQ-98: `[G:recovery]` row 9 `--retry-of` | The guide says to start a replacement with `--retry-of` | A new Task, never `--retry-of` (WC-6) | Minor | Contradiction in section 4.8; WC-6 wins. |
| GQ-99: N `worker-show` calls versus the batching policy | Follows from G-A's worst case | A per-sweep call bound, stated in the plan | Minor | N-40. |

### 4.5 Resolved gaps (kept for traceability)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| GQ-03 (NB-4): allowlist omitted read verbs | Fixed: `scope-03:99` now allows `task-list`, `run-list`, `run-current` and `gate-list`, and `inbox` stays forbidden | Pinned by SC-2 | Important (resolved) | `qa/qa-nb4-fix-log.md` edits 1-3. The summary line `gaps-and-questions.md:125` now reads Open 75 / Resolved 25. |
| GQ-07, GQ-13, GQ-18, GQ-42 | Vocabulary (Section C); `AUDIT_ROOTS` scans `commands/` (`test_worker_contract.py:1090-1094`); pane-key join for lc16; other read surfaces are plain reads | Used as designed | Critical / Minor / Important / Important (resolved) | GQ-07 is still Critical as an unwired capability in 4.2 (R-2). |
| GQ-20, GQ-45, GQ-55 | `stage.activity` is never a signal (C5); `check --unread` is destructive and forbidden (`message-check-handler.js:33-34`); `--format` is a local text switch (`:38`, `:55`) | Excluded | Minor / Important / Minor (resolved) | [CODE-VERIFIED] or CC as tagged. |
| GQ-68 to GQ-83 (B-02, B-03, B-05/NB-1, B-11 to B-14/NB-2, B-20 to B-27, NB-3) | Safe to close is a dimension; full verb form; stall needs positive proof, with fenced excluded; waiting kinds (a) and (b); every class has a report home; read-only proof tests designed; missing columns added; tags fixed; suite scans listed; `--ack` claim corrected; lint gates listed; PATH-first call form | Built into sections 3.1 to 3.3 | Important (resolved) | Residuals are GQ-84 to GQ-95. |
| GQ-96: blocked `/sc:implement` fits kinds (a) and (b) | Accepted: the dimensions are independent | - | Minor (resolved) | - |

### 4.6 [CODE-CONTRADICTED] findings, corrected

| Gap | Current State (claim) | Target State (correction) | Severity | Notes |
|---|---|---|---|---|
| C1 (scope-01 `:111`, `:129-138`; research-notes `:40`) | The analysis findings are numbered F1-F12 | Use F1-F14 and S1-S5 (`analyze-worker-contract.md:30-55`) | Minor | R-3: numbering only. |
| C2 (research-notes `:31`) | `test_how_we_work_routing_table.py` is about 360 lines | 1202 lines | Minor | R-3: count only. |
| C3 (scope-02 `:131`) | sc-crash-recovery is "pure read-only" | `Bash(git stash *)` is allowed (`SKILL.md:4`) | Important | R-3: it decides A4 and GQ-21. |
| C4 (scope-02 `:132`, `:133`, `:241`; research-notes `:160`) | crash-recovery scans `~/workspace/` with a 72 h default | This host uses `~/workspaces/` (`SKILL.md:25-27`); the 72 h default is not adopted | Important | R-3: a reason A4 is rejected. |
| C5 (scope-02 `:74`; 05 `:132`, `:137`, Gap 7 `:192`; research-notes `:145`) | `stage.activity` signals work in progress | It stays "working" after settlement (`lc17-show-1.json:132`, `lc01-show-1.json:132`); use `projection.*` | Important | R-3: a classifier input. |
| C6 (scope-04 `:93`, `:368`; research-notes `:225`) | The #409 Attention Ledger is age-ranked | No sort at `agent_focus.py:46` at `495eb96d` (partial CC) | Important | R-3: the sweep must sort oldest first itself. |
| C7 (scope-04 `:247`, `:371`; research-notes `:225`) | #409 wide views carry omission counts | Absent at `agent_focus.py:46-50`, `:164-167` | Important | R-3: the sweep must add `shown/total`. |
| C9 (scope-03 `:76`; research-notes `:75`) | The recommend docstring's `python -m` usage | Against the UV rule; never copied | Minor | R-3: a docstring. |
| C13 residual (scope-02 `:16`, `:235`) | Bare `orca` command form | `orca-ide orchestration <verb>` [CODE-VERIFIED] | Important | B-03 is resolved; GQ-85 is the residual. |
| scope-02 `:146` | Bug 1: ENCODED_CWD replaces only `/` | An encoding bug in `bootstrap_scan.sh:31` | Minor | K2 (GQ-19). |
| scope-02 `:165` | `ccsession --list` is read-only | It migrates names (`ensure_names_migrated`, `ccsession:285-287`) | Important | R-3: excluded source (GQ-21). |
| scope-01 `:100` | The "41 tests" cross-reference | Tagged CC; settled by GQ-84 (M1) | Minor | R-3: count only. |
| scope-03 `:108`, `:111` | recommend.md `name:` shape; Activation uses an "identical form" | Follow `issue.md` (newest template) for frontmatter and the Activation block | Minor | R-3: template detail. |
| scope-03 `:165` | No test globs every skill | Suite-wide scans exist (`scope-03:152-157`) | Important | R-3: these are SC-14 gates (B-21). |
| scope-04 `:33` | Generated files "Not read" | Tagged CC at `scope-04:33`; open, and the sweep does not depend on it | Minor | R-3: process note. |
| 06 `:63`, `:85` | `--format` help is self-contradictory | `--format` is a local text switch (GQ-55); forbidden | Minor | R-3: verb is not used. |
| 06 `:144` (CC by help) | A null `agentWait` means the same absence seen again | Help says looked and found no wait; see GQ-58 | Important | R-3: a classifier input. |
| Option A4 (research-notes `:160`; scope-02 `:241`) | Extend sc-crash-recovery | Rejected; see section 3.3 | Important | Shown only as a rejected option. |

### 4.7 [STALE DOC] findings

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| S-01: `orca-capabilities.md:8`, `:12` | Names CLI 1.4.237 and a 202-line guide | CLI 1.4.245 and a 215-line guide; `[G]` line numbers re-based | Minor | R-3: citations shift. Found at 05 `:199`. |
| S-02: `orca-capabilities.md:127` | Paging rule omits `page.hasMore` | Mention `page.hasMore`; the sweep pages on `page.nextCursor` | Minor | 05 `:200`. |
| S-03: `orca-capabilities.md` inventory | Missing `[H:worker-list]` line 22 (default scope) | Add it | Minor | 05 `:201`. |
| S-04: `orca-capabilities.md:97-102` | Candidate stale text against guide `[G]` 130-131 | Depends on C15 | Important | R-3: nested-worker rule (GQ-40). 05 `:202`. |
| S-05: `orca-capabilities.md:68`, `:177` | `ask` timeout | 600000 ms default, range 1 to 1800000 | Minor | 06 `:180`. |
| S-06: `orca-capabilities.md:8`, `:63` | Guide line numbers | Coordinator wait is `[G]:113`, not 108 | Minor | 06 `:181`. |
| S-07: `analyze-worker-contract.md` as cited by scope-01 | The old 55-line F1-F12 version | F1-F14 and S1-S5 | Minor | C1. |
| S-08: `sc-crash-recovery/SKILL.md:13`, `:155` | "Pure read-only, enforced by allowed-tools" | `Bash(git stash *)` is allowed | Important | C3. |
| S-09: `sc-crash-recovery/SKILL.md:4`, `:25-27`, `:53` | Hardcodes `~/workspace/...` | `~/workspaces/...` on this host | Important | C4. |
| S-10: #409 `concepts.md:23` | Ledger is age-ranked | The code has no sort | Important | C6. |
| S-11: #409 `DESIGN-CONTRACT.md:11` | Requires omission counts | Wide views have none | Important | C7. |
| S-12: recommend command docstring | `python -m` usage | UV form | Minor | C9. |
| S-13: `research/06-orca-open-questions.md:187` | Original summary stale | Superseded by `06:189` | Minor | GQ-89. |
| S-14: `research/research-notes.md:241-242` | Lists 05 and 06 as MISSING | Both exist | Minor | GQ-94. |

These were checked and are not stale: the WORKER-CONTRACT lines that 06 read (`06:182`) and `integration-gaps:11` (`06:183`).

### 4.8 Contradictions and the stronger evidence

| Contradiction | Side A | Side B | Stronger | Effect on Phase 1 |
|---|---|---|---|---|
| How many classes | The research question lists six | Section C lists seven, including fenced (`research-notes.md:194`) | Section C, which rests on WC-12 `:60` [CODE-VERIFIED] | Fenced stays its own class. If the owner keeps six, fenced folds into could not determine -> Open Questions. |
| Default window | The research question fixes 6 h | GQ-61 is open, and crash-recovery uses 72 h (`SKILL.md:26`) | Research question for Phase 1; the owner decision is still recorded | 6 h, activity only (N-41). |
| Null `agentWait` | `[H:worker-show]:16` | `[G:recovery]:58-61` | Neither is code. The sweep rule is conservative (GQ-58) | Never treated as stall proof. |
| Nested workers (C15) | `[G]` 130-131 | `orca-capabilities.md:97-102` | Unresolved; WC-13 governs the sweep | Report `parent` as a violation. |
| Retry form | `[G:recovery]` row 9 `--retry-of` | WC-6 `:70`, `:73` | WC-6 (repo contract) | Recommend "new Task". |
| Missing data | Grafana maps no-data to OK or firing (external, web-02) | WC-10 `:45` | WC-10 | A row that drops out is never finished. |
| Stall heuristics | Kubernetes taints and evicts after `Unknown` and restarts on liveness-probe failure; Harmonograf labels a progress-free run "stuck" with a UI alert only (external, web-01 D1, D3, D4). Only D1 contradicts WC-10; D3 is naming and D4 an action (synth-03 5.9) | WC-10, and only Orca stall proofs count | Codebase | Heuristics are a note column only, with no action. |

### 4.9 Open Questions ([UNVERIFIED], not stated as fact)

| # | Question | Blocks | Resolve by |
|---|---|---|---|
| OQ-1 | What does a populated `worker-list` row contain (G-A, C10)? | Call-count bound (GQ-99) | A live `worker-list --run <id> --json` capture |
| OQ-2 | What do live `unverifiable` and `exited` rows look like, and what is the end-of-turn marker (GQ-37, `research-notes.md:193`)? | Rules 2 and 7 | A captured stalled row and a transcript read |
| OQ-3 | Are `check --peek` / `--all` side-effect-free on the current runtime (GQ-44, GQ-57, GQ-59)? | Any use of `check` | Read the runtime handler, or test on a throwaway Run |
| OQ-4 | How does `gate-list` map to the Approval column (GQ-34)? | The Approval column | Plan probe |
| OQ-5 | Does the PATH form work under pipx (GQ-25), and how do `allowed-tools` patterns combine (GQ-26)? | SC-16 | Run `superclaude sweep --help` once outside a uv project |
| OQ-6 | Does the pane-key join hold for a second worker (K1)? | G6 if approved | Check one more worker |
| OQ-7 | Six classes or seven; is the window 6 h or 72 h; are person-started sessions reported; where does the report go; WC-14 or WC-1 (GQ-61, GQ-09, GQ-10, GQ-11)? | WC-14 text | Owner decisions |
| OQ-8 | `liveness.reason` values, `runtime_unavailable` shape, whether heartbeat feeds liveness, `inbox` read-marking, row caps (GQ-15 to GQ-17, GQ-46, GQ-65) | Could-not-determine wording | Captures |

### 4.10 Coverage of the assigned files

| File | Key findings reflected in | Excluded, with reason |
|---|---|---|
| `research/scope-01-contract.md` | Binding rules (3.3), G1-G7 and insertion points (3.1, 4.2), test pinning (3.2 SC-12) | - |
| `research/scope-02-orca-recovery.md` | Data sources and failure modes (3.1), A4 rejection and bugs (3.3, 4.3 K2), CC items (4.6) | `parse_session_log` reuse (`:157`) is UV and is a plan choice |
| `research/scope-03-cli-patterns.md` | Allowlist after NB-4, naming, call form, seam, registries, lint, scans (3.1, 3.2) | - |
| `research/scope-04-409-layout.md` | Skeleton, column sources, report rules, Q1-Q8 (3.1, 4.4) | - |
| `research/05-orca-row-schema.md` | G-A fallback, per-class signals, Gaps 1-10, stale docs (4.2, 4.4, 4.7) | - |
| `research/06-orca-open-questions.md` | G-B, check-mode constraints, Gaps 1-19, stale docs (4.2, 4.4, 4.7) | - |
| `gaps-and-questions.md` | Every row GQ-01 to GQ-100, K1-K4, AMBIGUITIES 1-11 (as GQ-09 to GQ-11, GQ-24, GQ-29, GQ-34, GQ-35, GQ-60 to GQ-63, GQ-66, GQ-67), C1-C15, sections (e) and (f) | - |
| `research/web-01-agent-supervisor-session-health.md` | Findings 1-7, D1-D4, recommendations 1-4 (3.3 External context, 4.8) | Recommendations 5 and 6 are excluded for Phase 1 (3.3) |
| `research/web-02-static-status-report-conventions.md` | Observation time, UNKNOWN on timeout, separate dimensions, oldest first, `shown/total`, optional if-then line (3.1, 3.3) | Grafana no-data mapping rejected (contradicts WC-10) |
