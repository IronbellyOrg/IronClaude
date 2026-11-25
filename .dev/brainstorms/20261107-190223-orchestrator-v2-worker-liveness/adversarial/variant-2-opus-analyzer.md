# Worker Liveness Design Spec, Variant 2 (analyzer persona: root cause and evidence first)

## 1. Overview and Goals

**Status:** design only, written 2026-11-07. No source file, Orca state or GitHub item was changed. Sources used are cited as `path:line`. Orca CLI behaviour comes from the enrichment pass (`enrichment/codebase-context.md`) plus three `--help` reads made for this variant (`orca orchestration check --help`, `reply --help`, `ask --help`, binary `~/.config/orca/linux-orca-cli-shim/orca`, 2026-11-07). No live worker was observed, so runtime claims about Orca are documented behaviour, not observed behaviour.

### 1.1 The root cause behind all eight cases

Each of the eight cases in `.dev/issues/431/issue-body.md:16-23` comes from the same defect. The coordinator treated **evidence that something once happened** as **evidence of what is happening now**:

| Weak signal relied on (`.dev/issues/431/description.md:19-23`) | What it actually proves | What the coordinator read into it |
|---|---|---|
| Timer heartbeat, phase "implementing", unchanged | A process or loop that can send a message exists | "The worker is making progress" |
| mtime of one file | Something wrote that file at time T in the past | "The worker is active now" |
| Helper agent name visible on screen | A subagent ran at some point | "A long step is running" |
| No failure message | Nothing was sent | "Nothing went wrong" |

Two structural facts in the v1 contract made these signals the only ones the coordinator had:

1. **Pull-only follow-ups.** Workers read coordinator messages only when they run `check` at checkpoints (`src/superclaude/core/WORKER-CONTRACT.md:59`). A worker that has stopped taking turns never reaches a checkpoint, so nothing written to its mailbox can wake it.
2. **Absence is never acted on.** The coordinator "treats a missing heartbeat as absence, never as death" and "acts only on Orca's stall proofs" (`WORKER-CONTRACT.md:44`). That rule is safe for stopping and retrying. But the contract names no *non-destructive* action for silence (probe, nudge, ask), so in practice silence led to waiting.

Orca already offers stronger evidence that IronClaude's rules never tell the coordinator to read: `worker-list` liveness verdicts, `worker-show` `observation.agentWait`, `worker-read` of the transcript, and `terminal send --wait-submit`, which reports observed submission and turn start (`enrichment/codebase-context.md:18-23`). The gap is in policy and state modelling, not mainly in missing tools.

### 1.2 Goals

