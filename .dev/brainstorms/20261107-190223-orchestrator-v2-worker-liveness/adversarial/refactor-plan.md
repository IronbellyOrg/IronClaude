# Refactoring Plan: Merge into Base (Variant B)

## Overview

- **Base variant:** B (`variant-2-opus-analyzer.md`), combined score 0.935 (see `base-selection.md`).
- **Incorporated from:** A (`variant-1-opus-architect.md`) and C (`variant-3-haiku-backend.md`), plus the debate's merge guidance (`debate-transcript.md:506-519`).
- **Planned changes:** 16.
- **Changes not being made:** 18.
- **Overall risk:** Medium. Fourteen changes are structural or additive at low or medium risk. Two changes, 7 (INV-020) and 8 (INV-023), carry the HIGH invariants and are rated High.
- **Debate status carried in:** NOT_CONVERGED only because INV-020 was unaddressed. Change 7 decides it and labels the decision "decided by merge, flagged for review". C-019/X-012 (the restart window) is decided in Change 10 and labelled as unmeasured policy.

Coverage requirements that the merged output must meet, and the change that delivers each:

| Requirement | Change |
|---|---|
| v1/v2 split stated for every change | 2 (every bound), and a "Phase" line in every change below |
| Each amended WC rule named by number | 12 |
| 8 cases mapped to named states with bounds | 4 |
| All 9 message types plus unknown types | 6 |
| Read acknowledgement | 7 |
| Ladder (probe, nudge, ask, restart with resume note, report) with caps | 10, 11 |
| Harness-neutral core with Claude Code and Orca as adapters | 13 |
| INV-005 resolution | 5 |
| INV-020 decision | 7 |
| INV-023 resolution | 8 |
| Restart window (C-019/X-012) | 10 |

The merge executor edits B's text in place. It keeps B's section numbering 1-13, adds subsections where a change says "insert", and tags each incorporated passage with its source (for example `[from A section 2]`).

## Planned Changes

### Change 1: Three evidence axes, `proof_class` and cost tiers (from Variant A)

- **Source:** Variant A, section 2 (Process, Interaction and Progress axes; FR-004 precedence) and section 3 (observation record `ironclaude.liveness/1` with `proof_class`; cost tiers T0, T1, T2).
- **Target:** Base section 2 (restructure) and section 3 (insert a new 3.3 "Observation record and cost tiers").
- **Rationale:** Merge guidance item 1 names A's axes, `proof_class` and cost tiers as backbone. U-001 and U-003 are endorsed by all three advocates; U-002 is partially adopted (B accepted `proof_class` in its Round 1 concession); C-007 settles the tiers.
- **Integration approach:** Keep B's state IDs S0-S11 and names as the named states. Add a column mapping each state to its value on each of the three axes, and replace B's section 2.3 precedence with A's FR-004 list, keeping B's wording where the two agree. Every signal in B's SG-1..SG-10 list gets a `proof_class` (positive proof, corroborating, or hint) and a tier (T0 fleet-wide, T1 per-worker cheap, T2 costly probe on trigger). B's FR-009 "costly probes only for triggered workers" becomes the T2 rule.
- **Phase:** v1 (record kept in coordinator run notes); the JSON record is v2.
- **Risk:** Medium. Restructuring section 2 can break B's cross-references from sections 4, 5 and 8, so the executor re-checks every "S<n>" reference.

### Change 2: Timing-parameter table and v1/v2 phase labels on every bound (from Variant A, Variant C)

- **Source:** Variant A section 4 parameter table (W 5, S 5, Q 10, G 10, A, D 60, F 30) and NFR-003 (one named parameter block); Variant C detection table (6-minute and 1-minute figures) and NFR-011 (staged rollout).
- **Target:** Base section 4.1 (insert a parameter table after FR-010) and section 4.2 (add a "Phase" column).
- **Rationale:** U-007 and S-011 (timing table) are endorsed by all three advocates. Merge guidance item 7: every bound, ack deadline and cost claim carries v1 or v2; v1 commits to 15 minutes; C's 6-minute and 1-minute figures are v2 profiles gated on a capacity test.
- **Integration approach:** One table lists each parameter with its v1 value, its v2 profile value and the gate for the v2 value. v1 values: sweep 5 min (wait `--timeout-ms 300000`), W minimum 10 min, inactivity 5 min, declared-window cap 45 min, read-only probe 10 min, record-or-report 15 min. v2 profile values from C: idle 6 min, mailbox drain 1 min, targeted probe 30 s, person-prompt 6 min. They apply only after C's capacity test 12 (six workers and the supported fleet limit, sweep at most 5 min) passes. NFR-003's rule is added: the parameters are overridable per Task by the brief, never by the worker. B's NFR-005 note (starting values, tuned from logs) stays.
- **Phase:** Both, labelled per row.
- **Risk:** Low.

