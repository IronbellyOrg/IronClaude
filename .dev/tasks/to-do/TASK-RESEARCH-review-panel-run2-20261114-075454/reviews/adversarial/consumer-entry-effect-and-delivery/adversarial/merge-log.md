# Merge Execution Log

## Metadata
- Base: Variant A (Proposal A; `adversarial/variant-1-original.md`)
- Executor: merge-executor (slot C-05, consumer-entry-effect-and-delivery)
- Changes applied: 16 of 16
- Status: success
- Timestamp: 2026-11-14
- Output: `.../consumer-entry-effect-and-delivery/merged-output.md` (38 `<!-- Source: ... -->` annotations plus the 3-line provenance header)
- Process note: the merged file was written in one Write call. No Edit was needed after validation.

## Changes Applied

### Change 1: Three separable parts
- Status: Applied
- Source: Variant B Sec 1 and Sec 8 item 4; debate S-002 (B, 88%)
- Target: Merged Section 1 (new 1.1 Entry, 1.2 Effect, 1.3 Delivery, 1.4 Which part carries which argument)
- Before: One paragraph bundling entry, effect and delivery.
- After: Headline kept; three labelled parts with C-001 (A, 90%), C-002 (Hybrid, 90%), C-003 (A, 93%); B's argument map in 1.4. Top-of-document merged resolution paragraph added.
- Provenance tag: `Base (original, modified) - restructured ... per Change 1`; `Variant B (Proposal B), Section 1 and Section 8 item 4 - merged per Change #1`; `Base (original)` for 1.3
- Validation: structure OK (H2 then H3); references resolve; no contradiction.

### Change 2: Stage 10.5 effect corrected (INV-001, INV-002)
- Status: Applied
- Source: invariant-probe INV-001, INV-002; Proposal A Sec 3 item 2; Proposal B E2
- Target: Merged Sections 1.2, 2 (Wave 4 and Stage 10.5 rows), 3.1 item 2, 8 objection 1
- Before: "advisory at generation time"; "one blocking edge ... a needs_human_decision item".
- After: Wave 4 advisory with no halt path; Stage 10.5 advisory-blocking (bundle ships, halt, unattended `blocked`, `--remediate` write path with nesting); engine-switch effect marked unmeasured and open.
- Provenance tag: `Debate (invariant-probe.md) - merged per Change #2`; `Base (original, modified) - ... corrected for Stage 10.5 per Change 2`
- Validation: structure OK; references OK; the old wording survives only inside quoted objection text and the Section 10 register (intended).

### Change 3: Reach part
- Status: Applied
- Source: Proposal B E4; round1-advocate-B strength 1; round2-advocate-A responses 1; round2-advocate-B (i); INV-003, INV-005, INV-006; C-004 (Hybrid, 88%)
- Target: New Section 3a (3a.1 chain, 3a.2 unknowns, 3a.3 remedy); Section 8 objection 2 modified
- Before: Quick-depth only limit (item 7, objection 2).
- After: Seven-step reach chain, "unsized" statement with B's n = 8 free check, remedy conditions INV-003, INV-004, INV-006 open.
- Provenance tag: `Variant B (Proposal B), Section 4 E4 - merged per Change #3`; `Debate (...) - merged per Change #3`
- Validation: structure OK; references OK; no contradiction. Every statement traces to R2A, R2B or the probe.

### Change 4: Invariant table with per-row verdicts
- Status: Applied
- Source: Proposal B Sec 5; S-003 (B, 85%); INV-007, INV-008, INV-012
- Target: Merged Section 5
- Before: "Preserved" column with a closing paragraph.
- After: One table, Keeps / Keeps with a cost / Endangers. Order: INV-M, INV-B, INV-N, INV-K, INV-J, then INV-A, INV-C and INV-D, INV-E, INV-F, INV-G, INV-H, INV-I, INV-L. INV-J (Endangers for a later revise loop) and INV-G (plugin reviewer agent must be read-only) carried. INV-K corrected per INV-012; the "fence test must be changed" wording replaced (Section 3.1 item 8).
- Provenance tag: `Variant B (Proposal B), Section 5 - merged per Change #4`; `Base (original, modified) - ...`
- Validation: structure OK; references OK; no contradiction.

