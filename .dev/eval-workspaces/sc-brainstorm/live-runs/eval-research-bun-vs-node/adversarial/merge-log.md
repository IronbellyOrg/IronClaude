# Merge Log

**Run**: eval-research-bun-vs-node
**Final convergence**: 0.82 (PASS, threshold 0.75)
**Base**: V1 (opus/analyzer)
**Augmentations**: V2 (sonnet/architect), V3 (haiku/scribe)

## Operations applied (in order)

1. Accept V1 as base structure (six-axis comparison + workload-scoped recommendation).
2. From V2: elevate native-module / APM / FaaS hosting compatibility to a separate top-line NFR.
3. From V2: absorb hosting platform support inline under operations rather than a separate appendix.
4. From V3: replace V1's prose risk paragraph with a structured `## Risks` table (Risk / Likelihood / Mitigation).
5. From V3: replace V1's single-line recommendation with a decision rule (adopt where X, pilot where Y, defer where Z).
6. From V3: add pilot exit criteria as a measurable acceptance criterion (performance, compatibility, operability gates).
7. Brainstorm normalization: add `## Provenance` section attributing each FR / NFR / AC / risk / open question to its source variant(s) and seed-brief anchor(s).
8. Brainstorm normalization: verify all seed-brief `must_preserve` anchors retained as requirements, criteria, or constraints.
9. Brainstorm normalization: verify no `out_of_scope` items promoted into requirements.
10. Frontmatter populated with `schema_version: 1.0`, `adversarial_status: pass`, `convergence_score: 0.82`, `fit_to_intent: pass`, empty `unresolved_conflicts` list.

## Dropped content (with rationale)

- V1's flat "single recommendation" — superseded by the V3 decision-rule pattern (more actionable, more defensible).
- V2's separate "hosting platform support appendix" — absorbed inline into operations NFR; appendix would have duplicated content.
- V3's specific numeric scoring weights — workload-specific and not generalizable; the decision-rule pattern is retained without prescribing weights.

## Anchor traceability

Every `must_preserve` anchor maps to at least one requirement, acceptance criterion, or risk row:

- "Bun runtime as primary candidate" → FR-1, FR-2, FR-3.
- "Node.js runtime as incumbent / comparator" → FR-1, FR-2.
- "backend services as the workload context" → FR-3, AC-1, AC-3.
- "deep research enrichment required" → NFR-6 (research provenance), Provenance.
- "no codebase enrichment" → NFR-6, Out of Scope, Provenance.
- "actionable adoption / retention / pilot decision" → FR-5, AC-4, AC-5.

## Unresolved conflicts

No blocking conflicts. Two workload-specific questions surface in `## Open Questions` rather than being resolved unilaterally.
