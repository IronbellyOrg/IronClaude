# Merge Log — Step 11.2 parser decision

## Metadata
- Base: Variant 1 (Proposal A)
- Modification source: independent fault-finder INV-005 (envelope field is illegal + unused)
- Status: success
- Date: 2026-06-02

## Changes applied to the merged decision (decision.md)
1. **Adopted Proposal A** as base (relocate one canonical parser; 24 checks call it on `content`; delete duplicate parsers; consistency test; CodeAssertion escape hatch). Source: variant-1-proposal-A.md. Provenance: Base.
2. **Removed A's step 2 (add `frontmatter` field)** — incorporated fault-finder INV-005. Evidence: `tests/roadmap/test_pipeline_envelope.py:312` 8-field canon; `envelope.py:127` frozen; zero `envelope.frontmatter` consumers. Provenance: Variant-fault-finder, Change #1.
3. **Rejected Proposal B** in full. Rationale (changes NOT made): B's literal "read envelope.frontmatter" is infeasible at gate time and carries an 8-module + sprint blast radius for a problem all 24 checks solve locally. Source: variant-2-proposal-B.md.
4. **Added NFR-007 import-direction guidance** (prefer one pipeline-level parser imported by roadmap). New analysis; not in either original variant. Provenance: merge-synthesis.

## Task-file changes applied (user-authorized tasklist modification)
- Injected superseding `**REMEDIATION (sc:adversarial decision — 2026-06-02)**` block at the top of Step 11.2 in `TASK-RF-20260531-042405.md` (L637). Supersedes C1 sub-steps (a) and (d); keeps (b)/(c)/(f).
- Added a Phase 11 findings entry documenting the decision + modification.

## Post-merge validation
- Internal references resolve (all file:line citations re-verified against source 2026-06-02).
- No new contradictions introduced.
- Cross-check: decision keeps Contract #6 (one parser) AND `test_pipeline_envelope.py:312` green (no field) AND NFR-007 (import direction) — no contract is traded for another.

## Return Contract
```yaml
merged_output_path: ".dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/step-11-2-parser-decision/decision.md"
convergence_score: 1.00
artifacts_dir: ".dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/step-11-2-parser-decision/adversarial/"
status: "success"
base_variant: "Proposal A (relocate one canonical parser), modified per fault-finder INV-005"
unresolved_conflicts: 0
fallback_mode: true   # native grounded reasoning + 1 independent fault-finder (right-sized vs full multi-advocate spawn)
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants: []
```
