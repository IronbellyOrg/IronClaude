# Score Re-Evaluation: slot X-13 process-redesign-modules (scoring-protocol.md A.5)

Scorer: SCORER RE-EVALUATION agent. Verdicts in this file are FINAL (no appeals).
Variant A = `variant-1-original.md` (Proposal A, Sweep-Sheet-shaped). Variant B = `variant-2-original.md` (Proposal B, Recipe-Ledger-shaped). Both are scored AS WRITTEN; debate files are evidence about which of their claims are wrong or missing.
Line refs "A:n" and "B:n" are line numbers in the variant files.
Inputs read: `scoring-protocol.md` (A.2 CEV, no partial credit, no specific evidence = NOT MET), `score-pass1.md`, `score-pass2.md`, both original variants, `quant-score.py` (the IC contradiction table), and the debate files cited per pair.
Not read, per the brief: the forbidden `.dev/tasks/` folders other than this task's own.

Standard applied to all 7 pairs: a criterion phrased as a universal ("defined on first use", "each identified risk", "no contradictions") is defeated by one cited counterexample; a coverage criterion ("covers count divergence scenarios") is met by one concrete cited scenario.

## 1. The 7 disputed pairs

### Pair 1: Correctness 3 (terminology used consistently and accurately), Variant B

Comparison:
- Pass 1 (NOT MET): B:34 and B:36 use "reviewer id" for two different identifier spaces; B:38 "profile" `rowcheck` names a layer no code owns.
- Pass 2 (MET): fixed vocabulary throughout (recipe card, row block, `assigned` / `observed`, `rowcheck`, overlay), avoids the shipped noun "ledger"; the `recipes` name clash with `cli/swarm/recipes/` is an external clash, not a misuse inside the document.

CLAIM: Terminology is used consistently and accurately throughout Variant B.
EVIDENCE: B:34 "reviewer ids are `<slot_id>-<i>` (`panel.py:668`)" and B:36 "the existing sidecar `{reviewer_id: {assigned, observed}}`" use one term, "reviewer id", for the id that names a panel slot reviewer and for the key of the coverage sidecar. The sidecar key is the card file stem, `rid = card.stem` (`cluster_cmd.py:146`), `reviewer-<N>` in the reflect flow. Verified in round1-advocate-B.md:63 and :124 ("Sidecar key = card file stem ... not `<slot_id>-<i>`"), conceded by B's advocate (concession 6), re-verified in round2-advocate-A.md:74 (three id spaces: resolution ids, card stems, v1 merge ids), and ranked HIGH by the fault-finder (round2.5 INV-003: a mismatch gives `assigned = None`, which makes every clean block invalid). I agree with Pass 2 that the `recipes` clash is external and I do not count it, and I do not rest the verdict on the word "profile".
VERDICT: NOT MET.
Why final: the conflation is conceded and independently re-verified, and Pass 2 itself lists it as a verified error under its correctness.1(c) without weighing it here, although this criterion says "accurately" and a consistently repeated wrong term is not accurate.

### Pair 2: Correctness 4 (no internal contradictions, cross-validated with IC), Variant A

Comparison:
- Pass 1 (NOT MET): the IC table finds 5 debate-verified contradictions in A (A:20 vs A:110; A:43 quote of `ledger.py:3-4`; A:18 vs A:69; and others).
- Pass 2 (MET): section 1 agrees with sections 2, 3.3 and 6; section 4 names its own byte-identity risk; no advocate or fault-finder raised a contradiction between two sections of A.

