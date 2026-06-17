# UC-1 PRE-Execution Coverage Audit — sc-bare-review M8/M9 Migration

**Mode:** pre · **Tier:** 1 (single-agent grounded pass) · **Date:** 2026-06-16
**Artifact under audit:** TASK-RF-bare-review-migration-20260616-045915.md
**Driving spec + evidence:** Migration §16 steps 8+9 (merged-requirements.compressed.md:688-703); mms-phase-8-postaudit/REPORT.md; mms-phase-9-postaudit/REPORT.md; phase-9-tasklist.md
**Stance:** Adversarial — hunting coverage gaps.

## 0. Grounding (re-verified this turn)
- SKILL.md = 231 lines (wc -l) — matches P8/P9 "not thin". OK
- 3 legacy scripts present (t2_dispatch.sh, t2_normalize.py, t2_preflight.sh) — matches P8 T08.07. OK
- phase-8-cp1/cp2 exist (false attest) — matches P8 §3. OK
- No phase-9-cp*.md — matches P9 T09.04/T09.08 UNBUILT. OK
Premise is grounded; no fabricated premise.

## 1. Obligation enumeration (22 total)
Source A §16 steps 8+9: O1 thin caller execs CLI relays contract (:701); O2 A/B parity vs today's output (:701); O3 scripts/*.sh deleted (:702); O4 production migration skill->CLI (:702).
Source B P8 REPORT: O5 T08.01 real thin caller <=80; O6 T08.07 retire scripts; O7 T08.11 parity drives CLI + survives deletion; O8 T08.17 integration suite; O9 T08.08 release-notes reconcile; O10 cp1/cp2 superseded.
Source C P9 REPORT + phase-9-tasklist: O11 OPS-001 operator-runbook; O12 OPS-002a env-readiness.md; O13 OPS-002b swarm_env_readiness.sh; O14 OPS-003 observability-procedure; O15 OPS-004a rollback-procedure; O16 OPS-004b tabletop sign-off (STRICT); O17 OPS-005 lens-contribution-policy; O18 OPS-006 post-release-metrics; O19 phase-9-cp1 + cp2 checkpoints.
Cross-cutting: O20 deletion AFTER passing parity gate; O21 golden captured BEFORE deletion; O22 on-disk verification + POST reflect anti-bias gate.

## 2. Coverage map
O1 -> Step 3.1/3.3 COVERED; O2 -> 4.1-4.5 COVERED; O3 -> 5.3/5.4/5.5 COVERED; O4 -> Phase2 WS-0 + 3.1 COVERED; O5 -> 3.1-3.3 COVERED; O6 -> 5.3-5.5/5.8/5.10 COVERED; O7 -> 4.3 + 5.11 COVERED; O8 -> NONE UNMAPPED; O9 -> 3.4 COVERED; O10 -> 7.1/7.2 COVERED; O11 -> 6.1; O12 -> 6.2; O13 -> 6.3; O14 -> 6.4; O15 -> 6.5; O16 -> 6.6 (PENDING HALT); O17 -> 6.7; O18 -> 6.8 (all COVERED); O19 -> NONE UNMAPPED; O20 -> 5.1 + Key Constraints COVERED; O21 -> 4.1/4.2 COVERED; O22 -> 3.3/5.10/PC.1/PC.5 COVERED.

## 3. Coverage
COVERED 20/22; UNMAPPED 2 (O8, O19); PARTIAL 0. coverage_pct = 0.909.

## 4. Gaps
GAP-1 (O8) T08.17 integration suite: neither authored nor formally waived. MINOR/WAIVABLE — P8 §5 says "author OR formally waive"; not a §16 cutover step. Recorded as silent omission.
GAP-2 (O19) phase-9-cp1/cp2 checkpoints: not authored, not explicitly superseded. MINOR/WAIVABLE — Tier:EXEMPT bookkeeping superseded by this tasklist's Phase Gate 6 + PC.1 + PC.5. Recorded.

## 5. Best-practice check — ALL PASS, no violations
- Deletion AFTER passing parity gate: PASS (Phase 5 L5-gated; Step 5.1 gate-check; WS-0->A->B->GREEN->C strict).
- Golden BEFORE deletion: PASS (Step 4.1 "WHILE SCRIPT STILL EXISTS"; 4.2 verify).
- Disk-verification vs false attestation: PASS (3.3, 5.10 I17; PC.1 PRESENT/ABSENT every deliverable; PC.2 vs baseline).
- POST reflect anti-bias gate: PASS (PC.5 independent wrapper, last gate, exit-code consumed, exit-11 caveat handled).
- Parity survives legacy deletion: PASS (4.3c removes skipif(LEGACY_SCRIPT.exists()); 5.11 re-runs after deletion).
- HALT discipline: PASS (6.6 needs_human_decision PENDING, never auto-stamp; PG6.5 forbids auto-stamp during fixes).
- Baseline to separate pre-existing red: PASS (1.3 baseline; STRICT gate not make lint).
- Sync / no .claude/ staging: PASS (3.2/5.9 sync-dev+verify-sync; no git add .claude).

## 6. Scope-creep / invented-obligation check
WS-0 (inline path wiring + 4 flags) is NOT creep: it is the enabling precondition for O1/O4. Inline run_cmd is the T03.01 stub (dispatch only, no normalize/reduce/emit_contract); a thin caller would emit NO return-contract.yaml without it. Correctly sequenced as BLOCKING prerequisite. 4 flags restore legacy t2_preflight.sh surface (behavior-preserving). No invented obligations; every item traces to spec/REPORT/phase-9-tasklist/build-request/research.

## 7. Verdict
coverage_pct 0.909 >= 0.90; all best-practice invariants pass; WS-0 justified; no creep. status success. Two minor waivable omissions recorded (recommend closing to reach 1.0): (1) add minimal tests/swarm/integration smoke OR explicit waiver citing P8 §5; (2) note phase-9 cp1/cp2 intentionally superseded by Phase Gate 6 + PC.1 + PC.5.

## RETURN CONTRACT
status: success
coverage_pct: 0.909
unmapped_requirements: ["O8: T08.17 tests/swarm/integration/ suite — neither authored nor formally waived", "O19: phase-9-cp1.md + phase-9-cp2.md checkpoints — not authored, not explicitly superseded"]
verdict: pass
run_id: pre-grounded-bare-rev-m8m9
