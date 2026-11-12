# Synthesis 03: Subsystem Reference (template section 5)

**Task:** TASK-TECHREF-orchestration-20261110-050239 (Supervised Orchestration Technical Reference, Heavyweight tier)
**Status:** Complete (2026-11-12)
**Date:** 2026-11-12
**Sections owned:** template section 5 (Subsystem Reference), subsections 5.1 to 5.7 (template: `.claude/templates/documents/technical_reference_template.md`, section 5 block at lines 263-327)
**Sources:** `research/01..06`, `research/gap-P3-G01..G06`, `research/web-01`, `research/web-02`, `gaps-and-questions.md`, `synthesis/evidence-routing.md`, the remediation plan `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/`. Every line number below was re-read in this run against the live file (HEAD `5bdb01681` plus seven uncommitted edits; Orca checkout `dc57b3d6e`) unless the text says "per gap-P3-Gnn" (taken from that gap file, which read the source).

## Reading guide

**Evidence classes and tags** (every non-trivial statement carries one) are those of the legend in section 1 (Overview). INSTALLED-FILES means Orca build files under `/opt/Orca/resources/app.asar.unpacked/out/`; HOST-INSTALLED means the `~/.claude/` copies and host settings. In this section CHECKOUT is HEAD `5bdb01681` plus the seven uncommitted edits (the list is in 5.1) and ORCA-CHECKOUT paths are written `IronOrca/src/...`.
**Hard boundaries kept in every subsection:** subordinate (sub-orchestrator) mode is deferred and not shipped; no installation rollout and no answer to the future-role question is claimed; the launch-level guard recognizing only the name `orca` is a recorded DEFECT (linked plan: `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/TASK-FIX-launch-guard-orca-names-20261111-235205.md`, a documentation-only draft, not a fix); no performance figure is given that was not measured.

---

## 5. Subsystem Reference

| # | Subsystem | Complexity | Primary files |
|---|---|---|---|
| 5.1 | Roles and authority | Standard | `src/superclaude/core/WORKER-CONTRACT.md` (sections 1-3), `src/superclaude/core/CLAUDE.md` |
| 5.2 | Coordinator lifecycle and Orca worker-side lifecycle | Complex | `WORKER-CONTRACT.md` section 4, `IronOrca/.../orchestration/preamble.ts` |
| 5.3 | Hook guards and job identity | Complex | `src/superclaude/hooks/scripts/{require-orca-worktree-agent,launch-level-guard,launch-job-identity}.sh`, `hooks.json` |
| 5.4 | Launchers | Complex | `skills/sc-issue-protocol/scripts/orca_worktree.py`, `cli/issue_watch/launch.py`, `skills/ccsession-tag/` |
| 5.5 | Orca-side enforcement (development source) | Standard | `IronOrca/src/main/runtime/.../worker-start-authority.ts` and two siblings |
| 5.6 | Installer, Orca skills install and doctor | Standard | `cli/install_hooks.py`, `install_core.py`, `install_user_setup.py`, `install_ccsession.py`, `doctor.py` |
| 5.7 | Worker result channel | Standard | `return-contract.yaml` (written by commands), `WORKER-CONTRACT.md` WC-4 and WC-5 |

---

### 5.1 Roles and Authority

**Purpose:** Defines the two session roles of supervised orchestration (a person-opened coordinator and a dispatched worker), what each may do, and which human rulings are encoded in the rules. Almost all of it is instruction text read by language-model sessions; the only IronClaude-side machine check on these rules is described in 5.3.

**Key Files:**

| File | Purpose |
|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md` | Sections 1-3 (`:9-65`): terms, command-side rules WC-2/4/8/9/10/11, worker duties WC-3/5/7/12/13/14/15. Section 4 opens at `:67-69` with the coordinator definition. 327 lines; not in `git status` (equals HEAD). NORMATIVE. |
| `src/superclaude/core/CLAUDE.md` | `:45-61` "Orca session launches" and the ownership paragraph. Working-tree wording is uncommitted. NORMATIVE. |
| `src/superclaude/core/HOW-WE-WORK.md` | `:400`: "The coordinator is a session the person opened ... never a session that Orca itself started as a worker." NORMATIVE, committed. |
| `CLAUDE.md` (project root) | `:312` states the same ownership rule in its own words; uncommitted edit; not pinned by a test. |
| `src/superclaude/skills/ccsession-tag/README.md` | `:239-245` second copy of the ownership paragraph (uncommitted). |
| `tests/skills/test_worker_contract.py` | Static text pins: `NEVER_AS_WORKER` (`:382`, 8 entries), `RULE_PHRASES` (`:25-374`). 739 tests passed in the research run (`research/06` F4). |
| `tests/core/test_orca_session_launch_guidance.py` | Pins the ownership paragraph in the two `COPIES` (`:8`); asserts `"coordinator is person-opened"` (`:33`) and the absence of `"coordinator under another orchestrator"` (`:36`). 5 passed. |
| `.dev/orca-command-refactor/decisions/APPROVED.md` | HISTORICAL record of owner decisions D1-D5 (`:8-12`), approved 2026-11-02. Not distributed. |

**How It Works:**

1. **Roles.** The contract defines a *worker run* as "a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages" (`WORKER-CONTRACT.md:11`); every other session is ordinary. The coordinator is "an Orca coordinator session the person opened" that "plans, creates Tasks, starts workers, reads their reports and performs every outward action" (`:69`). Subagents have no identity in the contract: a command's own Agent-tool fan-out "stays as it is" and may not send lifecycle messages (`:60`). NORMATIVE.
2. **No code identifies a role.** No command, hook or script in the checkout reads a preamble, a Task ID or a Dispatch ID (grep over `src/superclaude/commands` and `hooks/scripts`: no hit, `research/01` B.1). "Person-opened" is a procedural fact, not a runtime property. [CODE-VERIFIED by absence]
3. **Command-side limits.** Under `--unattended` a command asks no person (WC-2, `:31`), writes one report contract (WC-4, `:32-39`), never calls `worker-start`, `dispatch` or `task-create` (WC-8, `:40`), takes no outward action and no brief can turn one on (WC-9, `:41-45`, decision D4), and keeps heartbeats alive (WC-10, `:46`). The mode is selected only by a standalone `--unattended` token (decision D1, `:12-13`); 31 command files carry an `## Unattended mode` section (16 in P1 plus 15 in P2; set pinned by `tests/skills/test_worker_contract.py` `test_p1_command_set_is_complete` `:1457` and `test_p2_command_set_is_complete` `:1569`).
4. **Worker-session limits.** Questions go to the coordinator via the preamble's `ask`, at most once per Task (WC-3, `:53-58`); `worker_done` is sent exactly once from the top-level session (WC-5, `:59`); the worker runs each chained `Command:` by invoking its Skill (WC-7, `:60`); and "never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting" (WC-13, `:62`). The brief guard (`:16-22`) is a worker-session duty with four `guard refused:` cases; no executable implements it, tests pin its wording only (`research/01` B.2, G7). Rule IDs present are WC-2 to WC-15; there is no WC-1.
5. **Never-as-worker list** (`:23`): `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. Eight entries, pinned by `NEVER_AS_WORKER` (`tests/skills/test_worker_contract.py:382`); advisory, nothing stops a coordinator dispatching one.
6. **Ownership wording (three states).** Working tree (uncommitted): "The eligible session that creates a worktree owns its agent(s). A supervised orchestrator's coordinator is person-opened; ownership does not authorize a supervised worker to create worktrees or dispatch workers" (`core/CLAUDE.md:57-61`). HEAD and the installed `~/.claude/CLAUDE.md` on this host: the older sentence "becomes its orchestrator, or a coordinator under another orchestrator". Seven files are modified (` M`): `CLAUDE.md`, `core/CLAUDE.md`, `ccsession-tag/README.md`, the hook and its `plugins/` mirror, and two tests. A managed package (`.dev/tasks/done/TASK-WF-planTheExplicitl-20261110-024937/`) records the explicit request and its execution on 2026-11-10; its own advisory review did not finish. No source records acceptance, commit or rollout. [CODE-VERIFIED state]
7. **Human rulings.** D1 (flag only plus brief guard), D2 (only the person gives a Ruling), D3 (pr-submit never a worker), D4 (no outward action by a worker), D5 (nesting depth one, coordinator person-opened, adds WC-13) appear at `WORKER-CONTRACT.md:12,57,23,41,62,69`. HISTORICAL source: `APPROVED.md:8-12`. The owner ruling that a worker that only reads a command file does not satisfy WC-7 is recorded at `APPROVED.md:83` (row P1-C5) and pinned as text at `tests/skills/test_worker_contract.py:353-359`.
8. **Ruling rule end to end.** `/sc:implement` stops `E-HALT-QA` and `E-NO-RULING` are never asked (`WORKER-CONTRACT.md:57`); `refs/qa.md:249` lists "executor-invented approval" as `E-NO-RULING`. The ledger eligibility rule (`refs/retry.md:498`) checks only the ordering of a `T<id>: Ruling:` line against `blocked` and `halt` records. Nothing checks who wrote the line. [CODE-VERIFIED ceiling]

**Public Interface:** none in code. The interface is text: the rule IDs above, the `Command:` and guard lines of the brief (see 5.2), and the `worker_done` outcome mapping (see 5.7).

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Orca dispatch preamble | External text | Defines a worker run (`:7`, `:11`); issued per dispatch by the running Orca build (5.2). |
| `~/.claude/skills/sc-implement-protocol/refs/qa.md`, `refs/retry.md` | NORMATIVE | Halt table and Ruling eligibility the contract cites. |
| `superclaude install` | Installer | Copies the contract to `~/.claude/WORKER-CONTRACT.md` (5.6). |

**Consumers:**

| Used By | How |
|---|---|
| Coordinator session | Reads `~/.claude/WORKER-CONTRACT.md` voluntarily; no hook or startup step loads it (`research/02` G12, UNVERIFIED beyond three hook scripts and `hooks.json`). |
| Worker session and the 31 converted commands | Apply WC-2 to WC-15 and their `## Unattended mode` sections. |
| `tests/skills/test_worker_contract.py` | Pins phrases of the contract text. |

**Conventions & Patterns:**

- Authority is expressed as brief text and contract rules; mechanical enforcement is the exception (5.3, 5.5).
- A statement of the hook's reach always names the literal `orca worktree create` (`research/gap-P3-G02` section 3.5).
- Cite the ownership wording as "working-tree wording, uncommitted at 2026-11-12"; never describe the older wording as current.

**Evidence and contradictions:**

| Item | Class and tag | Note |
|---|---|---|
| No IronClaude hook or script distinguishes a coordinator from a worker; WC-13 text is the IronClaude-side barrier | CHECKOUT [CODE-VERIFIED] | A create carrying `--agent` passes the gate whatever the caller (5.3). |
| "eligible session" is undefined | NORMATIVE [UNVERIFIED] | Only the negative reading (a supervised worker is not eligible) is stated. Open question C8 of `gaps-and-questions.md`. |
| "orchestrator" in `core/CLAUDE.md:58` has no definition in the contract | CHECKOUT [CODE-VERIFIED] | No orchestrator role is implemented. Open question C9; future role owned by issue #444 (OPEN). |
| `WORKER-CONTRACT.md:14` lists `--monitor 1 (pr-submit)` as refused, but pr-submit has no `## Unattended mode` section and is on the never-as-worker list | CHECKOUT [CODE-CONTRADICTED] (internal) | Not a DEFECT: nothing claims pr-submit runs unattended. Open question C2. |
| Rule text "Every Orca worktree gets an agent" (`core/CLAUDE.md:55`) omits the claim-flow exception | NORMATIVE [CODE-CONTRADICTED] by 5.4 | Exception recorded at `docs/designs/sc-issue-claim-pipeline-flag.md:11,194,380` (2026-11-08). Open question C1. |
| Ruling authorship is not machine-checked | CHECKOUT [CODE-VERIFIED] ceiling | Open question C10. |
| WC-13 ban text and the `:69` sentence are pinned by no test (only the heading phrase at `test_worker_contract.py:155`) | CHECKOUT [CODE-VERIFIED] | `research/06` U5. |
| Test name `test_never_as_worker_list_names_all_seven_commands` (`:912`) is stale; the tuple has eight | CHECKOUT [CODE-VERIFIED] minor | |

**Extension points:** To add a rule: edit the contract (`src/superclaude/core/WORKER-CONTRACT.md`), add its phrases to `RULE_PHRASES` in `tests/skills/test_worker_contract.py`, run `make sync-dev` and `make verify-sync`, and reinstall (5.6). To add a converted command: add an entry to `UNATTENDED_EXPECT` (`:438`; `UNATTENDED_COMMANDS` is derived at `:746`) and a phase tuple. To add a role: N/A, deferred. A subordinate role is not designed or shipped; issue #444 owns the question and this reference does not resolve it.

---

### 5.2 Coordinator Lifecycle and Orca Worker-Side Lifecycle

**Purpose:** Describes the full life of a supervised Task from both ends: the coordinator's rules (create, wait, sweep, classify, escalate, admit, retry, merge) that exist only as contract text, and the worker-side half that Orca generates (dispatch preamble, heartbeat, `ask`, `check`, `worker_done`, settlement, liveness evidence). The two halves meet at Orca messages; the coordinator rules are normative, the worker-side behavior is read from Orca source.