CLAIM: Variant A contains no internal contradictions.
EVIDENCE: I checked each of the five IC entries (`quant-score.py` CONTRADICTIONS["A"]) for a leg inside the document, because this criterion asks for two statements of A that oppose each other, and the same facts already fail Correctness 1, 2 and 5 for A.
- A-X1 (A:20 vs A:110): A:20 says an item with no finding is reported in `observed`; A:110 says "`observed` is a declaration"; A:117 says "an item missing from `observed` is visible". These agree. What is wrong is the code fact (nothing but the orchestrator writes `observed`), which is an error against code, not against A.
- A-X2 (A:43): the quote of `ledger.py:3-4` ("Only this module changes a finding's status") does not carry the "no component edits a reviewer finding" claim. That is a support failure (Correctness 5), not an opposition between two statements.
- A-X3 (A:18, A:44 vs A:69): A:69 states the condition under which the new flags are safe ("only if ... additive and emitted only when a sheet exists"); A:89 says the core would not validate the v1 item link. No opposing pair.
- A-X4 (A:20 vs A:89): A:89 itself admits "on v1 the item link is an unvalidated key"; consistent with A:20.
- A-X5 (A:12, A:113 vs A:117): A:117 concedes only that the core cannot prove examination; A:83 and A:113 state the same fallback as A:12. Consistent.
I found no other pair of A statements in opposition. By contrast, the agreed NOT MET for B rests on a real two-statement conflict (B:22 recipes are first-review only, B:23 and B:36 tie `block_ok` to the C-02 clearing quorum that exists only in re-review) plus B-X5 (B:36, B:43 vs B:79); A has nothing of that kind, which is why equal IC values (0.8148 vs 0.8065) do not force equal verdicts.
VERDICT: MET.
Why final: the IC entries for A are false or unsupported claims against code, each already scored NOT MET under Correctness 1, 2 and 5, and none has an opposing statement inside A, so a NOT MET here would count the same defect twice under a criterion about self-contradiction.

### Pair 3: Clarity 4 (acronyms and domain terms defined on first use), Variant A

Comparison:
- Pass 1 (NOT MET): used without expansion: "G0 and D1-D7" (A:55), "INV-003" and "C-06" (A:88), "E1, E2, E5, E7" (A:25), "REQ-23" (A:61).
- Pass 2 (MET): header defines the tags and MR2; inline glosses for C4, C8, E3, E4, arm K, CB-2.

CLAIM: Acronyms and domain terms are defined on first use in Variant A.
EVIDENCE: A grep of A for `G0` returns only A:55 and A:56. A:55 "Every gate G0 and D1-D7 is a numeric design choice" never says what G0 or D1 to D7 are; D2, D7, D4 and D6 appear later by their threshold (A:55 D2, A:80 D7, A:81 D4, D6), not at first use. A:25 "Spec review: E1, E2, E5, E7 per scope slice 06 s19" is never expanded; A:27 glosses only E3 and E4. A:24 glosses C4 and C8 in the same sentence but not "C5 and C2". I do not rest on REQ-23 (glossed inline at A:61: "empty sheet equals the isolated brief by hash") or on INV-003 and C-06 (partly glossed at A:88). Pass 2's glosses are real but cover other terms, and a MET needs the first-met terms defined.
VERDICT: NOT MET.
Why final: G0 and D1 to D7 and E1/E2/E5/E7 are domain identifiers with no definition anywhere in A, so under A.2 no evidence can be cited for a MET and the criterion defaults to NOT MET.

### Pair 4: Clarity 4 (acronyms and domain terms defined on first use), Variant B

Comparison:
- Pass 1 (NOT MET): used without expansion: "INV-J" and "INV-N" (B:79), "C-08" and "X-14" (B:84, B:101), "G0 and D1 to D7" (B:65).
- Pass 2 (MET): header defines tags, `r10`, `r13`, `MR2`; inline glosses for CB-2, K, SS, and INV ids given with their content.

CLAIM: Acronyms and domain terms are defined on first use in Variant B.
EVIDENCE: A grep of B returns `G0` and `D1 to D7` only at B:65 ("Every gate G0 and D1 to D7 is a design choice no recorded run can evaluate"), with no definition; "extractors E1 to E7" at B:53 is not expanded; "X-14's rule" at B:101 is used with no gloss anywhere in B; "the H1 to H4 fixes" at B:104 is undefined; INV-L is first used at B:45 and glossed only at B:80. I do not rest on INV-J, INV-N or C-08, which carry partial glosses ("Medium non-blocking", "mirror pins", "transcript adapter"). The glosses Pass 2 cites (CB-2, K, SS, RL, Z0, `r10`) are real but do not cover these terms.
VERDICT: NOT MET.
Why final: B has the same kind of uncovered domain identifiers as A (G0, D1 to D7, E1 to E7) plus X-14 and H1 to H4, so the verdict for both variants must be the same and the cited counterexamples settle it.

### Pair 5: Risk Coverage 2 (mitigation strategy for each identified risk), Variant A

