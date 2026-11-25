# Merge Execution Log

## Metadata

- **Base:** `variant-2-opus-analyzer.md` (Variant B)
- **Executor:** merge-executor agent
- **Changes applied:** 16 of 16
- **Status:** COMPLETE
- **Timestamp:** 2026-11-07T20:55:00Z
- **Plan:** `refactor-plan.md` (16 planned changes, applied in plan order)
- **Output:** `merged-output.md`

## Changes Applied

### Change 1: Three evidence axes, `proof_class` and cost tiers

- **Status:** APPLIED
- **Source:** Variant A sections 2 and 3
- **Target:** Merged sections 2 (2.1 rewritten) and 3 (new 3.3)
- **Before:** Section 2 listed states S0-S11 with single-signal entry conditions; section 3 had no observation record and no cost model.
- **After:** 2.1 is "Two questions, answered on three axes" (Process, Interaction, Progress), and the state table names the axes. New 3.3 "Observation record and cost tiers" defines the record, `proof_class` (positive, corroborating, hint, unknown) and tiers T0, T1, T2. The base 3.3 moved to 3.4 "Adapter boundary".
- **Provenance tag:** `[from A section 2]`, `[from A section 3]`, plus `<!-- Source: ... -->` comments
- **Validation:** Every S0-S11 reference in sections 4, 5 and 8 was re-checked against 2.2 and resolves.

### Change 2: Timing-parameter table and phase labels

- **Status:** APPLIED
- **Source:** Variant A section 4 parameter table and NFR-003; Variant C detection table and NFRs
- **Target:** Merged 4.1 (parameter block after FR-010), 4.2 (Phase column), 1.4 (new NFR-008)
- **Before:** Timing values were scattered through 4.2 with no v1 or v2 label.
- **After:** One named parameter block in 4.1, a Phase column on every bound in 4.2, and NFR-008 requiring one block that a Task brief may override and a worker may not.
- **Provenance tag:** `[from A section 4]`, `[from A NFR-003]` (Change 2)
- **Validation:** All values in 4.2 appear in the block; the v2 figures (6 min, 1 min) are labelled v2 only.

### Change 3: Per-state bound corrections and contradiction fixes

- **Status:** APPLIED
- **Source:** X-014 and X-015 resolutions; merge decision on S7; Variant C NFR-004 (monotonic time)
- **Target:** Merged 4.2 rows S3, S6 and S7; NFR-004; AC-1
- **Before:** S7 reported at 30 min; AC-1 accepted case 1 at 20 min.
- **After:** S7 reported at L5 by 10 min; S3 and S6 bounded at 15 min; NFR-004 requires monotonic time; AC-1 records case 1 by 15 min.
- **Provenance tag:** `[from debate X-014]`, `[from debate X-015]`, `[Change 3]`
- **Validation:** Re-scan found no remaining "30 min" for S7 and no "20 min" bound; the only "20 min" left is the observed duration in case 6.

### Change 4: The 8 cases mapped to named states with phase-labelled bounds

- **Status:** APPLIED
- **Source:** Variant C case-mapping table; Variant A section 5; U-012 (H1-H4); C-032
- **Target:** Merged section 5 table
- **Before:** One "Bound" column; case 5 cause ranked.
- **After:** "v1 bound" and "v2 profile" columns; Response column edited per plan; case 5 hypotheses H1-H4 kept unranked and the cause stays UNVERIFIED; B's occurrence and detection text unchanged; 5.1 item 1 cites FR-026.
- **Provenance tag:** `[from C case table]`, `[from A section 5]`, `[Change 4]`
- **Validation:** Each bound matches 4.2 for its state. The plan wrote case 1 as "Recorded by 15 min"; the table states "15 min", the same value.

### Change 5: INV-005 semantic-change probe and declared windows

- **Status:** APPLIED
- **Source:** INV-005; merge guidance items 3 and 8; B Round 2 NE-1; A Round 2 NE-4
- **Target:** Merged 4.2 rows S1 and S2, 8.2 row S2, FR-010; new FR-026
- **Before:** S2 could be granted "2 window extensions"; no read-only probe inside a declared window.
- **After:** New FR-026 defines a read-only semantic-change probe that runs inside declared windows; a declared window defers typed actions only (also WR-7); window extensions removed.
- **Provenance tag:** `[from debate INV-005]`, `[Change 5]`
- **Validation:** Re-scan found no "window extension" text. NFR-004's cap of two T2 probes per worker per sweep bounds probe cost.

