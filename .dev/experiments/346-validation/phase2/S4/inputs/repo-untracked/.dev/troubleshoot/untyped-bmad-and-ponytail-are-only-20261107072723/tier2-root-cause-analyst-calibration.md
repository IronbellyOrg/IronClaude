# Calibration Report

(Returned by confidence-calibrator; persisted by parent; scores and structural table verbatim, prose condensed.)

**Card under calibration**: /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/tier2-root-cause-analyst-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-07T07:44:11Z

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | 13 cited items read; every snippet matched (owner-decisions.md:5; .memlog.md:32-33; install_user_setup.py:384,322-327,426-431; ironclaude/install.sh:26-29,140-151; spec2-health.sh:76,88-97; installed_plugins.json:64-71). |
| Runtime check | 0.5 | `mixed` with `source_static`; nothing run. BMAD half doc_contract x source_static = 0.5; Ponytail half static code path inherits EG 1.0; minimum 0.5. Probes named but no captured output. C3b caps at 0.5. |
| Symptom coverage | 0.5 | BMAD first-use ask explained as an unruled per-project request; Ponytail gap as a silent unretried plugin failure; neither shown to be the reporter's cause. |
| Reproducibility fit | 0.5 | Deterministic requirement gap and code path; no reproducer or failing boot attempted; symptom not intermittent. |
| Fix directness | 0.5 | One README section: small and localised, but not the code the evidence identifies; delivers none of the three asks. |
| Domain coherence | 0.5 | Owner-decision and spec policy for BMAD plus plugin-install and health path for Ponytail. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.58 | 3.5 / 6 = 0.5833 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 0.80 | not binding |
| gated_min | 0.58 | |
| verdict_cap | none | M3a applies only to runtime_behavior |
| **calibrated** | 0.58 | no structural cap lowered it |
| structural_flags | locus_unknown | C3b; no numeric change |

## Confidence

- **Self-reported (in card)**: 0.55
- **Calibrated (this report)**: 0.58
- **Formula applied**: min(0.58, 1.30, 0.80) = 0.58
- **Delta**: +0.03

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence` (multi_domain also matches)
- **Rubric rule fired**: Escalation decision rule 3: confidence < 0.85.
- **Execution restriction**: none; Tier 2 card, rubric defines no higher tier.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | - | - | calibrated 0.58 not below 0.50; no definite enum token in headline |
| C2 | no | - | - | no enum excluded; tasklist shows no producer menu |
| C3 | no | - | - | no control arm cited; "Ponytail banner in a non-seed worktree" is labelled weak and UNVERIFIED |
| C3b | yes | `locus_unknown` | Runtime check <= 0.5 (already 0.5) | card line 11; execution-locus.md:4-5 |
| C4 | no | - | - | no instrumentation or enabling task proposed; falsification standard gives confirm/falsify outcomes; tasklist E-1 to E-3 preregistered (card does not cite the E-row IDs) |
| C5 | no | - | - | Timestamp 07:43:28Z not later than card_mtime 07:43:49Z + 5 min, not T00:00:00Z |
| C6 | no | - | - | no numeric threshold; bracket not triggered |
| C7 | no | - | - | no environment property asserted as fact; evaluated on card text only |
| C8 | no | - | - | rows 1 and 2 exist with non-empty Status; card states row 2's user-scope UNVERIFIED |

## Notes (condensed)

- Verified citations (13): owner-decisions.md:5; .memlog.md:32-33; gap-closure SPEC.md:141,174; bmad/install.sh:21-26,57-60; test-57:449-452; bmad/manifest.yaml:12-14; startup.sh:1184; install_user_setup.py:384,322-327,426-431; main.py:236; installed_plugins.json:64-71; ironclaude/install.sh:26-29,140-151; spec2-health.sh:76,88-97 (path templates/VSCode-AIDev02/image/scripts/lib/spec2-health.sh).
- Not spot-checked: the card's negative search results and absence claims (CHANGELOG.md:232, spec-specstory-removal/SPEC.md:79, 2026-10-26 brainstorm, micro-first-owner-questions-brief-2026-11-02.md, scout-create.md:32,37, "docs/ has no placement statement"); any could flip the REFUTE.
- Weak point in the REFUTE reasoning (not a citation failure): the card omits gap-closure SPEC.md:77 ("Any BMad change ... BMad stays a per-project seed install, exactly as #207 built it" is a non-goal); SPEC.md:174 concerns Orca worktrees via a tracked install or worktree-create hook, not first-use creation in an arbitrary project; SPEC.md:141 is an explicit non-goal ending "Users run the one-command path instead". "Unruled" is arguable; "documented release non-goal, not owner-forbidden" is the safer reading.
- Claim-class sensitivity: if the Ponytail half were reclassified runtime_behavior, Runtime check 0.0 and calibrated 0.30; ESCALATE either way.
- Possible split_pending: Tier 1 and this card read the same lines (owner-decisions.md:5; SPEC.md:141,174) differently (Tier 1: reversal of a documented decision; this card: unruled). No split_pending context was passed.
- The card's "0.65 cap" self-assessment is not a rubric rule and was ignored.
