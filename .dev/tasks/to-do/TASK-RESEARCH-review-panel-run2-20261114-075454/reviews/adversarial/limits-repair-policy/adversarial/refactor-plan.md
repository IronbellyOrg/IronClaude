# Refactoring Plan: Merge into Base (Variant B, Proposal B)

## Overview
- Base: Variant B (Proposal B; `variant-2-original.md`; default model, default persona). Combined score 0.9474 against 0.8466 for Variant A (`base-selection.md`; margin 10.08 points, no tiebreaker).
- Incorporating strengths from: Variant A (Proposal A; `variant-1-original.md`).
- Planned changes: 16. Changes 1-14 and 16 change or add design text and evidence; Change 15 only records what the debate left open. Change 16 was added after the independent plan review (`plan-review.md`) found converged debate points (C-003, C-014, X-003) and stale base rows that no earlier change targeted.
- Risk level: Medium overall. Changes 1 and 6 are High (Change 1 reverses the base's headline position; Change 6 sits on an unresolved point); Changes 2, 3, 4, 5, 7 and 12 are Medium; the rest are Low.
- Source of every change: the debate itself (`debate-transcript.md`: Round 1, Round 2 final tables, both advocates' 12-bullet resolution texts, Round 2.5 probe) and `base-selection.md`. Nothing in this plan is a conclusion the debate did not reach. Where the advocates' final positions differ (C-001, C-002, C-009, C-012), the merged text states both positions and does not choose (Changes 6, 7 and 15).
- Edit verbs used below follow the template: replace, append, insert, restructure.
- Merged file name: `merged-output.md` in the output folder (`.../reviews/adversarial/limits-repair-policy/merged-output.md`), as for slots C-01 to C-03. It keeps the base's nine-section layout and adds one section 10.

## Planned Changes

### Change 1: Cut the three location fields in code, behind a keyword (from Variant A)
- **Source**: Variant A section 1 and section 2 items 1-2; debate points C-001 (by field), S-001, S-002; both advocates' final bullet 1.
- **Target**: Base section 1 (position paragraph) and section 3.6 "What B does not do" (replace the "No truncation step, no normaliser ... no repair-aware parse" sentence) (restructure).
- **Rationale**: Both Round 2 final tables name Hybrid on S-001 and S-002 (77% and 79%). The two final bullet-1 texts are identical for the three location fields (`anchor`, `anchor2`, citation `quote`) and differ on the claim (Variant A bullet 1 also cuts `claim` to 297 plus `...`; Variant B bullet 2 cuts no other field); that difference is Change 7. Variant B's advocate moved from "no edit by default" to the cut of the location fields because of the replay and the second-population run (70 of 70 over-limit anchor and anchor2 fields that occur verbatim keep a unique same-span prefix; B's own replay 89 of 89), no v1 vehicle for a re-ask (`merge_cmd.py:99-118`), and 10 of 273 merges below the C-03 floor under a no-edit rule (Round 2 B, W1 and E4). Variant A's advocate kept the claim cut as an option behind a kill line (K2).
- **Integration point**: New text, in this order. `parse_block(text, *, repair=False)` in both parsers; the production call sites `ledger.py:128`, `cluster_cmd.py:151` and `verify_cmd.py:133` pass `repair=True`, with the v2 sites (`cluster_cmd.py`, `verify_cmd.py`) subject to the owner reading of `SKILL.md:343` in Change 12; a test asserts every production call site passes the keyword explicitly and that the default stays `False`. One pure `repair_line(obj)` in the C-01 limits module cuts `anchor`, `anchor2` and a citation `quote` to the first 200 characters of their whitespace-flattened form, before `_check_finding` and `check_finding`; it touches no `prior` line; the report file is never edited; direct-parser pins (`test_review_findings.py:113,117`, `test_review_findings_v2.py:200,241`) stay unmodified. State the position as: the three location fields are cut in code and recorded; no other field is cut by default (the claim is unresolved C-001 and C-009, see Change 7); everything dropped is itemised.
- **Evidence limit to state in the text**: the 70 of 70 and 89 of 89 results cover `anchor` and `anchor2` on single-line tasklist rows only. The `quote` cut has no location measurement (it rests on the substring test at `verify_cmd.py:68-72`, C-014 63%), and no PR-code or multi-line corpus exists.
- **Risk**: High. It reverses the base's headline position (INV-C goes from "Kept" to "partly endangered", Change 11) and rests on the unrun M1/M2 measurements (Change 10). Round 2.5 INV-017 (HIGH, a shorter prefix that matches more than one place) is not closed by this text and is carried open (Change 15).

### Change 2: One shared record for cuts and drops (from Variant A, merged with the base's classifier)
- **Source**: Variant B section 3.1 "Line classifier and drop record" (base) plus Variant A section 2 item 3 (`repairs`); debate points S-002, U-009, C-010, C-012.
- **Target**: Base section 3.1 table, rows "Line classifier and drop record" and "Result shape" (insert).
- **Rationale**: Both final tables: S-002 Hybrid, C-010 Hybrid; both bullet 2: one record per cut and per residual drop.
- **Integration point**: The record becomes `{line, finding_id, blocking_state (true, false, unknown), rule, field, original_chars, kept_chars, original_sha256}`, never reviewer text (INV-H); `repairs` and `dropped` are additive keys beside the unchanged `ok`/`state`/`errors`; the per-block conservation property (non-blank lines = kept + priors + dropped) stays; the merged report's `### Lx` block prints "shortened from N" next to the anchor status (no new table column). `refs_changed` is recorded when `refs_norm(original) != refs_norm(repaired)`; the copy-to-`refs` rule is not adopted (see "Changes NOT Being Made").
- **Risk**: Medium. Round 2.5 INV-005 (`blocking_state` for CRITICAL with `blocking: false`), INV-007 (`blocking_state` of a dropped `prior` line), INV-008 (first-fault-only messages) and INV-011 (unit of `repaired_lines_rate`) are not addressed by the debate text and are carried open (Change 15).

### Change 3: First-pass state carrier (from Variant A)
- **Source**: Variant A section 2 item 8 and Round 2 N6; debate points C-013, X-004, A-005, U-004.
- **Target**: Base section 3.1 (new row "First-pass carrier"), section 5 INV-A and INV-L rows, section 6 (new test) (insert).
- **Rationale**: Both final tables: C-013 Hybrid (76%), X-004 Hybrid (82%), A-005 Hybrid (76%). B's Round 1 claim that its metric is "honest by construction" holds only for uncut fields; A's derivation is exact because the cut fires only on a field the unrepaired parse rejects.
- **Integration point**: The parse result gains `first_pass_state` (`state` unless `complete`, else `invalid` when `repairs` is non-empty); `cluster_cmd.py:155-163` and `verify_cmd.py:136-138` emit `first_pass_state` and `repairs` beside the unchanged `state`; `findings_block_compliance_rate` is the share of cards whose `first_pass_state` is `complete`; a differential test against a `repair=False` parse must show zero mismatches; `repaired_lines_rate` and `dropped_lines_rate` per model are reported next to it. State that the shadow-mode safety argument (A-005) holds only while shadow lasts unless `first_pass_state` is carried.
- **Risk**: Medium. Round 2.5 INV-002 (a third carrier: the manifest `completion` value) and INV-004 (no policy tag on ledger entries and telemetry) are not addressed and are carried open.

### Change 4: Re-ask trigger, transport and record (from Variant A, constrained by both advocates' Round 2 evidence)
- **Source**: Variant A section 2 item 6, Round 2 N1; Variant B section 3.2 (base); debate points C-005, C-006, U-005, A-006, X-002, X-003.
- **Target**: Base section 3.2 bullet 2 (trigger) and the transport and record bullets, and section 3.3 bullets 2-3 (restructure).
- **Rationale**: Both final tables: C-005 Hybrid, C-006 Hybrid, A-006 Hybrid (REJECT the unconditional form), X-002 Neither. B's Round 1 trigger (re-ask for 44 reviewer runs before the merge) had no v1 vehicle: no command parses a v1 block without merging, `merge_round` refuses a second merge of the same round (`ledger.py:114-118`), a refused merge writes nothing (`merge_cmd.py:109-116`).
- **Integration point**: Re-ask only for what is still invalid after the cut. v1 (spec loop): the trigger is a refusal (the dropped-blocking refusal of Change 5 or the C-03 quorum refusal); the coordinator re-asks the named reviewer and re-runs `merge` with the replacement report, whose `report_sha256` is in that round's entry; `blocking: false` drops are itemised and not re-asked in v1. Reflect: the E1 rule (an invalid block gets one bounded re-ask) plus B's amendment (an invalid block that carries a `prior` line is re-asked too); attempt 2 is recorded before the `collected` commit and only while the earlier attempt is not `complete` (`manifest.py:371-383`); v1 has no manifest. The prompt is stateless by default: the original brief, the reviewer's own block, the parser's per-line errors, whole block returned; no other reviewer's content, no new tool grant; `--resume` is an optimisation only. Record shape belongs to C-08. A transport that cannot re-ask degrades to itemise plus the refusal. State the recovery evidence as four confirmed re-asks of five (Agent path, one length cause); no recovery rate exists for gateway models (X-002).
- **Risk**: Medium. Round 2.5 INV-018 (HIGH: in reflect, `cluster_cmd`/`verify_cmd` run at step 6 after the `collected` commit at steps 3-4, so the re-ask and attempt-2 record cannot be driven from the carrier as written) and INV-003 (a v1 refusal-driven re-ask leaves no ledger trace, so K4 and K5 are not measurable live) are not addressed by the debate and are carried open.

### Change 5: Dropped-blocking refusal, implementation constraints (from both advocates' Round 2)
- **Source**: Variant B section 3.3 (base); Variant A Round 2 N5; debate points C-004, U-008.
- **Target**: Base section 3.3 (replace the firing statement and add the constraints).
- **Rationale**: Both final tables: C-004 Variant 2 (79%). After the cut it fires on 0 of 264 (audit-D, derived from the `flags.tsv` reason text, A N2, not re-executed) and 0 of 273 (executed on P273, B E4), so it is insurance for what the cut cannot reach (bad severity, bad refs, bad JSON, non-boolean `blocking`); the base text said "3 of 264", which holds only without the cut.
- **Integration point**: Firing condition: the derived verdict would be PASS and an unacknowledged dropped line has `blocking_state` `true` or `unknown`. The check runs at the end of `merge_round`, after the quorum check, on a working copy swapped in place on success (pins `test_review_ledger.py:352-361,373`); it reuses C-03's refusal subtype and exit 12 with `{"refusal": "dropped_blocking", reviewers, dropped}`; the ledger file is unchanged; an owner-and-reason acknowledgement option on `merge` lifts it, is recorded in the round entry and listed in the merged report; no refusal when a blocking row survives (the dropped ids are printed). Restate the fire counts as "3 of 264 without the cut, 0 with it". State the recorded price (B Round 2 N1): in v1 a lost blocking line is never recovered in a merge that succeeds with another blocking row standing (36 of the 39 merges that carry a dropped blocking line on P273); it is itemised and printed only.
- **Risk**: Medium. Round 2.5 INV-001 (HIGH: the rule sees only this round's drops; a lost blocking line in a FAIL round can be forgotten by a later passing round), INV-006 (acknowledgement not bound to item ids), INV-020 (two refusals can occur in sequence) and INV-026 (a measured fire rate of zero does not exercise the code path) are not addressed and are carried open.

### Change 6: Eligibility for clearing and quorum (unresolved C-002: both positions recorded)
- **Source**: Variant B Round 2 final bullet 5; Variant A Round 2 final bullet 6; debate points C-002, A-004.
- **Target**: Base section 2 (C-02 row) and section 3.3 bullet 2 (replace the sentence "because its `block_ok` is False ... does not count toward clearing"), plus section 10 "Unresolved conflicts" (insert).
- **Rationale**: Not resolved. A: Variant 1 (80%): `ok`/`complete` stays the parser's verdict on the repaired lines. B: Hybrid (74%): a derived eligibility. Both agree `ok`/`state` stay the parser verdict on the cut lines and that `repaired` and `dropped` counts are recorded beside `block_ok`. Both quantify the same cost: today's bare `ok` puts 10 of 273 merges (B) or at least 7 of 264 (A, three-reviewer panels only) below the C-03 floor.
- **Integration point**: Replace the base's `block_ok False` sentence with two stated alternatives and no choice. Alternative B (the base-side wording, B bullet 5): a reviewer counts for clearing (C-02 B2) and the floor (C-03) iff it has no block-level fault, no non-length drop on a `true` or `unknown` line, and no unresolved dropped line with `blocking_state` `true` or `unknown`; dropped `blocking: false` lines do not disqualify; no `repaired == 0` knob (B). Alternative A (A bullet 6): `block_ok` is the real parser verdict on the repaired lines (a length-only block is `ok`/`complete`; any residual fault is False), with `repaired` and `dropped` recorded, and C-03 may count only `repaired == 0` blocks for its floor as a recorded parameter, default off. Section 10 states that the debate did not settle which applies.
- **Risk**: High. C-02 and C-03 outcomes depend on it. Round 2.5 INV-005 and INV-007 bear on the `blocking_state` inputs to either alternative.

### Change 7: Claim field (unresolved C-001 and C-009: both positions and both K2 forms recorded)
- **Source**: Variant B Round 2 section 1.3, bullets 2 and 10 (K2); Variant A Round 2 section 1.3, bullets 1 and 11 (K2); debate points C-001 (claim part), C-009, C-012, C-010.
- **Target**: Base section 3.6 and section 8 (replace and restructure); section 10 "Unresolved conflicts" (insert).
- **Rationale**: Not resolved. A: Hybrid (62%): cut the claim to 297 plus `...` with a marker, a "shortened from N" row note and `original_sha256`, kept unless the blind two-judge test K2 fails; the evidence on A's side: with an anchors-only cut, 2 merges sit below the C-03 floor and 15 merges have a bad block against 4 with the claim cut, and 12 dropped lines (8 blocking) have a claim over 300 (B Round 2 E3, E4, section 1.3 (i)). B: Variant 2 (76%): no claim cut by default because anchors-only and cut-all give identical verdicts on all 273 merges, a claim limit of 450 with no claim cut reproduces cut-all, and claim meaning is unmeasured by anyone.
- **Integration point**: State both positions side by side with the P273 evidence above. State K2 in both forms: A bullet 11, the claim cut stands unless more than 20 percent of blocking claims are judged by both judges to lose a decision-relevant clause (falsifier of the cut); B bullet 10, a claim cut is allowed only if both judges mark at most 20 percent of blocking claims as losing a decision-relevant clause (precondition for the cut). The test population is the 34 claims of B's replay (22 blocking). The default is the owner's decision. What both agree on is implemented first: `repair_line` covers the three location fields (Change 1); the claim cut is a separate switch.
- **Risk**: Medium. Recorded as an unresolved conflict.

### Change 8: The raise-the-limits lever, narrowed (from Variant B Round 2, A's count)
- **Source**: Variant B section 3.5 (base), Round 2 bullet 8; Variant A Round 2 N8; debate points C-011, U-011.
- **Target**: Base section 3.5 and section 5 INV-C column (replace).
- **Rationale**: Both final tables: C-011 Hybrid (71%), U-011 Variant 2. The cut covers the anchors, so B no longer proposes raising them; any fixed limit has a tail, and a raise needs an admission curve and an owner decision.
- **Integration point**: The lever is a claim-only raise to 450 (12 of 12 claim-dependent lines on P273 at 450, 11 of 12 at 400), a separate owner decision, never part of the default policy; the CO-8 brief change (limits stated from the constants) is common ground; pin cost is stated per site: 2 assertion sites for a claim-only raise (`test_review_findings.py:117`, `test_review_findings_v2.py:241`), 3 if `card_convert.py` imports the shared claim constant (`test_review_card_convert.py:500`), and the quote pin (`test_review_findings_v2.py:200`) changes only if the quote limit is also raised. Replace the base's "four boundary assertions".
- **Risk**: Low.

### Change 9: Evidence corrections and additions (from the debate's own findings)
- **Source**: Scorer-identified contradictions in the base (`base-selection.md`, Correctness 4); Variant B Round 2 section 3 (E1-E5); Variant A Round 2 N2, N3; debate points A-001, A-003, X-002, X-003, S-003, U-006, U-007.
- **Target**: Base section 4.2, 4.4, 4.6 and section 8 answer 1 (replace, insert).
- **Rationale**: Both advocates conceded these in Round 2: "5 of 5" is four confirmed and one unconfirmed; the base's "none of the 42 merges where a blocking row survived" is wrong because the 3 no-survivor merges are inside the 42 (the re-evaluation reads 39 for the merges that kept a blocking row); "stall exposure is small" is withdrawn (79 of 855 reviewer-runs have `ok` False on P273; 10 of 273 merges below the floor under today's `ok`); A's "at most 4 residual lines" is a floor; all four PASS-by-loss rows are anchors over 200.
- **Integration point**: Correct the three figures in place. Add the P273 results as a labelled second population with its method line and its differences from audit-D (273 merges, 90 lines, 46 blocking, 79 ok-False runs against 264, 92, 49, 80; the 9-merge net difference, which B reports as 15 unreconciled, is not reconciled); add the prefix-location result (70 of 70 on anchor and anchor2), the verdict simulation (cut-all: 3 PASS to FAIL, 16 added blocking rows, 13 of 16 already FAIL, no FAIL to PASS), and the floor results (10 today, 5 with tolerant eligibility, 0 with the cut). Label the audit-D "0 of 264 after the cut" as derived from the `flags.tsv` reason text. State A-001 as the debate concluded: audit-D and P273 are adequate for ordering the policies but cannot give a recovery percentage, and a single population must be frozen before any percentage is stated. State A-003: reviewer behaviour is not stationary (CO-8 changes the claim rate), so the policy is written to hold in both directions.
- **Risk**: Low (corrections), with the population caveat kept.

### Change 10: Measurements, kill lines and tests (from Variant A, merged with the base's T-B1..T-B5)
- **Source**: Variant A section 5 (M1-M4) and Round 2 bullets 10-11 (K1-K5); Variant B section 6 (M1-M3, T-B1..T-B5) and Round 2 bullets 9-10; debate points S-004, U-003, U-004.
- **Target**: Base section 6 (restructure; the replaced base rows are named below).
- **Rationale**: Both final tables: S-004 Hybrid (82%), U-003 Variant 1 (85%). The cost-side re-merge is the only measurement in either proposal that can show the policy harmful.
- **Integration point**: Replace these base rows: base M1 ("the refusal fires on exactly the 3 merges ... and on none of the other 261") becomes "3 without the cut, 0 with it"; base M2 (re-ask recovery across 44 runs) becomes re-ask on the residual lines only; base M3 (raised constants 300/450 for anchors) becomes the claim-only admission curve of Change 8; base T-B4 (`review cluster` output byte-equal) becomes byte-equal on the existing v2 fixtures except for the additive keys `first_pass_state` and `repairs`. Add: M1 offline replay of the cut on two frozen populations (audit-D and the 1,215-report corpus) reporting lines passing the parser, fields locating uniquely over fields whose full anchor locates, `refs_changed` and the residual by rule; M2 re-merge with repair on and off counting added blocking rows judged false and PASS-to-FAIL flips; M3 two-judge claim-meaning test (K2, Change 7); M4 stateless re-ask on the residual per transport; unit tests: no-op on every valid fixture line, boundaries 200/201 and 300/301 with and without repair, idempotence, no invented anchor, conservation, differential first-pass, the merge matrix (one reviewer all dropped; one dropped blocking plus one empty block; surviving blocking row; only `blocking: false` drops; acknowledged drops; panels of 1 to 5), and the v2 loss unit (one block with one over-limit location field and one valid line: `complete`, both findings reach `cluster`; a claim fault stays `invalid` unless the claim switch of Change 7 is on). Kill lines K1-K5 as in both advocates' bullets 10 and 11 (K1 computed over fields that occur verbatim in the document, 75 percent on a code or multi-line corpus); rules written to a file before the first run; the owner may change the numbers.
- **Risk**: Low.

### Change 11: Invariant table (from Variant A, merged with the base's 14-row table)
- **Source**: Variant A section 4; Variant B section 5 (base); debate points S-005, A-004.
- **Target**: Base section 5 (replace the INV-C, INV-D, INV-G and INV-I cells).
- **Rationale**: Both final tables: S-005 Variant 2 (the 14-row table is wider), keep A's candid label.
- **Integration point**: INV-C reads "partly endangered" for the cut (the validators are unchanged and `repair` is off at the parser by default; a consumer that relied on the drop would see a change; none found in `tests/review`); INV-D lists the additive keys (`repairs`, `dropped`, `first_pass_state`, `repaired`); INV-G requires the re-ask prompt to hold only the reviewer's own block and its own errors and to grant no new tool (T-B5); INV-I notes that under Alternative A of Change 6 `block_ok` becomes True for a reviewer whose only fault was length, and that the eligibility rule is per Change 6 (C-002 unresolved).
- **Risk**: Low.

### Change 12: The `SKILL.md:343` sentence (from Variant A, accepted by both)
- **Source**: Variant A section 7 point 1 and Round 2 N7, bullet 12; Variant B Round 2 W6, bullet 11; debate point X-001.
- **Target**: Base section 3.4 "Reflect UC-1 and UC-2" row and section 8 (insert).
- **Rationale**: Both final tables: X-001 Variant 1 (66% and 68%). The sentence is step 4 of the reflect shadow procedure only (no match in the v1 prompt or spec-panel texts) and is pinned (`tests/cli/reflect/test_shadow_skill_contract.py:229-232`).
- **Integration point**: Leave the Normalize sentences byte-identical; add one sentence after them: the package's parser step shortens location fields in code and records every shortening, the orchestrator still never edits a finding, and the first-parse compliance rate reads `first_pass_state`. The owner confirms that package code is not "the orchestrator"; if not, the v2 call sites stay at `repair=False` (itemise and re-ask only) and the v1 `merge` keeps the cut, because no text rule binds it.
- **Risk**: Medium. An owner reading is required. Round 2.5 INV-019 (the unchanged text and the additive sentence both use "invalid" for different states) is not addressed and is carried open.

### Change 13: Third copy of the constants (from Variant B Round 2 bullet 12)
- **Source**: Variant B Round 2 W7 and bullet 12; Variant A Round 1 weakness 7; debate point C-011.
- **Target**: Base section 3.1 "Limits constants" row and section 3.6 (insert).
- **Rationale**: A's objection that B keeps `card_convert.py`'s marked claim cut while forbidding truncation elsewhere was conceded as a documentation fix.
- **Integration point**: `card_convert.py` imports the shared constants and keeps its marked claim cut (`text[: MAX_CLAIM - 3] + "..."`, `:200-201`) as a legacy conversion measure, named as an explicit exception that is reconsidered if the claim switch of Change 7 is turned on; the three production call sites passing `repair=True` rewrite no pin.
- **Risk**: Low. Round 2.5 INV-022 (two implementations of the same claim-cut arithmetic if a claim cut is adopted) is carried open.

### Change 14: Strongest objection, restated for the merged position (from both variants)
- **Source**: Variant A section 7; Variant B section 8; Round 2 (B) section 1.3 and C-012 row; Round 2 (A) section 1.3 (C-009 and C-012 paragraph) and W3.
- **Target**: Base section 8 (restructure).
- **Rationale**: After the merge two objections remain open in the debate's own record. (a) Provenance (C-012): the stored finding is not a byte copy of a line in the hashed report. B moved C-012 to Variant 1 for the cut anchor, because the stored anchor remains a flattened-form substring of the reported line and `original_sha256` plus the existing `report_sha256` keep provenance; the byte-copy objection is kept only for a claim cut. (b) Eligibility cost (C-002, Change 6): under the bare parser verdict a repaired block votes to clear and counts toward quorum (B's Round 1 weakness 3; A's W3 answer), under a derived eligibility some length-fault runs stay ineligible. Variant A's section 7 answer to the principle objection (the report file is never edited, `report_sha256` is recorded, the repaired object is a derived copy with `original_sha256`, a drop is also an edit and a larger one) is kept for the location fields; the evidence is 70 of 70 and 89 of 89 prefixes locating once and `refs_norm` changed on 0 of 125 lines.
- **Integration point**: Replace the base's objection and answer with this merged pair; keep the base's answer 5 (what B does not have: a measured re-ask recovery rate on gateway models, M2); withdraw answer 1 ("stall exposure is small", Change 9).
- **Risk**: Low.

### Change 15: Open invariants and unresolved conflicts section (transparency)
- **Source**: `invariant-probe.md`, `round2.5-fault-finder-raw.md`, `debate-transcript.md` Convergence Assessment.
- **Target**: Base section 9 "Open facts this proposal does not settle" (append) and a new section 10 (insert).
- **Rationale**: Convergence was BLOCKED_BY_INVARIANTS at 85.7% (24 of 28): 4 HIGH UNADDRESSED (INV-001, INV-017, INV-018, INV-023) and 12 MEDIUM; standard depth has no Round 3, so none was resolved. They must travel with the merged text; the merge does not resolve them.
- **Integration point**: Section 10 lists the unresolved points (C-001, C-002, C-009, C-012) with both positions (Changes 6 and 7) and every UNADDRESSED invariant of the probe by ID, severity, category and one sentence taken from `invariant-probe.md`, with the statement "not closed by this document". Do not add a fix for any of them.
- **Risk**: Low. This is transparency, not design.

### Change 16: Reach: v2 loss unit, PR and rf-qa rows, and base rows made stale by Change 1 (from both advocates' converged points)
- **Source**: Debate points C-003 (both Variant 1, 74%), C-014 (both Hybrid, 63%), X-003 (both Hybrid, 72%); Variant A section 2 item 7 and section 6; Variant B section 7 (base) and section 2 (base).
- **Target**: Base section 3.4 (module table, Reflect row and PR row), section 7 and section 2 table rows C-01 INV-003, INV-004, the "itemise branch" introduction and INV-022 (replace).
- **Rationale**: The plan review found these converged conclusions untargeted and found base rows that the cut makes false ("INV-003 does not arise", "INV-004 ... answers it with the re-ask ... not a repair", "B reads the merged text as the itemise branch", "a repair placed in callers is not needed").
- **Integration point**: (a) v2 loss unit: one over-limit location field no longer invalidates the whole reviewer (`cluster.py:255-257` skipped it before); the cut removes the loss unit only for the length share, and a claim fault or any non-length fault (reflect's residual is non-length for both policies: coverage rows, citation line numbers, X-003) still costs the reviewer unless the re-ask works; "A 4 of 92" is a v1 floor and does not size the v2 residual. (b) PR and rf-qa: a `quote` prefix passes the `verify_cmd.py:68-72` substring test; the quote limit is a per-profile parameter; the re-ask is the stateless in-session form; neither variant measured PR code, so a code corpus is required before a PR module relies on it; replace the base's "not a cut quote" wording. (c) Section 2 rows: INV-003 is answered by the `repair=False` keyword (every direct-parser pin stays unmodified); INV-004 holds because the cut sits in `findings_v2.parse_block` and the re-ask covers the non-length residual; the C-01 phrase "normalise-or-itemise" is read as both (cut the location fields, itemise the rest); INV-022 is satisfied because a repaired line locates and clusters like any other for verbatim anchors, with the unlocated and ambiguous cases carried in Change 15.
- **Risk**: Low. Round 2.5 INV-024 (the v2 loss unit is removed only for the length share) is the same limitation and is carried open.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-009 / C-001 (claim part) | Cut `claim` to 297 characters plus `...` as a default | Unresolved; the base wording (no other field cut) and A's alternative are both recorded (Change 7); not decided by this plan. |
| C-008 / U-002 | Copy tail-only reference tokens into `refs` (cap 8) | A demoted it to a recorded flag in Round 2; `refs_norm` changed on 0 of 125 lines; both final tables: record `refs_changed` only. |
| C-002 | A's bare parser verdict as the only eligibility test, with a C-03 knob counting only `repaired == 0` blocks | Unresolved; both alternatives recorded (Change 6). |
| C-011 (anchor part) | B-raise of anchor and anchor2 to 300 | B withdrew it: the cut covers anchors, 4 of 124 lines would still fail at 300/450, and it widens findings-v1 (INV-C). |
| A section 1 wording "touches no field the limits do not name" and "exact prefix" for claims | A's own sentences | Contradicted by A's own `refs` copy rule and its 297 plus `...` claim (scorer contradictions A-X1, A-X2); both removed. |
| A section 2 item 5 "recorded as attempt 2" (unconditional) | A's manifest claim | `manifest.py:371-372` raises `OutOfOrder` first; narrow form adopted (Change 4, A-006). |
| A section 3.4 / section 1 "at most 4 lines" and "INV-009 unchanged" | A's residual and C-02 statements | A withdrew both in Round 2 (floor, population-dependent; the cut removes INV-009 for length-only faults). |
| A's "SKILL.md:343 needs one sentence changed" | Editing the pinned sentence | A withdrew it: additive sentence only (Change 12). |
| B's Round 1 trigger "re-ask all 44 reviewer runs before the merge" | Base section 3.2 trigger | No v1 vehicle exists; replaced by the refusal-driven trigger (Change 4). |
| B's "5 of 5 re-asked blocks recorded valid", "stall exposure is small", "four boundary assertions" | Base sentences | Conceded wrong or incomplete by B in Round 2 (Changes 8, 9). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | High | Base position flips; the cut runs in production without M1/M2; a prefix matching several places (INV-017) silently absorbs a new blocking defect | Remove the `repair=True` argument at the call sites; the `repair=False` default restores today's behaviour |
| 2 | Medium | `blocking_state` mislabels CRITICAL or prior lines (INV-005, INV-007) | Keep `dropped` itemised only; no change to refusal inputs |
| 3 | Medium | Compliance figure drifts if `first_pass_state` is wrong (INV-002) | Differential test fails; read the metric from a `repair=False` parse |
| 4 | Medium | Reflect re-ask cannot be recorded before the `collected` commit (INV-018) | Reflect keeps today's orchestrator count; v1 unaffected |
| 5 | Medium | A later passing round forgets a lost blocking line (INV-001) | Acknowledgement option lifts the refusal; the refusal can be left unregistered |
| 6 | High | Clearing or quorum miscount under C-02/C-03 | Switch to the other alternative |
| 7 | Medium | A claim cut changes meaning, or an uncut claim keeps a reviewer invalid | Flip the claim switch |
| 8 | Low | None (owner lever, off by default) | Not enabled |
| 9 | Low | A corrected figure is itself wrong (population differences) | Revert to the base sentence with its caveat |
| 10 | Low | Kill lines not pre-registered | Re-run before first use |
| 11 | Low | Invariant row mislabelled | Revert the row |
| 12 | Medium | Owner reads package code as "the orchestrator" | v2 call sites stay at `repair=False` |
| 13 | Low | Two implementations of the claim cut | Single owner function |
| 14 | Low | None | Revert to the base objection |
| 15 | Low | None (documentation of open items) | N/A |
| 16 | Low | A stale base row survives | Re-run the section 2 consistency check |

## Review Status
- [x] Auto-approved (default, non-interactive run)
- [ ] User-approved (--interactive)
- Approved by: auto, after the independent plan review in `plan-review.md` (3 HIGH, 7 MEDIUM, 5 LOW defects; all applied in this revision)
- Approval timestamp: 2026-11-14T16:58:30Z
