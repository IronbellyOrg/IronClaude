# Base Selection Report

Generated: 2026-11-14T16:50:38Z. Variant A = Proposal A (`variant-1-original.md`, default model, default persona); Variant B = Proposal B (`variant-2-original.md`, default model, default persona). The two original proposals are scored; the debate outcome is not. Scorer files: `score-pass1.md` (quant layer + input-order pass), `score-pass2.md` (reverse-order pass), `score-reeval.md` (re-evaluation of the 4 disagreements), `quant-score.py` and `quant-score-output.json` (deterministic layer; the scorer ran it twice with identical output). Full CEV text (claim, evidence, verdict) for every criterion is in the two pass files; the tables below give the final verdict with a short excerpt of the evidence.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Proposal A) | Variant B (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 1.0000 (14 of 14 stem sets) | 1.0000 (14 of 14) |
| internal_consistency | 0.25 | 0.9725 (3 contradictions / 109 claims) | 0.9792 (3 / 144) |
| specificity_ratio | 0.15 | 1.0000 (60 concrete lines, 0 vague) | 1.0000 (120, 0) |
| dependency_completeness | 0.15 | 1.0000 (6 of 6 refs) | 1.0000 (13 of 13) |
| section_coverage | 0.15 | 0.7778 (7 H2 / max 9) | 1.0000 (9 H2 / max 9) |
| **quant_score** | | **0.9598** | **0.9948** |

Notes from the scorer (`score-pass1.md` 1.3 and 1.4): the three intra-variant contradictions per variant are listed there with both sides quoted (A: "touches no field the limits do not name" vs the copy-to-`refs` rule; "exact prefix" vs claim 297 plus `...`; "at most 4 lines" vs a derived upper bound. B: "5 of 5" vs the E3 row; "none of the 42 merges where a blocking row survived" vs its own 3-merge no-survivor rows; "four boundary assertions" vs the `card_convert` pin). RC is 1.0 for both because the prescribed keyword stem sets are loose (A matches the stems for the fail-closed and raise-limits requirements incidentally although it declines both); the qualitative layer carries that difference.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Two position-bias passes (pass 1 in order A, B; pass 2 in order B, A). Final verdict = the agreed verdict, or the re-evaluation verdict where the passes disagreed. Excerpts are from the pass-1 CEV text unless a re-evaluation row is shown.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence (excerpt) | Variant B | Evidence (excerpt) |
|-----------|-----------|--------------------|-----------|--------------------|
| Covers all explicit requirements from source input (R01 to R14) | NOT MET | R04 (fail-closed handling of a dropped blocking line) is declined: section 4.1, "Silent on: whether a residual dropped blocking line should make the merge fail closed? ... it is not part of A". R05 (raise-the-limits option) is not evaluated anywhere; search... | MET | R04 section 3.3 ("New refusal reason `dropped-blocking`"); R05 section 3.5 ("The raise-the-limits lever (B-raise)"); R06-R08 section 5 (INV-C, INV-I, INV-G rows); R09 section 6; R10 section 7; R11 section 8; R12 section 2 table; R13 section 4.1 ("The loss u... |
| Addresses edge cases and failure scenarios | MET | section 3.2, a non-verbatim anchor "fails to locate cut or uncut ... kept with `anchor_status: missing`"; section 7 point 4, a shorter prefix "more likely to match twice"; section 5 M3, re-ask recovery "near zero" and the prompt "rewrites unlisted lines". | MET | section 3.2, "A transport without the capability gets itemise-only plus the fail-closed rule of 3.3, never a truncation"; section 3.3, the acknowledgement exit "so that it cannot deadlock when a re-ask is impossible or fails"; section 4.4 rows A2, E3 (re-as... |
| Includes dependencies and prerequisites | MET | section 4.1, "**Dependency:** if 'called from inside both parsers' is read as unconditional (no keyword), `test_review_findings.py:113,117` and `test_review_findings_v2.py:200,241` must be rewritten"; C-02 and C-03 rows "consistent and dependent". | MET | section 2, "Where B is conditional on one: C-03's refusal object (without it B's fail-closed rule has no vehicle and falls back to a warning), and C-02's `block_ok` filter on clearing". |
| Defines success and completion criteria | MET | section 5 M1, "Position A is wrong on its central claim if fewer than 75 percent of the 48 blocking length lines come out located and unambiguous"; M2 and M3 each name a failure condition. | MET | section 6 table, M1 "the `dropped-blocking` refusal fires on exactly the 3 merges of 4.2 and on none of the other 261"; T-B1 to T-B5 with "holds / any counterexample". |
| Specifies what is explicitly out of scope | MET | section 4.1, "Silent on: whether a residual dropped blocking line should make the merge fail closed ... it is not part of A"; section 5 M3 "the case for the truncation half" is separable from the re-ask half. | MET | section 3.6 "What B does not do: No truncation step, no normaliser in front of the parser ... no change to a reviewer's `blocking`, `severity` or any other field"; section 9 lists facts it does not settle. |
| **Subtotal** | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence (excerpt) | Variant B | Evidence (excerpt) |
|-----------|-----------|--------------------|-----------|--------------------|
| No factual errors or hallucinated claims | NOT MET | section 2 item 5 says `record_attempt` "raises only when the earlier attempt `complete`d" and that the re-ask "is therefore recorded as attempt 2". `src/superclaude/cli/review/manifest.py` (read at HEAD) also raises `OutOfOrder` when `stage in m["stages"]`... | NOT MET | section 4.4 and 4.6 state "5 of 5 re-asked blocks recorded valid" while the E3 row in the same table shows "reviewer 2 still had two bad citations" and an unconfirmed "3 of 3" (B-X1); section 4.2 says "none of the 42 merges where a blocking row survived" al... |
| Technical approaches are feasible with stated constraints | NOT MET | Re-evaluation (final): NOT MET. A section 2 item 5 says `record_attempt` "raises only when the earlier attempt `complete`d"; `manifest.py:371-372` raises `OutOfOrder` first, so the recording design is not feasible as stated. | MET | section 3.1 and 4.1, the classifier plus additive `dropped` key leaves accepted and rejected line sets identical; section 4.3 replay executed against HEAD parsers; section 3.3 states the C-03 refusal object as a dependency. |
| Terminology used consistently and accurately | NOT MET | the one step is called "normalise" (title and line 5), "truncate", "cut" and "repair" (`repair_line`, `repair=`); "exact prefix" is applied to `claim` on line 5 although item 7 says the claim is "297 characters plus `...`". | MET | section 3.1 defines `blocking_state` as `true`, `false` or `unknown`; "dropped", "itemise", "refusal reason `dropped-blocking`", "B-core" and "B-raise" are used with one meaning throughout (sections 1, 3.3, 3.5, 5). |
| No internal contradictions (cross-validated with IC) | NOT MET | A-X1, A-X2, A-X3 (Part 1.3); IC 0.9725. | NOT MET | Re-evaluation (final): NOT MET. B 4.4/4.6 "5 of 5 re-asked blocks recorded valid" against its own E3 row ("reviewer 2 still had two bad citations"), and 4.2 "none of the 42 merges where a blocking row survived" against its own 3-merge no-survivor rows. |
| Claims supported by evidence or rationale within the document | MET | section 3.1 table gives each figure a source and a tag (`R02:99 ... [RECOMPUTED]`); section 3.2 lists the executed check and its result. | MET | sections 4.1 to 4.3 tables with tags and the replay method ("1,222 unique report blobs ... 5,270 lines"); section 4.4 run-by-run table. |
| **Subtotal** | **1/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence (excerpt) | Variant B | Evidence (excerpt) |
|-----------|-----------|--------------------|-----------|--------------------|
| Logical section ordering | MET | 1 position, 2 design consequence, 3 evidence, 4 invariants, 5 test or measurement, 6 effect on PR review and rf-qa, 7 strongest objection and answer; the objection comes last, after the material it attacks. | MET | 1 position, 2 relation to C-01 to C-03, 3 design, 4 evidence, 5 invariants, 6 tests, 7 effect, 8 objection, 9 open facts. |
| Consistent hierarchy depth (no orphaned subsections) | NOT MET | Re-evaluation (final): NOT MET. A section 4 holds a table and a single `### 4.1` with no sibling, unlike sections 3.1-3.4 and every B subsection. | MET | H2 sections 1 to 9; H3 under 3 (3.1 to 3.6) and 4 (4.1 to 4.6); no H4. |
| Clear separation of concerns between sections | MET | evidence (3), invariants (4), tests (5), downstream effect (6) and objection (7) are separate sections. | MET | slot relations (2), design (3), evidence (4), invariants (5), tests (6), effect (7), objection (8), open facts (9). |
| Navigation aids present | MET | header legend "`R02` = `research/02-finding-contract.md`, `S05` ... `S06` ..."; internal cross-references such as "See section 7." (item 7) and "(section 5)"; DC 6 of 6 resolve. | MET | cross-references "(section 4.3)", "(section 3.3)", "Section 7"; DC 13 of 13 resolve; the INV-A..INV-N source named at the head of section 5. |
| Follows conventions of the artifact type | MET | "Status: Complete", a code-state line, tag legend, then position, design, evidence, invariants, test, downstream effect and objection, the structure the slot brief requires. | MET | "Status: Complete" at lines 3 and 224, code-state line, tag legend, same required structure plus section 9. |
| **Subtotal** | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence (excerpt) | Variant B | Evidence (excerpt) |
|-----------|-----------|--------------------|-----------|--------------------|
| Unambiguous language (no "should consider", "might", "as appropriate") | MET | SR scan of the body found 0 occurrences of all ten hedge phrases. | MET | same scan, 0 occurrences. |
| Concrete rather than abstract | MET | item 1 gives the function signature "`repair_line(obj) -> (obj', repairs)` ... runs after `json.loads` and before `_check_finding` (`findings.py:188`)"; 60 concrete body lines. | MET | section 3.1 table fixes the record shape "`{line, id, rule, field, actual, limit, blocking_state}`"; section 3.3 names the refusal reason, exit code and acknowledgement fields; 120 concrete body lines. |
| Each section has a clear purpose or can be summarised in one sentence | MET | section 1 is titled "The position in one paragraph"; sections 3 to 7 are named by function (Evidence, Invariants, test, effect, objection). | MET | section 1 "The position in one paragraph"; sections 2 to 9 named by function; section 9 "Open facts this proposal does not settle". |
| Acronyms and domain terms defined on first use | NOT MET | "GQ-017" (section 3.2 heading), "CO-8 is decided" (item 7), "DR-006" (M1), "FX-1" (section 6), "E1" and "E2" (section 3.3) appear with no definition; only R02, S05 and S06 are defined in the header. | NOT MET | "INV-C" is used in section 2 (INV-003 row) before section 5 names the source of INV-A..INV-N; "C-08", "C-10", "C-11", "GQ-017" (4.3) and "debate N-B3" (section 2 row 1) are undefined; E1 and E2 are used without a definition. |
| Actionable next steps or decision points clearly identified | MET | section 7 point 1, "if the owner reads the sentence as covering code, Position A is wrong as written and the sentence has to be amended ... or the policy changes to B"; M1 "75 percent figure is my proposal, to be fixed before the run; the owner may change it". | MET | section 3.5 and 9, "Whether the owner accepts a widening of the findings-v1 grammar (B-raise); that is an owner decision"; section 6 "Rules for each measurement are written to a file before the first run". |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence (excerpt) | Variant B | Evidence (excerpt) |
|-----------|-----------|--------------------|-----------|--------------------|
| At least 3 risks with probability and impact assessment | MET | Re-evaluation (final): MET. Three risks carry a likelihood signal and an impact: re-ask recovery (section 7 point 5, "at most 4 of 92 lines"; M3 impact), unlocated anchor (section 3.2, 91.4 percent fidelity; "kept with `anchor_status: missing`"), wrong occurrence (section 7 point 4; M1 kill line). | MET | section 8 point 1, refusal exposure "3 of 264 merges" and re-ask volume "44 reviewer runs, not 80"; section 4.3, claim cut "34 claims ... 3 to 135 characters, median 37.5, 9 cut more than 60"; section 8 point 5, repeat-violation risk with the stated consequ... |
| Mitigation strategy for each identified risk | NOT MET | most risks have one (copy-to-`refs` for lost tokens; "keep the line but mark `anchor_ambiguous`" for ambiguity; stateless prompt for the dispatch paths), but the false-blocker risk in section 5 M2 ("this is a real cost to count, not assume") has only a meas... | MET | stall exposure, the acknowledgement option (3.3); no re-ask transport, "degrades to itemise plus refusal-on-PASS-by-loss" (section 8 point 4); headless path, "B excludes that path until isolation exists" (INV-G row); repeat offenders, B-raise and the brief... |
| Failure modes and recovery procedures | MET | section 7 point 4 (on many ambiguous anchors keep the line, mark `anchor_ambiguous`, refuse to let the row clear on a `prior resolved` alone); section 5 M3 (if re-ask recovery is near zero "the position reduces to truncation plus itemised drops"). | MET | section 3.3 (refusal when the round has no blocking row and a true or unknown line was dropped; acknowledgement as the human exit); section 3.2 (transport without the capability). |
| External dependencies and their failure scenarios | MET | section 4.1 C-02 and C-03 rows; INV-I row "if those slots decide otherwise the block stays `block_ok` False with its repaired findings kept"; item 6, "`--resume` for gateway model ids is documented nowhere ... the stateless form does not depend on it". | MET | section 2 ("without it B's fail-closed rule has no vehicle and falls back to a warning"); section 3.2 (the record shape "belongs to slot C-08", E1 run A2 refusal); `--resume` "[UNVERIFIED] for other gateway ids". |
| Monitoring or validation mechanism for risk detection | MET | section 5 M4, "Track `repaired_lines_rate` per model next to first-parse compliance. A rising repair rate means the brief is failing to state the limits"; M1 to M3 replays. | MET | section 3.1 `dropped` record and the conservation property ("every non-blank line ... is exactly one of kept finding, prior line, or dropped record"); section 6 M1 to M3 and T-B1 to T-B5. |
| **Subtotal** | **4/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence (excerpt) | Variant B | Evidence (excerpt) |
|-----------|-----------|--------------------|-----------|--------------------|
| Boundary conditions for collections (empty, single-element, maximum size) | MET | section 5 Boundary, "200 and 300 characters pass both with and without repair; 201 and 301 fail with `repair=False`"; section 5 refs copy "while it has room (cap 8)" and `refs_lost` when full; a 205-character raw anchor that flattens to 190 is not repaired. | MET | section 6 T-B3, "one reviewer with only dropped blocking lines (today's refusal at `ledger.py:150-157` stays); two reviewers, one with a dropped blocking line and one with an empty valid block"; section 4.2 total-loss merges "6 of 6 and 8 of 8 lines". |
| State variable interactions across component boundaries | MET | INV-I row, "`block_ok` becomes True for a reviewer whose only fault was length, so that reviewer counts for clearing and quorum. That is a C-02 and C-03 policy over `block_ok`"; item 8, the compliance metric from a `repair=False` parse. | MET | section 2 C-02 row, "an over-limit finding line makes the reviewer `block_ok` False, so its `prior` lines do not count until the re-ask returns a valid block"; section 3.3 `block_ok` and `complete` for quorum. |
| Guard condition gaps (missing validation, unguarded type assumptions) | MET | item 3, "`finding_id` and `blocking` are read from the raw object when it is a dict"; section 4.1, the step "never creates `anchor`, `quote` or `citations`"; section 5 idempotence and non-invention tests. | MET | section 3.1, `blocking_state` is "`true`, `false` or `unknown` (absent or non-boolean `blocking`)"; section 2 C-02 row, "a `prior` line with a bad status is itemised too (`findings.py:175-186`)". |
| Count divergence (off-by-one, inclusive/exclusive ranges, unit mismatches) | MET | section 3.1, "80 reviewer-runs with `block ok false` (a count of runs, not findings)" and the unit mismatch with 92; "the '4' of `COMBO-REPORT.md:292` is not reproduced"; section 5, limit measured after `flat()`. | MET | section 4.2 distinguishes 92 lines, 49 blocking rows, 44 triples, 42 merges, 80 runs; "Four verdicts flipped ... [CODE-CONTRADICTED] as '4'"; section 4.1, "Length is counted after whitespace flattening, in characters". |
| Interaction effects when features or components combine | MET | section 5, a cut can remove `AC-0.4` found only in the tail and "change `fp` and `same_defect`" (`refs_norm`); section 3.2 and 7 point 4, a shorter prefix with `locate` taking the first match; repair combined with C-02 clearing and C-03 quorum (4.1). | MET | section 3.5, "together they leave about 4 lines in 124 for the re-ask" (B-core with B-raise); section 2, the `dropped-blocking` refusal combined with C-02 `block_ok` filter and C-03 refusal object and exit 12. |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 1/5 | 3/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **22/30 = 0.7333** | **27/30 = 0.9000** |

### Edge Case Floor Check

Invariant & Edge Case Coverage: A 5/5, B 5/5. Floor is 1/5; both variants are eligible as base. No suspension.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness K2 (Technical approaches are feasible with stated constraints) | A | MET | NOT MET | DISAGREE | NOT MET (re-evaluation) |
| Correctness K4 (No internal contradictions (cross-validated with IC)) | B | NOT MET | MET | DISAGREE | NOT MET (re-evaluation) |
| Risk Coverage R1 (At least 3 risks with probability and impact assessment) | A | NOT MET | MET | DISAGREE | MET (re-evaluation) |
| Structure S2 (Consistent hierarchy depth (no orphaned subsections)) | A | MET | NOT MET | DISAGREE | NOT MET (re-evaluation) |

Disagreements re-evaluated: 4 of 60 criterion-variant pairs (56 agreed). Final verdicts that differ from pass 1: 3; that differ from pass 2: 1. Re-evaluation outcome: Correctness 2/A took pass 2's NOT MET; Correctness 4/B took pass 1's NOT MET; Risk Coverage 1/A took pass 2's MET; Structure 2/A took pass 2's NOT MET. Net effect: Variant A 22/30 (pass 1: 23, pass 2: 22), Variant B 27/30 (pass 1: 27, pass 2: 28). The re-evaluation file is `score-reeval.md`.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (Proposal A) | 0.4799 | 0.3667 | **0.8466** | not needed |
| B (Proposal B) | 0.4974 | 0.4500 | **0.9474** | not needed |

**Margin**: 10.08 percentage points (10.6% of the leader's score), above the 5% threshold.
**Tiebreaker applied**: No. For information only: the debate's per-point tally (debate-transcript.md Scoring Matrix, 28 points) is Variant 1 clean wins 2, Variant 2 clean wins 3, Hybrid 15, Neither 4, Split 4.

## Selected Base: Variant B (Proposal B; `variant-2-original.md`)

### Selection Rationale

- Highest combined score: B 0.9474 against A 0.8466, a margin of 10.08 points, so the tiebreaker did not apply and the debate's tally played no part in the selection.
- Both layers favour B: quant 0.9948 against 0.9598 (the gap comes from section_coverage, 9 H2 sections against 7, and a marginally higher internal_consistency); qual 27/30 against 22/30.
- Where the qualitative gap comes from (final verdicts): Completeness B 5 vs A 4 (A declines the fail-closed rule and never evaluates raising the limits; Completeness 1), Correctness B 3 vs A 1, Structure B 5 vs A 4 (A's lone `### 4.1`), Risk Coverage B 5 vs A 4. Clarity (4 each) and Invariant & Edge Case (5 each) are level. Correctness losses of A found by the scorers: the manifest claim (`manifest.py:371-372` raises `OutOfOrder` before the `complete` test), the "exact prefix" wording versus the 297 plus `...` claim cut, and the "touches no field the limits do not name" sentence versus the copy-to-`refs` rule. Correctness losses of B: the "5 of 5" re-ask figure against its own E3 row, "none of the 42 merges" against its own no-survivor rows, and the four-versus-five pin count.
- Caveat recorded by the debate, not by the score: the two proposals are not what the debate converged on. Both advocates' final tables and 12-bullet resolutions converge on a hybrid in which the three location fields (`anchor`, `anchor2`, citation `quote`) are cut to 200 flattened characters in code behind a `repair=False` keyword (Proposal A's mechanism), with Proposal B's itemised record, `blocking_state`, dropped-blocking refusal and acknowledgement exit. The base therefore needs a substantial merge from A, which Step 4 plans.

### Strengths to Preserve from Base (Variant B)

1. The itemised drop record with a three-valued `blocking_state` and the per-block conservation property (U-009, T-B1), which also covers bad `prior` lines.
2. The `dropped-blocking` refusal with an owner-and-reason acknowledgement exit, riding C-03's refusal object and exit 12 (U-008, C-004; both advocates' final tables: Variant 2).
3. The replay and E1 evidence base (U-006, U-007, S-003: both advocates: Variant 2), restated as four confirmed re-asks of five, Agent path, one length cause.
4. Pre-registered measurements and tests T-B1..T-B5, including T-B5 (the re-ask carries only the reviewer's own block and grants no tool) (S-004, U-010).
5. No edit of any field other than the three location fields; claim, `refs`, `severity`, `blocking` and `category` stay as the reviewer wrote them (B's final position on C-009; unresolved, see below).
6. The raise-the-limits lever kept separate and narrowed to a claim-only raise to 450 as an owner decision (U-011).
7. The 14-row invariant table split by policy, the module-by-module table, the conflict mapping table and the "open facts this proposal does not settle" section (S-005, S-006).

### Strengths to Incorporate from Non-Base Variant (Variant A)

1. `parse_block(text, *, repair=False)` with the three production call sites passing `repair=True`, and one pure `repair_line(obj)` that cuts `anchor`, `anchor2` and `quote` to the first 200 flattened characters before the check; it keeps the over-limit pins literal (U-001, S-002, C-001 by field; both advocates' final bullet 1). Source: A section 2 items 1-2.
2. The derived first-pass carrier: `first_pass_state` and `repairs` emitted by `cluster_cmd.py:155-163` and `verify_cmd.py:136-138`, a differential test against a `repair=False` parse, and `repaired_lines_rate` next to a `dropped_lines_rate` (C-013, X-004, U-004). Source: A section 2 item 8 and Round 2 N6.
3. The stateless re-ask (the original brief, the reviewer's own block, the parser's per-line errors) and the refusal-driven v1 transport, with attempt 2 recorded in the reflect manifest only before the `collected` commit and for a non-`complete` earlier attempt (C-005, C-006, U-005, A-006). Source: A section 2 item 6 as narrowed in Round 2.
4. The cost-side verdict replay M2 and numeric kill lines (S-004, U-003; both advocates: Variant 1 / Hybrid). Source: A section 5.
5. The recorded cut with a rendered "shortened from N" note in the row's `### Lx` block and `original_sha256` of the flattened original field (C-010, C-012). `refs_changed` is recorded only, not copied (C-008, U-002).
6. The v2 loss-unit test (one over-limit line and one valid line: block `complete`, both findings reach `cluster`) (C-003; both: Variant 1). A's candid "partly endangered" label for INV-C (S-005).
7. The additive sentence after the pinned Normalize sentences of `SKILL.md:343`, with the mechanical fallback that the v2 call sites stay at `repair=False` if the owner reads "the orchestrator" as covering package code (X-001; both advocates: Variant 1).

### Points the debate left unresolved (carried to the refactoring plan as flagged conflicts)

- C-001 and C-009: whether `claim` is cut (A: 297 plus `...` with a marker and a two-judge falsifier K2; B: no claim cut by default, claim-only raise as an owner lever). Both advocates agree a claim cut is allowed only if K2 passes.
- C-002: eligibility for clearing (C-02) and quorum (C-03): A keeps the bare parser verdict on the repaired lines (`ok`/`complete`); B derives eligibility that tolerates dropped `blocking: false` lines and fails on block-level faults or unresolved `true`/`unknown` drops and drops A's `repaired == 0` knob.
- C-012: provenance wording; same mechanism on both sides once the claim cut is excluded.
