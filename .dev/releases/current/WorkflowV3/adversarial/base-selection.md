# Base Selection

## Combined Scoring (compressed)

| Variant | Quant (coverage+consistency+specificity) | Qual (complete/correct/clear/risk) | Combined |
|---------|------------------------------------------|-------------------------------------|----------|
| V1 architect | 0.86 | 0.80 | **0.83** |
| V2 analyzer | 0.78 | 0.84 | 0.81 |
| V3 backend | 0.82 | 0.76 | 0.79 |

Edge-case floor: all variants >1/5 (STOP tables, overlap, empty input). Eligible.

## Selected Base: Variant 1 (opus:architect)

Preserve: component layout, 03_project_plan headings, strategy-as-ref, Wave 3=Synthesize, no new agents, empty MCP.

Incorporate from V2: YAGNI cut list, evidence S1–S14 as problem appendix (short), `--validate`/`--parallel` as E-LEGACY, tasklist never synthesized.

Incorporate from V3: STOP enum, `.dev/workflow/` guard, persist source.md before plan, enterprise→depth deep unless explicit.

Reject: resume, ledger, deps.yaml, `--overlap` user flag, invoking sc-tasklist on plan.md.