Comparison:
- Pass 1 (NOT MET): A:68 labels the endangered list "named, not resolved here"; the false-positive item (A:72) has only measurement M4, no mitigation.
- Pass 2 (MET): lists a mitigation per risk: per-class M1 gate, unit test for determinism, snapshot-path rule, additive flags, loader rule, M4 measurement, optional per-row carrier later.

CLAIM: Variant A gives a mitigation strategy for each identified risk.
EVIDENCE: A:68 heads the list "Endangered by A (named, not resolved here)". Four entries do carry a rule or gate: byte identity (A:69 additive, emitted only when a sheet exists), snapshot boundary (A:44 every attached path must be in the input snapshot), determinism (A:71 a unit test must pin it), class constants (A:73 the loader must not import class names); selection recall has the M1 gate (A:78). The fifth, "The script as a second source of false positives" (A:72), ends "Advisory-only checks do not stop a bad item from occupying a reviewer's time", and A:116 answers "it can only cost reviewer time, which M4 measures": a measurement is detection (Risk criterion 5), not a mitigation of the cost. Unobservable compliance (A:117) is conceded ("the core cannot prove that a given item was examined") with only a contingent later carrier.
VERDICT: NOT MET.
Why final: the criterion says "each", the false-positive risk has only a measurement and A's own heading says the list is not resolved, so one cited risk without a mitigation defeats MET.

### Pair 6: Risk Coverage 2 (mitigation strategy for each identified risk), Variant B

Comparison:
- Pass 1 (NOT MET): B:82 labels the list "Endangered or left open"; INV-C v1 weaker check is accepted as "a cost of the C-01 outcome" (B:19, B:86) with no mitigation.
- Pass 2 (MET): demotion containment, `requires_tools` lint (T-B5), T-B6, compliance counted and measured (M-B1), `ran` deferred to C-08; v1 weaker check "stated as the cost".

CLAIM: Variant B gives a mitigation strategy for each identified risk.
EVIDENCE: B:82 heads the list "Endangered or left open by this position". Mitigated: demotion (B:85 off by default, never CRITICAL, own flag only, `check_skipped`), INV-G tool wall (B:84 `requires_tools` lint, T-B5 at B:97), INV-H file level (T-B6 at B:98). Not mitigated: (1) the v1 spec loop "gets a weaker check than reflect" (B:86), accepted as "a cost of the C-01 outcome" (B:19); (2) `ran` "in this proposal ... is recorded and unverified" until the C-08 adapter (B:84), a deferral to another slot; (3) for a read-only slot C4 "loses its script-run test" and its Grep equivalence is "[UNVERIFIED]" (B:84); B:118 point 5 lists what B "cannot answer from evidence". Stating a cost is an acknowledgement of the risk, not a mitigation strategy.
VERDICT: NOT MET.
Why final: at least two identified risks (v1 weaker check, `ran` unverifiable) are explicitly accepted or deferred, so the "each" in the criterion is not met, the same as for A.

### Pair 7: Invariant & Edge Case 4 (count divergence scenarios), Variant A

Comparison:
- Pass 1 (MET): A:98 reviewer lost after assignment leaves items unexamined, shown by `observed`, and does not feed C-03's `min(2, requested)` floor; A:55 D2 arithmetic 0.12 x 14 = 1.68 vs +1.33 items.
- Pass 2 (NOT MET): no off-by-one, inclusive/exclusive or assigned-versus-observed reconciliation rule is stated; the figures are evidence figures, not divergence scenarios.

CLAIM: Variant A covers count divergence scenarios.
EVIDENCE: Pass 2's statement that no assigned-versus-observed rule is stated in A is not what the text says. A:33 states the reconciliation rule: "an empty block is complete only when the assigned rows are non-empty and all observed (`findings_v2.py:292`)". A:98 states a divergence scenario between assigned, requested and responding counts: "a reviewer lost after assignment leaves its items unexamined, which `observed` shows; it does not feed C-03's `min(2, requested)` floor, and A does not claim it does". A:55 states a gate-versus-estimate divergence ("D2 ... fails for either design even if the design performs exactly as predicted"), and A:78 a selection-cap-versus-candidates divergence (at most 12 selected from 20 to 34 candidate lines). Both passes accepted the same kind of evidence (assigned rows vs observed rows) as MET for B (B:36), where B adds the 11-of-13 duplicate-assignment count. Neither variant has an inclusive/exclusive or line-base off-by-one scenario; the criterion's parenthetical lists examples, and this coverage criterion is met by a concrete cited scenario.
VERDICT: MET.
Why final: the cited A:33 and A:98 give the same class of count-divergence evidence that both passes already accepted for B, so MET follows from applying one standard to both variants.

