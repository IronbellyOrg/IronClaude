# Debate Round 2: Rebuttal for Variant B (variant-2-opus-analyzer)

## Responses to Criticisms

Inputs re-read this round: the three Round 1 files, A's Round 2 rebuttal, B's "§2.3 Precedence", "§4" (FR-008 to FR-010, the per-state table, NFR-004), "§6.1", "§7.3", "§8.2", "§10.2" (C-7) and "§10.3", `WORKER-CONTRACT.md:40-75` and `seed-brief.md:30-91`. Nothing runtime was observed.

### Raised by A

- **A-B1. "B creates its own stall proof" (§8.2 S6 interrupt, then "that is stall proof, so L4").** **CONCEDE** (Round 1 concession 2).
  - The S6 interrupt rung is deleted, and with it the induced turn end.
  - The C-7 sentence in "§10.2" ("did not resume after two nudges and one direct question has met Orca's stall proof") is rewritten: "An idle worker whose transcript's final agent turn, read twice at least one sweep apart, sent no `worker_done` has met Orca's stall proof; nudges and questions add nothing to that proof." "§10.3"'s claim that C-7 "names an existing Orca proof kind" is only true after that rewrite.
  - Authority: `seed-brief.md:71` (three proof sources), `WORKER-CONTRACT.md:73` ("after Orca's positive stall proof").
- **A-B2. "B's interrupt can land on a person-only prompt" (S6 above S4 in "§2.3").** **CONCEDE.** With the interrupt gone, the remaining harm is ordering: a nudge chosen for S6 or S9 could still be typed onto a permission dialog. Two fixes, both needed:
  - Order: S8, then S4, then S9, then S6 (A's person-first, B's finished-unreported above exhausted).
  - An independent input veto (C): any positive person-prompt or `ask`-owned-input fact blocks every typed action, whatever state is displayed.
- **A-B3. "AC-1 allows 20 minutes for case 1."** **CONCEDE.** AC-1 is restated: S6 is *recorded* within 15 minutes (the "§4.2" S6 row already says so). The second read 5 minutes later is a restart-eligibility step, and exhaustion no longer leads to automatic restart at all (C-022 below), so it is not part of the detection bound.
- **A-B4. "NFR-004 contradicts FR-009."** **PARTIAL.**
  - Rebut the literal claim: NFR-004 counts "fleet-wide Orca calls". The per-worker contract-path `stat` (FR-009) is a local filesystem call, not an Orca call, so the Orca-call count stays fixed.
  - Concede the purpose: NFR-004 justifies itself as keeping "an LLM coordinator's context cost per sweep near constant". The stat results and per-worker heartbeat-record updates scale with the fleet, so that sentence is false as written. Restate NFR-004 as "fixed Orca calls plus O(n) cheap local stats, with sweep output capped to workers whose state changed" (C-039).
  - See New Evidence 4: NFR-004 says "three" while FR-009 names two Orca calls; B is inconsistent with itself as well.
