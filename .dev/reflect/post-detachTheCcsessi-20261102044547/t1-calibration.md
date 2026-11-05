# Tier 1 calibration (confidence-calibrator, model class opus; persisted by the orchestrator on receipt, 2026-11-02T04:57Z)

Calibrated C = 0.62 (card self-report 0.88). Recommendation: ESCALATE.

| # | Dimension | Score | Justification (calibrator) |
|---|---|---|---|
| 1 | Citation grounding | 0.85 | 13 of 14 checked citations held to the line; `live-check/after.txt:2-5` is under `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/`, not where the card's path resolves; "no leftover test shim", "ruff exit 0" and "T3.AC1/AC2 pass: verify-logs" lack a cited log |
| 2 | Coverage completeness | 0.85 | all 5 tasks and 6 hunks covered; T4.AC4 (live pids unchanged), T4 `bash -n`, T3.AC2 interim log and T1.AC3/T2.AC2 cleanup not evidenced in the card |
| 3 | Deviation-classification clarity | 0.75 | D1-D3 single class each; D1/D2 have inline rationale; D3 heading suffix has none and a convention is a weak fit for Necessary |
| 4 | Risk surface coverage | 0.40 | no risk register; pre-execution residuals (detached shims accumulate, interrupted pytest orphans) not carried; S_domains=3 and the grounding-gaps status effect not stated |
| 5 | Recommendation actionability | 0.25 | no recommendations section |

C = (0.85 + 0.85 + 0.75 + 0.40 + 0.25) / 5 = 0.62

Citations checked: test_ccsession_tiers.py:1452, 1536, 1538, 1541, 1543, 1554-1563; package artifacts/t1-before.log:16-20, 25-39; local-gateway-alias-proxy.py:861-869; ccsession:804-829; CHANGELOG.md:7-11, :38; verify-logs/pytest-ccsession.stdout.txt:17; artifacts/tasklist-diff-map.md:16; progress.md:4 — all held except the after.txt path resolution.

Escalation: low_confidence (C 0.62 < 0.85) and multi_domain (S_domains = 3).

Rubric defect reported: refs/reflection-rubric.md:39 names dimension-3 classes {Aligned, Refinement, Drift, Regression}; refs/deviation-taxonomy.md uses {Authorized, Necessary, Drift, Regression}. Scored against the taxonomy.
