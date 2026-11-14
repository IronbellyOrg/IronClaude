# Merge Log: C13 ledger model

## Metadata
- Base variant: Variant B (`adversarial/variant-2-original.md`, 291 lines, Option B "find once, then verify-only")
- Non-base variant: Variant A (`adversarial/variant-1-original.md`, Option A "re-find and cluster every round, D2/D3/D16 fixed")
- Plan: `adversarial/refactor-plan.md` (20 Planned Changes, 21 binding Amendments A-01 to A-21)
- Merged artifact: `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/reviews/adversarial/ledger-model/proposal-merged.md`
- Merge date: 2026-11-14T01:44:56Z (header time of the merged artifact)
- Executor: merge-executor (Step 5); read-only on every file except the merged artifact and this log
- Application order (Amendment A-16): 16, 9, 15, 13, 1, 2, 3, 11, 4, 12, 5 (with 6 merged), 7, 8, 10 (10a, 10b, 10c), 14, 17, 18, 19, 20
- Rule applied: where an Amendment names a clause of a Change, the Amendment text replaced that clause; the replaced clause was not applied
- Status: applied with documented deviations (see "Deviations from the plan")

## Changes Applied

Format per change: Status, Source, Target (location in the merged file, by section and Core item), Before (base text), After (merged text), Provenance tag (the tag family used in the merged file), Validation. "Core item N" refers to the numbered list in the merged "Core" section.

### Change 16 (Terminology, citations, glossary), applied first
- Status: APPLIED (Amendments A-19, A-20)
- Source: scoring defects R1, R3, L4; orchestrator check of `review_ledger.py:65` versus `:1591`
- Target: Citation key and glossary box (top of file); Core item 11; Contract fields (Plan answer row); CLI row `ledger answer`
- Before: Core 11 cited `:65` for the verifier's status words; "answer" named two steps; D-codes unglossed
- After: `:1591` (`VERIFY_RESULTS`) cited, `:65` named as `ANSWER_ACTIONS`; reviser step stays `ledger answer`, the other is "plan answer" or "verifier answer" (executor default of A-20, OD-7 open); glossary box of D1, D2, D3, D4, D5, D16a-c, U, X, I, W; G9 and G10 glossed only in Test coverage (after the tests are introduced, A-19)
- Provenance tag: `Source: Base (original, modified) ... Change #16 / Amendment A-19, A-20`
- Validation: all `:1591`/`:65` cites checked against the plan text; PASS

### Change 9 (Per-lens predicate, honest sizing)
- Status: APPLIED (Amendment A-10)
- Source: Advocate B Round 2 concession 5; X-007, C-014; A "Seams" row "Decider"
- Target: Core item 9; Contract fields (Row proposed additions, New row); Cost ("mostly a port" sentence, new work 3 and 7); Risk 5 and 16
- Before: "lens registry ... one table row per lens"; "B is mostly a port, not a new build"
- After: registry plus a new predicate and key set per non-spec lens, reviewer flag as candidate input, `effective_blocking` recorded; the sentence removed and replaced by the list of new code; `members[]` added to the Row additions (A-10)
- Provenance tag: `Change #9 / Amendment A-10, Disposition: modified`
- Validation: figures 2,668 / 1,578 / 77 / about 650 kept exact; PASS

### Change 15 (Evidence hygiene)
- Status: APPLIED (Amendments A-18, A-19)
- Source: X-005, C-016; Advocate A Round 2 "P4 holds for the cap and quorum changes only"
- Target: Position paragraph; Evidence opening paragraph; E-19 to E-24; P3, P4; the comparison table; P4a; weakest points
- Before: text that read as "B better on evidence" and "A strictly safer"
- After: neutral claim sentence in Position; Evidence opening restated; E-20 now says no loop reached a clean PASS, the improvement of 3 is below the spread of 4, the final-review count (3) is below both controls (8 and 4) but line 135 counts 6 loop-only unresolved labels (the arm is then above the second control, 4, A-18) and the report says "not a ranking"; E-19 says it bounds the cost and is not evidence of safety; E-23 says round-1 faithfulness is not evidence for rounds 2-3
- Provenance tag: `Change #15 / Amendment A-18, Disposition: modified`
- Validation: 11/9/8, 12/7/4, 13/9/3, 3 versus 4, 264, `FINAL-REPORT.md:75,97-98,105,135` all present (Threshold check below); PASS

### Change 13 (Persistence contract)
- Status: APPLIED (Amendment A-06)
- Source: B Core 1; A "Contract fields" and test 13; INV-014; C-009 SPLIT
- Target: Core item 1 ("Persistence contract" paragraph); Risk 7; T-A13, T-B13
- Before: schema bump `review-ledger/2` only
- After: Stage 0 additive `min_writer` key (about five lines), refusal to append for an unknown `min_writer`, writing version in the report header, additive Stage 0 keys under `review-ledger/1`, A's additive route rejected for the port with the INV-014 reason, HEAD `792cf8c52` fixture kept as the migration test, converter versus message is OD-5, owner-decline consequence stated
- Provenance tag: `Change #13 / Amendment A-06, Disposition: merged-from-multiple`
- Validation: PASS

### Change 1 (Cap by refusal, `--cap` conflict, `--round` help)
- Status: APPLIED (Amendments A-05, A-17, A-19)
- Source: A Core changes 1 and 2; C-004; INV-015
- Target: Core item 0; CLI row `review merge`; Stage table; Risk 11; T-A1 to T-A4
- Before: no round bounds on the master engine; base had `E-CAP` only in the port
- After: item 0(a) round `cap + 1` refused and round `cap` recorded as ESCALATE (A-17 wording), 0(b) `default=None` / `cap or 3` / conflicting `--cap` is a `ClickException` / same value no conflict / `--round` help "1 up to the ledger's cap", 0(c) merge after PASS or ESCALATE refused and header warning, 0(d) size; "Order of work" replaced as one paragraph (A-19, see Change 18)
- Provenance tag: `Change #1, Disposition: merged-from-multiple`
- Validation: `ledger.py:114-118`, `:93-96`, `merge_cmd.py:36-42,101-104` cites present; PASS

