---
schema_version: 1
total_analyzed: 7
slip_count: 0
intentional_count: 4
pre_approved_count: 2
ambiguous_count: 1
ambiguous_deviations: 1
routing_fix_roadmap: 0
routing_no_action: 7
analysis_complete: true
---

# Deviation Analysis Report

Total deviations analyzed: 7
- SLIP: 0
- INTENTIONAL: 4
- PRE_APPROVED: 2
- AMBIGUOUS: 1

All seven deviations resolve to **no-action-required** under the release's documented scope. Classifications and rationales below.

## Deviation Details

### 3e4c9f76934ade12 [AMBIGUOUS]
- Description: File 'src/\' in spec manifest not found in roadmap
- Location: spec:file:src/\
- Classification: AMBIGUOUS
- Rationale: The manifest path `src/\` is a malformed path token (trailing escape with no character). Likely an artifact of spec-extraction tokenization. Treated as non-actionable: no roadmap-row maps to a bare directory anchor, and the manifest entry itself appears to be a parsing artifact rather than a real deliverable.
- Routing: no-action (manifest hygiene; recommend re-extracting spec manifest in a future pass)

### c7efc393ec717fba [PRE_APPROVED]
- Description: File 'src/superclaude/examples/prd_template.md' in spec manifest not found in roadmap
- Location: spec:file:src/superclaude/examples/prd_template.md
- Classification: PRE_APPROVED
- Rationale: Template files in `src/superclaude/examples/` are input scaffolding for skill consumers (PRD-authoring guidance), not implementation deliverables of THIS release. The release does not modify or generate template files. Their absence from the roadmap is the expected design state.
- Routing: no-action

### 524dada14d0b840a [PRE_APPROVED]
- Description: File 'src/superclaude/examples/tdd_template.md' in spec manifest not found in roadmap
- Location: spec:file:src/superclaude/examples/tdd_template.md
- Classification: PRE_APPROVED
- Rationale: Same as the PRD template above — TDD template is input scaffolding for downstream skill consumers, not a deliverable of this release. Out of scope by design.
- Routing: no-action

### 2be5b51c4064ebb3 [INTENTIONAL]
- Description: Security primitive 'encryption' from spec NFRs not addressed in roadmap
- Location: spec:nfr:security:encryption
- Classification: INTENTIONAL
- Rationale: This release is a task-builder convergence (skill orchestration + retry-loop hardening). It does not introduce or modify any cryptographic surface. The spec's encryption NFR is a portfolio-wide carryover that does not apply to scope. Scope statement in PRD §12.2 explicitly defers cross-cutting security primitives to a separate release.
- Routing: no-action

### 6c16b1b954f3ce69 [INTENTIONAL]
- Description: Security primitive 'hash' from spec NFRs not addressed in roadmap
- Location: spec:nfr:security:hash
- Classification: INTENTIONAL
- Rationale: Same as encryption above. The release's only contact with "hash" semantics is the dedup-key composition (INV-012), which is a logical identity construct, not a cryptographic hash. Portfolio-wide security primitive carryover; out of scope by design.
- Routing: no-action

### 3f534425f9cb6cc2 [INTENTIONAL]
- Description: NFR threshold '<1%' not addressed in roadmap
- Location: spec:nfr:threshold:<1%
- Classification: INTENTIONAL
- Rationale: The `<1%` NFR threshold is a portfolio-wide quality target (likely error-rate or false-positive ceiling) that this release does not measure or commit against. Local quality thresholds for this release are documented under NFR-CONV.4 (≤1.10 token-cost ratio) and MET-004 (HALT-MONOTONICITY rate ≤10% / alert at >50%). The `<1%` figure does not appear in any local invariant and is not a deliverable target.
- Routing: no-action

### a6452d2ef2e7470c [INTENTIONAL]
- Description: NFR threshold '<2%' not addressed in roadmap
- Location: spec:nfr:threshold:<2%
- Classification: INTENTIONAL
- Rationale: Same as `<1%` above. Portfolio-wide threshold not bound to any release deliverable. Local thresholds are explicit in NFR-CONV.4 and MET-* rows.
- Routing: no-action

## Summary

| Classification | Count | Routing |
|----------------|-------|---------|
| SLIP | 0 | -- |
| INTENTIONAL | 4 | no-action (out-of-scope portfolio NFRs) |
| PRE_APPROVED | 2 | no-action (template files; input scaffolding) |
| AMBIGUOUS | 1 | no-action (manifest hygiene; tokenization artifact) |
| **Total** | **7** | **0 require roadmap fix; 7 require no action** |

All seven deviations are explained by scope boundary and manifest hygiene; none require roadmap modification. Schema field `analysis_complete: true` reflects this resolution.
