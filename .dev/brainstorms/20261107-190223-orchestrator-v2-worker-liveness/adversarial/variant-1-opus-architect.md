# Worker Liveness for Orchestrator v2: Layered State Model with Pluggable Signal Adapters (variant 1, architect)

## 1. Overview and Goals

Status: design only (2026-11-07). No source, contract or Orca state was changed. Sources were read on 2026-11-07; Orca facts come from the enrichment artifact (`enrichment/codebase-context.md`), which read Orca `1.4.245-aidev02` help and guide text. No live worker was observed for this design, so every Orca runtime behaviour below is documented behaviour, not observed behaviour.

### Problem in one paragraph

The coordinator decides that a worker is "alive" from signals that only prove a process exists: timer heartbeats with an unchanged phase, one file's mtime, a helper name on screen, or no failure message (`.dev/issues/431/issue-body.md:14`). In run `run_93bfa00cae2b` that cost about four hours twice (`issue-body.md:16-17`), plus a closing `status` message filtered out of the wait for about four hours (`:19`), mailbox answers unseen for 35-40 minutes (`:20`), a permission prompt unnoticed for about 20 minutes (`:21`), turns ended between chain steps (`:22`) and a repeat of context thrashing (`:23`).

### Root cause, stated architecturally

Three concerns are fused today and must be separated:

1. **Evidence** (what a source observed, when, and what it proves).
2. **Verdict** (which named state a worker is in).
3. **Action** (what the coordinator does about it).

Today a heartbeat is evidence, verdict and "no action" all at once. Under WC-10 the coordinator "treats a missing heartbeat as absence, never as death ... acts only on Orca's stall proofs" (`src/superclaude/core/WORKER-CONTRACT.md:44`), and the canonical wait wakes only on `worker_done,escalation,question` (`enrichment/codebase-context.md:15`). So the only things that can move the coordinator are a positive stall proof or a message of a listed type. Every failure in #431 sits in the gap between those two.

The #409 research reaches the same separation for display: keep "work status, terminal/process liveness, observation freshness, message delivery and independent validation as separate fields", and a stale source must produce "an explicit unknown" (`.dev/research/orca-dashboard-20261105/REPORT.md:41`). This design applies that separation to supervision.

### Architecture at a glance

```text
  +-------------------- coordinator (Orca session the person opened) --------------------+
  |                                                                                      |
  |  Response Ladder  <--  Policy (detection rules, bounds, budgets)  <--  State Model   |
  |  (L0..L5 actions)       harness-neutral, versioned                    (named states) |
  |        |                                                                  ^          |
  |        v                                                                  |          |
  |   Actuator port                                              Observation port        |
  +--------|------------------------------------------------------------------|----------+
           |                                                                  |
   +-------v--------+   +-----------------+   +------------------+   +--------+---------+
   | Orca mailbox   |   | Orca fleet      |   | Orca terminal    |   | Filesystem       |
   | adapter        |   | adapter         |   | adapter          |   | activity adapter |
   | check/send/ask |   | worker-list,    |   | read --screen,   |   | worktree mtime,  |
   |                |   | worker-show     |   | wait tui-idle,   |   | report-dir files |
   |                |   | agentWait       |   | send --enter     |   |                  |
   +----------------+   +-----------------+   +------------------+   +------------------+
                         +--------------------------------------+
                         | Claude Code adapter (transcript via  |
                         | worker-read; hook journal in v2)     |
                         +--------------------------------------+
```

The core (state model, policy, ladder) names no Orca verb and no Claude Code file. Adapters translate harness facts into a fixed observation vocabulary (section 3) and translate ladder actions into harness calls (section 11).

### Goals

- **G1. Bounded detection.** Every observed failure state is detected within a stated bound: 15 minutes or less for idle, blocked and thrashing; one wait cycle for missed message types (`seed-brief.md:42`).
- **G2. No lost message types.** No wait can delay a worker message past one wait cycle, and unknown types are surfaced (`seed-brief.md:43`).
- **G3. Confirmed reads.** A reply counts as read only after the worker acknowledges it; an unacknowledged reply escalates to a terminal-typed copy within a stated bound (`seed-brief.md:44`).
- **G4. One response per state** from a fixed ladder with repeat caps (`seed-brief.md:45`).
- **G5. Safe with WC-10.** Silence can trigger only read-only probes and harmless nudges; stopping, retrying or releasing still needs positive evidence (`seed-brief.md:36`).
- **G6. Portable.** The core is harness-neutral; Orca and Claude Code are the first adapters (`seed-brief.md:34`, `:47`).
- **G7. Extensible.** A new signal, state, message type or harness is added by registering data or an adapter, not by editing the policy core.

### Non-goals

- No change to WC-6 (retry is a new Task), WC-7 (lifecycle messages only from the top-level session), WC-8 (no Orca calls in commands) or the preamble's ownership of cadence and verb syntax (`WORKER-CONTRACT.md:7`, `:38`, `:58`, `:69`).
- No cross-agent knowledge catalogue: that is the rest of #423 (`enrichment/codebase-context.md:45`). This design is the supervision layer that catalogue would sit on.
- No dashboard: #409 consumes the observation store defined here.

### Top-level requirements

- **FR-001.** The coordinator shall keep, per worker, separate records for evidence (observations), verdict (state) and action history (ladder steps taken), and shall never derive an action directly from a single raw signal without first assigning a state.
- **FR-002.** Every observation shall carry `source`, `observed_at`, `freshness` and a `proof_class` of `positive`, `absence` or `unknown`, so policy can tell "saw X" from "did not see Y".
- **NFR-001.** The core state model, policy and ladder shall name no harness-specific command, file path or screen text; those live only in adapters.
- **NFR-002.** The liveness vocabulary (states, signal kinds, payload schemas) shall be versioned (`ironclaude.liveness/1`), and a reader shall treat an unknown version or field as `unknown`, never as healthy.

## 2. Worker State Model

### Design principle: three orthogonal axes, one derived state

Following the Kubernetes split between liveness ("making progress"), readiness ("can take input") and startup (grace period) (`enrichment/research-light.md:18-22`), each worker is described on three independent axes. The named state is derived from them; it is never stored on its own.

| Axis | Values | Main sources |
|---|---|---|
| **Process** | `alive`, `exited`, `unverifiable` | Orca `projection.liveness` (`enrichment/codebase-context.md:18`) |
| **Interaction** | `working`, `idle_prompt`, `person_prompt`, `in_ask`, `unknown` | `agentWait`, `tui-idle`, screen class, outstanding `ask` |
| **Progress** | `advancing`, `flat`, `thrashing`, `unknown` | progress-heartbeat digest, transcript last turn, worktree activity, compaction count |

Plus two lifecycle facts read from the message log and disk: `worker_done_seen` (bool) and `contract_on_disk` (the `worker_status` in `<report-dir>/return-contract.yaml`, if any; WC-4, `WORKER-CONTRACT.md:31-37`).

Keeping axes separate is the main maintainability choice: a new signal only has to feed one axis, and a new state is a new row in the derivation table below, not a new code path.

### Named states

States marked (+) are additions to the eight the brief requires; they exist so every worker is always in exactly one state.