### Change 3: Per-state bound corrections and contradiction fixes (from debate)

- **Source:** X-014 and X-015 resolutions; merge decision "unreachable reported by 10 min"; Variant C NFR-004 (monotonic time).
- **Target:** Base section 4.2 table (rows S3, S6 and S7), NFR-004 and section 13 AC-1.
- **Rationale:** These fix the internal contradictions that cost B on IC (`base-selection.md`): X-014 (AC-1 says 20 minutes, section 4.2 says 15) and X-015 (NFR-004 "three calls" against FR-009 "one `stat` per worker"). U-026 and C-045 (monotonic time) are endorsed by all three advocates.
- **Integration approach:** (a) AC-1's bound becomes 15 minutes in v1. (b) NFR-004 is reworded: three fleet-wide Orca calls per sweep, plus one local `stat` per worker contract path, scoped to that worker's own report directory (WC-11 single owner), plus at most two T2 probes per triggered worker. (c) S7 `unreachable`: L5 report to the person by 10 minutes of continuous `unverifiable` (two v1 sweeps), replacing B's 30 minutes; still never L4 or stop. (d) All bounds are measured on a monotonic clock. A wall-clock jump sets `coverage_degraded`, which is reported and is never treated as proof.
- **Phase:** v1 for (a)-(c); (d) monotonic time in v1, `coverage_degraded` flag in v2 state.
- **Risk:** Low.

### Change 4: The 8 cases mapped to named states with phase-labelled bounds (from Variant C, Variant A, debate)

- **Source:** Variant C case-mapping table (bounds per case); Variant A section 5; U-012 (H1-H4) and C-032 (case-4 batch-ack hypothesis).
- **Target:** Base section 5 table: replace the "Bound" column with "v1 bound" and "v2 profile" columns and edit the "Response" column. B's occurrence and detection causes stay as they are.
- **Rationale:** U-011 (occurrence/detection split) is endorsed by all three. Merge guidance item 7 requires phase labels. U-012 is kept only as an unranked, UNVERIFIED investigation order. Merge guidance item 2 makes exhaustion latch to L5.
- **Integration approach:** The table rows become:

  | Case | Named state | v1 bound | v2 profile | Response |
  |---|---|---|---|---|
  | 1 autocompact thrash | S6 `context-exhausted` | Recorded by 15 min | 6 min | L1 confirm twice, 5 min apart; L2 interrupt plus handoff request; then L5. L4 only on an Orca stall proof (Change 9) |
  | 2 idle at prompt | S3 `idle-at-prompt` | 15 min | 6 min | L1 confirm, L2 nudge under the lineage cap (Change 10) |
  | 3 alive judged from mtime | S3 | 15 min | 6 min | As case 2. A file mtime only corroborates and never decides S1 |
  | 4 closing report sent as `status` | S9 `finished-unreported` | One 5-min wait cycle | 1 min (drain) | L1 read contract, L2 nudge "send `worker_done` per WC-5", L5 by 10 min after the nudge. The coordinator never sends `worker_done` |
  | 5 mailbox answer unread | S5 `blocked-in-ask`, then the Change 7 ack path | Probe at 5 min, typed copy at an identified idle prompt, L5 by 15 min from enqueue | Same, with read-confirmation fields | Change 7. Cause UNVERIFIED; H1-H4 listed unranked |
  | 6 permission prompt | S4 `blocked-on-person-prompt` | 5 min plus Orca's observation delay (UNVERIFIED) | 6 min | L1 capture the prompt text, L5 at once, re-report every 15 min. The coordinator never answers it |
  | 7 stop between chain steps | S3, or S2 when declared | 15 min | 6 min | L2 nudge; WC-14 removes the occurrence |
  | 8 thrash after restart | S6 | 15 min | 6 min | As case 1, plus the same-cause rule: no plain restart (Change 10) |

- **Phase:** Both, per column.
- **Risk:** Low.

### Change 5: INV-005 semantic-change probe and declared windows (from debate)

