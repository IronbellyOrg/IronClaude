# Diff Analysis — Proposal A vs Proposal B (Step 11.2 parser remediation)

## Metadata
- Generated: 2026-06-02
- Variants: 2 (A = relocate one canonical parser; B = thread envelope into semantic-check dispatch)
- Mode: A (compare two authored proposals), depth=standard, blind=false

## Structural / Mechanism Differences

| # | Axis | Proposal A | Proposal B | Severity |
|---|---|---|---|---|
| S-001 | SemanticCheck signature | Unchanged (`Callable[[str], bool\|str]`) | Widened to carry envelope | High |
| S-002 | gate_passed dispatch | Unchanged | Modified to pass envelope to every check | High |
| S-003 | execute_pipeline (generic, shared w/ sprint) | Untouched | Must thread envelope into L267 gate call | High |
| S-004 | Control-flow ordering | Unchanged | Reorder extractor-before-gate | High |
| S-005 | In-gate data source | 24 checks parse their own `content` via the one canonical parser | 24 checks read `envelope.frontmatter` | Medium |
| S-006 | Parser count after change | 1 canonical (Contract #6 satisfied) | 1 canonical (Contract #6 satisfied) | Low (agree) |

## Contradiction with the substrate (verified facts)

| # | Point | Evidence | Impact |
|---|---|---|---|
| X-001 | Envelope never reaches semantic checks at gate time | `pipeline/gates.py:84` `check.check_fn(content)`; `pipeline/executor.py:267` `gate_passed(gate_target, step.gate)` (no envelope); `execute_pipeline` L63 has no envelope param | B requires generic-pipeline surgery; A needs none |
| X-002 | `envelope.frontmatter` not populated at current step's gate time | post-step extractor `roadmap/executor.py:1491` runs in `roadmap_run_step`; extractors write counts/artifacts only, no frontmatter field | B requires a reorder; A sidesteps |
| X-003 | Tier already exists for envelope-aware gating | `CodeAssertion` `models.py:108`, dispatched `gates.py:100` with `(envelope, repo_root)` | B duplicates CodeAssertion |

## Unique contributions
- U-001 (A): explicit escape hatch — any genuinely cross-step check becomes a `CodeAssertion`, not a widened SemanticCheck. Value: High (respects the R1.3 two-tier model).
- U-002 (B): most literal reading of 11.2(d) "no re-parsing." Value: Low (the literal reading is infeasible at gate time per X-001/X-002).

## Shared assumptions (A-NNN) — surfaced
- **A-001 [SHARED-ASSUMPTION, CONTRADICTED]:** BOTH proposals assume a `frontmatter: dict` field should be added to `PipelineEnvelope` (A step 2 / B step 6; mirrors task Step 11.2(a)). **CONTRADICTED by evidence:** `tests/roadmap/test_pipeline_envelope.py:312` asserts the envelope field-set is EXACTLY the §MVR §1 8 fields; `frontmatter` ∉ set; envelope is `frozen=True` (`envelope.py:127`); zero consumers of `envelope.frontmatter` in `cli/`. → The field-add is illegal + unused. This is the decisive finding: it is removable from A, but load-bearing (hence unshakable) for B.

## Summary
- High-severity mechanism differences all favor A (smaller, dispatch-preserving).
- The single highest-impact finding (A-001) indicts a sub-step shared by both proposals AND by the task text — resolved by dropping the field from A, which B cannot do.