**Key Files:**

| File | Purpose |
|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md` | Section 4 (`:67-282`): WC-6 retries (`:71-79`), brief contents (`:81-93`), liveness supervision (`:95-200`), worktrees (`:218-225`), git ownership (`:227-235`), result admission (`:237-246`), `/sc:implement` freeze (`:248-269`), fan-in (`:271-273`). Section 5 (`:283-327`) is the brief template. NORMATIVE. |
| `IronOrca/src/main/runtime/orchestration/preamble.ts` | `buildDispatchPreamble` (`:52-152`): the text a worker is given. ORCA-CHECKOUT; same text in the INSTALLED-FILES chunk `main/chunks/orcad-migration-source-retention-B-HAVPZ-.js` (per gap-P3-G01 S8). |
| `IronOrca/src/shared/orchestration-heartbeat.ts` | Heartbeat setting names and defaults (`:10-12`). |
| `IronOrca/src/main/runtime/orchestration/db/attempt-outcome-projection.ts` | 60 s attempt-observation window (`:11`); has no production writer except `worker_report` (see below). |
| `IronOrca/src/shared/orchestration-fleet-worker-projection.ts` | `projectLiveness` (`:53-100`, per gap-P3-G01 S5): the fleet liveness verdict a coordinator reads. |
| `IronOrca/src/main/runtime/orchestration/coordinator.ts` and `coordinator-task-dispatch.ts` | The retired automatic Task scheduler (dormant). |
| `tests/skills/test_worker_contract.py` | Static pins of section 4 phrases. Does not test coordinator behavior. |

**How It Works:**

```
 person opens coordinator session (NORMATIVE, WORKER-CONTRACT.md:69)
        |
 task-create --spec (brief + unique report dir)   [coordinator LLM]
        |
 worker-start  ---->  Orca writes dispatch preamble into worker session
        |                      |
        |            worker: heartbeat / ask / check / status ...
        |                      |
 check --wait --types <9 types> --timeout-ms 300000  <----  Orca mailbox
        |   sweep <= every 5 min: worker-list, worktree ps --agent-wait, stat contract
        |   S0-S11 state table --> ladder L0-L5 (WC-6 governs any restart)
        v
 worker_done --outcome --report-path   -->  Orca settles Task (valid report only)
        |
 coordinator opens return-contract.yaml, admits succeeded/partial/failed/blocked
        |
 dependents created only after inputs are admitted (--deps); merge, stage, publish on instruction
```

*Coordinator rules (NORMATIVE; no code runs the loop).*

1. **Retry is a new Task (WC-6).** The coordinator never uses `worker-start --retry-of`; every retry is a new Task from `task-create --spec` with its own report directory (`:73`). Orca counts failures per Task and trips at 3 (`dispatch-circuit-breaker.ts:1`), but its refusal sits inside the `if (params.retryOf)` branch of `worker-dispatch-start.ts:95-104`, so a coordinator that follows WC-6 never reaches it. The three-failed-starts comparison is the coordinator's own (`:75`) and no code performs it. [CODE-VERIFIED, ORCA-CHECKOUT]
2. **The wait (`:99-108`).** `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000` (`:101`). `--types` only decides when a waiter wakes; a returned Delivery is the whole FIFO batch, replayed until `--ack` and shared by every wait on one Run inbox (`:103`). The coordinator handles every message in the batch and writes one run-notes line per message ID before `--ack`; if the notes write fails, the batch is not acked (`:104`). After three empty waits in a row it enumerates workers with `worker-list` (`:107`). Per-type duties: table A.
3. **The sweep (`:110-114`).** After every wake or timeout, at most once every 5 minutes: one `worker-list`, one `worktree ps --agent-wait`, one `stat` per worker contract path (WC-11), updating each worker's heartbeat record (arrival time, progress token, declared window). Costly probes (transcript tail, screen read) run only for workers a trigger fired for. Deadline W is `max(10 min, 2 x observed median heartbeat interval)`, or the worker's `expect_silence_min`, capped at 45 minutes; a semantic change is a substantive change of the progress token, the contract file or the transcript content (a message arrival or a repeated identical read is not one); starting values: startup grace 10 minutes, a read-only probe after 10 minutes with no semantic change, a named state or an L5 report by 15 minutes after the last semantic change, an unreachable report after 10 minutes of continuous `unverifiable`. Every value is "a starting value, not a measured one" (`:97`); the coordinator keeps the values it uses in its run notes, a brief may override them, a worker may not. States: table B.
4. **Responses (`:131-192`).** Ladder, ack timeline, restart classes, resume note and the never-on-silence list: table C. Worktree, git and fan-in duties: table D.
5. **Admission (`:237-246`).** `succeeded`: dependents may start; `partial`: the coordinator records usability first; `failed` or `blocked`: no dependents; `guard refused:` with no contract: at most 2 brief fixes. `/sc:implement` follows its freeze rules (`:248-269`); the seven-condition resume check has no script (the executor-side ledger in `sc-implement-protocol` does).

*Coordinator loop tables.* All four tables are NORMATIVE contract text (`WORKER-CONTRACT.md` at HEAD, 327 lines, lines re-read 2026-11-12); no code runs the loop, detects a state or sends a nudge. The Orca column of table B is `research/gap-P3-G01.md` S9 (ORCA-CHECKOUT, installed files identical per S8; it names what Orca can show, not what a coordinator does).

Table A: per-message-type duty (`:105-108`; no code implements this dispatch table).

| Type | Duty |
|---|---|
| `heartbeat` | Update the worker's heartbeat record; never a stall proof. |
| `status` | With an ack line: ack rules (table C). Naming a report path or saying the work is complete: sets S9 when the brief has no later `Command:` line, otherwise logged. Any other: logged. |
| `worker_done` | Open the contract. A second one for the same dispatch is logged and ignored. The coordinator never sends or synthesizes `worker_done` for a worker. |
| `question` | Answer with `reply --id`, or forward to the person; starts the ack clock. |
| `escalation` | L1, then L5. |
| `decision_gate` | Goes to the person. |
| `handoff` | Any new work is left to the coordinator's decision (WC-13). |
| `merge_ready` | Merge only on the person's instruction. |
| `dispatch` | Logged as unexpected. |
| unknown type | The sender goes to S11 and is shown to the person; never silently acked. |
| `worker_done`, `question`, `escalation`, `handoff`, `merge_ready` with a Task ID or Dispatch ID that differs from the sender's current ones | Quarantined: logged and shown to the person, never applied. |

Table B: liveness states S0-S11 (`:116-129`).

| State | Trigger (abridged) | Coordinator response | Orca-side evidence (gap-P3-G01 S9) and class |
|---|---|---|---|
| S0 starting | No progress token or transcript 10 minutes after start | L1, then L2 "begin your brief", then L5 by 15 minutes | Worker `starting` with receipt `turn_start_unobserved` when the preamble was written but the turn start was not seen (`worker-start-readiness-settlement.ts:107-146`); the grace is the contract's. CODE-VERIFIED states, grace contract-only |
| S1 progressing | Token changed within W and a semantic change within 10 minutes | L0 | Contract-only; Orca adds `projection.stage.activity` only when liveness is `live` (`orchestration-fleet-worker-projection.ts:236`) |
| S2 long step | A declared window, or transcript activity under 5 minutes old | L1 at 10 minutes even inside the window (the window defers only nudges and typed text); past it, L1, L3, then L5 by 15 minutes | Contract-only (token, window), as S1 |
| S3 idle at prompt | No token change for W, last transcript entry 5 minutes old or older with no `worker_done` in the final turn, empty prompt, no pending ask | L1, L2, L3; L4 only with a stall proof; a third idle episode goes to L5 | No Orca verdict; raw evidence is `worker-read --source transcript\|terminal`, and `nextAction: none` when the agent is `live` with no pending input (`orchestration-fleet-worker-projection.ts:168-174`). Contract-only |
| S4 blocked on a person prompt | `agentWait` non-null | Capture the screen; L5 at 5 minutes plus Orca's own delay, re-reported every 15 minutes; never answer the prompt | `observation.agentWait` of `worker-show`: non-null names a worker parked on a human-only prompt (source hook, prompt text or title), `null` = looked and found none, absent = never looked (`orchestration-worker-specs.ts:58`; `worker-observation.ts:140-148`). CODE-VERIFIED |
| S5 blocked in ask | An open `question` | Answer it, then the ack timeline | A pending `question_threads` row sets `pendingInput` and the `input` attention category (`worker-terminal-attention-query.ts:46-49`; `orchestration-fleet-attention.ts:49-51`); the worker's `ask` blocks on `dispatch:<id>` (`ask-methods.ts:195`). CODE-VERIFIED |
| S6 context exhausted | Token unchanged for W while heartbeats arrive, or the S3 trigger; screen text such as `Autocompact is thrashing` confirmed by a second read 5 minutes later | Interrupt with "write your handoff file now, then end your turn" (the WC-14 exception); if the turn ends without `worker_done`, L4 within the budget, otherwise L5 and ask the person for a recorded stop | Contract-only; no Orca verdict or field |
| S7 unreachable | Liveness `unverifiable` | L5 after 10 minutes; never L4 | `projection.liveness.verdict == unverifiable` with one of ten reasons (item 9 below); Orca's guide: `unverifiable` is always absence (`bundled-skill-guides.ts:4504-4509`), so "unreachable" means no fresh positive evidence, not an uncontactable process. CODE-VERIFIED reason set; how often a stalled worker shows which reason is [UNVERIFIED] |
| S8 exited | Liveness `exited` | Settle under WC-6, then L4 or L5 | `verdict == exited` with source `execution_host`, `resource_release` or `worker_stop`: durable proof (`orchestration-fleet-worker-projection.ts:59-71`); `nextAction.kind == recover` when unsettled with nothing pending (`:155-166`). Not produced by a silent worker. CODE-VERIFIED |
| S9 finished but unreported | Contract present, no later `Command:` line, no `worker_done` within one sweep | L1 (read the contract), L2 "send `worker_done` per WC-5 with `--report-path <path>`", then L5 by 10 minutes after the nudge | Orca's analogues `finished_unverified` and `outcome_unknown` exist but their facts are never recorded, so Orca will not raise them; the contract's `stat` (WC-11) is the only detector. Contract-only; Orca analogue unreachable [CODE-VERIFIED by grep] |
| S10 settled | `worker_done` received | None | Accepted report: Dispatch `completed`/`failed`, `worker_report` fact, Task `completed`/`failed` (`worker-report-settlement.ts:93-94,205-267,282`); a second report for the Dispatch is a duplicate (`duplicate: true`). CODE-VERIFIED |
| S11 unknown | The deciding evidence is stale or unknown | L1, then as the resulting state; no typed input while S11 | Maps to `unverifiable` and to an absent `agentWait` ("never looked"). CODE-VERIFIED |

Table C: responses and records (`:131-192`).

| Item | Rule |
|---|---|
| L0 observe | Watch only; always. |
| L1 probe (`:151`) | Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat`; every sweep, at most 2 costly probes per triggered worker per sweep. |
| L2 nudge (`:152`) | Typed with `--wait-submit` (text at `:164`); the S6 variant is an interrupt plus a handoff request; at an identified prompt after L1 confirms S3, S9 or S6; 1 per incident, 2 per lineage, and a nudge with no turn start still counts. |
| L3 ask (`:153`) | Typed "Reply with `status`: current step, what you are waiting for" after L2 failed once and the state is still ambiguous; 1 per incident. |
| L4 restart with resume note (`:154`, `:157`) | Reconcile, stop the worker, settle it, set the old Task `failed --result cancelled`, create a new Task. Only on an Orca positive stall proof (`exited`, the process exit, or a transcript whose final agent turn sent no `worker_done`) or a person-directed cancellation with confirmed quiescence (WC-6), within 1 per rolling 60 minutes and 2 per lineage; the WC-6 three-failed-starts rule also applies, whichever is stricter. |
| L5 report to the person (`:155`) | The state, its evidence and what was tried; any person-only state or any cap reached; S4 is re-reported every 15 minutes. |
| Ack timeline (`:131-138`) | A1 at 0: record the answer as `pending_ack`. A2 at 5 minutes with no ack and no heartbeat showing the ask returned: L1 probe. A3 at 5 minutes, only when the probe positively shows an idle empty prompt: type ONE copy (text at `:143`) with `orca terminal send --text ... --enter --wait-submit`, at most one per message ID; a worker with no terminal skips A3. A4 at 15 minutes: L5 report with the message ID, answer, receipt fields and probe results. Never interrupt; never type into a busy, S11 or S4 session; without a positive idle identification skip to A4. A duplicate ack is a no-op; an ack does not prove the answer was right; at settlement a pending ack closes as `unacked-at-settlement`. |
| Restart cause classes (`:159`) | `idle`, `context-exhausted`, `exited`, `unreachable-then-exited`; the same class twice means no plain restart; for `context-exhausted` the next Task reduces the load (splits the `Command:` lines or narrows the inputs) or the coordinator goes to L5. |
| Resume note (`:167-180`) | Placed in the new Task's brief after the guard line and before the `Command:` lines; the new Task gets its own report directory and the old one is read-only input. Fields: `Resume` (replaced Task, cause class, evidence source and time), `Lineage` and attempt number, Task ID and Dispatch ID of the replaced attempt, completed `Command:` lines (n of m) and contract paths, last progress token, handoff file path, answered message IDs already applied, uncertain effects (actions started but not confirmed, such as a push or message send), load rule (pieces of at most 80 lines), `Start at: Command: line <k>`. For `/sc:implement`, its own `E-RESUME-NEEDED` re-run takes priority. |
| Never on silence (`:182-192`) | On silence, a passed deadline, `unverifiable` liveness or screen text alone the coordinator never: stops a worker; creates a retry Task; releases a worker or a worktree; marks a Task failed; answers a permission or person-only prompt; writes or drafts a Ruling; sends a lifecycle message for the worker. Silence authorizes only L1, L2 and L3. |
| Open points the contract lists (`:194-200`) | What `check --wait` wakes on without `--types` (the coordinator always lists every type); the cause of answers a worker did not see (a narrow `--types` list may miss a `status` reply); whether Orca has an attention category for a permission prompt or compact thrashing; what Claude Code does with text typed while a tool runs; whether two consumers on one mailbox both get a batch (owner question C11). |