### Change 2 (Quorum, degraded rounds, `--resolution` denominator)
- Status: APPLIED (Amendments A-01, A-13)
- Source: A Core changes 3-5; U-001; INV-007, INV-016
- Target: Core item 3 (quorum rule and table); Contract fields (Round entry, Stage 0); Risks 4, 12, 13; T-A5 to T-A9, T-Gg
- Before: one clause "require a quorum of valid blocks"
- After: the quorum rule with `quorum = min(2, panel_size)`, `degraded = valid < panel_size`, `below_quorum = valid < quorum`, the four-row decision table of A-01 in place of "a degraded would-be PASS is refused with nothing recorded"; `--resolution` checks apply only when given; header line `degraded: yes (<valid> of <panel_size> valid blocks, quorum <quorum>)` (wording adapted to INV-016, see Deviations)
- Provenance tag: `Change #2 ... Amendment A-01, Disposition: modified`
- Validation: A tests 7-9 rewritten to the table; replaced clauses not present in merged text; PASS

### Change 3 (Atomic refusal)
- Status: APPLIED-WITH-DEVIATION (Amendment A-05; one clause marked NOT APPLIED)
- Source: Advocate A Round 2 "Fixes A needs" 1; INV-019, INV-020
- Target: Core item 3 ("Atomic refusal and its one permitted write"); T-P19, T-P20
- Before: "nothing is recorded" on a refusal
- After: no row, member, history, round or clearing change; the only write is an append to `refusals[]` saved in the CLI's `except LedgerError` path; commit by writing the work copy back; ledger saved before `--out`; identical replay returns the stored result and does not append; atomicity test `ledger_without_refusals == deepcopy_before`
- Provenance tag: `Change #3 / Amendment A-05, Disposition: modified`
- Validation: NOT APPLIED clause: how `refusals[]` is held for a round-1 refusal before a ledger exists (the plan is silent; marked `[NOT APPLIED: ...]` in the merged text)

### Change 11 (`defer` through the decision function)
- Status: APPLIED (Amendment A-03)
- Source: INV-001 (orchestrator-confirmed `ledger.py:350-360`)
- Target: Core item 7 ("`defer` goes through the decision function"); CLI rows `defer`, `release`; Risk 17; T-P1; OD-11
- Before: `defer` recomputed PASS inline
- After: Stage 0 form (live blocking row only, shared `decide()`, `deferred_lids`); Stage 3 port `defer` words-only (`review_ledger.py:2359-2386`); `ledger release --id --quote` in phase `verify` only, owner may decline (OD-11)
- Provenance tag: `Change #11 / Amendment A-03, Disposition: modified`
- Validation: PASS

### Change 4 (`review merge` for round >= 2; `ledger revise`)
- Status: APPLIED (Amendments A-12, A-13)
- Source: A "CLI surface", "Consumer modules"; X-006, C-011, C-017; INV-006, INV-013, INV-018
- Target: Core item 3a; CLI rows; Consumer modules (spec loop row); Risk 7; OD-4; T-B2, T-C1, T-P6, T-P18
- Before: `review merge --round k>=2` refused unconditionally
- After: adapter or CLI refusal plus same-change prompt edit with pin test (OD-4); `revised: {round, old_sha256, new_sha256}` and the four INV-018 refusals; engine behind `ledger revise` per stage (A-12); shared exit-code table; plugin mirror of the prompts file; seams table as one paragraph under Core item 3 (A-12)
- Provenance tag: `Change #4 / Amendment A-12, Disposition: modified`
- Validation: exit codes 0/10/11 and 12 PENDING only where a sweep is required kept; PASS

### Change 12 (Rounds 2-3 are one reviewer; multi-reviewer limit)
- Status: APPLIED (Amendment A-15)
- Source: A "How it works"; C-010; B Risk 8
- Target: Core item 10; Risk 8; OD-10; T-Gc, T-B11
- Before: Risk 8 residual "needs new design"
- After: explicit limit; concatenation rule is the condition for lifting it; A's multi-reviewer merge stays the round-1 model
- Provenance tag: `Change #12, Disposition: merged-from-multiple`
- Validation: PASS

### Change 5 (Verify boundary follows C02/C15) merged with Change 6 (spanless and ambiguous rows)
- Status: APPLIED-WITH-DEVIATION (Amendments A-03, A-05, A-07, A-19; stage membership split, see Deviations)
- Source: A "Seams" table, Risks "Decider pre-empted"; X-003, C-012; INV-002, INV-008; A-006; `hunks_touch(None)` False
- Target: Core item 4 (refusal classes), Core item 3 (spanless rows), Data flow, P1, P5, P6, Risk 3, 4, 14, 15; T-Gf, T-P2, T-P8
- Before: whole-input refusal including new rows with a bad anchor; one re-ask then an X item
- After: invalid plan answers refuse the input (only `refusals[]` written); invalid new rows demoted to `deferred` / `scope: outside` / `origin: unanchored` / `flag: <code>` in the same atomic write; the required child of `touched_ok: no` never demoted; replay returns the stored result; two refusals record ESCALATE with `refused_twice`; spanless rows get `unanchored`, ambiguous rows `anchor_ambiguous`; the human path is `ledger release` (Stage 3) or `defer` (Stage 0) or re-anchor
- Provenance tag: `Change #5, #6 / Amendments A-05, A-07, Disposition: modified`
- Validation: codes `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `E-INCOMPLETE`, `E-FROZEN`, `E-SCHEMA` and `review_ledger.py:1778-1794` kept; Risk 6 not targeted (A-19); PASS

### Change 7 (Evidence rules for the answer; what each `prior` status does)
- Status: APPLIED (Amendments A-11)
- Source: B Core 5 and 11; Advocate A Round 2 fix 3; INV-003, INV-004, INV-009; C-008, A-007
- Target: Core item 5 ("Evidence rules"), Core item 11, Contract fields (Plan answer), P3, comparison table; T-B3, T-B7, T-P3, T-P4, T-P9
- Before: one-line statement of the answer protocol
- After: part (a) for the port (`result` values at `:1591`, whole-input refusal for a missing or non-locating quote, proposed 12 to 200 characters, overlap with the mapped span widened by 3 lines or a changed hunk, deletion-only rule); part (b) for the adapter and option (i) (`resolved` is the only clearing status, duplicate ids collapse, unanimity); the claim that INV-003 and INV-004 need new rules inside the port removed
- Provenance tag: `Change #7 / Amendment A-11, Disposition: modified`
- Validation: example line `{"prior": "L3", "status": "resolved"}` kept in the rules-file note (Test coverage); PASS

