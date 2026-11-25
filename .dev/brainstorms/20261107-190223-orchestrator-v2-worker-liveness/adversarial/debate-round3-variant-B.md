# Debate Round 3: Final Arguments for Variant B (variant-2-opus-analyzer)

## 1. Final Position

Sources re-read this round: `invariant-probe.md` (all), `debate-round2-variant-{A,B,C}.md` (Agreement Summary, Revised Positions, still disputed), `variant-2-opus-analyzer.md` lines 72, 74, 184, 222, 380, 421, 425, `WORKER-CONTRACT.md:1-80`, `seed-brief.md:17-29, 60-79, 89`, `.dev/issues/431/issue-body.md:16, 23, 43`. Nothing runtime was observed.

1. The merge stands: A's evidence axes and tiered calls, B's occurrence/detection split, status-body ack and handoff, C's proof/reconcile/stop/settle gate and v2 ledger.
2. All three HIGH gaps share one root cause: every variant assumed the worker's own channel (heartbeat, ack, lifecycle message) stays meaningful while the worker is in the failure state. While thrashing, the heartbeat lies. Inside `ask`, the worker cannot speak. After `/clear`, the session is no longer the worker.
3. The fix has the same shape each time: treat the worker channel as a claim, and on a fixed clock look for a contradiction between it and one independent source the coordinator reads itself.
4. Each fix below is a v1 contract sentence plus a v1 coordinator rule built only on documented Orca verbs. Every surface it cannot verify is labelled UNVERIFIED and is never used as stop or retry proof.
5. I withdraw B's Round 2 C-7 rewrite (two reads of the final turn equal a stall proof). C's New Evidence 1 is right; see section 4.

## 2. Resolution of HIGH items

### INV-005

**Root cause.** Case 1 is detectable only if something other than the worker's own heartbeat is compared against time. In the run, timer heartbeats kept arriving with an unchanged "implementing" phase for about four hours (`issue-body.md:16`). B's S6 trigger needed a conformant progress token (`variant-2:184`, payload proposed at `:425`), and its fallback route needed S3, which fresh transcript activity refutes. So a worker with no token reads as advancing. The missing piece is a trigger that does not depend on the worker cooperating.

**Proposed resolution: a semantic-stagnation probe that fires on the coordinator's own clock.**

1. **Trigger (v1, coordinator rule).** For each worker whose liveness is `live`, the coordinator keeps a "last semantic change" time. Only these count as a semantic change:
   - a change in heartbeat phase text or in the progress token (when present);
   - a new or changed file under the Task's report directory, or a new handoff or contract file (local `stat`, already in FR-009);
   - a lifecycle message other than `heartbeat` (`status`, `question`, `handoff`, `worker_done` and the rest).
   
   Heartbeat arrival and transcript growth are deliberately **not** on the list, because a thrash loop produces both (`invariant-probe.md` INV-005; `variant-1:169`).
2. **Probe.** When no semantic change is seen for 10 minutes, the next sweep runs one read-only classification: `orca terminal read --screen` for a terminal-backed worker (documented, `seed-brief.md:70`), and `worker-read --source transcript` otherwise (documented reader; returned shape UNVERIFIED, INV-009). This replaces B's token-only S6 trigger and is the same fixed 10-minute probe B adopted in Round 2 for declared windows. A declared `expect_silence_min` window defers typed actions only, never this probe.
3. **Classification.**
   - Screen shows the exhaustion banner (the literal `Autocompact is thrashing`, documented once at `issue-body.md:43`), or a context-limit message: record S6 and latch it (the latch agreed in Round 2, X-007/C-003).
   - Screen shows a running tool or an active Agent fan-out: record `advancing-unconfirmed`, re-arm the probe for 10 more minutes, take no action.
   - Neither, or no screen exists: record `stagnant-unclassified`. Report it to the person at L5 with the evidence (phase text, last semantic change time, screen excerpt) by the next sweep. This is report-only. It is never stall proof and never leads to L4.
4. **Bound.** 10 minutes of stagnation plus at most one 5-minute sweep: S6 or `stagnant-unclassified` is **recorded within 15 minutes** for every worker, with or without a progress payload. That meets the target at `seed-brief.md:42` without depending on the banner text staying the same, because the fallback outcome is a report, not silence.
5. **Cost.** One screen read per stagnant worker per 10 minutes. False positives (a long read-only research step) cost one read and, at worst, one report; they never cause a typed action.

