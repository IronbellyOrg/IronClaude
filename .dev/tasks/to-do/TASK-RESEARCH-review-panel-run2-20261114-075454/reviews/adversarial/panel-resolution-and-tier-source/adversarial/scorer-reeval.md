# Position-Bias Re-Evaluation (Step 3) - slot C-09 panel-resolution-and-tier-source

Re-evaluator verdicts are FINAL (scoring-protocol A.5). Variant A = `variant-1-original.md`, Variant B = `variant-2-original.md`. Sources re-read: both variants in full, `scorer-pass1.md`, `scorer-pass2.md`, rubric A.2 and A.5. Pass 1 labels K#/S#/RK#; pass 2 labels K#/S#/R#; same criteria.

## Standards applied (the same for A and B)

- K2 (feasible with stated constraints): MET when the core approach can be built under the constraints the variant itself states, and the variant states what it costs. A design flaw that contradicts another sentence belongs to K4, an overclaim to K1; neither is re-counted here.
- K3 (terminology): NOT MET only when one label or term carries two meanings in the same document with no disambiguation. An overclaimed statement is not a terminology fault.
- S3 (separation of concerns): NOT MET when a design element is first introduced (not merely evaluated) inside the evidence section, so the design section is incomplete without it.
- RK1: each counted risk needs a stated impact plus a likelihood given as a measured rate, a stated certainty, or an explicit trigger condition. Neither variant uses graded (low/medium/high) probabilities, so the same reading applies to both.
- RK2: a risk has a mitigation when the document names a procedure, a detector, a fail-loud behaviour or a scope cut that limits it, anywhere in the document. A risk stated as accepted "by design" with nothing else is unmitigated.

## Re-evaluation table

| Criterion | Variant | Pass 1 | Pass 2 | Final verdict | Reasoning |
|---|---|---|---|---|---|
| K2 Technical approaches feasible with stated constraints | A | NOT MET | MET | **MET** | The strict default, the vendor lookup and the scarcest-first order are buildable under the constraints A states, and A prices the cost (4.2: "The pin `test_review_cli.py:56-61` is rewritten with the change ... I do not call that 'pins unmodified'"; 3.3: strict gave "0 skipped slots in 40 of 40 gateway runs"); pass 1's evidence (spec loop not unchanged, exit rule never fires) is a contradiction scored under K4, and B's K2 is MET on the same footing. |
| K3 Terminology consistent and accurate | A | NOT MET | MET | **MET** | A scopes its terms explicitly: "the package owns the tier data ... the Coder env stays the runtime owner of which model each slot serves" (sec 1) and the 2.1 table row "model id behind a slot ... stays outside"; "single source" is an overclaim (K1/K4), not a term used in two senses, and "fails loudly" is not in A's sec 1 text, where the loud exit is stated once in 2.3 item 3. |
| K3 Terminology consistent and accurate | B | MET | NOT MET | **NOT MET** | B uses the label "E2" for two things: its own evidence item ("E2. `ccsession-models.json` reaches workspaces ...", sec 3) and the E2 experiment ("owner order in the E2 harness" in E6; "the E2 default panel" in E10; "neither E1 nor E2 used" in sec 5 item 4; "the choice of E2 panels" in sec 8), so "E1 nor E2" in sec 5 item 4 reads as B's own E1 and E2; A has no such collision (its evidence is numbered 3.1-3.5 and "E2" only ever means the experiment). |
| S3 Separation of concerns | A | MET | NOT MET | **NOT MET** | A first introduces two design elements inside the evidence section and not in sec 2: the scarcest-tier-first slot order (3.3, third bullet; sec 2.3 item 4 only points to it with a wrong pointer "see 3.4") and the marker-variable list for environment detection ("Under A, detection stays a function of the env but reads a named list of marker variables ... (design inference)", 3.4), which sec 2 never states; B's equivalent material (overlay, derive-and-compare, additive keys) is defined in its sec 2 and only evaluated in sec 3/E9. |
| RK1 At least 3 risks with probability and impact | B | MET | NOT MET | **MET** | B's sec 4 "Endangered or conditioned" gives four risks with impact and a likelihood handle: DR-014 repeated model (E4 rates "18 of 40", "30 of 40", "40 of 40" soft repeats), overlay reproducibility ("two workspaces resolve the same template to different models, and `tiers_sha256` differs"), cross-repo ordering ("fails every workspace whose env lacks the slot"), table-parse fragility ("a layout change ... breaks it loudly"); this is the same grade of probability A gets credit for in 4.2 (spec-loop panel "from 4 reviewers to as few as 2" with the sec 3.3 rates, INV-L "every existing shadow run", availability "40 of 40"), so ruling B NOT MET would require ruling A NOT MET too. |
| RK2 Mitigation for each identified risk | B | NOT MET | MET | **MET** | Each of B's risks has a named limiter: table fragility "breaks it loudly, which is the intended direction"; reproducibility "the overlay records `tiers_source` so a replay can tell which tiers it used" (plus frozen tiers in goldens, E9(c)); cross-repo ordering is handled by the ordering rule in sec 2 ("after the Coder `defaults.sh` carries the matching slot") and E6; DR-014 by `distinct_models`/`requested_slots`, reflect strict (`SKILL.md:340`) and the spec loop's quorum floor (E7, sec 7); unlike A's INV-L ("degrades the parity evidence ... by design of that script", nothing else), no B risk is left as accepted-with-nothing. |

## Corrected qualitative totals (54 agreed pairs from the two files + these six)

Variant A (agreed: C1-C5 MET; K1 NM, K4 NM, K5 MET; S1, S2, S4, S5 MET; L1-L3, L5 MET, L4 NM; RK1, RK3, RK4, RK5 MET, RK2 NM; IE1-IE5 MET; plus final K2 MET, K3 MET, S3 NOT MET):

| Dimension | Variant A | Variant B |
|---|---|---|
| Completeness | 5/5 | 4/5 |
| Correctness | 3/5 | 2/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **Total met** | **25/30** | **24/30** |
| **qual_score** | **0.8333** | **0.8000** |

Variant B (agreed: C2-C5 MET, C1 NM; K1 NM, K2 MET, K4 NM, K5 MET; S1 NM, S2-S5 MET; L1-L3, L5 MET, L4 NM; RK3-RK5 MET; IE1-IE5 MET; plus final K3 NOT MET, RK1 MET, RK2 MET).

NOT MET list: A = K1, K4, S3, RK2, L4. B = C1, K1, K3, K4, S1, L4.

Edge case floor: A 5/5, B 5/5, both eligible.

### Verdicts changed

| Relative to | Variant A | Variant B | Both |
|---|---|---|---|
| Pass 1 (input order A,B; 24/30 and 24/30) | 3 changed (K2, K3, S3) | 2 changed (K3, RK2) | 5 of 6 |
| Pass 2 (reverse order B,A; 25/30 and 23/30) | 0 changed | 1 changed (RK1) | 1 of 6 |

Each of the six final verdicts equals exactly one pass, as required for a disagreement pair; five equal pass 2 and one (B, RK1) equals pass 1.

Status: Complete
