# Step 3 — Quantitative Scoring Layer (50% weight)

<!-- Produced by the neutral sc:debate-orchestrator per refs/scoring-protocol.md §A.1. This layer is computed only from the variant text, with no LLM judgment. The unit splitting and pattern matching were done by script. The rules are listed below so the computation can be re-run exactly. -->

- Variant A = `variant-1-original.md` (reviewer 1, sonnet:analyzer)
- Variant B = `variant-2-original.md` (reviewer 2, haiku:qa)
- Source requirements: `reviewer-snapshot/root/spec.md` R-001, R-002, R-003, and `reviewer-snapshot/root/completed.md` T-101, T-102, T-103. Total = 6.

## Summary

| Metric | Weight | Variant A (sonnet:analyzer) | Variant B (haiku:qa) |
|--------|--------|-----------------------------|----------------------|
| requirement_coverage (RC) | 0.30 | 0.6667 (4/6) | 0.8333 (5/6) |
| internal_consistency (IC) | 0.25 | 1.0000 (1 − 0/36) | 0.9808 (1 − 1/52) |
| specificity_ratio (SR) | 0.15 | 0.9259 (25/27) | 0.9744 (38/39) |
| dependency_completeness (DC) | 0.15 | 1.0000 (4/4) | 1.0000 (3/3) |
| section_coverage (SC) | 0.15 | 0.8571 (6/7) | 1.0000 (7/7) |
| **quant_score** | | **0.8675** | **0.9413** |

Weighted contributions:
- A: 0.30×0.6667 + 0.25×1.0000 + 0.15×0.9259 + 0.15×1.0000 + 0.15×0.8571 = 0.2000 + 0.2500 + 0.1389 + 0.1500 + 0.1286 = **0.8675**
- B: 0.30×0.8333 + 0.25×0.9808 + 0.15×0.9744 + 0.15×1.0000 + 0.15×1.0000 = 0.2500 + 0.2452 + 0.1462 + 0.1500 + 0.1500 = **0.9413**

## RC — Requirement Coverage

Rule: a requirement counts as covered if its ID string appears in the variant (step 2), or if any 3 consecutive words of its description appear in the variant (step 3, lower-cased tokens `[a-z0-9-]+`).

| Req | Description (source) | A: ID | A: 3-word | B: ID | B: 3-word |
|-----|----------------------|-------|-----------|-------|-----------|
| R-001 | "The greet function MUST return the exact string Hello, Ada! for Ada." (`spec.md:6`) | no | no | no | no |
| R-002 | "The greet function MUST reject an empty name with ValueError." (`spec.md:9`) | yes (2 hits) | no | yes (1) | no |
| R-003 | "Tests MUST exercise the ordinary greeting and empty-input rejection." (`spec.md:12`) | no | no | yes (1) | no |
| T-101 | "implements R-001 ordinary greeting." (`completed.md:6`) | yes (2) | no | yes (1) | no |
| T-102 | "implements R-002 empty-name rejection." (`completed.md:7`) | yes (3) | no | yes (2) | no |
| T-103 | "implements R-003 both ordinary and empty-input tests." (`completed.md:8`) | yes (2) | no | yes (2) | no |
| **RC** | | **4/6 = 0.6667** | | **5/6 = 0.8333** | |

Notes:
- Neither variant names R-001 or matches its description, even though both address it through T-101.
- Only B names R-003 ("R-003 not accepted absent execution", risk 1).
- Sensitivity (not used): if a `spec.md:<line>` citation counted as a reference, B would also cover R-001 via `spec.md:6`, giving 6/6. A cites only `spec.md:9`, so it stays at 4/6. The protocol's matching rule is ID or keyword, so citations are not counted.

## IC — Internal Consistency

Claim units: each claim-bearing field value is split on `; ` and at sentence boundaries. The fields are `verdict`, `coverage_audit`, `class`, `severity`, `rationale`, `evidence_missing`, `why_not_classifiable`, `next_evidence_needed`, `decision_needed_by_user`, `risks[]`, `change` and `verifier`. Prose assertions inside `evidence` fields that go beyond a bare citation are added: A has 2 (T-101 "verification_ran false", T-103 "absent from changes.patch:1-9"); B has 6 (T-101 "verification_ran false", "execution.log:5 disclaims a run"; T-102 "broadening = D-1"; T-103 "absent from changes.patch:1-9", "completed.md:8 [x] and tasklist_completion_pct 1.0 overclaim acceptance", "T1 G-2 ... too broad: exercise is statically visible"). Metadata keys (`reviewer`, `persona`, `model_class`, `self_reported_confidence`) are excluded.

Scorable claims are all non-vague units (concrete + neither, from the SR table below). Vague units are not scorable, per the protocol.

| | Variant A | Variant B |
|---|-----------|-----------|
| Units total | 38 (36 field units + 2 evidence assertions) | 53 (47 field units + 6 evidence assertions) |
| Vague (excluded) | 2 | 1 |
| Scorable claims | 36 | 52 |
| Intra-variant contradictions | 0 | 1 |
| **IC** | **1 − 0/36 = 1.0000** | **1 − 1/52 = 0.9808** |