Table D: worktree, git and fan-in duties (`:218-235`, `:271-273`).

| Duty | Rule |
|---|---|
| Worktree creation (`:220`) | Every worktree is created by Orca at its default location; never raw `git worktree add`, never under `.dev/worktrees/`; one feature worktree per feature, on its feature branch, where the coordinator runs. Enforcement: none for these parts; the gate blocks only `orca worktree create` without `--agent` (5.3 ceilings). |
| Child worktree and setup (`:221`) | Child created with `--setup skip` (Orca's `worker-start` otherwise defaults a new worktree to `--setup run`, which runs the repository's own setup hooks). `--setup run`, `make sync-dev` or any other repository target or hook only when the user's instruction in the coordinator's own conversation names that step, confirmed with the person at the moment of action unless that instruction is in the live conversation. A child is dispatched only after its setup succeeded. |
| Placement (`:222-223`) | A placement map (which Task writes in which worktree, sole writer or not) in the run notes and each `worker-start --comment`; a Task in a child gets an absolute report directory inside that child, read by absolute path before merge-back; a resume runs in its existing child by `--worktree id:<worktree id>`. |
| Merge-back and removal (`:224-225`) | After a child's result is admitted: merge the child branch into the feature branch, `orca worktree rm`, delete the branch; a discarded experiment is removed unmerged; a merge conflict is stopped and reported, never resolved automatically. Never removes a worktree or branch holding unmerged commits, an open PR, uncommitted changes, an unfinished `/sc:implement` ledger or an unread report without the user's instruction; never runs one managed package in two worktrees. |
| Git and GitHub ownership (`:229-235`) | The coordinator performs every git and GitHub outward action, install, VM and paid run, only when the user's instruction names it (confirmation as above); every such action targets `IronbellyOrg/IronClaude`, never the upstream and never through Orca's issue or PR linking while Orca records the project as the upstream; progress posts are such actions; PRs only through `/sc:pr-submit --monitor 3` in an ordinary top-level session (decision D3); before any push that would publish worker commits the person has not seen, show them and push only on the person's go (a commit grant covers one Task); commit or merge in a worktree only when no worker runs there and no `/sc:implement` plan there is frozen, compare `git status --porcelain` with the settled contracts, stage explicit paths plus `.dev/tasks`, commit with `git commit --only -- <paths>`, treat "nothing to commit" as success, stop on any hook rewrite, hook failure or conflict, never `--no-verify`; the plan or brief records who owns each PR. |
| Fan-in (`:273`) | For N input Tasks feeding one merge Task: wait until all N have settled; admit an input only if `succeeded`, or `partial` judged usable; each `blocked` or `failed` input is answered or retried as a new Task before the merge, or dropped with the reason recorded; N is at most the merge command's maximum of 10 and a re-run replaces its input; create the merge Task only with at least 2 admitted inputs and list every dropped input and reason in its brief; with fewer than 2 there is no merge and the coordinator reports the single result or the failure. |

*Worker-side half (ORCA-CHECKOUT; INSTALLED-FILES identical except where noted).*

6. **Preamble.** The worker is told, per dispatch, to send `worker_done --task-id --dispatch-id --outcome succeeded` (or `failed`) exactly once (`preamble.ts:106`), to heartbeat only when the setting is on (`:77`; with `heartbeatIntervalMinutes` null the preamble has no heartbeat command at all), to `ask --timeout-ms 600000` and resume by message ID on timeout (`:118`), and to run `check --terminal <h> --json` then `--ack <delivery_id>` at checkpoints (`:128,133`). The CLI word is `devMode ? 'orca-dev' : (cliCommand ?? 'orca')` (`:54`). The preamble has no `Dispatch ID is:` line, no `check --wait`, and no mention of IronClaude, `return-contract.yaml` or WC rules (gap-P3-G01 S1).
7. **Heartbeat setting.** Default on, interval 5 minutes, range 1-60 (`orchestration-heartbeat.ts:10-12`), baked into the preamble at dispatch time; the installed defaults are identical (per G01 S8). The running setting is [UNVERIFIED] DEPLOYED-RUNNING.
8. **Heartbeat recording.** Orca keeps only `dispatch_contexts.last_heartbeat_at` for the current Dispatch (visible as `worker-show --json` `dispatch.lastHeartbeatAt`); a late heartbeat from a settled Dispatch is suppressed. The 2x-interval stale warning exists only in the retired scheduler. Heartbeat age as a stall signal is IronClaude policy applied to a raw timestamp, not an Orca verdict (G01 S4, C12).
9. **Liveness evidence a coordinator can read.** `worker-show` returns two words: `projection.liveness.verdict` (fleet agent liveness: `live`, `exited`, or `unverifiable` with a reason) and `observation.status` (PTY liveness); text mode prints only the first (G01 S5). `unverifiable` is "always absence" (Orca guide `bundled-skill-guides.ts:4504-4509`) and carries one of ten reasons: `missing_status`, `stale_status` (no agent-hook activity for 30 minutes, `agent-status-freshness.ts:4`), `restored_unconfirmed`, `future_status`, `unsupervised_settled`, `host_unavailable` (also for a local chat-session worker), and four federated reasons. `exited` is durable proof of stop or release. [CODE-VERIFIED, ORCA-CHECKOUT]
10. **The 60 s window is not fed.** `DEFAULT_FRESH_AFTER_MS = 60_000` and a `finished_unverified` outcome exist (`attempt-outcome-projection.ts:11`), but the only production facet writer records `worker_report`; the `liveness`, `process_turn` and `outcome` facets are written only in tests, in the checkout and in the installed chunk (G01 S3, S8). Nothing should be documented as relying on `finished_unverified`. [CODE-VERIFIED by whole-`src` search]
11. **Settlement.** A valid `worker_done` moves the Dispatch and Task to `completed` or `failed` and promotes ready dependents `pending` to `ready`; it starts nothing. A report can be rejected (`unknown_task`, `unknown_dispatch`, `task_dispatch_mismatch`, `inactive_dispatch`, `stale_dispatch`); a second `worker_done` for one Dispatch is a duplicate (G01 S7).
12. **Retired scheduler.** `class Coordinator` still exists but is fenced three ways: CLI handlers throw `orchestration_migration_required` (`dispatch-handlers.ts:73-83`), the RPC contract retires `orchestration.run` and `orchestration.runStop` (`orchestration-rpc-contract.ts:45`), and `orchestrationMigrationFence` rejects them before any handler (`orchestration-contract-fence.ts:20`). Reachability was traced in the checkout; the installed bundle was checked textually only. Not a DEFECT: nothing in IronClaude claims it runs.

**Public Interface:**

```text
# Coordinator verbs named by the contract (syntax authority: the dispatch preamble, WORKER-CONTRACT.md:7)
orca orchestration task-create --spec <text> [--deps <json_array>]
orca orchestration worker-start --task <id> [--worktree new-child --base-branch <ref> --setup skip] [--comment <text>]
orca orchestration check --wait --types <list> --timeout-ms 300000 | --ack <delivery_id>
orca orchestration reply --id <message_id> --body <text>
orca orchestration worker-list | worker-show --dispatch <id> --json | worker-read --source transcript|terminal
orca worktree ps --agent-wait          # installed files only, see contradictions
# Worker verbs from the preamble: send --type worker_done|heartbeat|escalation|status, ask, check
```

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Running Orca build | External runtime | Issues the preamble, mailbox and settlement; its version and settings were not observed. |
| `WORKER-CONTRACT.md` read by the coordinator | Text | Not auto-loaded; `install_core.py:27` installs it; `HOW-WE-WORK.md:396-406` points to it but omits WC-6, liveness and the freeze rules. |
| `sc-implement-protocol` refs (`qa.md`, `retry.md`, `ledger.md`) | Skill text | Halt table, Ruling rule, `q0-head`, ledger regex the freeze check cites. |

**Consumers:**

| Used By | How |
|---|---|
| Person-opened coordinator session | Follows section 4 as instructions. |
| Worker session | Follows the preamble plus WC-3/5/10/12/14/15 (5.1). |
| `/sc:implement` | Executor-side ledger and ladder; the coordinator-side freeze has no script. |

**Conventions & Patterns:**

- The preamble is the authority for verb syntax and cadence (`:7`); the contract never copies them.
- Silence authorizes only read-only probes, a nudge and a question, never a stop, retry or release (`:182-192`).
- Orca guidance is mirrored with one deliberate override: Orca's guide recommends `--retry-of`, WC-6 forbids it (`:73`).

**Evidence and contradictions:**

| Item | Class and tag | Note |
|---|---|---|
| `worktree ps --agent-wait` (`:110`) | ORCA-CHECKOUT `core.ts:154` lacks the flag; INSTALLED-FILES `cli/specs/core.js:157-158` accepts it | State divergence between two Orca builds 1048 commits apart, not a DEFECT. Wording: "accepted by the installed build files read on this host; absent from the development checkout `dc57b3d6e`; the running build was not checked". |
| Contract label "two consumers on one mailbox" UNVERIFIED (`:200`) | Both Orca help texts say listeners get the same Delivery (`orchestration.ts:120`, `cli/specs/orchestration.js:118`) | Label is stale-conservative (owner question C11); running build unobserved. |
| `:78` "task on the command line" | Terminal delivery is a typed agent turn (`deliver-worker-dispatch-preamble.ts:102-109`, G01 S10) | Timing claim stays [UNVERIFIED]. |
| Section 5 template keeps P0 wording (`:295,303-307`) | CHECKOUT [CODE-VERIFIED] stale | Pinned by tests (`test_worker_contract.py:360-367`); all 31 commands are converted. |
| No code runs the lifecycle; tests pin phrases only | CHECKOUT [CODE-VERIFIED] | 739 contract tests passed in one run; they prove the text is present. |
| Running Orca: heartbeat setting, hook evidence, depth, behavior | DEPLOYED-RUNNING [UNVERIFIED] | Accepted limit (gap register B). |

**Extension points:** To add an S-state or ladder rung: edit `WORKER-CONTRACT.md` section 4, extend `RULE_PHRASES` in `tests/skills/test_worker_contract.py` (rows S0-S5, S7, S8 and the W formula are currently unpinned, `research/02` G15), run `make sync-dev` and reinstall. To change the heartbeat cadence: an Orca setting, not IronClaude code. A coordinator program: N/A, not built; the loop is a person-directed LLM session by design.

---

### 5.3 Hook Guards and Job Identity

**Purpose:** Three shell hooks give the only IronClaude-side machine checks around Orca use: a worktree gate that requires `--agent` on `orca worktree create`, a launch-level guard that limits sessions bound by the `/sc:issue --claim` launch marker, and a Linux job-identity adapter that wraps those sessions' Bash calls. None of them identifies a worker or a coordinator (5.1). The launch-level guard recognizes the Orca CLI only under the name `orca`; that is a recorded DEFECT (see "DEFECT" below), not a fixed one.

**Key Files:**

