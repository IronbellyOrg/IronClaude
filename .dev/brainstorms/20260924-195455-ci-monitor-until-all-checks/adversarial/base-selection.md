# Base Selection

## Combined Scoring

| Variant | Quant (est) | Qual (est) | Combined | Eligible |
|---------|-------------|------------|----------|----------|
| V1 architect | 0.82 | 0.80 | 0.81 | yes |
| V2 refactorer | 0.88 | 0.87 | **0.875** | yes |
| V3 qa | 0.80 | 0.90 | 0.85 | yes |

Edge-case floor: all ≥1/5 (pending mix, empty stdout, halt-then-wait).

## Selected Base: Variant 2 (sonnet:refactorer)

Rationale: wait≠fix is the invariant that makes HALT stop *fix* not *wait*. Fewest files. Same FRs as V1 with less scaffolding.

## Strengths to preserve
- FR-W1–W9, wait-only after halt, REPORT_ONLY on CI findings when budget spent
- as_array never `--argjson ""`
- no `--ci-timeout`, no second round counter

## Strengths to incorporate
- V1: Wave 8 entry table in existing SKILL.md / ci-poll.md
- V3: AC-CLS-4 mix pending+pass test; T-CI-POLL-AS-ARRAY-EMPTY; T-CI-W8-AFTER-HALT; E9 note