### Change 6: Message-type table, persist before ack, never synthesize

- **Status:** APPLIED
- **Source:** Variant C message-type table, FR-014, NFR-005, FR-018
- **Target:** Merged 6.2 table and FR-012
- **Before:** 6.2 had no "never implies" column; FR-012 did not order persistence and ack.
- **After:** 6.2 gains a "Never implies" column `[from C]` for 9 types plus unknown; the `worker_done` row says the coordinator never sends or synthesizes it; FR-012 requires persist before ack.
- **Provenance tag:** `[from C]`, `[Change 6]`
- **Validation:** All 9 types plus unknown present; cross-checked against FR-011's type list.

### Change 7: INV-020 ack path (decided by merge, flagged for review)

- **Status:** APPLIED
- **Source:** Merge guidance item 4; INV-020; Variant A section 7; Variant C FR-017
- **Target:** Merged 7.2 (FR-015), 7.3 (table and FR-016, FR-017), 8.3 terminal copy text
- **Before:** A1-A5 timeline that resent the answer by mailbox before escalating.
- **After:** A1-A4 timeline: A1 T+0 record `pending_ack` with reply ID `R-<task>-<n>`; A2 T+5 read-only probe; A3 one typed copy only at a positively identified idle prompt; A4 T+15 L5 report. No blind resend; absolute input veto; worker acks at the first legal opportunity plus a heartbeat when `ask` returns; a worker without a terminal skips A3. Rejected alternatives listed. Labelled "Decided by merge, flagged for review (INV-020; open question 2 in section 13.2)".
- **Provenance tag:** `[from A section 7]`, `[from C FR-017]`, `[Change 7]`
- **Validation:** Re-scan found no "A5". Open question 2 in 13.2 and R16 both point to the decision.

### Change 8: INV-023 identity, settlement and late-message quarantine

- **Status:** APPLIED
- **Source:** INV-023 union (debate Round 2.5); merge guidance item 5; C FR-005; U-022
- **Target:** Merged 6.2 lifecycle rows, new FR-028, 8.1 L4 row, 9.1 WR-3, 10.1 (new C-15 for WC-6)
- **Before:** No identity check on lifecycle messages; L4 required only a stall proof.
- **After:** FR-028 checks Task ID and Dispatch ID (plus `attempt_epoch` in v2); failing messages are quarantined; compaction does not clear identity. L4 requires reconcile, stop and settle, through an Orca stall proof or the person-directed cancellation path (C-15). WR-3 handoffs carry Task ID and Dispatch ID.
- **Provenance tag:** `[from debate INV-023]`, `[from C FR-005]`, `[Change 8]`
- **Validation:** C-15 row present in 10.1 with wording in 10.2; open question Q8 asks the person to accept it.

### Change 9: Never a stall proof

- **Status:** APPLIED
- **Source:** Merge guidance item 2; X-003, X-004, C-022, C-044; Variant C FR-020
- **Target:** Merged 8.2 rows S3 and S6, 10.1 rows C-7 and C-9, 10.2 C-7 wording, FR-023
- **Before:** C-9 made twice-confirmed exhaustion a v2 stall proof; S3 could escalate on nudge receipts.
- **After:** C-9 deleted (ID not reused). S6 latches to L5 and asks for a recorded stop. S3 treats nudges and `ask` as preconditions, not proof. FR-023 says heartbeats, exhaustion, repeated identical reads and nudge receipts are never stall proofs. C-7 wording names only existing Orca proof kinds.
- **Provenance tag:** `[from debate]`, `[from C FR-020]`, `[Change 9]`
- **Validation:** Remaining "C-9" mentions are the deletion note, the 10.1 source comment and Q8; none treats exhaustion as proof. AC-4 now checks this.

### Change 10: Ladder caps keyed by lineage, and the restart window

