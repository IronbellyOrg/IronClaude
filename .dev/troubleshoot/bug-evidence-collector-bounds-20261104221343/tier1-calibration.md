# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/tier1-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-04T22:24:20Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

`runtime_observed` mapped to `runtime_repro` (captured executed probe verified in probe-evidence.out / probe-evidence.sh).

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | E3-E7 match (collect-conflict-evidence.sh:82-86, :147-151, :185, :193-194; conflict-intent.md:19, :30; conflict-mechanical.md:71, :247, :249); E1-E2 match probe-evidence.out:4-8. E8 line mismatch in the working copy (claim true; supporting row only) |
| Runtime check | 1.0 | mixed = min(A2 runtime_repro 1.0, C1 runtime_repro 1.0); probe-evidence.out:7-8 and :1-6 |
| Symptom coverage | 1.0 | behaviour definitions (a) and (b) both explained |
| Reproducibility fit | 1.0 | deterministic; hermetic scratch repo |
| Fix directness | 0.5 | A2 local to bounded(); C1 changes a layout contract across both refs and the e2e tests plus an attempt-count rule |
| Domain coherence | 0.5 | two independent defects sharing one script: shell runtime logic (A2) and a protocol-doc layout collision (C1) |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.83 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 1.30 | |
| gated_min | 0.83 | |
| verdict_cap | none | |
| calibrated before structural caps | 0.83 | |
| **calibrated** | 0.50 | C7 cap (<= 0.5) |
| spot_check_unverifiable | none | |
| structural_flags | uncited (C7) | C6 skipped (no tasklist_path) |

## Confidence

- **Self-reported (in card)**: 0.85
- **Calibrated (this report)**: 0.50
- **Formula applied**: min(0.83, 1.30, 1.30) = 0.83, then C7 cap min(0.83, 0.50) = 0.50

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 (signal-driven): confidence < 0.85; independently multi_domain (Domain coherence 0.5)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.50 not below 0.50; headline has no enum token |
| C2 | no | — | — | no enum excluded; producers.md header-only |
| C3 | no | — | — | no control arm cited |
| C3b | no | — | — | runs-in known (tier1-hypothesis.md:11; execution-locus.md:2-3) |
| C4 | no | — | — | direct code changes with a falsification standard |
| C5 | no | — | — | Timestamp line carries no value |
| C6 | skipped | — | — | input absent: tasklist_path |
| C7 | yes | uncited | calibrated capped at <= 0.5 | card names the environment property "PATH without `timeout`" (:11) and "macOS does not ship it" (:53) with no cited 2x2 row |
| C8 | no | — | — | behaviour-definitions.md rows 1-3 with non-empty Status |

## Notes

- E8 cites test_conflict_scripts.py:1393-1394 at HEAD e2f77381 (correct there: `if real_timeout is None:` / `pytest.skip(...)`); the calibrator read the working copy, where fix-pass test insertions moved it to :1455-1456.
- The A2 probe discards the collector's stdout, so the `EVIDENCE_FAIL timeout` token is inferred, not observed.
- The C1 probe runs the collector twice into the same --out; it does not run the real abort-and-restart; the link rests on the refs (E6, E7).
- Tier 2 should treat A2 and C1 as separate hypotheses.
