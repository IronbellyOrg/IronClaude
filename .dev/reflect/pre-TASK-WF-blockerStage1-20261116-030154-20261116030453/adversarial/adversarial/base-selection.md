# Base Selection

Scorers: two independent sonnet-class judge agents (pass 1 in input order V1, V2, V3; pass 2 in reverse order V3, V2, V1), full CEV lines in `scoring-pass1.md` and `scoring-pass2.md` (same folder). Judge class overlaps variant 1's class (sonnet), so `judge_class_collision: true`; the leading metric (requirement coverage) is a count of verified defects, not a taste judgment.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (pass 1 / pass 2 / mean) | V2 (pass 1 / pass 2 / mean) | V3 (pass 1 / pass 2 / mean) |
|--------|--------|------------------------------|------------------------------|------------------------------|
| RC requirement coverage (of 6 verified defects: C-001, C-002, C-003, C-004, C-005, C-007) | 0.30 | 1.000 / 1.000 / 1.000 (6 of 6) | 0.500 / 0.500 / 0.500 (3 of 6) | 0.333 / 0.333 / 0.333 (2 of 6) |
| IC internal consistency (1 - refuted claims / scorable claims) | 0.25 | 0.810 / 0.688 / 0.749 | 0.833 / 0.857 / 0.845 | 0.833 / 0.800 / 0.817 |
| SR specificity ratio | 0.15 | 0.930 / 0.966 / 0.948 | 0.850 / 0.833 / 0.842 | 0.938 / 0.949 / 0.944 |
| DC dependency completeness (cited quote found at cited line) | 0.15 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 |
| SC section coverage (5 H2 sections each) | 0.15 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 |
| **quant_score** (pass 1 / pass 2 / mean) | | 0.942 / 0.9168 / **0.9294** | 0.786 / 0.7893 / **0.7877** | 0.749 / 0.7424 / **0.7457** |

The quantitative layer is deterministic in definition; the two passes differ only in how many claims each scorer counted as refuted or vague (IC and SR), and the ranking does not depend on which pass is used.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Subtotals after the disagreement resolution below (criteria met of 5 per dimension; full evidence lines in the two scoring files):

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 3 | 3 | 3 |
| Correctness | 3 | 5 | 3 |
| Structure | 5 | 5 | 5 |
| Clarity | 2 | 4 | 2 |
| Risk Coverage | 4 | 2 | 3 |
| Invariant & Edge Case Coverage | 5 | 2 | 5 |
| **Total (of 30)** | **22** | **21** | **21** |
| qual_score | 0.7333 | 0.7000 | 0.7000 |

Reasons behind the Correctness gap: V1 loses Correctness criteria 1 and 2 (it states 9 `review` subcommands exist where 7 do, and its `verify-sync` half and `.dev/pr-monitor/` finding were refuted by PLAN:25 and PLAN:72); V3 loses criteria 1 and 3 (its F1 ties "never reads `~/.claude`" to T4, which is a T3 clause at PLAN:209); V2 has no refuted factual claim (its F3 blocking grade is a grading dispute, not a false statement).

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Eligible as base |
|---------|-----------------------------|------------------|
| V1 | 5/5 | yes |
| V2 | 2/5 | yes (floor is 1/5) |
| V3 | 5/5 | yes |

## Position-Bias Mitigation

Dual pass ran as specified (pass 1 order V1, V2, V3; pass 2 order V3, V2, V1). Of 90 criterion-variant pairs the passes agreed on 87 and disagreed on 3. Each disagreement was re-evaluated with both pieces of evidence and the comparison rule "the same kind of evidence earns the same verdict for every variant":

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Basis for the final verdict |
|-----------|---------|--------|--------|-----------|-------|-----------------------------|
| Invariant 4 (count divergence) | V1 | NOT MET | MET | no | MET | V1's Checked list holds three verified count checks (7 tasklist Medium lines, 14 worked cases, 11 files holding the old sentence); the wrong "9 subcommands" count is already charged under Correctness 1 and 2 |
| Invariant 3 (guard conditions) | V2 | MET | NOT MET | no | MET | V2 F1 argues that the PLAN:115 grep rejects correct reuse, the same evidence that earned V1 and V3 a MET in both passes |
| Risk 3 (failure modes of later stages) | V2 | NOT MET | MET | no | NOT MET | V2 names only the same package's final review (F1, F2); V1 (stage 3 scan) and V3 (archive move, T2 scan) name a later stage or package |

disagreements_found: 3; verdicts_changed by re-evaluation: 1 (V1 Invariant 4 stays at pass 2's MET; V2 Invariant 3 stays at pass 1's MET; V2 Risk 3 stays at pass 1's NOT MET, so pass 1 changed for V1 only and pass 2 for V2 Invariant 3 and Risk 3).

## Combined Scoring

| Variant | quant (mean of passes) | qual | Combined = 0.5 quant + 0.5 qual | Rank |
|---------|------------------------|------|---------------------------------|------|
| V1 (analyzer, sonnet) | 0.9294 | 0.7333 | **0.8314** | 1 |
| V2 (qa, haiku) | 0.7877 | 0.7000 | **0.7438** | 2 |
| V3 (refactorer, opus) | 0.7457 | 0.7000 | **0.7229** | 3 |

Margin V1 over V2: 0.0876 (10.5 percent of 0.8314, outside the 5 percent tiebreak band). V2 over V3: 0.0209 (inside 5 percent, but they do not contest first place, so no tiebreaker is applied). Per-pass check: pass 1 gave 0.821 / 0.743 / 0.725 and pass 2 gave 0.8251 / 0.7446 / 0.7212: same order.

Tiebreaker applied: no.

## Selected Base: Variant 1 (sonnet:analyzer)

**Selection rationale.** Variant 1 is the only card that raises all six defects the debate verified as real (C-001, C-002, C-003, C-004 through its "ledger adapters" minor, C-005, C-007), and it supplied the decisive argument on C-002 (Task 3, Task 5 and T4 cannot all pass because the only tracked stoprule copies sit under `.dev/`). It scored 5/5 on the invariant and edge-case dimension. It also carries the most refuted statements (two refuted findings, two refuted sub-claims, one wrong count), so the merge must remove them.

**Strengths to preserve from the base.** F1 (stoprule file), F2 (allow-list narrower than the stage 3 scan, regraded non-blocking by the debate), F3's Task 7 half (C-001), F4 (scale-map layout and dependency), F6 (ledger adapters, Task 10 dependency).

**Strengths to incorporate from non-base variants.**
- From V3: C-001's decisive grounding in `source.md:17` and `stage-requests/README.md:33` ("a line that a later task of the same package makes false is written with its end point") and the `__pycache__` noise in the PLAN:115 grep; the OD10 undecided fact on C-002 (SPEC:582, SPEC:1038).
- From V2: the missing mapping decision of SPEC:404 and the "ledger adapters" of SPEC:945 stated as a plan decision gap (C-004), kept as non-blocking with V2's dissent recorded.
- From the debate and probe: Task 12 as a second false match for C-001 (V1 Round 2); invariant probe items INV-001 to INV-005 as non-blocking findings.
- Removed from the base because refuted: the `verify-sync` half of F3, F5 (`.dev/pr-monitor/`), the "reaches it only through Task 9" wording of F4, the "9 review subcommands" count.
