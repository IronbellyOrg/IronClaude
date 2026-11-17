# Score Re-evaluation: slot C-06 limits-repair-policy (Step 3, position-bias disagreements)

Re-evaluator verdicts are FINAL. Variant A = `variant-1-original.md` (Proposal A). Variant B = `variant-2-original.md` (Proposal B). Scored on the ORIGINAL variants. Debate files were used only as pointers to defects. Every defect relied on below was re-read in the variant text or in code/data at HEAD (read-only).

Disagreement check: comparing the `PASS1|...` and `PASS2|...` machine lines, the passes differ on exactly four pairs: Correctness 2 (A), Correctness 4 (B), Risk Coverage 1 (A), Structure 2 (A). All other 56 verdicts agree.

## Pair 1: Correctness criterion 2, Variant A

Criterion: "Technical approaches are feasible with stated constraints."

Pass 1 (MET): "section 2 item 2, `parse_block(text, *, repair=False)` with the three production call sites passing `repair=True` keeps four direct pins unmodified; section 3.2 reports an executed check at HEAD ... The manifest recording claim is a separate factual error already scored in K1."

Pass 2 (NOT MET): "The stated constraint is the manifest: A's s2 item 5 asserts the second attempt is recordable 'as attempt 2' ... for residual blocks the E1 A2 record shows the commit has already happened (`OutOfOrder`) ... The recording design is not feasible as stated."

Re-check at HEAD:
- Variant A section 2 item 5: "`record_attempt` raises only when the earlier attempt `complete`d ... The re-ask is therefore recorded as attempt 2 and adds no vote." Section 7 point 6 repeats it ("an attempt-2 record in a manifest that already supports it (`manifest.py:378-383`)").
- `src/superclaude/cli/review/manifest.py` `record_attempt`: `if stage in m["stages"] or _next_state(m["state"]) != stage: raise OutOfOrder(...)` (lines 371-372) runs before the `earlier[-1]["completion"] == "complete"` test. So A's "raises only when" is false.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:342` (step 3) says "record each attempt's completion the same way with `--stage collected`, then advance `collected`. A stage accepts attempts only while it is the next stage to commit." The Normalize step with the re-ask is `:343` (step 4), after `collected` is committed. So a re-ask in the reflect flow cannot be recorded as attempt 2 under the stated manifest constraint. A's own cited run (E1 A2, quoted in variant B section 3.2) hit exactly this refusal.

CLAIM: A's approach is not feasible within the manifest constraint it states, because the one mechanism A names for recording and counting the re-ask (attempt 2, no extra vote) is refused by the manifest in the sequence the skill prescribes.
EVIDENCE: variant A section 2 item 5 and section 7 point 6 versus `manifest.py:371-372` (OutOfOrder once the stage is committed) and `SKILL.md:342-343` (`collected` committed in step 3, re-ask in step 4). Supporting pointer, not re-run by me: round2.5-fault-finder-raw.md INV-017 [RAN] reports that A's cut prefix can match a `deferred` row and turn today's refusal into PASS, which conflicts with A's own INV-I row "Preserved ... moves toward FAIL". The executed anchor-locates check in A section 3.2 shows the truncation half is feasible, but the re-ask half depends on the manifest mechanism, and B shows the contrast: B defers the record shape to slot C-08 instead of claiming the manifest already supports it.
VERDICT: NOT MET. (Pass 1 treated this as only a K1 factual slip; the criterion tests whether the stated mechanism can work under the stated constraint, and it cannot.)

## Pair 2: Correctness criterion 4, Variant B

Criterion: "No internal contradictions."

Pass 1 (NOT MET): B-X1 section 4.4 totals and 4.6 "all 5 re-asked blocks recorded valid afterwards" versus the E3 row "reviewer 2 still had two bad citations"; B-X2 section 4.2 "none of the 42 merges where a blocking row survived" versus its own table (3 of the merges have no blocking row left); B-X3 "four boundary assertions" versus the `card_convert.py` pin.

Pass 2 (MET): "The s4.4 '5 of 5 recorded valid' vs E3 row is an overstatement (K1), but the text says 'recorded valid' and marks the E3 value 'to be confirmed', so it is reconcilable, not a contradiction."