### Change 8 (One-way blocking, regrade and re-attack, field classes)
- Status: APPLIED (Amendments A-04, A-10, A-15)
- Source: Advocate B Round 2 concessions; C-005, C-006; INV-011, INV-012
- Target: Core item 2; Contract fields (Row, New row); P2; Risk 15; register rows INV-011, INV-012; T-Ga
- Before: 13 frozen fields, no upward path, "accepted text cannot be re-attacked"
- After: 13 frozen fields kept; named inputs `regrade_of` and `reattack_of` with code changes (a) to (d); `parent` keeps its meaning; guarantee restated; master field list removed from the base text and field classes kept in the register, scoped to the round-1 merge and option (i) (A-10); risk HIGH (A-15)
- Provenance tag: `Change #8 / Amendments A-04, A-10, Disposition: modified`
- Validation: `review_ledger.py:1592-1606,1669-1675,1769,1746-1751,1654-1658,66,1703` cites present; PASS

### Change 10 (Late-finding visibility), applied as 10a, 10b, 10c
- Status: APPLIED (Amendment A-02)
- Source: A Correctness P6, Risks "late findings", U-004; C-007, X-004; Advocate B Round 2 concession 7 and Fixes B needs 3; INV-013
- Target: 10a Core item 6 (`would_block`, merged-report listing); 10b Core item 7 (W term) and the decision formula; 10c "brief for a round k reviewer" paragraph, Risks 1, 2, 17, 19, OD-1, OD-2, the Correctness "Two tests"
- Before: outside rows never block, no sweep term in `decide`; unconditional changed-text policy
- After: W = would-block outside rows found in rounds >= 2 on a lens with `sweep: none`; W > 0 gives ESCALATE with `reason: outside_would_block`; W never in U, never in the plan; OD-1 decides only ignore versus count; the deferral policy and the reversal of the older-defect clause are not the default; "W > 0 ends a loop at round 2 without a fix cycle" in Core item 7 and Risk 1
- Provenance tag: `Change #10 (10a, 10b, 10c) / Amendment A-02, Disposition: modified`
- Validation: no statement remains that an outside row enters U (grep); 89% / 100% kept as a bound on cost, not as safety; PASS

### Change 14 (Measure what both sides left unmeasured)
- Status: APPLIED (Amendment A-19)
- Source: A U-003, U-004, U-005; B Risk 3
- Target: Risk 3 Mitigation cell (the plan target is corrected by A-19); Correctness "Two tests"; T-A11, T-P2; Contract fields
- Before: no refusal log
- After: per-round refusal log (code, count, second refusal) in Risk 3; late-row measurement from `row["history"][0]["round"]` and `members`, changed ranges as observation only; E2-shaped fixture (49 `3-dropped-blocking`, 48 length rejections, three flips) as T-A11; `unanswered_priors` and `not_cleared` dropped with rationale (logged below)
- Provenance tag: `Change #14, Disposition: modified`
- Validation: PASS

### Change 17 (One test plan)
- Status: APPLIED (Amendments A-07, A-08, A-09, A-15, A-16)
- Source: A "Test coverage needed" (15 new tests, 1 rewritten into 2, gate commands); B "Test coverage needed"; S-005; probe acceptance tests
- Target: Test coverage needed (existing-tests table with the Stage 0-2 and Stage 3 columns; new-tests table with columns id, test, stage, source, status)
- Before: B's table of 9 replaced and 15 renamed tests plus 15 new groups
- After: key (test, stage); A tests T-A1 to T-A15 (T-A10 replaced by T-B3, T-A12 dropped, T-A5/7/8 rewritten to the A-01 table); B groups T-B1 to T-B15 (T-B10 replaced by T-P2); 16 probe tests T-P1 to T-P10, T-P13, T-P14, T-P17 to T-P20 (T-P5 and T-P17 are the A-09 INV-005 and INV-017 acceptance tests); T-Ga to T-Gg (A-15 groups a to g, T-Gf are the three A-07 tests); T-C1
- Provenance tag: `Change #17 / Amendments A-08, A-15, Disposition: merged-from-multiple`
- Validation: all test line anchors (`:193-217` ... `:518-566`, `test_review_cli.py:196,328,425`, `test_review_rules_text.py:34-42,65-73`, `test_review_loop_extension.py:49-55,120-127`) present; 54 test ids defined and referenced; PASS

### Change 18 (Staged delivery with a decision gate)
- Status: APPLIED-WITH-DEVIATION (Amendments A-14, A-16, A-19, A-21)
- Source: both advocates' Round 2 merged-proposal lists; C-001 SPLIT, C-013 UNRESOLVED
- Target: Cost ("Delivery stages and the Stage-2 gate", replacing "Order of work"); How it works intro paragraph; Position paragraph; comparison table; Core item 0 to 3
- Before: "Order of work" paragraph; three owner decisions
- After: stage table (stage, contents, exit condition) for Stages 0, 1, 2, 3 and "Always"; option (i) specified as in A-14(3); the gate argued both ways; "The plan does not assert which side wins"; the neutral replacement of "B is the better rounds 2-3 target" (A-14(1)) is in the log's "Changes NOT Being Made" row; invariant sentence stated symmetrically (A-14(2)); intro paragraph added under "How it works" and said so here (A-19)
- Provenance tag: `Change #18 / Amendment A-14, Disposition: modified`
- Validation: A's "land changes 1 to 5 first", M/Medium and B's XL/High, three owner decisions all present; deviation: Change 5 stage membership split (see Deviations); PASS with deviation

### Change 19 (Open-decision and unresolved-conflict register)
- Status: APPLIED (Amendments A-13, A-20)
- Source: S-006, C-013, A-002, A-004 and the owner decisions of Changes 4, 10, 13, 16, 18
- Target: new section "Open decisions and unresolved conflicts" (after Cost): unresolved-conflict table with both advocates' final positions, other open points (C-015, A-005, A-007, A-001/A-003, SPLIT and NEITHER carried), OD-1 to OD-11 table
- Before: none
- After: as stated; OD numbers replace D-1 to D-10, OD-11 added; B's three decisions mapped to OD-1/OD-2, OD-3, OD-6 in Cost
- Provenance tag: `Change #19 / Amendments A-13, A-20, Disposition: merged-from-multiple`
- Validation: OD-1 to OD-11 all defined (11 of 11 resolve); PASS

### Change 20 (Invariant register and restated sufficiency claim), applied last
- Status: APPLIED-WITH-DEVIATION (Amendment A-09; state name)
- Source: `invariant-probe.md` (20 findings: 10 HIGH UNADDRESSED, 7 MEDIUM UNADDRESSED, 1 LOW UNADDRESSED, 2 ADDRESSED in principle)
- Target: new section "Invariant register" (after Correctness): restated sufficiency claim, 20-row table (probe severity, probe status, finding, design status in the port, design status in option (i), closure rule), the four conditions of `closed-in-port`, F1 to F6; P1/P2 sentences replaced
- Before: unconditional sufficiency claim
- After: claim restated as "no PASS and no clear without a positive, script-checked signal on the recorded-round path, given INV-001 to INV-009 closed"; F4 (owner C05 hook), F5 (owner C01), F6 residual with the owner not named by the probe; probe status UNADDRESSED kept for every row; design status three-state per A-09
- Provenance tag: `Change #20 / Amendment A-09, Disposition: merged-from-multiple`
- Validation: 20 of 20 INV ids present; no HIGH item marked resolved; see Deviations for the state name