### Change 5: Return-contract statement
- Status: Applied
- Source: R2A item (ii); R2B concession 1; Proposal B E8; INV-007, INV-008, INV-009, INV-014 F3
- Target: Merged Section 2 (reflect UC-1 and Wave 4 rows), Section 5 INV-M row, Section 3.1 item 3
- Before: "reaches consumers only as `status`, `coverage_pct`, `tier_reached`"; "four readers".
- After: Consumers also read `needs_human_decision`, `unmapped_requirements`, `run_id`, `report_path`; two of three fields fixed before the engine is read; map unpinned (INV-011); short or refused panel stays in the closed enum (INV-009); "at least the four skill readers, one closed-enum validator and the tests" (INV-008); additive keys at "1.1" safe; the 1.1 to 1.2 bump wrong (Sections 9a, 10).
- Provenance tag: `Base (original, modified) - ...`
- Validation: structure OK; references OK; the old counts appear only in the Section 10 register and the INV-008 probe row (quoted).

### Change 6: Engine-switch statement
- Status: Applied
- Source: R2A item (v); INV-008, INV-010, INV-011, INV-012; Proposal B E5, E13
- Target: Merged Section 3.1 item 8; Section 8 objection 3
- Before: "one controlled change at reflect's default".
- After: Prose edit in three places, no staged selector, flips every UC-1 caller, shadow-first doubles Tier-2 reviewer spend, reflect-owned tests change at Stage 3, contract-compat test necessary not sufficient; gate kept (replay, contract-compat test, headless smoke run).
- Provenance tag: `Debate (invariant-probe.md) - merged per Change #6`; `Base (original, modified) - ...`
- Validation: structure OK; references OK; no contradiction.

### Change 7: Lens statement
- Status: Applied
- Source: Proposal B E7; R2A concession 6; R2B (v); C-007 (Hybrid, 88%)
- Target: Merged Section 2 (new row "Lens for Wave 4 and Stage 10.5")
- Before: No lens row.
- After: `reflect-pre` lens at Wave 4 and Stage 10.5; five Stage 7 dimensions only for a Stage 7 feed, net-new code (`findings_v2.py:36`; no `tasklist` or `effect` match in `cli/review`). Tags state whose check it is.
- Provenance tag: `Variant B (Proposal B), Section 4 E7 - lens row merged per Change #7`
- Validation: structure OK (table intact); references OK; no contradiction.

### Change 8: Relation to Stages 6-10
- Status: Applied
- Source: Proposal B E3; R2A (iv); R2B (iii); X-001 (Hybrid, 90%)
- Target: Merged Section 2 (Stages 6-10 row), Section 8 objection 1
- Before: "a direct call would add a new revise loop"; Stages 6-10 "out of scope".
- After: Blocking already exists in Stages 8-10 (`:1604-1615`); a call-site direct call adds no loop; a Stage 7 feed swap changes the block's evidence base, touches P2 pins (`tests/tasklist/test_tasklist_cli.py:568-580`) and halt strings, and is a separate later module.
- Provenance tag: `Debate (round2-advocate-A.md) - Stages 6-10 row merged per Change #8`
- Validation: structure OK; references OK; no contradiction.

### Change 9: Wave 4 and "door open"
- Status: Applied
- Source: Proposal B Sec 3 (entry shape); B E1; R2A bullet 5; R2B amendments to bullets 5, 8, 9; INV-014 F3
- Target: Merged Section 2 (Wave 4 row) and new Section 9a
- Before: No later-module section.
- After: Eight conditions (additive keys at "1.1"; `artifacts` rule and `EXPECTED_NESTING` / `UNATTENDED_EXPECT` by hand; eval allow-list and staging; parity test per plugin file; Wave 4 `plan-review` edits both trees; own replay and smoke run; blocking feed must not fail open; costs B carried), stated as conditions, not a plan.
- Provenance tag: `Variant B (Proposal B), Section 3 - merged per Change #9`; `Debate (...) - merged per Change #9`
- Validation: structure OK; references OK. The two source line numbers for the Stage 7 some-versus-zero gate (`:1608` from A R2, `:1702` from B R1) disagree; both are cited with attribution rather than one being chosen.

