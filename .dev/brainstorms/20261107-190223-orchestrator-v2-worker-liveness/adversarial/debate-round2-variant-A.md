# Debate Round 2: Rebuttal for Variant A (variant-1-opus-architect)

## Responses to Criticisms

Inputs for this round: the three Round 1 files, A's sections 4, 5, 8 and 10, `WORKER-CONTRACT.md:40-75` and `seed-brief.md:60-90`. All were re-read this round. Nothing runtime was observed.

### Raised by B

- **B-A1. "The wake set excludes `heartbeat` (X-001)."** **CONCEDE.** I already conceded this in Round 1 (concession 1). A's wording in "§10 WC rules amended" ("all nine types except `heartbeat`") changes to all nine. A's "at most once per S" sweep limit ("§4 The sweep") stays, so a heartbeat wake costs one batch read, not one sweep.
- **B-A2. "The v2 WC-6 amendment redefines an Orca proof (X-004, C-022)."** **CONCEDE.** Withdraw the last bullet of "§10 WC rules amended". `seed-brief.md:71` lists exactly three proof sources. WC-6 settles only "after Orca's positive stall proof" (`WORKER-CONTRACT.md:73`). An exhaustion verdict ends at L5 in v2 as well, unless Orca adopts the proof class.
- **B-A3. "A terminal copy is typed into a worker blocked in `ask` (X-010)."** **CONCEDE.** "§8 State-to-ladder map" row blocked-in-ask ("ack clock -> L2 terminal copy") gets C's FR-017 guard: no typing while `ask` owns input. Report instead.
- **B-A4. "'The nudge is harmless to a working session' is asserted, not shown."** **PARTIAL.**
  - Concede the heading. "§8 Nudge text" says "harmless", but its own next paragraph marks mid-turn queueing UNVERIFIED. The heading should read "designed to be harmless; queueing UNVERIFIED".
  - Rebut the implication that A counts a lost nudge as delivered. L2 uses "the submit-confirming send" ("§8 Rungs"). Case 2's response names the `--wait-submit` receipt ("§5"). `seed-brief.md:67` says that is the only verb with a turn-start receipt. So A has the same lost-nudge rule as B's FR-020.
  - Until queueing is observed, nudges go only to a positively identified prompt (C), as I stated in Round 1 under A-018.
- **B-A5. "No worktree activity in v1."** **CONCEDE.** Already conceded under C-013. B's v1 `stat` of the worker's own contract path goes in at T1 for suspicious workers only, so NFR-004 stays true (see X-015).
- **B-A6. "A fixed Q = 10 and W = 5 against a preamble-owned cadence (`:7`)."** **PARTIAL.**
  - Rebut for W. In "§4 Timing parameters", W is the wait timeout. It bounds wake delay and does not depend on heartbeat cadence.
  - Rebut "fire on schedule". A false flat-progress trigger at Q only schedules a T2 probe (FR-012: absence "shall only ever schedule a T2 probe"). It never acts.
  - Concede for Q. Q's own "Why" cell and Open question 2 ("Q = 10 min assumes [the cadence] is under 6 minutes") show A knew Q depends on cadence and left the dependency as a stated assumption rather than designing it out. Adopt B's form: Q = max(10 min, 2 × median observed interval), with the guard in New Evidence item 4.
- **B-A7. "Case-5 cause ranked 'probable' on one hypothesis."** **REBUT.**
  - A's "§5 Mapping" row 5 says "(cause not established)".
  - Open question 5 calls the pull model "a probable mechanism ... but not established". That repeats the brief's own words: "a probable mechanism for case 5 (UNVERIFIED as the cause)" (`seed-brief.md:79`).
  - A ranks nothing. Its response, the ack bound, does not depend on the cause. I accept B's H1-H4 as an investigation list, not as a design input.

### Raised by C