## Post-Merge Validation

### Structural integrity
- Heading hierarchy: 1 H1, 9 H2, 24 H3, 0 H4 or deeper; starts at H1; no level gaps; no orphan subsection (every H3 sits under an H2). Section order is B's (Design, How it works, Evidence, Correctness argument), then the new Invariant register, then Risks, Test coverage, Cost, then the new Open decisions section.
- HTML comments: 106 opened, 106 closed (3 header comments plus 103 `Source:` tags; 77 of them carry `Disposition:`). No changelog paragraph at the top.
- Tables remain tables; no emoji characters (grep over the emoji and dingbat ranges returned none).
- File size: 623 lines, 24,017 words (base: 291 lines, 8,348 words).
- Result: PASS

### Internal references
Method: grep extraction of every token from the merged file (outside HTML comments for the E-token scan) compared with its definition site.

| Reference family | Distinct referenced | Defined | Broken |
|---|---|---|---|
| `E-N` (Evidence, E-1 to E-33) | 33 | 33 | 0 |
| `INV-nnn` (register rows) | 20 | 20 | 0 |
| `OD-n` (owner decisions) | 11 | 11 | 0 |
| `T-xx` (test ids) | 54 | 54 | 0 |
| `P1` to `P6`, `P1a` to `P6a` | 12 | 12 | 0 |
| `Core item N` (items 0 to 7, 9 to 11 and 3a referenced; 0 to 12 and 3a defined) | 12 | 14 | 0 |
| `Risk N` (1, 3, 8, 19 referenced; 1 to 20 defined) | 4 | 20 | 0 |
| Total | 146 | | 0 broken |

`Change N` and `A-nn` appear only inside provenance comments and resolve to `refactor-plan.md`; prose in the merged file never refers to a plan change number (grep found one "Change 8" inside an HTML comment). Result: 146 of 146 resolved, 0 broken. PASS

### Contradiction re-scan
New contradictions introduced by the merge, found and fixed in the merged file (three leftovers, then re-scanned):
1. Degraded-round table versus leftover text. Three places said "below-quorum would-be PASS" or "degraded would-be PASS" only (Consumer modules spec-loop row, T-A15, P4a) while the A-01 table also refuses a would-be PASS beside a non-valid reviewer's dropped line. Fixed to "a would-be PASS that the quorum table of Core item 3 refuses". Residual: none.
2. Outside rows and U versus W. The falsifier remedy said outside rows "count toward the decision" while W is counted by default. Reworded: counted is already the default until OD-1; the remedy applies if the owner chose to ignore W. No sentence remains in which an outside row enters U or the plan (grep for "enters U", "enter U", "toward U" matched only the explanation of the deleted clause inside a comment).
3. `defer`. Stage 0 form (shared `decide()`) and Stage 3 form (words-only plus `ledger release`) are stated once in Core item 7 and used consistently in Core item 3, the CLI table, Risk 17, OD-11 and the register. Residual tension recorded in OD-11: if the owner declines `ledger release`, a spanless row at Stage 3 ends in ESCALATE because the ported `defer` changes no status.
4. Refusal writes. "Nothing is recorded" was replaced by the `refusals[]` rule in Core item 3, P1, P5, Data flow, T-A1, T-A3. The existing test `test_review_cli.py:425` ("writes nothing") would conflict, so its assertion is narrowed to "nothing but `refusals[]` is written". Open: a round-1 refusal has no ledger to append to; marked `[NOT APPLIED: ...]` in the merged text.
5. `parent` versus `reattack_of` and `regrade_of`. `parent` appears once in prose and keeps its existing meaning (the required child of `touched_ok: no`); the two new ids are separate inputs. No contradiction.
6. `merge --round k>=2` refusal versus the adapter. Core item 3a, Core item 10, the CLI table, Data flow, T-B2, T-Gc and T-C1 all treat the choice as OD-4 and refuse a multi-reviewer round >= 2 in both variants. No contradiction.
7. Plan-internal tension carried, not introduced: Change 5 is in Stage 1 by Amendment A-21 and in Stage 2 option (ii) by Change 18. Resolved by splitting it (see Deviations).
- Result: 0 new contradictions after the fixes (3 found, 3 fixed, 1 clarification open as a NOT APPLIED note)

## Dropped or paraphrased anchors

Anchors the plan lists as dropped-with-rationale or modified, and anchors the merge could not preserve. "Replacement" names where the content went in the merged file.

