# Calibration Report

(Returned by confidence-calibrator; persisted by parent; scores and structural table verbatim, prose condensed.)

**Card under calibration**: /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/tier2-devops-architect-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-07T07:44:11Z

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | About 15 cited ranges read; every one matched; the cited code supports the sticky `.configured` marker claim. Contract-tests grep not re-run (no Grep tool in the calibrator role). |
| Runtime check | 0.0 | `mixed` with `source_static`: min(static_defect inherits EG 1.0, runtime/environment 0.0) = 0.0; card says "Runtime check performed?: no"; no literal runnable command, so the 0.5 override does not apply. C3b also caps at 0.5 (not binding). |
| Symptom coverage | 0.5 | Ponytail half conditionally explained (sticky install failure on Default, or Minimal profile); BMAD half left as owner decision; "BMAD should self-create directories" unaddressed. Link to the reporter's symptom UNVERIFIED. |
| Reproducibility fit | 0.0 | Trigger is a network/time-budget shortfall in an unknown environment (SAME-ENV unknown); never observed; no reproducer attempted. |
| Fix directness | 0.5 | Exact fix (`configured()` predicate in catalogue/ironclaude/install.sh) but not shown to cause the symptom; test file not located; no BMAD fix. |
| Domain coherence | 0.5 | Boot-time install idempotency plus a separate owner-policy domain (BMAD); also timing/offline risks. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.42 | (1.0+0.0+0.5+0.0+0.5+0.5)/6 = 0.4167 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 0.30 | binds |
| gated_min | 0.30 | min(0.42, 1.30, 0.30) |
| verdict_cap | none | M3a applies only to runtime_behavior |
| **calibrated** | 0.30 | C7 cap (0.5) non-binding |
| structural_flags | locus_unknown, uncited | C3b and C7 non-binding numerically |

## Confidence

- **Self-reported (in card)**: 0.55
- **Calibrated (this report)**: 0.30
- **Formula applied**: min(0.42, 1.30, 0.30) = 0.30
- **Delta**: -0.25

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence` (also multi_domain, not_reproducible)
- **Rubric rule fired**: Escalation decision rule 3: confidence < 0.85.
- **Execution restriction**: none; already Tier 2.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | - | - | no definite enum token in headline; producers.md `producer-count: n/a`; tasklist total-rows=0 |
| C2 | no | - | - | no enum excluded |
| C3 | no | - | - | no control arm cited |
| C3b | yes | `locus_unknown` | Runtime check <= 0.5 (already 0.0) | card line 11; execution-locus.md:4-5 |
| C4 | no | - | - | card proposes a code fix, not a measurement row; falsification standard maps outcomes; tasklist E-3 carries both values |
| C5 | no | - | - | Timestamp 07:43:28Z earlier than card_mtime 07:44:05Z, not T00:00:00Z |
| C6 | no | - | - | no numeric threshold; bracket not triggered; bracket.md absent |
| C7 | yes | `uncited` | calibrated <= 0.5 cap, non-binding at 0.30 | card names environment properties (offline boots, Orca config directory, Minimal profile) with no 2x2 row cited (calibrator evaluated on card text; the ref does not define "2x2 row") |
| C8 | no | - | - | behaviour-definition row 1 exists with non-empty Status |

## Notes (condensed)

- Spot-checks matched: install_user_setup.py:44,309,398-399,426-430,436-444,40; main.py:269-280; ironclaude/install.sh:26-29,32-35,95-97,122-125,140-141,143-149; ironclaude/manifest.yaml:24-25; startup.sh:917-918,1092,1180-1181; test-startup-boot.sh:2105,2136,2209,2223; Dockerfile.coder:139; bmad/install.sh:21-53; profiles.yaml:19-21; user_settings_defaults.json:36. No citation failed to verify.
- Mechanism supported: `install_plugins` installs only entries missing at user scope (install_user_setup.py:383-387); a plain rerun without `--force` retries only what is missing.
- Not independently verified: the card's contract-tests grep; how `setup_success` is derived in main.py (exit-0 claim rests on `install_user_setup` returning all(ok) with ok=True for the plugin shortfall); whether an ironclaude contract test exists.
- Card completeness observation: a marketplace "registered from another source" is recorded as failed (install_user_setup.py:355-359, 370-372) and would be retried every boot under the proposed predicate.
- Sensitivity: if Runtime check and Reproducibility were both 0.5, calibrated would be 0.50; ESCALATE under every defensible scoring.
- All optional inputs supplied except bracket.md (absent; C6 evaluated against the headline and the tasklist).
