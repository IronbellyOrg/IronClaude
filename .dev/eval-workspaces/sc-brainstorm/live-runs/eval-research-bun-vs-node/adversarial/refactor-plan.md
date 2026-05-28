# Refactor Plan — Base + Augmentation

**Base**: V1 (analyzer/opus) six-axis comparison + workload-scoped recommendation.

## Augmentations applied

1. Elevate native-module / APM / FaaS hosting from a sub-bullet of "ecosystem" into a top-line NFR (from V2).
2. Add a formal `## Risks` table (Risk / Likelihood / Mitigation) replacing V1's prose risk paragraph (from V3).
3. Replace V1's single-line recommendation with a structured decision rule: "adopt where X, pilot where Y, defer where Z" (from V3).
4. Add pilot exit criteria under acceptance criteria — performance, compatibility, operability gates (from V3).
5. Move hosting platform support inline into operations requirements (from V2).
6. Add explicit `## Provenance` section attributing each FR / NFR / AC / risk / open question to source variant(s) and seed-brief anchors (brainstorm-owned normalization layer).

## Sections produced

- `## Functional Requirements`
- `## Non-Functional Requirements`
- `## Acceptance Criteria`
- `## Risks` (table)
- `## Open Questions`
- `## Provenance`

## Anchor preservation

All six seed-brief `must_preserve` anchors verified present in the final merged spec. Cross-reference in `## Provenance`.

## No-scope-creep check

- No `out_of_scope` item promoted to requirement.
- Codebase introspection explicitly excluded (NFR-6, Out of Scope reference).
- Browser / frontend, Deno, and implementation work all excluded.