| Anchor (ID or verbatim text) | Source variant | Change | Decision basis | Replacement or disposition |
|---|---|---|---|---|
| C-001, X-002: "re-find and cluster every round as the default model for rounds 2 and 3; D16c closed as by design" | A | 18 | SPLIT 58%, B won X-002 at 70%; prompt-only verification has no code check | Kept only as the Stage-2 option (i), specified in Cost; D16c named in Core item 3a and the comparison table |
| "B is the better rounds 2-3 target" (plan wording) | plan | 18, A-14(1) | neutrality | Replaced in the merged text by "the advocates ended SPLIT (58%): A is the shippable first step, B has the stronger clearing rule on the evidence of the code; no measurement separates them" (the gate argument in Cost) |
| C-002, X-001: clearing a `resolved_check` row when a quorate valid reviewer does not re-report it | A | 7 | B won at 93% and 90%; empty block is valid (`document_review_loop_prompts.md:58`) | Not adopted; E-30 states the limit; P3 |
| C-005: recompute `blocking` from the current group (`ledger.py:213-218`) | A | 8 | B won at 95%; A-adv conceded | Not adopted; one-way blocking with `regrade_of` (Core item 2) |
| C-006: re-cluster and re-match every round with the 3-line `same_defect` rule; stored `claim` not updated | A | 8 | B won at 80% | Not adopted in the port; E-4, T-B5 characterization pair; option (i) carries INV-012 field classes |
| C-008: `prior` lines as inert notes (`test_prior_lines_never_change_a_status`) | A | 7 | B won at 80% | Reversed for round 2 onward in the port (existing-tests table); kept green at Stages 0 to 2 |
| C-009 (partial): additive keys under an unchanged `review-ledger/1` as the persistence design | A | 13 | SPLIT 58%; INV-014 | Kept for Stage 0 keys with `min_writer`; rejected for the port (Core item 1) |
| C-012: refuse a degraded would-be PASS with no bound on re-runs and mutate before refusing | A | 3, 5 | SPLIT 55%; INV-002, INV-020 | Replaced by the A-01 table, bounded refusal (P5) and atomic refusal (Core item 3) |
| X-005, C-016: round-1 E2 faithfulness as support for the round engine; "the bundle does not favour verify-only" | A | 15 | both advocates withdrew | Removed; E-23 and E-20 state the no-ranking facts |
| P3 of A: "Status is truthful ... only by the four-step chain" | A | 15 | third step is silence (X-001) | P3a "(not carried)" paragraph; replaced by P3 |
| P4 of A: "strictly safer than today" as a general property | A | 15 | holds for cap and quorum only (Round 2 A) | P4a restricted accordingly |
| A change 4: the clearing loop runs only when the round is not degraded | A | 2 | the base has no silence-clearing loop | Not carried; `degraded` kept for round 1 and multi-reviewer first reviews (Core item 3) |
| U-003 / "One bookkeeping addition": `unanswered_priors` as telemetry only | A | 14 | an unanswered plan row is refused (E-INCOMPLETE) | Replaced by the refusal log (Risk 3, T-P2); sentence under Contract fields |
| `not_cleared` (merge result key and round result) | A | 2 | no clearing loop to gate | Dropped; sentence under Contract fields |
| A tests 10 and 12 | A | 17 | clearing positive case; `unanswered_priors` | T-A10 replaced by T-B3; T-A12 dropped (rows in the new-tests table) |
| C-010: merge supports several reviewers in rounds 2 and 3 | A | 12 | A won at 80%, unused in the shipped config | Explicit limit (Core item 10, OD-10); A's multi-reviewer merge kept as the round-1 model |
| C-015 consumer objection (PR bots re-find by construction; tasklist row) | A | 19 | SPLIT 55%, A-13 | Open point in the register and consumer table; E-32 |
| A-005 (no addressee for an unattended ESCALATE or PENDING) | debate | 19 | NEITHER 63%, A-13 | Register item, owner C19 |
| A-001 and A-003 | B | none | A-13: kept as in the base | Unchanged; listed in "Other open points" |
| A "Seams" table (four rows) | A | 4 | A-12 | Preserved as one paragraph under Core item 3 (the table form is not kept) |
| B "answer" used for two steps; `:65` cite; unglossed D-codes | B | 16 | scorer R1, R3, L4 | Glossary box; `:1591` cite; "plan answer" wording |
| B "Core 3a: `review merge --round k>=2` refused" | B | 4 | X-006 | Replaced by OD-4 (adapter or same-change refusal) |
| B `check_verify` whole-input refusal for new rows | B | 5 | X-003 | Invalid plan answers refuse; invalid new rows are demoted (Core item 4); E-8 notes the conflict |
| B "first-pass blocking frozen, no upward path; verified row cannot be re-attacked" | B | 8 | concessions | `regrade_of`, `reattack_of` (Core item 2) |
| B "outside rows deferred, never block; `decide` has no sweep term" | B | 10 | concession 7 | W term (Core item 7) |
| B "mostly a port; byte-identical predicate and key set" | B | 9 | concession 5 | Removed; Cost lists the new code |
| B "applied the spread screen better than A" | B | 15 | withdrawn | Removed (Evidence opening, E-20) |
| B `defer` recomputes PASS inline (master) | B | 11 | INV-001 | Core item 7 |
| B "one re-ask, a second refusal is an X item" | B | 5 | INV-002 | Replaced by `refusals[]` and `refused_twice` (P5) |
| B Risk 8 residual "needs new design" | B | 12 | C-010 | Replaced by the explicit limit and OD-10 |
| B "Order of work" paragraph | B | 18 | staged delivery | Replaced by the stage table; its content is preserved inside it (round-1 fixes first, then the port, prompt switch, falsifier) |
| A "Cost" 50 to 70 lines estimate as an estimate for the whole design | A | 18 | scope | Kept as the Stage 0 estimate only |
| A header text `degraded: yes (<valid> of <quorum> valid blocks)` | A | 2 | INV-016 redefines degraded | Modified to `degraded: yes (<valid> of <panel_size> valid blocks, quorum <quorum>)` |
| A "It does not add positive (evidenced) clearing"; "D16c is closed as by design" (what Option A explicitly does not do) | A | 18 | the port adds it; option (i) keeps it prompt-only plus the `prior` gate | Described in the comparison table and the option (i) specification; not adopted as the target |
| A Evidence 5 sentence that D3 "would have blocked the three flips" | A | 2, 14 | not replayed | Kept as an [inference] in E-23 |
| A "Consumer modules" row text for the spec loop ("`:13` becomes enforced by code") | A | 4 | merged | Preserved in the spec-loop row |
| A Evidence 3 (verify-only already exists as a reviewer protocol; rf-qa shape) | A | none | duplicates B's E-14 and E-16 | Merged into E-14 and E-16 (no separate item) |
| A external-context bullets (Cursor, LinkedIn, Zenodo) | A | none | duplicate B's E-26 and E-28 | Merged into E-26 and E-28 |
| A "Three-round example under the default templates" (panel of 3, quorum 2, one truncated block) | A | 12 | illustration only; the rules it shows are in Core items 3 and 10 and the table | Narrative omitted; no requirement lost (T-A5, T-A6, T-A9 carry its cases) |
| B U-015 "re-ask rule: first refusal returns its list, second becomes an X item" (T-B10) | B | 5, 17 | INV-002 | Same as the "one re-ask" row: replaced in effect by `refusals[]` and `refused_twice`; T-B10 replaced by T-P2 |

Anchors present in the plan's accepted content and absent from the merged output without an entry: none found (see the Dropped-anchor audit).

## Threshold preservation check

Every numeric threshold of the plan's Threshold Preservation table, with its state in the merged file. Line numbers are lines of `proposal-merged.md` (first occurrence).