- **Source:** Invariant probe INV-005 (HIGH, ADDRESSED); merge guidance items 3 and 8; B Round 2 New Evidence 1; A Round 2 NE-4 (gap filter on W).
- **Target:** Base section 4.2 rows S1 and S2, base section 8.2 row S2 (replace "2 window extensions"), and FR-010.
- **Rationale:** Merge guidance item 3 adopts the shared semantic-change probe with a 15-minute record-or-report bound, held by B and C; A's 25-minute fallback is the outlier. Item 8: a declared window defers typed actions only. U-008 (`expect_until`) is partly kept on those terms. U-014 (adaptive W) is kept with A's gap filter.
- **Integration approach:** Add a semantic-change record per worker: the last time the progress token, the contract file or the transcript content changed in substance (not arrival, and not a repeated identical read). If there has been no semantic change for 10 minutes, a T2 read-only probe runs. It runs inside declared windows too, because a declared window defers only nudges and typed text. By 15 minutes the coordinator either records a named state or sends an L5 report. This path never leads to L4. In FR-010, W excludes intervals that span a declared window or a coordinator outage when the median is computed (the gap filter).
- **Phase:** v1.
- **Risk:** Medium. Probing inside declared windows raises T2 probe cost. NFR-004's cap of two T2 probes per triggered worker bounds it.

### Change 6: Message-type table: what each type never implies, persist before ack, never synthesize (from Variant C)

- **Source:** Variant C message-type table (9 types plus unknown, each with "what it never implies"); C FR-014 (never synthesize `worker_done`); C NFR-005 (persist before ack); C FR-018 (idempotency).
- **Target:** Base section 6.2 table (append a column "Never implies") and FR-012 (amend).
- **Rationale:** U-025 (persist before ack) is endorsed by all three. C-032 (case-4 batch ack) is endorsed by all three. Merge decision: wake on all nine types at 300000 ms, which B FR-011 already states.
- **Integration approach:** B's table keeps all nine rows (`heartbeat`, `status`, `worker_done`, `question`, `escalation`, `decision_gate`, `handoff`, `merge_ready`, `dispatch`) and the *unknown* row, and gains C's "Never implies" text for each. For example, `heartbeat` never implies progress; `status` never implies completion; `merge_ready` never implies merge permission. FR-012 gains: each message's handling is written to the run notes before `check --ack` (persist before ack). FR-013 stays: an unknown type is surfaced, logged and probed, and never acknowledged silently. Add C FR-014 to section 6.2's `worker_done` row: the coordinator never sends or synthesizes `worker_done` for a worker. Lifecycle-message identity checks come from Change 8.
- **Phase:** v1. The durable ledger behind persist-before-ack is v2 (Change 14).
- **Risk:** Low.

### Change 7: INV-020 ack path. Decided by merge, flagged for review (from debate, Variant A, Variant C)

- **Source:** Merge guidance item 4; INV-020 (HIGH, UNADDRESSED in debate); A section 7 (reply IDs `R-<task>-<n>`, heartbeat when `ask` returns); C FR-017 (no interrupt, copy only at a confirmed safe prompt); C-034.
- **Target:** Base section 7.2 (amend FR-015), section 7.3 (replace the A1-A5 table and FR-016), and the section 8.3 terminal copy text.
- **Rationale:** INV-020 blocked convergence because the advocates resolved it in three incompatible ways. Merge guidance item 4 says the merge must decide it. The decision below takes the option each sub-point's guidance names as common ground or as the faster bound.
- **Decision (label in the merged text: "Decided by merge, flagged for review"):**
  1. **No blind mailbox resend while delivery is uncertain.** The coordinator never sends a second mailbox copy of an answer whose read is unconfirmed.
  2. **Worker floor signal.** The worker sends the status-body ack `ack <message_id> <applied|queued|refused> <reason>` at the first legal opportunity: the first point at which its top-level session holds the answer and may send (WC-7). This is the minimum all three advocates accept. The worker also sends **one heartbeat when `ask` returns**, so "answered" becomes observable even before the ack arrives.
  3. **Coordinator timeline, measured from enqueue (the `reply`/`send` success):**
     - T+0: record `pending_ack` with reply ID `R-<task>-<n>`.
     - T+5 min with no ack or `ask`-return heartbeat: L1 read-only probe (prompt-wait listing, transcript tail, screen read).
     - If, and only if, the probe **positively identifies an idle input prompt** (empty prompt, no tool running, no person prompt, no `agentWait`): one terminal-typed copy with `--wait-submit`, carrying the reply ID and the duplicate-ack instruction. At most one typed copy per message ID.
     - T+15 min with still no ack: L5 report to the person with the message ID, the answer text, the receipt fields and the probe results.
  4. **Absolute input veto.** The coordinator never interrupts, never types into a session whose state is busy, unknown (S11) or blocked on a person prompt (S4), and never answers a person prompt. B's A3 condition "worker S3, S5 or S11" narrows to "positively identified idle prompt". B's A4 second copy is removed.
  5. Section 7.4 idempotency and section 7.5 "what the ack does not settle" stay unchanged.