Re-check:
- B section 4.4 table, E3 row: "reviewer 3 fully fixed; reviewer 2 still had two bad citations; '3 of 3 (to be confirmed by `review cluster`)'". The totals paragraph then says "5 re-asks, and all 5 re-asked blocks recorded valid afterwards", and section 4.6 and section 8 point 5 repeat "5 of 5". The source file `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboE-r3/panel/notes.md` line 2 reads "reviewer 2's re-ask still has two bad citations ... which are left as written", and line 3 "Valid blocks after re-ask: 3 of 3 (to be confirmed by `review cluster`)". The word "recorded" does not reconcile "all 5 valid" with a row that says one of the five still has bad citations; the document asserts both.
- B section 4.2 closing paragraph: the refusal fires "on none of the 42 merges where a blocking row survived". The same section's table says 42 distinct (row, package) merges hold a dropped blocking line and "4 rows in 3 merges" end with no blocking row left. Those 3 are inside the 42, so merges with a surviving blocking row number 39, not 42. This is an arithmetic self-contradiction inside one section (I did not recompute `flags.tsv`; the contradiction is between B's own numbers).
- B-X3 (four versus five boundary assertions) is a tension between sections 2/3.1 and 5, but B never states the pin count for `card_convert`; I verified `tests/review/test_review_card_convert.py:500` asserts `len(f["claim"]) == 300` and `card_convert.py:86` holds `MAX_CLAIM = 300`, and I treat it as an omission, not a stated opposite. It is not needed for the verdict.

CLAIM: B contains at least two stated-opposite pairs inside the document (5 of 5 valid versus an E3 reviewer still invalid; 42 merges with a surviving blocking row versus 3 of those 42 with none).
EVIDENCE: B section 4.4 totals paragraph and E3 row; B section 4.2 table and closing paragraph (quotes above).
VERDICT: NOT MET. (The same 5-of-5 defect was scored NOT MET under Correctness 1 by pass 2; a document that states a count and its own row disagreeing is a contradiction, and A was held to this same standard in both passes.)

## Pair 3: Risk Coverage criterion 1, Variant A

Criterion: "Identifies at least 3 risks with probability and impact assessment."

Pass 1 (NOT MET): "only the re-ask exposure is bounded (section 7 point 5 ...). Wrong occurrence (point 4) gives a qualitative likelihood only ... false-blocker rows (M2) have a stated impact ... but no likelihood."

Pass 2 (MET): "(1) re-ask recovery risk, quantified 'at most 4 of 92 lines (1 of 49 blocking) depend on re-ask recovery' ... (2) wrong occurrence, 'A shorter prefix is more likely to match twice' ... (3) false-blocker rows ... (4) meaning loss in a cut claim. Probabilities are mostly qualitative but each risk has a stated likelihood and impact."

Re-check against the variant text. Three risks carry both a probability signal and an impact:
1. Re-ask recovery: section 7 point 5, "at most 4 of 92 lines (1 of 49 blocking) depend on re-ask recovery"; impact in section 5 M3, "the position reduces to truncation plus itemised drops, and the residual is a fail-closed question for C-03."
2. Anchor that does not locate: section 3.2, "Luna's verbatim anchor fidelity is 91.4 percent ... A non-verbatim anchor fails to locate cut or uncut", with the impact "kept with `anchor_status: missing` and `span None` ... a visible row, where today it is dropped and no row exists." The 91.4 percent figure is tagged [UNVERIFIED for long anchors], but the criterion asks for an assessment, not a verified one.
3. Wrong occurrence: section 7 point 4, "A shorter prefix is more likely to match twice, and `locate` takes the first match ... the one I cannot close from code: M1 measures it", with impact (binds to the earlier occurrence; the row clears or matches wrongly) and a stated kill line in M1 ("fewer than 75 percent of the 48 blocking length lines ... located and unambiguous").
Risk 3 of pass 2's list (false-blocker rows, M2) and the meaning-loss risk have impact but no likelihood, and I do not count them. Pass 1 undercounted by treating only numeric bounds as probability.

CLAIM: A identifies three risks, each with a probability signal (numeric bound, a stated fidelity rate, a comparative likelihood with a measurement and kill line) and a stated impact.
EVIDENCE: A section 7 point 5; A section 3.2 ("91.4 percent" and "`anchor_status: missing`"); A section 7 point 4 and section 5 M1 (quotes above).
VERDICT: MET.

## Pair 4: Structure criterion 2, Variant A

Criterion: "Consistent hierarchy depth (no orphaned subsections)."

Pass 1 (MET): "H2 sections 1 to 7; H3 only under 3 (3.1 to 3.4) and 4 (4.1); no H4."

