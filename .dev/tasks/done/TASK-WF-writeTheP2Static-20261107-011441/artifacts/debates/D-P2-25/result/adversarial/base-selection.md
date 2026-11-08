# Base Selection Report

Scope note: the two variants are short decision documents, so the rubric scores the quality of each DOCUMENT (coverage, accuracy, structure, clarity, risk and edge-case handling). It does not decide which OPTION is better; that comes from the debate scoring matrix (`debate-transcript.md`: A wins 9 points, B wins 1, 4 unresolved and lean A). The base chosen here is the skeleton the merged output is built on.

## Quantitative Scoring (50% weight)

Requirement set (no formal IDs, so section-level topic matching): the four judging aspects of the shared "How to judge" section: (1) text truth and clarity under `--unattended`; (2) spec and WC compliance; (3) size and test risk; (4) coordinator and owner gain or loss.

| Metric | Weight | Variant A (option A, inline) | Variant B (option B, pass the flag) |
|--------|--------|------------------------------|-------------------------------------|
| requirement_coverage | 0.30 | 0.750 (3 of 4: aspect 2 absent, no spec section or WC cited) | 1.000 (4 of 4: 2.1, WC-9, test and spec size, coordinator effect via nested contracts) |
| internal_consistency | 0.25 | 1.000 (0 contradictions in ~6 claims) | 1.000 (0 contradictions in ~6 claims) |
| specificity_ratio | 0.15 | 0.875 (7 concrete, 1 vague: "may be lower") | 0.727 (8 concrete, 3 vague: "larger", "accordingly", "its own gates") |
| dependency_completeness | 0.15 | 1.000 (4 of 4 references resolve in the working tree) | 0.750 (6 of 8: D-P2-24 and D-P2-13 were not read, so not resolved) |
| section_coverage | 0.15 | 1.000 (1 of 1 H2) | 1.000 (1 of 1 H2) |
| **quant_score** | | **0.906** | **0.922** |

