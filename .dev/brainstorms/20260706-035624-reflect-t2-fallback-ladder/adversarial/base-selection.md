# Base Selection

## Quantitative Summary

| Variant | Requirement coverage | Specificity | Risk coverage | Testability | Combined score |
|---|---:|---:|---:|---:|---:|
| Variant 1 — Architect | 0.90 | 0.82 | 0.82 | 0.78 | 0.83 |
| Variant 2 — Analyzer | 0.96 | 0.92 | 0.94 | 0.88 | 0.93 |
| Variant 3 — Backend/Refactorer | 0.92 | 0.88 | 0.86 | 0.96 | 0.91 |

## Qualitative Findings

- Variant 1 has the cleanest architecture boundary language and strongest warning against invisible replacement semantics.
- Variant 2 has the best state machine, terminal failure taxonomy, and return-contract terminal-reason enum.
- Variant 3 has the best implementation sequencing, minimal-risk rollout, and test seam discipline.

## Selected Base

Variant 2 is selected as the base because it most completely resolves the key semantic ambiguity: exactly when fallback engages, when `T1Model02` engages, and how the terminal degraded states remain honest.

## Incorporated Strengths

- From Variant 1: explicit reflect/swarm seam, append-only ledger framing, and `original_primary_pool_fully_succeeded`/certification-basis language.
- From Variant 3: staged implementation plan, contributor selection helper, stub-first integration, and warning that first implementation can stay localized before extracting.

## Decision

Use Variant 2 as base, merge Variant 1’s boundary terminology and Variant 3’s rollout/test discipline.