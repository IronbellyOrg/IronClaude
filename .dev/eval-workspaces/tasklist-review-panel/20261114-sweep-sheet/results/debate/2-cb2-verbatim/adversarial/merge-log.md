# Merge log

## Metadata
- Base: V3 (sonnet:architect)
- Executor: the orchestrator (main Sonnet session); the `merge-executor` agent was not used (it prefers Opus)
- Merged output: `../VERDICT.md`
- Changes planned (to study files): 0. Applied: 0. Failed: 0. Skipped: 0.
- Status: complete (PASS; nothing to apply to the study files)

## Changes applied to the merged output (VERDICT.md built from the artifacts)
| # | Section of VERDICT.md | Source | Note |
|---|---|---|---|
| 1 | 1 Verdict | `debate-transcript.md` convergence assessment, `debate/invariant-probe.md` summary | PASS because 0 blocking defects survived and 0 HIGH UNADDRESSED probe items |
| 2 | 2 Surviving blocking defects | `debate/round2-V1.md`, `round2-V2.md`, `round2-V3.md` route rulings; `adversarial/work/corrections.md` | the four verdict tests; route R-E treated at length because two advocates called it the strongest remaining attack; the orchestrator re-read `analysis/analyze.py` 1086-1100, `bin/check-order.sh` 70-95 and `TESTING.md` 223-228 |
| 3 | 3 Attack questions | V1, V2, V3 position papers and Round 1 | Z0 report counts corrected (237 not 591); the 0.001 to 0.003 figure kept only as an illustration of a guess |
| 4 | 4 Non-blocking notes N1 to N9 | probe INV-001 to INV-012, V2 R-G to R-I, V3 round 2 | N9 replaces V3's wrong sentence (b) |
| 5 | 5 Files changed, test run | file-time check (no file under `SW` or the repo newer than the first artifact, outside this folder) | no test run, because a PASS changes no file |
| 6 | 6 How the debate was run | all artifacts | limits stated: condensed scoring, orchestrator is Sonnet, advocate transcripts not inspectable |

## Post-merge validation
- Structural integrity: headings 1 to 6 in order, no level gaps. Pass.
- Internal references: file paths in VERDICT.md exist (`adversarial/work/corrections.md`, `adversarial/base-selection.md`, `debate/` files, the cited study files). Pass.
- Contradiction re-scan: the verdict says "all three advocates ended on NO" and "V2 started on YES"; V2's paper ends "YES, but NO if proof of bias is required". Consistent with the round files. Pass.
- Numbers re-derived by the orchestrator: 4.87% (0 of 60), 1.26% (0 of 237), 1.02% (0 of 291), 0.70, 0.95, 0.998 (at 2%, 5%, 10% over 60 reports), 59 Z0 runs in Stage 2. Pass.

## Summary
Planned 0, applied 0, failed 0, skipped 0.
