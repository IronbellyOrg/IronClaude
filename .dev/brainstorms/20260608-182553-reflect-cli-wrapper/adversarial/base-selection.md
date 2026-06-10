# Base Selection

## Combined scores (quant 0.50 + qual 0.50)
| Variant | Quant | Qual (/30) | Combined | Edge-case floor |
|---------|-------|-----------|----------|-----------------|
| V1 opus:architect | 0.88 | 26/30 (0.87) | **0.875** | pass (4/5) |
| V2 sonnet:analyzer | 0.83 | 25/30 (0.83) | 0.830 | pass (5/5) |
| V3 haiku:backend | 0.80 | 22/30 (0.73) | 0.765 | pass (3/5) |

## Selected base: **Variant 1 (opus:architect)**
Rationale: highest completeness + structure + integration plan; the load-bearing NOT-HomeIsolation boundary; reuse map with real anchors; opt-in reversible template flag. Tiebreak not needed (V1 leads by >5%).

## Strengths to incorporate from non-base:
- From V2: fail-closed `degraded` verdict + post-contract degradation checklist (U-001); summarize_changes:unavailable not-a-halt (U-002); compare-before-write + sidecar (U-003); 4-state verdict vocab.
- From V3: stdin prompt delivery (U-004); atomic os.replace + yamllint dumper (U-005); concrete file layout + main.py line (U-006); --no-promote as hard prompt flag.
- Correct V3's X-001: reflect `--output` belongs in the prompt, not the claude argv.