- **Rejected alternatives (list in the merged text):**
  - B's single mailbox resend with the same reply ID (rejected by point 1).
  - B's 25-minute person report (slower than guidance's 10-15 minute range).
  - C's 10-minute person report. With 5-minute v1 sweeps it leaves no cycle between the typed copy and the report; it is recorded as a candidate v2 profile.
  - A's two-step `A` timeout (copy after one `A`, L5 after a second `A`), which gives a 20-minute worst case.
  - B's typed copy for an S11 or S5 worker without positive idle identification.
- **Phase:** v1 for points 1-5. v2 adds C's answer lifecycle (`answer_pending` through `resolved`) and the answer `sha256` in the ack payload (Change 14).
- **Risk:** High. This is a merge-made decision on a HIGH invariant that the debate did not converge on.

### Change 8: INV-023 identity, settlement and late-message quarantine (from debate, Variant C)

- **Source:** INV-023 union (Round 2.5 section of the debate); merge guidance item 5; C FR-005 identity key; U-022 (`attempt_epoch`, v2).
- **Target:** Base section 6.2 (lifecycle rows), section 8.1 (L4 row), section 9.1 WR-3 (handoff contents) and section 10 change table (WC-6 row).
- **Rationale:** Merge guidance item 5 applies the union. The INV-023 gap is why A and B score NOT MET on Invariant criterion 5 (`base-selection.md`).
- **Integration approach:** (a) Every lifecycle message (`worker_done`, `question`, `escalation`, `handoff`, `merge_ready`) is checked against the current Task ID and Dispatch ID. In v2 `attempt_epoch` is checked too. (b) Two settlement paths: an `exited` attempt settles by WC-6's existing proof; an attempt with a live terminal settles only through a person-directed cancellation with confirmed quiescence (no tool running, no input accepted, two reads 5 minutes apart). That path is the new WC-6 bullet in Change 12. (c) A message from a settled or replaced attempt is quarantined: logged, shown to the person and never applied. (d) WR-3 handoff files record Task ID, Dispatch ID and applied ack IDs. (e) A context compaction does not clear identity unless the session reports that it has lost the IDs; that loss is reported, not guessed.
- **Phase:** v1 for (a) with Task and Dispatch IDs, and for (b)-(e). v2 for `attempt_epoch`.
- **Risk:** High. The person-directed path depends on a WC-6 amendment the person must accept.

### Change 9: Never a stall proof: exhaustion, heartbeats, repeated reads and the coordinator's own nudges (from debate, Variant C)

- **Source:** Merge guidance item 2; X-003, X-004, C-022, C-044; Variant C FR-020 (restart only after positive proof plus reconcile, stop and settle) and C's never-on-silence list.
- **Target:** Base section 8.2 rows S3 and S6, base section 10.1 rows C-7 and C-9, and section 10.2 C-7 wording (replace).
- **Rationale:** Item 2 says that context exhaustion, heartbeats, repeated identical transcript reads and the coordinator's own nudges never settle an attempt. Only Orca's three stall proofs, or the person's recorded stop under the WC-6 amendment, do. B's C-7 sentence ("did not resume after two nudges and one direct question has met Orca's stall proof") and C-9 (v2 exhaustion as proof) contradict this.
- **Integration approach:** (a) Rewrite C-7's sentence. Ladder exhaustion leads to L5. L4 requires one of Orca's positive stall proofs: `exited`, process exit, or a transcript whose final agent turn sent no `worker_done`. (b) S3 row: L4 needs that proof plus reconcile, stop and settle (C's gates); 2 nudges and 1 ask are preconditions, not proof. (c) S6 row: confirmed exhaustion latches to L5 and asks the person for a recorded stop. Delete "In v2, two confirmed exhaustion reads become a stall proof". (d) Delete row C-9 from the change table. (e) FR-023 (never on silence) adds "never treat a heartbeat, a repeated identical read, or a nudge's own receipt as proof".
- **Phase:** v1 and v2 (the rule holds in both).
- **Risk:** Medium. Removing the v2 exhaustion proof means a thrashing worker waits on the person.

### Change 10: Ladder caps keyed by lineage, and the restart window (from Variant A, Variant C, debate)

- **Source:** A section 8 (L0-L5 caps, same-cause rule, `replaces` chain); A Round 2 UA-3 (lineage); C FR-019/020 (probe x2, ask 1 per incident, replacement budget, stricter of this and WC-6); C-019/X-012.
- **Target:** Base section 8.1 (add a "Cap" column), section 8.2 "Repeat caps" column and FR-021.
- **Rationale:** U-009 is partly kept as the lineage key. Lineage-keyed caps fix the guard gap all three variants share (Invariant criterion 3, `base-selection.md`). Merge guidance item 6: keep two per lineage (agreed) and choose the rate window explicitly as unmeasured policy.
- **Integration approach:** A lineage is the original Task plus every replacement Task (the `replaces` chain), with a lineage ID carried in every resume note. Caps:
  - **L1 probe:** read-only, every sweep; T2 probes at most 2 per triggered worker per sweep.
  - **L2 nudge:** 1 per incident and **2 per lineage**. Replacement does not reset the count. A nudge whose receipt shows no turn start counts as used.
  - **L3 ask:** 1 per incident.
  - **L4 restart with resume note:** only with a Change 9 proof, after reconcile, stop and settle. Budget: **1 replacement per rolling 60 minutes and 2 per lineage**, plus the same-cause rule (no plain restart after a same-class failure). The stricter of this budget and WC-6's three failed starts applies.
  - **L5 report:** no cap; S4 re-reported every 15 minutes.
- **Restart window decision (label in the merged text: "unmeasured policy; revisit with replay data"):** chosen value **1 per rolling 60 minutes plus 2 per lineage**. This is the Round 3 position of A and B, and C's original value. **Rejected alternative:** 2 per rolling 6 hours plus 2 per lineage (B's and A's original value, C's Round 3 position). All three advocates agree that neither value is measured (`debate-transcript.md:502`).
- **Phase:** v1 (counts kept in run notes); v2 (counts in the durable ledger, Change 14).
- **Risk:** Medium.