- **Status:** APPLIED
- **Source:** Variant A section 8 and Round 2 UA-3; Variant C FR-019 and FR-020
- **Target:** Merged 8.1 (Cap column, lineage definition), 8.2 caps, FR-021
- **Before:** Caps per Task; restart window "2 per rolling 6 h".
- **After:** Lineage defined as the original Task plus all its replacements. L1 at most 2 T2 probes per worker per sweep; L2 1 per incident, 2 per lineage; L3 1 per incident; L4 1 per rolling 60 min and 2 per lineage, plus the same-cause rule, with the stricter of this and WC-6 applying; L5 no cap. Marked "Unmeasured policy; revisit with replay data." 2 per rolling 6 hours listed as rejected.
- **Provenance tag:** `[from A section 8]`, `[from C FR-019]`, `[Change 10]`
- **Validation:** "6 h" appears only as the rejected alternative (FR-021, open question 1). "unit of work" appears once, in the `handoff` row, meaning new work under WC-13, not a budget unit; AC-7 now says lineage.

### Change 11: Combined resume note

- **Status:** APPLIED
- **Source:** Variant C FR-021, FR-023; U-028
- **Target:** Merged 8.5
- **Before:** Text-only resume note.
- **After:** Lineage, Task and Dispatch ID and Uncertain effects lines added to the text block; v2 `resume-note.json` fields added after it.
- **Provenance tag:** `[from C FR-021]`, `[Change 11]`
- **Validation:** Field names match FR-028 identity terms.

### Change 12: Worker-contract amendments by WC number

- **Status:** APPLIED
- **Source:** Base 10.1 and 10.2; Variant C FR-022, FR-024; U-033; X-015; Change 8
- **Target:** Merged 10.1 table, 10.2 wording, "Not amended" line
- **Before:** C-1..C-9 without WC numbers in a single table.
- **After:** v1 table C-1..C-8 plus C-15 (WC-6), C-16 (WC-7 Skill invocation), C-17 (WC-11 stat scope), each naming its WC rule; v2 table C-10..C-14; "Not amended" line for WC-8, WC-9, WC-13; 10.2 rewords C-1, C-3b, C-7 and adds C-15, C-16, C-17 wording; 10.3 restates the GitHub-target constraint (`seed-brief.md:38`).
- **Provenance tag:** `[from C FR-022]`, `[from C FR-024]`, `[Change 12]`
- **Validation:** Existing `WORKER-CONTRACT.md` line references kept unchanged. C's WC-2 and WC-4 amendments were not made (plan scope) and are carried as open question 13.

### Change 13: Harness-neutral core with Claude Code and Orca adapters

- **Status:** APPLIED
- **Source:** Variant A section 11; Variant C FR-025
- **Target:** Merged section 11 (11.1-11.4)
- **Before:** Base adapter sketch with `observe_fleet` and `nudge(...)`.
- **After:** Merged `LivenessAdapter` interface (`id`, `version`, `capabilities`, `cost`, `observe`, `receive_messages`, `ack_delivery`, `submit_text`, `reconcile`, with `Receipt`); capability-to-state table; Orca, Claude Code (hooks optional) and Filesystem adapters; A's porting checklist; extension points in 11.4.
- **Provenance tag:** `[from A section 11]`, `[from C FR-025]`, `[Change 13]`
- **Validation:** Re-scan found no "observe_fleet" or "nudge(" left. The capability-to-state table covers S0-S11, so no capability gap is hidden.

### Change 14: v2 robustness block

- **Status:** APPLIED
- **Source:** Variant C NFR-004, NFR-006, NFR-008..NFR-011, FR-015, control envelope, U-031
- **Target:** Merged section 10 (placed as new 10.5)
- **Before:** No v2 robustness section.
- **After:** 10.5 table, all v2: transactional ledger, controller lock with fail-closed, independent watchdog (6 min, or mailbox older than 2 min), untrusted-input limits (16 KiB, depth 8), answer lifecycle, control envelope, `coverage_degraded`, staged rollout.
- **Provenance tag:** `<!-- Source: Variant C ... added by Change 14. All items v2 -->`
- **Validation:** Placed at 10.5 rather than the plan's "new 10.3" to keep base 10.3 and 10.4 numbering stable. NFR IDs in its source comment are Variant C's own IDs, labelled as such.

### Change 15: Risk table additions

