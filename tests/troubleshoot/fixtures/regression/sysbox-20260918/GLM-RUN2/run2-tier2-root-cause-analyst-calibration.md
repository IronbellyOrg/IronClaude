# Calibration Report

**Card under calibration**: /config/workspace/Coder/.claude/worktrees/sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/run2-tier2-root-cause-analyst-hypothesis.md
**Rubric**: /config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-09-19T00:00:00Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 0.5 | Dense `file:line` cites (startup.sh:569/:656-668/:719/:734, test-startup-boot.sh:1941-1947/:1960-1968, dotfiles.tf:154-160) but calibrator was scoped to card+rubric only, so no snippet was spot-check verified; the load-bearing 13.9s duration is explicitly "inherited evidence ... not independently re-read". |
| Runtime check | 0.5 | Frontmatter absent → claim_class defaults `runtime_behavior`, evidence_class `none`. Card contains a runnable discriminating command (`ws_ssh 'cat ~/.aidev/status/seed-repo-outcome; grep ^section.8 ...'`) with no captured output; no executed reproducer, `clone-failed` is deduced, never observed. |
| Symptom coverage | 0.5 | Explains the seed FAIL and the rerun FAIL as collateral (ordering :1962 before :1968), but the actual cause of the fast clone failure under sysbox is declared "unobservable from repo"; enum is inferred by elimination. |
| Reproducibility fit | 0.0 | Symptom is environment-dependent (sysbox-runc arm in CI only; DinD and sysx-blank pass); no reproducer executed. |
| Fix directness | 0.5 | Proposed change is a read-only diagnostic projection in the test harness, not a fix of the failing behavior; right area, but it defers the real fix to a later run and carries stated base-drift risk (6ced457). |
| Domain coherence | 0.5 | Two related domains: test-harness assertion logic + startup.sh §8 outcome logic, with host-side networking as the unnamed underlying cause. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.42 | 2.5 / 6 |
| gate_M1: evidence_grounding + 0.30 | 0.80 | |
| gate_M2: runtime_check + 0.30 | 0.80 | |
| gated_min | 0.42 | mean is binding |
| verdict_cap | 0.84 | AFFIRM, runtime_behavior, runtime_check < 1.0 — not binding |
| **calibrated** | 0.42 | |
| spot_check_unverifiable | none (no URLs) | all cites are local paths, unverified by scope restriction |

## Confidence

- **Self-reported (in card)**: 0.87 — read, not used
- **Calibrated (this report)**: 0.42
- **Formula applied**: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)`, AFFIRM cap 0.84 not binding
- **Delta**: -0.45. The card's confidence rests on source-logic elimination plus one inherited timing datum; nothing in the enum deduction has been observed at runtime, and the "fix" is instrumentation, not a fix.

## Escalation recommendation

**Verdict**: ESCALATE
**Reason**: `forced_by_depth_deep`
**Rubric rule fired**: "`--depth deep` set → ESCALATE (set `escalation_reason: forced_by_depth_deep`)". Also independently triggered: `confidence < 0.85` (low_confidence) and Reproducibility 0.0 (not_reproducible).

## Notes

- Card has no frontmatter: `claim_class`, `evidence_class`, `verdict_direction` all defaulted (runtime_behavior / none / AFFIRM). Claim text ("fast-failing git clone", "the orchestrator never re-ran") is dynamic control flow, so the runtime_behavior default is also the correct classification.
- Task brief said "5 rubric dimensions"; rubric defines six — all six scored per rubric.
- Spot-check of cited lines was not performed because the read scope was restricted to the card and rubric; Evidence grounding capped at 0.5 accordingly. Wave 5 evidence-validator should verify startup.sh:656-668, :719, :734 and test-startup-boot.sh:1960-1968 specifically, plus re-read Job 105657435166 startup-run.json for the 13.9s figure.
- The proposed fix would produce the missing runtime evidence (named enum); the next sysx run's `seed-repo-outcome` value is the single datum that would move Runtime check to 1.0.