### Change 11: Combined resume note (from Variant C)

- **Source:** Variant C FR-021 (`resume-note.json` with `uncertain_effects`); C FR-023 stage checkpoints; U-028.
- **Target:** Base section 8.5 (append lines to the text block, and add a v2 JSON form after it).
- **Rationale:** U-028 (`uncertain_effects`) is endorsed by all three. Merge decision: the combined resume note. U-020 (the D2 freeze clause) stays as B wrote it.
- **Integration approach:** Add to B's text block: `Lineage: <lineage id>, attempt <n>.`, `Uncertain effects: <actions started but not confirmed, e.g. a push or a message send>; verify before redoing.`, and `Task ID / Dispatch ID of the replaced attempt: <ids>` (Change 8). In v2 the same fields are written to `resume-note.json`, together with `attempt_epoch` and the checkpoint `sha256` (U-023, partial).
- **Phase:** text form v1, JSON v2.
- **Risk:** Low.

### Change 12: Worker-contract amendments by WC number (from Variant B base, Variant C, debate)

- **Source:** Base section 10.1 C-1..C-8 and 10.2; Variant C FR-022 and FR-024 (WC-7 Skill invocation, chunked reads); U-033; X-015; Change 8 (WC-6).
- **Target:** Base section 10.1 table and section 10.2 wording (amend in place). Insert a "Not amended" line after the table.
- **Rationale:** U-033 (WC-7 Skill amendment) is endorsed by all three after A's Round 1 concession. Merge decisions: rules live in contract section 3; B's handoff; C's chunked reads; new WC numbers WC-14 and WC-15 from B.
- **Integration approach:** The merged table names each rule by number:
  - **WC-3** (`ask` flow): the status-body ack, plus one heartbeat when `ask` returns (Change 7). The single-ask rule is unchanged.
  - **WC-5** (closing): closing report only as `worker_done`, never `status` (B C-4).
  - **WC-6** (retries and settlement): new bullet: a person-directed cancellation with confirmed quiescence settles a live attempt (Change 8). Context exhaustion is explicitly *not* a stall proof (Change 9).
  - **WC-7** (lifecycle from the top-level session): add that a chained command is run by invoking its Skill. A worker that only reads the command file does not satisfy WC-7 (U-033).
  - **WC-10** (absence is not death): silence authorizes L1, L2 and L3 only, and declared windows defer typed actions only (B C-1, Change 5).
  - **WC-11** (single owner): the coordinator's per-sweep `stat` is scoped to the worker's own contract path (X-015).
  - **WC-12** (pull mailbox): handle every message in a batch before `--ack`; ack coordinator answers (B C-3a, WR-4).
  - **Heartbeats bullet:** carries the progress token (B C-2, WR-5); cadence stays the preamble's.
  - **WC-14 (new):** continuous chain (B C-5, WR-1).
  - **WC-15 (new):** reads of unknown-size files and prior reports in pieces of at most 80 lines, plus per-stage handoff files `<report-dir>/handoff/<n>-<command>.md` of at most 40 lines, written even on failure (B C-6, WR-2, WR-3).
  - **Contract section 4, new subsection "Liveness supervision":** B C-7 with the Change 9 rewrite.
  - **Brief layout:** one `Chain:` line (B C-8).
  - **Not amended:** WC-8 (commands contain no Orca calls), WC-9 and WC-13.
