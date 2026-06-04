# Merge Log

Base: variant-1-opus-architect.md (state machine skeleton).
Output: ../merged-requirements.md

| Step | Change | Source | Provenance tag |
|------|--------|--------|----------------|
| 1 | Imported 5-stage state machine (S0–S4 + S-KILL), between-tool gate, CP-1/CP-2 | V1 base | [V1] |
| 2 | Imported "seam not weld" surface doctrine + never-link-sem-core + full-initiative kill switch | V1 base | [V1] |
| 3 | Inserted Eval Harness §with V2 scenario matrix (10 scenarios × tools × baselines) | V2 R-01 | [V2] |
| 4 | Inserted Metric Catalog §(RQ/SA/MC/CP/MCP, ~30 metrics w/ units+baselines+thresholds) | V2 R-02 | [V2] |
| 5 | Inserted Judging Protocol §(ground-truth tiers + blind adjudication + dedup; reject inspect keyword judge) | V2 R-03 | [V2] |
| 6 | Inserted Statistical Validity §(Simpson's, effect sizes, confidence labels, repeated-run) | V2 R-04 | [V2] |
| 7 | Per-tool hypotheses (H-sem/inspect/weave) folded into S1 sections | V2 R-05 | [V2] |
| 8 | Inserted Cost Model §(C1–C5 taxonomy) replacing V1's abstract cost columns | V3 R-08 | [V3] |
| 9 | **Resolved X-005**: multi-vendor token economics → provider-weighted token gate | V3 R-09 | [V3-KEY] |
| 10 | Latency harness + install matrix promoted into Phase 0 + Cost Model | V3 R-10/R-11 | [V3] |
| 11 | Merged scorecard: V2 value/cost/risk scorecards + V3 TCO 1-5 budgets (joint gate) | V2 R-06 + V3 R-12 | [V2+V3] |
| 12 | sem-collision 4-step neutralization into sem S0; usage-monitoring into S4; maintenance matrix into C4 | V3 R-13/R-14/R-15 | [V3] |
| 13 | **Promoted A-001..A-004 → Phase 0 pre-flight gates G0-1..G0-3 + CP-1 substrate stratification** | diff-analysis + invariant probe | [MERGE] |
| 14 | Tiered sample sizes: V3 5PR/3merge (shadow directional) + V2 20PR/10merge (graduate) | X-002 resolution | [V2+V3] |
| 15 | Data Sources & Corpus §(native→curated→synthetic→generalization) | V2 R-07 | [V2] |

## Validation
- Structural integrity: 14 top-level sections, contiguous; frontmatter present. ✔
- Internal references: all gate IDs (G0-*, CP-*, S0–S4) and metric IDs (RQ/SA/MC/CP/MCP) resolve. ✔
- Contradiction re-scan: X-001..X-005 all resolved (4 reconciled numerically, X-005 folded as provider-weighting). 0 unresolved. ✔
- Invariant probe: 4 HIGH items (A-001..A-004) addressed via Phase 0 gates. ✔
- Provenance: every grafted section tagged [V1]/[V2]/[V3]/[MERGE]. ✔

Unresolved conflicts: 0. Status: success.