| Source | Value | State | Where in the merged file |
|---|---|---|---|
| A, B | cap 3 reviews (two fix cycles; ESCALATE at the cap) | PRESENT-exact | line 46 (Core item 0(a)); Core item 7 |
| A | `--cap` default `None`; round 1 creates with `cap or 3` | PRESENT-exact | line 47 (Core item 0(b)) |
| A | `quorum = min(2, panel_size)`; quorum 1 for a lone reviewer; panel of 3 gives quorum 2 | PRESENT-exact (meaning of `degraded` modified to `valid < panel_size`, INV-016, logged) | line 63 (Core item 3) |
| A | about 50 to 70 added lines in `ledger.py`, about 15 in `merge_cmd.py` | PRESENT-exact as the Stage 0 estimate only; dropped as an estimate for the whole design (logged) | Core item 0(d); Cost table line 537 |
| A | 37 tests in the two gate files (24 + 13), 178 skill-text tests | PRESENT-exact | line 438 (Test coverage) |
| A | 1 test rewritten into 2, about 14 new, 15 listed | PRESENT-modified-with-log (the merged list is larger: T-A1 to T-A15 plus B, probe and amendment groups) | New tests table |
| B | 24 existing ledger tests: 9 replaced, 15 renamed | PRESENT-exact (`:376-385` listed once) | line 443 |
| B | 2,668-line script; 1,578-line test file; 77 test functions; about 650 reviser-side lines (`:940-1590`) | PRESENT-exact (the "mostly a port" wording modified, logged) | lines 34, 248, 419; Cost table |
| B | 13 frozen row fields | PRESENT-modified-with-log (two named exceptions: `regrade_of`, `reattack_of`) | line 295 (P2); Core item 2 |
| B | exit codes 0 PASS, 10 REVISE, 11 ESCALATE, 12 PENDING (sweep-required lenses only); refusal exit codes 1, 2, 3, 4 | PRESENT-exact | lines 163, 222 (CLI surface) |
| B | `E-CAP`: refuse a fourth review or a third fix cycle | PRESENT-exact | line 96 (Core item 7); Core item 0 is the master-ledger equivalent |
| B | "one re-ask, a second refusal is an X item and ESCALATE" | PRESENT-modified-with-log (two refusals record an ESCALATE round with `refused_twice`) | line 88 (Core item 4); P5 |
| B | 89% (review 2) and 100% (review 3) `origin=changed`, n = 2 + 2 | PRESENT-exact with its limits | lines 228, 263 (E-19); P4 |
| A, B | new CRITICAL+MAJOR labels 11/9/8 and 12/7/4 (controls), 13/9/3 (ledger arm); improvement 3 versus spread 4 | PRESENT-exact | line 264 (E-20) |
| A, B | 264 merges, 0 violations; 49 `3-dropped-blocking` lines, 48 length rejections; 3 verdict flips; 195 chained rows and 83 mega-rows | PRESENT-exact as sourced figures (the misbooking claim stays [inference]) | lines 236, 267 (E-4, E-23) |
| B | sweep costs about 10 to 15 minutes; a loop is 13 to 17 script calls | PRESENT-exact as estimates | line 266 (E-22); Cost |
| A, B | M effort and Medium risk (A), XL and High (B) | PRESENT-exact, attached to the stages | lines 565, 568 (stage table) |
| probe | evidence quote 12 to 200 characters, widened by 3 lines | PRESENT-exact, labelled proposed | line 92 (Core item 5); Contract fields |
| A (A-01 row) | denominator `max(report count, resolution count)` | PRESENT-modified-with-log: `len(resolution.reviewers)` when a resolution is given, else the report count with the round marked `degraded` when more than one round-1 report exists (INV-007) | line 63 (Core item 3) |
| A-11, A-21 | quote bound 12 to 200 | PRESENT-exact (same as the probe row) | line 92 |

Result: 20 threshold rows checked; PRESENT-exact 16, PRESENT-modified-with-log 4 (the 1/2/about-14 test counts, the 13 frozen fields, the re-ask, the denominator), ABSENT 0. The `degraded` meaning change (INV-016) is logged inside the quorum row, which stays PRESENT-exact.

## Dropped-anchor audit

Accepted requirement-level anchors of Variant A, each either present in the merged file under a provenance tag or logged above.

| Variant A anchor | State | Where |
|---|---|---|
| 15 tests (new tests 1 to 15) | 13 appear (T-A1 to T-A9, T-A11, T-A13, T-A14, T-A15; T-A5, T-A7, T-A8 rewritten to the A-01 table); T-A10 replaced by T-B3; T-A12 dropped and logged | New tests table (tag `Source: Variant A ... "New tests" 1-15`) |
| 1 existing test rewritten into 2 (`:376-385`) | appears | Existing-tests table, row `:376-385` |
| 5 core changes: cap by refusal; `--cap` conflict error; quorum of valid blocks; clearing only from a real review (D2); degraded can fail but not pass | cap, `--cap`, quorum, degraded rule appear (Core item 0(a), 0(b), Core item 3 and table); clearing-only-from-a-real-review dropped and logged ("A change 4") | Core items 0 and 3 |
| Four Round 2 self-fixes of A (atomic refusal, sticky blocking, `prior`-gated clearing with `unverified` FAIL, bounded refusal) | appear | Core item 3, register INV-011, Core item 5, option (i) specification, P5 |
| P1 to P6 | P1a, P2a, P4a (restricted), P5a, P6a appear; P3 not carried and logged (P3a note) | "Properties argued from Variant A" |
| Quorum `min(2, panel_size)` and lone-reviewer quorum 1 | appears | Core item 3 |
| Cap (3 reviews, refusal, ESCALATE at `n == cap`) | appears | Core item 0(a) |
| Additive keys under `review-ledger/1` | appears for Stage 0 keys; rejected for the port, logged | Core item 1, Contract fields |
| Telemetry (`unanswered_priors`) | dropped and logged; the late-row telemetry (U-004) appears | Contract fields note; Correctness "Two tests" |
| Seams table (parse, cluster and match, decider, verdict mapping) | appears as one paragraph (table form logged) | Core item 3 |
| Consumer rows (spec loop, tasklist, reflect, PR, rf-qa) | spec loop, rf-qa, reflect, PR appear; tasklist and the PR objection appear as rows and as the C-015 open point | Consumer modules; Other open points |
| Measurement plan (late-row rate from `row["history"][0]["round"]`, `members`, changed ranges) | appears | Correctness "Two tests"; Stage 1; Risk 19 |
| Fixture at HEAD `792cf8c52` (U-002) | appears | Core item 1; T-A13 |
| E2 flip fixture (U-005) | appears | T-A11; E-23 |
| Plugin mirror `plugins/superclaude/rules/prompts/` (U-006) | appears | Core item 3a; Consumer modules; Risk 7 |
| Evidence 1 to 9 of A | merged into E-2, E-5, E-13, E-14, E-16, E-23, E-26, E-28, E-29 to E-33 | Evidence |
| Risk rows of A (late findings, silence clears, refusal wastes a run, `--cap` default, denominator, seams, decider, drift) | late findings Risk 19, refusal Risk 13, `--cap` Risk 11, denominator Risk 12, drift in Risk 7, seams and decider in Risk 4 and the seams paragraph; "silence still clears" is replaced by the gate argument and P3 | Risks and mitigations |
| Cost rows (50-70 and 15 lines, M/Medium, sequencing, run cost, not costed here) | appear | Cost |
| "What Option A explicitly does not do" | modified and logged | Dropped table |
| Three-round example | omitted, logged | Dropped table |