- **Phase:** v1 for all rows; v2 rows C-10..C-14 stay in a separate v2 table, minus C-9 (Change 9).
- **Risk:** Medium. Several rules change wording at once, and each one must keep `WORKER-CONTRACT.md`'s existing line references valid.

### Change 13: Harness-neutral core with Claude Code and Orca adapters (from Variant A, Variant C)

- **Source:** A section 11 (`LivenessAdapter`: `id`, `version`, `capabilities`, `cost`, `observe`, `nudge`; `Receipt`; registries; porting checklist); C FR-025 (`capabilities`, `observe`, `receive_messages`, `ack_delivery`, `submit_text`, `reconcile`) and FR-026 observation JSON; U-006, U-017, U-029, X-019, C-030.
- **Target:** Base section 11 (restructure 11.1-11.4).
- **Rationale:** Seed constraint 2 (portable core). Merge decisions: merged adapter interface, hooks optional, C's portability. U-006 (`Receipt`) is endorsed by all three. U-005 (a compulsory v2 Stop hook) is rejected by all three (X-019, C-030). U-017: exhaustion text patterns live in versioned adapter data (A Round 3, INV-005).
- **Integration approach:** The core (state model, sweep, ladder, ack protocol, caps) is written only against one interface: `id`, `version`, `capabilities()`, `cost()`, `observe()`, `receive_messages()`, `ack_delivery()`, `submit_text()` (replaces `nudge`, returns a `Receipt` with accepted / submitted / turn-started) and `reconcile()`. Two adapters are described. **Orca:** `worker-list`, prompt-wait listing (`agentWait`), `check --wait/--ack`, `terminal send --wait-submit`, `worker-read --source transcript`. **Claude Code:** transcript tail, screen-text classifier and exhaustion patterns as versioned data; hooks optional, never required. A capability the adapter lacks makes its state read `unknown`, never "fine". A's porting checklist is appended.
- **Phase:** interface and Orca/Claude Code mapping in v1; `reconcile()` crash tests in v2.
- **Risk:** Medium. Merging two method sets may hide a capability gap. The executor keeps a capability-to-state table.

### Change 14: v2 robustness block (from Variant C)

- **Source:** Variant C NFR-004 (`coverage_degraded`), NFR-006 (transactional ledger), NFR-008 (16 KiB, depth 8), NFR-009 (observability, watchdog alert at 6 min), NFR-010 (fail closed), NFR-011 (staged rollout), FR-015 (answer lifecycle), control envelope, U-031 (controller lock).
- **Target:** Base section 10 (insert a new 10.3 "v2 supervisor robustness"), after the v2 change rows.
- **Rationale:** U-025, U-026, U-030, U-031 and U-032 are endorsed by all three; C-035, C-045, C-047 and A-001 settle them. Merge decision: C's durable state in v2. U-024, U-027 and U-034 are partial and therefore v2 only.
- **Integration approach:** One subsection lists, all as v2: the durable transactional ledger (persist before ack); the controller lock, failing closed for automatic replacement if another writer cannot be excluded; the independent watchdog, which alerts if a sweep is late; untrusted-input limits; the answer lifecycle `answer_pending -> answer_enqueued -> read_confirmed -> continuation_observed -> resolved`; the control envelope `continue_assignment | describe_state | report_completion`; and staged rollout. Each item cites C.
- **Phase:** v2.
- **Risk:** Low. Additive, and v1 does not depend on it.

### Change 15: Risk table additions (from Variant C, debate)

- **Source:** Variant C risk table (15 rows); INV-020; C-019/X-012; merge guidance item 7.
- **Target:** Base section 12 (append rows; keep the Likelihood and Impact columns).
- **Rationale:** B's likelihood and impact columns are a strength to preserve (`base-selection.md`, Risk criterion 1). The merge-made decisions need their own risk rows.
- **Integration approach:** Append rows, each with likelihood, impact and mitigation:
  - The INV-020 decision is wrong for some harness. Medium / High. Flagged for review; L5 by 15 min bounds the cost.
  - The restart window is unmeasured. Medium / Medium. Replay data (U-016).
  - The v2 profiles miss their capacity gate. Medium / Low. v1 values stay.
  - A late message from a replaced attempt is applied. Low / High. Change 8 quarantine.
  - Monotonic-clock or ledger failure. Low / Medium. `coverage_degraded`, fail closed.
  - Add C's rows that B lacks, given B's likelihood and impact.
