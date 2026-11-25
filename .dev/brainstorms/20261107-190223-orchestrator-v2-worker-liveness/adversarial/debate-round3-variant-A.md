# Debate Round 3: Final Arguments for Variant A (variant-1-opus-architect)

## 1. Final Position

The merged design is the right answer, not Variant A alone: A's three evidence axes with `proof_class` and cost tiers, B's status-body acknowledgement, occurrence/detection split and handoff files, and C's proof, reconcile, stop and settle gates with the input veto.
A's contribution to the merge is the extension scaffolding: one signal registry with named adapters, a lineage-keyed action ledger, and a one-sentence test for what goes in v1 contract text and what waits for #423.
All three HIGH probe items can be closed in v1 with documented verbs plus a few contract sentences. None needs a new Orca proof, typed input into a busy session, or a command-side Orca call.
The common fix is one principle: **a v1 trigger must never depend on a signal the failing worker stops producing, or keeps producing by accident.** Case 1 keeps the transcript fresh, case 5 blocks the ack, and case 8 erases the preamble. Each resolution below uses a signal the failure cannot fake: a semantic-change test, a worker heartbeat when `ask` returns, and the person's recorded action.
Context exhaustion still never reaches L4. Only Orca's three stall proofs, or a person's own recorded stop (amendment below), settle an attempt.

## 2. Resolution of HIGH Items

### INV-005: case 1 detection while heartbeats keep arriving

**Problem restated.** Every v1 route the probe lists either is only proposed (the `step_seq` payload) or reads a signal a thrash loop keeps fresh (the transcript tail, `variant-1-opus-architect.md:169`: "a thrash loop produces fresh entries"). A's own case-1 row (`variant-1-opus-architect.md:275`) triggers on `step_seq`, so a worker without the payload is never probed.

**Proposed resolution: a payload-independent "arrival without semantic change" trigger, plus a screen-inclusive probe and a report-only fallback.**

