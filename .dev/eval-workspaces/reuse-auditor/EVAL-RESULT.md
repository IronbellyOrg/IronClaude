# reuse-auditor agent eval — 2026-06-07

**Verdict: PASS** (grounded behavioural eval against live code).

## Fixture note
The brainstorm's canonical pair (`_bind_specs` vs `_inject_*`) could not be used —
`_bind_specs`/`_persist_bound_specs` does **not exist** in the tree at this commit
(`grep -rn 'def _bind_specs'` → empty; it survives only as prose in the spec/agent).
Substituted a **real, live** instance of the exact idiom the feature targets: the
roadmap/sprint post-LLM frontmatter-injection family.

## Positive fixture — `_inject_provenance_fields` (roadmap/executor.py:715)
| Assertion | Expected | Got | ✓ |
|---|---|---|---|
| tier | confident-duplicate | confident-duplicate | ✓ |
| verdict | extract-shared / mirror-shape | extract-shared | ✓ |
| S_reuse | ≈0.82–0.90 band | 0.90 | ✓ |
| C_cap floor ≥0.80 | pass | 0.91 | ✓ |
| C_shape floor ≥0.70 | pass | 0.88 | ✓ |
| name-agnostic neighbour find | finds `_inject_pipeline_diagnostics` + cross-module `_inject_source_field` | both found, re-Read-verified | ✓ |
| consolidation | N≥2, centralize | N=2, recommend_centralize=true | ✓ |
| evidence_grounded | true | true | ✓ |

## Negative fixture — `validate_session_id` (install_hooks.py:537)
| Assertion | Expected | Got | ✓ |
|---|---|---|---|
| tier | distinct | distinct | ✓ |
| verdict | distinct | distinct | ✓ |
| S_reuse | <0.65 | 0.55 | ✓ |
| shared-verb exclusion fires | yes (found `validate_eval_id` etc. but rejected) | C_cap 0.54 < floor → distinct | ✓ |

The negative case is the stronger proof: the agent **did** surface same-verb
neighbours (`validate_eval_id`, eval-id path-safety guards) and correctly rejected
them via the two-floor guard + shared-verb exclusion — no false positive.

## Minor finding (non-blocking)
The agent has no `Write` tool (frontmatter `tools:` = Read/Grep/Glob/auggie/serena),
so it **emits** `reuse-audit.yaml` as its final message rather than writing it; the
caller persists it. This matches the `evidence-validator` template precedent exactly
(same no-Write pattern). Wording in the agent ("Your only write is reuse-audit.yaml")
is aspirational vs the toolset — candidate for a one-line tightening, not a defect.
