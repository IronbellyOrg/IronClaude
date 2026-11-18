# Merge Execution Log

## Metadata
- Base: Variant B (Proposal B, `variant-2-original.md`; default model, default persona)
- Plan: `refactor-plan.md` (16 planned changes, approved by auto after `plan-review.md`, 2026-11-14T16:58:30Z)
- Executor: merge-executor agent (c06-merge-executor), run in the foreground
- Output: `.../reviews/adversarial/limits-repair-policy/merged-output.md`
- Changes applied: 16 of 16
- Status: success
- Timestamp: 2026-11-14T17:14:53Z (completion of the log)
- Merge date written in the merged file header: 2026-11-14T17:03:26Z (`date -u`, taken before the first write)
- Inputs read: `refactor-plan.md`, `variant-2-original.md`, `variant-1-original.md`, `round2-advocate-A.md`, `round2-advocate-B.md`, `invariant-probe.md`, `round2.5-fault-finder-raw.md`, the protocol's provenance and post-merge validation text (`sc-adversarial-protocol/SKILL.md` "Provenance Annotation System" to "Post-Merge Consistency Validation") and `refs/artifact-templates.md` Sections 5 and 6. The excluded task folder and the queued-run file were not read.
- Code lines re-read to confirm cites copied from the debate: `merge_cmd.py:99-118`, `manifest.py:371-383`, `ledger.py:114-118,128,146`, `card_convert.py:200-201`, `tests/cli/reflect/test_shadow_skill_contract.py:229-232`, and the three production `parse_block` call sites (`ledger.py:128`, `cluster_cmd.py:151`, `verify_cmd.py:133`). All matched. Other cites were copied from the plan and the debate files without re-reading.

## Changes Applied

### Change 1: Cut the three location fields in code, behind a keyword
- **Status**: Applied
- **Source**: Variant A (Proposal A), Section 1 and Section 2 items 1-2; round2-advocate-A.md and round2-advocate-B.md section 6 bullet 1; round2-advocate-B.md section 0, W1, N1, E2, E4
- **Target**: Base section 1; section 3.6 (replaces the "No truncation step, no normaliser ... no repair-aware parse" sentence); a short row "Repair step" in the section 3.1 table
- **Before**: Position "never edits reviewer text"; section 3.6 listed what B does not do (no truncation, no normaliser, no repair-aware parse).
- **After**: Section 1 states the cut of `anchor`, `anchor2` and citation `quote` to 200 flattened characters by one pure `repair_line`, behind `parse_block(text, *, repair=False)`, with the three production call sites passing `repair=True`, a test that every call site passes the keyword and the default stays `False`, no `prior` line touched, report file never edited, direct-parser pins unmodified. Section 3.6 gives the reasons (replay and second-population run, no v1 vehicle for a pre-merge re-ask, 10 of 273 merges below the floor under no-edit) and the evidence limit (single-line tasklist rows only; `quote` has no location measurement; no PR-code corpus; Round 2.5 INV-017 carried open).
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 1 and Section 2 items 1-2 - merged per Change 1 -->` and `<!-- Source: Base (original, modified) - headline position reversed ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (one wording adjustment, see Post-Merge Validation item D1)