| State | Derivation (all must hold) | Entry condition | Exit conditions |
|---|---|---|---|
| **starting** (+) | Dispatched less than the startup grace (default 10 min) ago, no progress observation yet | `worker-start` returned ready | First progress observation -> `progressing`; grace expires with no observation -> evaluate normally |
| **progressing** | Process `alive`; Progress `advancing` within the quiet window Q (default 10 min) | Any progress observation newer than Q | Progress `flat` for Q -> `long-step-in-progress` or `idle-at-prompt`; any blocker evidence -> that blocked state |
| **long-step-in-progress** | Process `alive`; Interaction `working` (positive: busy screen, fresh transcript tool entry, or declared long step); Progress `flat` | Progress flat for Q while working evidence is positive | Progress advances -> `progressing`; working evidence disappears -> re-derive; declared step deadline passes -> stays here, flagged `over_deadline` |
| **idle-at-prompt** | Process `alive`; Interaction `idle_prompt` (positive); no `worker_done`; no outstanding `ask` | Idle observed with Progress flat | Nudge accepted and turn started -> `progressing`; contract on disk -> `finished-unreported` |
| **blocked-on-person-prompt** | Interaction `person_prompt` (positive `agentWait`, or screen class `permission_prompt`) | `agentWait` non-null or classifier match | Prompt gone (agentWait null, screen not matching) -> re-derive |
| **blocked-in-ask** | Worker sent `question` (or an `ask` is pending) and it is unanswered, or answered but unacknowledged (sub-state `awaiting-ack`) | `question` received | Coordinator answers -> `awaiting-ack`; ack received -> `progressing`; ack timeout -> ladder (section 7) |
| **context-exhausted** (compact-thrashing) | Progress `thrashing` (positive: thrash screen text, or compaction count over threshold) or context-limit text, with Progress digest flat | Classifier or compaction counter fires | Session cleared/restarted (new Task) -> old attempt settled; never self-exits |
| **unreachable/exited** | Process `exited` (positive stall proof), or `unverifiable` for two consecutive sweeps (absence; sub-state `unverifiable`) | Fleet adapter verdict | `exited` -> settle and maybe restart (WC-6); `unverifiable` -> stays until verdict changes or person decides |
| **finished-unreported** | `contract_on_disk` with a final `worker_status`, or a non-`worker_done` message that carries a report path or `worker_status`; and no `worker_done` | Disk read or message parse | `worker_done` seen -> `settled` |
| **settled** (+) | `worker_done` seen | `worker_done` | Terminal for this attempt |

- **FR-003.** The coordinator shall assign every unsettled worker exactly one state from the table above at every sweep; if no row matches, the state is `unknown` and is treated as a trigger for the L1 probe, never as healthy.
- **FR-004.** States shall be derived with this precedence when several rows match: `settled` > `unreachable/exited (exited)` > `blocked-on-person-prompt` > `context-exhausted` > `finished-unreported` > `blocked-in-ask` > `idle-at-prompt` > `long-step-in-progress` > `progressing` > `starting` > `unverifiable`. Rationale: states that need a person or that waste the most time win; a state that needs no action never hides one that does.
- **FR-005.** A state transition shall be recorded with the observations that caused it (ids, sources, times), so every ladder action is traceable to evidence.

### Transition diagram

```text
             +----------+   first progress    +-------------+
  dispatch ->| starting |-------------------->| progressing |<-----------------------------+
             +----------+                     +------+------+                              |
                                                     | progress flat for Q                 |
                         +---------------------------+-------------------------+           |
                         | working evidence          | idle evidence           |           |
                         v                           v                         |           |
              +----------------------+     +-----------------+   nudge ok      |           |
              | long-step-in-progress|     | idle-at-prompt  |-----------------+-----------+
              +----------+-----------+     +--------+--------+                             |
                         | thrash evidence          | contract on disk                     |
                         v                          v                                      |
              +-------------------+       +---------------------+  worker_done  +---------+
              | context-exhausted |       | finished-unreported |-------------->| settled |
              +-------------------+       +---------------------+               +---------+
  any state --agentWait--> blocked-on-person-prompt --prompt gone--> re-derive
  any state --question---> blocked-in-ask --answer--> awaiting-ack --ack--> progressing
  any state --liveness exited--> unreachable/exited --(settle, WC-6)--> new Task
```

## 3. Signals and Adapters

### Observation record (the port between adapters and core)

Every adapter emits records of one shape. This is the single contract adapters must satisfy; the core never sees raw harness output.

```yaml
schema: ironclaude.liveness/1
worker: <dispatch id>            # identity key; Task id kept alongside
kind: <signal kind, from the registry below>
axis: process | interaction | progress | lifecycle | delivery
value: <kind-specific scalar or small map>
observed_at: <ISO UTC, when the adapter looked>
evidence_at: <ISO UTC, time of the underlying event, if the source gives one>
source: <adapter id and version, e.g. orca-fleet/1.4.245>
proof_class: positive | absence | unknown
proves: <one short phrase from the registry>
```

