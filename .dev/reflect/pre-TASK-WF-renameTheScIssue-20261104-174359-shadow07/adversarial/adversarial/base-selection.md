# Base Selection — Hybrid Scoring (Mode A, reviewer cards shadow07)

## Quantitative Scoring (50% weight)

Metrics computed over the three cards as artifacts. Deterministic counts by the orchestrator.

### Requirement coverage (RC, weight 0.30)

Requirement set = the six debate topics A-F (audit obligations derived from the briefs + spec surface). A topic counts covered when a card raises or explicitly dispositions it.

- Card 1: A (F1), B (F2), C (H3 explicit disposition — conceded in R2 as answering the wrong question), F blank, D/E blank → 4/6 = 0.67
- Card 2: B (F1), C (F2), D (F3), E (F4); A and F blank (A conceded as a genuine miss) → 4/6 = 0.67
- Card 3: A (F1), E (explicit rebuttal), F (F2); B, C, D blank (B and D conceded as misses) → 3/6 = 0.50

### Internal consistency (IC, weight 0.25)

- Card 1: ~14 scorable claims; 1 internal tension (H3 verdict vs its own F2 logic) → 1 − 1/14 = 0.93
- Card 2: ~16 claims; 2 internal tensions (F1 "self-contradictory" vs satisfiability; F4 category vs its own "this is intentional" admission) → 1 − 2/16 = 0.88
- Card 3: ~12 claims; 1 internal tension (remedy sentence vs its own cp-only analysis) → 1 − 1/12 = 0.92

### Specificity ratio (SR, weight 0.15)

Concrete indicators (file:line citations, named tests, quoted AC text) vs vague assertions.

- Card 1: 20/23 = 0.87
- Card 2: 22/25 = 0.88
- Card 3: 16/18 = 0.89

### Dependency completeness (DC, weight 0.15)

Internal references resolving within the card to the quoted text.

- Card 1: 18/18 = 1.00 (Makefile 112-125 span is partial but resolves; widened to 108-163 in debate)
- Card 2: 14/17 = 0.82 (the three Task-1 findings citations plan:51/50/52 do not resolve to the quoted text)
- Card 3: 15/15 = 1.00 (281-283 range one line short; quote accurate, counts resolved)

### Section coverage (SC, weight 0.15)

H2/H3-level sections per card: card 1 = 4, card 2 = 3, card 3 = 4. Max = 4.

- Card 1 = 1.00, Card 2 = 0.75, Card 3 = 1.00

### Quantitative totals

quant = RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15

| Metric (weight) | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| RC (0.30) | 0.67 | 0.67 | 0.50 |
| IC (0.25) | 0.93 | 0.88 | 0.92 |
| SR (0.15) | 0.87 | 0.88 | 0.89 |
| DC (0.15) | 1.00 | 0.82 | 1.00 |
| SC (0.15) | 1.00 | 0.75 | 1.00 |
| **quant_score** | **0.864** | **0.789** | **0.813** |

(Card 1: 0.201 + 0.233 + 0.131 + 0.150 + 0.150 = 0.864; Card 2: 0.201 + 0.220 + 0.132 + 0.123 + 0.113 = 0.789; Card 3: 0.150 + 0.230 + 0.134 + 0.150 + 0.150 = 0.813.)

## Qualitative Scoring (50% weight) — Additive Binary Rubric (CEV)

Pass 1 order: card 1, card 2, card 3. Pass 2 order: card 3, card 2, card 1. Both passes agreed on every criterion-variant pair (disagreements = 0; no re-evaluation required). The rubric scores each CARD AS WRITTEN — the artifact being compared — not the post-debate repaired state; debate corrections are credited in the selection rationale, not by erasing the defects the debate found.

### Completeness (5)

