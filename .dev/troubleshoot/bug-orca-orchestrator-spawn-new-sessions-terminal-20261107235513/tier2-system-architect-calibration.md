# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/tier2-system-architect-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T00:14:12Z
(Returned by confidence-calibrator; persisted by the parent. Notes condensed by the parent; scores, trace and rule rows as returned.)

Declared (bold-line header): `claim_class: mixed`, `evidence_class: source_static`, `verdict_direction: AFFIRM`.

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 0.5 | Every install-flow citation matched on Read (install_core.py:70-72, :94-105, :19; main.py:178, :365; core/CLAUDE.md:45-53; CLAUDE.md:308 and :320 in both the worktree and /home/coder/workspaces/IronClaude). The code shows the rule is not delivered, not the empty terminal; the step from "rule absent" to "orchestrator runs a bare create" is inferred. "No Python code outside install_core.py writes CLAUDE.md" is only partly verified. |
| Runtime check | 0.0 | `mixed` takes the minimum of its parts: the `static_defect` part inherits Evidence grounding (0.5); the `runtime_behavior` part with `source_static` is 0.0. "Runtime check performed?: no". |
| Symptom coverage | 0.5 | Explains why the rule is missing; not the empty plain terminal or the waiting orchestrator. |
| Reproducibility fit | 0.5 | Install skipping is deterministic but not run; the empty terminal not reproduced; LLM choice on an unknown host (`runs-in=unknown`). |
| Fix directness | 0.5 | Targets install_core.py but needs new marker-upsert logic, an edit to core/CLAUDE.md and a new test; does not make the LLM obey. |
| Domain coherence | 0.5 | Install-tool Python, instruction-text delivery and LLM obedience: two to three related domains. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.42 | (0.5+0.0+0.5+0.5+0.5+0.5)/6 = 0.4167 |
| gate_M1: evidence_grounding + 0.30 | 0.80 | |
| gate_M2: runtime_check + 0.30 | 0.30 | binding |
| gated_min | 0.30 | |
| verdict_cap | none | M3a is literal to `runtime_behavior`; this card is `mixed` (a 0.84 cap would not bind anyway) |
| **calibrated** | 0.30 | C3b and C7 caps (0.5) not binding |
| spot_check_unverifiable | none | |
| structural_flags | locus_unknown (C3b), uncited (C7) | both non-binding |

## Confidence

- **Self-reported (in card)**: 0.40 (not used as input)
- **Calibrated (this report)**: 0.30
- **Formula applied**: min(0.42, 0.80, 0.30) = 0.30.
- **Delta**: -0.10

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: § Escalation decision rule 3 (`confidence < 0.85`). `source_only_dynamic_claim` does not apply literally (class is `mixed`). 
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | headline states a mechanism, not an enum token |
| C2 | no | — | — | card excludes no producer as a cause |
| C3 | no | — | — | no control arm cited |
| C3b | yes | `locus_unknown` | Runtime check ≤ 0.5 (already 0.0) | card `runs-in=unknown`; execution-locus.md `RUN-SITE: pending-producers` |
| C4 | no | — | — | no tasklist-style measurement row or enabling task in the card; fix verification is a unit test |
| C5 | no | — | — | Timestamp 2026-11-08T00:12:39Z earlier than card_mtime 00:14:07Z + 5 min |
| C6 | no | — | — | no numeric threshold or bracket |
| C7 | yes | `uncited` | calibrated ≤ 0.5, not binding | card asserts host properties (stale installed ~/.claude/CLAUDE.md; pipx package built 2026-11-05 predates #415) citing O5 but no discriminator or 2x2 row (borderline; same outcome either way) |
| C8 | no | — | — | row 6 cited and present with Status `fetched:local-source`; no row covers the LLM-obedience half |

## Notes

- Verified: install_core.py:70-72, :94-105, :19; main.py:178 and :365; core/CLAUDE.md:45-53 and :28-30 (marker precedent); worktree and /home/coder/workspaces/IronClaude CLAUDE.md:308 and :320 (bare create, no `--agent`); the `~/.claude/CLAUDE.md` loaded in the calibrator's session has no "Orca session launches" block.
- Unverified: "No Python code outside install_core.py writes CLAUDE.md" (only the first 120 lines of install_user_setup.py read); the pipx package content; the "steered toward bare create" framing is stronger than the evidence (CLAUDE.md:307-310 only says how to create a worktree, it does not forbid `--agent`); the core rule applies to a "ccsession-backed Claude session" and excludes supervised `worker-start`.
- tier1-observation.md O4/O5 reports 3 `worktree create` calls with `--agent` and 9 without since 11-05 on a host where the rule was never delivered; the card does not mention it. It weakens "rule absent causes bare create" as a sufficient cause, not as a necessary one. Every supervised spawn from 06:15 on was `worker-start --agent claude`.
- **Cross-artifact disagreement (acted on by the parent)**: diagnosability-tasklist.md "Fix candidate (a)" said to run `superclaude install` so the #415 rule reaches ~/.claude/CLAUDE.md; `install_core.py:70-72` skips an existing CLAUDE.md on a plain install, so the paired grep would still return 0. The card is right, the tasklist wording was wrong.