- **FR-006.** Freshness shall be computed as `now - observed_at` for the look and `now - evidence_at` for the event; a record older than two sweep intervals shall be downgraded to `unknown` (the #409 rule that a stale source is an explicit unknown, `REPORT.md:41`).
- **FR-007.** A record whose adapter reports the capability as unsupported (Orca's `capability_unsupported` reason, `enrichment/codebase-context.md:18`, or a worker with no terminal, `:23`) shall be `proof_class: unknown`, and the policy shall fall back to the next signal for that axis.

### Cost tiers

- **T0 (free):** data already in a delivered message batch (heartbeats, status, any type).
- **T1 (one call for the whole fleet):** `worker-list` projection and `worktree ps --agent-wait` (`enrichment/codebase-context.md:18-19`).
- **T2 (one call per worker):** screen read, transcript tail, worktree scan, report-dir read. Run only for workers whose T0/T1 evidence is flat or suspicious.

### Signal registry and evaluation

| # | Signal | Source (adapter) | Proves | Does not prove | Cost | Brittleness | Core or adapter |
|---|---|---|---|---|---|---|---|
| S1 | Timer heartbeat (today) | Mailbox (Orca `heartbeat`; free-text `--phase`, raw `--payload`, `enrichment/codebase-context.md:14`) | The top-level session completed a turn step recently | Progress: case 1 sent "implementing" for about four hours while thrashing (`issue-body.md:16`) | T0 | Low | Kind is core; transport is adapter |
| S2 | **Progress-bound heartbeat** (new payload) | Same verb, payload schema below | A self-reported step id and step-local counter, so "same step, no new actions" becomes visible | Truth: it is a claim by the worker; a confused or thrashing model can misreport. Not sent during `ask`, `check --wait` or subagent fan-out (`WORKER-CONTRACT.md:44`, `:61`) | T0 | Low (IronClaude owns the schema) | Schema is core; transport adapter |
| S3 | **Whole-worktree activity** | Filesystem adapter: newest mtime under the worker's worktree, pruning `.git`, `.venv`, `node_modules`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, `dist`, `build` and the coordinator's own files | Something wrote a file at time T | Who wrote it in a shared worktree (WC-11 allows shared feature worktrees, `WORKER-CONTRACT.md:45`); progress in read-only steps (research, review); case 3 showed one file's mtime misleading (`issue-body.md:18`) | T2, bounded by pruning; recursive scan, so cap depth and entries | Low | Core kind; FS adapter is harness-neutral |
| S4 | **Terminal state classification** | Terminal adapter: `terminal read --screen`, `terminal wait --for tui-idle` (`enrichment/codebase-context.md:21-22`) plus a versioned pattern file per harness | Positive match: thrash text (`issue-body.md:43`), permission prompt (`:44`), idle prompt, busy indicator | Anything on a non-match: an unknown screen is `unknown`. Not available for workers without a terminal | T2 | **High**: screen text changes with harness versions | Classes are core; patterns are adapter data |
| S5 | **Transcript timestamps** | Claude Code adapter via `worker-read --source transcript` (never a guessed path, `enrichment/codebase-context.md:58`) | Time of the last model turn or tool call; whether the final turn ended without `worker_done` (an Orca stall proof, `:20`); compaction events (entry type UNVERIFIED) | That the activity was useful (a thrash loop produces fresh entries) | T2 | Medium: internal format; trailing entries lack timestamps, so scan back (`:58`) | Adapter only |
| S6 | **Per-step deadlines** | Brief (`Expect:` line, section 10) plus S2 step ids | That a declared step overran its expected time | That the worker is stuck: an overrun is a reason to probe | T0 | Low | Core |
| S7 | **All-type wait filter** | Mailbox adapter: `check --wait --types <set> --timeout-ms` (types are only the wake condition; the batch is never filtered, `enrichment/codebase-context.md:15`) | Every delivered message is seen within one wait timeout | Nothing about silent workers | T0 | Low | Core rule; adapter syntax |
| S8 | **Read acknowledgement** | Worker sends an ack `status` (section 7) | The worker's top-level session processed the reply | That the worker acted correctly on it | T0 | Low | Core protocol |
| S9 | Fleet liveness verdict | Fleet adapter: `projection.liveness` `live`/`unverifiable`/`exited`, `attention.categories`, `requiresAction`, `nextAction` (`enrichment/codebase-context.md:18`) | `exited` is a positive stall proof (`:20`) | `live` is PTY liveness only: "A live terminal can still hold a dead or stuck agent" (`:18`) | T1 | Low | Adapter maps to Process axis |
| S10 | Person-only prompt | Fleet adapter: `observation.agentWait` (hook, prompt text or title evidence; null = looked, none; absent = never looked) (`enrichment/codebase-context.md:19`) | Positive: the worker is parked on a prompt only a person can answer | null does not prove "working"; absent means "never looked" (`unknown`) | T1 | Low to medium | Adapter maps to Interaction axis |
| S11 | Contract on disk | FS adapter: `<report-dir>/return-contract.yaml` (`WORKER-CONTRACT.md:31-35`) | The command finished with a final `worker_status` | That `worker_done` was sent (case 4) | T2, one small file | Low | Core (contract is IronClaude's) |
| S12 | Harness lifecycle hooks (v2) | Claude Code hooks `Notification` (`idle_prompt`, `permission_prompt`), `Stop`, `PreCompact`, `SessionStart` (`enrichment/research-light.md:39-45`) written to a local journal | Typed event at the moment it happens | Delivery: hooks may not fire in every client (`research-light.md:46`); `idle_prompt` timing UNVERIFIED (`:45`) | T2 read of a small file | Medium | Adapter; journal schema core |

### S2: progress-bound heartbeat payload (schema `ironclaude.progress/1`)

The preamble still owns the heartbeat verb and cadence (`WORKER-CONTRACT.md:7`); IronClaude only defines what goes into the raw `--payload` (`enrichment/codebase-context.md:14`), which no IronClaude convention defines today (`:64`).

```json
{
  "schema": "ironclaude.progress/1",
  "task": "<task id>",
  "step": "c2:implement:T05",
  "step_started_at": "2026-11-07T12:01:00Z",
  "step_seq": 14,
  "actions_since_last": 3,
  "last_action_at": "2026-11-07T12:20:41Z",
  "expect_until": "2026-11-07T13:00:00Z",
  "context": "ok | compacted_recently | near_limit | unknown",
  "pending_ack": ["<message id>"]
}
```

- `step`: `c<n>` is the index of the brief's `Command:` line being run, then an optional command stage the session can name (for `/sc:implement`, the ledger task id). Changes only when the worker moves on.
- `step_seq`: increments on each heartbeat **only** when `actions_since_last > 0`. A repeated `step_seq` is the core "flat" signal.
- `context`: the session's own view; `compacted_recently` when it saw a compaction since the last heartbeat. Self-report, so advisory.
- `pending_ack`: replies seen but not yet acted on (section 7).
- **FR-008.** The worker session shall send S2 payloads on every heartbeat it already sends; it shall add no heartbeat beyond the preamble cadence except the ack in section 7.
- **FR-009.** The coordinator shall treat S2 as a claim: "advancing" requires S2 to advance **and** at least one independent signal (S3, S5, S12) not to contradict it within the same sweep. S2 alone can move a worker to `flat`; it can never on its own prove `advancing` for longer than 2Q.

### Adapter set for the first harness pair

| Adapter | Harness | Signals | Actuators |
|---|---|---|---|
| `orca-mailbox` | Orca | S1, S2, S7, S8, all message types | send reply, ask follow-up |
| `orca-fleet` | Orca | S9, S10 | none (read-only) |
| `orca-terminal` | Orca + terminal-backed worker | S4 (screen, tui-idle) | typed nudge with `--wait-submit` receipt (`enrichment/codebase-context.md:23`) |
| `claude-code-transcript` | Claude Code, read through Orca `worker-read` | S5 | none |
| `fs-activity` | any | S3, S11 | none |
| `claude-code-hooks` (v2) | Claude Code | S12 | none |

## 4. Detection Rules and Time Bounds

### Timing parameters (defaults; one table, so tuning is a data change)

| Parameter | Default | Why |
|---|---|---|
| `W` wait timeout | 5 min | Bounds message-wake delay for any type left out of the wake set (S7). Today's canonical 15 min (`enrichment/codebase-context.md:15`) plus "three consecutive empty waits" before a sweep gives up to 45 min (`:20`), which cannot meet G1 |
| `S` sweep interval | 5 min (every wait return, at most once per `S`) | T1 calls cover the whole fleet in one call each |
| `Q` quiet window | 10 min | Longest no-progress gap tolerated before a T2 probe; above the WC-10 4-minute Bash split (`WORKER-CONTRACT.md:44`) plus one heartbeat interval (preamble cadence, UNVERIFIED value) |
| `G` startup grace | 10 min | Session boot and resume (Kubernetes startup-probe analogue, `enrichment/research-light.md:22`) |
| `A` ack timeout | 5 min when the worker is blocked in `ask`; 10 min otherwise | An `ask`-blocked worker returns at once; others pull at checkpoints (WC-12, `WORKER-CONTRACT.md:59`) |
| `D` default step deadline | 60 min, overridden by the brief's `Expect:` line | A declared long step is not a stall |
| `F` fan-out allowance | 30 min of no heartbeat while the screen shows subagent work | WC-10 accepts the fan-out gap (`WORKER-CONTRACT.md:44`) |

- **NFR-003.** All timing parameters shall live in one named parameter block (coordinator run notes in v1; a config file in v2) and shall be overridable per Task by the brief, never by the worker.

### The sweep (runs on every wait return, at most once per `S`)

```text
sweep():
  batch   <- messages delivered by this wait (T0)            # every type, section 6
  fleet   <- orca-fleet.list()                               # T1: liveness, attention
  waits   <- orca-fleet.agent_waits()                        # T1: agentWait per worker
  for w in unsettled workers:
      obs <- T0 + T1 observations for w
      if axis evidence is flat, absent, unknown or suspicious for >= Q (or a deadline passed):
          obs += T2 probes for w in cost order: contract-on-disk, transcript tail,
                 tui-idle (short timeout), screen class, worktree activity
      state <- derive(obs)                                   # section 2 table + precedence
      ladder.step(w, state)                                  # section 8
```

- **FR-010.** The coordinator shall run the sweep at least every `S` minutes while any worker is unsettled, whether or not the wait returned a message.
- **FR-011.** T2 probes shall run only for workers whose T0/T1 evidence is flat, absent, unknown or past a deadline, so steady-state cost is two fleet calls per sweep regardless of fleet size (NFR-004).
- **NFR-004.** Steady-state sweep cost shall be O(1) harness calls for a healthy fleet and O(k) for k suspicious workers.

### Per-state rules

| State | Trigger (cheap) | Confirming probe | Detection bound |
|---|---|---|---|
| progressing | S2 `step_seq` or `step` changed within Q, and no contradicting S3/S5 | none | n/a |
| long-step-in-progress | S2 flat for Q | Positive working evidence: busy screen class, transcript entry newer than Q, or S3 newer than Q; or the brief declared this step long | Probe at Q; flagged `over_deadline` at `D` (or `Expect:`) |
| idle-at-prompt | S2 flat, or no heartbeat at all, for Q with no outstanding `ask` | `tui-idle` returns idle within a short timeout, or screen class `idle_prompt`; and transcript final turn ended with no `worker_done` | **Q + S = 15 min** |
| blocked-on-person-prompt | S10 `agentWait` non-null in any sweep | Optional screen class `permission_prompt` (for the report text) | **S + S = 10 min** worst case |
| blocked-in-ask | A `question` in the batch (T0), or S2 shows an `ask` outstanding | none needed | One wait cycle, **W = 5 min**; ack bound **A** after the answer |
| context-exhausted | Heartbeats keep arriving while S2 `step_seq` is flat for Q (the case 1 signature), or S2 `context` reports two compactions inside 30 min | Screen class `compact_thrashing` (`issue-body.md:43`), or transcript shows 3 or more compactions within 30 min (entry type UNVERIFIED), and S3 shows no writes since the step began | **Q + S = 15 min** |
| unreachable/exited | S9 `exited` | none: `exited` is a positive stall proof (`enrichment/codebase-context.md:20`) | **S = 5 min** |
| unreachable (unverifiable) | S9 `unverifiable` in two consecutive sweeps | T2 probes, which may themselves be unavailable | **2S = 10 min** to report; never auto-restart (WC-6, `WORKER-CONTRACT.md:72`) |
| finished-unreported | Any non-`worker_done` message carrying `report_path`, `worker_status` or a contract path; or S11 contract with a final `worker_status` found during an idle probe | Read the contract (S11) | **W = 5 min** via messages; **Q + S = 15 min** via the idle path |
| starting | Dispatched less than G ago | none | Ends at G |

- **FR-012.** Absence of a signal for Q shall only ever schedule a T2 probe; it shall never by itself change a worker's state to anything except `unknown`.
- **FR-013.** `context-exhausted` shall require one cheap trigger **and** one confirming probe from a different source; one source alone yields `unknown` plus a T2 probe on the next sweep.

## 5. Mapping of the 8 Observed Cases

Case text is from `.dev/issues/431/issue-body.md:16-23`. "Lost" is the time the issue reports; "bound" is this design's worst-case detection time.

| # | Case (lost) | State | Detecting signal (trigger -> confirm) | Bound | Response (section 8) |
|---|---|---|---|---|---|
| 1 | #339 first session, full context, autocompact thrashing, "implementing" heartbeats continue (~4 h) | context-exhausted | S2 `step_seq` flat for Q while heartbeats arrive -> screen class `compact_thrashing` or transcript compaction count | 15 min | L1 probe, then L4 report-and-restart (v1: person authorizes; v2: confirmed thrash counts as positive evidence) with a resume note that narrows reads |
| 2 | #339 replacement idle at prompt after a turn ended; last file change 12:07 (~4 h); stopped again later | idle-at-prompt | No heartbeat / S2 flat for Q -> `tui-idle` idle and transcript final turn without `worker_done` | 15 min | L2 typed nudge with `--wait-submit` receipt; second occurrence in the same Task counts toward the nudge cap |
| 3 | #331 silent from 17:10; one file's mtime 18:17 read as alive at 18:19; idle at 18:38 | idle-at-prompt | Single-file mtime is no longer a signal; S3 whole-worktree activity is used only as a non-contradiction check, and the idle confirm is screen/transcript | 15 min | L2 nudge |
| 4 | #361 closing report sent as `status`; wait listened to three types (~4 h) | finished-unreported | Wake set covers every type but heartbeat, and `W` = 5 min bounds the rest (S7); `status` parse finds `report_path` / `worker_status` | 5 min | Read contract (S11); L2 nudge "send `worker_done`"; dependents follow the contract only after `worker_done` settles the Task |
| 5 | #331 and #375 mailbox answers unseen 35-40 min until typed (cause not established) | blocked-in-ask, sub-state awaiting-ack | No ack within `A` (S8) | A = 5 to 10 min | L2 escalation: same answer, same reply id, typed into the terminal with `--wait-submit` (section 7) |
| 6 | #394 permission prompt up to ~20 min | blocked-on-person-prompt | S10 `agentWait` non-null in the T1 sweep | 10 min | L5 report to person with the prompt text; the coordinator never answers the prompt |
| 7 | #339 and #331 stopped between chain steps without a message | idle-at-prompt (if the turn ended) or long-step-in-progress (if working) | S2 `step` shows `c<n>` finished; idle confirm vs working confirm separates the two | 15 min | idle: L2 nudge naming the next `Command:` line; working: L0 wait until deadline. Prevented by worker rule WR-1 (section 9) |
| 8 | #339 replacement thrashed again at 18:11, found 18:57 (~46 min) | context-exhausted, **repeat cause** | Same as case 1 | 15 min | Restart budget sees the same cause twice for the same work unit: no third like-for-like restart; L5 report with a split proposal (section 8, restart budget) |

- **FR-014.** Every case above shall be reproducible as an acceptance scenario (section 13, AC-1 to AC-8) with its stated bound.

## 6. Message-Type Coverage

### Wake set versus read set

Orca's `--types` is only the wake condition for `check --wait`; a returned delivery is the whole FIFO batch and is never filtered by type (`enrichment/codebase-context.md:15`). So two distinct sets exist, and conflating them caused case 4:

- **Read set** (what the coordinator processes): every message in every batch, always. Nothing is ever discarded by type.
- **Wake set** (what ends a wait early): every known type except `heartbeat`, so six chatty workers do not wake the coordinator every few minutes. Heartbeats are read in the next batch, at most `W` later.

```text
check --wait --types "status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question" --timeout-ms 300000
```

The nine types are those `orca orchestration send --help` lists (`enrichment/codebase-context.md:14`). Whether `check --wait` without `--types` wakes on every type, including future ones, is UNVERIFIED; if it does, v2 should omit `--types` and drop heartbeats from wake by other means. Until verified, the explicit list plus `W` = 5 min bounds any unlisted or unknown type to one wait cycle.

- **FR-015.** The coordinator shall process every message in every delivered batch regardless of type, and shall never use `--types` to mean "ignore".
- **FR-016.** The wake set shall include every known type except `heartbeat`, and the wait timeout shall not exceed `W`.
- **FR-017.** A message of a type not in the registry below, or with an unparseable payload, shall be surfaced to the person verbatim in the next coordinator report and recorded as a `progress: unknown` observation for its sender; it shall never be dropped or acted on as if it were a known type.
- **FR-018.** Message handling shall be a registry (type -> handler -> state effect), so a new Orca type is one registry row (NFR-005).
- **NFR-005.** Adding a message type shall require only a new row in the handler registry and no change to the sweep or the ladder.

### Handler registry

| Type | Expected sender | Coordinator handling | State effect |
|---|---|---|---|
| `status` | Worker | Parse body and payload. If it carries an ack payload (section 7), close the ack. If it carries `report_path`, `worker_status` or a contract path, read the contract (S11) | Progress observation; `finished-unreported` when a final status is present |
| `dispatch` | Coordinator to worker | Inbound to the coordinator is unexpected: surface to the person | none; flag anomaly |
| `worker_done` | Worker (WC-5, `WORKER-CONTRACT.md:57`) | Settle; open the contract (`:88`); apply "Reading a result" rules (`:121-128`) | `settled` |
| `merge_ready` | Not an IronClaude worker type (workers never merge or push, WC-9, `:39`) | Treat as a possible closing message: read the contract; surface | `finished-unreported` candidate |
| `escalation` | Worker | Report to the person at once | Interaction `person_prompt`-like; ladder L5 |
| `handoff` | Not expected (work for another worker goes in the `worker_done` body, WC-13, `:60`) | Treat as possible closing message; read contract; surface | `finished-unreported` candidate |
| `decision_gate` | Worker or Orca | Person decision: report to the person; the coordinator never decides a person's gate | ladder L5 |
| `question` | Worker under `ask the coordinator` (WC-3, `:53`) | Answer per WC-3 or forward to the person; start the ack clock (section 7) | `blocked-in-ask` |
| `heartbeat` | Worker top-level session (`:61`) | Parse S2 payload; update progress digest | Progress observation |
| unknown | any | FR-017 | `unknown` for that sender |

## 7. Reply Read-Acknowledgement Protocol

### Why an application-level ack

Orca gives the sender no read receipt: "A successful `send` proves durable enqueue. Wake and nudge are best-effort attention only" (`enrichment/codebase-context.md:16`). `check --ack` is the reader acknowledging its own batch to Orca, not a signal to the sender (`:16`). In MQTT terms a mailbox delivery is a broker PUBACK, not a reader ack (`enrichment/research-light.md:34-35`). The pull model of WC-12 (`WORKER-CONTRACT.md:59`) means a worker idle at its prompt never pulls, which is a probable, UNVERIFIED, mechanism for case 5 (`seed-brief.md:79`). The protocol below works whichever cause is true, because it measures the outcome (the worker read it) rather than guessing the cause.

### Protocol (`ironclaude.ack/1`)

1. **Coordinator sends** a reply or follow-up whose first line is `reply-id: R-<task id>-<n>; ack: required`, followed by the answer. The reply id is unique per Task and never reused.
2. **Worker acks on read**, before acting on the content, with one `status` message from its top-level session (WC-7):
   - body first line: `ack R-<task id>-<n>`
   - payload: `{"schema":"ironclaude.ack/1","ack":"R-<task id>-<n>","via":"mailbox|terminal","disposition":"accepted|duplicate|not-applicable"}`
   - `status` is used, not `heartbeat`, because heartbeats follow the preamble cadence and are not sent while blocked in `ask` (`WORKER-CONTRACT.md:61`), and because `status` is in the wake set (section 6), so the coordinator wakes at once.
3. **Coordinator clock.** The ack timer `A` starts when `send` returns: 5 min when the worker was blocked in `ask`, 10 min otherwise (section 4).
4. **Escalation on timeout.** The coordinator types the **same text with the same reply id** into the worker's terminal with the terminal adapter's submit-confirming nudge (`terminal send --text --enter --wait-submit`, the only verb with an observed turn-start receipt, `enrichment/codebase-context.md:23`). The receipt proves submission and turn start, not reading, so the ack clock restarts for `A`.
5. **Second timeout** (no ack after the terminal copy): the worker state is re-derived with a T2 probe; if it is not `progressing`, ladder L5 reports to the person with the reply id, both send times and the probe result.
6. **No terminal available** (worker without a terminal, `enrichment/codebase-context.md:23`): step 4 is skipped and step 5 follows the first timeout.

### Idempotency

- The worker acts on a reply id at most once. A second copy (mailbox plus terminal, or a resumed `ask` returning the same answer) is acked with `disposition: duplicate` and otherwise ignored.
- The coordinator never sends different content under an existing reply id. A correction is a new id whose first line adds `supersedes: R-...`; the worker acks both and applies only the newest.
- An answer that arrives after the worker has settled is not acted on; it is carried by a new Task (WC-3, `WORKER-CONTRACT.md:56`; WC-6).
- The worker lists ids it has seen but not finished acting on in the S2 `pending_ack` field, so a restart can tell "read, not applied" from "never read".

### Requirements

- **FR-019.** Every coordinator message that the worker must act on shall carry a unique reply id and `ack: required`.
- **FR-020.** The worker top-level session shall send the ack `status` within its current turn on first sight of a reply id, whether it arrived by `ask` return, `check` or terminal input.
- **FR-021.** The coordinator shall escalate an unacked reply to a terminal-typed copy after `A`, and report to the person after a second `A`; total worst case 10 min for an `ask`-blocked worker and 20 min otherwise.
- **FR-022.** A reply id shall be applied at most once by the worker; duplicates shall be acknowledged and ignored.

## 8. Response Ladder

### Rungs

| Rung | Action | Evidence required | Cap |
|---|---|---|---|
| **L0 Observe** | Nothing; keep sweeping | none | unlimited |
| **L1 Probe** | Read-only T2 probes (section 4) | Absence or flat evidence for Q, a deadline, or `unknown` | once per worker per sweep |
| **L2 Nudge** | Type the nudge text (below) into the worker terminal with the submit-confirming send; never with `--interrupt` | A confirmed `idle-at-prompt` or `finished-unreported`, or an unacked reply (section 7) | 2 per state episode; 4 per Task |
| **L3 Ask** | Send an ack-required status request by mailbox, then by terminal if unacked (section 7) | `long-step-in-progress` past its deadline, or `unknown` after two L1 probes | 1 per state episode |
| **L4 Restart with resume note** | Stop the worker, set the old Task `failed --result cancelled`, create a new Task whose brief carries the resume note (WC-6, `WORKER-CONTRACT.md:69-73`) | **Positive** evidence only: Orca stall proof (`exited`, own process-exit observation, or a transcript whose final turn sent no `worker_done`, `enrichment/codebase-context.md:20`) after L2 failed twice; or confirmed `context-exhausted` (v1: only with the person's go; v2: see section 10) | restart budget below |
| **L5 Report to person** | Coordinator report with state, evidence ids, times, what was tried and one recommended action | Any state that only a person can resolve, any spent cap, any `unverifiable` past 2S | once per state episode, then at the person's chosen cadence |

### State-to-ladder map

| State | Sequence |
|---|---|
| starting, progressing | L0 |
| long-step-in-progress | L0 until deadline; then L1, L3; no ack within A -> L5 |
| idle-at-prompt | L1 (confirm) -> L2 -> (still idle after next sweep) L2 -> L4 if stall proof holds, else L5 |
| blocked-on-person-prompt | L5 immediately with the prompt text; L0 afterwards (Orca: "A waiting worker is healthy, not failed", `enrichment/codebase-context.md:19`) |
| blocked-in-ask | Answer (WC-3) -> ack clock -> L2 terminal copy -> L5 |
| context-exhausted | L1 (second source, FR-013) -> L5 with a ready restart plan -> L4 on go (v1) or under budget (v2) |
| unreachable/exited | `exited`: L4 within budget, else L5. `unverifiable`: L1, then L5 at 2S; never L4 (`WORKER-CONTRACT.md:72`) |
| finished-unreported | Read contract -> L2 nudge "send `worker_done` with report path <path>" -> second L2 -> L5 |
| unknown | L1 -> L1 -> L3 -> L5 |

### Nudge text (one template, harmless to a working session)

```text
Coordinator check, reply-id: N-<task id>-<n>; ack: required.
If you are in the middle of a step, keep working and only send the ack.
If your turn has ended: run the preamble's check, then continue with the first
unfinished Command: line of your brief (last step seen: <step>).
If your command has finished: send worker_done with --report-path <contract path>.
```

Typing into a session that is mid-turn is expected to queue the text for after the turn (UNVERIFIED for Claude Code; to be checked in the first v1 run). Because the text asks for nothing that changes a working session's plan, a false-positive nudge costs one extra short turn.

### Restart budget (OTP-style intensity, per work unit)

A **work unit** is the chain of Tasks linked by `replaces T<n>` in their briefs (the WC-6 retry record, `WORKER-CONTRACT.md:69`). Budgets follow Erlang/OTP's MaxR in MaxT (`enrichment/research-light.md:26-28`):

- At most **2 liveness restarts per work unit in 6 hours**. The third need goes to L5.
- **Same-cause rule:** if the restart cause (state name) repeats for the same work unit, the next attempt may not be like-for-like. It must change the plan (smaller chunks, split the Task, a different command stage) and the person must approve it (case 8).
- These budgets sit beside, not in place of, WC-6's three-failed-starts limit (`WORKER-CONTRACT.md:71`) and the two-brief-fix limit (`:126`); the first limit reached wins.

### Resume-note format (carried in the new Task's brief, because a brief cannot change after creation, `WORKER-CONTRACT.md:69`)

```text
Resume: replaces T<old id>; cause: <state> confirmed <ISO time> by <evidence ids>
Restart: <k> of 2 for work unit <id>; same-cause repeat: <yes|no>
Done on disk: <Command: index> -> <contract path> (worker_status: <value>)   # one line per finished step
Resume input: <the command's own resume input, e.g. the /sc:implement ledger path> | none
Last step seen: <S2 step id>; pending acks: <reply ids or none>
Constraints: read files in chunks of at most 80 lines; write a handoff file before each stage (WR-3)
Report directory: <new, unique to this Task>
```

### What never happens on silence alone

- **FR-023.** On absence, flat or `unknown` evidence alone the coordinator shall never stop, retry, release or cancel a worker, mark its Task failed, or create a replacement Task (WC-6, WC-10).
- **FR-024.** The coordinator shall never answer a person-only prompt (permission, approval, decision gate) by typing into the worker; that is the person's decision (L5).
- **FR-025.** The coordinator shall never send `--interrupt`, `/clear`, `/compact`, Escape or any other control input to a worker on silence; a clear-and-restart happens only through L4 as a new Task.
- **FR-026.** The coordinator shall never send `worker_done` or any lifecycle message on a worker's behalf, and never edit the worker's files.
- **FR-027.** Each ladder action shall be recorded with its rung, cap counter, evidence ids and result, and a spent cap shall move the worker to L5.

## 9. Worker-Side Rules

Detection bounds the cost of a failure; worker rules remove the failure. Each rule is placed by one test: **who knows the fact the rule depends on?** The preamble is Orca's and owns only verb syntax and cadence (`WORKER-CONTRACT.md:7`); commands contain no Orca calls and do not know they are in a chain (`:5`, WC-8 `:38`); the worker session knows the brief, its chain and its own context. So almost every rule belongs to the worker session, which means contract section 3.

### Rules

- **WR-1. No turn ending between chain steps.** After a `Command:` line's command finishes, the worker session, in the same turn, writes the WR-3 handoff file, runs the preamble's `check` (WC-12), and starts the next `Command:` line. The only ways a worker turn may end are: `worker_done` sent, `check` returned `consumer_fenced` (`WORKER-CONTRACT.md:59`), or the session is blocked in `ask`. Fixes case 7 (`issue-body.md:22`) at the source.
- **WR-2. Context-safe reads.** The worker session reads any file over 200 lines, or any report from an earlier step, in chunks of at most 80 lines, and prefers the WR-3 handoff file over the full report. When its own view of context is `near_limit` it writes the handoff file for the current step first. Addresses cases 1 and 8, whose recovery note was "read reports in small pieces" (`issue-body.md:23`).
- **WR-3. Per-stage handoff files.** After each `Command:` line the worker writes `<report-dir>/handoff/c<n>.md` (at most 20 lines): command line, contract path and `worker_status`, the three to five facts the next step needs, pending reply ids, next step. It is inside the worker's own report directory, so WC-11 holds (`WORKER-CONTRACT.md:45`). A restart (L4) reads these instead of re-reading full reports.
- **WR-4. Acknowledge replies** as section 7 states.
- **WR-5. Progress payload** on every heartbeat as section 3 (S2) states; no extra heartbeats.
- **WR-6. Close only with `worker_done`.** A worker never uses `status`, `handoff` or `merge_ready` to report completion; its closing report is exactly one `worker_done` (WC-5, `WORKER-CONTRACT.md:57`). Fixes case 4 at the source; FR-015 to FR-017 remain the safety net.
- **WR-7. Long-step declaration.** Before a step the session expects to run past Q without a heartbeat (subagent fan-out, a long eval split into 4-minute waits per WC-10), the worker sends one S2 heartbeat with `expect_until` set. This converts an accepted WC-10 gap (`WORKER-CONTRACT.md:44`) into a declared one the coordinator can tell apart from idleness.

### Placement

| Rule | Worker contract (section 3) | Brief (coordinator template) | Preamble (Orca) | Command file |
|---|---|---|---|---|
| WR-1 chain continuation | **Owner** (new duty WC-14) | one line: `Chain: run every Command: line in one turn; end only with worker_done` | no | no: commands cannot see the chain |
| WR-2 chunked reads | **Owner** for the worker session | optional `Constraints:` line in resume notes | no | v2: a command whose own steps read large reports gets the same rule in its `## Unattended mode` section |
| WR-3 handoff files | **Owner** | report directory already in the brief | no | no |
| WR-4 ack | **Owner** (WC-12 amendment) | no | uses the preamble's `status` verb syntax | no |
| WR-5 progress payload | **Owner** (Heartbeats bullet amendment) | no | cadence and verb stay the preamble's | no |
| WR-6 close only with `worker_done` | **Owner** (WC-5 amendment) | no | no | no |
| WR-7 long-step declaration | **Owner** (WC-10 amendment) | optional `Expect:` per `Command:` line | no | v2: a command may name its known long steps in `## Unattended mode` |

- **FR-028.** WR-1 to WR-7 shall be stated once, in `WORKER-CONTRACT.md` section 3; the brief template gains the `Chain:` and optional `Expect:` lines; no rule shall be copied into the preamble or require a command to call Orca (WC-8).
- **FR-029 (v2, optional adapter).** On Claude Code, a `Stop` hook may refuse a turn end (exit code 2 keeps the session working, `enrichment/research-light.md:41`) only while a chain-pending marker written by WR-3 exists in the report directory and no `worker_done` has been sent. Guarded by a per-Task cap of 3 refusals to prevent a loop. This is enforcement of WR-1, never a replacement for it.

## 10. Contract Changes: v1 Now vs v2 (#423)

The split rule: **v1 now** is anything a coordinator session and a worker session can do by following text, using Orca verbs that already exist (`seed-brief.md:65-71`). **v2** is anything that needs a running component, persisted state across coordinator turns, or a harness hook. v1 changes are prose amendments; none adds an Orca call to a command (WC-8, `WORKER-CONTRACT.md:38`) or copies preamble syntax (`:49`).

### Delivery table

| Capability | v1 now (contract and coordinator rules text) | v2 (#423 machinery) |
|---|---|---|
| All-type wake set, read every batch entry, surface unknown types (section 6) | Yes: section 4 coordinator rule | Handler registry in code |
| W = 5 min wait timeout and per-cycle sweep (section 4) | Yes: coordinator rule; sweep done by hand with `worker-list`, `worker-show` | Liveness supervisor runs the sweep on a timer |
| S2 progress payload on heartbeats | Yes: WR-5, raw `--payload` (`seed-brief.md:65`) | Schema validation, payload history |
| Read acknowledgement `ironclaude.ack/1` (section 7) | Yes: WR-4 plus coordinator rule | Ack ledger with automatic terminal-typed copy |
| `agentWait` poll for person prompts (S10) | Yes: sweep step | Same, automated |
| Terminal classification (S4) | Confirming probe only, by hand, with `terminal read --screen` | Versioned pattern data in the terminal adapter |
| Transcript timestamps (S5) | Probe via `worker-read --source transcript` only (`seed-brief.md:75`) | Transcript adapter reading last tool call and model turn times |
| Whole-worktree activity (S3) | Not in v1: per-worktree scans by hand are too costly; issue-body case 3 shows one-file mtime misleads (`issue-body.md:18`) | fs-activity adapter with prune list |
| Per-step deadlines (S6) | Optional `Expect:` brief line (WR-7) | Deadline table derived from command metadata |
| Hooks journal (S12) | No | Claude Code adapter: `Notification`, `Stop`, `PreCompact`, `SessionStart` (`research-light.md:39-46`) |
| Restart with resume note (L4) | Yes, as WC-6 already allows after positive stall proof; resume note is a new brief section | Restart budget counter persisted per work unit |
| Confirmed context-exhausted as restart evidence | No: person decides (L5) | Yes, after the amendment to WC-6 below and a validated detector |
| Feed to #409 dashboard | No | Observation store exposes liveness, freshness and delivery as separate fields (`seed-brief.md:81`) |

### WC rules amended (proposed wording)

Each amendment keeps its rule's existing meaning and adds to it; inserted text is quoted.

- **WC-10** (`WORKER-CONTRACT.md:44`), replace its last sentence with: "The coordinator therefore treats a missing heartbeat as absence, never as death: it never stops, retries or releases a worker because a heartbeat is late. **Absence past a stated bound authorizes only a probe, a nudge or a question (the response ladder, rungs L1 to L3); stop, retry and release still need Orca's stall proofs. A step expected to exceed the cadence is declared first with one heartbeat whose payload sets `expect_until` (WR-7).**"
- **WC-12** (`:59`), append: "**When a `check` batch contains a coordinator reply carrying a reply ID, the worker sends one `status` message whose payload is `ironclaude.ack/1` with that ID before acting on the reply, and acknowledges each reply ID once. A worker that finishes a command step runs `check` before starting the next `Command:` line.**"
- **WC-3** (`:56`), append: "**The answer to an `ask` is acknowledged as WC-12 states; an answer that arrives typed into the terminal is acknowledged the same way, naming the reply ID it carries.**"
- **WC-5** (`:57`), append: "**`worker_done` is the only closing message; `status`, `handoff` and `merge_ready` never report completion.**"
- **Heartbeats** (`:61`), append: "**Each heartbeat carries the `ironclaude.progress/1` payload (task, step, step start time, step sequence, actions since last heartbeat, last action time, optional `expect_until`, context estimate, pending reply IDs). Cadence and verb remain the preamble's.**"
- **New WC-14. Chain continuity and handoff files** (section 3): "After each `Command:` line, in the same turn, the worker writes its handoff file `<report-dir>/handoff/c<n>.md`, runs `check`, and starts the next `Command:` line. Its turn ends only after `worker_done`, on `consumer_fenced`, or while blocked in `ask`. It reads large files and earlier reports in chunks of at most 80 lines and prefers handoff files."
- **Section 4 coordinator rules**, new subsection "Liveness supervision": the wake set (all nine types except `heartbeat`), the 5-minute wait timeout, the sweep, the per-state bounds of section 4 of this design, the ladder with its caps, and "never answer a person-only prompt for the person".
- **Brief layout** (`:90` onward): add the `Chain:` line, the optional per-`Command:` `Expect:` line, and the optional `Resume note:` block used only by L4.
- **WC-6** (`:73`), v2 only, append: "**A context-exhausted verdict confirmed by two independent signals (progress flat for Q while a heartbeat or terminal reports compaction, plus the screen or transcript showing the compaction-failure text) counts as a positive stall proof for that attempt. Restarts of one work unit are capped at 2 in 6 hours; a third same-cause stall goes to the person.**" Until this amendment lands, case 1 and case 8 end at L5 with the person's go.

WC-7 and WC-8 are not amended: every new duty is the top-level worker session's, and no command gains an Orca call. WC-11 holds because handoff files sit in the worker's own report directory (`:45`).

### v2 components (for #423)

1. **Liveness supervisor**: runs the sweep, owns the state model and the ladder; produces actions as proposals the coordinator executes, so a person can audit every step.
2. **Observation store**: append-only `ironclaude.liveness/1` records; the only input to verdicts; the #409 feed.
3. **Adapter registry**: section 11.
4. **Ack ledger and restart budget**: small persistent tables keyed by reply ID and work unit.
5. **Deadline table**: per-command expected step durations, data not code.

- **FR-030.** The v1 amendments above shall be adoptable independently and in any order; none shall depend on a v2 component.
- **FR-031.** v2 components shall consume only the observation record and adapter interfaces, so the v1 text and v2 code describe one model.
- **Open (carried to section 13):** whether IronClaude's Python CLI may call Orca directly or the supervisor must run as a coordinator-session procedure; the developer guide currently describes the orchestration skill as a discovery stub (`issue-body.md:53`).

## 11. Portability and Extension Points

The core (state model, detection rules, ladder) never names Orca, Claude Code or a screen string. Everything harness-specific sits behind one adapter interface, as the seed brief requires (`seed-brief.md:34`).

### Adapter interface (language-neutral sketch)

```text
interface LivenessAdapter
  id() -> string                       # "orca-mailbox", "claude-code-transcript", ...
  version() -> string                  # adapter version, recorded in every observation
  capabilities() -> set<SignalKind>    # e.g. {S4_terminal_class, S10_agent_wait}
  cost(kind) -> T0 | T1 | T2           # cost tier, section 3
  observe(worker, kind) -> Observation | Unsupported | Error
  nudge(worker, text) -> Receipt       # optional; Unsupported if the harness has no input channel

Observation  = ironclaude.liveness/1 record (section 3): signal, value, proof_class, observed_at, source, adapter id and version
Receipt      = { accepted: bool, submitted: bool, turn_started: bool | unknown, evidence: string }
```

Rules for adapters:

- An adapter reports what it saw, never a state. Mapping observations to states is the core's job, so a new adapter cannot silently change a verdict rule.
- `Unsupported` is a first-class answer: the core falls back to the next signal, and a state whose only signals are unsupported is reported as `unknown`, which leads to a probe (FR-003), never to action.
- `Receipt.turn_started` is `unknown` unless the harness proves it; only Orca's `terminal send --wait-submit` is documented to do so (`seed-brief.md:67`).
- Screen and transcript patterns (for example the thrash text in `issue-body.md:43` and the permission prompt text at `:44`) are versioned data files owned by the adapter, keyed by harness version, with a test fixture per pattern.

### Registries (the extension points)

| Registry | Key | Adding an entry needs | Example extension |
|---|---|---|---|
| Signal kinds | `S<n>` id | an id, proof class, cost tier | S13 "GPU job progress" for eval workers |
| Adapters | adapter id | the interface above | a Codex CLI or Aider adapter; a tmux-only adapter without Orca |
| States | state name | precedence slot, bound, ladder entry | `rate-limited` (provider throttling) |
| Message types | type string | handler (wake or read-only, closing or not) | a future Orca type; until registered it is `unknown` and surfaced (FR-018) |
| Screen patterns | harness + version | pattern, expected state, fixture | a new Claude Code prompt wording |
| Deadlines | command + step | expected duration | `/sc:implement` per-task budget |

### Porting checklist for another harness

1. Map its process view to Process axis values (alive / exited / unverifiable).
2. Provide at least one positive-proof signal for each blocked state it can enter, or accept that state as `unknown` with probe-only handling.
3. Provide a nudge channel, or declare `nudge` unsupported, in which case L2 is skipped and L3 (ask through the mailbox) is the first active rung.
4. Ship its pattern data with fixtures.

- **FR-032.** The core shall depend only on the adapter interface and the observation record; adding a harness shall require no change to the state model, detection rules or ladder.
- **FR-033.** Every observation shall record its adapter id and version, so a verdict can be traced to the adapter that produced its evidence.
- **NFR-006.** A new adapter for an existing signal kind shall be addable as one module plus its pattern data and fixtures.
- **NFR-007.** Pattern data shall be testable offline against recorded screens and transcripts, with no live worker.

## 12. Risks, False Positives and Edge Cases

| # | Risk or edge case | Effect if mishandled | Mitigation in this design |
|---|---|---|---|
| R1 | Shared feature worktree: another worker's writes move worktree mtimes (WC-11 allows sharing, `WORKER-CONTRACT.md:45`) | S3 reports activity for an idle worker, as one file did in case 3 (`issue-body.md:18`) | S3 counts only the worker's own report directory in a shared worktree; whole-worktree only in a child worktree; S3 is never sufficient alone for `progressing` |
| R2 | Nudge typed into a session that is working | Text queues into the next turn or interrupts reasoning; queueing behaviour UNVERIFIED | L2 only after a terminal or transcript probe shows idle; nudge text is idempotent ("if you are working, continue and ignore this") and carries a reply ID so its effect is measurable |
| R3 | Screen text changes across harness versions | S4 misclassifies | S4 is a confirming probe, never sole evidence for L4; patterns versioned with fixtures (NFR-007) |
| R4 | Legitimately repetitive work read as thrashing | False `context-exhausted` | Requires two independent signals (section 10, WC-6 amendment); OpenHands saw false positives with early thresholds (`research-light.md:48`) |
| R5 | Hooks do not fire in some hosts (VS Code report, `research-light.md:46`) | S12 silent | S12 is additive; absence of a hook event is `unknown`, not evidence |
| R6 | Worker on a host where Orca reports `unverifiable` | No process view | Probe and mailbox ask only; L4 forbidden without positive proof (`WORKER-CONTRACT.md:72`) |
| R7 | Duplicate or late acknowledgements | Coordinator double-acts | Acks idempotent by reply ID; late ack after a terminal copy is recorded, not re-acted (section 7) |
| R8 | Restart loop on a recurring cause (case 8 repeated case 1, `issue-body.md:23`) | Hours lost repeatedly | Budget 2 per 6 h per work unit; same-cause rule sends a third stall to the person; resume note includes the cause and WR-2 constraints |
| R9 | Heartbeat payload lies (stale counter re-sent by a looping session) | False `progressing` | S2 is a claim; `progressing` needs non-contradiction from S4 or S5 at sweep time when S2 has been unchanged for Q |
| R10 | Wake set without `heartbeat` hides a worker whose only traffic is heartbeats | Late detection | W = 5 min timeout reads the whole batch every cycle, so heartbeats are processed within W |
| R11 | Sweep cost grows with fleet size | Coordinator turn time and tokens | T1 fleet call per sweep; T2 probes only for workers whose verdict is not `progressing`; cost bound in NFR-004 |
| R12 | Coordinator itself goes idle or compacts | Nothing is swept | Out of scope for worker liveness; v2 supervisor runs outside the coordinator's turn (section 10); v1 relies on the coordinator's wait loop |
| R13 | Resume note causes repeated side effects | Duplicate commits or files | Restart is a new Task with its own report directory (WC-6, `WORKER-CONTRACT.md:69`); the note points at old handoff files read-only |
| R14 | Person prompt answered by coordinator | Policy breach | FR-024 forbids it; L5 reports only |

- **NFR-008.** The design shall prefer a late action to a wrong destructive one: every rung that can lose work (L4) needs positive evidence; every rung driven by silence (L1 to L3) shall be harmless when the verdict is wrong.

## 13. Acceptance Criteria and Open Questions

### Per-case acceptance (FR-014)

Each scenario runs with the section 4 defaults against a staged worker (recorded screens and transcripts are acceptable for adapter-level checks per NFR-007; the end-to-end check needs a live Orca run). "Detected" means the observation store holds the named state for that worker.

| AC | Case | Given | Then, within the bound |
|---|---|---|---|
| AC-1 | 1 | Heartbeats arrive every few minutes with an unchanged S2 `step_seq`; screen shows the thrash text (`issue-body.md:43`) | `context-exhausted` detected within 15 min; L1 probe recorded; v1: L5 report to the person; v2: L4 new Task with a resume note |
| AC-2 | 2 | Turn ended at the prompt, no heartbeat, no `worker_done` | `idle-at-prompt` within 15 min; one L2 nudge with a `--wait-submit` receipt; a second idle in the same Task increments the nudge cap |
| AC-3 | 3 | One file in a shared worktree is touched by another writer while the worker sits idle | Worker still detected `idle-at-prompt` within 15 min; S3 does not yield `progressing` |
| AC-4 | 4 | Worker sends its closing report as `status` with a `report_path` | Message read within W = 5 min; state `finished-unreported`; contract opened; L2 nudge asks for `worker_done` |
| AC-5 | 5 | Coordinator replies by mailbox; worker sends no ack | Terminal-typed copy with the same reply ID sent within A (5 min if in `ask`, else 10 min); a later ack is recorded once |
| AC-6 | 6 | Worker blocked on a permission prompt | `blocked-on-person-prompt` within 10 min; L5 report includes the prompt text; no input typed into the worker |
| AC-7 | 7 | Worker finishes `Command:` line 1 and ends its turn | `idle-at-prompt` within 15 min; nudge names line 2; with WR-1 in force the turn does not end (worker-side check) |
| AC-8 | 8 | Same work unit hits `context-exhausted` a second time | No like-for-like restart; L5 report with the cause history and a split proposal |

### General acceptance

- **AC-9.** Every wait the coordinator issues wakes on all nine Orca types except `heartbeat`, uses W = 5 min, and every batch entry of every type, including an unknown type, is read and logged (FR-015 to FR-018).
- **AC-10.** No stop, retry, release, Task failure or replacement Task is ever produced from absence, flat or `unknown` evidence (FR-023); checked by replaying all eight cases with stall proofs withheld.
- **AC-11.** Each ladder rung's cap is enforced, and a spent cap yields L5 (FR-027).
- **AC-12.** An adapter returning `Unsupported` for every T2 signal produces `unknown` plus probe scheduling, never an action beyond L3 (FR-003, FR-032).
- **AC-13.** The v1 amendments in section 10 can be applied to `WORKER-CONTRACT.md` without any command file gaining an Orca call (`grep` for Orca verbs in command files returns no new hits) (FR-028, FR-030).
- **AC-14.** A healthy fleet of N workers costs two T1 calls per sweep regardless of N (NFR-004).

### Open questions

1. Does omitting `--types` on `check --wait` wake on every type including `heartbeat`? Section 6 assumes an explicit list because this is UNVERIFIED.
2. What heartbeat cadence does the dispatch preamble set? Q = 10 min assumes it is under 6 minutes (UNVERIFIED value; the preamble owns it, `WORKER-CONTRACT.md:49`).
3. Which transcript entry type marks a compaction, and is it written during thrashing? UNVERIFIED; until known, the transcript cannot be the confirming probe for `context-exhausted` and the screen class is used.
4. Does text typed into a busy Claude Code session queue for the next turn or interrupt it? UNVERIFIED; R2 mitigation assumes the worst.
5. What caused case 5? The WC-12 pull model is a probable mechanism (`seed-brief.md:79`) but not established; the ack protocol bounds the cost whatever the cause.
6. Which values can `worker-list` `projection.attention.categories` take, and does any cover thrashing or idleness? UNVERIFIED (`seed-brief.md:68`); if one does, it becomes a T1 trigger and lowers bounds.
7. Does Orca keep per-message read state on the recipient side that a coordinator could query? If yes, S8 gains a cheap first stage before the ack timeout.
8. May the v2 supervisor be IronClaude Python code that calls Orca, or must it remain a coordinator-session procedure (section 10, FR-031)?
9. Should the WC-6 amendment (confirmed context exhaustion as positive stall proof) need the person's one-time approval per run rather than per incident?
10. Do the defaults (W, S, Q, A) hold for fleets larger than six workers, or should S scale with fleet size? Needs a measured run.
