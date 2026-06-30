# Diff Analysis: reflect-into-review-audit Proposal Comparison

## Metadata
- Generated: 2026-06-04
- Variants compared: 3 (A=additive single-agent · B=replacement · C=reject)
- Focus areas: integration-fit, overlap-risk, token-cost, maintainability
- Categories: structural (2), content (5), contradictions (4), unique (4), shared assumptions (4)

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| S-001 | Decision shape | Per-target, single seam each | Per-target, replace verifier | Global reject + per-target concession | Medium |
| S-002 | Confidence granularity | Split (auggie 88% / audit 72%) | Split (45% / 40%) | Split (full-reflect 90% / even-A 68%) | Low |

## Content Differences

| # | Topic | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| C-001 | Which reflect element | `evidence-validator` only | whole `/sc:reflect --mode post` | none | High |
| C-002 | auggie-review Wave-3 citation gap | Fill with disjoint-context evidence-validator | Replace inline+auggie-reviewer wholesale | Human reviewer already is the disjoint check | High |
| C-003 | cleanup-audit validate step | Add 100% evidence-validator (DELETE/CONSOLIDATE) | Replace 10% audit-validator w/ reflect | Keep audit-validator; reflect reuses it anyway | High |
| C-004 | Token cost | +2–8k / run | +35–70k +10–25k auggie | +0 | High |
| C-005 | Where reflect belongs | new seam (Wave 3 / Validate) | upstream verifier | already wired (remediation C/E) | Medium |

## Contradictions

| # | Point of Conflict | A Position | B Position | C Position | Impact |
|---|---|---|---|---|---|
| X-001 | Is the disjoint-context property worth its cost for *recommendations*? | Yes, cheaply (evidence-validator) | Yes, fully (ensemble) | No — recommendations ≠ applied work; human gates them | High |
| X-002 | Does R0/PR#112 evidence transfer to read-only review/audit? | Partially (cite as existence proof of citation drift) | Yes (disjoint-set property) | No — it's applied-change QA; cannot occur when nothing applied | High |
| X-003 | cleanup-audit + reflect = ? | non-circular IF only evidence-validator | circular (reflect re-runs audit-validator) | circular → self-defeating; reject | High |
| X-004 | Is the minimal add (A) above the bar? | Yes (~88% auggie / ~72% audit) | n/a (wants more) | Open (~68% — C's least-confident point) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | A | "evidence-validator ≠ audit-validator, so no circular overlap" — the one non-circular reflect element for cleanup-audit | High |
| U-002 | A | Scope-gating cleanup-audit's 100% re-Read to DELETE/CONSOLIDATE only (destructive recs) | Medium |
| U-003 | B | Names the semantic-fit defect explicitly: review findings ≠ "completed work", so UC-2 deviation taxonomy has no referent | High |
| U-004 | C | "The human who gates a recommendation IS the disjoint context" — reframes the entire value proposition | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | Cost figures (35–70k Tier2; +2–8k evidence-validator) are accurate | all cite `integration-analysis.md:347` for Tier-2; A estimates evidence-validator | UNSTATED (evidence-validator cost is an estimate, not measured) | YES |
| A-002 | One reflect element (evidence-validator) optimally fills BOTH targets' gaps, though the gaps differ (auggie=same-context citation; audit=10% sample) | A applies it to both | UNSTATED | YES |
| A-003 | A citation gate is purely additive safety — a drop-not-downgrade gate never removes a *correct* finding whose citation was merely imprecise | all assume evidence-validator only improves precision | UNSTATED (false-drop / recall-loss risk unaddressed) | YES |
| A-004 | review/audit outputs are recommendations a human gates (not auto-applied) | B & C state it; A implicitly relies on it | STATED (B `:falsifiable`, C Pillar 4) | NO |

### Promoted [SHARED-ASSUMPTION] diff points
| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | evidence-validator cost is estimated, not measured | If +2–8k is wrong on large audits, A's cost edge over B narrows | UNSTATED → debate |
| A-002 | one agent fits two different gaps | If the gaps need different treatment, "A for both" is wrong; maybe A-for-auggie only | UNSTATED → debate |
| A-003 | citation gate has no false-drop / recall cost | A drop-not-downgrade gate on imprecise-but-correct findings could *lower* review recall | UNSTATED → debate (highest-value probe target) |

## Summary
- Total structural: 2 · content: 5 · contradictions: 4 · unique: 4 · shared assumptions: 4 (UNSTATED: 3, STATED: 1)
- Highest-severity items: C-001, C-002, C-003, C-004, X-001, X-002, X-003, U-001, U-003, U-004, A-003
- **Convergence note:** all three variants already agree B is weak (semantic-fit + circular overlap). The live disagreement is narrow: **A vs C on the cheap `evidence-validator` add, per-target.** Expect high convergence on "reject B" and contested convergence on X-004.
