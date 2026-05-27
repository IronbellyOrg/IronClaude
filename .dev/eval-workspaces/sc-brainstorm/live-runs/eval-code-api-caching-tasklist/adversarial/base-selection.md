# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---:|---:|---:|---:|
| Requirement coverage | 0.30 | 0.86 | 0.90 | 0.78 |
| Internal consistency | 0.25 | 0.92 | 0.90 | 0.94 |
| Specificity ratio | 0.15 | 0.82 | 0.88 | 0.80 |
| Dependency completeness | 0.15 | 0.80 | 0.86 | 0.76 |
| Section coverage | 0.15 | 0.86 | 1.00 | 0.86 |
| **Quant score** | **1.00** | **0.86** | **0.91** | **0.84** |

## Qualitative Scoring (50% weight)

| Dimension | Variant 1 | Variant 2 | Variant 3 |
|---|---:|---:|---:|
| Completeness | 4/5 | 5/5 | 4/5 |
| Correctness | 5/5 | 5/5 | 5/5 |
| Structure | 5/5 | 4/5 | 4/5 |
| Clarity | 4/5 | 5/5 | 4/5 |
| Risk coverage | 4/5 | 5/5 | 5/5 |
| Invariant & edge coverage | 3/5 | 4/5 | 4/5 |
| **Qual score** | **0.83** | **0.93** | **0.87** |

## Combined Scoring

| Variant | Quant | Qual | Combined |
|---|---:|---:|---:|
| Variant 1 — architect:opus | 0.86 | 0.83 | 0.845 |
| Variant 2 — backend:sonnet | 0.91 | 0.93 | 0.920 |
| Variant 3 — security:haiku | 0.84 | 0.87 | 0.855 |

## Selected Base: Variant 2 (backend:sonnet)

Variant 2 is selected as the base because it has the strongest implementation-actionable requirements, explicit invalidation and resilience coverage, and the most complete testing/rollout section. Variant 1's policy registry and Variant 3's security classification are mandatory incorporations.

## Strengths to Preserve

- Read-through mechanics for approved endpoints.
- Mutation-driven invalidation and manual purge scopes.
- Stampede protection.
- Shadow-mode to cohort rollout sequence.
- Load, integration, and fault-injection testing.

## Strengths to Incorporate

- From Variant 1: endpoint policy registry and policy-version observability.
- From Variant 3: deny-by-default endpoint sensitivity classification, security approval for sensitive scopes, audit logs for purge/policy changes, and explicit tenant/auth key requirements.
