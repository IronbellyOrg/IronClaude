# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-tier1-lock-trust-20261104221453/tier1-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-04T22:25:10Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

`runtime_observed` mapped to `runtime_repro` (captured parent probe).

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | conflict-mechanical.md:84-90, :296; conflicts.py:202-210, :11-21; test_conflicts_core.py:2445, :2473; pyproject.toml:16; test.yml:22; SKILL.md:219; pr-submit.md:54 all match; probe marker is probe-lock-trust.out:6 (card says :5) |
| Runtime check | 1.0 | mixed = min(runtime part: executed probe, backend executed: yes; static part 1.0); path/editable arms unobserved (E9) |
| Symptom coverage | 1.0 | the reported finding is fully explained by the missing gate before `uv lock` with Tier 1 default |
| Reproducibility fit | 1.0 | deterministic offline reproducer |
| Fix directness | 0.5 | right place but wide: conflicts.py, test_conflicts_core.py, conflict-mechanical.md, SKILL.md, pr-submit.md, test_conflict_sync_protocol.py; conditional command form; 3.10 fail-closed |
| Domain coherence | 0.5 | security trust gate + stdlib-only library with a portability constraint + protocol prose + tests |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.83 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 1.30 | |
| gated_min | 0.83 | |
| verdict_cap | none | |
| **calibrated** | 0.83 | |
| spot_check_unverifiable | none | |
| structural_flags | none | C6 skipped (no tasklist_path) |

## Confidence

- **Self-reported (in card)**: 0.85
- **Calibrated (this report)**: 0.83
- **Formula applied**: min(0.8333, 1.30, 1.30) = 0.83

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 (signal-driven) confidence < 0.85; secondary multi_domain (Domain coherence 0.5)
- **Execution restriction**: none (audit.log header: no_escalate false, depth standard)

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.83 not below 0.50; no enum headline token |
| C2 | no | — | — | no enum exclusion |
| C3 | no | — | — | no control arm in execution-locus.md; the post-fix command check is not a control arm (would not change the verdict) |
| C3b | no | — | — | runs-in stated (tier1-hypothesis.md:11) |
| C4 | no | — | — | code and test fix, no measurement row |
| C5 | no | — | — | no Timestamp value |
| C6 | skipped | — | — | input absent: tasklist_path |
| C7 | no | — | — | the 3.10/tomllib fact is a fix constraint cited to file:line (E6); the cause is not environment-dependent |
| C8 | no | — | — | behaviour-definitions.md rows 1-3 non-empty Status |

## Notes

- Probe marker line is probe-lock-trust.out:6, not :5.
- Only backend-path + dynamic was probed (together); path/editable arms unobserved; the gate is a conservative superset.
- Untested: direct URL/path references in project.dependencies or build-system.requires, [tool.uv.workspace] members, the real Tier 1 flow online.
- A legitimately dynamic `project.dynamic` in a base pyproject halts every Tier 1 (false positive); on Python 3.10 every Tier 1 halts.