**Bucket.**
- v1 now: the coordinator rule above, a new section 4 bullet, plus one worker duty: heartbeat phase text names the current `Command:` line index and step, so an advancing worker changes it (amends the Heartbeats bullet, `WORKER-CONTRACT.md:61`).
- v1 first-run verification: record the exact banner text and whether the transcript contains a distinguishable compaction entry (UNVERIFIED, `variant-1:169`). If one exists, add "3 or more compaction entries in 30 minutes" as a second S6 source.
- v2: the adapter's compaction counter and the `PreCompact` / `SessionStart source=compact` hooks as event sources (prior art only, `seed-brief.md:89`); a conformant `ironclaude.progress/1` payload becomes a richer change signal, never a required one.

**WC rule.** Adds a section 4 coordinator rule (proposed number WC-16, "semantic-stagnation probe"). It amends the Heartbeats bullet (`WORKER-CONTRACT.md:61`) with the phase-text duty. It is consistent with WC-10 (`:44`): the probe is read-only and the outcome is a report, never a stop, retry or release.

**Capabilities relied on.** Documented: `terminal read --screen`, `worker-read --source transcript`, `worker-list` liveness, local `stat` (`seed-brief.md:66-71`). UNVERIFIED: worker-read's timestamp shape, the banner's stability, transcript compaction entries. None of the UNVERIFIED items is required for the 15-minute report bound.

### INV-020

**Root cause.** For a worker blocked in `ask`, the design had no observable that separates "the answer reached the `ask`" from "the answer sits in the mailbox unseen". The worker sends no heartbeat while blocked (`WORKER-CONTRACT.md:56`, `:61`), it cannot send an ack from inside `ask`, and the input veto rightly forbids typing. B's S5 exit "times out with no resume" (`variant-2:74`) also cannot be observed (INV-006).

The contract already holds the observable, once one sentence is added. Because no heartbeat is sent *while* blocked in `ask`, the first heartbeat or status after the answer is enqueued proves the `ask` has returned. So the design should make the worker speak at both edges of the block.

**Proposed resolution.**

1. **WC-3 amendment (v1, worker duty), two sentences:**
   - "When `ask` returns an answer, the worker's next Orca call is one `status` whose first body line is `answer received: <question message ID>`, sent before it re-invokes the command."
   - "On each `ask` timeout, before resuming the same message ID, the worker sends one heartbeat with phase `awaiting answer <question message ID>`."
   
   Both happen outside the blocked call, so they do not conflict with "no heartbeat while blocked in `ask`" (`:56`, `:61`). The second also fixes INV-006: "resumed after timeout" now has a visible marker every `ask` timeout (600000 ms default, per `invariant-probe.md` INV-006).
2. **Named anomaly `answer_unconsumed` (v1, coordinator rule).** The coordinator records `T_a`, the time it enqueued the answer to question ID `Q`. It raises `answer_unconsumed` when, at a sweep after `T_a + 10 min`, all of these hold:
   - no `answer received: Q` status;
   - an `awaiting answer Q` heartbeat dated after `T_a` (the `ask` timed out and re-waited on `Q` without seeing the answer), **or** no message of any kind from the worker since `T_a`;
   - no `worker_done` and no new contract.