Arithmetic: A = 0.225 + 0.250 + 0.131 + 0.150 + 0.150 = 0.906. B = 0.300 + 0.250 + 0.109 + 0.113 + 0.150 = 0.922. Counts are manual estimates, stated so a reader can redo them.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after position-bias resolution (see that section). Evidence is shortened to the cited location or quote.

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| C1 covers all explicit requirements | NOT MET | No spec 2.1, WC-4 or WC-9 engagement | NOT MET | No text-truth or coordinator/owner gain-loss statement |
| C2 edge cases and failure scenarios | NOT MET | "quality ... may be lower" is a weakness, not a failure scenario | MET | "a nested `blocked` stops release-split as `blocked`" |
| C3 dependencies and prerequisites | MET | Names the Error Handling fallback, `EXPECTED_NESTING`, the command section | MET | "design and workflow since P1, tasklist since P2" |
| C4 success or completion criteria | NOT MET | None stated | NOT MET | None stated |
| C5 out-of-scope items | NOT MET | None stated | NOT MET | None stated |
| **Subtotal** | **1/5** | | **2/5** | |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| R1 no factual errors | NOT MET | "workflow and tasklist ... stage files" contradicts `workflow.md:76` (does not stage `.dev/tasks`) and `tasklist.md:115` (stages nothing); "design is dialogue-heavy" has no support in `design.md:28-41` | MET | Claims match the `## Unattended mode` sections; `WORKER-CONTRACT.md:25` matches the blocked rule |
| R2 feasible under the stated constraints | MET | `SKILL.md:281` and `:439` exist; produces the three required files | NOT MET | `workflow.md:80` writes a package and `tasklist.md` needs a roadmap; neither writes `release-N-spec.md` (C-002, 95%) |
| R3 terminology consistent and accurate | MET | "fallback" mirrors the skill's own wording at `SKILL.md:281`; used consistently | MET | "nested-result rule", `<command>-<n>` match `WORKER-CONTRACT.md:24-25` |
| R4 no internal contradictions | MET | None found | MET | None found |
| R5 claims supported by evidence in the document | NOT MET | Staging rationale is wrong; "dialogue-heavy" and "quality may be lower" are unsupported | MET | WC-9 reasoning matches `workflow.md:76` |
| **Subtotal** | **3/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| S1 logical ordering | MET | Mechanism, strengths, weakness, judging | MET | Same |
| S2 consistent hierarchy | MET | H1, one H2 | MET | Same |
| S3 separation of concerns | MET | Option statement apart from "How to judge" | MET | Same |
| S4 navigation aids | MET | "Part 3 text near lines 262-282 ... Error Handling table" | MET | "spec section 2.1", "WC-9", "D-P2-24", "D-P2-13" |
| S5 artifact-type conventions | MET | Decision-option form | MET | Decision-option form |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| L1 unambiguous language | NOT MET | "the section and the skill make Part 3 produce" has no antecedent for "the section" | NOT MET | "invokes /sc:design, /sc:workflow or /sc:tasklist" leaves the choice open (A-002); "change accordingly" |
| L2 concrete | MET | Write tool, paths, line ranges | MET | `<report-dir>/nested/<command>-<n>/` |
| L3 clear purpose per section | MET | Yes | MET | Yes |
| L4 terms defined on first use | NOT MET | `EXPECTED_NESTING` undefined | NOT MET | `EXPECTED_NESTING`, `D-P2-24`, `D-P2-13` undefined |
| L5 actionable next steps or decision points | MET | Names the SKILL.md Part 3 and release-split.md edits | MET | Lists the sites that change |
| **Subtotal** | **3/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| K1 at least 3 risks with probability and impact | NOT MET | One weakness only | NOT MET | Risks named, no probability or impact |
| K2 mitigation per risk | NOT MET | None | NOT MET | None |
| K3 failure modes and recovery | NOT MET | None | NOT MET | Names the blocked stop, gives no recovery procedure |
| K4 external dependencies and their failures | NOT MET | Callee dependency failures not discussed | MET | "each with its own gates, blocked paths and staging behaviour"; "a nested `blocked` stops release-split" |
| K5 monitoring or validation mechanism | NOT MET | None | NOT MET | None |
| **Subtotal** | **0/5** | | **1/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| E1 boundary cases (here: no-split, single-release, maximum scope) | NOT MET | No-split branch (`SKILL.md:277,318-320`) not addressed | NOT MET | Same |
| E2 state interactions across component boundaries | NOT MET | Staging interaction asserted incorrectly | MET | "write packages under `.dev/tasks`, which a worker must not stage, WC-9" |
| E3 guard-condition gaps | NOT MET | None identified | NOT MET | Guards named, no missing guard identified |
| E4 count divergence (numbering such as nested `<n>`) | NOT MET | Not discussed | NOT MET | Not discussed |
| E5 interaction effects | NOT MET | None | MET | "interacts with D-P2-24 and D-P2-13" (marginal) |
| **Subtotal** | **0/5** | | **2/5** | |

### Qualitative Summary

| Dimension | A | B |
|-----------|---|---|
| Completeness | 1/5 | 2/5 |
| Correctness | 3/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 3/5 |
| Risk Coverage | 0/5 | 1/5 |
| Invariant & Edge Case | 0/5 | 2/5 |
| **qual_score** | **12/30 = 0.400** | **17/30 = 0.567** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case | Eligible as base |
|---------|-----------------------|------------------|
| A | 0/5 (below the 1/5 floor) | NO |
| B | 2/5 | YES |

The floor is not suspended: not all variants scored 0/5. Variant A is ineligible as base.

## Position-Bias Mitigation