### Change 2: One shared record for cuts and drops
- **Status**: Applied
- **Source**: Variant A section 2 item 3 (`repairs`) merged with Variant B section 3.1; both final bullets 2
- **Target**: Base section 3.1 rows "Line classifier and drop record" and "Result shape"; section 3.3 bullet 1; section 3.1 sentence on the "shortened from N" note
- **Before**: record `{line, id, rule, field, actual, limit, blocking_state}`; one additive key `dropped`.
- **After**: record `{line, finding_id, blocking_state (true, false, unknown), rule, field, original_chars, kept_chars, original_sha256}`, never reviewer text; additive keys `repairs` and `dropped` beside unchanged `ok`/`state`/`errors`; per-block conservation kept; `### Lx` block prints "shortened from N" next to the anchor status (no new column); `refs_changed` recorded when `refs_norm(original) != refs_norm(repaired)`; copy-to-`refs` not adopted. Reviewer entries add `repaired` and `dropped` beside `block_ok`. Round 2.5 INV-005, INV-007, INV-008, INV-011 are listed in section 10 and are not closed.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 2 item 3 (`repairs`) merged with the base's classifier - merged per Change 2 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: First-pass state carrier
- **Status**: Applied
- **Source**: Variant A section 2 item 8; round2-advocate-A.md section 3 N6; both final bullets 7 (A) and 6 (B)
- **Target**: Base section 3.1 (new row "First-pass carrier"), section 3.2 bullet 1, section 5 INV-A and INV-L rows, section 6.2 (T-A5)
- **Before**: no carrier for first-pass state; INV-A said `dropped` is not emitted; INV-L said `dropped` goes to the notes only.
- **After**: `first_pass_state` (`state` unless `complete`, else `invalid` when `repairs` is non-empty); `cluster_cmd.py:155-163` and `verify_cmd.py:136-138` emit `first_pass_state` and `repairs` beside the unchanged `state`; `findings_block_compliance_rate` is the share of cards whose `first_pass_state` is `complete`; `repaired_lines_rate` and `dropped_lines_rate` per model reported next to it; differential test against a `repair=False` parse; A-005 stated as holding only while shadow lasts unless the carrier is used. Round 2.5 INV-002 and INV-004 are listed in section 10 and are not closed.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 2 item 8 and Debate (round2-advocate-A.md section 3 N6) - merged per Change 3 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Re-ask trigger, transport and record
- **Status**: Applied (with a note on the target)
- **Source**: Variant A section 2 item 6; round2-advocate-A.md section 3 N1; round2-advocate-B.md section 1.2 N1 and W5; both final bullets 3-5 (A) and 3-4 (B)
- **Target**: Base section 3.2 (trigger, transport and record bullets, plus the recovery-evidence statement). The plan also names "section 3.3 bullets 2-3"; those base bullets (eligibility and refusal reason) are rewritten under Changes 6 and 5, and the v1 refusal-driven trigger sits in section 3.2 with the v1 price in section 3.3.
- **Before**: trigger "a dropped line whose `blocking_state` is `true` or `unknown`, or a block-level failure" before the merge; fallback "itemise-only plus the fail-closed rule, never a truncation"; "5 of 5" recovery wording.
- **After**: re-ask only for what is still invalid after the cut; v1 trigger is a refusal (dropped-blocking or the C-03 quorum refusal), the coordinator re-asks the named reviewer and re-runs `merge` with the replacement report (`report_sha256` in that round's entry); `blocking: false` drops itemised and not re-asked in v1; reflect keeps the E1 rule plus the invalid-block-with-prior amendment; stateless prompt by default, `--resume` an optimisation only; attempt 2 recorded before the `collected` commit and only while the earlier attempt is not `complete` (`manifest.py:371-383`); v1 has no manifest; record shape belongs to C-08; a transport that cannot re-ask degrades to itemise plus the refusal; recovery evidence stated as four confirmed re-asks of five. Round 2.5 INV-018 and INV-003 pointers added; neither is closed.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 2 item 6 and Debate (round2-advocate-A.md section 3 N1; round2-advocate-B.md section 1.2 N1) - merged per Change 4 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Dropped-blocking refusal, implementation constraints
- **Status**: Applied
- **Source**: Variant B section 3.3; round2-advocate-A.md section 3 N2 and N5; round2-advocate-B.md section 1.2 N1, N2, N5 and section 3 E3-E4; both final bullets 8 (A) and 7 (B)
- **Target**: Base section 3.3 (firing statement replaced; constraints added), section 4.2 (fire counts)
- **Before**: "fires on 3 of 264" with "none of the other 261" in M1; refusal bullet without implementation constraints.
- **After**: fires when the derived verdict would be PASS and an unacknowledged dropped line has `blocking_state` `true` or `unknown`; runs at the end of `merge_round`, after the quorum check, on a working copy swapped in place on success (pins `test_review_ledger.py:352-361,373`); reuses C-03's subtype and exit 12 with `{"refusal": "dropped_blocking", reviewers, dropped}`; ledger file unchanged; owner-and-reason acknowledgement lifts it, recorded in the round entry and listed in the merged report; no refusal when a blocking row survives; counts restated as 3 of 264 without the cut and 0 with it (0 of 264 labelled as derived from the `flags.tsv` reason text, 0 of 273 executed on P273); recorded price (36 of the 39 merges that carry a dropped blocking line on P273). Round 2.5 INV-001, INV-006, INV-020, INV-026 pointers added; none is closed.
- **Provenance tag**: `<!-- Source: Debate (round2-advocate-A.md section 3 N2 and N5; round2-advocate-B.md section 1.2 N2 and N5, section 3 E3-E4) - merged per Change 5 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Eligibility for clearing and quorum (unresolved C-002)
- **Status**: Applied
- **Source**: round2-advocate-B.md section 6 bullet 5; round2-advocate-A.md section 6 bullet 6; both final tables (C-002, A-004)
- **Target**: Base section 2 (C-02 row), section 3.3 (eligibility bullet), section 10.1
- **Before**: "because its `block_ok` is False ... does not count toward clearing" (a single rule, stated as a cost of B).
- **After**: both alternatives stated side by side with each advocate's final position (A: Variant 1, 80 percent; B: Hybrid, 74 percent), the shared ground (`ok`/`state` stay the parser verdict on the cut lines; `repaired` and `dropped` recorded beside `block_ok`), the common cost figures (10 of 273 below the floor on P273; at least 7 of 264 on audit-D) and the statement that the merged text does not choose. Section 10.1 repeats both positions.
- **Provenance tag**: `<!-- Source: Debate (round2-advocate-B.md section 6 bullet 5; round2-advocate-A.md section 6 bullet 6) - merged per Change 6 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (no statement decides C-002)

### Change 7: Claim field (unresolved C-001 claim part and C-009)
- **Status**: Applied
- **Source**: round2-advocate-B.md section 1.3 and section 6 bullets 2 and 10; round2-advocate-A.md section 1.3 and section 6 bullets 1 and 11; Variant A section 2 item 7 and section 7 point 3
- **Target**: Base section 3.6 and section 8 (the claim point sits in section 8 Answer 1 point 4), section 10.1, section 6.1 (M5) and section 6.3 (K2)
- **Before**: base wording that no other field is cut and that B rejects truncation as a default.
- **After**: both positions side by side with the P273 evidence, both forms of K2 (A: falsifier of the cut; B: precondition for the cut), the test population (34 claims, 22 blocking), the statement that the default is the owner's decision and that only the location-field cut is implemented first; the claim cut is a separate switch.
- **Provenance tag**: `<!-- Source: Debate (round2-advocate-A.md section 1.3 and section 6 bullets 1 and 11; round2-advocate-B.md section 1.3 and section 6 bullets 2 and 10) - merged per Change 7; both positions recorded, neither chosen -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (no statement decides C-001 claim part or C-009)

### Change 8: The raise-the-limits lever, narrowed
- **Status**: Applied
- **Source**: Variant B section 3.5 and Round 2 bullet 8; round2-advocate-A.md section 3 N8; round2-advocate-B.md section 1.1 W3 and section 3 E1
- **Target**: Base section 3.5 and the section 5 INV-C column (replaced); section 6.1 (M3)
- **Before**: raise anchor and anchor2 to 300 and claim to 450 (120 of 124 lines admitted) with "four boundary assertions" rewritten and "about 4 lines in 124 for the re-ask".
- **After**: claim-only raise to 450 (12 of 12 claim-dependent lines on P273 at 450, 11 of 12 at 400), a separate owner decision never part of the default; CO-8 brief change common ground; pin cost per site (2 sites, 3 with `card_convert.py`; quote pin only if the quote limit is also raised); the section 4.3 replay kept as evidence only.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Round 2 N8 and Debate (round2-advocate-B.md section 1.1 W3, section 3 E1, section 6 bullet 8) - merged per Change 8 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Evidence corrections and additions
- **Status**: Applied
- **Source**: Scorer-identified contradictions (`base-selection.md`); round2-advocate-B.md section 3 E1-E5, section 1.1 W1-W2, section 1.2 N2-N3; round2-advocate-A.md section 3 N2-N3; debate points A-001, A-003, X-002, X-003, S-003, U-006, U-007
- **Target**: Base section 4.2 (paragraph after the audit-D table rewritten; new H4 "Second population P273"), 4.3 (reading paragraph), 4.4 (totals paragraph), 4.6 (two rows), section 8 (stall-exposure answer)
- **Before**: "5 of 5 re-asked blocks recorded valid"; "none of the 42 merges where a blocking row survived"; "stall exposure is small"; no second population.
- **After**: four confirmed re-asks of five (one unconfirmed, orchestrator-reported) in 4.4, 4.6 and section 8; in 4.2, 42 merges carry a dropped blocking line and 3 have no blocking row left, so 39 kept a blocking row (marked [RECOMPUTED]); the audit-D "0 of 264 after the cut" labelled as derived from the `flags.tsv` reason text; P273 added as a labelled second population with method line, differences from audit-D (273/90/46/79 against 264/92/49/80; the 9-merge net difference, reported by B as 15 unreconciled, is not reconciled), prefix location (70 of 70), verdict simulation (3 PASS to FAIL, 16 added blocking rows, 13 of 16 already FAIL, no FAIL to PASS), floor results (10 today, 5 tolerant eligibility, 0 with the cut), recovery by policy; A-001 and A-003 stated; the stall-exposure answer withdrawn and replaced with 79 of 855 runs and 10 of 273 merges.
- **Provenance tag**: `<!-- Source: Debate (round2-advocate-B.md section 3 E1-E5, ...) - merged per Change 9 (second population added, labelled) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Measurements, kill lines and tests
- **Status**: Applied
- **Source**: Variant A section 5 (M1-M4) and Round 2 bullets 10-11; Variant B section 6 and Round 2 bullets 9-10; debate points S-004, U-003, U-004
- **Target**: Base section 6, restructured as 6.1 Measurements, 6.2 Tests, 6.3 Kill lines
- **Before**: base M1 (refusal on exactly the 3 merges, none of the other 261), M2 (re-ask across 44 runs), M3 (raised constants 300/450 for anchors), T-B1 to T-B5.
- **After**: M1 conservation, fire-set and cut replay over two frozen populations (fire count 3 without the cut, 0 with it); M2 re-ask on the residual lines only; M3 claim-only admission curve and incidence levers; M4 cost-side re-merge (added); M5 two-judge claim test (added); T-B1 to T-B5 kept with T-B2, T-B3, T-B4 modified; T-A1 to T-A6 added (no-op, boundaries 200/201 and 300/301, idempotence and non-invention, call sites, differential first-pass, v2 loss unit); K1 to K5 as in both advocates' bullets, K1 computed over verbatim fields (75 percent for code or multi-line), K5 denominators 264 and 273 both noted. Numbering note: the plan's "added M1-M4" overlap the base's M1-M3 by content, so they are merged under M1, M2 and M4 and the base ids M1-M3 are kept; M5 is the plan's added M3 (two-judge test).
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 5 (M1-M4) and Debate (...) - merged per Change 10 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: Invariant table
- **Status**: Applied
- **Source**: Variant A section 4; Variant B section 5; debate points S-005, A-004
- **Target**: Base section 5 (INV-C, INV-D, INV-G, INV-I cells replaced; INV-A, INV-B, INV-H, INV-J, INV-K, INV-L cells adjusted for consistency)
- **Before**: INV-C "Kept"; INV-D `dropped` object; INV-G "B excludes that path ... itemise-only there"; INV-I without the `block_ok` note.
- **After**: INV-C "partly endangered" for the cut; INV-D lists `repairs`, `dropped`, `first_pass_state`, `repaired`; INV-G requires the re-ask prompt to hold only the reviewer's own block and errors and grant no tool (T-B5), `--resume` optimisation only; INV-I notes that under Alternative A `block_ok` becomes True for a length-only reviewer and that eligibility is per section 3.3 (C-002 unresolved). Columns renamed "The policy" and "Claim-only raise".
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 4 - merged per Change 11 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 12: The `SKILL.md:343` sentence
- **Status**: Applied
- **Source**: Variant A section 7 point 1; round2-advocate-A.md section 3 N7 and bullet 12; round2-advocate-B.md section 1.1 W6 and bullet 11; debate point X-001
- **Target**: Base section 3.4 "Reflect UC-1 and UC-2" row; section 8 Answer 1 point 1; section 5 INV-K
- **Before**: "The skill's E1 re-ask rule and compliance metric stay as written."
- **After**: Normalize sentences byte-identical (pinned at `tests/cli/reflect/test_shadow_skill_contract.py:229-232`); one added sentence (package parser step shortens location fields in code and records every shortening, the orchestrator still never edits a finding, first-parse compliance reads `first_pass_state`); owner confirms package code is not "the orchestrator", fallback v2 call sites at `repair=False` and v1 `merge` keeps the cut. Round 2.5 INV-019 pointer added; not closed.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 7 point 1 and Debate (...) - merged per Change 12 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 13: Third copy of the constants
- **Status**: Applied
- **Source**: round2-advocate-B.md W7 and bullet 12; Variant A Round 1 weakness 7 (as cited in the plan); debate point C-011
- **Target**: Base section 3.1 "Limits constants" row and section 3.6
- **Before**: `card_convert.py` marked truncation described as "a measurement converter ... not a production path".
- **After**: `card_convert.py` imports the shared constants and keeps its marked claim cut (`text[: MAX_CLAIM - 3] + "..."`, `:200-201`) as a legacy conversion measure, named an explicit exception, reconsidered if the claim switch is turned on; the three production call sites passing `repair=True` rewrite no pin. Round 2.5 INV-022 carried open.
- **Provenance tag**: `<!-- Source: Debate (round2-advocate-B.md section 6 bullet 12) - merged per Change 13 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 14: Strongest objection, restated for the merged position
- **Status**: Applied
- **Source**: Variant A section 7; Variant B section 8; round2-advocate-B.md section 1.3 and C-012 row; round2-advocate-A.md section 1.3 and W3
- **Target**: Base section 8 (restructured); section 4.5 provenance bullet
- **Before**: one objection against B (spends a model call) with five answers.
- **After**: Objection 1 (provenance and principle, C-012) with A's answer kept for the location fields (report file never edited, `report_sha256` recorded, derived copy with `original_sha256`, a drop is also an edit and a larger one, 70 of 70 and 89 of 89, `refs_norm` changed on 0 of 125); the byte-copy objection kept only for a claim cut; Objection 2 (eligibility cost, C-002) quantified on P273; base answer 5 kept with "four confirmed of five"; base answer 4 (degradation to itemise plus refusal) kept; base answers 1 to 3 withdrawn or replaced.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 7 (...) - merged per Change 14 (answer to Objection 1, for the location fields) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 15: Open invariants and unresolved conflicts section
- **Status**: Applied
- **Source**: `invariant-probe.md`; `round2.5-fault-finder-raw.md`; the Convergence Assessment as recorded in `refactor-plan.md` (the debate transcript itself was not read; the 85.7 percent, 24 of 28 figure is taken from the plan)
- **Target**: Base section 9 (last bullet appended) and new section 10 (10.1 unresolved conflicts with both positions, 10.2 owner decisions, 10.3 the 20 UNADDRESSED findings)
- **Before**: section 9 only.
- **After**: section 10 lists C-001 (claim part) and C-009, C-002 and C-012 with both positions, four owner decisions (claim default, reading of `SKILL.md:343`, claim-only raise, kill-line numbers), and every UNADDRESSED finding of the probe by ID, severity, category and one sentence (4 HIGH: INV-001, INV-017, INV-018, INV-023; 12 MEDIUM: INV-002, INV-003, INV-005, INV-006, INV-007, INV-008, INV-010, INV-016, INV-019, INV-024, INV-025, INV-026; 4 LOW: INV-004, INV-011, INV-020, INV-022), each stated as not closed; the 6 ADDRESSED findings named in one line. No fix was added for any of them. Short pointers to the relevant probe ids were added in sections 3.2, 3.3, 3.4, 3.6 and 5 (pointers only).
- **Provenance tag**: `<!-- Source: Debate (the Convergence Assessment of debate-transcript.md as recorded in refactor-plan.md Change 15; invariant-probe.md; round2.5-fault-finder-raw.md) - merged per Change 15 (new section; transparency only) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 16: Reach: v2 loss unit, PR and rf-qa rows, and base rows made stale by Change 1
- **Status**: Applied
- **Source**: debate points C-003, C-014, X-003; Variant A section 2 item 7 and section 6; Variant B sections 7 and 2
- **Target**: Base section 3.4 (Reflect row, PR row), section 7, section 2 table rows (placement outcome, INV-003, INV-004, INV-014 wording, INV-022, last row)
- **Before**: "INV-003 does not arise", "answers it with the re-ask ... not a repair", "B reads the merged text as the itemise branch", "a repair placed in callers is not needed", "not a cut quote".
- **After**: (a) v2 loss unit: the cut removes it only for the length share; claim or non-length faults still cost the reviewer unless the re-ask works; "4 of 92" is a v1 floor. (b) PR and rf-qa: a `quote` prefix passes the `verify_cmd.py:68-72` substring test, per-profile quote limit, stateless in-session re-ask, code corpus required. (c) Section 2: INV-003 answered by the `repair=False` keyword; INV-004 holds because the cut sits in `findings_v2.parse_block`; "normalise-or-itemise" read as both; INV-022 satisfied for verbatim anchors with the unlocated and ambiguous cases carried in section 10. Round 2.5 INV-024 carried open.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 2 item 7 and Section 6 - merged per Change 16 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1 (the title) after the three provenance comment lines; H2 sections 1 to 10 in order; H3 subsections 3.1-3.6, 4.1-4.6, 6.1-6.3 and 10.1-10.3; one H4 ("Second population P273") under 4.2. No level gaps and no orphaned subsections. 30 heading lines in total.
- Section ordering: PASS. The base's sections 1 to 9 keep their numbers and order; section 10 (Change 15) is last; section 6 gained 6.1 to 6.3 and section 3.5 and 3.6 were retitled (no reference uses a title).
- Document flow: PASS. Tables kept as tables; the one base table cell that contained unescaped pipes (the `contract.py` grep pattern in 4.1) was escaped; no table cell in the merged file contains an unescaped pipe (grep over table rows returned no match).
- The file ends with "Status: Complete" and does not contain the end-of-log marker.

### Internal References
- Method: grep of every "section N", "sections N and M" and "(section N)" in the merged file, separating internal references from references to the advocates' round files (for example "round2-advocate-B.md section 3 E4"), which point outside the document and were not counted.
- Distinct internal targets used: 1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3, 4.4, 4.5, 5, 6.1, 6.2, 6.3, 7, 8, 9, 10, plus the named items M2, K1, K2, K4, T-B5, INV-A to INV-N and Answer 1 point 4 in section 8. Counted by distinct target, not by occurrence.
- Resolved: all distinct targets exist. Broken: 0.
- Id namespaces: the C-01 ids of section 2, INV-A to INV-N of section 5 and the Round 2.5 ids INV-001 to INV-026 are three separate numberings; the merged file says so in section 2 and in section 10. Each id of the section 10.3 table was checked against the probe's list (20 UNADDRESSED: 4 HIGH, 12 MEDIUM, 4 LOW; the six ADDRESSED ids named once).

### Contradiction Re-Scan
- Scan A (removed wording from the plan's "Changes NOT Being Made" table and the executor brief): searched the merged file for "touches no field the limits", "exact prefix", "recorded as attempt 2", "at most 4 residual", "at most 4 lines", "5 of 5", "stall exposure is small", "four boundary", "re-ask all 44", "none of the 42", "44 reviewer runs": 0 matches. Also 0 matches for the unresolved-marker text and for the end-of-log marker.
- Scan B (stale base wording that Change 1 makes false): searched for "B-core", "B-raise", "never a truncation", "No truncation step", "does not arise", "itemise branch", "honest by construction": 0 matches in the merged text.
- Scan C (statements that decide an unresolved point): read sections 1, 3.3, 3.6, 5, 6, 8 and 10 for any sentence that chooses between the two claim positions (C-001 claim part, C-009), the two eligibility alternatives (C-002) or the provenance position for a claim cut (C-012). None remains after the fix in D1.
- New contradictions introduced: 0 after the defects below were fixed. Defects found and fixed during validation:
  - D1. Change 1's integration text says "no other field is cut by default". Left as written it would decide the claim point that the same sentence calls unresolved. The merged text says instead that no field other than the three location fields is cut by "the part of the policy both positions share" and points to sections 3.6 and 10 (sections 1 and 3.6).
  - D2. The refusal name was written `dropped-blocking` in the base and `dropped_blocking` in the debate's object. The merged text uses `dropped_blocking` for the refusal key and the reason; the prose phrase "the dropped-blocking refusal" is kept as a noun phrase.
  - D3. Base statements that the plan's rows did not name but that Changes 1, 4 and 16 make false were corrected in the plan's own terms: section 2 INV-014 row ("B's remedy is the re-ask before the merge"); section 2 first row (the debate reference N-B3 and "a repair placed in callers is not needed"); section 3.2 fallback ("never a truncation"); section 3.5 ("about 4 lines in 124 for the re-ask"); section 5 INV-G ("itemise-only there" for the headless resume path); section 5 INV-J and sections 3.4 and 7 ("continuation" now "second prompt", the Agent path still continues the same agent); section 7 (the base's over-limit-quote-as-re-ask design removed because the quote is now cut).
  - D4. Duplicate subsection headings 10.2 and 10.3 and leftover stub placeholders were created by an edit and removed before this validation was run.
  - D5. Provenance comments quoted removed base wording (for example the "none of the 42 merges" figure); they were reworded so the removed wording does not survive anywhere in the file.
  - D6. Two wording slips in the first draft ("both inside both parsers", "next row but one") were corrected.
- Remaining inconsistencies noted, not defects of the plan: the base cites `cluster.py:256-257` (sections 2 and 4.1) and the plan cites `cluster.py:255-257` (section 3.4) for the same v2 loss unit; both are within the same function and both were left as written. The advocates cite the pinned test lines as 229-232 (A) and 230-232 (B); the plan's 229-232 was used and matches the file.

### Items to flag to the orchestrator
- The convergence figure in section 10 (85.7 percent, 24 of 28) comes from the plan; the debate transcript was not read.
- Confidence percentages of the advocates' final tables (C-001, C-002, C-009, C-012) are quoted only where the plan quotes them; the plan's "C-014 63 percent" was not carried.
- `[DEBATE-ESTABLISHED]` is used for statements that rest on the P273 replay and N1-N9; the merge re-ran none of them. `[RECOMPUTED]` is used once (42 minus 3 = 39).

## Summary

- Total changes planned: 16
- Successfully applied: 16
- Failed: 0
- Skipped: 0
- Items of the "Changes NOT Being Made" table applied: 0 (documentation only; none of the removed wording survives, Scan A)
- Unresolved points carried as recorded, not chosen: C-001 (claim part) and C-009, C-002, C-012 (sections 3.3, 3.6, 8 and 10.1)
- Round 2.5 findings listed in section 10.3 as not closed: 20 UNADDRESSED (4 HIGH, 12 MEDIUM, 4 LOW)
- Post-merge validation: PASS (structural integrity PASS, internal references 0 broken, new contradictions 0 after the fixes D1 to D6)
- Pipeline-level status (convergence blocked by invariants, unresolved conflicts) is the orchestrator's to set; this log reports only that the merge was executed and validated.

END-OF-MERGE-LOG