Variant B anchors checked as well (U-007 to U-020): sweep (Core item 8), integrity layer (Core item 1), frozen fields and `caused_by` (Core item 2, 6), evidenced clearing (Core item 5), registry (Core item 9), falsifier (Correctness), 89%/100% (E-19), characterization pair (T-B5), re-ask (replaced, logged), existence proof (E-12), served-model flag (T-B12), three owner decisions (Cost), concatenation (Core item 10), PR and rf-qa mapping (E-16, E-17, Consumer modules): all present.

Result: anchors audited 21 groups for Variant A plus 14 for Variant B; unaccounted 0.

## Amendment application

| Amendment | Result | Reason or note |
|---|---|---|
| A-01 (PR-001) degraded-round table, denominator row | APPLIED | Table in Core item 3; A tests 7 to 9 rewritten (T-A7, T-A8, T-Gg); INV-007 checks only when `--resolution` is given; threshold row in this log |
| A-02 (PR-002) outside rows and W | APPLIED | "outside rows that would block count toward U" deleted; W term in Core item 7 and the formula; 10a, 10b, 10c applied; Risk-summary sentence "W > 0 ends a loop at round 2 without a fix cycle" in Core item 7 and Risk 1 |
| A-03 (PR-003) `defer`, `ledger release` | APPLIED | Core item 7; Core item 3 spanless wording; Risk rollback for spanless rows named in Risk 14; OD-11 |
| A-04 (PR-004) `reattack_of`, `regrade_of` | APPLIED | Core item 2 (a) to (d); P2 restated; the plan's "Strengths to Preserve" phrase has no counterpart section in the merged file, so only P2 and Core item 2 carry the restated guarantee; Change 8 risk HIGH in Risk 15 |
| A-05 (PR-005) "nothing is recorded" | APPLIED-WITH-DEVIATION | `refusals[]` rule in Core item 3, T-A1, T-A3, P1, P5, Data flow; replay rule added; deviations: `test_review_cli.py:425` assertion narrowed and a round-1 refusal before a ledger exists is marked NOT APPLIED |
| A-06 (PR-006) `min_writer` | APPLIED | Core item 1; stage table; T-P14 |
| A-07 (PR-007) partial acceptance | APPLIED | Core item 4; P1 and P6 reworded; three tests in T-Gf |
| A-08 (PR-008) tests by stage | APPLIED | Existing-tests table has Stages 0 to 2 and Stage 3 columns; key (test, stage). Placement of `:408-417` (changes at Stage 1, not in A's must-stay-green list) is the executor's reading of the amendment |
| A-09 (PR-009) register three-state | APPLIED-WITH-DEVIATION | Two design-status columns (port and option (i)); INV-003, 004, 005, 006, 017 `closed-in-port` with the four conditions; option (i) `open`; sentence replaced; deviation: the state name `closed-by-design` stands for `closed-by-Change-N`, because the merged text has no change numbers |
| A-10 (PR-010) vocabulary | APPLIED | Master field list removed from Core item 2; field classes kept in INV-011 and INV-012 rows with their scope; `members[]` in Row additions |
| A-11 (PR-011) evidence vocabulary | APPLIED | Core item 5 parts (a) and (b); the claim that INV-003 and INV-004 need new rules inside the port deleted |
| A-12 (PR-012) engine behind `ledger revise` | APPLIED | Core item 3a; Stage 3 removal in Risk 7 rollback; seams paragraph under Core item 3 |
| A-13 (PR-013) NOT-Being-Made rows | APPLIED | C-015, A-005, A-001/A-003, seams preserved: in the register of Open decisions and in the "Dropped or paraphrased anchors" table; denominator row in A-01 |
| A-14 (PR-014) neutrality | APPLIED | (1) wording replaced (logged row); (2) symmetrical sentence in Cost; (3) option (i) specification in Cost; the gate argued both ways |
| A-15 (PR-015) test groups and Change 8 risk | APPLIED | T-Ga to T-Gg; Risk 15 HIGH with the stated rationale |
| A-16 (PR-016) order and splits | APPLIED | Order followed; Change 5 merged with Change 6; Change 10 split into 10a to 10c; test table skeleton with the five columns; stage table; no changelog paragraph at the top |
| A-17 (PR-017) Change 1 wording | APPLIED | Core item 0(a), T-A2 |
| A-18 (PR-018) line 135 | APPLIED | E-20 |
| A-19 (PR-019) targets | APPLIED | Risk 3 Mitigation cell for Change 14; intro paragraph under How it works for Change 18 (said so in the Change 18 entry); Order of work one paragraph; Evidence D E-19 to E-24; Risk 6 not targeted; G9 and G10 glossed in Test coverage |
| A-20 (PR-020) names | APPLIED | OD-1 to OD-11; `ledger answer` kept; "plan answer" and "verifier answer" used |
| A-21 (PR-021) labels | APPLIED-WITH-DEVIATION | The plan's Overview and Risk Summary have no counterpart in the merged proposal; "Stages are delivery stages" is in the glossary and Stage membership is in the stage table; the denominator and 12-to-200 threshold rows are in this log's Threshold check |

Result: APPLIED 18, APPLIED-WITH-DEVIATION 3 (A-05, A-09, A-21), NOT APPLIED 0. (A-08 is counted as APPLIED; its one reading is noted in the row.)

## Deviations from the plan

1. **Change 5 stage membership.** Amendment A-21 puts Change 5 in Stage 1; Change 18 lists it under the Stage-2 option (ii). The merged stage table splits it: the refusal log and bounded refusal (which both options need) are Stage 1; the demotion rules of `check_verify` are Stage 3 with the port.
2. **A-09 state name.** `closed-by-design` replaces `closed-by-Change-N`; "pinned by test X" names a planned test, and the register states that no row is closed until its test exists.
3. **A-05 side effects.** The plan says `test_review_cli.py:425` is "kept"; the merged text keeps it but narrows its assertion to "nothing but `refusals[]` is written". A round-1 refusal before a ledger exists is marked `[NOT APPLIED: ...]` because the plan does not say where `refusals[]` lives then. The orchestrator should decide this.
4. **Degraded header wording.** A's `degraded: yes (<valid> of <quorum> valid blocks)` is changed to `... of <panel_size> valid blocks, quorum <quorum>)` because INV-016 redefines `degraded` as `valid < panel_size`.
5. **No change numbers in prose.** The stage table and Open decisions refer to Core items; plan change numbers live only in provenance comments, so every reference resolves inside the merged file.
6. **Added evidence subsection F (E-29 to E-33) and subsection "Properties argued from Variant A" (P1a to P6a).** The plan names no new evidence ids or property ids; they were added to carry A's evidence and P1 to P6 anchors under the anchor-level rule.
7. **Risks table extended (rows 11 to 20).** The plan's Risk Summary is plan-level; its rows and rollbacks were folded into new risk rows and into the Mitigation cells of Risks 1 to 10 rather than copied one per change.
8. **Interpretation of Change 10(c).** After A-02 replaced clauses (b) and (c), the default is taken from the title of Change 10 and from "10c (the default and OD-1)": W counted until the late-row rate is measured; the older-defect clause is kept as today until OD-2.
9. **Stage 0 size estimate.** The plan attaches A's 50-to-70-line estimate to the wider Stage 0 (cap, quorum, atomic refusal, `defer`); A's estimate covered A's own five changes. Kept as the plan says, marked [inference], with the caveat in Core item 0(d) and the Cost table.
10. **F6 owner.** The probe names owners for F4 (C05 hook) and F5 (C01) only; F6's owner is stated as not named by the probe.
11. **Inputs not read in full.** The plan said read all inputs first. Read in full: `variant-2-original.md`, `refactor-plan.md`, `variant-1-original.md`, `invariant-probe.md`; read in part: `debate-transcript.md` (lines 330 to 523 plus a grep of the whole file), `diff-analysis.md` (lines 60 to 116, unique contributions and assumptions). Not read: `base-selection.md`, `refactor-plan-review.md`, the round and scorer raw files; their content reached the merge through the plan's embedded citations. No plan citation was found wrong.
12. **T-C1.** An id added for the skill-text pin test of Change 4 option (b), which the plan describes without a name.

## Summary
- Changes planned: 20 (Change 10 applied as 10a to 10c; Change 5 and Change 6 merged into one edit). Applied: 20, of which 4 with deviation (Changes 3, 5 with 6, 18 and 20). Not applied: 0 (one clause inside Change 3 is marked `[NOT APPLIED: ...]` in the merged text and listed above).
- Amendments: 21 of 21 applied (18 APPLIED, 3 APPLIED-WITH-DEVIATION: A-05, A-09, A-21).
- Merged file: 623 lines, 24,017 words; 1 H1, 9 H2, 24 H3; 103 `Source:` tags (77 with `Disposition:`).
- Validation: references 146 total, 146 resolved, 0 broken; heading hierarchy PASS; new contradictions 0 after 3 found and fixed; thresholds 20 checked, 16 PRESENT-exact, 4 PRESENT-modified-with-log, 0 ABSENT; anchors audited 35 groups, 0 unaccounted.
- Items for the orchestrator: the round-1 pre-ledger refusal (Deviation 3); OD-11 consequence (a spanless row ends in ESCALATE at Stage 3 if the owner declines `ledger release`); the Change 5 stage split (Deviation 1); the INV-010 sufficiency claim is conditional and 10 HIGH probe items remain UNADDRESSED by debate.

## Orchestrator validation of the merge (added by the debate-orchestrator after the executor returned)

Independent checks run by the orchestrator on `proposal-merged.md` (read-only batch plus targeted reads), separate from the executor's own validation above:

| Check | Result |
|-------|--------|
| Header provenance comments and title | present (three header comments, then the H1) |
| Heading hierarchy | 1 H1, 9 H2, 24 H3, 0 deeper; matches the executor's count; no level gap |
| `Source:` tags / `Disposition:` tags | 108 lines contain `Source:` and 77 contain `Disposition:` (counted before the orchestrator's edit below). The executor counted 103 provenance tags; the difference is prose lines that use the word, such as "Source: the Round 2.5 probe..." in the Invariant register, which are not tags |
| Emoji | none |
| Leftover contradictory wording | no "count toward U", "enters U" outside provenance comments; "nothing is recorded" survives only inside the sentence that explains why it was replaced by the `refusals[]` rule |
| Unresolved conflicts S-006, C-013, A-002, A-004 | all four in "Open decisions and unresolved conflicts" with both advocates' final positions |
| Probe findings INV-001 to INV-020 | all 20 present in the Invariant register with probe severity, probe status UNADDRESSED/ADDRESSED and the design status; the register states no row is closed until its acceptance test exists |
| Variant A test anchors T-A1 to T-A15 | all 15 present (T-A10 replaced, T-A12 dropped, each with its reason) |
| New amendment test groups T-Ga to T-Gg | all present |
| Thresholds spot-checked | `min(2, panel_size)`, `cap or 3`, 2,668, 77, 89%, 1,578, 650, 37 tests, 178, 264, 49 and 48: present; the three label series appear as `11/9/8`, `12/7/4`, `13/9/3` (no spaces) in one place |
| Neutrality | the only "safer" sentence is P4a, which restricts the claim to the cap and quorum changes; the gate is argued both ways |

Edits made by the orchestrator to `proposal-merged.md` after the executor returned (both in "Other open points kept visible"): (1) a bullet that keeps the executor's `[NOT APPLIED]` item visible in the open-points list: where `refusals[]` lives when a round-1 refusal happens before any ledger exists (the plan did not say; the bound "two refusals, then ESCALATE" does not yet cover round 1); (2) a bullet on the length of the document (about three times the base). Both carry a `Source:` comment.

Not independently verified by the orchestrator: the executor's totals (146 references, 35 anchor groups, 20 thresholds) were not recomputed; the 24,000-word text was read in part (header, Invariant register, Cost and stage table, Open decisions), not line by line. The executor itself did not read `base-selection.md`, `refactor-plan-review.md` or the raw round files in full (its Deviation 11); their content reached it through the plan.

Executor deviations 1 to 12 are accepted as recorded; two need an owner decision and are listed in the merged proposal: the round-1 refusal before a ledger exists (new open point) and the consequence of declining `ledger release` (OD-11).
