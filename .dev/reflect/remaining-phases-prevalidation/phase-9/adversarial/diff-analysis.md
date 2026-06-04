# Diff Analysis — Phase 9 Unchecked-Item Pre-Validation

## Metadata
- Generated: 2026-06-02
- Variants compared: 3 (opus:architect, sonnet:analyzer, haiku:qa)
- Mode: B (source = Phase 9 items 9.11/9.12/PG9.1/PG9.2 + BUILD-REQUEST §R1.4/§MVR §3/§Contract #3)
- Items in scope: 9.11, 9.12, PG9.1, PG9.2 (the genuinely-unchecked subset; 9.7–9.10 are already `[x]`)

## Convergence (agreement points — high scrutiny applied per AD-2)

| # | Agreement | Variants | Classification |
|---|-----------|----------|----------------|
| C-001 | The driving prompt's "unchecked = 9.7–9.12" is wrong; real unchecked = 9.11, 9.12, PG9.1, PG9.2 (9.7/9.8/9.9 DONE, 9.10 N/A) | all 3 | STATED, verified against task file |
| C-002 | All four items are NECESSARY (spec-required) and NONE are superseded by 9.1–9.10 | all 3 | STATED |
| C-003 | The file-editing `build_remediation_prompt` (remediate_prompts.py:17) carries NO `roadmap_ids`; §3's "remediate roadmap_ids subset" belongs on the roadmap/tasklist-producing remediate surface, not this prompt | all 3 | STATED — **highest-severity shared finding** |
| C-004 | 9.11 must be split into H4's a/b/c/d(/e) per-sub-action structure; the body and the H4 preamble are inconsistent | all 3 | STATED |
| C-005 | PG9.1 check (a) "12 sub-steps all have schema+template+dual-write+parity" will FALSE-FAIL the by-design wiring exemption | all 3 | STATED |
| C-006 | 9.12 should consume `r1-4-cutover-counters.yaml` (H5 product) as SoT, not re-narrate a counter in prose | all 3 | STATED |
| C-007 | 9.12's completion criterion (≥3 release cycles) is structurally unsatisfiable within task lifetime → re-scope to initial-state decision + deferral | all 3 | STATED |
| C-008 | PG9.2 is structurally sound (standard L5 conditional act-on-verdict); KEEP | all 3 | STATED |
| C-009 | No step-count-budget risk: dual-write adds render paths, not pipeline steps (Acceptance Gate #6 ≤14 untouched) | architect (explicit), others implicit | STATED |

## Divergences (content differences)

| # | Topic | architect | analyzer | qa | Severity |
|---|-------|-----------|----------|----|----|
| X-001 | The "20 options" PRESERVE invariant | Surfaces that commands.py now has 30 @click.option (8 tool-write added 9.2–9.9); reads invariant as "20 pre-existing unchanged, additive allowed" (QA-accepted precedent) | not raised | not raised | MEDIUM |
| X-002 | Count reconciliation framing | "11 genuine + wiring exempt" | adds the {body 4-list} vs {H4 4-list} contradiction (remediate vs parity-test) | adds glob-count mismatch (9 txts today vs 12 expected vs 13 yaml) | LOW (all point same direction) |
| X-003 | PG9.2 verdict | KEEP + optional H2 Phase10-before-11.4 carry-forward note | KEEP + optional precision on recorded count | KEEP, clean once PG9.1 fixed | LOW |
| X-004 | 9.12 sequencing | re-scope + handoff | re-scope + handoff | ADDS: 9.12 must run AFTER 9.11 (input glob depends on secondary validation txts) | LOW (additive) |

## Shared assumptions (UNSTATED → promoted)

| A-NNN | Assumption | Impact | Status |
|-------|-----------|--------|--------|
| A-001 | The proven 9.2–9.9 tool-write recipe (schema+template+flag+param+tool_def+parity+registry) transfers cleanly to test_strategy/certify/reflect | If a secondary step's gate has a shape the recipe can't express, parity could be harder — but evidence (8 steps, 256/256) says recipe is robust | ACCEPTED (low risk) |
| A-002 | wiring_verification's yaml counter entry + remediate's yaml entry are interpreted as "exempt / parity-only" by 9.12 and PG9.1 | If interpreted literally as dual-write-pending-3-cycles, the readiness verdict mis-counts | PROMOTED → must be encoded in REFACTORs |

## Summary
- Structural/content differences: 4 (all low-medium, same-direction)
- Contradictions: 0 cross-variant (variants agree); 2 spec-internal contradictions surfaced (remediate dual-meaning C-003; 4-list vs 4-list X-002)
- Unique contributions: X-001 (architect: 20-option invariant audit), X-004 (qa: 9.12-after-9.11 sequencing)
- Convergence: 9/9 core points agreed → ~100% on verdicts (all REFACTOR×3 + KEEP×1); divergences are additive refinements, not conflicts