Contradictions found (category: opposing claims about the same subject):
- **B, 1**: T-103 evidence says "exercise is statically visible" (`variant-2-original.md:8`), but risk 1 says "R-003 not accepted absent execution" (`variant-2-original.md:23`). R-003's only verb is "exercise" (`spec.md:12`), so the two claims assign opposite outcomes to the same requirement. diff-analysis C-003 flagged this, and B's advocate conceded it (R1 concession 1).
- **A, 0**: The pairs checked were:
  - The D-1 `class: drift` against the recommendation "Drift (LOW) or no-deviation". The counter-view is hedged ("could be read") and so not scorable.
  - The T-103 "implemented" verdict against the gap question "whether static presence suffices for T-103 done". "Implemented" and "done" are different predicates.
  - Neither pair is an opposing claim. A's out-of-range citation `interaction-effects.yaml:14-21` is a citation defect, not an intra-variant contradiction, so it is not counted here (it belongs to qualitative Correctness).

## SR — Specificity Ratio

Rule: SR = concrete / (concrete + vague). Units are the same as for IC.
- A unit is **vague** if it matches `may|might|could|appropriate|as needed|properly|adequate|various|etc.|should consider|best practice(s)|industry standard`.
- Otherwise it is **concrete** if it contains a digit, a backtick, a `file.(py|md|yaml|log|patch|json)` name, an ID (`X-n`), a named entity (ValueError, ModuleNotFoundError, pytest, Bash, conftest, src), a threshold or class label (LOW/MEDIUM/HIGH, Drift/Authorized/Necessary/Regression, true/false), or a quoted literal.
- Units that are neither concrete nor vague drop out of SR.

| | Variant A | Variant B |
|---|-----------|-----------|
| Concrete (field units) | 23 | 32 |
| Concrete (evidence assertions) | 2 | 6 |
| **Concrete total** | **25** | **38** |
| Vague | 2 | 1 |
| Neither (excluded) | 11 | 14 |
| **SR** | **25/27 = 0.9259** | **38/39 = 0.9744** |

Vague units:
- A: rationale "Counter-view: `not name` is a common idiom for 'empty' and could be read as adherent/no deviation" (`could`).
- A: risk "[INFERRED] plain pytest may raise ModuleNotFoundError for src ..." (`may`).
- B: risk addendum "[INFERRED: may later mean blank]" (`may`).

Neither units:
- A: the three verdict labels, "No test execution", "diff/provenance for tests file", "diff including tests file or commit history", "whether omission from supplied diff is acceptable", "all verdicts static", "extra falsy handling untested", "only exercises ''", and "attach log".
- B: the three verdict tokens, "No requirement-bearing spec span absent from slice", "no git history", "no test hunk to classify", "pass/fail not observable", "unrun != contradiction", "spec says empty not blank", "spec has no type rule", "message unchecked (not required by spec)", "interaction-effects coverage is static only", "must not become runtime clearance", and "output saved".

## DC — Dependency Completeness

Rule: an internal reference is a reference from one part of the card to an item defined elsewhere in the same card. Here those are task IDs defined in `per_task` and deviation IDs defined in `deviations`. External references (file:line citations, `spec.md` requirement sections, `t1-card.md` items) are excluded, per the protocol's edge case.

| Variant | Internal references | Resolved | DC |
|---------|---------------------|----------|----|
| A | `mapped_task: T-102` (l.12) → per_task T-102. Risk "coupling T-101/T-102" (l.23) → T-101 and T-102. Gap 1 decision "T-103 done" (l.19) → T-103. | 4/4 | **1.0000** |
| B | T-102 evidence "broadening = D-1" (l.7) → deviations D-1. `mapped_task: T-102` (l.13) → per_task T-102. Rec 3 verifier "T-103 in_supplied_diff true" (l.31) → T-103. | 3/3 | **1.0000** |

Excluded as external:
- A's "t1-card.md (D-1)" (l.27) refers to the T1 card's D-1, not A's own.
- B's "T1 G-2" (l.8, l.20).
- A's `interaction-effects.yaml:14-21`. This citation is out of range, because the file has 13 lines (diff-analysis C-014). It is an external citation, so DC is unaffected. The defect is recorded for the qualitative Correctness dimension instead.

## SC — Section Coverage

Rule: count H2 headings. Both variants are YAML reviewer cards (prerequisites.md, `type_check` WARN), so each has 0 H2 headings. Fallback: top-level content keys are counted as sections. Identity and metadata keys (`reviewer`, `persona`, `model_class`) are excluded, consistent with SR's exclusion of metadata. This matches the section enumeration in diff-analysis S-001.

| Variant | Sections | Count | SC |
|---------|----------|-------|----|
| A | per_task, deviations, grounding_gaps, risks, recommendations, self_reported_confidence | 6 | 6/7 = **0.8571** |
| B | per_task, coverage_audit, deviations, grounding_gaps, risks, recommendations, self_reported_confidence | 7 | 7/7 = **1.0000** |

Sensitivity (not used): counting all top-level keys gives A 9/10 = 0.9000, and A's quant_score becomes 0.8739. B is unchanged. The ranking is unchanged.

## Result

| Variant | quant_score | quant × 0.50 |
|---------|-------------|--------------|
| A (sonnet:analyzer) | **0.8675** | 0.4337 |
| B (haiku:qa) | **0.9413** | 0.4707 |

Quantitative margin: B − A = 0.0738. The qualitative layer (A.2, the 30-criterion CEV rubric with position-bias passes) is not computed in this call.