## 2. Final qualitative totals

Method: the 53 agreed criterion-variant pairs come from the YAML fences at the end of `score-pass1.md` and `score-pass2.md` (a pair is agreed when both fences give the same verdict); the 7 disputed pairs use the final verdicts above. I confirmed that exactly 7 pairs differ between the fences, and they are the 7 listed.

Final verdicts for the 7 disputed pairs:

| # | Criterion | Variant | Pass 1 | Pass 2 | Final | Changed vs Pass 1 | Changed vs Pass 2 |
|---|---|---|---|---|---|---|---|
| 1 | Correctness 3 | B | NOT MET | MET | NOT MET | no | yes |
| 2 | Correctness 4 | A | NOT MET | MET | MET | yes | no |
| 3 | Clarity 4 | A | NOT MET | MET | NOT MET | no | yes |
| 4 | Clarity 4 | B | NOT MET | MET | NOT MET | no | yes |
| 5 | Risk Coverage 2 | A | NOT MET | MET | NOT MET | no | yes |
| 6 | Risk Coverage 2 | B | NOT MET | MET | NOT MET | no | yes |
| 7 | Invariant & Edge Case 4 | A | MET | NOT MET | MET | no | yes |

Of the 7 final verdicts, 1 differs from Pass 1 (pair 2) and 6 differ from Pass 2 (pairs 1, 3, 4, 5, 6, 7). Each disputed pair matches exactly one pass, so 1 + 6 = 7.

Per-dimension subtotals (agreed pairs plus final verdicts):

| Dimension | A | B |
|---|---|---|
| Completeness | 5/5 | 5/5 |
| Correctness | 2/5 | 0/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 5/5 |
| **Total met of 30** | **24** | **23** |
| **qual_score (met / 30)** | **0.8000** | **0.7667** |

Edge Case Floor (>= 1/5 on Invariant & Edge Case): A 5/5 eligible, B 5/5 eligible.

Cross-check of the arithmetic: Pass 1 totals were A 23, B 23; the final differs from Pass 1 only in pair 2 (A +1), giving A 24, B 23. Pass 2 totals were A 25, B 26; the final differs from Pass 2 in pairs 1 (B -1), 3 (A -1), 4 (B -1), 5 (A -1), 6 (B -1) and 7 (A +1), giving A 25 - 1 - 1 + 1 = 24 and B 26 - 1 - 1 - 1 = 23.

Where the two variants differ after re-evaluation: Correctness (A 2/5, B 0/5: A keeps terminology accuracy and has no two-statement contradiction; B has the id-space conflation and the first-review vs C-02 quorum conflict) and Structure (A 4/5, B 5/5: A puts design answers in its Evidence section, agreed by both passes). Both lose Clarity 4 and Risk Coverage 2.

## 3. Machine-readable verdicts

```yaml
pass: reeval
disputed_pairs:
  correctness.3: {variant: B, pass1: NOT MET, pass2: MET, final: NOT MET}
  correctness.4: {variant: A, pass1: NOT MET, pass2: MET, final: MET}
  clarity.4: {variant: A, pass1: NOT MET, pass2: MET, final: NOT MET}
  clarity.4b: {variant: B, pass1: NOT MET, pass2: MET, final: NOT MET}
  risk.2: {variant: A, pass1: NOT MET, pass2: MET, final: NOT MET}
  risk.2b: {variant: B, pass1: NOT MET, pass2: MET, final: NOT MET}
  invariant.4: {variant: A, pass1: MET, pass2: NOT MET, final: MET}
changed_vs_pass1: 1
changed_vs_pass2: 6
subtotals:
  A: {completeness: 5, correctness: 2, structure: 4, clarity: 4, risk_coverage: 4, invariant_edge: 5, total: 24}
  B: {completeness: 5, correctness: 0, structure: 5, clarity: 4, risk_coverage: 4, invariant_edge: 5, total: 23}
qual_score: {A: 0.8000, B: 0.7667}
edge_case_floor: {A: eligible, B: eligible}
```

Status: Complete