- **G1.** Name every worker condition as a state with evidence-based entry and exit conditions. "Alive" alone is not a state.
- **G2.** Separate *process exists*, *making progress*, *waiting legitimately* and *finished* as different questions answered by different signals, following the Kubernetes liveness/readiness split (`enrichment/research-light.md:18-22`) and the #409 rule that keeps liveness, freshness, delivery and work status in separate fields (`.dev/research/orca-dashboard-20261105/REPORT.md:41`).
- **G3.** Detect idle, blocked and thrashing workers within 15 minutes, and missed message types within one wait cycle (`seed-brief.md:42-43`).
- **G4.** Prove that an answer was read with an acknowledgement from the worker, not with delivery to its mailbox (`seed-brief.md:44`).
- **G5.** Map every detected state to one response from a fixed ladder with repeat caps. Silence alone never stops, retries or releases a worker (`seed-brief.md:36`, `WORKER-CONTRACT.md:44,72`).
- **G6.** Keep the core model harness-neutral, with Orca and Claude Code as the first adapters (`seed-brief.md:34`).
- **G7.** Split the changes into contract text that can ship in v1 now and machinery that belongs in v2 (#423).

### 1.3 Non-goals

- Changing Orca or its dispatch preamble. The preamble stays the authority for verb syntax and heartbeat cadence (`WORKER-CONTRACT.md:7`).
- Adding any Orca call to a command (`WORKER-CONTRACT.md:5,38`).
- Having the coordinator answer person-only prompts, such as permission prompts, on the person's behalf.

### 1.4 Top-level requirements

- **FR-001.** The coordinator classifies each worker into exactly one state from section 2 at every sweep and records the state, the evidence that set it and the evidence's observation time.
- **FR-002.** A heartbeat counts as evidence of progress only when it carries a progress token that differs from the previous one. A heartbeat without a token proves only that the process exists.
- **FR-003.** Every coordinator wait wakes on every Orca message type, and the coordinator processes every message in a returned batch before it acknowledges the batch.
- **NFR-001.** Every state that blocks work is detected within the bound in section 4. The worst case is 15 minutes, except a long step the worker declared (at most 45 minutes, section 4).
- **NFR-002.** A false-positive nudge into a working session must be harmless: idempotent text that does not change the task (section 8.3).
- **NFR-003.** The harness-neutral core never reads harness-specific data directly. Screen text, transcript files and hook events are reached only through adapters (section 11).

## 2. Worker State Model

### 2.1 Two questions, answered separately

The model separates two questions that v1 merged:

- **Is the process there?** Answered by Orca's fleet verdict (`projection.liveness`: `live`, `unverifiable`, `exited`; `enrichment/codebase-context.md:18`) and by heartbeat *arrival*.
- **Is the agent moving the task forward, waiting for a known reason, or finished?** Answered by progress-token *change*, transcript activity, prompt-wait evidence, the contract file on disk and message content.

A worker is in exactly one **work state**. Each state record also carries a separate **process verdict** (`live`, `unverifiable`, `exited`) and an **observation freshness** (time of the newest evidence used). Stale evidence gives the state `unknown`, never a healthy state (FR-004; `.dev/research/orca-dashboard-20261105/REPORT.md:41,64`).

- **FR-004.** If none of the evidence behind a state is younger than 2 sweep intervals (10 minutes), the coordinator records the work state as `unknown` and runs a probe (section 8, L1). `unknown` is never reported as healthy.

### 2.2 States

All state names are harness-neutral. "Turn" means one cycle of agent activity that ends with the agent waiting for input; every adapter must define it (section 11).

| # | State | Entry condition (evidence) | Exit condition | Blocks work? | Legitimate? |
|---|---|---|---|---|---|
| S0 | `starting` | Worker started; no heartbeat or transcript activity yet | First progress token or first transcript activity leads to `progressing`; grace period (10 min) passes leads to a probe | No | Yes |
| S1 | `progressing` | The progress token changed within the current expected-silence window, **or** transcript activity (new tool call or model turn) is newer than 5 min and the token is not frozen (see S6) | The token stops changing or activity stops (to S2, S3, S6), or another state's evidence appears | No | Yes |
| S2 | `long-step-in-progress` | The worker *declared* a long step (heartbeat with `expect_silence_min`, section 9) and the declared window has not passed; **or** no token change, but transcript activity is newer than 5 min (for example Agent-tool fan-out, which WC-10 accepts, `WORKER-CONTRACT.md:44`) | Window passes with no activity (to probe), token changes (to S1), or other evidence appears | No | Yes, within the window |
| S3 | `idle-at-prompt` | No transcript activity for 5 min or more, **and** the adapter classifies the session as waiting for input with no tool running, **and** no `worker_done` has been received, **and** no `ask` is pending | A nudge is followed by turn start (to S1); `worker_done` arrives (to S9) | **Yes** | No: a turn ended with work left |
| S4 | `blocked-on-person-prompt` | Orca `observation.agentWait` is non-null (evidence: hook, prompt text or title; `enrichment/codebase-context.md:19`), or the adapter classifies a permission or confirmation prompt on screen | The prompt disappears and activity resumes (to S1) | **Yes** | The waiting is legitimate (Orca: "a waiting worker is healthy, not failed"), but only the person may resolve it |
| S5 | `blocked-in-ask` | The coordinator received a `question` (or an `ask` message) from this worker and has not yet seen the worker acknowledge an answer (section 7) | The worker sends `ack` for the answer (to S1); the ask times out with no resume (to S3) | Waiting on the coordinator | Yes. No heartbeat is expected here (`WORKER-CONTRACT.md:56,61`) |
| S6 | `context-exhausted` (includes compact thrashing) | Any of: (a) the adapter classifies a context-limit or thrashing message on screen (for example `Autocompact is thrashing`, `issue-body.md:43`); (b) heartbeats keep *arriving* but the token is unchanged for 2 or more expected windows (arrival without progress, the signature of case 1); (c) the adapter reports 3 or more compactions within 30 minutes | Only a restart from on-disk state (section 8). The session is never expected to recover by itself | **Yes** | No |
| S7 | `unreachable` | `projection.liveness` is `unverifiable` with reason `host_unavailable`, `stale_status` or `missing_status` (`enrichment/codebase-context.md:18`), or the adapter's probe fails | Verdict returns to `live` (to the previous state); verdict becomes `exited` (to S8) | Unknown | Unknown. Absence, so **no** stop or retry (`WORKER-CONTRACT.md:72`) |
| S8 | `exited` | `projection.liveness` is `exited`, or the worker's own process exit is observed. This is Orca stall proof (`enrichment/codebase-context.md:20`) | Settled by the coordinator per WC-6 (`WORKER-CONTRACT.md:73`) | **Yes** | No |
| S9 | `finished-unreported` | The worker's contract file `<report-dir>/return-contract.yaml` exists (its path is known before dispatch, `WORKER-CONTRACT.md:31`) **or** a non-`worker_done` message carries a closing report (case 4), **and** no `worker_done` has been received | `worker_done` received (to S10) | **Yes**: dependents wait on settlement (`WORKER-CONTRACT.md:121-127`) | No |
| S10 | `settled` | `worker_done` received | Terminal | No | Yes |
| S11 | `unknown` | FR-004: the evidence is stale | Any fresh evidence | Treated as possibly blocking | Undetermined |

The brief's required states map as follows: progressing = S1, long-step-in-progress = S2, idle-at-prompt = S3, blocked-on-person-prompt = S4, blocked-in-ask = S5, context-exhausted/compact-thrashing = S6, unreachable/exited = S7 and S8, finished-unreported = S9.

### 2.3 Precedence when evidence conflicts

Evidence can point at several states at once. For example, a session thrashing on autocompact may also show a prompt. The coordinator takes the highest row that applies:

1. S8 `exited` (positive proof, settled per WC-6)
2. S9 `finished-unreported` (the contract exists on disk: work is done whatever the screen shows)
3. S6 `context-exhausted` (no in-place recovery exists, so it outranks S3, where a nudge would only feed a full context)
4. S4 `blocked-on-person-prompt`
5. S5 `blocked-in-ask`
6. S3 `idle-at-prompt`
7. S2 `long-step-in-progress`
8. S1 `progressing`
9. S7 `unreachable`, then S11 `unknown`

Reason for this order: rank by **strength of proof** first (an exit, or a file on disk, beats an inference), then by **cost of the wrong response**. Nudging a thrashing session wastes the nudge and adds to its context, and nudging a session that is blocked on a prompt types text into the prompt.

### 2.4 Transitions (text form)

```text
starting --token/activity--> progressing <--> long-step-in-progress
progressing --turn ends, work left--> idle-at-prompt --nudge + turn start--> progressing
progressing --question sent--> blocked-in-ask --ack of answer--> progressing
any live state --agentWait non-null--> blocked-on-person-prompt --prompt cleared--> progressing
progressing|long-step --frozen token with arrivals / thrash text--> context-exhausted --restart (new Task)--> [new worker: starting]
any --liveness unverifiable--> unreachable --live--> previous | --exited--> exited
any --contract on disk, no worker_done--> finished-unreported --worker_done--> settled
any --worker_done--> settled
```

- **FR-005.** Every transition is logged in the coordinator's run notes as `<time> <worker> <from> -> <to> evidence=<source>@<observed_at>`. This gives the #409 dashboard its "last-seen" and "evidence freshness" fields (`.dev/research/orca-dashboard-20261105/REPORT.md:35,77`).

## 3. Signals and Adapters

Rule for this section: each signal is judged by **what it proves**, not by how often it fires. A signal that fires often but proves only that a process exists (case 1) is worse than a rare signal that proves the current state.

### 3.1 Signal evaluation

| ID | Signal | Source | Proves | Does not prove | Cost | Brittleness | Layer | Verdict |
|---|---|---|---|---|---|---|---|---|
| SG-1 | **Progress-bound heartbeat** (progress token = step ID plus a monotonic counter of completed units, plus an optional declared silence window) | Worker top-level session, using the preamble's heartbeat command. `--phase` is free text and `--payload` raw JSON (`enrichment/codebase-context.md:14`) | When the token *changes*: the agent completed a unit since the last heartbeat. When it *arrives unchanged* repeatedly: a loop is running but not progressing (S6 signature) | Progress *inside* a unit; whether the counter is honest (a model can increment it without doing work) | Very low: one message per cadence tick, already sent | Low: a convention in IronClaude text; no harness dependency | **Core** | **Primary** progress signal. Bind the counter to on-disk units where possible (ledger lines, `Command:` lines completed) to limit dishonest increments |
| SG-2 | Whole-worktree activity (git status and file mtimes, excluding caches and virtualenvs) | Filesystem | Something wrote somewhere in the tree | *Which* worker wrote it: in the shared feature worktree several workers, the coordinator and hooks write (`WORKER-CONTRACT.md:45`). Also not *current* activity: case 3's last file was the final output before idle (`description.md:13`) | Medium: recursive scan; must exclude `.venv`, caches, `node_modules` | Medium | Core (filesystem adapter) | **Confirming only**, and only scoped to an area one writer owns: the worker's own report directory, or its child worktree when it has one. Never whole-tree in a shared worktree. Never alone sufficient for S1 |
| SG-3 | Terminal state classification (working, idle prompt, permission prompt, context full or thrashing) | `orca terminal read --screen`, `orchestration worker-read --source terminal` (`enrichment/codebase-context.md:22`); `terminal wait --for tui-idle` (`:21`) | The rendered state *at the time of reading*: the only direct evidence for S3, S4 and S6 text | Anything about the past; the text patterns are tied to harness versions | Medium: one screen read per worker; costly in coordinator context if read often | **High**: UI wording changes between harness versions | **Adapter** (Claude Code) | **Confirming probe**, run only when a core trigger fires. Never the primary signal (answers open question `seed-brief.md:54`) |
| SG-4 | Transcript timestamps (last tool call, last model turn) | Claude Code JSONL with ISO UTC `timestamp`, reached via `worker-read --source transcript`; never guess the path (`enrichment/codebase-context.md:58`) | When the agent last *did* anything, which separates S2 (active) from S3 (inactive). Orca's third stall proof, "a transcript whose final agent turn sent no `worker_done`" (`:20`), is read from here | Whether the activity is useful (a thrashing loop is active); trailing metadata entries have no timestamp, so a reader must scan back (`:58`) | Low to medium | Medium: the file format belongs to the harness | **Adapter** | **Primary** activity signal for S2 vs S3, and the stall-proof source |
| SG-5 | Per-step deadlines (expected-message deadlines) | Coordinator, from the worker's declared `expect_silence_min` or from per-command defaults | That silence has passed a stated expectation. This turns "absence" into a trigger for a probe (not for a stop) | Anything about the cause | Very low | Low | **Core** | **Primary trigger.** It is the bridge that lets WC-10 stay intact: a passed deadline authorizes a probe only (section 10) |
| SG-6 | All-type wait filter | `orca orchestration check --wait --types <all nine>`. `--types` is only the wake condition; a delivery is always the whole FIFO batch (verified in `check --help`, 2026-11-07) | That no message type can wait unseen past one wait cycle | Nothing about workers that send nothing | None | None | Core (Orca mailbox adapter) | **Mandatory** (section 6) |
| SG-7 | Read acknowledgement | Worker sends an `ack` naming the message ID it acted on (section 7) | The worker's agent *read and acted on* the message | Whether the answer was correct | Very low | Low | **Core** | **Mandatory** for every answer and follow-up |
| SG-8 | Orca fleet verdict | `worker-list` `projection.liveness`, `attention.categories`, `requiresAction`, `nextAction` (`enrichment/codebase-context.md:18`) | `exited` is positive stall proof; `unverifiable` gives a reason | Progress. "A live terminal can still hold a dead or stuck agent" (`:18`). Which attention categories exist is UNVERIFIED | Low: one call per sweep for the whole fleet | Low: an Orca projection | Orca adapter | **Primary** for S7 and S8 |
| SG-9 | Prompt-wait evidence | `worker-show` `observation.agentWait` (null = looked, none; absent = never looked); `orca worktree ps --agent-wait` (`enrichment/codebase-context.md:19`) | A person-only prompt is pending, with its evidence | Prompt content beyond the evidence field | Low per call | Low | Orca adapter | **Primary** for S4 |
| SG-10 | Contract file on disk | `<report-dir>/return-contract.yaml`, path known before dispatch (`WORKER-CONTRACT.md:31,81`) | The command finished and wrote its outcome | That the worker *session* is done (a chain may have more `Command:` lines) | Very low: one `stat` | None | **Core** (filesystem) | **Primary** for S9 on the last `Command:` line |
| SG-11 | Harness lifecycle events (Claude Code `Notification` with `idle_prompt`/`permission_prompt`, `Stop`, `PreCompact`, `SessionStart` source `compact`) | Hooks (`enrichment/research-light.md:39-46`) | A typed state change at the moment it happens | Delivery: one report says `Notification` did not fire in the VS Code extension (`:46`); `idle_prompt` timing is UNVERIFIED | Low at run time; setup cost | Medium | Adapter, **v2** | Accelerator only. Orca already installs hooks that feed `agentWait` and transcript reporting (`enrichment/codebase-context.md:19,22`), so v2 should read Orca's evidence before IronClaude adds its own hooks |

### 3.2 The arrival vs change matrix (core detection logic)

Case 1 shows that heartbeat arrival and heartbeat change must be read as two separate bits. With transcript activity as a third bit:

| Heartbeat arrives on cadence | Token changes | Transcript active (< 5 min) | Most likely state |
|---|---|---|---|
| yes | yes | any | S1 `progressing` |
| yes | no (2 or more windows) | yes | S6 `context-exhausted` (thrash loop) or a repetition loop. Confirm with SG-3 |
| yes | no (1 window) | yes | S1/S2, inside a long unit. Wait one more window |
| yes, but no token | n/a | any | Process-exists only. The state is decided by the other signals (FR-002) |
| no | n/a | yes | S2 `long-step-in-progress` (Agent fan-out, accepted by WC-10) |
| no | n/a | no | S3, S4 or S5. Separate them with SG-9, the pending-ask record and SG-3 |
| no | n/a | unreadable | S7 or S11. Probe with SG-8 |

UNVERIFIED: which component sent the case 1 heartbeats. The description says they "came from a timer, not from progress" (`description.md:11`). If a harness-level timer sends them (not the agent), they can never carry an agent-written token, and FR-002 already treats them as process-exists only. If the agent sends them, the token freezes during thrashing and row 2 catches it. The design is correct under either hypothesis.

### 3.3 Adapter boundary

- **Core (harness-neutral):** progress tokens and deadlines (SG-1, SG-5), message coverage and acknowledgements (SG-6, SG-7), contract file (SG-10), owner-scoped filesystem activity (SG-2), the state machine and the ladder.
- **Orca adapter:** mailbox (`check`, `reply`, `send`), fleet verdict (SG-8), prompt-wait (SG-9), nudge with turn-start receipt (`terminal send --text --enter --wait-submit`, `enrichment/codebase-context.md:23`).
- **Claude Code adapter:** screen patterns (SG-3), transcript reading via Orca (SG-4), hook events (SG-11, v2).

- **FR-006.** The core decides a state only from core signals plus *normalized* adapter observations (`{kind, value, observed_at, source}`, section 11). It never matches screen text itself.
- **FR-007.** Screen classification (SG-3) may *confirm* or *refine* a state after a core trigger (SG-1, SG-5, SG-9). On its own it may move a worker into S6 only when the matched text is a known exhaustion pattern seen in two reads at least 5 minutes apart. Even then a restart still needs Orca stall proof or the person's go (section 8.2, S6 row).

## 4. Detection Rules and Time Bounds

### 4.1 Sweep loop

The bounds below come from one loop, not from per-worker timers:

- **FR-008.** The coordinator waits with `check --wait`, all types (section 6), and `--timeout-ms 300000` (5 minutes). The guide's canonical value is 900000 (`enrichment/codebase-context.md:15`); 5 minutes is needed for the 15-minute target, because detection takes trigger plus confirmation, which is at least two sweeps. After every wake *or* timeout it runs one **sweep**.
- **FR-009.** A sweep makes these cheap calls for the whole fleet: one `worker-list` (SG-8), one prompt-wait listing (`worktree ps --agent-wait`, SG-9), one `stat` per worker contract path (SG-10), and an update of each worker's heartbeat record (arrival time, token, declared window). Costly probes (transcript tail SG-4, screen read SG-3) run **only** for workers that met a trigger in this sweep.
- **FR-010.** The expected-silence window for a worker is `W = max(10 min, 2 x its observed median heartbeat interval)`, or the worker's declared `expect_silence_min` when one is active, capped at 45 minutes. The coordinator derives W from evidence, so the preamble keeps sole ownership of cadence (`WORKER-CONTRACT.md:7`).

Why the loop design: in the observed run, the only sweep trigger was "after three consecutive empty waits" of up to 15 minutes each, so up to 45 minutes (`enrichment/codebase-context.md:20`). Case 8 was found by such a sweep after 46 minutes (`issue-body.md:23`). That matches the documented trigger, and it is the most likely root cause of that latency (confidence: medium-high).

### 4.2 Per-state rules

All bounds are measured from the moment the state actually began to the moment the coordinator records it. They assume FR-008 (5-minute sweeps); a slower loop adds the difference.

| State | Trigger (core) | Confirming probe | Detection bound | Notes |
|---|---|---|---|---|
| S0 `starting` | No token and no transcript activity 10 min after start | Transcript tail; `agentWait` (a launch prompt is S4; compare #315, `issue-body.md:64`) | **15 min** | Startup grace avoids false stalls (`enrichment/research-light.md:18,22`) |
| S1 `progressing` | Token changed within W | None | n/a | |
| S2 `long-step-in-progress` | Declared window active; or no token change but transcript activity < 5 min | Transcript tail when the declared window passes | Re-checked every sweep. Once activity stops it moves to S3, S4 or S6 within **10 min** | A declared window is capped at 45 min; then it is probed like any silence |
| S3 `idle-at-prompt` | No token change for W (default 10 min), or no heartbeat for 2 x the median interval | (1) transcript last timestamped entry is 5 min or older and the final turn sent no `worker_done`; (2) adapter classifies an empty input prompt with no tool running; (3) no pending ask for this worker | **15 min** (W 10 + one sweep 5) | Both (1) and (2) are needed. (1) alone cannot tell "waiting on a long tool call" from "idle" when the harness writes no entry during a tool call (UNVERIFIED for Claude Code) |
| S4 `blocked-on-person-prompt` | `agentWait` non-null for the worker in the sweep's prompt-wait listing | Screen read to capture the prompt text for the person | **5 min** after the prompt appears, plus Orca's own observation delay (UNVERIFIED) | Polled for *every* worker, every sweep. Not tied to silence, because heartbeats may continue from a timer |
| S5 `blocked-in-ask` | `question` message received from the worker | None. The pending-ask record is the evidence | **1 wait cycle (5 min)** to see the question | The ack deadlines in section 7 bound the answer path |
| S6 `context-exhausted` | Heartbeats *arrive* but the token is unchanged for W; **or** the S3 trigger fires; **or** (v2) the adapter reports 3 or more compaction events in 30 min | Screen read: known exhaustion text (for example `Autocompact is thrashing`, `issue-body.md:43`) | **15 min** to a recorded S6 (W 10 + one sweep). Restart decisions need a second read 5 min later | The frozen-token trigger fires at one W, not two, so a read happens within the target |
| S7 `unreachable` | `projection.liveness` = `unverifiable` | Re-read next sweep | **5 min** | Report to the person after **30 min** continuous; never stop or retry (`WORKER-CONTRACT.md:72`) |
| S8 `exited` | `projection.liveness` = `exited` | None (positive proof) | **5 min** | Settled per WC-6 |
| S9 `finished-unreported` | Contract file appears and no `worker_done` arrived within one sweep; or a non-`worker_done` message whose body names a report path or says the work is complete | Read the contract's `worker_status`; check the brief has no later `Command:` line | **5 min** (one wait cycle) | Case 4's bound drops from about 4 hours to 5 minutes |

- **NFR-004.** Every sweep makes a fixed number of fleet-wide Orca calls (three), whatever the fleet size, plus at most two costly probes for each worker that met a trigger. This keeps an LLM coordinator's context cost per sweep near constant and keeps per-worker probe cost proportional to suspicion.
- **NFR-005.** The thresholds (W minimum 10 min, inactivity 5 min, sweep 5 min, declared-window cap 45 min) are starting values to tune from logged transitions (FR-005), not proven optima. OpenHands reports that early stuck-detector thresholds gave false positives (`enrichment/research-light.md:48`).

## 5. Mapping of the 8 Observed Cases

Each case lists two causes. The **occurrence cause** is why the worker got into the state. The **detection cause** is why the coordinator did not notice. Most of the hours lost came from the detection cause. Confidence is given for each.

| # | Case (`issue-body.md`) | Root cause and confidence | State | Detecting signal (new design) | Bound | Response |
|---|---|---|---|---|---|---|
| 1 | #339 first session stuck about 4 h; full context, autocompact thrashing; "implementing" heartbeats kept arriving (`:16`) | **Occurrence:** the session's working set (large reports read whole, long chain) exceeded the context window, so each compaction refilled within 3 turns (`:43`). Confidence **medium**: the error text is verbatim, but which files filled the context was not recorded. **Detection:** heartbeat arrival was read as progress, and the heartbeat carried no progress content (`description.md:11`). Confidence **high** | S6 | SG-1 arrival-without-change (token frozen for W) leads to an SG-3 confirming read | 15 min | L1 confirm, L2 interrupt and handoff request, then L4 restart with resume note when stall proof exists, else L5 report (section 8) |
| 2 | #339 replacement idle about 4 h at the input prompt; last file change 12:07; restarted by a terminal nudge, then stopped again (`:17`) | **Occurrence:** the agent ended its turn with work left. In a turn-driven harness nothing starts a new turn, and the v1 contract has no rule against ending a turn between chain steps. Confidence **high** for the mechanism (a typed nudge restarted it, which shows the session was intact and waiting for input). Why the model chose to end its turn: **low** (not recorded). **Detection:** no idle signal was polled, and WC-12 pull means mailbox messages cannot wake an idle agent (`WORKER-CONTRACT.md:59`). Confidence **high** | S3 | SG-5 deadline (no token change for W), confirmed by SG-4 (final turn without `worker_done`) and SG-3 (empty prompt) | 15 min | L2 nudge with turn-start receipt; a repeat in the same Task counts toward the nudge cap (section 8) |
| 3 | #331 silent from 17:10; judged alive at 18:19 from one QA file written 2 min earlier; idle at 18:38 (`:18`, `description.md:13`) | **Detection only:** a *past* write (one file's mtime) was read as a *current* state. The file was the last output before the turn ended. Confidence **high**. **Occurrence:** same as case 2, turn ended (confidence **medium**) | S3 | Same as case 2. SG-2 can only confirm and never decides S1 (section 3.1) | 15 min | L2 nudge |
| 4 | #361 finished 08:22 and sent its closing report as `status`; the wait listened only to `worker_done, escalation, question`; unread about 4 h (`:19`) | **Detection, primary:** the wait's wake filter excluded `status`. The guide's canonical filter has the same gap (`enrichment/codebase-context.md:15`). Confidence **high**. **Detection, secondary hypothesis:** a delivery is the whole FIFO batch and is replayed until acknowledged (`check --help`), so any later wake for another worker's message would have returned the `status` message too. Four hours unseen suggests the coordinator processed only the messages that matched its type of interest and then acknowledged the whole batch. Confidence **low to medium**, not verified. **Occurrence:** the worker broke WC-5, which says closing is `worker_done` exactly once (`WORKER-CONTRACT.md:57`). Confidence **high** | S9 | SG-6 all-types wait; FR-003 whole-batch processing; SG-10 contract on disk | 5 min (one wait cycle) | L1 verify the contract, then L2 nudge "send `worker_done` per WC-5"; L5 if not sent in 10 min |
| 5 | Answers to #331 Gate 3 and #375 task 1 sent by mailbox reply; workers waited 35-40 min until the answers were typed into their terminals (`:20`, `:45`) | **Cause not established** (`issue-body.md:20`). Competing hypotheses, ranked: **H1** (medium): the worker's `ask` timed out (default 10 min, max 30 min, timeout leaves the question pending; `ask --help`) and the agent ended its turn or slept instead of running `ask --resume <id>`. A reply then has no waiting reader. "ask unanswered 40 min" (`:45`) fits a worker re-resuming or reporting across several timeouts. **H2** (low to medium): the worker raised the question with `send --type question` and later `check`, not with blocking `ask`, so the reply waited in a mailbox the worker pulls only at checkpoints (WC-12). **H3** (low): the reply named a message ID other than the pending ask's ID (`reply --id <msg_id>`, `reply --help`). **H4** (low): routing. A new question defaults to the owning Run mailbox (`ask --help`), and the reply reached a different handle. **Common factor, high confidence:** delivery to the mailbox gave no proof of reading (`enrichment/codebase-context.md:16`), and the typed terminal copy worked. The design makes the cause irrelevant to detection | S5 to unread reply | SG-7 ack missing past its deadline | Ack deadline 5 min; terminal copy sent by 10 min (section 7) | Section 7 escalation: terminal-typed copy with `--wait-submit`, then L5 |
| 6 | #394 worker blocked on a permission prompt up to about 20 min ("This shell script runs rm and could not be checked..."), no message (`:21`, `:44`) | **Detection:** `agentWait` exists but no IronClaude rule polls it (`enrichment/codebase-context.md:71`). Confidence **high**. **Occurrence:** the harness's safety check for a shell script it could not analyse asks the person whatever the command's unattended mode says. Whether the worker's permission mode allows that prompt is UNVERIFIED. Confidence **medium** | S4 | SG-9 `agentWait`, polled fleet-wide every sweep | 5 min | L5 report to the person with the prompt text. The coordinator never answers the prompt (section 8) |
| 7 | #339 and #331 stopped between chain steps without a message; silence was ambiguous (`:22`) | **Occurrence:** the worker runs several `Command:` lines (`WORKER-CONTRACT.md:92`), and the end of one command's output reads like a natural end of turn, so the agent stops. No rule says otherwise. Confidence **medium**. **Detection:** silence had one meaning for two states (S2 vs S3). Confidence **high** | S3 (or S2 when a long step was declared) | SG-1 declared window plus SG-4 activity separate S2 from S3 | 15 min | L2 nudge; worker rule WR-1 removes the occurrence (section 9) |
| 8 | #339 replacement hit thrashing again at 18:11; stuck until 18:57 (46 min); the earlier 18:19 alive check missed it; restarted from disk with a "read in small pieces" note (`:23`) | **Occurrence:** the restart repeated the cause. The resumed session again loaded more than the context could hold. A restart that does not change the context load cannot fix a context-load failure. Confidence **high** for "same cause recurred" (same error text); **medium** for "large reads were the load". **Detection:** the sweep ran only after three empty waits, and the alive check used weak signals (cases 1 and 3). Confidence **medium-high** | S6 | Same as case 1 | 15 min | Restart budget rule: a *same-cause* S6 recurrence never gets a plain restart. The resume must reduce the load (split the Task or narrow the inputs), or it goes to the person (section 8.4) |

### 5.1 What the root causes have in common

1. **Proof of a past event used as proof of current state** (cases 1, 3, 8): fixed by FR-002, SG-2 limits and the arrival/change matrix.
2. **No non-destructive response to silence** (cases 2, 3, 7, 8): fixed by deadlines that trigger probes and nudges (SG-5, section 8), without touching WC-10's ban on stopping on absence.
3. **A delivery treated as a read** (cases 4, 5): fixed by the all-type wait, whole-batch processing and worker acknowledgements (sections 6, 7).
4. **Known evidence never polled** (case 6, and partly 1): fixed by the fixed-cost fleet sweep (FR-009).
5. **Worker behaviours that create the states** (cases 2, 7, 8, and case 4's wrong type): fixed by worker-side rules (section 9).

## 6. Message-Type Coverage

### 6.1 Mechanism (verified)

`orca orchestration check --help` (read 2026-11-07) says: "`--types` is the wake condition for `--wait`; a returned Delivery is always the whole FIFO batch, so it is never filtered by type", and "A bound Run replays the same Delivery until `--ack` or all its messages are marked read ... process every message before acknowledging." So a narrow filter *delays* a message; it does not drop it. A message is lost from attention only when the coordinator acknowledges a batch it did not fully process.

- **FR-011.** The coordinator's wait lists every type explicitly: `--types "status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat"`. It does not rely on leaving out `--types`, because what `--wait` does without `--types` is not stated in the help (UNVERIFIED).
- **FR-012.** For each returned delivery the coordinator handles **every** message through the table below, records each message ID with its handling in the run notes, and only then runs `check --ack <deliveryId>`.
- **FR-013.** A message whose type is not in the table (a future Orca type, or a misspelling) is **surfaced**: logged with its full body, shown to the person in the next status report, and treated as possibly blocking (the sender's state is set to S11 and probed). It is never acknowledged silently.

Waking on `heartbeat` makes the coordinator wake often. That is intended: each wake updates the heartbeat record (FR-009) and costs one small batch. If wakes become too frequent, the coordinator may batch-process heartbeats without a sweep, but it may not filter them out of the wake set. Each wake still runs a sweep at most once every 5 minutes.

### 6.2 Per-type handling (coordinator side)

| Type | Expected sender and meaning | Liveness effect | Coordinator action |
|---|---|---|---|
| `heartbeat` | Worker top-level session, at preamble cadence (`WORKER-CONTRACT.md:61`) | Arrival: process exists. Token change: S1. Declared window: S2 | Update the record (FR-009). No reply |
| `status` | Worker progress note, or a mis-typed closing report (case 4) or ack (section 7) | Treated like a heartbeat for arrival. Content can set S9 or clear a pending ack | If the body or payload is an `ack`, apply section 7. If it names a report path or says the work is complete, set S9 and run its rule. Otherwise log it |
| `worker_done` | Worker, exactly once (`WORKER-CONTRACT.md:57`) | S10 | Open the contract (`WORKER-CONTRACT.md:88`); apply "Reading a result" (`:119-128`). A second `worker_done` for the same dispatch is logged as a contract violation and ignored |
| `question` | Worker under `On a blocked gate: ask the coordinator` (`WORKER-CONTRACT.md:53`) | S5 | Answer with `reply --id <that message id>` within the coordinator's answer bound, or forward to the person. Start the ack clock (section 7) |
| `escalation` | Worker reporting a problem it cannot resolve | Keeps the current state; flags it for attention | Probe (L1), then report to the person (L5) when it needs a person's decision |
| `decision_gate` | Worker or Orca asking for a decision | S5-like: the worker waits on a decision | Ruling halts and other person-only decisions go to the person, never answered by the coordinator (`WORKER-CONTRACT.md:55`) |
| `handoff` | A worker passing work or context | Can mean the sender is finishing; check for S9 | Read it; if it implies a new unit of work, the coordinator decides (WC-13, `WORKER-CONTRACT.md:60`) |
| `merge_ready` | A worker saying its branch is ready | Can mean finished; check for S9 | Merges are coordinator actions only with the person's instruction (`WORKER-CONTRACT.md:106,111`). Log it and check that `worker_done` follows |
| `dispatch` | Normally coordinator to worker. Received by the coordinator only through misrouting or an echo | None | Log it as unexpected (FR-013 path) |
| *unknown* | Any | S11 for the sender | FR-013 |

### 6.3 Worker side

- **FR-014.** A worker sends its closing report only as `worker_done` (WC-5). A `status` message never carries a closing report (WR-6, section 9). Section 6.2 still catches a mis-typed one, so FR-014 reduces the occurrence and FR-011/FR-012 cover the detection.
- The worker's own `check` (WC-12) returns the whole batch too. WR-4 (section 9) asks it to handle every coordinator message in the batch before acknowledging it, mirroring FR-012.

## 7. Reply Read-Acknowledgement Protocol

### 7.1 Why an application-level ack

Orca's own reference says a successful `send` "proves durable enqueue", and wake and nudge prove neither reading nor a started turn (`enrichment/codebase-context.md:16`). `check --ack` acknowledges the reader's *own* batch and is not visible to the sender as a receipt (same source). This matches MQTT QoS 1, where PUBACK comes from the broker, not the reader (`enrichment/research-light.md:34-35`). The only proof that the agent read an answer is a message the agent itself sends after acting on it.

### 7.2 What the worker sends

- **FR-015.** When the worker's top-level session receives a coordinator message that needs action (the answer to its `ask`, a `reply`, or a follow-up found by `check`), it sends one acknowledgement **before** acting on the content. The ack uses the preamble's `send` command with type `status` and a body that starts with this fixed line:

  ```text
  ack <message_id> <applied|queued|refused> <one-line reason>
  ```

  `applied`: the answer will be used now (for example the WC-3 re-invocation). `queued`: it is understood and will be used at the next step boundary. `refused`: it cannot be used (for example an answer to a Ruling halt, `WORKER-CONTRACT.md:55`, or an answer that arrived after the worker settled, `:56`). If the preamble's send command takes a JSON payload, the same fields also go there as `{"ack": "<message_id>", "disposition": "...", "v": 1}`. The fixed body line stays the authority, so an adapter without payloads still works.
- Why `status` and not a new type: Orca's type list is closed (`enrichment/codebase-context.md:14`), and the coordinator now wakes on `status` (FR-011). The body prefix makes the ack machine-checkable.
- WC-7 holds: only the top-level session sends the ack (`WORKER-CONTRACT.md:58`).

### 7.3 Timeouts and escalation (coordinator)

The clock starts when the coordinator's `reply` or `send` returns success.

| Step | Time after send | Condition | Coordinator action |
|---|---|---|---|
| A1 | 0 | Reply sent | Record `pending_ack[<message_id>] = {worker, sent_at, copy_count: 0}` |
| A2 | 5 min | No ack | L1 probe: prompt-wait (`agentWait`), transcript tail, screen read. If the worker is S4 (person prompt) or S6 (exhausted), switch to that state's rule. Otherwise go to A3 |
| A3 | 5 min (right after A2) | No ack, worker S3, S5 or S11 | Send a **terminal-typed copy**: `orca terminal send --text "<copy text>" --enter --wait-submit <s>` (`enrichment/codebase-context.md:23`), the only verb with an observed turn-start receipt. Record the receipt fields (input accepted / submitted / turn started) |
| A4 | 10 min | No ack after the copy, or the receipt shows no turn start | Second copy only if the first was not submitted. If it was submitted and still no ack, do not retype; go to A5 |
| A5 | 15 min | Still no ack | L5: report to the person with the message ID, the answer text, both receipts and the probe results |

The case 5 bound drops from 35-40 minutes to a typed copy within 5 minutes and a person report within 15 minutes.

Terminal copy text (one line, so it fits a prompt):

```text
[coordinator] Answer to your message <message_id>: <answer>. If you already applied <message_id>, only send: ack <message_id> applied (duplicate). Otherwise send the ack first, then continue.
```

- **FR-016.** A worker without a terminal (`enrichment/codebase-context.md:23`, "Not every worker has a terminal") skips A3 and A4. Unacked at A2 goes straight to A5.
- **FR-017.** The coordinator keeps each pending ack until it is acknowledged, the worker settles, or A5 fires. On settlement, any pending ack is closed as `unacked-at-settlement` and listed in the run notes.

### 7.4 Idempotency

At-least-once delivery means duplicates (`enrichment/research-light.md:32,62`). Here a duplicate can arrive through both the mailbox and the typed copy.

- **FR-018.** The worker keys every answer by message ID. The first copy is acted on. Any later copy of the same ID gets only `ack <id> applied (duplicate)` and no new action. The worker records applied IDs in its handoff file (WR-3, section 9), so a resumed or restarted session can also recognise them.
- **FR-019.** WC-3's single-ask rule stays (`WORKER-CONTRACT.md:54`): a duplicate answer never causes a second re-invocation.
- The coordinator treats a second ack for the same ID as a no-op.

### 7.5 What the ack does not settle

An ack proves the agent read the answer and chose a disposition. It does not prove the answer was right or that the work succeeded. Resolution is still read from the contract after `worker_done`. This follows the #409 rule to keep "delivered", "seen", "answered" and "resolved" separate (`.dev/research/orca-dashboard-20261105/REPORT.md:75`).

## 8. Response Ladder

### 8.1 Rungs

| Rung | Action | Effect on worker | Evidence needed to use it |
|---|---|---|---|
| **L0 observe** | Sweep only | None | Always |
| **L1 probe** | Read-only: `worker-show`, transcript tail via `worker-read --source transcript`, screen read, contract `stat` | None | A core trigger fired (section 4) |
| **L2 nudge** | Typed text through the terminal with `--wait-submit` (section 8.3). In the S6 variant: an interrupt plus a handoff request | Starts a turn; harmless if one is already running (NFR-002) | L1 confirms S3, S9, or S6, or a pending ack reached A3 |
| **L3 ask** | Coordinator asks the *worker* a direct question through a terminal-typed message: "Reply with `status`: current step, what you are waiting for" | Starts a turn | L2 failed once, and the state is still ambiguous (S11, or S2 past its window) |
| **L4 restart with resume note** | Stop the worker, set the old Task `failed --result cancelled`, create a new Task with a resume note (`WORKER-CONTRACT.md:69-73`) | Ends the session | **Orca positive stall proof only**: `exited`, the worker's process exit, or a transcript whose final agent turn sent no `worker_done` (`enrichment/codebase-context.md:20`), **and** the restart budget allows it (section 8.4) |
| **L5 report to person** | A short message in the coordinator's own conversation: worker, state, evidence with times, what was tried, the decision needed | None | Any state that only a person can resolve, or any rung cap reached |

### 8.2 Response per state

| State | Ladder path | Repeat caps |
|---|---|---|
| S0 starting | L1, then L2 nudge "begin your brief", then L5 | 1 nudge |
| S2 long step, window passed | L1 (activity on the transcript resets to S2 with a fresh 15-min window, at most twice), then L3, then L5 | 2 window extensions, 1 ask |
| S3 idle-at-prompt | L1 confirm, then L2 nudge. If not progressing after the nudge: the final turn without `worker_done` is Orca stall proof, so L4 is *allowed*, but run L3 first. L4 only after 2 nudges and 1 ask have failed | 2 nudges per 60 min per Task; a third idle episode in the same Task goes to L5 with a proposal (the Task is too long for one session) |
| S4 blocked-on-person-prompt | L1 to capture the prompt text, then **L5 immediately** | The coordinator never answers the prompt. Re-report every 15 min while it stays open |
| S5 blocked-in-ask | Answer, then section 7 | Section 7's A1-A5 |
| S6 context-exhausted | L1 confirm twice (5 min apart). L2 variant: `terminal send --interrupt` plus "write your handoff file now (WR-3), then end your turn". If the session then ends its turn without `worker_done`, that is stall proof, so L4 under the restart budget. If it does not, L5: ask the person for a go to stop it (v1). In v2, two confirmed exhaustion reads become a stall proof (section 10, C-9) | 1 interrupt; restart budget (8.4) |
| S7 unreachable | L0/L1 each sweep; L5 after 30 min | Never L4 on `unverifiable` (`WORKER-CONTRACT.md:72`) |
| S8 exited | Settle per WC-6, then L4 under the budget, or L5 when the budget is spent | Budget |
| S9 finished-unreported | L1 (read the contract), then L2 nudge "send `worker_done` per WC-5 with `--report-path <path>`", then L5 after 10 min | 1 nudge. The coordinator never sends `worker_done` for the worker (WC-7 lifecycle messages come only from the worker) |
| S11 unknown | L1; then as the resulting state | n/a |

### 8.3 Nudge text

Requirements: one line; idempotent; harmless if the session is working; tells an idle worker the next action without changing its task (NFR-002).

```text
[coordinator liveness check <UTC time>] If a step is running, ignore this and continue. If your turn ended before worker_done, continue with your next Command: line now. If all Command: lines are done, send worker_done per WC-5. Do not restart finished steps.
```

- **FR-020.** Every nudge uses `--wait-submit`, and the result (accepted, submitted, turn started) is logged. A nudge whose receipt shows no turn start counts as failed for the caps.
- What happens when typed text arrives while a tool call is running is UNVERIFIED for Claude Code (it may be queued as the next user message). The nudge text is written so that it is harmless when read late.

### 8.4 Restart budget and same-cause rule

Following OTP restart intensity (`enrichment/research-light.md:26-28`) and SQS dead-lettering (`:32`):

- **FR-021.** The budget is per **unit of work** (the original Task and all its replacement Tasks), because every retry is a new Task (`WORKER-CONTRACT.md:69`) and Orca counts failures only per Task (`:71`). The budget is **2 restarts in 6 hours** per unit, on top of WC-6's existing three-failed-starts limit (`:71`). When it is spent, go to L5.
- **FR-022.** **Same-cause rule (from case 8).** Each restart records its cause class (`idle`, `context-exhausted`, `exited`, `unreachable-then-exited`). If the replacement ends in the *same* class as the previous attempt, a plain restart is not allowed. For `context-exhausted`, the next Task must reduce load: split the remaining `Command:` lines across Tasks, or pass narrower inputs. Otherwise go to L5 with that proposal. Restarting into the same load repeats the failure (case 8, confidence high).

### 8.5 Resume-note format

The resume note goes in the **new Task's brief** (a brief cannot change after creation, `WORKER-CONTRACT.md:69`), after the guard line and before the `Command:` lines (`:92`):

```text
Resume: replaces Task <old task id> (cause: <class>, evidence: <source>@<time>).
Completed Command: lines: <n of m>, contracts: <paths>.
Last progress token: <step>/<counter>.
Handoff file: <old report-dir>/handoff/<latest>.md (read this first, at most 80 lines at a time).
Answered message IDs already applied: <ids>.
Load rule: read reports and logs in pieces of at most 80 lines; do not reread whole prior reports.
Start at: Command: line <k>.
```

The new Task gets its own report directory (`WORKER-CONTRACT.md:69,81`). The old directory is read-only input. For an `/sc:implement` Task, the D2 freeze rules (`:132-137`) take priority: an `E-RESUME-NEEDED` re-run is the command's own resume, not this note.

### 8.6 What never happens on silence alone

- **FR-023.** On silence, a passed deadline, `unverifiable` liveness or screen text alone, the coordinator never: stops a worker; creates a retry Task; releases a worker or worktree; marks a Task failed; answers a permission or person-only prompt; writes or drafts a Ruling (`WORKER-CONTRACT.md:55`); sends a lifecycle message for the worker. Silence authorizes L1, L2 and L3 only (section 10, C-1).

## 9. Worker-Side Rules

Root cause addressed: in cases 2, 3 and 7 the worker made itself unobservable by ending a turn (confidence high for 2 and 7, medium for 3). In cases 1 and 8 it made itself unrecoverable by loading too much context (high). In case 4 it reported the right content under the wrong type (high). The coordinator-side rules in sections 4 to 8 bound detection time. The worker-side rules below remove the causes.

### 9.1 Rules

| ID | Rule | Cause removed | Home |
|---|---|---|---|
| **WR-1 continuous chain** | The worker session does not end its turn between `Command:` lines. It ends a turn only (a) after sending `worker_done`, (b) while blocked in the preamble's `ask` (WC-3), or (c) on `consumer_fenced` (`WORKER-CONTRACT.md:59`). After each command finishes, the next action in the same turn is the next `Command:` line, or the WC-5 steps. | Cases 2, 3, 7 | Contract section 3 (new WC-14), plus one brief-layout line (section 10) |
| **WR-2 context-safe reads** | Read any file of unknown size, and every prior report, log or transcript, in pieces of at most 80 lines. Never reread a whole prior report: use its handoff file (WR-3). | Cases 1, 8 | Contract section 3 (new WC-15) |
| **WR-3 per-stage handoff file** | After each `Command:` line completes, the worker session writes `<report-dir>/handoff/<n>-<command>.md` (at most 40 lines): the command line, `worker_status` from its contract, deliverable paths, decisions taken, applied ack IDs (FR-018), and the next `Command:` line. The file is inside the Task's own report directory, so WC-11's single-owner rule holds (`WORKER-CONTRACT.md:45`). It is listed in the top-level contract's `artifacts` (`:32`). | Makes L4 cheap and lossless (section 8.5). Bounds the context needed to resume | Contract section 3 (WC-15). Written by the session, not the command, so commands stay unchanged |
| **WR-4 whole batch** | When `check` returns a batch, the worker acts on or acknowledges (FR-015) every message in it before `--ack` | Section 6 secondary hypothesis for case 4; case 5 H3 | Contract WC-12 amendment |
| **WR-5 progress token** | Every heartbeat carries a token that changes only when on-disk progress changes: step = current `Command:` line index, `n` = count of completed units (for example ledger lines or written files), plus an optional `expect_silence_min`. It is carried in the preamble's heartbeat command, in `--payload` JSON `{"v":1,"step":<k>,"n":<count>,"expect_silence_min":<m>}`, or in the `--phase` text `step <k>/<m> n=<count>` when the preamble's command shows no payload (UNVERIFIED which form a given preamble uses) | Case 1: a timer heartbeat proved the process, not progress (`enrichment/research-light.md:20,60`) | Contract Heartbeats bullet (`:61`). The **cadence** stays the preamble's (`:7`); only the **content** is the contract's |
| **WR-6 closing report type** | The closing report is sent only as `worker_done`, never as `status`, `handoff` or a mailbox reply | Case 4 | Contract WC-5 amendment |
| **WR-7 declare long silence** | Before a step expected to exceed the cadence (an Agent-tool fan-out, a long split wait under WC-10), send one heartbeat with `expect_silence_min` set (at most 45) | Makes WC-10's accepted gap (`:44`) visible, so S2 is not confused with S3 | Contract WC-10 amendment |

### 9.2 Why not the preamble or the commands

- **Not the preamble.** Orca issues it per dispatch, and the contract never copies it (`WORKER-CONTRACT.md:7`). IronClaude cannot change its text. Each rule above is about *what the session does with* the preamble's verbs, which is the contract's job (`:49`).
- **Not the commands.** WR-1, WR-4, WR-5, WR-6 and WR-7 are lifecycle behaviour, which is only the top-level session's job (WC-7, `:58`). Commands contain no Orca calls (`:5`, WC-8 `:38`). WR-2 is a session reading habit. A command-level copy would need to be written in every chain-running command, and it would drift. WR-3's file is written by the session after the command exits, so no command changes.
- **The brief carries a pointer, not a copy.** One added brief line (section 10, C-8) makes WR-1 visible in the prompt the worker actually acts on. This matters because a contract rule that is not in the prompt was likely not applied in cases 2 and 7 (confidence medium: the workers had the contract available and still ended their turn).

### 9.3 Requirements

- **FR-024.** WR-1 to WR-7 are stated once, in `WORKER-CONTRACT.md` section 3. No command file restates them.
- **FR-025.** A handoff file is written even when the command's `worker_status` is `failed` or `blocked`, so a resume always has a starting point.
- **NFR-006.** WR-3 adds at most one file of at most 40 lines per `Command:` line. WR-5 adds no message beyond the cadence the preamble already sets.

## 10. Contract Changes: v1 Now vs v2 (#423)

Test for "v1 now": the change is contract or brief text only. It uses only Orca verbs the preamble or `--help` already documents, and it adds no IronClaude code. Everything that needs a process running between coordinator turns, a harness hook, or stored state is v2.

### 10.1 Change table

| ID | Change | Rule amended | v1 now | v2 (#423) | Constraint respected |
|---|---|---|---|---|---|
| C-1 | Silence past a deadline authorizes probe, nudge and ask only | WC-10 (`:44`) | Yes | Same rule, applied by the monitor | WC-10's "never stop on absence" kept word for word |
| C-2 | Progress token in heartbeat content | Heartbeats bullet (`:61`) | Yes | Typed field validated by the monitor | Preamble keeps cadence and syntax (`:7`) |
| C-3 | Read-acknowledgement of answers | WC-12 (`:59`), WC-3 (`:56`) | Yes | Pending-ack store and timers | Still pull-based; the ack is a worker send |
| C-4 | Closing report only as `worker_done` | WC-5 (`:57`) | Yes | n/a | WC-7 lifecycle from top level only |
| C-5 | WC-14 continuous chain (WR-1) | new | Yes | Stop-hook enforcement (C-11) | WC-7, WC-8 |
| C-6 | WC-15 chunked reads and handoff files (WR-2, WR-3) | new | Yes | Context-usage telemetry (C-13) | WC-11: file is in own report dir |
| C-7 | Coordinator "Liveness supervision" subsection: all-types wait, whole batch, 5-min sweep, ladder, caps, budget, resume note, never-on-silence list | new, contract section 4 | Yes (as coordinator procedure) | Deterministic monitor | WC-6, WC-10 |
| C-8 | Brief layout: one added line after the guard line | Brief layout (`:92-96`) | Yes | Template field | Guard line unchanged |
| C-9 | Twice-confirmed context exhaustion counts as stall proof | WC-6 (`:73`) | **No**: needs Orca or the person to accept a new proof kind | Yes, if Orca's recovery rules are extended or the person approves it as an IronClaude-only proof | WC-6: positive proof still required; this widens what counts, which is a policy change |
| C-10 | Liveness monitor process | n/a | No | Yes | SA-2 boundary open (13.2, Q6) |
| C-11 | Claude Code hook forwarding (Notification, Stop, PreCompact, SessionStart) | n/a | No | Yes, Claude Code adapter | Hooks are harness adapters, not core |
| C-12 | #409 dashboard fields: state, evidence source, observed_at, freshness, delivery stage | n/a | No | Yes | REPORT :41, :75 |
| C-13 | Context-usage telemetry and versioned screen patterns | n/a | No | Yes | FR-007 stays the v1 floor |
| C-14 | Restart-budget store across Tasks | n/a | Run notes (v1) | Persistent store | WC-6 three-failed-starts (`:71`) unchanged |

### 10.2 Proposed wording (v1)

**C-1, WC-10, replace the last sentence of `:44`:**

> The coordinator therefore treats a missing heartbeat as absence, never as death: it never stops, retries or releases a worker because a heartbeat is late, and it stops, retries or releases only on Orca's stall proofs. Absence past the deadline in "Liveness supervision" (section 4) authorizes only read-only probes, a typed nudge and a direct question to the worker, in that order. A worker that announced a long step with `expect_silence_min` is not probed before that window ends.

**C-2, Heartbeats bullet, add after the first sentence of `:61`:**

> Each heartbeat carries a progress token, in the preamble command's payload or phase text: the current `Command:` line index and a count that rises only when on-disk progress rises (WC-15), plus `expect_silence_min` before a step expected to outlast the cadence. A heartbeat whose token has not changed is evidence that the process exists, not that the work is progressing.

**C-3a, WC-12, append to `:59`:**

> When `check` returns a batch, the worker handles every message in it before acknowledging the batch. For each coordinator message that answers or directs it, the worker first sends `status` with a body starting `ack <message_id> applied|queued|refused`, then acts. A message ID already applied gets only `ack <message_id> applied (duplicate)`.

**C-3b, WC-3, append to the timeout bullet `:56`:**

> When the answer arrives, the worker sends the WC-12 ack for that message ID before re-invoking the command.

**C-4, WC-5, append to `:57`:**

> The closing report is never sent as `status`, `handoff` or a reply; a coordinator may not read those as completion.

**C-5, new WC-14 (contract section 3):**

> **WC-14. No turn ends between chain steps.** The worker session ends its turn only after `worker_done`, while blocked in the preamble's `ask`, or on `consumer_fenced`. When a `Command:` line finishes, the next action in the same turn is the next `Command:` line, or the WC-5 steps after the last one.

**C-6, new WC-15 (contract section 3):**

> **WC-15. Context-safe reading and handoff files.** The worker reads prior reports, logs and transcripts in pieces of at most 80 lines and never rereads a whole prior report. After each `Command:` line, whatever its outcome, the worker session writes `<report-dir>/handoff/<n>-<command>.md` (at most 40 lines: the command line, `worker_status`, deliverable paths, decisions, applied message IDs, the next `Command:` line) and lists it in `artifacts`.

**C-7, new subsection "Liveness supervision" under section 4.** Its content is sections 4, 6, 7 and 8 of this spec in short form: wait with every type listed and `--timeout-ms 300000`; process the whole batch before `--ack`; a sweep after every wake or timeout; the state table; the ladder with caps; the restart budget; the resume note in the new Task's brief; the never-on-silence list. One sentence ties it to WC-6: "An idle worker whose transcript's final agent turn sent no `worker_done` and that did not resume after two nudges and one direct question has met Orca's stall proof; the coordinator then settles it under WC-6."

**C-8, brief layout, line added after the guard line:**

```text
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
```

### 10.3 Constraints check

- **WC-6.** Every restart is still a new Task after positive proof (`:69`, `:73`). C-7's sentence names an *existing* Orca proof kind (final turn without `worker_done`); it does not create a new one. C-9, which would, is deferred to v2 and needs approval.
- **WC-7.** Ack lines, heartbeats and `worker_done` are sent only by the top-level session. Subagents send nothing.
- **WC-8.** No command gains an Orca call. Every new duty is a session duty (section 3) or a coordinator duty (section 4).
- **WC-10.** The "never stop, retry or release on absence" sentence is kept. C-1 only adds what absence *does* authorize.
- **Preamble owns cadence (`:7`).** C-2 sets heartbeat *content*. It names no verb syntax and no interval.

### 10.4 v2 scope for #423

#423 is about cross-agent knowledge sharing and names #339 as the prerequisite for session supervision (`seed-brief.md:81`). This spec proposes that #423 own: C-10 monitor (the sweep and ladder from section 8 as code, with the core and adapters from section 11); C-11 hook forwarding; C-12 dashboard fields shared with #409; C-13 telemetry; C-14 budget store; and the C-9 policy decision. #339's hourly `sc:sweep` is too coarse to meet NFR-001 (`seed-brief.md:81`) and is replaced by the 5-minute sweep.

## 11. Portability and Extension Points

Root cause of the current non-portability: the observed checks were Claude-Code-specific (screen reading, one file's mtime) and Orca-specific (filter strings), and they were mixed into one coordinator judgement. The design separates the **state model and ladder** (core, harness-neutral) from **how a fact is observed or an action is delivered** (adapters).

### 11.1 Adapter interface

The interface is stated as a capability contract, not code (design only). Every return value is a normalized observation (FR-006) or an action receipt.

| Operation | Returns | Used by | Required? |
|---|---|---|---|
| `observe_fleet()` | per worker: `{kind: process_verdict, value: live\|unverifiable\|exited, reason, observed_at, source}` | S7, S8 | Required |
| `observe_messages(since)` | whole batch, every type, with `message_id`, `type`, `sender`, `sent_at` | SG-1, SG-6, SG-7 | Required |
| `prompt_wait(worker)` | `{waiting: true\|false\|unknown, prompt_text, observed_at, source}` | S4 | Optional; `unknown` if absent |
| `last_activity(worker)` | `{last_agent_turn_at, last_tool_call_at, final_turn_sent_done: bool\|unknown, observed_at}` | S2 vs S3, stall proof | Optional; without it S3 falls back to SG-3 and person report |
| `read_screen(worker)` | classified `{class: working\|idle\|person_prompt\|context_exhausted\|unknown, pattern_id, pattern_version, observed_at}` | SG-3 confirm only | Optional |
| `report_dir_state(task)` | contract present, `worker_status`, newest handoff file, mtimes | S9, resume note | Required (filesystem) |
| `nudge(worker, text)` | `{accepted, submitted, turn_started: bool\|unknown}` | L2, A3 | Optional; without it L2 is skipped to L5 (FR-016) |
| `interrupt(worker)` | receipt | S6 L2 | Optional |
| `stop(worker)`, `start_task(brief)` | receipt, new IDs | L4 only, only after stall proof | Required for L4 |

### 11.2 First adapters

| Adapter | Implements | Backing facts (documented, not run here) |
|---|---|---|
| Orca mailbox | `observe_messages` | `check --wait --types <all 9>`, `--ack`, `reply` (`seed-brief.md:65-67`) |
| Orca fleet | `observe_fleet`, `prompt_wait`, `stop`, `start_task` | `worker-list` liveness, `worker-show` `observation.agentWait`, `worktree ps --agent-wait` (`seed-brief.md:68-69`); WC-6 for `start_task` (`WORKER-CONTRACT.md:69`) |
| Claude Code terminal and transcript | `last_activity`, `read_screen`, `nudge`, `interrupt` | `worker-read --source transcript` (never a guessed path), `terminal read --screen`, `terminal send --text --enter --wait-submit` (`seed-brief.md:67,70,75`) |
| Filesystem | `report_dir_state` | contract and handoff files (WC-4, WC-15) |

### 11.3 Another harness

A harness without a transcript or a terminal (for example a headless API agent) implements only the required operations. The core then works in a degraded but safe mode: S3 and S6 can be reached only through the progress token (SG-1) and the contract file. Every case it cannot classify goes S11, then L1, then L5. It never goes to L4 without an adapter that can give stall proof. This is the safety property that makes partial adapters acceptable.

### 11.4 Extension points

- **Screen patterns** are versioned data `{pattern_id, harness, harness_version_range, regex, class}`. The case 1 and case 8 text (`.dev/issues/431/issue-body.md:43`) and the case 6 prompt text (`:44`) are the first entries. They are confirming evidence only (FR-007).
- **Hook events** (v2, C-11): a harness that emits typed events (Claude Code Notification `permission_prompt`/`idle_prompt`, Stop, PreCompact, SessionStart `compact`; `enrichment/research-light.md:39-46`) maps them into the same observation kinds. They make detection faster and never become a new authority for L4.
- **Message-type registry**: the 9 types plus an `unknown` row (FR-013). A new Orca type is added as data.
- **Boundary rule.** Under SA-2, no command, skill or agent runs an `orca` command (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:980`). In v1 the coordinator session itself runs these verbs, as today. Whether a v2 monitor may live in IronClaude package code and call Orca, or must be an Orca-side or coordinator-side process, is open (13.2, Q6).
- **NFR-007.** Adding a harness changes only adapter code and pattern data, never the state table, precedence, ladder or caps.

## 12. Risks, False Positives and Edge Cases

| # | Risk or edge case | Likelihood | Impact | Mitigation in this design |
|---|---|---|---|---|
| R1 | Nudge typed while a tool runs is queued and read later, possibly mid-reasoning (UNVERIFIED Claude Code behaviour) | Medium | Low | Nudge text is idempotent and harmless late (8.3); 2-nudge cap; never sent in S2 inside its window |
| R2 | False S3: a long Agent-tool fan-out looks idle on screen (WC-10's accepted gap, `WORKER-CONTRACT.md:44`) | Medium | Low | WR-7 declares the window; S2 precedence over S3 when the transcript shows activity; a nudge is harmless anyway (NFR-002) |
| R3 | Screen classifier breaks on a harness update | High over time | Medium | Screen is confirming only (FR-007); patterns versioned (11.4); unknown screen gives S11, never L4 |
| R4 | Worktree activity attributed to the wrong worker in a shared worktree (case 3) | High in shared worktrees | Medium | SG-2 counts only the worker's own report dir or child worktree, and is confirming only |
| R5 | Clock skew between Orca observation time, file mtimes and the coordinator | Low | Low-medium | Compare times from one source only; freshness from `observed_at` of the same adapter (FR-004) |
| R6 | Dishonest or mechanical token increments (a model bumps `n` without progress) | Low-medium | Medium | `n` is tied to on-disk units the coordinator can count (handoff files, ledger lines); mismatch gives S11 and a probe |
| R7 | Restart loop on a recurring cause (case 8) | Medium | High | Budget 2 per 6 h per unit of work (FR-021); same-cause rule (FR-022); WC-6 three-failed-starts (`:71`) |
| R8 | Typed answer arrives while the worker is blocked in `ask` | Low | Low | The ack plus the message-ID idempotency (FR-018) makes the second copy a no-op |
| R9 | Two listeners (coordinator plus another session) receive the same delivery | Low | Medium | Only the coordinator acks; any other reader uses `--peek`, which does not mark read (`enrichment/codebase-context.md:16`). Whether two consumers on one mailbox both receive a batch is UNVERIFIED |
| R10 | Coordinator token cost of 5-minute sweeps over six workers | Medium | Medium | Fixed 3 calls per sweep (FR-009); costly probes only on trigger (NFR-004) |
| R11 | `idle_prompt` timing unknown, and Notification may not fire in some clients (`enrichment/research-light.md:45-46`) | Medium | Low | Hooks are accelerators only (v2), never the sole signal |
| R12 | Coordinator itself goes idle or loses context, so nothing sweeps | Medium | High | Out of scope for worker liveness. v1: the coordinator's own WC-14-equivalent (wait loop never ends its turn); v2: the monitor runs outside the coordinator's context (Q6) |
| R13 | An S4 prompt is a dangerous action (case 6: `rm` script, `.dev/issues/431/issue-body.md:44`) | Medium | High if answered | The coordinator never answers person-only prompts (FR-023); L5 immediately |
| R14 | An ack line in `status` gets lost in the batch noise | Low | Low | FR-012 logs every message; pending-ack table closes on match by message ID |
| R15 | Interrupting an S6 session corrupts a half-written file | Low | Medium | Handoff file per completed step (WR-3); new Task gets a new report dir (WC-6), so partial files are never reused as inputs |

**False-positive budget.** The design accepts many false-positive *nudges* (cheap, idempotent) in exchange for zero false-positive *stops* without proof. This is the same trade the OpenHands detector moved to after early false positives (one corrective nudge before declaring stuck, `enrichment/research-light.md:47-50`).

## 13. Acceptance Criteria and Open Questions

### 13.1 Acceptance criteria

Each criterion maps to a success criterion in `seed-brief.md:42-47`. They are verified by a **replay test**: each of the 8 cases is written as a table-driven fixture of timed observations (the normalized form, FR-006). The core must produce the expected state, the expected rung and the time from onset to detection. A replay needs no live Orca and no live worker, so it can run in v1 review and later in v2 CI.

| AC | Criterion | Seed criterion | Verification |
|---|---|---|---|
| AC-1 | Each of the 8 cases is classified into the state in section 5, within the bound in section 4: 15 min or less for S3, S4, S6; one wait cycle (5 min) or less for S9 | `:42` | Replay fixtures 1-8; case 1 detected by 20 min after onset at worst (thrashing confirmation 2 reads, 5 min apart, after the 15-min bound), case 4 by 5 min |
| AC-2 | The coordinator wait lists all 9 types. A fixture with an unknown type yields a surfaced message and S11 for the sender, not a silent ack | `:43` | Fixture plus inspection of the C-7 wording |
| AC-3 | Every coordinator answer gets an ack by message ID. With no ack, a terminal-typed copy is sent by 5 min and the person is told by 15 min | `:44` | Fixtures for case 5 under each hypothesis H1-H4; each must reach A3 by 5 min |
| AC-4 | Each state has exactly one ladder path with caps (8.2). No fixture reaches L4 without a stall-proof observation | `:45` | Property check over all fixtures: L4 ⇒ stall proof present ∧ budget left |
| AC-5 | Section 10 separates v1 text changes from v2 work and lists every amended WC rule with proposed wording | `:46` | Review against 10.1 and 10.2 |
| AC-6 | The core uses only adapter operations (11.1). Removing the Claude Code adapter leaves every fixture safe (no L4) though slower | `:47` | Replay with optional adapters disabled |
| AC-7 | Case 8 replay: a second `context-exhausted` attempt for the same unit of work does not get a plain restart (FR-022) | `:45` | Fixture 8 |
| AC-8 | A false-positive fixture (long Agent fan-out with `expect_silence_min=30`) produces no nudge inside its window and at most one nudge after it | NFR-002 | Fixture |

### 13.2 Open questions

| Q | Question | Why it matters | How to settle |
|---|---|---|---|
| Q1 | What caused case 5? H1 ask timeout without `ask --resume`; H2 `send --type question` plus pull-only WC-12; H3 wrong message ID; H4 routing to the Run mailbox | The ack protocol covers all four, but the fix for the root cause differs | Read the run's message log for #331 and #375 (`orchestration inbox` read-only), when available |
| Q2 | Does the preamble's heartbeat command include `--payload`? | Decides WR-5's token form | Read a live preamble |
| Q3 | What does `check --wait` do without `--types`? | If it wakes on all types, FR-011's explicit list is only belt and braces | Orca `--help` or the Orca maintainers |
| Q4 | What values can `projection.attention.categories` take? Does any cover thrashing or idle? | Could replace screen classification for S6 and S3 | Orca documentation |
| Q5 | How old can an Orca liveness observation be at read time? | Sets the real detection floor for S7 and S8 | Orca documentation (`observed_at` is exposed per REPORT :35, but the refresh rate is UNVERIFIED) |
| Q6 | May a v2 liveness monitor live in IronClaude package code and call Orca, given SA-2 (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:980`)? | Decides where C-10 lives | Maintainer decision; SA-2 names commands, skills and agents, not package CLI code |
| Q7 | Why did the harness show the case 6 permission prompt to a worker at all? | A launch-mode fix could remove S4 for this cause | #394 and #412 lines of work (`.dev/issues/431/issue-body.md:63,65`) |
| Q8 | Will the person accept C-9 (twice-confirmed exhaustion as stall proof)? | Removes the L5 wait in S6 | Person decision for #423 |
| Q9 | Does Claude Code queue typed text during a running tool call, and when is it read? | Bounds R1 | One controlled test in v2 |

### 13.3 Recommendation

Adopt the v1 contract text now (C-1 to C-8): it removes the two causes behind most of the lost time (a narrow wait filter and turns ending between chain steps) and bounds the rest with a sweep and ladder that never stops a worker on silence. Build the monitor, adapters, hook forwarding and budget store as #423 v2 work, after Q2, Q3 and Q6 are answered.