### Change 10: Plugin delivery
- Status: Applied
- Source: Proposal B E9 and Sec 8 third objection; R2B (iv); C-003 (A, 93%), A-006 (B, 90%)
- Target: Merged Section 3.1 item 9; Section 8 objection 4
- Before: "cannot work without `sc-reflect-protocol`".
- After: "No panel-only copy" kept; three-case account; CLI availability and `verify-sync` coverage unchecked; parity test per added file; the "cannot work" wording withdrawn.
- Provenance tag: `Variant B (Proposal B), Section 8 third objection - merged per Change #10`; `Base (original, modified) - ...`
- Validation: structure OK; references OK; no contradiction.

### Change 11: Measurement
- Status: Applied
- Source: Proposal A Sec 6; Proposal B Sec 6; R2A bullet 8; R2B amendments to bullets 4 and 8; INV-005, INV-006, INV-013
- Target: Merged Section 6 (6.1 to 6.6)
- Before: Four base items.
- After: Two-arm replay (arm R a real Wave 4 or Stage 10.5 call; arm D the E2 path; loop and cost columns), reach share, contract-compat test, non-regression plus smoke run, free check, and "Instrument gaps (open)" with six items (no GT scorer; aggregator blind spots; harness denies Bash, Agent, Task, `mcp__*`; no engine selector; denominator unset; no numeric threshold).
- Provenance tag: three `<!-- Source: ... -->` lines before Section 6 (Base modified, Variant B Section 6, Debate)
- Validation: structure OK; references OK. The section states that the measurement has no working instrument (INV-013).

### Change 12: Dependence on slots and later consumers
- Status: Applied
- Source: Proposal A Sec 4; Proposal B Sec 2 and Sec 7; C-010 (A, 94%), C-012 (Hybrid, 82%)
- Target: Merged Section 4 (reverse-view paragraph) and Section 7
- Before: One condition per slot; A-only effect on PR review and rf-qa.
- After: Slot text kept with slot prefixes (C-01 INV-020, C-03 INV-006 and INV-007 and so on) to avoid clashing with probe ids; reverse view for a later direct module (C-02 INV-001/002/003, C-03 INV-007); module-declared effect as the rule for later consumers, none added here.
- Provenance tag: `Variant B (Proposal B), Section 2 - merged per Change #12`; `Variant B (Proposal B), Section 7 - merged per Change #12`
- Validation: structure OK; references OK; no contradiction.

### Change 13: Shared assumptions
- Status: Applied
- Source: diff-analysis "Shared Assumptions"; both Round 2 "Shared assumption responses"
- Target: New Section 9b
- Before: None.
- After: Table A-002 Neither (88%), A-003 Hybrid (82%), A-004 Hybrid (88%), A-005 Neither (90%), A-006 B (90%); A-001 and A-007 noted as STATED and not scored.
- Provenance tag: `Debate (diff-analysis.md, round2-advocate-A.md, round2-advocate-B.md) - merged per Change #13`
- Validation: structure OK; references OK; A-004 row words the Stage 10.5 halt as the exception to fail-open.

### Change 14: Counter-evidence
- Status: Applied
- Source: Proposal B E11, E12, E13
- Target: Merged Section 3.2 (items 11 to 13)
- Before: Items 1 to 10 only.
- After: Three appended items with B's tags kept ([RECOMPUTED], [UNVERIFIED]). One reference ("FX-11") was dropped and the sentence kept as "no multi-round ledger exists".
- Provenance tag: `Variant B (Proposal B), Section 4 E11, E12 and E13 - merged per Change #14`
- Validation: structure OK; references OK; no contradiction.

### Change 15: Withdrawn and corrected claims
- Status: Applied
- Source: round1 and round2 advocate concessions; probe "Claims ... FALSE or unsupported"
- Target: New Section 10
- Before: None.
- After: 21-row table (claim, origin, disposition) covering every item listed in the plan plus probe falsities 1 to 6 and B's R2 withdrawal of "B's seam is needed for the loop".
- Provenance tag: `Debate (round1-advocate-A.md, round1-advocate-B.md, round2-advocate-A.md, round2-advocate-B.md, invariant-probe.md) - merged per Change #15`
- Validation: structure OK; references OK. The withdrawn texts are quoted only as withdrawn.