- **Phase:** both, per row.
- **Risk:** Low.

### Change 16: Acceptance criteria merge (from Variant A, Variant C)

- **Source:** A section 13 AC-1..14; C FR-027 tests 1-12; U-016 (replay fixtures as a measurement gate).
- **Target:** Base section 13 acceptance list (extend AC-1..8).
- **Rationale:** Completeness criterion 4 credits all three. Merging them gives one test per bound and per HIGH invariant. Change 3 fixes AC-1.
- **Integration approach:** Keep B's AC-1..8 (AC-1 at 15 min). Add, de-duplicated and each labelled v1 or v2: a replay of each of the 8 cases reaching its Change 4 bound; the INV-020 timeline (no mailbox resend, L5 by 15 min); typed copy refused at a busy or person prompt; quarantine of a late `worker_done`; the L2 count surviving replacement; same-cause restart refused; unknown type surfaced; C's test 12 capacity run (v2 gate); crash and `reconcile()` tests (v2).
- **Phase:** both, per item.
- **Risk:** Low.

## Changes NOT Being Made

| # | Contribution | From | Reason |
|---|---|---|---|
| 1 | WC-6 amendment making confirmed context exhaustion a stall proof (v2) | A section 10 | Merge guidance item 2; X-003, X-004, C-022, C-044 |
| 2 | C-7 sentence: an idle worker that "did not resume after two nudges and one direct question has met Orca's stall proof" | B section 10.2 | Contradicts B's own L4 gate and merge guidance item 2; rewritten by Change 9 |
| 3 | C-9: two confirmed exhaustion reads become a stall proof (v2) | B section 10.1, 8.2 S6 row | Merge guidance item 2 |
| 4 | 25-minute degraded fallback for INV-005 | A (Round 3) | Merge guidance item 3: the 15-minute record-or-report bound covers it, because the fallback outcome is a report, not an action |
| 5 | Single mailbox resend with the same reply ID | B (INV-020) | Change 7 point 1: no blind resend while delivery is uncertain |
| 6 | 25-minute person report for an unacked answer | B (INV-020) | Outside the 10-15 minute range in merge guidance item 4 |
| 7 | 10-minute person report for an unacked answer, as a v1 value | C FR-017 | Leaves no 5-minute cycle between the typed copy and the report; recorded as a v2 profile candidate (Change 7) |
| 8 | Two-step `A` ack timeout (copy after one `A`, L5 after a second) | A section 7 | 20-minute worst case against the 15-minute target (IC contradiction) |
| 9 | 1-minute mailbox drain and 6-minute idle and person-prompt bounds as v1 values | C FR-010, detection table | Merge guidance item 7: v2 profiles gated on a capacity test (Change 2) |
| 10 | L2 cap "2 per episode, 4 per Task" | A section 8 | Resets on replacement; replaced by the lineage cap (Change 10) |
| 11 | Nudge caps "2 per 60 min per Task" and "2 per attempt" | B section 8.2, C FR-019 | Same guard gap; replaced by 2 per lineage (Change 10) |
| 12 | Restart window of 2 per rolling 6 hours plus 2 per lineage | A, B (original); C (Round 3) | Rejected alternative for C-019/X-012 (Change 10); unmeasured, like the chosen value |
| 13 | Compulsory v2 Stop hook (FR-029) | A section 9 | U-005 rejected by all three (X-019, C-030); hooks are optional adapter features |
| 14 | Handoff files `<report-dir>/handoff/c<n>.md` of at most 20 lines | A WR-3 | Merge decision: B's handoff format (`<n>-<command>.md`, at most 40 lines, written on failure) |
| 15 | 30-minute report for S7 `unreachable` | B section 4.2 | Merge decision: report by 10 minutes (Change 3) |
| 16 | "2 window extensions" for S2 past its window | B section 8.2 | Replaced by the INV-005 semantic-change probe (Change 5) |
| 17 | Answer lifecycle and control envelope as v1 requirements | C FR-015, control envelope | U-024 and U-027 partial: v2 only (Change 14) |
| 18 | Amendments to WC-2 and WC-4 | C FR-024 | Not debated as points; no merge decision. Listed under Open Questions |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | State references in sections 4, 5 and 8 break or drift | Restore B's section 2 and keep A's axes as an appendix table |
| 2 | Low | A bound shown without its phase | Drop the v2 column; v1 values are B's |
| 3 | Low | AC-1 or NFR-004 wording still conflicts | Revert to B's text and re-list X-014/X-015 as open |
| 4 | Low | A case row loses B's cause text | Restore B's section 5 table and add only the bound columns |
| 5 | Medium | T2 probe cost rises inside declared windows | Keep the record-or-report bound; remove probing inside windows |
| 6 | Low | Persist-before-ack wording implies a ledger v1 does not have | Reword to "written to run notes" |
| 7 | High | The ack path stalls, or a typed copy lands at a wrong prompt | Revert to B's A1-A5 minus the resend, and mark INV-020 open |
| 8 | High | A legitimate message gets quarantined, or the person-directed path is not accepted | Keep the ID check; drop the live-terminal settlement path and leave such workers at L5 |
| 9 | Medium | A thrashing worker waits on the person longer | None in the rule. The L5 report carries the evidence the person needs to act fast |
| 10 | Medium | Caps stop recovery of a lineage too early | Raise the lineage cap in the parameter table (Change 2); the window is labelled as policy |
| 11 | Low | Resume note grows past what a brief can carry | Move the extra fields to the handoff file and point to it |
| 12 | Medium | Contract wording drifts from `WORKER-CONTRACT.md` line references | Apply rule by rule; revert a single row |
| 13 | Medium | A capability gap is hidden by the merged interface | Keep A's interface and add C's methods as optional |
| 14 | Low | v2 items read as v1 commitments | Move the subsection to an appendix |
| 15 | Low | Duplicate risk rows | De-duplicate against B's R1-R14 |
| 16 | Low | Too many acceptance criteria to run | Keep B's AC-1..8 plus the HIGH-invariant tests |

