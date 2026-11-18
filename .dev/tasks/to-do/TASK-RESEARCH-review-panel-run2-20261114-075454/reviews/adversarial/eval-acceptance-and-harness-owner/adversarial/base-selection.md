# Base Selection Report

Slot X-14 `eval-acceptance-and-harness-owner`. Variants: Variant A = Proposal A (`variant-1-original.md`, default model, default persona); Variant B = Proposal B (`variant-2-original.md`, default model, default persona). Both original variants were scored as written, not the hybrid the debate converged on. Full Claim-Evidence-Verdict text per criterion is in `score-pass1.md` (order A then B), `score-pass2.md` (order B then A) and `score-reeval.md` (the four disagreements). The quantitative layer is `quant-score.py` with output `quant-score-output.json` (run twice by the scorer, and a third time by the orchestrator: the output sha256 `ec0fbb9cd858d07ef1eb8393c33f372e9c11b75cb22b331c942c2c000fc5617f` was identical every time).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Proposal A) | Variant B (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 1.0000 (12 of 12 requirements R1..R12 matched) | 1.0000 (12 of 12) |
| internal_consistency | 0.25 | 0.9921 (1 contradiction in 126 scorable claims) | 0.9815 (2 contradictions in 108 scorable claims) |
| specificity_ratio | 0.15 | 1.0000 (concrete 126, vague 0) | 1.0000 (concrete 108, vague 0) |
| dependency_completeness | 0.15 | 1.0000 (54 of 54 internal references resolved) | 1.0000 (64 of 64) |
| section_coverage | 0.15 | 1.0000 (9 H2 sections; max 9) | 0.8889 (8 H2 sections) |
| **quant_score** | | **0.9980** | **0.9787** |

Notes. RC, SR and DC saturate at 1.0 for both variants, so the quantitative layer separates them only through IC and SC. The 12 source requirements were extracted by the scorer from the X-14 conflict row and the proposal structure it asks for (list R1..R12 inside `quant-score.py`). Intra-variant contradictions counted in IC (quotes in `score-pass1.md` section 1.3): A has one (additive ledger keys while the adjudicated C-01 deferred passthrough keys, yet "Nothing below disagrees with a recorded outcome"); B has two (wrong-blocker counts "not gates" against the control wrong-blocker ceiling that gates, B:13; and E6 "the same three easy catches inside it" against B:94 "I make no claim about that split"). Facts the debate found false are not counted in IC; they are counted under Correctness.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Rule applied: MET only with a specific quote or line reference; otherwise NOT MET; no partial credit. Claims the variant's own advocate conceded false, or the diff analysis marked [CODE-CONTRADICTED], count against Correctness (K1) for that variant. Final = the agreed verdict of the two passes; where they disagreed, the re-evaluation verdict (`score-reeval.md`). `A:n` and `B:n` are line numbers in the two variants.

Claims found false, inaccurate or conceded (the basis of K1):
- Variant A: "a silent swap passes `model_ok`" (A:65; the swap is logged to `$RID.fallback.log`, `run-reviewer.sh:75`); "the per-reviewer counts ... that `parse_block` already returns" (A:30; `findings.py:127` returns `ok, findings, priors, errors` and no counts); "the product kernel has no served-model field" (A:65; `review/telemetry.py:49,364,378` declare and read `model.observed`).
- Variant B: "the later harness carries 89 test files ... fixable in place" (B:51, B:95; 28 of the 89 belong to designs 4 and 5 whose `lib/` code is absent from git at the study tip, and design 2's judge wrapper keeps the weak `rc` plus `jq -e .` completion test); "the same three easy catches inside it" (B:47; GT7 is flagged `blocking_in_implement: false`); "the manifest cannot hold `model_observed`" (B:53; contradicted beyond the files searched by `telemetry.py:49`).

### Completeness (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|-----------|-----------|------------|-----------|------------|
| C1 Covers all explicit requirements | MET (pass 1 MET, pass 2 NOT MET, re-evaluated MET) | A:11, A:19-21, A:96-109, A:123-130, A:132-136. Re-evaluation: the X-14 row names reflect UC-2, PR review and rf-qa, not tasklist review; the omission from A's Section 3 list is a thoroughness gap, not a missed explicit requirement. | MET | B:13, B:17-21, B:63-71, B:81-86, B:88-97; B names tasklist review (B:29) and the registry-owner answer (B:85). |
| C2 Addresses edge cases and failure scenarios | MET | A:115 M-2 injected-fault fixtures (prefix collision, plausible `score.json` from a dead judge, fallback overwrite, batch outside the manifest). | MET | B:75 M1 defect-class tests (`fullpkg`, missing `score.json`, run absent from the manifest). |
| C3 Includes dependencies and prerequisites | MET | A:19-21 DEPENDS clause per adjudicated slot (C-01 INV-003; C-02 INV-001, INV-002, INV-018; C-03 INV-007, INV-001). | MET | B:18, B:20 dependence on C-01 helpers, C-06 repair policy, C-03 INV-001; B:70 identity waits for C-08. |
| C4 Defines success/completion criteria | MET | A:113-121 M-1..M-5 each with Right-if / Wrong-if. | MET | B:75-79 M1..M5 each with "Position B is wrong if". |
| C5 Specifies what is out of scope | MET | A:143-149 "What this proposal does not claim". | MET | B:99-104 open facts; B:79 and B:102 what B does not require or use. |
| **Subtotal** | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|-----------|-----------|------------|-----------|------------|
| K1 No factual errors or hallucinated claims | NOT MET | Three conceded or contradicted claims (list above). | NOT MET | Three conceded or contradicted claims (list above). |
| K2 Feasible with stated constraints | MET (pass 1 MET, pass 2 NOT MET, re-evaluated MET) | A:69 E-12 a tenth optional module breaks no pin; A:28 `unrecorded` state; A:30 counts are stated as additions; the false "already returns" clause is scored under K1, and the counts are derivable from the lists `parse_block` returns (`ledger.py:128-149`). | MET | B:37 gate exists with 410 lines and 20 tests; B:33 fixes derive from verified defects; B:71 states the testpaths limit. |
| K3 Terminology consistent and accurate | MET | Hyphenated ids `E-1..E-15`, `M-1..M-5`, `P-1..P-5` distinct from the study names E1/E2 and the `E2:<path>` prefix (A:7). | NOT MET (pass 1 NOT MET, pass 2 MET, re-evaluated NOT MET) | One token E1/E2 names an evidence item, a study and a citation prefix, sometimes within one sentence (B:9, B:13, B:37, B:39, B:57). |
| K4 No internal contradictions | NOT MET | Pass 1: A-IC-1 (additive ledger keys against C-01's deferred passthrough keys while stating no disagreement, A:15, A:30, A:106). Pass 2: "`verify-run` never imports a v1 or v2 engine internal" (A:19) against "imports `findings._check_finding`" (A:31), a private helper (`findings.py:188`). | NOT MET (pass 1 NOT MET, pass 2 MET, re-evaluated NOT MET) | B-IC-1 (B:13 wrong-blocker counts "not gates" against the control ceiling that gates) and B-IC-2 (B:47 against B:94). |
| K5 Claims supported by evidence or rationale | MET | Tagged and cited items E-1..E-15 (A:45, A:47, A:136). | MET | Tagged and cited items E1..E12 (B:39, B:41, B:43, B:93-97). |
| **Subtotal** | **3/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|-----------|-----------|------------|-----------|------------|
| S1 Logical section ordering | MET | Sections 1-9 in dependency order (constraints from adjudicated slots precede the design). | MET | Sections 1-8 in dependency order. |
| S2 Consistent hierarchy depth | MET | H2 1-9; H3 4.1-4.3 all populated. | MET | H2 1-8, no H3. |
| S3 Separation of concerns | MET | Design, evidence (split by subject), invariants, measurements, module effects are separate. | MET | Same separation. |
| S4 Navigation aids | MET | Citation-key line (A:7), "Section 4, E-1" cross-references; 54 of 54 resolve. | MET | Citation-form line (B:9), "(section 3, E4)" cross-references; 64 of 64 resolve. |
| S5 Follows artifact conventions | MET | Position, consistency, design, evidence, invariants, test, effect, objection, non-claims. | MET | Same parts without a non-claims section. |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|-----------|-----------|------------|-----------|------------|
| L1 Unambiguous language | MET | Vague-word grep 0 hits; A:11 states decisions flatly. | MET | 0 hits; B:13 "There is no `superclaude review verify-run`." |
| L2 Concrete rather than abstract | MET | Files, lines, counts (A:30, A:61). | MET | 410 lines, 20 tests, `d2d8a2d16` (B:37; B:43; B:51). |
| L3 Clear purpose per section | MET | Headings state purpose. | MET | Headings state purpose. |
| L4 Acronyms defined on first use | NOT MET | "T-1..T-10", "S-0..S-5", "OQ-16", "REQ-36", "GT3/GT7", "E2 study" undefined. | NOT MET | "OQ-6", "GQ-082", "CO-16", "FX-17", "GT" ids, "O3 con", E1/E2 undefined. |
| L5 Actionable next steps / decision points | MET | A:136 M-3 reading; A:126 status "lead". | MET | B:97 flip condition; B:79 M5. |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|-----------|-----------|------------|-----------|------------|
| R1 At least 3 risks with probability and impact | NOT MET | A:105-109 severity labels only; no probability. | NOT MET | B:69-71 three risks, no probability. |
| R2 Mitigation for each identified risk | NOT MET | Only INV-H has a mitigation (A:105); INV-D, INV-C, INV-K end as unchecked items. | MET | Each endangered item has a stated answer (B:69, B:70, B:71). |
| R3 Failure modes and recovery | MET | A:28 `pass/flag/unrecorded`; A:100 INV-I; A:33 judge accepted only if `score.json` exists, parses and satisfies the equation. | MET | B:33 judge-completion check; B:75 unaudited runs print as such; B:78 M4. |
| R4 External dependencies and failure scenarios | MET | A:19-21 C-01, C-02, C-03 dependencies; A:147 identity stays `unrecorded` if C-08 does not land. | MET | B:18, B:70 C-06 and C-08 dependencies. |
| R5 Monitoring or validation mechanism | MET | A:115 M-2; A:121 M-5; A:105 INV-H scan test. | MET | B:75 M1; B:77 M3; B:78 M4. |
| **Subtotal** | **3/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|-----------|-----------|------------|-----------|------------|
| I1 Collection boundaries | MET | A:117 M-3 zero in every arm; A:21 `requested` collapses to 1; A:37 empty baseline at `:313`. | MET | B:28 empty legacy baseline; B:45 0 of 8; B:76. |
| I2 State variable interactions across components | MET | A:20 derive the verdict from rows and still read older ledgers; A:21 manifest written before the drop. | MET | B:19 call `ledger verdict`, not stored fields; B:43 severity typing changes with C-02. |
| I3 Guard-condition gaps | MET | A:47 judge completion; A:29 exact tuple keys. | MET | B:51 prefix match and judge completion; B:75 M1. |
| I4 Count divergence | MET | A:61 69 against 71 to 76; A:49 65 against 38; A:67 batch j1. | MET | B:43 65, 38, 89; B:75 69 against 71 or 76. |
| I5 Interaction effects | MET | A:21 union default raises false-blocker cost; A:19 law depends on C-06. | MET | B:19 and B:76 metric changes meaning when C-02 lands. |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 3/5 | 2/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **25/30 = 0.8333** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Eligible as base |
|---------|--------------------------------|------------------|
| A | 5/5 | Yes |
| B | 5/5 | Yes |

The floor is met by both; no suspension warning is needed.

## Position-Bias Mitigation

Pass 1 evaluated A then B (A 25/30, B 25/30). Pass 2 evaluated B then A (B 27/30, A 23/30). The passes agreed on 56 of 60 criterion-variant pairs and disagreed on four. Each disagreement was re-evaluated with both passes' evidence side by side (`score-reeval.md`); the re-evaluation verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness C1 | A | MET | NOT MET | DISAGREE | MET |
| Correctness K2 | A | MET | NOT MET | DISAGREE | MET |
| Correctness K3 | B | NOT MET | MET | DISAGREE | NOT MET |
| Correctness K4 | B | NOT MET | MET | DISAGREE | NOT MET |

Disagreements re-evaluated: 4. Final verdicts changed from pass 1: 0. Final verdicts changed from pass 2: 4. Reading: the position-bias disagreement was one-directional (pass 2, which read B first, scored B 2 points higher and A 2 points lower than pass 1); the comparison re-evaluation sided with pass 1 on all four pairs.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (Proposal A) | 0.4990 | 0.4167 | **0.9157** | 11 points won (55% of the 20 decided points; 25.0% of all 44) |
| B (Proposal B) | 0.4894 | 0.4167 | **0.9060** | 9 points won (45% of the 20 decided points; 20.5% of all 44) |

**Margin**: 0.0097 (0.97%) (below the 5% threshold)
**Tiebreaker applied**: Yes

Tiebreaker walk (protocol A.4):
- Level 1, debate performance (points won in the Step 2 scoring matrix): A won 11 points, B won 9, 20 were agreed ties and 4 are unresolved. Measured as the share of decided points, A leads by 10 percentage points (55% against 45%), which is outside the 5% band, so Level 1 selects A. Measured as the share of all 44 points the lead is 4.5 percentage points (25.0% against 20.5%), inside the band; under that reading the protocol passes to Level 2.
- Level 2, correctness criteria count: A 3 MET, B 2 MET. A wins.
- Both readings select Variant A, so the selection does not depend on which denominator is used. Level 3 (input order, which also favours A) is not needed.

Where the margin comes from: the whole margin is in the quantitative layer (IC 0.9921 against 0.9815; SC 1.0 against 0.8889). The qualitative totals are equal at 25/30 with opposite splits: A is ahead on Correctness (3 against 2), B is ahead on Risk Coverage (4 against 3).

## Selected Base: Variant A (Proposal A; `variant-1-original.md`)

### Selection Rationale

- Combined score A 0.9157 against B 0.9060; margin 0.97%, below the 5% threshold; the tiebreaker (debate performance, then correctness count) selects A on both readings (above).
- The debate's own scoring matrix has A winning the points that decide a base for this slot: the metric of record (C-002, X-003, C-015), tested placement (C-003, C-014, X-001), the tiers (C-001) and the integrity checks (C-009), against B's wins on the kernel command and its inputs (C-004, C-006, X-002, X-005), the repaired reflect gate (C-010), module coverage (S-005) and the fuller severity reading (C-013, A-011).
- The convergence the debate reached is a hybrid whose backbone is A's: A's three tiers, metric of record and tested `scripts/` plus `tests/` set, with A's kernel `verify-run` command and ledger-entry additions removed (A's advocate withdrew them in Round 2) and B's procedure items added (B's advocate conceded the placement and the headline metric in Round 2). Taking A as the base and applying B's contributions is therefore the smaller edit.
- Honest limits on this selection: the two variants tie on the qualitative layer (25/30 each) and the margin is 0.97%; the base is selected by the tiebreaker, not by a wide score gap. Both variants contain statements the debate found false (Correctness K1 NOT MET for both).

### Strengths to Preserve from Base

1. Three acceptance tiers S, Q, G with the "lead" label (A:11), and the metric of record: ground-truth items found in a ledger row flagged blocking where the item is blocking in implement, plus wrong blockers, plus control found, with the any-severity count as a secondary number (A:11, A:117, A:128).
2. Tested harness code under `scripts/` with `tests/` (collected by `testpaths = ["tests"]`, `pyproject.toml:108`) and generic harness parts as arguments-driven scripts: judge wrapper with a completion record and the `wrong_blockers` check, anonymiser, ground-truth registry, seeded-plan manifest, table builder with exact-key lookup and a refusal of runs without a verifier record, statistics with a stated minimum detectable effect and comparison count (A:33).
3. Three-valued check output `pass / flag / unrecorded` and "unaudited" as a reported state (A:28, A:67).
4. The expected-cells manifest written at dispatch time (A:21, A:33), owed to the dispatch slot.
5. Pre-registration by commit order as a Tier Q condition (A:11); Tier G seeded defects with a clean twin and hold-out set (A:11, A:125).
6. The consistency table with a DEPENDS clause per adjudicated slot (A:15-23) and the stated effect on PR review and rf-qa (A:123-130).

### Strengths to Incorporate from Non-Base Variants

1. From Variant B, Section 2 and Section 4 (debate points C-004, C-006, X-002, X-005; B won all four): no kernel `verify-run` and no ledger-entry additions; the verifier is a script in `scripts/` computing conservation and completeness from stored data (reports, `report_sha256`, ledger members); a check that needs a record no code writes reports `unrecorded`.
2. From Variant B, Section 2 and M4 (C-010): fix `scripts/reflect_shadow_exit.py:313` (empty legacy baseline read as 0.0) and `:59` (card-name regex against `panel_lint.py:188`), and re-run the repaired gate over the shadow manifests so the verdict no longer turns on the empty-baseline artifact.
3. From Variant B, Section 2 (S-005): tasklist review coverage and the import of the untracked E2 harness (`git ls-files` prints 0; `lib/` hidden by `.gitignore:13`; the study tip is not an ancestor of HEAD).
4. From Variant B, E4 (C-013, A-011): the 89-against-38 reading of severity typing, the condition that the rule is committed after C-02 lands, and B's M2 offline discrimination on the 71 valid rows before the rule is committed.
5. From Variant B, Section 7 answer 5 and the reading note (S-007, U-009, U-014): the explicit concessions and flip condition; the control-package wrong-blocker ceiling as a secondary column.
6. From the debate, as agreed wording (C-008, X-004): a use case is "accepted" only with Tier S, a pre-registered Tier Q and Tier G; otherwise its status is "not worse on what is pinned, lead only"; building and shadow runs are not held up.
7. Corrections to A's own text found false or inconsistent in the debate: "silent swap" (logged), "counts `parse_block` already returns" (it returns none), "no served-model field" (declared in `telemetry.py:49`, no writer), the E-1 sentence that omits the control guard, the `scripts/` precedent (three `eval_*.py` have no tests), the first-error statement about the ledger entry (a returned warning), and the private `findings._check_finding` import.