- **C-A1. "Wake completeness is weakened rather than met."** **CONCEDE.** Same as B-A1.
- **C-A2. "The v2 proof amendment crosses the authority boundary ... A's v1 person-go path must likewise be an explicit person-directed exception, not represented as ordinary WC-6 compliance."** **CONCEDE, both parts.**
  - The amendment is withdrawn (B-A2).
  - On the v1 path: "§8 Rungs" L4 lists "confirmed `context-exhausted` (v1: only with the person's go)" as an alternative to Orca's stall proof. It also cites `WORKER-CONTRACT.md:69-73` as its authority. That citation is wrong for this branch. WC-6's settlement sentence (`:73`) covers only a stop "after Orca's positive stall proof". The contract has no person-directed stop path (New Evidence 1).
  - Fix: L4 keeps only the Orca-proof branch. Context exhaustion goes to L5 with a ready restart plan. The stop is the person's own decision, recorded as such, and is never presented as WC-6 compliance.
- **C-A3. "Ack timeout does not establish safe input ownership."** **CONCEDE.** Same as B-A3. A's R2 idle-probe mitigation becomes a mandatory precondition of every L2 copy, not a risk note.
- **C-A4. "Incidental writes can hide context exhaustion."** **CONCEDE.**
  - In "§4 Per-state rules", the context-exhausted confirm ends with "and S3 shows no writes since the step began". A partial write or a shared writer (WC-11, `:45`) therefore vetoes explicit thrash evidence.
  - Drop that conjunct. Explicit compaction-failure evidence from screen or transcript, together with a flat S2, confirms the state on its own.
  - S3 activity may lower confidence in the report text, but it never clears the state.
- **C-A5. "New report directories do not make replay idempotent (R13)."** **CONCEDE.**
  - A fresh directory (WC-6, `:69`) isolates output files. It does nothing for source edits made before a crash.
  - Add C's `uncertain_effects` line to A's "§8 Resume-note format".
  - Any uncertain effect blocks automatic replay and goes to L5.

Tally: 11 criticisms. 8 CONCEDE, 2 PARTIAL (B-A4, B-A6), 1 REBUT (B-A7).

## Updated Assessment

Round 1 changed A's position in six places:

1. **Recovery authority (C).** I now hold that A has no automatic or semi-automatic path to replace a context-exhausted worker. This holds in v1 and v2, with or without the person's go wrapped as L4. C's "Response Ladder" stance (FR-019) is the correct backbone. A keeps its contribution: the person receives a ready restart plan at L5.
2. **Input safety is a gate, not a precedence (C).** C's Round 1 C-002 argued that a person or `ask`-owned prompt must veto typing whatever state is displayed. A's person-first order fixes the selector, but an independent veto is still needed when states coexist. Both stay: A's order for display and action selection, and C's veto for actuation.
3. **Caps must survive new Task IDs (C, C-018).** Re-reading "§8 Rungs" shows L2 capped "4 per Task". WC-6 makes every retry a new Task (`:69`), so that cap resets on each replacement. C's per-incident and per-lineage caps are right. A's own "work unit" (`replaces T<n>` chain) is the natural key for them.
4. **Exit from context-exhausted (B and C both moved me toward a latch).**
   - In Round 1 I held "no self-exit". C's Round 1 X-007 reason refines that: genuinely resumed work can occur.
   - B's own falsifier for its C5 critique gives the condition: a new checkpoint revision written after the thrash.
   - Resolution: the incident latches. It clears only on a changed `step_seq` plus a new handoff or contract artifact dated after the confirmation, or on a restart or a person action. Heartbeats, `actions_since_last` and incidental writes never clear it.
5. **Command-internal checkpoints (C, X-018).** I keep chain continuity in contract section 3. I accept C's narrower point that a command's own stage checkpoints are files the command writes, with no Orca call. They violate neither WC-8 (`:38`) nor WC-7 (`:58`). This is a merge, not a reversal.
6. **v1/v2 labelling (B and C on C-028, C-009, C-041).** A's one-sentence v1/v2 test stays. B and C convinced me that every bound, ack deadline and cost claim needs a v1 or v2 label. A deadline should be read as escalation eligibility, not as a promise that the worker can acknowledge in time (A-004).

Unchanged after Round 1: A's three axes plus `proof_class` (C-001; C and B both credit it); person-first precedence (X-005, unanimous); cost tiers (C-007, unanimous); status as the ack carrier (X-008, C-014, unanimous in substance); never interrupt (X-002, unanimous in substance).

## New Evidence

