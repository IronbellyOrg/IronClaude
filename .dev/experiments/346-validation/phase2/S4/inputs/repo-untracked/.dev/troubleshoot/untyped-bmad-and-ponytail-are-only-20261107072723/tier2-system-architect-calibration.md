# Calibration Report

(Returned by confidence-calibrator; persisted by parent; scores and structural table verbatim, prose condensed.)

**Card under calibration**: /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/tier2-system-architect-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-07T07:44:11Z

Declared: `claim_class: doc_contract`, `evidence_class: source_static`, `verdict_direction: AFFIRM`, `runs-in=unknown`.

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | Every file:line read matched (bmad-help/SKILL.md:25-26; install.sh:21-26,42; SPEC.md:141,174; ARCHITECTURE-SPINE.md:105,141,228). The card marks the one inferential step (`{project-root}` resolves to cwd) UNVERIFIED itself. |
| Runtime check | 0.5 | Cross-tab doc_contract x source_static = 0.5; runnable falsifier named but no captured output; C3b also caps at 0.5. |
| Symptom coverage | 0.5 | Explains the three BMAD asks; scopes out Ponytail, so one half of #478 is unexplained. |
| Reproducibility fit | 0.5 | Deterministic from code; no reproducer attempted; RUN-SITE/SAME-ENV unknown; E-1 to E-3 pending. |
| Fix directness | 0.5 | Design 2 names files and a test but spans specs, install.sh, manifest and tests; gated on an owner decision; rests on unverified mechanisms. |
| Domain coherence | 0.5 | Spec, installer shell and skill discovery plus tests: related BMAD-catalogue domains. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.58 | 3.5 / 6 = 0.583 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 0.80 | not binding |
| gated_min | 0.58 | |
| verdict_cap | none | M3a applies only to runtime_behavior |
| **calibrated** | 0.58 | no structural cap fired |
| structural_flags | locus_unknown | no numeric effect |

## Confidence

- **Self-reported (in card)**: 0.45
- **Calibrated (this report)**: 0.58
- **Formula applied**: min(0.583, 1.30, 0.80) = 0.58
- **Delta**: +0.13

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence` (multi_domain also holds)
- **Rubric rule fired**: Escalation decision rule 3: confidence < 0.85.
- **Execution restriction**: none; Tier 2 card, so ESCALATE means it cannot be the sole basis to stop or to recommend a fix.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | - | - | no enum token; producers header-only; calibrated 0.58 >= 0.50 |
| C2 | no | - | - | no enum excluded |
| C3 | no | - | - | no control arm cited |
| C3b | yes | `locus_unknown` | Runtime check <= 0.5 (already 0.5) | card line 11; execution-locus.md:4-5 |
| C4 | no | - | - | no measurement row or enabling task added by the card |
| C5 | no | - | - | Timestamp 07:43:28Z earlier than card_mtime 07:44:06Z, not T00:00:00Z |
| C6 | no | - | - | no numeric threshold; bracket not triggered |
| C7 | no | - | - | asserted environment properties cited to rows 2 and 3; two uncited properties marked UNVERIFIED |
| C8 | no | - | - | rows 2 and 3 exist with non-empty Status (behaviour-definitions.md:6-7) |

## Notes (condensed)

- Spot-checks matched: bmad-help/SKILL.md:25-26; bmad/install.sh:21-26,42; bmad/manifest.yaml:8-20; SPEC.md:141,174; owner-decisions.md:5; ARCHITECTURE-SPINE.md:105,128-129,141,228; test-57:446-452; test-startup-boot.sh:2209-2224. Not read: test-19/test-46 grep-only claims.
- Understated conflict: gap-closure SPEC.md:77 (non-goal "Any BMad change ... stays a per-project seed install") and .memlog.md:32-33 ("never globally or at user level"; slug keeps #207 per-project seed behaviour unchanged) bear on Design 2's user-level shim; the card's files-to-change list omits them, so the owner question is closer to already answered than the card suggests. No further score reduction (card gates on the owner).
- Claim-class sensitivity: if reclassified mixed/runtime_behavior, Runtime check 0.0 and calibrated 0.30; still ESCALATE.
- Row 3 was bound after card receipt; the card's E5 cited it beforehand; row now present with populated Status (C8 passes on current state); row 3 notes shell execution by a user-level skill is UNVERIFIED and the page was read only to character 100000 of 118986.
- All optional inputs supplied; nothing skipped.
