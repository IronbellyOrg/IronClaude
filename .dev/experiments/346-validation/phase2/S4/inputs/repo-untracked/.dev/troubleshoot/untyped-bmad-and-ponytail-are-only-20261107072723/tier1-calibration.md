# Calibration Report

(Returned by confidence-calibrator; persisted by parent. Structural table and scores verbatim; prose condensed.)

**Card under calibration**: /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-07T07:38:05Z

## Per-dimension scores

Declared on the card: `claim_class: mixed`, `evidence_class: source_static`, `verdict_direction: AFFIRM`.

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | 13 cited ranges read; each matched (E1 bmad/install.sh:21-26,40-42,57-60; E2 owner-decisions.md:5; E3 install_user_setup.py:384, installed_plugins.json:64-70; E4 profiles.yaml:18,21). |
| Runtime check | 0.5 | `mixed` takes the lower half: BMAD half doc_contract x source_static = 0.5; Ponytail half config_value x source_static inherits EG = 1.0. Card states no runtime check. C3b also caps at 0.5. |
| Symptom coverage | 0.5 | BMAD asks explained by the 2026-09-25 owner decision; Ponytail shown user-global under Default, but why the reporter lacked it is unexplained (two unverified scenarios). |
| Reproducibility fit | 0.5 | BMAD deterministic code path with named tests, nothing run; Ponytail depends on unknown profile and boot outcome. |
| Fix directness | 0.5 | Fix is a README paragraph plus an owner decision; it does not deliver what the reporter asked. C4 also caps at 0.5. |
| Domain coherence | 0.5 | Two related domains (owner-decision policy for BMAD; profile gating plus plugin install for Ponytail); the card's self-score 1.0 not supported. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.58 | (1.0+0.5+0.5+0.5+0.5+0.5)/6 = 0.583 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 0.80 | not binding |
| gated_min | 0.58 | mean is the minimum |
| verdict_cap | none | M3a applies only to claim_class runtime_behavior |
| **calibrated** | 0.58 | no structural cap lowers it |
| structural_flags | locus_unknown, no_prereg_falsifier | both non-binding |

## Confidence

- **Self-reported (in card)**: 0.60
- **Calibrated (this report)**: 0.58
- **Formula applied**: min(mean(all_six), EG+0.30, RC+0.30) = min(0.58, 1.30, 0.80) = 0.58
- **Delta**: -0.02

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: Escalation decision rule 3 (signal-driven): confidence < 0.85 -> ESCALATE. Domain coherence 0.5 would also trigger `multi_domain`, listed after `low_confidence`.
- **Execution restriction**: none (`--no-escalate` false, depth standard).

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | - | - | no enum token in headline; calibrated 0.58 not below 0.50 |
| C2 | no | - | - | no enum excluded |
| C3 | no | - | - | no control arm cited |
| C3b | yes | `locus_unknown` | Runtime check <= 0.5 (already 0.5, non-binding) | tier1-hypothesis.md:11; execution-locus.md:4 |
| C4 | yes | `no_prereg_falsifier` | Fix directness <= 0.5 (already 0.5, non-binding) | diagnosability-tasklist.md:17-18 (E-2, E-3 lack full outcome mapping); E-1 has one; Task 1 links rows with verification and rollback |
| C5 | no | - | - | timestamp 07:37:35Z earlier than card_mtime 07:38:02Z, not T00:00:00Z |
| C6 | no | - | - | no numeric threshold asserted; bracket not triggered |
| C7 | no | - | - | environment statements tied to cited lines; tasklist has zero discriminator rows so no 2x2 row exists to cite (judgement call: if read strictly, C7 caps at 0.50, still ESCALATE) |
| C8 | no | - | - | behaviour-definitions rows 1 and 2 exist with non-empty Status; card cites both |

## Notes (condensed)

- Spot-checks all matched (bmad install.sh, manifest.yaml, install.js options, owner-decisions.md:5, gap-closure .memlog.md:27/32, main.py:236, install_user_setup.py:384/392-410/426-430/437-443, user_settings_defaults.json:36/52-70, installed_plugins.json:64-70, profiles.yaml:18/21, startup.sh:1158-1169, ironclaude/install.sh:88-90/143-146, test-57:450/452).
- Caveat: install.js:14-37 does not cover the whole options list (`--channel` begins at line 39); "no user-scope option" holds for the cited range only; behaviour-definitions row 2 already marks user-scope capability UNVERIFIED.
- "30 s budget" (install_user_setup.py:40) and the outer `timeout 60` (ironclaude/install.sh:122) are consistent.
- If the parent treated E4's "not retried" and the "if I'm wrong" scenario as asserted runtime claims, Runtime check would be 0.0 and calibrated 0.30; outcome unchanged (ESCALATE).
- Inputs: none absent; bracket.md not read (no threshold asserted).