### Change 16: Open conditions from the probe
- Status: Applied
- Source: `invariant-probe.md`; status BLOCKED_BY_INVARIANTS; R2A bullet 10
- Target: New Section 11 (11.1 status, 11.2 table, 11.3 holds-while and reopen, 11.4 not checked)
- Before: None.
- After: All 15 items INV-001 to INV-015 with status and severity as in the probe (3 ADDRESSED: INV-009 LOW, INV-012 MEDIUM, INV-015 LOW; 12 UNADDRESSED: 7 HIGH, 5 MEDIUM). Holds-while: C-01 to C-03 stand. Reopen: replay shows the direct path catches materially more blocking GT items per cost not explained by depth routing; owner chooses plugin parity; blocking GT items sit in phases that never reach the panel. No convergence claimed beyond the debate; orchestrator's sycophancy note carried.
- Provenance tag: `Debate (invariant-probe.md) - merged per Change #16`; `Debate (round2-advocate-A.md) - merged per Change #16`
- Validation: structure OK; references OK; severity counts re-checked against the probe summary.

## Post-Merge Validation

### Structural Integrity
- (a) PASS. Read-back and Grep of `^#{1,6} ` show one H1 (line 5, preceded only by HTML comments), then H2 sections 1, 2, 3, 3a, 4, 5, 6, 7, 8, 9, 9a, 9b, 10, 11 in plan order. H3 appear only under an H2 (1.1-1.4, 3.1-3.2, 3a.1-3a.3, 6.1-6.6, Objection 1-4, 11.1-11.4). No H4 and no level gaps.

### Internal References
- Total "Section N" references found: 80. Excluded: 12 inside provenance comments that cite sections of Proposal B (the protocol's required `Variant B (Proposal B), Section <ref>` form), which point at the source paper, not the merged file. Internal references checked: 68. Resolved: 68. Broken: 0.
- Targets checked: 1, 1.1, 1.2, 2, 3 (items 1, 3, 8, 9), 3a, 3a.1, 3a.3, 4, 5, 6, 6.1, 6.2, 6.3, 6.4, 6.6, 7, 8 (objections 1, 3, 4), 9a, 9b, 10, 11. All exist.
- Probe ids INV-001 to INV-015: each is defined in the Section 11.2 table and referenced by bare id elsewhere. Earlier-slot ids carry a slot prefix (C-01 INV-020, C-02 INV-001/002/003, C-03 INV-006/007).

### Contradiction Re-Scan
- Greps for "four readers", "advisory at Stage 10.5", "advisory at generation", "only as `status`", "zero edits", "must be changed", "1.1 to 1.2", "cannot work without" and "new revise loop" found hits only in these places: quoted objection text in Section 8 objection 1 (the opening of the objection, answered right below it); the Section 10 register and the INV-007 and INV-008 probe rows (claims quoted as withdrawn); Section 3.1 items 1 and 8, Section 8 objections 1 and 4 and Section 9a item 1 (each states the withdrawal beside the quote). Intended, not contradictions.
- New contradictions introduced: none found.
- One tension noted, not a contradiction: Proposal B conceded Stage 10.5 is fenced (no revise loop), and the probe shows Stage 10.5 still halts. Both are stated: no revise loop (`:1621-1623`) and advisory-blocking (Sections 1.2, 10 item 17).
- Two source line citations for the Stage 7 some-versus-zero gate differ; both are cited with attribution (Section 9a item 7).
- No fixes were needed.

### Forbidden-path grep
- (d) PASS. `TASK-RESEARCH-review-panel-unify-20261113-155942` and `REVIEW-PANEL-UNIFY-RUN2-QUEUED`: 0 hits in `merged-output.md`. Neither variant contains them; the strings appear only in `refactor-plan.md` as a rule and were not carried over.

### Emoji grep
- (e) PASS. A grep for any non-ASCII character (`[^\x00-\x7F]`) returned 0 matches, so no emoji-like characters, em dashes or en dashes are present.

## Summary
- Planned changes: 16
- Applied: 16
- Failed: 0
- Skipped: 0
- Validation: PASS (structure, references, contradiction re-scan, forbidden strings, emoji)
- Caveat: the merged file states the conditional status BLOCKED_BY_INVARIANTS and does not claim more than the debate produced. No test was run by this merge.
- Result: PASS
