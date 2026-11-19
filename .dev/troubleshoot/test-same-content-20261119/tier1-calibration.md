# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/troubleshoot/test-same-content-20261119/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-19T01:26:55Z
(Persisted by the parent from the `confidence-calibrator` agent's returned report.)

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | `install_keep.py:21` is `return filecmp.cmp(a, b, shallow=False)`; `except OSError` at :22-23 matches; `tests/cli/test_install_keep.py:39-43` matches the card; behaviour-definitions row 1 holds the verbatim `_cache.get((f1, f2, s1, s2))` and `_sig` source. |
| Runtime check | 1.0 | Cross-tab (`runtime_behavior`, `runtime_repro`) gives 1.0: captured probe shows equal signatures and a True second call; a second probe replays the exact test sequence 200 times (188 wrong True, always when the mtime was unchanged) and flips to False after `clear_cache()`. The card's own 0.5 predates that evidence and was not used. |
| Symptom coverage | 1.0 | Explains the failure at :43, the intermittence, and the `make test` failures. |
| Reproducibility fit | 1.0 | A reproducer exists and matches the cited cause. The mtimes inside the failing pytest process were not recorded at calibration time (closed afterwards by the parent, see REPORT). |
| Fix directness | 1.0 | One line (`filecmp.clear_cache()`) at the single producer (producers.md P1); the probe applied it to a local copy and got False. |
| Domain coherence | 1.0 | One domain: a stdlib cache behaviour against a test and docstring contract. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 1.00 | all six dimensions score 1.0 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | always applies |
| gate_M2: runtime_check + 0.30 | 1.30 | always applies |
| gated_min | 1.00 | min of the three |
| verdict_cap | none | M3a not binding: claim_class runtime_behavior but runtime_check is 1.0 |
| **calibrated** | 1.00 | no structural cap fired |
| spot_check_unverifiable | none | no remote URLs cited |
| structural_flags | none | C1, C2, C3, C3b, C5, C8 evaluated and not fired; C4, C6, C7 skipped for missing inputs |

## Confidence

- **Self-reported (in card)**: 0.85 (read, not used in scoring)
- **Calibrated (this report)**: 1.00
- **Formula applied**: `min(mean(all_six)=1.00, EG+0.30=1.30, RC+0.30=1.30)` = 1.00; verdict-direction cap does not apply (runtime_check is 1.0); no structural cap fired.
- **Delta**: +0.15 (the card self-scored Runtime check and Reproducibility at 0.5 before the 200-run replay was added).

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 1, Hard stops: "`--no-escalate` set → STOP at Tier 1 (regardless of confidence)." Without that flag rule 3 would have fired `intermittent`.
- **Execution restriction**: `--no-escalate` is set; C1 did not fire.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | Calibrated 1.00 is not below 0.50; the headline is not an enum token (producers.md: observation-kind string). |
| C2 | no | — | — | The card excludes no enum; producers.md gives the exit statement at install_keep.py:21. |
| C3 | no | — | — | The card cites no control arm; the `clear_cache()` contrast is a probe result. |
| C3b | no | — | — | execution-locus.md gives RUN-SITE and SAME-ENV yes, so runs-in is known. |
| C4 | skipped | — | — | input absent: tasklist_path (null: verdict sufficient, no discriminator required); card has a Falsification standard and no measurement-row table. |
| C5 | no | — | — | Card Timestamp 2026-11-19T01:26:20Z; card_mtime 2026-11-19T01:26:47Z. |
| C6 | skipped | — | — | input absent: tasklist location; the headline asserts no numeric threshold. |
| C7 | skipped | — | — | input absent: tasklist_path; the timestamp-tick property is backed by captured probe counts. |
| C8 | no | — | — | behaviour-definitions.md row 1 has Status `fetched:raw-source`; the card cites row 1. |

## Notes

- All cited lines verified by Read: `install_keep.py:21-23`, `tests/cli/test_install_keep.py:37-43`, `install_core.py:121-125` (same `filecmp.cmp` call in the private `_same_content`). The caller lines (`install_user_setup.py:90`, `install_commands.py:61`) were not re-read by the calibrator.
- `input_absent: tasklist_path`.
- Residual gap named by the calibrator: mtimes and `filecmp._cache` inside a failing pytest process were not captured; the parent captured them afterwards (tier1-observation.md, "Parent probe 3").
- The proposed deterministic test needs `import os`.
- Calibrator limits: only Read; it did not re-run the probes.