Pass 1: scored in input order (A, B) by the orchestrator. Pass 2: scored in reverse order (B, A) by an independent evaluator agent (a36db5cbfc9e9c44a) that was not shown Pass 1 or the debate. The evaluator's own subtotals contained two addition slips (Variant A Clarity 3 MET reported as 2; Variant B Clarity 2 MET reported as 1), so totals were recomputed from its criterion table: Pass 2 totals A 11/30, B 16/30. Pass 1 totals: A 12/30, B 19/30.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| C3 | A | MET | NOT MET | DISAGREE | MET (the text names the fallback row and nested list it depends on) |
| R3 | A | NOT MET | MET | DISAGREE | MET ("fallback" copies the skill's own wording at `SKILL.md:281`; consistent) |
| L1 | A | MET | NOT MET | DISAGREE | NOT MET ("the section" has no antecedent) |
| C1 | B | MET | NOT MET | DISAGREE | NOT MET (aspects 1 and 4 missing) |
| R2 | B | NOT MET | MET | DISAGREE | NOT MET (debate point C-002 at 95%: callees do not write the spec files) |
| S4 | B | NOT MET | MET | DISAGREE | MET (cites 2.1, WC-9 and decision IDs) |
| L5 | B | MET | NOT MET | DISAGREE | MET (lists the sites that change, as A's is scored) |
| K3 | B | MET | NOT MET | DISAGREE | NOT MET (a failure mode with no recovery procedure) |
| K4 | B | MET | NOT MET | DISAGREE | MET ("blocked paths", "a nested `blocked` stops release-split") |
| E3 | B | MET | NOT MET | DISAGREE | NOT MET (guards named, no missing guard identified) |

Disagreements re-evaluated: 10 (A 3, B 7). Final verdict equals Pass 1 in 4 cases and Pass 2 in 6; so 6 final verdicts differ from Pass 1. All other 50 criterion-variant pairs agreed.

Final totals after resolution: **A 12/30, B 17/30**. (Check for A: C3 1 + Correctness 3 + Structure 5 + Clarity 3 + 0 + 0 = 12. Check for B: 2 + 4 + 5 + 3 + 1 + 2 = 17.)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (option A, inline) | 0.453 | 0.200 | **0.653** | not needed (A would win 9 debate points) |
| B (option B, pass the flag) | 0.461 | 0.283 | **0.744** | not needed (B wins 1 debate point) |

**Margin**: 9.1 points (above the 5% threshold)
**Tiebreaker applied**: No

## Selected Base: Variant 2 (option B document)

### Selection Rationale
Variant 2 has the higher combined score (0.744 vs 0.653) and is the only variant eligible under the edge-case floor, because Variant A scores 0/5 on Invariant & Edge Case Coverage. The result concerns document quality only. It does not mean option B is the better OPTION: the debate matrix favours option A on 9 of 14 points, B on 1, and 4 lean A (see `debate-transcript.md`). The merged output therefore keeps Variant 2's coverage (spec 2.1, WC-9, blocked paths, cross-references) as its skeleton and carries the debate verdict for option A.

### Strengths to Preserve from Base
1. Covers the compliance questions (spec 2.1, WC-9, the nested-result rule) and the blocked-path and staging risks (Variant 2 whole document).
2. Cross-references to decisions and rules (S4).
3. Concrete nested-directory pattern `<report-dir>/nested/<command>-<n>/`.

### Strengths to Incorporate from Non-Base Variants
1. From Variant 1, first paragraph: the mechanism of the recommended option (inline Write, no nested call, nested list unchanged), as the decision text.
2. From Variant 1, "Claimed strengths": zero further edits, deterministic path, reuse of the existing fallback row (U-001).
3. From the debate (both advocates): verified facts for the rejected option (C-002 deliverable mismatch, C-003 flag idiom, C-005 nesting depth, C-006 staging, X-002 late blocked), with file:line citations.
4. Correction of Variant 1's inaccurate claim that workflow and tasklist "stage files" (they defer or do nothing under `--unattended`).
5. From Variant 2: its unique contributions as acknowledged costs of choosing A (per-spec nested contracts, design's no-architecture-change guard).