3. **Ladder for `answer_unconsumed`.** The input veto stays absolute: no typing while the `ask` owns input.
   - L1: re-derive state with `worker-show` and a screen read (read-only), and confirm the answer was sent as a reply to `Q` and not as a fresh message. A wrong reply target is the cheapest cause to rule out and needs no worker action.
   - L2: re-send the answer once, as a mailbox reply to `Q` carrying the same reply ID (A's template ID), so a worker that receives both treats the second as a no-op (INV-013). No terminal text.
   - L5: if `answer_unconsumed` still holds at the next `ask` timeout after L2, report to the person with `Q`, `T_a`, both send receipts and the screen excerpt. The person may answer in their own session. That is the person's action, not the coordinator typing.
4. **Bound.** Recorded within 15 minutes of `T_a` (10 minutes plus one sweep). Reported to the person within about 25 minutes (one more `ask` timeout plus a sweep). That is slower than the 15-minute idle target, and it is stated as such. The only faster remedy, typing, is vetoed for safety, and case 5 is not in the 15-minute list at `seed-brief.md:42`.
5. **Idle-at-prompt case 5 is unchanged.** A worker idle at a positively identified empty prompt still gets the S3 route and a typed copy (A3 as conceded in Round 2).

**Bucket.** v1 now: the WC-3 amendment and the coordinator anomaly rule. v1 first-run verification: whether the preamble's `ask` returns on a reply addressed to `Q`, and how it matches (UNVERIFIED; the preamble is the authority for verb syntax, `WORKER-CONTRACT.md:7`). v2: an Orca-side read receipt or an `ask`-state field in `worker-show` would replace the inference (none is documented, `seed-brief.md:67`).

**WC rule.** Amends WC-3 (`WORKER-CONTRACT.md:56`) and the Heartbeats bullet (`:61`: add "except the single timeout heartbeat in WC-3"). It adds the anomaly to section 4. It does not touch WC-10: nothing is stopped or retried.

**Capabilities relied on.** Documented: mailbox send with durable enqueue (`seed-brief.md:67`), `status` and `heartbeat` types (`seed-brief.md:65`), `worker-show`, screen read. UNVERIFIED: `ask` matching semantics, its default timeout value, and worker conformance with the new sentences (to be checked in the first v1 run with C's conformance gate, C-043).

### INV-023

**Root cause.** The contract defines a Worker run by what the session's *current prompt* carries: a live preamble with Task and Dispatch IDs (`WORKER-CONTRACT.md:11`, `:16`). An in-place `/clear` removes that prompt. A compaction may summarise it away (UNVERIFIED). Either way the PTY stays `live`, so Orca's `exited` proof never fires and WC-6 (`:73`) gives the coordinator no settle path. The run's own mitigation, "one session cleared and restarted from on-disk files" (`seed-brief.md:29`, `issue-body.md:23`), therefore left the old Task unsettled. Any later `worker_done` from that session broke WC-5's exactly-once rule (`:57`) and WC-7's top-level-worker rule (`:58`). The underlying defect is that identity was implicit (whatever the session remembers) rather than checked by the coordinator on every message.

**Proposed resolution.**

1. **Identity check on every lifecycle message (v1, coordinator rule).** A message counts for lifecycle only when its `--task-id` and `--dispatch-id` (documented heartbeat fields, `seed-brief.md:65`) match an unsettled attempt. Any other message is recorded as `foreign` with its body and never changes a Task's state. Its report file may be read as data and offered to the person.
2. **Two separate paths (also resolves INV-024).**
   - **Process ended** (liveness `exited`, `seed-brief.md:68`, `:71`): this is already Orca's positive stall proof, so WC-6 (`:73`) settles the attempt today. No amendment is needed.
   - **PTY alive, session cleared or compacted in place**: this needs the amendment below.
3. **Contract amendment, a WC-6 bullet (v1):** "A worker session that a person or the harness clears in place has ended its Worker run; it is an ordinary session from then on. When the person reports the clear, or the coordinator observes it (below), the coordinator records it as the person's action, stops the worker, sets the old Task `failed --result cancelled` with the reason `cleared in place`, and only then creates any new Task. Work continues only through a new Task started by `worker-start`, never by typing a brief into the cleared session." This is A's person-directed-stop sentence (A Round 2 New Evidence 1), narrowed to the PTY-alive case. C is right that it is amendment text, not existing authority, so it must land in the contract before the coordinator uses it.
4. **Compaction in place is not a clear.** A compacted session stays the Worker run while its messages keep passing the identity check in step 1. If, after a compaction, the worker sends messages without its IDs, or the screen shows it no longer knows its Task, treat it like a clear (step 3). Whether compaction keeps the preamble is UNVERIFIED and goes on the first-run checklist.
5. **v1 detection without a hook.** A cleared worker sends no more heartbeats (it has no preamble), so it falls into silence. The fixed 10-minute probe (INV-005) reads the screen. An empty conversation, or a fresh prompt with no history, is recorded as `suspected_cleared`. Because that classification is UNVERIFIED, it leads to an L5 report asking the person to confirm, never to settlement on its own. The person's confirmation is the evidence that clears INV-002's "which observation proves a person acted" question for this case.
6. **Recovery wording.** Every L5 restart plan and resume note says "stop, settle, new Task". The coordinator never suggests clear-and-continue in the same session. A FR-025's ban on the coordinator typing `/clear` stays.

**Bucket.** v1 now: the identity check, the WC-6 bullet and the recovery wording. v1 first-run verification: whether compaction keeps the preamble; what screen and transcript show after `/clear` (UNVERIFIED). v2: `SessionStart` with source `clear` or `compact` as a positive event (prior art, `seed-brief.md:89`; A S12), and an Orca-side session-identity field if one is added.

**WC rule.** Adds a WC-6 bullet (after `:73`). Adds the identity check to section 4 as the enforcement side of the Terms definition (`:11`). Keeps WC-5 (`:57`) and WC-7 (`:58`) intact, because a cleared session's messages never count as the worker's `worker_done`.

**Capabilities relied on.** Documented: `--task-id` / `--dispatch-id` on heartbeat (`seed-brief.md:65`), `exited` liveness as stall proof (`:71`), screen read (`:70`). UNVERIFIED: whether every message type carries and returns those IDs to the coordinator in the delivery (heartbeat documented; other types assumed), compaction's effect on the preamble, and the post-clear screen.

## 3. Responses to the other MEDIUM/LOW UNADDRESSED items

- **INV-001 (coordinator state lost on its own compaction or resume): accept fix.** v1 rule: every sweep starts by reading the liveness section of the run notes (pending acks, latches, `T_a` times, lineage counters), never from memory; no counter resets because the coordinator's context did.
- **INV-006 (S5 "no resume" exit cannot be observed): accept fix.** Delete that exit from `variant-2:74`; the WC-3 timeout heartbeat (INV-020, step 1) makes "resumed" visible, and S5 never relabels to S3 while `ask` is open.
- **INV-009 (worker-read may not return timestamps): accept fix.** First-run verification item; fallback: compare a tail digest across sweeps (coarser bound, stated as 20 minutes) and never derive proof from it; the INV-005 trigger does not depend on it.
- **INV-010 (caps compose without precedence): accept fix.** One rule: any cap that fires stops automation for the lineage; a failed start counts as a restart against the lineage cap; lineage counters are never reset by a new Task ID; only the person resets them.
- **INV-011 (lineage identity drifts as briefs change): accept fix.** Each brief carries `Lineage: <root Task ID>`, and the WC-6 three-failed-starts comparison (`WORKER-CONTRACT.md:71`) ignores the resume-note path as well as the report directory.
- **INV-016 (correlated fleet silence): accept fix.** v1 rule: if at least half the live workers (minimum 2) go quiet in one sweep, or Orca calls fail, send one infrastructure report, hold per-worker ladders at L1, and resume them only after a sweep where Orca calls succeed; a wall-clock jump of more than 2 × S between sweeps is handled the same way (covers INV-004).
- **INV-022 (declaration before a command's internal fan-out): accept partial fix.** The declaration is per command, sent by the worker session before it invokes a command whose `## Unattended mode` section names an expected maximum silence; commands still make no Orca calls (WC-8). It stays coarse by design, and the fixed 10-minute probe is the cover.
- **INV-024 (person-directed stop needs an amendment): accept fix.** Split as in INV-023 step 2: process ended is settled today by `exited` proof; PTY alive needs the WC-6 bullet.

## 4. Final per-point positions (still disputed after Round 2)

| Point | Final winner (A/B/C/merge) | Confidence % | One-line reason |
|---|---|---|---|
| X-003 / C-044 | C | 85 | Two unchanged reads cannot prove a completed final turn (a long tool call looks the same, INV-008); proof needs positive adapter evidence of the turn boundary, otherwise proof is none. B's Round 2 C-7 rewrite is withdrawn. |
| X-007 / C-003 | merge | 80 | A's latch with C's completed-unit predicate: it clears on a validated new completed unit or checkpoint after confirmation, a settled restart, or a person's recorded disposition; never on heartbeats, counter churn or mtime alone. |
| X-012 / C-019 | C | 60 | Both numbers are policy, not measured; in v1 automatic replacement happens only on Orca proof, so the stricter one per 60 minutes plus two per lineage costs little and fails safer. Revisit after replay data. |
| X-013 | merge | 85 | 15-minute v1 target for recorded state; C's 6-minute v2 profile optional and gated on measured end-to-end queue and probe budgets (C New Evidence 5). |
| C-005 | merge | 75 | A progress claim needs a corroborating signal (A), and the corroboration must be a completed unit, not traffic (C); this is also the INV-005 semantic-change list. |
| C-008 | merge | 85 | Due timer at S; sweep on any wake or timeout once due, at most once per S; v2 schedules due work independently so a flood cannot starve it. |
| C-011 | merge | 80 | Accept C's scope: the transcript is preferred when it is current and the harness provides it; the screen confirms prompt state; parsing stays behind the adapter; neither a quiet tail nor a quiet screen is proof. |
| C-018 | merge | 75 | Caps keyed by incident and lineage, inherited across new Task IDs; adopt C's two automatic nudges across the whole lineage as the initial ceiling (C New Evidence 3). |
| C-045 | C | 70 | Monotonic due times need a boot or clock-domain identity in v2; in v1 a wall-clock jump triggers the fleet rule (INV-016) and an immediate sweep, never a cascade of fired deadlines. |
| Declared window (B R2 New Evidence 1) | B | 85 | A declared window defers typed actions only; the fixed 10-minute probe keeps running. C accepted this in Round 2; it is now the INV-005 trigger. |

Points where B now accepts another variant's position: X-003 / C-044 (C), X-012 / C-019 (C), C-045 (C), C-011 (C's scope inside the merge), C-018 (C's lineage nudge ceiling inside the merge), C-005 (C's completed-unit predicate inside the merge).