| File | Purpose |
|---|---|
| `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | PreToolUse(Bash) worktree gate, 358 lines. Header `:1-61` states scope and ceilings; orca-word test `:145`; verdict `:349`; block message `:351-358`. Working tree carries an uncommitted message change (`:354-355`). |
| `src/superclaude/hooks/scripts/launch-level-guard.sh` | Launch-level guard, 747 lines. Fail handling `:147-163`; governed-session lookup `:257-273`; `orca` arm `:458-478`; decision matrix `:722-742`; default deny `:747`. |
| `src/superclaude/hooks/scripts/launch-job-identity.sh` | Bash header plus embedded Python, 566 lines. `LEVELS` `:74`; hook mode `:414-489`. |
| `src/superclaude/hooks/hooks.json` | Registrations: guard on UserPromptSubmit `:63-71` and PreToolUse `:115-124`; gate `:105-114`; identity `:125-134`. |
| `src/superclaude/cli/install_hooks.py` | Lists the three scripts in `_FRESHNESS_SCRIPTS` (`:88,90,93`); copy and merge (5.6). |
| `docs/designs/sc-issue-launch-level-hook.md` | NORMATIVE design: status `:6,10`, failure table `:216`, residual risks `:440`. |
| `tests/hooks/test_require_orca_worktree_agent.py`, `test_launch_level_guard.py`, `test_launch_level_guard_registration.py`, `test_launch_level_guard_with_identity.py`, `test_launch_job_identity.py`, `test_launch_level_observations.py` | Read, not run in this research. 12 live observations are skipped tests (`test_launch_level_observations.py:79-84`). |

**How It Works:**

*Registration.* All entries are `"type": "command"` with the installed flat path `~/.claude/hooks/<name>.sh`. The Bash PreToolUse group is, in array order, `block-bare-python.sh` (timeout 3, `hooks.json:95-104`), the worktree gate (3, `:105-114`), the guard (5, `:115-124`, matcher `^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)`) and identity (5, `:125-134`). The guard also runs on every UserPromptSubmit (5, `:63-71`). No registration sets `onFailure` (pinned by `test_launch_level_guard_registration.py:63-65`). The array position is a registry property, not a documented execution order (see "Documented host behavior"). No project-level registration exists; the guards run only if the user-level `~/.claude/settings.json` registers them, which `superclaude install` does (5.6) and which this host's settings show (HOST-INSTALLED, `research/03` B.4).

*Worktree gate (`require-orca-worktree-agent.sh`).* jq extracts `tool_input.command` for `tool_name == "Bash"` (`:345-347`) and pipes it to one stateful awk scanner (`:74-340`). The scanner collects each simple command's words, skips assignments, wrappers (`env sudo nice nohup time exec timeout command coproc`) and keywords, and takes the basename of the command word; the command is tracked as an Orca command only when `b == "orca" || b ~ /^\$/` (`:145`). At each separator it prints `orca` only when the first two non-option arguments are `worktree create`, no word is `--agent`, `--agent=...`, `--help` or `-h` (`:99-103`). Block is exit 2 with a five-line message (`:351-358`); anything else is exit 0. A flag in one command never satisfies another. Fail open (exit 0): `jq` or `awk` missing (`:65-72`), empty or non-JSON input, non-Bash tool (so a Monitor call is never scanned), missing command, scanner error. Header-listed ceilings (`:39-61`) include `bash -c`/`eval`/`env -S`/`ssh` strings, `xargs orca`, `find -exec orca`, quoted `--agent`, built command words, global options before `worktree`, non-Bash tools, `claude --bare`, humans, and scripts that call Orca as a subprocess (`orca_worktree.py` runs Orca itself, so its own create is outside the hook). It also does not block raw `git worktree add`, paths under `.dev/worktrees/`, `--setup run`, or removal of a worktree that holds unmerged work (the script has no match for `git worktree`, `worktree add`, `.dev/worktrees`, `setup`, `worktree rm` or `unmerged`, grep 2026-11-12; `research/02` 5.4), although the project rule says never to create a worktree that way; those parts of `WORKER-CONTRACT.md:220-225` are text only (table D in 5.2). The hook contains no role, session or environment predicate; the block message's "workers cannot create worktrees" (`:355`) is advice, not a test.

*Launch-level guard (`launch-level-guard.sh`).* Governs only a session whose top-level `session_id` has a file under `$HOME/.claude/state/launch-level/sessions/<sid>` (`:257`); everything else is ungoverned and never blocked. The record content selects the level: `worktree` (W), `full` (F), `full-submit` (FS); any other content gives W plus the LL-STATE note; `<sid>.ok` lifts W to WA (`:264-272`). A session becomes governed when its first prompt carries `[sc-launch:v1:<32 hex>]` and `pending/<nonce>` exists as a regular file; the nonce is consumed with one `mv` and published with a hard link, so a binding cannot be replaced (per research/03 C.2). Each tool call gets zero or more classes (BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL); the first blocked class in that precedence order denies (`:722-742`). Classification is textual: `bash -c "git commit -m x"` and `echo "git commit"` both count as a commit, and the accepted leaks (variables, escapes, `bash ./push.sh`) are pinned by tests (`test_launch_level_guard.py:3602-3622`). The `orca` arm (`:458-478`) reads the next two non-option words; the allow list is `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read` and `orchestration check|inbox|run-current|task-list|worker-show`; every other `orca` command adds ESCAPE, which is denied at every level (`:737`), unless the segment ends in `--help` or `-h` (`:477`). Consequence for orchestration: inside a governed session no `orca` mutation (`worker-start`, `dispatch`, `terminal send`, `agent launch`, `worktree create`) is possible under the name `orca`, but a supervised worker or a person-opened coordinator is not bound by any level.

*Failure behavior.* The EXIT trap (`:147-163`): exit 0, or exit 2 after a deliberate deny, passes; any other exit is an internal failure, which for a governed session prints LL-BROKEN (LL-NOBIND on the prompt branch) and exits 2, and for any other session exits 0. "Fail closed for governed sessions" therefore holds only for the script's own failure paths. Identity loss (no valid `session_id`) allows silently (`:390-394`); `agent_id` is never read on PreToolUse. A hook stopped at its timeout never reaches a deny: in a probe a TERM during stdin read or during a 64 KB governed command ended with exit 143 and no output, a KILL with 137 (gap-P3-G06 section 3, single runs). The design records "call goes ahead" as residual risk R2 (`sc-issue-launch-level-hook.md:216,440`).

*Job identity (`launch-job-identity.sh`).* "Linux same-user job identity, not a sandbox" (`:2`). Modes: no argument or `hook` (PreToolUse Bash adapter), `execute SESSION TOOL_ID COMMAND`, `prepare SESSION COMMAND [TOOL_USE_ID]`, `run TOKEN`, `identify [PID]`. In hook mode, for a session with a store record it validates the event and rewrites the Bash command to `/bin/bash <script> execute <sid> <tool_use_id> <original>` through `hookSpecificOutput.updatedInput`, with no `permissionDecision` (`:475-483`); any validation failure prints "launch job: governed Bash call cannot be wrapped safely" and exits 2 (`:484-486`), including a non-string `agent_id` or `agent_type` (`:448-450`). It ignores non-Bash tools, so Monitor calls are not wrapped (`:426-428`), and unbound sessions (`:429-437`). `LEVELS` is the three words (`:74`); a `degraded` record (which the guard writes for a leading marker with a missing nonce, and reads as W) makes the identity hook block every Bash call, pinned by `test_launch_level_guard_with_identity.py:186-212`; open question C12. `identify` has no runtime consumer in this checkout; its consumer, `launch-level-pre-push.sh`, exists on ORIGIN/MASTER only.

*DEFECT: the Orca CLI is recognized only under the name `orca`.* Both scripts test the last path component of a shell word against exactly `orca` (gate `:145`; guard `:458`). `orca-ide` (the installed command name on Linux and WSL), `orca-dev` (dev builds) and `orca.cmd` (Windows) match no arm. Probes of 2026-11-11 (gap-P3-G02; the key rows re-run in its fix cycle 1 and independently in `qa/phase-3-verification-content.md`; not re-run by the author of this section; 11 of the probes were re-run on 2026-11-12, see 13.2.1; prefix `G2-` per the register's note):

| Probe | Gate rc | Guard rc (bound session, W and FS) |
|---|---|---|
| G2-P01 `orca worktree create --name x` | 2 | 2 (ESCAPE) |
| G2-P02 `orca-ide worktree create --name x` | 0 | 0 |
| G2-P03 `orca-dev worktree create --name x` | 0 | 0 |
| G2-P08 `orca.cmd worktree create --name x` | 0 | 0 |
| G2-P06 `orca-ide orchestration worker-start --name w` | 0 | 0 (bare name: 2, G2-P07) |
| G2-P24 `orca-ide terminal send --terminal t1 --text approved` | 0 | 0 |
| G2-P28 `orca-ide agent launch --agent claude --worktree path:/x` | 0 | 0 (bare name pinned ESCAPE, `test_launch_level_guard.py:3102`) |

Determination (owner-confirmed 2026-11-11, register D): the guard's ESCAPE class and the approval-forgery guarantee at `sc-issue-launch-level-hook.md:193` ("terminal and messaging tools are ESCAPE") hold for the Orca CLI only under `orca`; no scope decision accepts alternate names (O-7, R1, R12, R15 cover built or hostile cases). It is a DEFECT of partial wiring (effective for one name Orca uses). The gate stays a documented ceiling, though its header list (`:39-61`) omits alternate names. Remediation plan: `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/TASK-FIX-launch-guard-orca-names-20261111-235205.md` (three tasks: guard arm, gate test, ceilings and design text). It is a draft written by a documentation run, not reviewed by `/sc:workflow` or executed; nothing here is fixed, merged or deployed. Which name a launched or supervised session actually types was not observed (G02 R1). On Linux Orca's own printed recovery commands use `orca-ide` (`orchestration-recovery-command.js:6-15`, INSTALLED-FILES), and on this host `orca` and `orca-ide` reach the same launcher.

*Documented host behavior (DOCUMENTED; not observed on this host).*

- Timeout: https://code.claude.com/docs/en/hooks says a `PreToolUse` command hook that reaches its timeout is cancelled, its output discarded and the call is not blocked unless `onFailure: "block"` is set (needs Claude Code v2.1.295 or later). Neither guard registration sets it. This matches the design's V8. The signal used and any message shown are undocumented [UNVERIFIED].
- Exit codes: exit 2 blocks and stderr is the reason; exit 0 applies stdout JSON; another code with plain-text, empty or invalid stdout is a non-blocking error; another code with schema-valid JSON is decided by the JSON. "Never exit 1" is the repository's convention, not a documented requirement.
- Order: matching hooks run in parallel, all run to completion, decisions merge `deny` > `defer` > `ask` > `allow`; several `updatedInput` rewrites are neither merged nor ordered (https://code.claude.com/docs/en/hooks-guide, "Limitations"). Describe hook order as unspecified, documented as parallel. A `deny` or exit 2 blocks in every permission mode, `bypassPermissions` included.
- Subagents: hooks from settings, managed policy and plugins fire for subagent tool calls, with optional `agent_id` and `agent_type` in the payload (https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/sub-agents). Whether a subagent payload's `session_id` is the parent's is undocumented [UNVERIFIED]; the guard's session binding assumes it (design ship gate U1; skipped test OB-H1 item 1).
- Bypass routes (documented, not observed as bypasses): `--bare` and `CLAUDE_CODE_SIMPLE=1` skip all hook discovery including `--settings` hooks (https://code.claude.com/docs/en/headless, cli-reference, env-vars); `--safe-mode` skips user, project and plugin hooks but keeps managed ones; `disableAllHooks` outside managed settings disables non-managed hooks (the claim preflight already refuses it, `orca_worktree.py:977-982`); `allowManagedHooksOnly` limits hooks to managed ones. Managed-policy hooks under `--bare` are undocumented.

**Public Interface:**

```text
require-orca-worktree-agent.sh : stdin {"tool_name":"Bash","tool_input":{"command":"..."}}  -> exit 0 | exit 2 + stderr (ORCA WORKTREE BLOCK ...)
launch-level-guard.sh          : stdin PreToolUse or UserPromptSubmit payload (session_id, tool_name, tool_input, agent_id?) -> exit 0 | exit 2 + LL-* message
launch-job-identity.sh         : hook | execute SESSION TOOL_ID COMMAND | prepare SESSION COMMAND [TOOL_USE_ID] | run TOKEN | identify [PID]
```

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| `jq`, `awk` (gate); `jq`, `sed`, `tr` and coreutils (guard); `uv`, Linux `/proc`, pidfd, subreaper (identity) | Tools | Gate fails open without `jq`/`awk`; identity exits 2 for a bound session without `uv`. |
| `$HOME/.claude/state/launch-level/{pending,sessions}` | File store | Written by `orca_worktree.py` (5.4); read by guard and identity. |
| `~/.claude/settings.json` registrations | Host config | Installed by `install_hooks.py` (5.6); `disableAllHooks` switches them off. |

**Consumers:**

| Used By | How |
|---|---|
| Claude Code (PreToolUse, UserPromptSubmit) | Runs the hooks on tool calls and prompts. |
| `orca_worktree.py` `enforcement_preflight` | Checks the guard and identity registrations, not the gate (5.4). |
| `launch-level-pre-push.sh` (ORIGIN/MASTER only in the repository; an installed host copy exists at `~/.claude/hooks/launch-level-pre-push.sh` and equals ORIGIN/MASTER, `cmp` 2026-11-12; active use as a git hook not observed) | Calls `launch-job-identity.sh identify`. Not read by this research. |

**Conventions & Patterns:**

- Decision contract: allow is exit 0, block is one stderr message and exit 2, never exit 1; fail open for anything a hook cannot judge, except the guard's governed-session failure paths.
- Scripts are standalone flat files, so the gate's scanner is a derivative (267 lines, 25 differing lines) of the `block-bare-python.sh` tokenizer, not a byte copy (the header's "copied" is [CODE-CONTRADICTED], low impact).
- Statements of the gate's reach name the literal `orca worktree create`.

**Evidence and contradictions:**

| Item | Class and tag | Note |
|---|---|---|
| Name `orca` only | CHECKOUT [CODE-VERIFIED] DEFECT (guard) / ceiling (gate) | Above; plan is a draft. |
| "Fail-closed for governed sessions" (research/03 C.3) | CHECKOUT, qualified by gap-P3-G06 | Holds for the script's own failure paths; not at a timeout, not on identity loss. |
| Host behavior at a hook timeout | DOCUMENTED; host [UNVERIFIED] | Open (G06 R1, R4). |
| Gate timeout 3 s is pinned, but no TIMING test exists for the gate | CHECKOUT [CODE-VERIFIED] debt | The value is pinned in both `hooks.json` trees by `tests/cli/test_install_hooks.py:827-846` (whole registration dict); `block-bare-python.sh` 3 s by `:765-780`; the identity hook 5 s, last in PreToolUse, by `:895-914`; the guard 5 s per event by `tests/hooks/test_launch_level_guard_registration.py:44-50`. G06 section 1.1 reported the gate's value as unpinned; the ranges above show the pin; the missing timing test is G06 R3. |
| L2 pre-push layer: absent at HEAD, present on ORIGIN/MASTER | `orca_worktree.py:800-801` and `refs/claim.md:127` are stale against ORIGIN/MASTER | `launch-level-pre-push.sh` and the 1,884-line `orca_worktree.py` were read by no research file. |
| Installed set on this host is mixed | HOST-INSTALLED | Guard and identity equal ORIGIN/MASTER and differ from HEAD; the gate equals HEAD and ORIGIN/MASTER and differs from the working tree; an installed `launch-level-pre-push.sh` exists and equals ORIGIN/MASTER (research/06 F6; `cmp` re-run at about 02:14 UTC on 2026-11-12, after a refresh at 01:59:25 UTC; matrix in 3.0.3). |
| The 12 live observations (OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX) | CHECKOUT [CODE-VERIFIED] skipped | Fixtures are synthetic; no live governed session was run. |
| WC-13 has no hook enforcement (a create WITH `--agent` is what the gate allows) | CHECKOUT [CODE-VERIFIED] | `worker-start` is an allowed case in the gate tests (`test_require_orca_worktree_agent.py:115`). |

**Extension points:** To add a guarded verb or name: gate scanner `:145` and `track`/`fin` (`:94-103`), guard `orca` arm (`:455-478`) and the decision matrix (`:722-742`), then `tests/hooks/test_require_orca_worktree_agent.py` (`BLOCKED`, `ALLOWED` tables) and `tests/hooks/test_launch_level_guard.py` (ESCAPE and NONE grids around `:3093-3151`); then copy the edited gate script byte for byte over `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` by hand (keep mode 0755): `make sync-dev` writes `.claude/` only, `superclaude install` writes `~/.claude/`, and the plugin mirror is a hand-maintained tracked copy pinned by `tests/cli/test_install_hooks.py:849-857` (a byte-equality test exists for five of the 13 mirrored scripts: codegraph-session-start `:724-733`, block-bare-python `:783-791`, require-orca-worktree-agent `:849-857`, launch-job-identity `:930-939`, launch-level-guard `:1085-1095`; the other eight mirrors have none; a new mirrored script needs its own). To add a hook script: add it to `_FRESHNESS_SCRIPTS` (`install_hooks.py:42`) and to `hooks.json`; `make verify-sync` requires every `hooks/scripts/*.sh` to be listed. The alternate-name change is exactly the remediation plan; do not duplicate it elsewhere.

---

### 5.4 Launchers

**Purpose:** Starts non-worker (not supervised) Claude sessions through `orca agent launch`: the interactive `/sc:issue --claim` flow (`orca_worktree.py`), the timer-run issue watcher (`launch.py`), and the ccsession wrapper chain that names the launched tab and lets the claim verify it. Neither launcher starts a supervised worker, calls `worker-start`, or contains a role check.

**Key Files:**

| File | Purpose |
|---|---|
| `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | Standard-library helper, 1,473 lines at HEAD. Subcommands `preflight` (`:192`), `worktree` (`:607`), `prompt` (`:746`), `launch` (`:1274`); `build_parser` `:1432`, `main` `:1464`. The only file in the skill that calls `orca`. |
| `src/superclaude/cli/issue_watch/launch.py` | Watcher's Orca adapter, 370 lines: `build_claim_prompt` (`:84`), `launch_argv` (`:95`), `find_orca` (`:163`), `check_origin` (`:233`), `outcome_of` (`:326`), `OrcaLauncher` (`:352`). Reached from `superclaude issue-watch once` (`cli/main.py:563-565`). |
| `src/superclaude/skills/ccsession-tag/{ccsession-orca,ccsession,hooks/session-name.sh,hooks/session-start.sh}` | Writer side of the tab title and tab record (per gap-P3-G05). |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `SKILL.md` | Skill text that calls the script (Waves 0, 5, 7, 8). |
| `tests/skills/test_issue_orca_worktree.py`, `tests/issue_watch/test_launch.py`, `tests/unit/test_ccsession_tag.py` | Fake-Orca tests; no test starts a real Orca. |

**How It Works:**

1. **Claim flow (`orca_worktree.py`).** The caller is a Claude session running Bash from the skill, not a Python importer. Every outcome prints one JSON object and exits 0 (exit 2 is argparse only). `preflight` runs `orca status --json` and requires `ok` and `runtime.reachable` (`:192`). `worktree` finds an existing worktree by comment marker, recorded path, basename `issue-<N>` or branch, else runs
   `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <repo>#<N>" --json` (`:666-682`).
   **There is no `--agent` and no `--prompt`** (docstring and test `test_fo18_exact_commands_and_no_forbidden_flag`, `test_issue_orca_worktree.py:837`). The reason recorded in the script and `refs/claim.md:101`: the issue directory and the pending launch record must be in place before an agent starts. The created path is read from a second `worktree list`, not from the create reply; for a created worktree the script then closes Orca's plain first tab (`close_first_tab`, `:550-604`) only when exactly one agent-less terminal is listed.
2. **Accepted exception to "every worktree gets an agent".** `core/CLAUDE.md:55` and project `CLAUDE.md:312` state the rule without exception; the agent-less create is recorded by owner decision of 2026-11-08 in `docs/designs/sc-issue-claim-pipeline-flag.md:11,194,380` ("The owner approved this first-tab close in place of 'agent on create'"). The approval is a sentence in a design document, not a primary owner message. Between worktree create and launch, or when launch is refused, a worktree can exist with its first tab closed and no agent. Owner question C1 (name the exception in the rule text) is open.
3. **Launch gates (`cmd_launch`, `:1274`).** In order: usable worktree record; duplicate-launch guard (record or `<git-dir>/sc-issue-launch-<N>.json` mirror, `already_launched` with no Orca call); stale-prompt check; `enforcement_preflight` (`:925`, IR-4: `jq`, `uv`, `cat sed tr mkdir mv ln rm`, Linux process interfaces, `~/.claude/hooks/launch-level-guard.sh` present with `# launch-level-guard-version: 1` (`launch-level-guard.sh:10`), `CLAUDE_CONFIG_DIR` unset or `$HOME/.claude`, no `disableAllHooks`, guard registered on UserPromptSubmit and on PreToolUse for every tool in `GOVERNED_TOOLS`, identity hook registered for Bash); `l2_status` (`:1018`, warn-only); then `publish_pending(word)` (`:1077`) writes `pending/<nonce>` (32 hex from `secrets.token_hex(16)`, mode 0600) holding `worktree`, `full` or `full-submit`. IR-4 verifies the claim process's environment, not the agent's, and does not check the worktree gate's registration (`GUARD_COMMAND` and `IDENTITY_COMMAND` only, `:808-809`).
4. **The launch call (`:1351-1355`).** `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`. On failure the pending record is deleted and a hand command is printed with the warning that a hand-started agent is not governed. The guard consumes the marker once (5.3).
5. **Shim check (advisory).** After launch, `behind_ccsession(handle)` (`:1142`) tries `SHIM_TRIES = 5` times (`:780`), `SC_ORCA_SHIM_INTERVAL` seconds apart (default 2.0): `orca terminal read --terminal <h> --screen --json` for `SHIM_MARKERS = ("[ccsession]", "Session name (Enter or Ctrl+C")` (`:774`), then `orca terminal show --terminal <h> --json` and the title pattern `SHIM_TITLE = sc-launch-v1-[0-9a-f]{1,12}-\d{4}-\d{6}-[0-9a-f]{4}\b` (`:779`) against `result.terminal.title`. A miss, or no terminal handle, adds `W-LAUNCH-NOT-CCSESSION`; status stays `launched`, the `launch` entry is still written and nothing closes the agent. Each read has a 15 s cap; with every call hanging the worst case is 5 x (15 + 15) + 4 x 2 = 158 s, otherwise about 8 s of pauses (arithmetic from the constants).
6. **Where the title comes from (ccsession).** `ccsession-orca` sees the claim prompt as one positional word, so no question is asked and `ccsession --auto-name "<prompt>"` builds `<folder>-sc-launch-v1-<12 hex>-<MMDD>-<HHMMSS>-<4 hex>` (words cut to 12 characters, folder to 20). The label is shown as `<label> · Claude Code` by an OSC escape at launch and by `orca terminal rename` from the SessionStart hook; both carry the same text. A valid `CCSESSION_NAME`, a Claude `--name`, `CCSESSION_AUTOSTART=0`, or an unwritable name-list directory yields a different or empty label and a false `W-LAUNCH-NOT-CCSESSION` (gap-P3-G05 F9, causes 1-5).
7. **Watcher (`launch.py`).** `launch_argv` returns exactly 12 elements: `[orca, "agent", "launch", "--agent", "claude", "--worktree", "path:<worktree>", "--surface", "terminal", "--prompt", "/sc:issue --claim <n>", "--json"]` (`:95-116`). The prompt must match `^/sc:issue --claim [1-9][0-9]{0,8}$` (`:33`); `ORCA_AGENT = "claude"` is fixed (`:28`); origin must be `ironbellyorg/ironclaude` (`:50`, `check_origin` `:233`). `find_orca` probes `_ORCA_CLIS = ("orca-ide", "orca")` with `skills list --json` and accepts only an exit-0 reply whose `topics` include `orca-cli` (`:163`). The watcher never creates a worktree (it uses the configured checkout), writes no state itself, and records a pending entry before the call (`cycle.py` `_launch`). Its prompt carries no `[sc-launch:...]` marker, so the watcher-started session is ungoverned; it binds a second, marked agent only if that session runs the claim (Path B, inferred from two verified hops, not run end to end).
8. **Reply shapes.** `OPERATION_ID_PATHS` (`launch.py:42`) and `OP_UNKNOWN_TEXT` are marked "PROPOSAL, UNVERIFIED" in the code; whether real Orca replies carry `receipt.operation_id` is [UNVERIFIED]. Reply shapes of `agent launch`, `worktree create` and `terminal` in the claim script are fixture-only.

**Public Interface:**

```text
uv run --no-project python <skill>/scripts/orca_worktree.py preflight | worktree --issue N --repo owner/repo --base origin/<b> | prompt ... | launch --level worktree|full [--submit] ...
superclaude issue-watch once [--dry-run] [--config PATH]
launch_argv(orca: str, worktree: Path | str, prompt: str) -> list[str]     # launch.py:95, 12 elements, ValueError on a prompt not from build_claim_prompt
find_orca(...) -> str | None   check_origin(...)   outcome_of(result: CommandResult) -> LaunchOutcome
```

(Flag names of the claim script's subcommands beyond those cited were not re-read in this run; see `build_parser`, `:1432-1461`.)

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Orca CLI (`orca`; the watcher also probes `orca-ide`) | External | The claim script uses the literal `orca` in every argv; it does not try `orca-ide`. |
| `launch-level-guard.sh`, `launch-job-identity.sh` and their registrations | Hooks (5.3) | IR-4 refuses a governed launch when absent (`W-ENFORCEMENT-ABSENT`). |
| Orca's Claude command set to `ccsession-orca` | Host setting | Manual step; neither installer nor doctor sets or checks it (5.6). Value on any host [UNVERIFIED]. |
| `~/.claude/state/launch-level/pending/` | File store | Handoff of the nonce to the guard. |

**Consumers:**

| Used By | How |
|---|---|
| `/sc:issue --claim` skill (Waves 0, 5, 7, 8) | Calls the script through Bash. |
| `superclaude issue-watch once` | Calls `OrcaLauncher.launch`; `status_report` prints a retry command (does not run it). |
| Launch-level guard | Binds the launched agent when the pending record is consumed. |

**Conventions & Patterns:**

- All subprocesses go through `run()`: no shell, captured output, timeouts (`DEFAULT_TIMEOUT` 120, preflight 30, terminal reads 15; `SC_ORCA_TIMEOUT` replaces every timeout).
- One JSON object per outcome, exit 0; warnings are codes ranked by `WARNING_ORDER`.
- Key environment variables (full 23-variable table: gap-P3-G05 F8, owned by section 9.2):

| Variable | Default | Effect here |
|---|---|---|
| `ORCA_PANE_KEY`, `ORCA_TERMINAL_HANDLE` | unset outside an Orca terminal | Set by Orca at PTY spawn; ccsession needs both for tab title and record. |
| `CCSESSION_AUTOSTART` | `1` | `0` disables question and auto-name. |
| `CCSESSION_NAME` | unset | Valid name replaces the auto label and defeats `SHIM_TITLE`. |
| `CCSESSION_ASK_TIMEOUT` | `30` s | `0` or any non-digit (for example `30s`) means no limit. |
| `SC_ORCA_TIMEOUT` | unset | Float above 0 replaces every call timeout. |
| `SC_ORCA_SHIM_INTERVAL` | `2.0` s | Pause between the five tries. |
| `CLAUDE_CONFIG_DIR` | unset | Claim preflight rejects any value other than `$HOME/.claude`; ccsession ignores it. |

**Evidence and contradictions:**

| Item | Class and tag | Note |
|---|---|---|
| Version: HEAD 1,473 lines versus ORIGIN/MASTER 1,884 lines (453 insertions, 42 deletions) | `git diff --numstat HEAD origin/master` (research/04 F5) | The installed `~/.claude` copy equals ORIGIN/MASTER. ORIGIN/MASTER adds an owned L2 pre-push hook with refusal off (`IR7_REFUSE = False`). This subsection describes HEAD; L2 statements are stale against ORIGIN/MASTER and the installed copy. The newer version was read only in its header and grep hits. |
| Stale second screen marker | CHECKOUT [CODE-CONTRADICTED] | `SHIM_MARKERS[1]` (`:774`) is the old question wording; the current text is `Session name (Enter = auto-named, Ctrl+C = cancel; ...)` (`ccsession-orca:200`). No effect on claim launches today (a prompt-carrying launch is never asked). Open question C17. |
| No test joins `--auto-name` output to `SHIM_TITLE` | CHECKOUT [CODE-VERIFIED] debt | A change to `auto_name` could turn every claim into a warning. Open question C19. |
| Bare `orca` everywhere | CHECKOUT [CODE-VERIFIED] | The claim script and ccsession (`ccsession:534,537,549-555`) use the bare name; the watcher resolves `orca-ide` first. See the DEFECT in 5.3. |
| Claim preflight and ccsession disagree on `CLAUDE_CONFIG_DIR` | CHECKOUT [CODE-VERIFIED] | Open question C18. |
| `SHIM_TITLE` matches because of one live title copied into a test | HISTORICAL observation, 2026-11-08 | Title survival in `terminal show` is not otherwise pinned; Orca shows the newest of the renamed and last OSC title (G05 R4). |
| Orca-side: how the Claude command and prompt are joined; `ORCA_PANE_KEY` across restart; 60 s readiness failure semantics | ORCA-CHECKOUT read; host values [UNVERIFIED] | G05 R1, R2, R7. |
| Never-as-worker for `/sc:issue` is prompt text only | CHECKOUT [CODE-VERIFIED] | No code in either launcher refuses a worker; `uv run ... orca_worktree.py` has command word `uv`, so the gate does not match it (header `:60-61`). |

**Extension points:** To add a launch step: `cmd_launch` gate order (`:1274-1409`) and a new warning code in `WARNING_ORDER`, with tests in `test_issue_orca_worktree.py` (groups LA, IR). To change the watcher's prompt: only `build_claim_prompt` and `PROMPT_PATTERN` (`launch.py:33,84`); `test_security_invariants.py:204` pins the literal 12-element argv. To add an Orca binary name: `_ORCA_CLIS` in `install_user_setup.py:35` (imported by `launch.py`; parity pinned by `tests/issue_watch/test_find_orca_parity.py`); the claim script's literal `orca` is a separate edit. A supervised-worker launcher: N/A, not built.

---

### 5.5 Orca-Side Enforcement (Development Source)

**Purpose:** Records what Orca itself enforces about helper starts and report routing, read from Orca source. This is not IronClaude code. It matters because WC-13 (5.1) says a worker never starts workers "at any depth setting", while Orca's own controls differ by build: the development checkout refuses a worker's helper start by default and the installed build files do not. Source was read only; no Orca process or CLI was started.

**Key Files** (all ORCA-CHECKOUT, `/home/coder/workspaces/IronOrca`, `main`, commit `dc57b3d6e81c9825446a520bf0aee8600a2f5586`, clean tree, version 1.4.214):

| File | Purpose |
|---|---|
| `src/main/runtime/rpc/methods/orchestration/worker/worker-start-authority.ts` | `resolveWorkerStartRun` (`:12`) and `assertHelperStartScope` (`:51`): who may call `worker-start` and what a worker may start. |
| `src/main/runtime/orchestration/dispatch-report-mailbox.ts` | `isDispatchReportType` (`:5`), `activeCreatorDispatch` (`:16`), `dispatchReportMailbox` (`:31`): where a helper's reports go. |
| `src/main/runtime/orchestration/db/runs/worker-run-binding.ts` | `findCallerWorkerDispatches` (`:11`), `workerRunBindingRefusal` (`:45`), `unboundWorkerMessage` (`:76`). |
| `src/shared/nested-worker-depth.ts`, `src/shared/default-global-settings.ts` | Depth cap default (`nested-worker-depth.ts:4`, `default-global-settings.ts:153`). |
| `src/main/runtime/orchestration/db/dispatch-depth.ts` | `resolveChildDispatchDepth` (`:165`, throws `nested_worker_depth_exceeded` when `childDepth > maxDepth`, per research/05 5.2). |
| `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js` | INSTALLED-FILES counterpart; build record in `out/package.json`. |

**How It Works:**

1. **Worker-start authority.** The Run's bound coordinator may call `worker-start` for its Run (`worker-start-authority.ts:21-30`; a different `--run` gives `consumer_fenced`). A caller that coordinates no Run must prove exactly one active, non-self Dispatch of its own; it then starts only a local helper in that Dispatch's Run (`:31-47`). Any other caller gets `consumer_fenced` ("worker-start needs the coordinator bound to the Run, or a worker on an active Dispatch in it"). `assertHelperStartScope` rejects `--on` and `--terminal` (`invalid_argument`) and any Task not last run by a helper of this creator Dispatch (`task_not_found`, "start new helper work with --spec") (`:56-69`). Only caller: the `orchestration.workerStart` handler (`worker/workers.ts:42,56`). [CODE-VERIFIED]
2. **Race and depth.** The creator is re-proven inside the creating transaction (`worker-dispatch-start.ts:137-147`, per research/05), and the child depth is `resolveChildDispatchDepth(params.creator, params.maxDepth)` (`:167`). The check is `childDepth > maxDepth` refuses. A coordinator-started worker has depth 1; a helper start from it has child depth 2.
3. **Depth default differs by build.**

| Source | Default `nestedWorkerMaxDepth` | Effect on a worker's helper start (2 > cap?) |
|---|---|---|
| ORCA-CHECKOUT `dc57b3d6e` | 1 (`nested-worker-depth.ts:4`; `default-global-settings.ts:153`) | 2 > 1: refused by the cap. |
| INSTALLED-FILES `1.4.245-aidev02.9cfecdd30b2a` | 2 (`nested-worker-depth.js:10`; `default-global-settings.js:161-162`; legacy 1 migrated to 2 once; file comment: upstream v1.4.251+ defaults to 4) | 2 > 2 is false: NOT refused by the cap; a helper's own helper (child depth 3) is. |
| Running Orca, stored setting | not read | [UNVERIFIED] DEPLOYED-RUNNING. |

   At the installed default the only barrier keeping a worker from starting a helper is WC-13 text, which no IronClaude code enforces (the gate does not inspect `worker-start`). Derived from reading two sources, not from a run. The preamble mirrors the cap: `canDispatchSubWorkers = dispatch.depth < maxDepth` (`coordinator-task-dispatch.ts:123`; also `dispatch-methods.ts`, `deliver-worker-dispatch-preamble.ts`), so at cap 2 a depth-1 worker is told how to start helpers (`preamble.ts:219-256`) while WC-13 forbids it. [CODE-VERIFIED text; which text a worker obeys is [UNVERIFIED]]
4. **Dispatch-report mailbox.** `worker_done`, `heartbeat`, `escalation`, `status` and untyped messages are dispatch reports (`dispatch-report-mailbox.ts:5-13`); gates and handoffs stay with the Run's coordinator. `dispatchReportMailbox` returns `dispatch:<creator id>` while the creator Dispatch is in the same Run and `pending` or `dispatched`, else `run:<run id>` (`:16-36`), recomputed on every send, so a helper's reports follow creator settlement without rewriting routes. Callers: `send-methods.ts:150-153`, `ask-methods.ts:113`, `worker-topology.ts:176`, `terminal-resize-listeners.ts:147`. Coordinator-started workers have no creator Dispatch, so their reports go to `run:<id>` (this part is an inference from `resolveCreatorDispatchId` returning null for a caller without an active non-self Dispatch, not a run).
5. **Worker-run binding.** `workerRunBindingRefusal` refuses a caller that works a Dispatch in a Run (or in a Run it descends from) binding that Run (`worker_cannot_coordinate_own_run`), and refuses a takeover flag from a caller working an active Dispatch (`worker_cannot_take_over_run`) (`worker-run-binding.ts:45-73`). Callers: the bind path (`run-binding.ts:49`) and `resolveRunScope` (`run-scope.ts:187`). It is narrow: it is NOT called on `orchestration.runCreate` (`runs/runs.ts:31-55`, `db/runs/run-create.ts:7-50`), so a worker with an active Dispatch can create a new Run and become its bound coordinator; the depth cap is then the only source barrier on what it starts (the earlier report records that a new Run does not reset delegation depth, HISTORICAL, not re-derived). Same source at the installed build's commit (`git diff --quiet` of `run-create.ts`: no difference); the bundle's `runCreate` handler head shows no worker refusal.
6. **Orca's federated own-Run preamble variant** (`buildOwnRunSubDispatchSection`, `preamble.ts:240-256`, selected only for remote-host preambles) tells a remote worker to `run-create` its own Run. It is Orca's text, untraced end to end, and not evidence that IronClaude ships sub-orchestration.

**Public Interface:**

```ts
resolveWorkerStartRun(runtime, args: { coordinator; from: string; callerSession; runId?: string }): { run: RunRow; helperCreator?: DispatchContextRow }
assertHelperStartScope(db, creator: DispatchContextRow, args: { task?: TaskRow; params: { on?: string; terminal?: string } }): void
dispatchReportMailbox(db, dispatch): string          // "dispatch:<id>" | "run:<id>"
workerRunBindingRefusal(db, caller, runId, attempted: { takeover: boolean; bind: boolean }): OrchestrationError | null
```

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| `runtime.getNestedWorkerMaxDepth()` | Store setting | Read from Orca's settings store (`workspace-selectors.ts`, per research/05); not observable here. |
| Runtime-attested pane and incarnation identity | Orca internals | `resolveDispatchCreator` trusts runtime-attested identity; params are untrusted for remote matching. |

**Consumers:**

| Used By | How |
|---|---|
| `orchestration.workerStart`, send, ask, escalation, run-binding RPC paths | Live callers of every function above (none is dead code). |
| `WORKER-CONTRACT.md` WC-13 | Relies on these controls only partially; its ban is text (5.1). |

**Conventions & Patterns:**

- Orca fails closed for helper starts (`consumer_fenced`) and resolves report routes from current database state, not stored addresses.
- Always name the Orca build when stating a depth fact: checkout `dc57b3d6e` (1), installed files (2), running (unknown).

**Evidence and contradictions:**

| Item | Class and tag | Note |
|---|---|---|
| Checkout default 1 versus installed default 2 | ORCA-CHECKOUT and INSTALLED-FILES [CODE-VERIFIED, both] | Different builds of one repository, the installed commit 1048 commits ahead (`git rev-list --count`); neither value is wrong for its own build. |
| "Orca refuses a worker's helper start by default" | True for the checkout, false for the installed files | Never state it without the build. |
| Cited files identical at the installed commit except the depth default and the `runUse` takeover check | `git diff --quiet dc57b3d6e 9cfecdd30b2a... -- <file>` (research/05 section 1) | Whether the minified bundle equals that commit's output is shown only for the depth files, `runCreate` and `worker-dispatch-start` heads. |
| Orca-side depth fence for `dispatch`, `task-create`, `worktree create --agent`, `agent launch` | HISTORICAL / [UNVERIFIED] (earlier report `:402-407`, AC-0.7 quoted second-hand) | Only `worker-start` is traced; do not present WC-13's four other verbs as fenced by the cap. |
| Orca test suite that exercises helper routing (`structured-chat-worker-helpers.test.ts`) | Not run | Titles read only. |
| Subordinate (sub-orchestrator) mode | Deferred, not shipped | Not built in IronClaude (no command, skill, flag or contract role); barred by WC-13 text, not by an Orca refusal. |

**Extension points:** N/A for IronClaude: these files are Orca's. IronClaude can only (a) restate controls in the contract with the build named, and (b) pin them with a test against a recorded build, which does not exist. A change to the depth cap is an Orca setting ("Nested worker depth", Settings, Orchestration; the control is in the checkout's `OrchestrationPane.tsx`, line not re-read here). A subordinate role would need an Orca-side delegation path and an IronClaude contract change together; it is not designed here.

---

### 5.6 Installer, Orca Skills Install and Doctor

**Purpose:** Puts the Orca-facing components on a host and checks some of them: the worker contract and core guidance (`install_core.py`), the three guard hooks and their registrations (`install_hooks.py`), the ccsession launchers (`install_ccsession.py`), a request to Orca to install its own skills (`install_user_setup.py`), and a health check (`doctor.py`). IronClaude never ships the Orca skills; Orca is their only producer.

**Key Files:**

| File | Purpose |
|---|---|
| `src/superclaude/cli/install_core.py` | `KNOWN_CORE_FILES` includes `WORKER-CONTRACT.md` (`:27`); `install_core_files` copies core `.md` files to `~/.claude/`, skipping an existing file unless forced (`:70-72`) and warning about stale kept files (`:94-105`). |
| `src/superclaude/cli/install_hooks.py` | 611 lines. `_FRESHNESS_SCRIPTS` (`:42`) lists the gate (`:88`), identity hook (`:90`) and guard (`:93`); `_copy_scripts` (`:251-290`); `_merge_settings` (`:298`). |
| `src/superclaude/cli/install_user_setup.py` | `_ORCA_SKILLS` (`:34`), `_ORCA_CLIS` (`:35`), `_ORCA_TIMEOUT = 25` (`:39`), `_NETWORK_BUDGET = 30` (`:40`); `_find_orca` (`:198`), `install_orca_skills` (`:230`), `install_user_setup` (`:449`). |
| `src/superclaude/cli/install_ccsession.py` | `wire_ccsession` (`:11`): links `ccsession` and `ccsession-orca` into `~/.local/bin`, seeds the env file. |
| `src/superclaude/cli/doctor.py` | `run_doctor` (`:17`) runs seven checks; `_check_ccsession` (`:57`) is the only Orca-adjacent one. |
| `src/superclaude/cli/main.py` | Order of steps: `install` calls `install_core_files` (`:178`), `wire_ccsession` (`:209`), `install_hooks(force=force)` (`:217`), `install_user_setup(force=force)` (`:236`); `update` passes `force=True` to core (`:365`), hooks (`:394`) and user setup (`:404`). |
| `tests/cli/test_install_user_setup.py`, `tests/cli/test_install_hooks.py`, `tests/unit/test_install_ccsession.py`, `tests/unit/test_cli_doctor.py`, `tests/cli/test_update_command.py` | Pins, read not run; the update-command fixture stubs `install_orca_skills` and `install_plugins` (`test_update_command.py:33-54`), so no test runs the real Orca step through `install` or `update`. |

**How It Works:**

1. **Order.** `install`: core files, slash commands, agents, skills, `wire_ccsession`, hooks, templates, user setup (rules, output styles, settings defaults, Orca skills, plugins), codegraph phase, retired-MCP step; `update` is the same without the last two (per gap-P3-G03 D). A `False` from `wire_ccsession` makes both commands exit 1. Pinned by `test_update_command.py:94-110` (per G03).
2. **Hooks.** `_copy_scripts` copies each listed script flat into `<settings dir>/hooks/` and sets mode 0755; an existing destination is skipped unless `force` (`install_hooks.py:279-281`), reported as "Skipped ... (use --force to overwrite)" (`:204`). Registration merge (`_merge_settings`, `:298-491`, per research/03 B.3): ownership by exact command identity; an already-registered managed command is skipped unless `force`, refreshed in place when forced; new entries are inserted so `launch-job-identity.sh` stays last (`:460`); a settings backup is made first and the write is atomic. Consequence: a plain `superclaude install` keeps an older installed script and an outdated registration silently; `orca_worktree.py` tells the operator to run `superclaude install --force` for that case. The installer does not check that `jq`, `awk` or `uv` exist or that `disableAllHooks` is unset; only the claim preflight does, and only for the launch-level guard path.
3. **Orca skills request (`install_orca_skills`, `install_user_setup.py:230-278`).** If not forced and all three `~/.claude/skills/<name>/SKILL.md` exist: "already installed", Orca not contacted. Else `_find_orca()` probes `orca-ide` then `orca` with `skills list --json` (10 s each) and accepts only exit 0 with a topic named `orca-cli` (`:198-221`; a bare `orca` on Linux is often the GNOME screen reader). Then it runs `[orca, "skills", "install", "--agent", "claude-code", "--skill", "computer-use", "--skill", "orca-cli", "--skill", "orchestration"]` with timeout `max(1.0, min(25, deadline - now))` (`:224-227,243-253`), no `--force`, no `env=` argument. Every return path has `True` first (`:239,242,263,278`), so Orca absence, failure, timeout or partial install does not fail `install` or `update`, except a malformed `skills list --json` reply, which raises out of `_find_orca` (it iterates `topics` after the `try`, `:219`; see the evidence table below, L32 and owner question C3); `force` only bypasses the "already installed" skip and is never forwarded to Orca (an edited copy is skipped and reported by Orca). One 30 s deadline (`:451`) is shared with the plugin step.
4. **Where Orca writes.** Orca's `skills install` writes the shared `~/.agents/skills` folder and links into each detected agent's folder; for Claude the root is `~/.claude/skills`, replaced by `<CLAUDE_CONFIG_DIR>/skills` when that variable is set in the child's environment (ORCA-CHECKOUT, per gap-P3-G03 A.5). The installer's check uses `home/.claude/skills`, so with `CLAUDE_CONFIG_DIR` set the "already installed" test and the `n/3 files present` post-check can disagree with where Orca wrote (derived from source, not observed; open question C4). Orca's own help says the request "needs no network"; the code comment `install_user_setup.py:36-38` that says it downloads is [CODE-CONTRADICTED], low impact.
5. **ccsession wiring.** `wire_ccsession` refuses (returns `False`) on missing or symlinked skill files, links `~/.local/bin/ccsession` and `ccsession-orca` (an absent `ccsession-orca` is a warning, not a failure), and seeds `~/.claude/ccsession.env` from the example only when missing. It never configures Orca's Claude command setting; pointing Orca at `ccsession-orca` is a manual step documented in `ccsession-tag/README.md:211-226` and `core/CLAUDE.md:51`, and neither installer nor doctor verifies it.
6. **Doctor.** Seven checks: pytest plugin, agents, skills, configuration, ccsession, codegraph, retired MCP (`doctor.py:29-49`). `_check_ccsession` (`:57-131`) requires the skill folder, `ccsession`, `ccsession-orca`, both hook scripts, the env file, both `~/.local/bin` links resolving to the skill scripts, and `SessionStart`, `UserPromptSubmit` and `SessionEnd` registrations; a missing `~/.local/bin` on `PATH` adds a warning to the check name only. The skills check fails only for skills named by `> Skill <name>` lines in installed commands, and no command names `orchestration`, `orca-cli` or `computer-use`, so doctor can never fail for a missing Orca skill. Doctor checks none of: an Orca CLI, the Orca skills, the three guard hooks' presence or registration, `WORKER-CONTRACT.md`, the Orca Claude-command setting. It fails where the installer only warns (missing `ccsession-orca`, an unmanaged link), so `install` can exit 0 while `doctor` exits 1.
7. **Host observation (HOST-INSTALLED; this host only; research 2026-11-11, `cmp` of all eight files re-run at about 02:14 UTC on 2026-11-12, after the installed files' ctime of 2026-11-12 01:59:25 UTC; matrix in 3.0.3).** The installed set is mixed relative to refs: guard, identity hook, `orca_worktree.py`, the ccsession README and `CLAUDE.md` equal ORIGIN/MASTER only (installed `CLAUDE.md` equals `origin/master`, not HEAD); the worktree gate equals HEAD and ORIGIN/MASTER and differs from the working tree (uncommitted message change); an installed copy of `launch-level-pre-push.sh` exists in `~/.claude/hooks/` and equals ORIGIN/MASTER (its use as a git hook was not observed); `WORKER-CONTRACT.md` equals HEAD and the working tree but not ORIGIN/MASTER (338 lines there, with a coordinator preflight at `:217`, commit `146be6fc3`), so every `WORKER-CONTRACT.md` line number in this reference holds for HEAD and the installed copy only; `HOW-WE-WORK.md` equals none of the three. The installed `CLAUDE.md` and gate still carry the older ownership wording. Host `settings.json` registers the three guard hooks and the ccsession hooks; `disableAllHooks` is unset. The Orca stub `~/.claude/skills/orchestration/SKILL.md` is Orca-shipped text identified by digest; which invocation wrote it is not established (no install log exists). No installation rollout is claimed by this reference.

**Public Interface:**

```text
install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]
install_hooks(target_path: Path | None = None, force: bool = False) -> Tuple[bool, str]   # install_hooks.py:153
install_orca_skills(home: Path | None = None, deadline: float | None = None, force: bool = False) -> Tuple[bool, str]
install_user_setup(force: bool = False) -> Tuple[bool, str]
wire_ccsession(home: Path | None = None) -> tuple[bool, str]
run_doctor(verbose: bool = False) -> Dict[str, Any]    # {"checks": [...], "passed": bool}
superclaude install [--force] | update | doctor [--verbose]
```

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Orca CLI on `PATH` (`orca-ide`, `orca`) | External | Optional; absence is a skipped step. |
| `~/.claude/settings.json` | Host config | Merged by `install_hooks`; malformed or non-object targets are refused. |
| `src/superclaude/hooks/hooks.json` | Source of registrations | Plugin mirror `plugins/superclaude/hooks/hooks.json` is a subset. |

**Consumers:**

| Used By | How |
|---|---|
| Operator | `superclaude install`, `update`, `doctor`, `./update.sh` (runs doctor last). |
| Claim preflight (5.4) | Tells the operator to run `superclaude install --force` for stale registrations. |
| Eval hook adapter | Calls `install_hooks(force=False)` into a per-eval HOME (per research/03 B.3). |

**Conventions & Patterns:**

- Installers take `home` or `target` parameters so tests run in a temp directory; `shutil.which` and `subprocess.run` are faked in tests.
- Existing destination files are kept without `force`; the run still reports success and prints a stale-file warning for core files.
- `make verify-sync` requires every `hooks/scripts/*.sh` to be listed in `_FRESHNESS_SCRIPTS`; the name still says "freshness" though it holds the guards.

**Evidence and contradictions:**

| Item | Class and tag | Note |
|---|---|---|
| `_find_orca` reads `topics` outside its `try` (`:216-219`) | CHECKOUT [CODE-VERIFIED] | A malformed `skills list --json` reply (exit 0, `topics` null or a non-list) can raise `AttributeError` or `TypeError` through `install_orca_skills` (`:240`), `install_user_setup` (`:456`) and `main.install` (`:236`, no `try`), aborting `install` at the user-setup step. Pinned as the original's behavior by `tests/issue_watch/test_find_orca_parity.py`. A well-formed Orca does not trigger it. Owner question C3. Not a DEFECT: the step runs; one path leaks an exception. |
| `docs/getting-started/installation.md:497-504` says the installer "always writes under `$HOME/.claude/`" | [CODE-CONTRADICTED] by derivation for the Orca step | Owner questions C4, C5. |
| `installation.md:359-360` "the step never makes `superclaude install` fail" | Imprecise | True of plugin and Orca requests; rules, output styles, settings defaults and the escaping exception can still fail it. |
| `main.py:478-485` doctor docstring lists three checks | Stale | `run_doctor` runs seven. |
| Behavior of a killed `skills install` (timeout at the shared 30 s deadline) | ORCA-CHECKOUT read; live [UNVERIFIED] | Orca's own comment: an interrupted two-rename update leaves `.orca-old` for the next plan to restore (`swap.ts:82-106`, per G03 R1). |
| `~/.claude` mixed install set | HOST-INSTALLED, moment-in-time | Matrix in 3.0.3 (`cmp` re-run 2026-11-12); re-read `git status` and `cmp` at assembly. |

**Extension points:** Add an Orca skill: edit `_ORCA_SKILLS` (`install_user_setup.py:34`; the name must be one Orca ships; the count 3 is hard-coded in `tests/cli/test_install_user_setup.py:289,358`, and also named in `installation.md:361` and the `main.py:233,403` headers). Add an Orca binary name: edit `_ORCA_CLIS` (`:35`; `launch.py` imports it). Add a launcher beside `ccsession-orca`: `install_ccsession.py:41`, `doctor.py:62,65-76,77`, and the fixtures in `tests/unit/test_install_ccsession.py` and `tests/unit/test_cli_doctor.py`. Add a guard hook: `_FRESHNESS_SCRIPTS` plus `hooks.json`, then `make sync-dev` and `make verify-sync`; installed copies change only through `superclaude install --force` or `update`.

---

### 5.7 Worker Result Channel (`return-contract.yaml`)

**Purpose:** Carries a worker command's result from the worker to the coordinator: a command run with `--unattended` writes `<report-dir>/return-contract.yaml`, the worker maps its `worker_status` to `worker_done --outcome` and passes the path, Orca carries `--report-path` without opening the file, and the coordinator opens it and admits or rejects the result. The whole channel is a text protocol: the writer and the reader are language-model sessions, and no executable in `src/` produces, parses or routes on the worker fields.

**Key Files:**

| File | Purpose |
|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md` | The only complete schema, WC-4 (`:32-39`); outcome mapping WC-5 (`:59`); reader rules (`:237-246`); nested-result rule (`:25`). Prose, no machine schema. |
| `src/superclaude/commands/*.md` (31 files with `## Unattended mode`) | Per-command `Contract.` bullet: where the file lands, what `report_path`, `artifacts` and the status mapping mean for that command. |
| Producer skills with a field-level spelling | `skills/sc-workflow-protocol/refs/return-contract.md` (worker block `:43-57`), `sc-brainstorm-protocol/SKILL.md` (`:384-392`), `sc-impact-protocol/SKILL.md` (`:99-102`), `sc-graph-protocol/SKILL.md` (`:111-115`), `sc-init-lite-protocol/SKILL.md` (`:61`) (per gap-P3-G04 3.1). |
| `src/superclaude/cli/reflect/contract.py` | `parse_contract` (`:65`, `yaml.safe_load` at `:77`, tolerates unknown top-level fields) and `derive_verdict`: reflect's own contract, not `worker_status`. |
| `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` | Reads the workflow PACKAGE contract (`:325-327`: `contract_version == "1.1"`, matching slug, status `success` or `partial`), not the worker contract. |
| `tests/skills/test_worker_contract.py` | Static pins: `RULE_PHRASES` WC-4, WC-4-mapping, WC-4-missing-directory-error, WC-5 (`:102-149`); `UNATTENDED_EXPECT` (`:438`, 31 keys); `UNATTENDED_COMMANDS` derived (`:746`). |

**How It Works:**

1. **Schema (WC-4, `:33`).** Top-level keys: `worker_contract_version` (`"1"`), `worker_status` (`succeeded`, `partial`, `failed` or `blocked`), `command` (the exact command line), `report_path` (main deliverable, may be null), `artifacts` (every other file written, excluding paths git ignores and paths outside the repository, `:34`), `blocked_question` when blocked, `reason` when failed (for `/sc:implement` also when blocked, carrying the STOP code). The field is `worker_status`, not `status`, because workflow, adversarial and reflect contracts already use `status` with other values (`:35`).
2. **Where the file lands (`:15`, `:32`).** Exactly one report directory per brief: the command's own directory-valued `--output` or `--output-dir`, or `--report-dir`. Neither or both is refused: the command does no work, writes nothing and prints the exact chat error `unattended mode needs exactly one report directory: ...` (`:38`). That string occurs only in the contract and `test_worker_contract.py:120`; no command file emits it verbatim.
3. **Four layouts** (gap-P3-G04 3.3; the contract names only the first two, for brainstorm and reflect, `:35`): (a) worker fields merged into the command's own contract (brainstorm and reflect with `--output`; impact and graph with `--output-dir`; also cli-portify, release-split, auggie-review); (b) a separate worker contract at `<report-dir>/return-contract.yaml` that lists the command's own contract in `artifacts` (adversarial, workflow, and brainstorm and reflect with `--report-dir`); (c) a full contract, existing fields plus worker fields, in `<report-dir>` (impact and graph with `--report-dir`); (d) a worker-only file (the remaining commands).
4. **Status mapping (`:36`).** `success` to `succeeded`, `partial` to `partial`, `failed` to `failed`, `stopped-precondition` to `failed`, and the flag-STOP `blocked` of impact and graph to `failed`. It omits `dry-run`, which reflect and brainstorm map to `succeeded`; other commands carry their own mapping in the `Contract.` bullet (release-split `split-approved`, `no-split`, `split-with-remediation`; cleanup-audit checkpoint stop). Only troubleshoot maps its own `blocked` to `blocked`.
5. **One flow (`/sc:workflow` as a worker, gap-P3-G04 section 2).** Coordinator brief with a `Command:` line and a unique report directory; worker invokes the command through its Skill (WC-7); the skill generates the plan package, writes the package contract (contract 1.1) and then the worker contract on every outcome; the worker reads its own contract's `worker_status` (never the package's `status`) and sends `worker_done` once with `--outcome failed` for `failed`, `blocked` or no contract, else `succeeded` (`:59`); the coordinator opens the file (`:39`, `:93`) and applies `:237-246`. Any other `worker_status` value is treated as `failed` (`:59`): the designed safety net, because nothing validates the file.
6. **Readers.** Worker side: the worker LLM (`:59`). Coordinator side: the coordinator LLM and its run notes (`:242`, `:246`). Nested: the calling command reads the nested contract per `:25`. Code readers exist only for other contracts: the reflect wrapper (`contract.py:65-82`; `derive_verdict` routes a missing contract with child exit 0 to blocked, reason `contract-missing`, and any non-zero child exit to blocked, reason `child-crash`), the workflow-package archive check, and the swarm and cli-portify pipelines for their own contracts. Orca's role ends at transporting `--report-path`; Orca-side use beyond settlement was not traced (research/02 5.2; G04 R8).
7. **Negative result.** A search of `src` for `worker_status`, `worker_contract_version` and `blocked_question` in `.py`, `.sh`, `.ts`, `.js`, `.json`, `.yaml`, `.yml` and `.toml` files returned zero matches (re-run 2026-11-12, CHECKOUT). Every hit is in a `.md` file. The `plugins/` mirror carries the `## Unattended mode` section for 2 of the 31 converted commands in `src/superclaude/commands` (`plugins/superclaude/commands/recommend.md` and `workflow.md`, `grep -rl '^## Unattended mode' plugins/superclaude/`, 2026-11-12) and `plugins/superclaude/core/` has no `WORKER-CONTRACT.md` and no `CLAUDE.md`; the plugin build is not equivalent to the source (G04 R7, answered by this read).
8. **`/sc:implement` has no producer.** The contract speaks of an implement worker contract (`:33`, `:243`, `:250`), but `commands/implement.md` and `skills/sc-implement-protocol/**` contain no `unattended`, `worker_status` or `WORKER-CONTRACT` text (count 0, re-run 2026-11-12), and implement is in neither the P1 nor the P2 list. Scope decision of record: the worker-contract plan `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/source.md` (section 3 row `implement`, section 6 phase P4, section 9 approved decisions of 2026-11-02; lines per gap-P3-G04 5.1), pinned by the deferral legend `tests/skills/test_worker_contract.py:1932` and the rows at `:2349,2357,2365` ("/sc:implement is converted in P4"). This is a future-phase item, not a DEFECT; the contract text is forward-looking. How a coordinator should read a successful implement run today is [UNVERIFIED]; the ledger is the evidence until then. Open question C7.

**Public Interface:**

```yaml
# <report-dir>/return-contract.yaml (WC-4; types as implied by the prose and producer examples)
worker_contract_version: "1"
worker_status: succeeded | partial | failed | blocked
command: "<exact command line>"
report_path: <path> | null
artifacts: [<paths>]
blocked_question: "<question>"      # when blocked
reason: "<text>"                     # when failed (implement: also when blocked, STOP code)
```

```text
worker_done --task-id <T> --dispatch-id <D> --outcome succeeded|failed --report-path <report-dir>/return-contract.yaml   # syntax authority: the preamble
```

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Each command's `## Unattended mode` section | Text | Fixes directory flags, gate resolutions, status mapping. |
| Orca `worker_done` transport | External | Carries `--report-path`; "does not check the file" (`:39`). |
| The coordinator reading `~/.claude/WORKER-CONTRACT.md` | Text | Not auto-loaded (5.2). |

**Consumers:**

| Used By | How |
|---|---|
| Worker session | Maps `worker_status` to `--outcome` (`:59`). |
| Coordinator session | Opens the file and admits or rejects (`:237-246`). |
| Calling commands (nested propagation) | Read the nested contract (`:25`; for example `commands/reflect.md`, `commands/task.md`, `commands/workflow.md`). |
| `tests/skills/test_worker_contract.py` | Pins phrases of the contract and 31 command sections; parses no produced file. |

**Conventions & Patterns:**

- `artifacts` leaves out gitignored and out-of-repository paths because WC-9 stages every listed path.
- A contract is written on every outcome, including stops before other output exists (`:37`); under the contract this is an instruction, so "no contract" maps to `--outcome failed`.
- Package contract (`<pkg>/return-contract.yaml`, `status: success|partial|failed`, read by code) and worker contract (`<report-dir>/return-contract.yaml`, `worker_status`, read by no code) are different files; never conflate them.

**Evidence and contradictions:**

| Item | Class and tag | Note |
|---|---|---|
| No code writes, parses or validates the worker fields; no test parses a produced file | CHECKOUT [CODE-VERIFIED] negative | A producer writing a wrong enum or `status` for `worker_status` would pass every test; the coordinator's admission rule is the net. |
| No produced contract was examined | [UNVERIFIED] | G04 R1: the field set is specified in prose and pinned as text. |
| `report_path` form (absolute versus repo-relative) differs by command | CHECKOUT [CODE-VERIFIED] | Reflect says absolute, workflow ref says repo path; contract gives no form (G04 R2). Open question C13. |
| `:36` mapping is incomplete (omits `dry-run` and per-command values) | CHECKOUT [CODE-VERIFIED] | Open question C14. |
| `blocked` has two meanings (person gate `:31`; flag STOP mapped to `failed` `:36`) | CHECKOUT [CODE-VERIFIED] | Open question C15. |
| `:35` names one merge mode for brainstorm and reflect; `--report-dir` modes and the impact and graph layout are not named | Stale-incomplete | Section 3.3 above is authoritative. |
| `/sc:implement` producer absent | Future-phase (P4), cited decision | Item 8. |
| `WORKER-CONTRACT.md:59,89,295,303-307` P0 and P1 conditionals read as historical | CHECKOUT [CODE-VERIFIED] stale | Pinned by tests. |

**Extension points:** To convert a command: add an `## Unattended mode` section (report-directory rule, gate resolutions, `Contract.` bullet naming `report_path`, `artifacts` and the status mapping, nested directories `<caller report-dir>/nested/<command>-<n>/`), add an entry to `UNATTENDED_EXPECT` (`test_worker_contract.py:438`; its checker requires `return-contract.yaml`, `~/.claude/WORKER-CONTRACT.md` and `--report-dir` in the section and no `src/superclaude/` path or Orca command name) and a phase tuple, update the flags table in the contract brief template (`:307-327`), run `make sync-dev` and reinstall. To add a field: edit WC-4 and the five producers that spell fields out, plus the `WC-4` entry of `RULE_PHRASES`. To validate produced files: no hook exists; a validator would be new code and a new test. Producer for `/sc:implement`: planned P4, not built.

---

## Routing dispositions

| Artifact routed to this output | Where used or disposition |
|---|---|
| `research/01-roles-authority.md` | 5.1 (roles, ownership wording, rulings, deferred mode); C.1 table folded into 5.5; gaps G1-G12 into 5.1 evidence table. |
| `research/02-lifecycle.md` | 5.2 (contract section 4, retries, wait, S-table, ladder, admission, SD-1); section 6.3-6.4 enforcement ceiling folded into 5.2 and 5.3. |
| `research/03-guards.md` | 5.3 (registration, gate, guard, identity, fail-open cases, ceilings, host drift); C.3 wording qualified by gap-P3-G06. Probe catalogue IDs not reproduced (cited as `G2-` rows only). |
| `research/04-launchers.md` | 5.4 (claim flow, watcher, shim check, version divergence, accepted agent-less create). |
| `research/05-orca-provenance.md` | 5.5 (authority, mailbox, run binding, depth default checkout versus installed). |
| `research/06-distribution-evidence.md` | 5.1 (ownership states, test pins), 5.6 (per-file installed provenance F6). Dev-guide staleness left to synth-05. |
| `research/gap-P3-G01.md` | 5.2 (preamble, heartbeat, liveness projection, retired scheduler) and 5.5 (depth and preamble consequence). Corrections C3-C6, C12 applied. |
| `research/gap-P3-G02.md` | 5.3 (name `orca` DEFECT, probes, determination, wording). Corrections table applied; probe IDs prefixed `G2-`. |
| `research/gap-P3-G03.md` | 5.6 (installer, Orca skills request, doctor, host observation, `_find_orca` exception, `CLAUDE_CONFIG_DIR`). |
| `research/gap-P3-G04.md` | 5.7 (schema, layouts, producers, readers, negative search, implement P4). |
| `research/gap-P3-G05.md` | 5.4 (ccsession title writer, shim check causes, key variables; the full 23-variable table is left to section 9.2 / synth-04). |
| `research/gap-P3-G06.md` | 5.3 (timeouts, fail-open qualification, probe of a killed guard). Speed figures are carried to section 11 by synth-04, only cited here as recorded results. |
| `research/web-01-claude-code-hook-execution.md` (W1) | 5.3 "Documented host behavior" (timeout, exit codes, order, `updatedInput`, permission modes), DOCUMENTED with URLs. |
| `research/web-02-claude-code-subagent-hooks.md` (W2) | 5.3 (subagent firing, `agent_id`, bypass routes, `session_id` gap), DOCUMENTED with URLs. |
| `gaps-and-questions.md` | Precedence rules A2 applied; owner questions C1-C4, C7-C15, C17-C19 and defect register D referenced as open, never as decisions; accepted limits B stated in evidence tables. |
| Remediation plan `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/` | Linked in 5.3 as a draft plan, not a fix. |
| Not used here (routed elsewhere) | `qa/*decision.md` (synth-05 verification log), `BUILD-REQUEST.md`, `research-notes.md`, earlier `RESEARCH-REPORT-sub-orchestrator-mode.md` (cited only as HISTORICAL where research files cite it). |

Blockers: none. Notes for the assembler: (1) re-read `git status` and the per-file `cmp` of installed files at assembly, since 5.1, 5.3 and 5.6 describe a moment-in-time state; (2) the DEFECT row, the "fail-closed" qualifier, the depth-default contrast and the P4 implement deferral must survive into sections 8, 10 and 14 unchanged.

Status: Complete