1. **WC-6 has no settlement path for a stop without Orca proof.**
   - `WORKER-CONTRACT.md:72` says "No retry while the earlier attempt is not settled or reads `unverifiable`: absence never authorizes a retry."
   - `:73` allows the coordinator to settle a stalled attempt "after Orca's positive stall proof".
   - The contract states no path for a person-directed stop of a live but thrashing worker. The person-go branch in every variant (A's L4, B's C-9, and C's L5 hand-off) therefore needs an explicit contract sentence in a v1 amendment, or the person must stop and settle the worker themselves. No variant proposed that sentence. Proposed text for the section 4 coordinator rules: "A stop the person directs in their own session is the person's action; the coordinator records it and then settles the old Task before creating the new one."
2. **A's L2 cap resets on replacement.** "§8 Rungs", L2, says "2 per state episode; 4 per Task". Read with WC-6 (`:69`, every retry is a new Task), a case-8 loop gets a fresh nudge budget on every replacement. This supports C-018 for C and is a defect in A that no Round 1 file named.
3. **Heartbeats also stop during `check --wait`.**
   - `WORKER-CONTRACT.md:61` says the worker sends none "while blocked in `ask` or `check --wait`".
   - Round 1 cited only the `ask` half against C's heartbeat ack (C-014). The `check --wait` half matters for any carrier, because `status` cannot be sent from inside a blocking `check --wait` either.
   - So every variant's ack deadline needs the same "re-derive state before escalating" step (A-004). A worker in `check --wait` is pulling, not ignoring.
   - Whether workers ever use `check --wait` today is UNVERIFIED.
4. **B's adaptive window needs a gap filter (UNVERIFIED reasoning, not tested).**
   - FR-010's W = max(10 min, 2 × median interval) uses observed intervals.
   - WC-10 accepts fan-out gaps longer than the cadence (`:44`). If those gaps enter the median, the window grows, and silence detection slows for the rest of the run.
   - Compute the median only over intervals outside declared `expect_until` and fan-out periods (A's F parameter).
   - Before any interval exists, A's startup grace G applies.
5. **External prior art agrees with three concessions** (`seed-brief.md:85-90`, research-light, not re-fetched):
   - SWE-agent treats context exhaustion as an exit status and saves the patch first. That supports a handoff before any person-approved restart (C-024).
   - The Claude Code `Stop` hook fires once per turn, and exit 2 keeps the session working. A Stop hook that refuses a turn end can therefore loop, which supports X-019 and C-030 (no compulsory Stop hook).
   - OpenHands found that early thresholds gave false positives. That supports latching on two sources rather than one count (C-012).

## Revised Per-Point Positions

Only the points where A's Round 1 pick changes, plus two disputed points where I propose a resolution without changing my pick (marked "no change").

| Point | Round 1 pick | Round 2 pick | Confidence 0-1 | Reason |
|---|---|---|---|---|
| X-006 | B | merge | 0.7 | Finished-unreported stays above context-exhausted (B). C's objection holds, though: contract existence alone is not completion. S9 needs a final `worker_status` and no remaining `Command:` line, so a blocked contract with a pending ask stays blocked. C's input veto applies. |
| X-007 | A | merge | 0.75 | Latch the incident. It clears only on a changed `step_seq` plus a new handoff or contract artifact dated after confirmation, or on a restart or a person action. Heartbeats and incidental writes never clear it (Updated Assessment 4). |
| X-009 | A | merge | 0.75 | C's 2/5/10 become escalation deadlines (read_unknown), not proof of a missed read. B's `queued` disposition gives a busy worker an honest ack. The `check --wait` gap applies too (New Evidence 3). |
| X-011 | merge | C | 0.75 | Same substance as Round 1. Typing goes only to a positively identified prompt until queueing is observed. A's template text keeps its reply id. |
| X-017 | merge | merge (no change) | 0.65 | Resolution: the cause stays UNVERIFIED in the design (C). B's H1-H4 become an ordered investigation checklist for the first v1 run, not a basis for choosing a fix. The ack bound is cause-independent (A). |
| X-018 | A | merge | 0.7 | Chain continuity stays in contract section 3 (A, B). Command-internal stage checkpoints are command-written files with no Orca call (C). |
| C-003 | A | merge | 0.75 | Same latch as X-007. |
| C-004 | A | merge | 0.65 | A's `ironclaude.progress/1` field set, with B's phase-text fallback in v1, so a mangled payload does not break progress tracking (A-007), and C's epoch and sequence fields in v2. |
| C-008 | A | merge | 0.7 | An independent due timer at S runs the sweep even under a message flood (C). A sweep may run on any wake or timeout once it is due (B). It runs at most once per S (A). |
| C-009 | A | merge | 0.7 | v1 commitments of 15 min or less (A/B). C's tighter figures are v2 targets, each labelled with its queue and probe budget. |
| C-011 | B | merge | 0.6 | Transcript primary, screen confirming (B). Frame parsing stays behind the adapter, and ambiguous input prohibits typing (C). |
| C-017 | A | merge | 0.8 | A's L0-L5 with no interrupt. L4 keeps only the Orca-proof branch (C-A2 concession). C's reconcile, stop-confirm and settle steps run before create. |
| C-018 | A | C | 0.75 | A's "4 per Task" resets on every WC-6 replacement (New Evidence 2). Caps must be keyed by incident and work unit (lineage). |
| C-021 | A | merge | 0.75 | A's text note in the new brief (v1), B's `/sc:implement` D2 priority and C's `uncertain_effects` blocker (C-A5 concession). |
| C-026 | A | B | 0.55 | Two separate rules (chain continuity; reads and handoffs) are easier to cite. B and C both prefer this. |
| C-028 | A | merge | 0.7 | Keep A's v1/v2 test and delivery table. Label every bound and cost claim by phase (B, C). |
| C-033 | A | merge | 0.75 | Cases 1 and 8: latch, then L5 with a ready restart plan. Never L4 on exhaustion (C). A's same-cause rule blocks a like-for-like repeat. |
| C-034 | A | merge | 0.7 | B's short non-restarting text with A's reply id, sent only at an identified prompt with C's action dedup. |
| C-035 | A | merge | 0.6 | Surface unknown types verbatim with a registry row (A). C's raw-input bounds and poison-message tolerance. |
| C-039 | A | merge | 0.6 | A's tiered calls bound each sweep, not the cumulative context. Cap sweep output to changed workers and measure a multi-hour budget (B, C). |
| C-040 | A | merge | 0.55 | Empty waits are not free. Measure them in the replay fixtures (all three now say UNVERIFIED). |
| C-041 | A | merge | 0.65 | Status-carried ack opportunity (A/B) plus `queued` (B). Deadlines bound read_unknown handling only, and state is re-derived before escalating (C). |

Position changes: 21 (X-017 is listed with no change).

## Agreement Summary

**All three agree in substance** after reading the three Round 1 files. Variant labels differ on some of these, but the design content is the same:

- X-001, X-002, X-003, X-004, X-005, X-008, X-010, X-011, X-012, X-013, X-014, X-015, X-016, X-019, X-020, X-021
- C-001, C-002, C-006, C-007, C-010, C-012, C-013, C-014, C-015, C-016, C-019, C-020, C-022, C-023, C-024, C-025, C-027, C-029, C-030, C-032, C-036, C-037, C-038, C-042, C-043, C-044, C-045, C-046, C-047
- S-005, S-006, S-007, S-008, S-010

**Likely agreed after A's Round 2 moves**, pending confirmation from B and C. A moved to the merge or variant that B and C already share or that combines both:

- X-006, X-009, X-018
- C-004, C-009, C-017, C-021, C-026, C-028, C-033, C-034, C-035, C-039, C-040, C-041

**Still disputed:**

- **X-007 / C-003.** Exit from context-exhausted. B: no self-exit. C: verified resumed work may clear the incident. A: latch with a stated clearing condition.
- **X-017 / C-031.** Ranking of the case-5 cause. B ranks H1-H4. C leaves it unranked. A: the cause is UNVERIFIED and the H-list is an investigation order.
- **C-008.** Sweep trigger: B's every wake, C's independent due timer, A's at most once per S.
- **C-011.** Whether the screen or the transcript is primary, and where parsing lives.
- **C-018.** Cap keying. B picked A's per-Task caps in Round 1. A now concedes to C because of the reset defect.
- **C-005.** C wants a semantic revision on top of A's claim-plus-corroboration rule. A and B hold A. The gap is small.