1. Covers its assigned audit obligations — Card 1 MET (all six brief hypotheses dispositioned, each with a reason); Card 2 MET (coverage-matrix audit + AC audit + test-spec-vs-disk walkthrough); Card 3 MET (all four brief items addressed). Evidence: card 1 H1-H6 section; card 2 three-part analysis; card 3 sections 1-4.
2. Addresses edge cases / failure modes — MET all three. Evidence: card 1 "a line containing both the old and new name would still pass"; card 2 exact-list assertions and probe set; card 3 "no task AC would catch this".
3. Includes dependencies / prerequisites — scored lens-relative (persona-sliced panel; the strict reading penalizes all three identically and does not differentiate). Card 1 MET (per-hypothesis grounding chains); Card 2 MET (matrix-to-task mapping); Card 3 MET (task-by-task dependency walk). Strict-reading note: all three would be NOT MET (each is silent on another persona's slice); recorded, not differentiating.
4. Success criteria defined — MET all three (structured findings blocks with severity + blocking flags).
5. Out-of-scope explicit — MET all three (card 1 named non-findings H3-H6; card 2 inline "No finding." verdicts; card 3 named non-findings).

Completeness: 5/5, 5/5, 5/5.

### Correctness (5)

1. No factual errors (as-written) — Card 1 MET; Card 2 NOT MET (plan:94 same-phrasing claim false — withdrawn in R2; F4's "exception the plan never states" false — withdrawn in R2); Card 3 NOT MET (remedy sentence "may linger until someone runs make sync-dev" false — corrected in R1 by its own advocate).
2. Technical approaches feasible — MET all three.
3. Terminology consistent — MET all three.
4. No internal contradictions (as-written) — Card 1 MET; Card 2 NOT MET (F4 vs "this is intentional"; "self-contradictory" vs satisfiability); Card 3 MET.
5. Claims evidenced — Card 1 NOT MET (H4 verdict carries no citation); Card 2 NOT MET (three findings citations off by 7-8 lines); Card 3 MET (one range one line short, quote accurate — counted as evidenced).

Correctness: Card 1 4/5, Card 2 2/5, Card 3 3/5.

### Structure (5)

1. Logical ordering — MET all three. 2. Consistent hierarchy — MET all three. 3. Separation of concerns — MET all three. 4. Navigation aids — MET all three (internal cross-references; TOC not expected at card size). 5. Artifact-type conventions — MET all three (panel skeleton, findings-v2 block, self-report line).

Structure: 5/5, 5/5, 5/5.

### Clarity (5)

1. Unambiguous language — MET all three. 2. Concrete over abstract — MET all three. 3. Section purpose statable in one sentence — MET all three. 4. Terms defined on first use — MET all three. 5. Actionable next steps — MET all three (findings blocks).

Clarity: 5/5, 5/5, 5/5.

### Risk Coverage (5)

1. ≥3 risks with probability/impact — NOT MET all three (2/4/2 findings, every one MINOR — the audited plan genuinely has no higher-severity surface; uniform, not differentiating). 2. Mitigation per risk — NOT MET all three (cards identify, plans remediate). 3. Failure modes and recovery — MET all three (card 1 mixed-line grep failure + backstop test; card 2 red-check undefined pass; card 3 mirror reader impact). 4. External dependency failure scenarios — MET all three (CI and pre-commit paths reasoned by cards 1 and 3; test-pin reasoning by card 2). 5. Monitoring/validation mechanism — NOT MET all three (no card proposes a monitoring hook).

Risk Coverage: 2/5, 2/5, 2/5.

### Invariant & Edge Case Coverage (5) — floor 1/5

1. Collection boundaries — Card 1 MET (mirror-only single-file "Only in" case; grep substring boundary); Card 2 MET (probe set includes the outside-a-code-span non-match, tests:452); Card 3 NOT MET.
2. State variable interactions — Card 1 MET (mirror state vs src state under cp-only sync); Card 2 MET (test literal vs agent file state coupling); Card 3 MET (paragraph/test-literal sync state).
3. Guard condition gaps — Card 1 MET (grep AC guard ambiguity); Card 2 MET (expected-exit-code guard absent; AC2 verifier absent); Card 3 NOT MET.
4. Count divergence — Card 3 MET (ten-copies arithmetic check); Cards 1/2 NOT MET.
5. Interaction effects — NOT MET all three (no card addresses combined-change interactions).

Invariant & Edge Case: Card 1 3/5, Card 2 3/5, Card 3 2/5.

### Qualitative Summary

| Dimension | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness (as-written) | 4/5 | 2/5 | 3/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 | 5/5 |
| Risk Coverage | 2/5 | 2/5 | 2/5 |
| Invariant & Edge Case | 3/5 | 3/5 | 2/5 |
| **Total (of 30)** | **24/30** | **22/30** | **22/30** |

qual_score: card 1 = 0.800, card 2 = 0.733, card 3 = 0.733.

### Edge Case Floor Check

Card 1 3/5, Card 2 3/5, Card 3 2/5 — all ≥ 1/5. No variant ineligible; floor not suspended.

## Position-Bias Mitigation

Dual-pass (forward 1→2→3, reverse 3→2→1) produced identical verdicts on all 90 criterion-variant pairs. Disagreements found: 0. Verdicts changed: 0. The two judgment calls (lens-relative Completeness criterion 3; as-written Correctness) were adopted identically in both passes.

## Combined Scoring

variant_score = (0.50 × quant) + (0.50 × qual)

- Card 1: 0.432 + 0.400 = **0.816**
- Card 2: 0.395 + 0.367 = **0.762**
- Card 3: 0.407 + 0.367 = **0.773**

| Variant | Quant | Qual | Combined | Rank |
|---|---|---|---|---|
| Card 1 (analyzer, 0.80) | 0.864 | 0.800 | **0.816** | 1 |
| Card 3 (refactorer, 0.72) | 0.813 | 0.733 | **0.773** | 2 |
| Card 2 (qa, 0.82) | 0.789 | 0.733 | **0.762** | 3 |

Tiebreaker: the top-two margin (card 1 vs card 3 = 0.043) is within 5%, so the tiebreaker protocol applies. Level 1 (debate points won per the scoring matrix): card 1 co-won C-001, co-won C-002, and carried C-006 via concession (2.5 points); card 3 co-won C-001 and won C-005 (1.5 points). Card 1 wins level 1 → base selection confirmed. (Note: card 3 vs card 2 margin 0.011 is also within 5%, but the tiebreaker applies to the top two only; for the record, level 1 would favor card 2 there — card 2 won C-003, C-004 and co-won C-006 — an ambiguity between rank order and debate contribution that the refactor plan resolves by taking the merged topic C, D and F content from card 2 regardless of rank.)

## Selected Base: Card 1 (analyzer, calibrated 0.80)

Selection rationale: card 1 wins on the axis that matters most for a merge base — as-written correctness and citation integrity. Its findings block survives an evidence-validator re-Read unmodified (both citations line-exact), while 3 of card 2's 4 findings are mis-cited by 7-8 lines and card 3 carries a false remedy sentence. It owns the mechanistic precision on the top-Medium topic A (the `diff -rq` "Only in" detection semantics plus two independent CI/pre-commit bounding mechanisms), and it dispositioned all six brief hypotheses with reasons. Debate survival rate: card 1 2/2 findings survive intact (100%); card 2 2/4 survive narrowed (F4 withdrawn); card 3 1/2 survives corrected (F2 reclassified).

Strengths to preserve from card 1 (base):
- F1's mechanism-first framing: cp-only sync-dev + diff -rq only-in detection + CI regenerate-before-verify + verify-sync off the commit path → local-only, detectable, MINOR.
- F2's concrete failure mode (a line holding both names passes a loose reading) + the named backstop (`test_old_summary_path_is_gone`).
- The H1-H6 disposition style with named, reasoned non-findings.

Strengths to incorporate from non-base variants:
- From card 2: T2 (plan:56) reuse propagation for topic B; topic D in full (unique); narrowed topic C claim (expected exit-code value unstated, trivially inferable; different evidence objects — real artifacts/pre/ copies vs in-module literals); corrected citation discipline (print plan:43/44, not 51/50).
- From card 3: reader-impact / "no task AC would catch this" framing for topic A; topic E substance-altitude classification (adopted as merged verdict); topic F reclassification to documentation note; F1 citation additions (Makefile:178; whole-target span 108-163; manual-removal remedy); ten-copies arithmetic check as positive coverage evidence.
