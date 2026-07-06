# Base Selection — Detection Contract Setup

## Quantitative Scoring

| Variant | Coverage | Specificity | Minimal-risk path | Edge cases | Score |
|---|---:|---:|---:|---:|---:|
| Variant 1 — architect | 0.92 | 0.86 | 0.78 | 0.82 | 0.85 |
| Variant 2 — refactorer | 0.88 | 0.84 | 0.96 | 0.78 | 0.87 |
| Variant 3 — qa | 0.90 | 0.88 | 0.74 | 0.96 | 0.87 |

## Qualitative Scoring

| Variant | Strengths | Weaknesses | Qual Score |
|---|---|---|---:|
| Variant 1 | Clear boundaries, metadata model, integration ownership | Slightly larger initial surface | 0.88 |
| Variant 2 | Safest incremental path, reuse-first, avoids parser duplication | Less comprehensive edge-case taxonomy | 0.90 |
| Variant 3 | Strong validation and test coverage, stale/wrong evidence matrix | Strict decline stance may overblock v1 | 0.89 |

## Selected Base

Variant 2 is selected as the base because it best preserves current fail-closed behavior while improving UX in small reversible slices. Variant 1 contributes architecture and metadata. Variant 3 contributes validation policy, stale/wrong evidence handling, and acceptance tests.

## Incorporation Plan

- Add Variant 1's shared-helper ownership model and metadata/provenance fields.
- Add Variant 3's UX state taxonomy, evidence rejection matrix, and tests.
- Keep Variant 2's implementation order and reflect diagnose-only v1 posture.