Pass 2 (NOT MET): "s4 'Invariants' contains a table followed by exactly one subsection, '### 4.1 Consistency with the adjudicated slots': a lone subsection with no sibling ... The lone 4.1 is an orphaned subsection."

Re-check of the heading outline of `variant-1-original.md`: H2 1 to 7. H3 headings exist only at 3.1, 3.2, 3.3, 3.4 (line 29, 42, 49, 55) and 4.1 (line 71). Section 4 holds a table and then one H3 and nothing else; there is no 4.2. For B, section 3 has 3.1 to 3.6 and section 4 has 4.1 to 4.6, so every subsection has siblings. Pass 1 recorded only that every H3 has an H2 parent and there is no H4, which is true of both variants and would make the "no orphaned subsections" test unfailable for any document built from this template. A single H3 under an H2 is the standard outline-hygiene defect (a 4.1 with no 4.2), and it is the only structural difference between A and B on this criterion; the two passes disagree only on whether that counts.

CLAIM: A's section 4 has a single subsection (4.1) with no sibling, so the hierarchy is inconsistent with the sibling-bearing sections 3 (3.1 to 3.4) and with every subsection in B.
EVIDENCE: `variant-1-original.md` heading lines: `### 3.1`, `### 3.2`, `### 3.3`, `### 3.4`, `### 4.1 Consistency with the adjudicated slots`; no `### 4.2`.
VERDICT: NOT MET.

## Final verdict table

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| Correctness 2 (feasible with stated constraints) | A | MET | NOT MET | NOT MET | The attempt-2 manifest record A relies on is refused by `manifest.py:371-372` once `collected` is committed, which the reflect step order (`SKILL.md:342-343`) guarantees. |
| Correctness 4 (no internal contradictions) | B | NOT MET | MET | NOT MET | B says all 5 re-asked blocks are valid while its own E3 row says reviewer 2 still has bad citations, and says 42 merges kept a blocking row while its own table leaves 3 of those 42 with none. |
| Risk Coverage 1 (3 risks with probability and impact) | A | NOT MET | MET | MET | Three risks (re-ask dependence "at most 4 of 92", non-locating anchor at 91.4 percent verbatim, wrong occurrence with the 75 percent kill line) each carry a probability signal and an impact. |
| Structure 2 (consistent depth, no orphaned subsections) | A | MET | NOT MET | NOT MET | Section 4 has the lone subsection 4.1 with no 4.2, while sections 3 in A and 3 and 4 in B carry multiple siblings. |

## Final per-variant qualitative totals

Agreed verdicts from both passes plus the four final verdicts above.

Variant A NOT MET set: Completeness 1, Correctness 1, 2, 3, 4, Structure 2, Clarity 4, Risk Coverage 2 (eight).

Variant B NOT MET set: Correctness 1, 4, Clarity 4 (three).

| Dimension | Variant A | Variant B |
|---|---|---|
| Completeness | 4 / 5 | 5 / 5 |
| Correctness | 1 / 5 | 3 / 5 |
| Structure | 4 / 5 | 5 / 5 |
| Clarity | 4 / 5 | 4 / 5 |
| Risk Coverage | 4 / 5 | 5 / 5 |
| Invariant & Edge Case Coverage | 5 / 5 | 5 / 5 |
| **Total met** | **22 / 30** | **27 / 30** |
| **qual_score** | **0.7333** | **0.9000** |

Cross-check against the passes: A pass 1 was 23 and pass 2 was 22; the three A pairs moved by +0 net (K2 to NOT MET: -1 from pass 1, S2 to NOT MET: -1 from pass 1, R1 to MET: +1 from pass 2 side), giving 22. B pass 1 was 27 and pass 2 was 28; K4 settles at NOT MET, giving 27.

### Edge Case Floor Check (Invariant & Edge Case Coverage, floor 1 of 5)

| Variant | Score | Eligible as base |
|---|---|---|
| A | 5 / 5 | Yes |
| B | 5 / 5 | Yes |

The floor is not suspended (neither variant scores 0 of 5; the dimension has no disagreement).

### Machine-readable verdicts

REEVAL|Correctness|2|A|NOT MET
REEVAL|Correctness|4|B|NOT MET
REEVAL|Risk Coverage|1|A|MET
REEVAL|Structure|2|A|NOT MET
FINAL_QUAL|A|22
FINAL_QUAL|B|27

END-OF-SCORE-FILE
