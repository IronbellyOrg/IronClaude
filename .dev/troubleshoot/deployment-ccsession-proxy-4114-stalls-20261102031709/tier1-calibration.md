# Calibration Report

**Card under calibration**: /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-02T03:28:40Z
**Source**: confidence-calibrator agent (persisted by the parent on receipt)

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Re-read every key citation; all matched: ccsession:801-804, ccsession:1432-1440 (`exec "$CLAUDE_BIN"` at 1438), local-gateway-alias-proxy.py:857-872 (bind then bare `serve_forever()`, no fork/setsid), daemon.log:680-681 and 750-751 (`session-killed` at 00:01:42.345Z and 22:59:18.584Z), ccsession:762-763, README.md:415-418, test_ccsession_tiers.py:1379 with `pkill -f` cleanup at 1416-1418. Secondary cites (py:687, py:834, ccsession:722, ccsession:351) match. E2/E4 values match tier1-observation.md O1-O4 and O10. |
| Runtime check | 1.0 | Cross-tab (`runtime_behavior`, `runtime_repro`) = 1.0. O10 executed reproducer with captured output in live-check/before.txt. Caveat: the sweep in O10 is a stand-in for Orca's, disclosed in Grounding Gaps. |
| Symptom coverage | 1.0 | One mechanism covers both strings, both incidents to the minute, the 03:08 recovery and why 4013 stays healthy; alternatives each ruled out with a cite. |
| Reproducibility fit | 0.5 | Mechanism deterministic and reproduced, but the reproducer enacts behaviour row 1 with a stand-in sweep; field attribution of the dead 4114 shims is inferred by elimination from daemon.log; exception-driven death cannot be excluded from field evidence (stderr -> /dev/null). |
| Fix directness | 1.0 | Two files, one change each, at the launch site and in `__main__`; argv unchanged so `pgrep -f` (ccsession:722) works; new test tied to O10. C4 did not fire. |
| Domain coherence | 1.0 | Single domain: process lifecycle and ancestry. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.92 | (1.0+1.0+1.0+0.5+1.0+1.0)/6 = 0.9167 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 1.30 | does not bind |
| gated_min | 0.92 | the mean is the minimum |
| verdict_cap | none | runtime_check = 1.0, so the 0.84 AFFIRM cap does not apply |
| **calibrated** | 0.92 | no structural caps fired |
| spot_check_unverifiable | none | no remote URLs cited |
| structural_flags | none | C1-C8 evaluated: none fired, none skipped |

## Confidence

- **Self-reported (in card)**: 0.85 (read, not used as input)
- **Calibrated (this report)**: 0.92
- **Formula applied**: `min(mean=0.92, EG+0.30=1.30, RC+0.30=1.30)` = 0.92; no verdict-direction cap; no structural cap.
- **Delta**: +0.07 (the card under-reported relative to its own dimension table).

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 4, Default: "confidence ≥ 0.85 AND single-domain AND reproducible → STOP at Tier 1." Rules 1-3 checked: no --no-escalate/--depth quick; depth standard; confidence 0.92; domain coherence 1.0; reproducibility 0.5 (not 0.0); not intermittent (event-triggered, reproduced); type deployment (not security); runtime_check 1.0 so source_only_dynamic_claim does not apply; split_pending n/a.
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | Calibrated 0.92 ≥ 0.50; headline names no enum token. |
| C2 | no | — | — | No enum exclusion declared; mechanism alternatives carry source cites (py:687, 834, 852-854, 857-870). |
| C3 | no | — | — | execution-locus.md:13 `CONTROL-PROOF: yes: ccsession:804` for the 4013 control arm; ccsession:804 confirmed as the launch statement. |
| C3b | no | — | — | runs-in line and execution-locus.md:4-5 give a known locus (SAME-ENV: yes). |
| C4 | no | — | — | diagnosability-tasklist.md:12-13 total-rows=0, "No discriminator required"; Task 1 is an optional env-override with Verification and Rollback. |
| C5 | no | — | — | Card Timestamp 03:28:01Z not later than card_mtime 03:28:39Z + 5 min; not T00:00:00Z. |
| C6 | no | — | — | No numeric threshold or bracket in the headline. |
| C7 | no | — | — | Environment properties cite behaviour-definition rows 1-2 and O2/O4; no 2x2 rows exist to cite. |
| C8 | no | — | — | behaviour-definitions.md rows 1 and 2 have non-empty Status. |

## Notes

- Spot-check: all cites verified; ccsession:351 is the "python3 takes it (macOS has no flock command)" comment, supporting the python-instead-of-setsid precedent.
- Dominant weakness: ownership of the dead field shims is inferred by elimination; the reproducer proves a descendant sweep kills a shim inside the terminal tree, not that Orca did so to the 4114 shims. Whether `terminateOwnedTree` also signals the process group is not established; setsid covers both cases.
- C4 sensitivity: if Task 1 were treated as an enabling task needing linked measurement IDs, C4 would cap Fix directness at 0.5 (mean 0.83, ESCALATE low_confidence). Not fired: total-rows=0 leaves nothing to link and Task 1 has operational verification/rollback.
- Fix-design assertions not verified by the calibrator (implementer/test responsibility): macOS safety of the double fork, "no threads before serve_forever", no-subreaper inference from 4013's ppid=1.
- No defaulted or absent inputs.