- **Status:** APPLIED
- **Source:** Variant C risk table; INV-020; C-019/X-012; merge guidance item 7
- **Target:** Merged section 12
- **Before:** R1-R15 with Likelihood and Impact.
- **After:** R1, R5, R7, R8, R10, R11, R12 updated; Phase column added; R16-R20 for the merge decisions (R16 points to open question 2); R21-R33 from C's table, with likelihood and impact marked as merge estimates; false-positive budget paragraph kept.
- **Provenance tag:** `[from C risk table]`, `[Change 15]`
- **Validation:** R1-R33 each have one row; no reference to a missing R number.

### Change 16: Acceptance criteria merge

- **Status:** APPLIED
- **Source:** Variant A section 13; Variant C FR-027 tests 1-12; U-016
- **Target:** Merged 13.1, 13.2, 13.3
- **Before:** AC-1..AC-8; open questions Q1-Q9 with Q8 on C-9; recommendation "adopt C-1 to C-8".
- **After:** AC-1, AC-3, AC-4 and AC-7 updated; AC-9..AC-17 added with v1, both, v2 gate or v2 labels (INV-020 timeline, typed copy refused, late `worker_done` quarantine, L2 count across replacement, same-cause restart refused, unknown type surfaced, bounds per profile, capacity test as v2 gate, crash and `reconcile()` tests). 13.2 lists the plan's open questions 1-14 first (item 2 is INV-020), then base Q1-Q9 with Q8 replaced by the C-15 acceptance question. 13.3 says adopt C-1 to C-8 and C-15 to C-17, and v2 after Q2, Q3, Q6 and AC-16.
- **Provenance tag:** `<!-- Source: Base 13.1 ... Change 16 -->`
- **Validation:** Every AC names a seed criterion or NFR and a phase.

### Numbering and placement decisions

- New IDs: FR-026 (semantic-change probe), FR-027, FR-028 (lifecycle identity check); C-15, C-16, C-17; AC-9..AC-17; R16..R33.
- C-9 deleted and its ID not reused.
- 7.3 steps renumbered A1-A4 (the base had A1-A5).
- New 3.3 inserted; base 3.3 is now 3.4.
- The v2 robustness block is 10.5, not the plan's "new 10.3", so base 10.3 and 10.4 keep their numbers. This is a placement choice only; content is as planned.
- Section 13 heading set to "Acceptance Criteria and Open Questions" (title case, matching the other top-level headings).

## Post-Merge Validation

### Structural Integrity

- **Heading hierarchy:** PASS. One H1, thirteen H2 sections numbered 1-13, H3 subsections numbered within each section, no skipped levels.
- **Section ordering:** PASS. Sections 1-13 in order; subsections sequential (3.1-3.4, 10.1-10.5, 13.1-13.3).
- **Document flow:** PASS. No placeholder text remains; each section carries a source comment.

### Internal References

- **Total:** 334 references (FR, NFR, AC, C and R IDs and "section N.N" cross-references).
- **Resolved:** 334. Every FR and NFR ID used is defined; every C ID has a table row except C-9, whose mentions are the deliberate deletion notes; every R ID has a row; every "section N.N" target exists.
- **Broken:** 0. NFR-009..NFR-011 occur only in the 10.5 source comment, where they are Variant C's own IDs and are labelled "Variant C".

### Contradiction Re-Scan

- **New contradictions:** 0.
- **Details:** Scanned for "30 min", "20 min", "6 hours", "6 h", "C-9", "window extension", "per 60 min per Task", "A5", "unit of work", "nudge(", "observe_fleet", em dashes, "PLACEHOLDER" and "Q10". Remaining hits are intended: "30 min" in the v2 compaction rule (S6, 3 or more compactions in 30 minutes) and observed case durations; "20 min" only as the case 6 observed duration; "6 h" only as the rejected restart window; "C-9" only as deletion notes; "unit of work" only in the `handoff` row (WC-13 meaning). No em dashes, no placeholders. One wording note, not a contradiction: the S6 definition in 2.2 lists the compaction count as signal (c) without a phase label, while 4.2 labels the same signal v2; both say the adapter reports it.

## Summary

- **Planned:** 16
- **Applied:** 16
- **Failed:** 0
- **Skipped:** 0
- **Post-merge validation:** PASS