## Review Status

- [x] Auto-approved (non-interactive run)
- Approved by: auto
- Timestamp: 2026-11-07T20:35:00Z
- Flagged for review in the merged output: Change 7 (INV-020, "decided by merge, flagged for review") and Change 10 (restart window, "unmeasured policy").

## Open Questions

The merge executor carries these into the merged output's open-questions section. None of them blocks the merge.

1. **Restart window (C-019/X-012).** The chosen 1 per rolling 60 minutes is unmeasured policy. The rejected alternative is 2 per rolling 6 hours. Revisit with replay data (U-016).
2. **INV-020 decision.** The person should confirm or overturn Change 7: no resend, the floor ack plus an `ask`-return heartbeat, a typed copy only at an identified idle prompt, and L5 by 15 minutes.
3. **Undebated points S-001, S-002, S-003, S-004, S-009, S-012 and S-013.** These are presentation choices kept as B has them. S-013's content is covered by the X-018/C-023 merge.
4. **MEDIUM invariants INV-001, INV-006, INV-009, INV-010, INV-011, INV-016 and INV-024.** All three advocates accepted the fixes. The executor should confirm each fix is visible in the merged text. **INV-022** was accepted narrowed (A), in part (B), and as optional coarse declarations (C). The form is open.
5. **Case 5 cause.** UNVERIFIED. H1-H4 are kept unranked as an investigation order.
6. **`agentWait` reliability.** Orca's observation delay for a person prompt is UNVERIFIED, so case 6's v1 bound is "5 min plus that delay".
7. **Payload intactness.** Whether the preamble's `send` carries a JSON payload intact, and so whether the ack's payload form is usable, is UNVERIFIED. The body line remains the authority.
8. **`worker-read` timestamps.** Whether transcript entries carry timestamps fine enough for the 5-minute inactivity test is UNVERIFIED for Claude Code.
9. **Capacity test for the v2 profiles.** C's test 12 (six workers and the supported fleet limit) gates the 6-minute and 1-minute figures. Fleet size and cost budget are unmeasured.
10. **`--types` omitted.** What `check --wait` wakes on without `--types` is not stated in the help. The design lists all nine types explicitly.
11. **Busy-session typing.** What Claude Code does with typed text that arrives while a tool call runs is UNVERIFIED. Change 7's input veto avoids the case, but nudges (L2) still rely on the text being harmless when read late.
12. **`attention` categories.** Whether Orca's attention or prompt-wait categories separate permission prompts from other waits is UNVERIFIED.
13. **C's WC-2 and WC-4 amendments.** These were not debated. The merge leaves both rules unamended in v1. The person decides whether C's FR-024 wording for them is wanted.
14. **GitHub-target constraint.** No variant restates the seed constraint "GitHub target only `IronbellyOrg/IronClaude`; no Orca `--issue`/`--pr` link flags" (`seed-brief.md:38`). The merged output should restate it once in its constraints.