1. **Trigger (v1, payload optional).** The coordinator keeps, per worker, a *semantic fingerprint* built only from things a thrash loop does not change by itself:
   - the heartbeat `--phase` text (documented free text, `seed-brief.md:65`), and the `ironclaude.progress/1` step id and counter when present;
   - the set of files in the worker's own report directory, including WR-3 handoff files, and the contract's existence (a WC-11-scoped `stat` of the worker's own directory, already agreed under C-013; `WORKER-CONTRACT.md:45`).
   Transcript freshness, heartbeat arrival and `actions_since_last` are **not** in the fingerprint.
   Rule: *if at least one heartbeat arrived in the last Q and the fingerprint has not changed for Q (10 min), schedule a T2 probe.* The trigger fires on case 1 with no payload at all: case 1 sent "implementing" for about four hours (`variant-1-opus-architect.md:165`, `seed-brief.md:17`). A declared long step (WR-7) does not suppress this read-only probe (B New Evidence 1, accepted by C).
2. **Probe content (v1).** The T2 probe reads the screen as well as the transcript, for terminal workers: `orca terminal read --screen` (documented, `enrichment/codebase-context.md:22`) and `worker-read --source transcript` (documented). It classifies:
   - `compact_thrashing` when the screen or the transcript text matches the harness pattern file entry for thrashing. The one known string is "Autocompact is thrashing" (`enrichment/codebase-context.md:67`). The pattern is UNVERIFIED across harness versions and lives in adapter data, not core;
   - `working` when a tool call is visibly running, or the transcript shows a tool result that wrote inside the report directory since the last probe;
   - `unknown` otherwise.
3. **Confirmation (v1).** `context-exhausted` is recorded on a `compact_thrashing` match plus an unchanged fingerprint (the C-A4 concession: incidental writes elsewhere never veto it). Bound: Q (10) + at most one sweep (5) = **15 min**, meeting `seed-brief.md:42` whenever the pattern matches.
4. **Pattern-independent fallback (v1, the case the probe says is missing).** If the fingerprint stays unchanged across **two** consecutive probes with heartbeats still arriving and no `working` classification, the coordinator records `no-semantic-progress (cause unknown)` and reports at L5 with the evidence (phase text, last fingerprint change, probe outputs). Bound: about **25 min**, labelled degraded. It never types, never stops, and never latches exhaustion. A long read-only research step can trip it; the report says so, and its cost is one person-facing message.
5. **v2.** A `PreCompact` (`manual`/`auto`) and `SessionStart` source `compact` hook journal turns compaction into a typed event (`enrichment/research-light.md:42-43`, prior art; firing in every client is UNVERIFIED, `research-light.md:46`). Two or more compaction events inside one unchanged fingerprint window confirm thrash without screen text.

**Bucket.** Items 1-4 are v1: coordinator rules using documented verbs and a stat of the worker's own report directory. Item 5 is v2 (#423).

**WC rule.** Amends **WC-10** (`WORKER-CONTRACT.md:44`) with one sentence: "Heartbeats that arrive with no change in phase text, progress payload or report-directory files for 10 minutes schedule a read-only probe; they are not evidence of progress." This keeps WC-10's "act only on Orca's stall proofs" intact, because a probe and a report are not acts on the worker (`seed-brief.md:71`: nudge and ask are not forbidden; probes are read-only). WR-5 (progress payload) becomes an accuracy improvement, not a precondition.

**Capabilities relied on.** Heartbeat `--phase` text: documented. `terminal read --screen`, `worker-read`: documented. Report-directory `stat`: documented filesystem behaviour. The thrash string matching every harness version: UNVERIFIED. Compaction entry type in the transcript: UNVERIFIED (not relied on in v1). Hooks firing: UNVERIFIED (v2 only).

### INV-020: case 5 when the worker is blocked in `ask`

**Problem restated.** While a worker is blocked in `ask` it sends no heartbeat (`WORKER-CONTRACT.md:56`, `:61`) and cannot send the status ack, and the agreed input veto forbids the typed copy that fixed case 5 in the run (`seed-brief.md:29`). There is no sender read receipt (`seed-brief.md:67`). So "answer enqueued, `ask` still blocked" is invisible.

**Proposed resolution: make the `ask` return observable, then name the contradiction as an anomaly.**

1. **Worker rule (v1, amends WC-3).** Each time the preamble's `ask` returns, the worker session, before anything else, sends one heartbeat with the phase text `ask <message-id>: answered` or `ask <message-id>: timed out, resuming`. This is legal: the worker is no longer blocked at that moment, and it uses the preamble's own heartbeat verb and syntax (`WORKER-CONTRACT.md:7`). When answered, the status ack (WR-4) follows as already agreed. No new message type, no payload dependency.
2. **Coordinator record (v1).** When the coordinator sends an answer to an `ask`, it records in run notes: the ask's message ID, the reply id, and the enqueue time (send proves durable enqueue, `seed-brief.md:67`).
3. **Named anomaly `ask-answer-undelivered` (v1).** Raised by either of:
   - (a) **positive:** a heartbeat `ask <id>: timed out, resuming` arrives after the answer to `<id>` was enqueued. The worker's `ask` cycled without receiving an answer that Orca had accepted. This is direct evidence of case 5 in the ask path;
   - (b) **absence:** the answer to `<id>` was enqueued at t0, and by t0 + T_ask + one sweep there is neither an `answered` heartbeat nor an ack nor a `worker_done`. T_ask is the preamble's `ask` timeout; the probe reads the default as 600000 ms (INV-006). That value is UNVERIFIED here, and the preamble owns it.
   Bound: 10 + 5 = **15 min** from enqueue for (b); (a) is detected at the next wake after the heartbeat, at most 5 min.
4. **Ladder for the anomaly (v1).** No step types into a session whose input `ask` owns.
   - L1: a read-only probe classifies the worker: `ask` call still running (screen or transcript), idle at a positively identified empty prompt, or `unknown`.
   - If idle at an identified prompt (the `ask` returned and the turn ended), the veto no longer applies: L2 typed copy with the same reply id and the `--wait-submit` receipt (as agreed under X-011 and C-034).
   - If the `ask` is still running, or the anomaly came from route (a), the coordinator does not resend and does not type. It reports at L5 at once: the reply id, the answer text, and the evidence, stating "the ask channel did not deliver this answer". The person may type it, because the veto binds the coordinator, not the person.
   - A second `ask-answer-undelivered` in the same lineage marks the mailbox path for that worker as `degraded`. Later answers to that lineage go straight to L5 with the answer text.
5. **B's S5 exit (fixes INV-006 as a side effect).** Remove "the ask times out with no resume (to S3)" (`variant-2-opus-analyzer.md:74`). A worker leaves blocked-in-ask only on observed evidence: an `answered`/`timed out` heartbeat, an ack, `worker_done`, or an identified idle prompt.
6. **v2.** Ask Orca (#423) for a delivery state on the reply, either "consumed by the ask's waiter" or a per-message read receipt (`seed-brief.md:67` documents its absence). With it, route (b) no longer waits a full T_ask.

**Bucket.** Items 1-5 are v1. Item 1 is worker-session contract text, item 3 a coordinator rule, both using only documented verbs. Item 6 is v2 and needs Orca.

**WC rule.** Amends **WC-3** (`WORKER-CONTRACT.md:56`): add after "never creates a duplicate": "Each time `ask` returns, the worker first sends one heartbeat naming the message ID and whether an answer arrived." Adds one section 4 coordinator rule: the anomaly and its ladder above. The Heartbeats bullet (`:61`) stays true, because no heartbeat is sent *while* blocked. It does not touch WC-12 (`:59`).

**Capabilities relied on.** Heartbeat verb and free-text phase: documented. Send proves enqueue: documented. That a resumed `ask` on the same message ID returns an answer enqueued during the previous cycle: UNVERIFIED. This is exactly what route (a) detects when it fails. That workers obey the new heartbeat rule: UNVERIFIED until the first v1 run; until then route (b) still bounds detection.

### INV-023: case 8 recovery after an in-place `/clear` or compaction

**Problem restated.** In the run, one session was cleared and restarted from on-disk files (`seed-brief.md:29`). After `/clear` the current prompt no longer carries the live preamble, so the session is no longer a Worker run (`WORKER-CONTRACT.md:11`, and the guard's "current prompt carries a live Orca preamble", `:16`). A later `worker_done` from it breaks WC-5 (`:57`) and WC-7 (`:58`), and Orca settles the Task on any valid `worker_done` (`:121`). A's FR-025 (`variant-1-opus-architect.md:417`) stops the coordinator from sending `/clear`, but says nothing about a person doing it.

**Proposed resolution: separate clear from compaction in Terms, treat a clear as a person-ended attempt, and recover only through a new Task.**

1. **Terms (v1, section 1).** Add to "Worker run": "A compaction, automatic or manual, does not end a Worker run. A `/clear`, or any reset that discards the conversation holding the preamble, ends it. The session is then an ordinary session and sends no lifecycle message." Compaction must not end the run, or every long run would become non-conformant mid-command. A worker that compacts keeps its Task and Dispatch IDs through the WR-3 handoff file, which records them (add both IDs to the WR-3 field list).
2. **Who may clear (v1).** The coordinator never sends `/clear` or `/compact` (FR-025, unchanged). The harness compacts but never clears on its own. So a clear is always a person's action. Under A's Round 2 amendment, which B adopted ("A stop the person directs in their own session is the person's action; the coordinator records it and then settles the old Task before creating the new one"), a person's clear is such a stop. The amendment gains one clause: "Clearing a worker's session is such a stop."
3. **Coordinator handling (v1).**
   - **Evidence.** The person's statement in the coordinator's conversation, recorded in run notes, is the v1 evidence. A transcript discontinuity seen by `worker-read` (a different transcript, or one without the preamble) is a *trigger to ask the person*, never proof. What `worker-read` returns after a clear is UNVERIFIED.
   - **Settle.** On the recorded clear, the coordinator sets the old Task `failed --result cancelled` with the reason `cleared by person`, under the amended person-stop rule, not under WC-6's stall-proof sentence (`:73`). The settlement is recorded in the lineage ledger, so caps and the same-cause rule carry over (C-018).
   - **Recover.** Recovery is a new Task (WC-6, `:69`) with a resume note built from the WR-3 handoff files and C's `uncertain_effects` check. It runs in a new worker, never in the cleared session: the cleared session holds no current Dispatch ID, and a follow-up `send` cannot carry a new brief (`:74`).
   - **The cleared terminal.** It belongs to the person. The coordinator does not type into it or release it until the person says so.
4. **Late lifecycle messages (v1, the WC-5/WC-7 break).** If a `worker_done` or heartbeat arrives from a dispatch already recorded as cleared:
   - The coordinator records it as a **non-conformant settlement**. It does not dispatch dependents from it.
   - It reads the contract on disk and handles it under the existing `partial` rule (`WORKER-CONTRACT.md:124`): the coordinator records whether the deliverable is usable before anything depends on it.
   - If Orca has already settled the old Task from that message, the coordinator does not create a second settlement. It records the mismatch and still runs recovery through a new Task when the contract is not admitted.
   This reuses an existing rule instead of inventing a new outcome.
5. **The run's actual practice.** The coordinator's guidance to the person becomes: "Do not clear a worker. Stop it, or tell me, and I will create a new Task from its handoff files." That gives the same fresh-context benefit, with a settled old Task and a conformant new run.
6. **v2.** A `SessionStart` hook journal with source `clear` (`enrichment/research-light.md:43`, prior art) gives machine evidence of a clear, so the coordinator need not ask the person. If Orca lets a coordinator fence a dispatch (a `consumer_fenced` result already exists on the worker side, `WORKER-CONTRACT.md:59`; whether a coordinator can trigger it is UNVERIFIED), a cleared dispatch can be fenced. Its later `worker_done` is then refused at the source.

**Bucket.** Items 1-5 are v1 contract text (Terms, the section 4 person-stop amendment, WR-3 fields). Item 6 is v2.

**WC rules.** Amends **Terms "Worker run"** (`:11`), adds the clear clause to the **person-directed stop amendment** in section 4 beside **WC-6** (`:72-73`), and adds a **WC-5** note (`:57`): "a `worker_done` from a session cleared after dispatch is non-conformant; the coordinator admits its contract only under the `partial` rule". WC-7 is unchanged. The fix keeps lifecycle messages tied to the session that received the preamble.

**Capabilities relied on.** Person statement in the coordinator conversation: documented (it is the coordinator's own conversation). `task-update --status failed --result cancelled`: documented (`WORKER-CONTRACT.md:69`, `:73`). Compaction keeping the preamble in context: UNVERIFIED. That is why item 1 puts the IDs in the handoff file. Hook firing and coordinator-side fencing: UNVERIFIED (v2 only).

## 3. Responses to the MEDIUM and LOW Unaddressed Items

- **INV-001 (coordinator loses its own liveness state).** Accept fix. Run notes hold one liveness ledger section (pending acks, latches, lineage counters, due times). Every sweep starts by reading that section, so the coordinator's own compaction or `--resume` loses at most one sweep of state.
- **INV-006 (B's S5 "ask times out with no resume" exit).** Accept fix. Delete the transition. Blocked-in-ask is left only on observed evidence, including the new `ask` return heartbeat (INV-020 item 5).
- **INV-009 (`worker-read` timestamps unknown).** Accept fix. A first-v1-run gate records what `worker-read --source transcript` returns. If timestamps are missing, the transcript-gap trigger degrades to the fingerprint trigger (INV-005) plus `terminal wait --for tui-idle` and the screen. Bounds affected are labelled degraded, and two identical tails stay absence, never proof (C-044).
- **INV-010 (cap precedence).** Accept fix. One lineage ledger: a failed start counts as a restart attempt; the first cap reached moves the lineage to L5; no counter resets on a new Task ID; only a person's recorded disposition resets one. The brief-fix cap (`WORKER-CONTRACT.md:126`) stays separate because nothing ran.
- **INV-011 (lineage identity drifts with each brief).** Accept fix. Every brief carries a fixed `Lineage: T<root>` line, written to run notes before `task-create`. WC-6's "unchanged command line" test (`:71`) ignores report-directory and resume-note path values.
- **INV-016 (correlated silence).** Accept fix. If Orca calls fail, or at least half the live workers (minimum 2) go quiet in one sweep, send one infrastructure report and suspend per-worker escalation. Read-only probes continue. On recovery, all due times are re-based, not fired at once.
- **INV-022 (WR-7 declarations before command fan-out).** Accept, narrowed. The declaration is per `Command:` line from the session (coarse), and commands never emit Orca calls (WC-8, `:38`). The fixed 10-minute read-only probe runs during declared windows anyway (B New Evidence 1). Reject making commands declare.
- **INV-024 (two person-stop paths).** Accept fix. If the person ends the process, `exited` is already Orca's stall proof and WC-6 (`:73`) settles it today. The amendment covers only an interrupt or clear with the PTY still `live` (INV-023 item 2).

## 4. Final Per-Point Positions (still disputed after Round 2)

Points listed as still disputed in any Round 2 "still disputed" list (A, B or C).

| Point | Final winner (A/B/C/merge) | Confidence % | One-line reason |
|---|---|---|---|
| X-007 / C-003 | merge | 85 | A's latch with C's sharpening: it clears only on a validated completed unit (new handoff or contract artifact plus changed step) after confirmation, a restart, or a recorded person disposition, never on heartbeats or counter churn. |
| X-017 / C-031 | merge | 95 | Cause stays UNVERIFIED. H1-H4 are an investigation order for the first v1 run. The ack bound and the new `ask-answer-undelivered` anomaly are cause-independent. |
| C-008 | merge | 90 | A due timer at S, sweep on any wake or timeout once due, at most once per S. The v1 timer is the 5-minute wait timeout. v2 schedules due work independently (C's flood guarantee). |
| C-011 | C (scoped merge) | 80 | Transcript preferred only when the adapter reports it capable and current; screen confirms prompt state; parsing stays in the adapter. The INV-005 probe reads both. |
| C-018 | C | 85 | Caps keyed by incident and lineage, inherited across replacements; C's two automatic nudges per lineage as the initial ceiling (policy, UNVERIFIED as optimal). |
| C-005 | merge | 80 | A payload is a claim needing a non-contradicting signal (A). Progress means a completed unit, not traffic (B/C). This is the same predicate as the INV-005 fingerprint. |
| X-012 / C-019 | C | 60 | Two per lineage binds in both proposals. C's one replacement per hour is the stricter rate window, and A's same-cause rule still blocks like-for-like repeats. Neither number is measured. |
| X-013 | merge | 85 | A 15-minute v1 target with available evidence; C's 6-minute v2 profile only after an end-to-end queue and probe capacity test. |
| X-003 / C-044 | C | 90 | Two identical transcript reads are absence, never Orca's final-turn stall proof; positive completed-turn evidence is required. This withdraws A's Round 1 two-read assumption. |
| C-045 | C | 70 | Record the clock domain (boot identity) with due times; on a change, reconcile and sweep once without resetting budgets. v2, and it pairs with the INV-016 re-basing. |
| Declared-window behaviour (B New Evidence 1) | B | 90 | A declared window defers typed actions only; the 10-minute read-only probe keeps running. INV-005 depends on this. |
| X-006 | merge | 80 | Finished-unreported needs a final `worker_status`, no open eligible ask or re-invocation, and no remaining `Command:` line. File time alone is not input-generation proof (C New Evidence 4). |

**Positions where A now accepts another variant's position:** C-011 (C, scoped), C-018 (C), X-012 / C-019 (C's rate window), X-003 / C-044 (C), C-045 (C), declared-window behaviour (B). A also accepts C's sharpening of A's latch (X-007 / C-003) and C's generation caveat on X-006.