- **A-B5. "B can type a copy into a worker blocked in `ask`" (A3 covers S5 and S11).** **CONCEDE.** A3 types only when the worker is in S3 *and* the adapter positively identifies an empty input prompt with no tool running and no open `ask`. S5 and S11 go to the person (A5). R8's mitigation ("the ack plus message-ID idempotency makes the second copy a no-op") is withdrawn; see C-B5.
- **A-B6. "Host loss goes unreported for 30 minutes" (S7).** **CONCEDE.** Report `unverifiable` at 10 minutes continuous. Reporting is non-destructive, and S7 still never stops or retries (`WORKER-CONTRACT.md:72`).
- **A-B7. "Every wake triggers a sweep; FR-008 carries no limit."** **PARTIAL.**
  - Rebut the substance: "§6.1" states "Each wake still runs a sweep at most once every 5 minutes", and allows batch-processing heartbeats without a sweep. B never intended an unbounded sweep rate.
  - Concede the placement: an FR that an implementer reads alone must carry the limit. FR-008 becomes "a sweep runs on any wake or timeout once one is due, at most once per S" (A's C-008 merge).

### Raised by C

- **C-B1. "Interrupting is not a harmless nudge."** **CONCEDE.** Same as A-B1. Never `--interrupt` (A FR-025, C "Response Ladder"). C's narrowing is accepted: the ordinary S3 route is valid only on an independently read final-turn proof; failed nudges add nothing.
- **C-B2. "Person-only prompts lose the safety precedence" (context-exhausted and finished-unreported both above person-prompt).** **CONCEDE.** Same fix as A-B2. C is also right that S9 above S4 was unsafe for the same reason: S9's response is a typed nudge. The input veto makes the precedence question about display only.
- **C-B3. "Contract existence does not prove completion" (S9).** **PARTIAL.**
  - Rebut in part: B already scoped the signal. SG-10 says the contract does not show "that the worker session is done (a chain may have more `Command:` lines)" and is "Primary for S9 on the last `Command:` line". The S9 per-state row reads `worker_status` and checks "the brief has no later `Command:` line" before acting.
  - Rebut the blocked-contract half: under WC-5 (`WORKER-CONTRACT.md:57`) a `blocked` or `failed` contract is terminal too. It maps to `worker_done --outcome failed`. A blocked contract with no `worker_done` *is* finished-unreported, except on one path (next bullet).
  - Concede the definition: the S9 state row and "§2.3" ("work is done whatever the screen shows") are broader than the probe. Under `On a blocked gate: ask the coordinator`, the worker writes its blocked contract and *then* asks (`WORKER-CONTRACT.md:53`). C's blocked-contract-plus-pending-ask fixture is exactly that path and must stay S5. S9 is redefined: contract for the last `Command:` line, no open question for the Task, contract newer than any answer delivered to it, and no `worker_done`.
- **C-B4. "Bounds and acceptance disagree" (AC-1 20 min; adaptive W can exceed 10).** **PARTIAL.**
  - AC-1: CONCEDE (A-B3).
  - Adaptive W: CONCEDE the fact. FR-010 lets W grow to 45 minutes, and the S3 row's "15 min (W 10 + one sweep 5)" holds only when W = 10. B published a bound that its own window can break.
  - Rebut the remedy implied, which is dropping adaptation: a fixed W reintroduces the dependency on a preamble-owned cadence (`WORKER-CONTRACT.md:7`, `:49`) that A itself now concedes (A's Round 2, B-A6).
  - Resolution: split the trigger from the label. The *probe* trigger (one transcript tail, T2) fires at a fixed 10 minutes of no token change. The adaptive W only decides whether silence is *shown* as suspicious and whether the coordinator escalates past L1. The detection bound is then 15 minutes for every cadence, and adaptation still prevents false nudges. Classification and restart eligibility are labelled separately, as C asks.
- **C-B5. "Typing into ask is not repaired by dedup" (A3 includes S5; R8).** **CONCEDE.** Same as A-B5. Dedup works only after the intended model parses the text. It cannot stop the `ask` process in the foreground from receiving keystrokes.
- **C-B6. "Activity may silence observation too long" (proposed WC-10 wording: no probe before a declared window ends, up to 45 minutes).** **PARTIAL.**
  - Rebut for person prompts and exit: FR-009 runs `worker-list` and the prompt-wait listing for the whole fleet every sweep, and the S4 row says "Polled for *every* worker, every sweep. Not tied to silence". A declared window never hides S4, S7 or S8.
  - Concede for thrashing, more strongly than C put it (New Evidence 1): FR-010 replaces W with `expect_silence_min`, so the S6 frozen-token trigger is suppressed for the whole window. A case-1 thrash inside a declared 45-minute window is found at about 50 minutes.
  - Fix: the WC-10 wording says "is not *nudged* before that window ends". Cheap observation continues, and the 10-minute fixed probe trigger (C-B4 resolution) still runs one transcript tail per 10 minutes for a worker in a declared window. Only typed actions wait for the window.

Tally: 13 criticisms. 8 CONCEDE (A-B1, A-B2, A-B3, A-B5, A-B6, C-B1, C-B2, C-B5), 5 PARTIAL (A-B4, A-B7, C-B3, C-B4, C-B6), 0 REBUT in full.

## Response to A's Round 2

**Changes my view:**

1. **A's B-A7 rebuttal (case 5).** A is right. A's "§5 Mapping" row 5 says "(cause not established)", and A's open question repeats `seed-brief.md:79`. My Round 1 critique A7 ("ranked 'probable' on one hypothesis") overstated A. I withdraw it. I also accept A's and C's use of H1-H4: an ordered investigation checklist for the first v1 run, not a basis for choosing a fix. The ack bound is cause-independent. (X-017, C-031 move to merge.)
2. **A's New Evidence 1 (no person-directed stop path in WC-6).** Confirmed by re-reading `WORKER-CONTRACT.md:72-73`: settlement is defined only "after Orca's positive stall proof". This hits B directly. B's S6 row ends at "L5: ask the person for a go to stop it (v1)", and B's C-9 offers the person the option to approve exhaustion "as an IronClaude-only proof". The person can stop their own worker, but the person cannot turn that into Orca's proof. I drop C-9 and open question Q8, and adopt A's proposed sentence for section 4 ("A stop the person directs in their own session is the person's action; the coordinator records it and then settles the old Task before creating the new one"). (X-004, C-022 move to C.)
3. **A's New Evidence 2 (L2 cap resets per Task).** It also breaks my Round 1 pick of A on C-018, which rested on "caps per state episode and per Task are clearer". WC-6 makes every retry a new Task (`:69`), so a per-Task cap resets in exactly the case-8 loop. Caps are keyed by incident and by lineage (C). (C-018 moves to C.)
4. **A's New Evidence 3 (`check --wait` gap, `:61`).** Accepted, and it has a second consequence for B beyond ack deadlines: `check --wait` periods produce heartbeat gaps that feed B's median. See item 5.
5. **A's New Evidence 4 (gap filter for adaptive W).** Accepted. The median is computed only over intervals outside declared `expect_silence_min` windows, known fan-out periods and `ask` / `check --wait` blocks. Before any interval exists, the startup grace (B's S0 row, A's G) applies. Combined with the C-B4 trigger/label split, adaptive W no longer affects any published bound.
6. **A's latch for context exhaustion (X-007, C-003).** A's clearing condition (a changed `step_seq` plus a new handoff or contract artifact dated after confirmation, or a restart, or a person action) is the falsifier I wrote for C in Round 1 (C5: "changed `progress_rev` plus a checkpoint sha change"). B's token already counts only on-disk progress (WC-15 wording in "§10.2"). I accept the latch.
7. **A's C-008 merge (due timer, sweep on any wake once due, at most once per S).** Accepted; it resolves A-B7. In v1 the 5-minute wait timeout is the timer; under a message flood, "on any wake once due" keeps sweeps running.

**Does not change my view:**

- **A's Agreement Summary lists X-008 and C-014 as agreed with A's or C's label.** In substance yes: status carrier. I keep B's specific point that the ack's body line is authoritative and the payload optional, because payload transport is UNVERIFIED (A-007). A and C both accepted this in Round 1 (A's A-007 row, C's C-043 row), so this is agreement, not dispute.
- **A's B-A6 PARTIAL (W is the wait timeout, not a cadence window).** Fair for A's W. It does not change my critique of Q, which A conceded.
- **A's proposed exit from S6 via "incidental writes never clear it".** Agreed, and it strengthens C-B6's fix: a write during a declared window cannot clear or hide an S6 incident either.

## Updated Assessment

Round 1 arguments from A and C changed B's position in these places:

1. **Recovery authority (A's B1, C's C-022).** B has no path from context exhaustion to automatic or person-blessed L4. Exhaustion latches, then goes to L5 with a ready restart plan and resume note. The person stops the worker as their own action (A's New Evidence 1). Only Orca's three proof sources settle an attempt.
2. **Input safety is a veto, not only a rank (C's C-002, X-010).** B keeps a display precedence (S8, S4, S9, S6, S5, S3, S2, S1), and adds C's independent rule: no typed text while a person prompt or `ask` owns input, or while the prompt binding is ambiguous. Typing goes only to a positively identified empty prompt until busy-input queueing is observed (A-018 stays REJECT).
3. **Durability belongs in the design, not the risk table (C's S-008, C-037).** B adopts C's persist-before-ack (NFR-005), `attempt_epoch` fencing (FR-005), `reconcile()`, `uncertain_effects` and controller lock for v2. For v1, B's FR-012 (whole batch before `--ack`) stays, with C's caveat that it is not crash-safe by itself.
4. **Rules live in two homes, not one (C's X-018, C-023).** B's Round 1 strength 10 claimed one home. C showed that a command's own stage checkpoints are files it writes with no Orca call, so WC-8 (`:38`) and WC-7 (`:58`) are untouched. Chain continuity and lifecycle stay in contract section 3; command-internal checkpoints may live in commands.
5. **Bounds are phase-labelled and split (C's C-009, X-014).** Every bound states v1 or v2, and initial classification is separate from restart eligibility. B's 15-minute v1 figures stand; C's 6-minute and 1-minute figures are v2 targets with a probe and queue budget.
6. **Case-5 ranking (A's B-A7 rebuttal, C's X-017).** H1-H4 are an investigation order, not a design input.
7. **What B keeps after Round 1:** the occurrence/detection split (S-006, unanimous), the arrival-versus-change matrix (A-016, unanimous), the all-nine-types wake with whole-batch handling (X-001, unanimous), the status-body ack with `queued` (X-008, X-009, C-041), the WC-11-scoped contract `stat` (C-013, unanimous), separate `unreachable` and `exited` states (S-010, unanimous), the handoff file on failure (C-024), and the `/sc:implement` freeze priority in the resume note (C-021, C-046).

## New Evidence

1. **B's declared window suppresses B's own thrash trigger (self-found defect).**
   - FR-010: W is "the worker's declared `expect_silence_min` when one is active, capped at 45 minutes".
   - The S6 trigger ("§4.2") is "Heartbeats *arrive* but the token is unchanged for W". During a declared window that W is up to 45 minutes.
   - So a worker that declares a long step and then thrashes, the case-1 pattern (`seed-brief.md:17`), is first probed after 45 minutes and recorded at about 50. That breaks the 15-minute thrashing target (`seed-brief.md:42`). No Round 1 file named this mechanism; C's C-B6 critique is the nearest.
   - Fix: as in C-B4 and C-B6 above. The declared window defers typed actions only; the fixed 10-minute probe trigger keeps running. The S4 prompt listing already runs regardless.
2. **WC-5 makes blocked and failed contracts terminal; WC-3's ask path is the only exception.**
   - `WORKER-CONTRACT.md:57`: `--outcome failed` when `worker_status` is `failed` or `blocked`, or no contract exists.
   - `:53`: under `ask the coordinator`, the worker lets the command write its blocked contract, then asks, then re-invokes with the same report directory, and "the second run's contract replaces the blocked one whole".
   - So a contract on disk is a correct S9 signal in every case except the window between a blocked contract and the re-run's contract. The S9 redefinition in C-B3 (no open question, contract newer than any answer) closes exactly that window. This narrows C's critique rather than rejecting it.
3. **A second Round 1 asymmetry in B's C-7 text.** "§10.3" defends C-7 because it "names an *existing* Orca proof kind". That defence holds only for the transcript clause. The "after two nudges and one direct question" clause made the coordinator's own actions a precondition, which reads as part of the proof. The rewrite in A-B1 removes that reading. Neither A nor C quoted "§10.3".
4. **NFR-004 says "three" fleet-wide Orca calls; FR-009 names two** (`worker-list` and `worktree ps --agent-wait`). The third may be the `check --wait` itself, but B does not say so. UNVERIFIED which call was meant; NFR-004 should list them by name.
5. **`seed-brief.md:71` lists "Nudge and ask are not forbidden" in the same paragraph as the three proof sources.** It permits the actions. It does not make them evidence. This is the textual basis for the rewritten C-7 sentence and for dropping C-9: what is permitted on silence (probe, nudge, ask) and what counts as proof (three Orca sources) are separate lists.

## Revised Per-Point Positions

Only points where B's Round 1 pick changes.

| Point | Round 1 pick | Round 2 pick | Confidence 0-1 | Reason |
|---|---|---|---|---|
| X-004 | B | C | 0.8 | Drop C-9. The person cannot turn exhaustion into Orca's proof; WC-6 settles only on Orca's proof (`:73`). The person's own stop is the path (A New Evidence 1). |
| X-007 | B | merge | 0.75 | A's latch: clears only on a changed `step_seq` plus a new artifact dated after confirmation, a restart, or a person action. Heartbeats and incidental writes never clear it. |
| X-014 | A | merge | 0.8 | 15 minutes to a recorded S6; restart eligibility labelled separately (C). |
| X-015 | A | merge | 0.7 | A's tiers plus C's capacity test. NFR-004 restated as fixed Orca calls plus O(n) local stats, output capped to changed workers. |
| X-017 | B | merge | 0.75 | Cause UNVERIFIED (C); H1-H4 become an investigation order for the first v1 run; the ack bound is cause-independent (A). |
| X-018 | B | merge | 0.75 | Chain continuity in contract section 3; command-internal stage checkpoints in commands with no Orca call (C). |
| C-003 | B | merge | 0.75 | Same latch as X-007. |
| C-005 | A | merge | 0.65 | Payload is a claim needing a non-contradicting signal (A); B's WC-15 count already rises only with on-disk progress, which is C's semantic revision. |
| C-008 | B | merge | 0.75 | Due timer at S; sweep on any wake or timeout once due; at most once per S. Limit written into FR-008. |
| C-011 | B | merge | 0.65 | Transcript primary, screen confirming (B); frame parsing behind the adapter and ambiguous input prohibits typing (C). |
| C-014 | B | merge | 0.7 | Status-body carrier (A/B) with C's immutable identity, digest and disposition. |
| C-017 | A | merge | 0.8 | A's L0-L5 without interrupt; L4 only on Orca proof; C's reconcile, stop-confirm and settle before create. |
| C-018 | A | C | 0.75 | Per-Task caps reset on every WC-6 replacement; key caps by incident and lineage. |
| C-022 | B | C | 0.8 | Same as X-004. Context exhaustion is never a stall proof written by IronClaude, in v1 or v2. |
| C-023 | B | merge | 0.7 | Same split as X-018. |
| C-031 | B | merge | 0.75 | Same as X-017. |
| C-033 | A | merge | 0.8 | Cases 1 and 8: latch, then L5 with a ready restart plan; the person stops; never L4 on exhaustion; same-cause rule blocks a like-for-like repeat. |
| C-041 | B | merge | 0.7 | Status ack plus `queued`; deadlines bound read_unknown handling only; re-derive state (including `check --wait`) before escalating. |
| C-043 | B | merge | 0.65 | Body-line authority (B) plus C's payload conformance gate in the first v1 run. |

Position changes: 19.

## Agreement Summary

**All three agree in substance** (labels may differ; B's Round 2 moves included):

- X-001, X-002, X-003, X-004, X-005, X-006, X-007, X-008, X-009, X-010, X-011, X-014, X-015, X-016, X-017, X-018, X-019, X-020, X-021
- C-001, C-002, C-003, C-004, C-006, C-007, C-009, C-010, C-012, C-013, C-014, C-015, C-016, C-017, C-018, C-020, C-021, C-022, C-023, C-024, C-025, C-026, C-027, C-028, C-029, C-030, C-031, C-032, C-033, C-034, C-035, C-036, C-037, C-038, C-039, C-040, C-041, C-042, C-043, C-044, C-045, C-046, C-047
- S-005, S-006, S-007, S-008, S-010

**Still disputed (small gaps):**

- **X-012 / C-019. Restart numbers.** All agree on a per-lineage cap. C wants one per 60 minutes and two per lineage; A and B proposed two per 6 hours plus two per lineage. The values are policy, not measured (all three say so).
- **X-013. Idle latency.** All agree on 15 minutes in v1. Open: whether C's 6-minute v2 target is worth its 1-minute sample and drain cost (C-039, A-002).
- **C-005.** A held A's claim-plus-corroboration rule; B and C now say merge. A called the gap small.
- **C-008.** A and B: merge (due timer, any wake, at most once per S). C: independent timer. Likely agreed once C confirms the merge keeps its flood guarantee.
- **C-011.** Whether the transcript is named primary. A and B: yes. C states only that parsing lives behind the adapter.
- **Declared-window behaviour (B New Evidence 1, no ID).** B now proposes that declared windows defer typed actions only, with a fixed 10-minute probe trigger. A and C have not answered this.
