# Base Selection Report

Variants: A = V1 `opus:architect`, B = V2 `sonnet:qa`, C = V3 `opus:analyzer` (files `variant-1-opus-architect.md`, `variant-2-sonnet-qa.md`, `variant-3-opus-analyzer.md`).
Source requirements for the quantitative layer: the 39 item IDs of `proposed-cuts.md` (the brief says 36; see debate-transcript X-014) plus the required row fields (verdict, scope, guard, confidence, evidence).

## Quantitative Scoring (50% weight)

| Metric | Weight | A (V1) | B (V2) | C (V3) |
|--------|--------|--------|--------|--------|
| requirement_coverage | 0.30 | 1.000 (39/39 IDs, all 5 row fields; grep `^\| (R\|T\|S\|D)[0-9]+ ` = 39) | 1.000 (39/39) | 1.000 (39/39) |
| internal_consistency | 0.25 | 0.846 (6 of 39 rows carry a claim the debate and live files disproved: R3 five-field scope, R2 comment edit, T7 merge fails on long-identifiers.json, S2 deletes `SCHEMA_VERSION`, D1 collapse orphans OQ-n labels, D8 rows off by one) | 0.897 (4 of 39: R2 KEEP over a dead field, R3 KEEP, T6 cut of the only render/export import check, S2 deletes `SCHEMA_VERSION`) | 0.872 (5 of 39: T3 cut of spec-backed tests, T5 "real Collector" conclusion, T6 cut of the single-Console guard, S3 reference count, S2 leaves unused `resources` import: ruff F401) |
| specificity_ratio | 0.15 | 1.000 (191 concrete refs, 0 vague) | 0.995 (205 concrete, 1 vague) | 1.000 (246 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.000 (every "see Extra findings n", "T9", "D12" reference resolves) | 1.000 | 1.000 |
| section_coverage | 0.15 | 1.000 (1 H2; max across variants is 1) | 1.000 | 1.000 |
| **quant_score** | | **0.9615** | **0.9736** | **0.9680** |

Computation: `0.30*RC + 0.25*IC + 0.15*SR + 0.15*DC + 0.15*SC`. IC counts rows whose factual or scope claim the live files or another advocate's verified evidence contradicted (an input from Step 2, not an LLM judgment of style).

## Qualitative Scoring (50% weight): Additive Binary Rubric (30 criteria, CEV)

Pass 1 in input order (A, B, C); Pass 2 in reverse order (C, B, A). Verdicts below are the final verdicts after disagreement handling. Evidence cites the variant file.

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | 39 rows, verdict/scope/guard/confidence/evidence columns | MET | same | MET | same |
| Addresses edge cases/failures | MET | Extra findings 2 (R1/T9 clash), 3 (R1 ranges) | MET | Extra 3 (interactions), R9 untested question path | MET | Extra 3 (R1 unused imports), 30 (clash) |
| Includes dependencies/prerequisites | MET | Extra 17 (what waits on owner, schemaVersion 2) | MET | Extra 3 (cut ordering, S1 before R2) | MET | Extra 31 (pytest/ruff after every CUT-SMALLER) |
| Defines success/completion criteria | NOT MET | states the 694 baseline is not re-measured; names no post-cut check | NOT MET | "Not verified" list only; no post-cut check | MET | Extra 31 names the two commands |
| Specifies out-of-scope items | MET | rule 3 and rule 4 items deferred to owner | MET | "I did not touch them" (untracked files) | MET | "Question for the owner" rows |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims | NOT MET | T7 merge breaks on long-identifiers.json (advocate 3 grep); S2 `SCHEMA_VERSION` used at export.py:195 | NOT MET | R2 `count_text` dead (view.py:209, :732 only); S2 same NameError | NOT MET | T5 conclusion and S3 count (55 vs 37 occurrences) wrong; T3 contradicts ARCHITECTURE-SPINE.md:154 |
| Technical approaches feasible | NOT MET | T7 and S2 as written fail tests or imports | NOT MET | S2 as written fails | NOT MET | S2 leaves `resources` unused (ruff F401, rule 5) |
| Terminology consistent | MET | CUT/CUT-SMALLER/DEFER-OWNER/KEEP used as defined | MET | same | MET | same |
| No internal contradictions | MET | T9 narrowed to avoid the R1 range clash | MET | T9 KEEP consistent with R1 note | MET | R1 "NOT 65-70; T9 handles it" consistent | 
| Claims supported by evidence | MET | evidence column per row | MET | same | MET | same |
| **Subtotal** | **3/5** | | **3/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Logical section ordering | MET | R, T, S, D order | MET | same | MET | same |
| Consistent hierarchy depth | MET | one title, one table, one H2 | MET | same | MET | same |
| Clear separation of concerns | MET | table vs Extra findings | MET | extra findings grouped | MET | false claims vs missed |
| Navigation aids present | MET | path legend; "see Extra findings 1" | MET | path legend; "Interactions" section | MET | path legend; "see Extra findings 1" |
| Follows artifact-type conventions | MET | requested columns | MET | same | MET | same |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET | exact line lists | MET | exact line lists | MET | exact line lists |
| Concrete rather than abstract | MET | symbol-level scopes | MET | line ranges | MET | line ranges |
| Each section has a clear purpose | MET | | MET | | MET | |
| Acronyms and terms defined | MET | PKG/TESTS/SPEC/ISS legend | MET | PKG/TESTS/SPEC legend | MET | PKG/TESTS/I/SPEC legend |
| Actionable next steps | MET | owner questions worded | MET | owner questions worded | MET | owner questions worded |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Risk Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Identifies at least 3 risks with probability and impact | MET | confidence % per row; Extra 2, 5, 7 (loss of every no-blink guard, T47 break, untracked owner file) | MET | confidence %; R9, S6, D6 | MET | confidence %; Extra 26 (untracked owner file), 30 | 
| Mitigation for each risk | MET | keep ranges, stage first | MET | stub kept, tests first | MET | follow with pytest/ruff |
| Failure modes and recovery | MET | tracked (recoverable) vs untracked (not) | MET | same | MET | same |
| External dependencies and failure scenarios | MET | owner approval gates | MET | owner approval gates | MET | owner approval gates |
| Monitoring or validation mechanism | NOT MET | none named | NOT MET | "Not verified" only | MET | pytest/ruff after each CUT-SMALLER |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Collection boundaries | MET | R10 bound; T1 variants | MET | R10, T10 | MET | R10, T10 (8 variants) |
| State variable interactions across boundaries | MET | R1/T9 interaction | MET | interactions section | MET | cross-item clash |
| Guard condition gaps | MET | R3 counter guard | MET | R3, R8 pinned text | MET | R3 `_BLOCK_FIELDS` |
| Count divergence | MET | 39 vs 36 IDs | MET | 39 vs 36 | MET | 39 vs 36; 8 vs 10 variants |
| Interaction effects | MET | R1+T9 | MET | S1+S2+R2 | MET | R1+T9 |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 4/5 | 4/5 | 5/5 |
| Correctness | 3/5 | 3/5 | 3/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 | 5/5 |
| Risk Coverage | 4/5 | 4/5 | 5/5 |
| Invariant & Edge Case | 5/5 | 5/5 | 5/5 |
| **qual_score** | **26/30 = 0.867** | **26/30 = 0.867** | **28/30 = 0.933** |

Edge-case floor (>= 1/5 on Invariant & Edge Case Coverage): A 5/5, B 5/5, C 5/5. All eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Completeness 4 (success criteria) | A | NOT MET | NOT MET | AGREE | NOT MET |
| Risk Coverage 1 (probability and impact) | A | MET | NOT MET (probability only implicit in confidence %) | DISAGREE | MET (confidence % is the stated probability; findings give impact) |
| Structure 4 (navigation aids) | B | MET | NOT MET (no explicit cross-reference in the table) | DISAGREE | MET ("Interactions between items" section cross-references rows) |
| Completeness 4 | C | MET | MET | AGREE | MET |
| Correctness 4 (no internal contradictions) | C | MET | NOT MET (T6 keeps test_terminal.py:214-231 while R1 narrows terminal tests) | DISAGREE | MET (different tests; no conflict) |

Disagreements re-evaluated: 3. Final verdicts changed: 0 (each re-evaluation confirmed pass 1).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (V1 opus:architect) | 0.4808 | 0.4333 | **0.9141** | 32/39 = 82% (not in top two) |
| B (V2 sonnet:qa) | 0.4868 | 0.4333 | **0.9201** | 27/39 = 69% |
| C (V3 opus:analyzer) | 0.4840 | 0.4667 | **0.9507** | 27/39 = 69% |

**Margin**: top two are C (0.9507) and B (0.9201): 3.06% (below the 5% threshold)
**Tiebreaker applied**: Yes
- Level 1, debate performance (points where the post-debate result matches the variant's original verdict and scope): C 27/39, B 27/39. Tied within 5%.
- Level 2, correctness criteria met: C 3/5, B 3/5. Tied.
- Level 3, input order: B (variant 2) precedes C (variant 3).
- Note for the record: A (V1) won the most debate points (32 of 39) but its combined score ranks third (0.9141), outside the top-two set the protocol compares.

## Selected Base: Variant B (V2, sonnet:qa)

### Selection Rationale
By the protocol's deterministic tiebreak chain (levels 1 and 2 tie, level 3 is input order), V2 is the base. The base only fixes the document skeleton (one table of verdicts, an Extra findings section). The content of every row comes from the debate result, because after Round 1 each advocate conceded 15 to 20 points and the post-debate result differs from every variant on a different set of rows (V1 matches 32 rows, V2 27, V3 27). The merge therefore replaces rows and adds columns as the refactor plan states; no row is carried over from the base without being checked against the debate matrix.

### Strengths to Preserve from Base
1. V2's guard-first framing: every row names the test, golden, spec text or owner decision that would break (kept as the "Surviving guard" column).
2. V2's interactions list (R1+T9, S1+S2+R2, D2+R8, D13+D12) and its untracked-files finding.

### Strengths to Incorporate from Non-Base Variants
1. From V1: symbol-level edit lists for R1; the R1/T9 no-blink clash; extra stale spots for D2; owner-decisions-20261108.md untracked.
2. From V3: R3 aggregate counters; S2 `SCHEMA_VERSION` and `resources`; the full false-claims list; pytest and ruff after every cut as the completion criterion.
