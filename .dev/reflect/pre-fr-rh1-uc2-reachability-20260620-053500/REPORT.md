# Reflect PRE Report — FR-RH1 UC-2 Reachability Gate tasklist

**Mode:** pre (UC-1 coverage/gap audit)
**Depth:** deep → **Tier 2 (forced)**
**Status:** success
**Calibrated confidence:** 0.90
**Spec:** `.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md` (patched FR-RH1, obligations R1-R9)
**Tasklist under audit:** `.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/TASK-RF-uc2-reachability-gate-20260620-043410.md`
**Run id:** `pre-fr-rh1-uc2-reachability-20260620-053500`

## Verdict

**Coverage 1.0 — all 9 obligations (R1-R9) have both an implementing and a verifying item.** No unmapped requirements, no spec-violating items, no Regression, `needs_human_decision: false`. The tasklist is coverage-complete against the patched spec and is approved to execute.

The Tier-2 heterogeneous ensemble (analyzer/sonnet, qa/haiku, refactorer/opus — full model-class + vendor diversity) converged on the facts and surfaced four **verification-rigor** improvements that are advisory, not blocking.

## Coverage matrix (R1-R9)

| Obligation | Covered | Implement | Verify | Notes |
|---|---|---|---|---|
| R1 real-boot-only Regression | ✅ | Phase 2 patch, Phase 3 Step 5.6 + taxonomy | Phase 5 proxy/static-can't-prove-Regression fixture | Positive real-boot case conditional (H4) |
| R2 telemetry-only `--no-reachability` | ✅ | Phase 3 SKILL.md + Phase 4 wrapper | Phase 5 skip fixture + test | strong |
| R3 telemetry-only spec-and-tasklist-absent | ✅ | Phase 3 SKILL.md | Phase 5 missing-inputs fixture + test | strong |
| R4 contract 1.6.0 (1.5.0 D13-only) | ✅ | Phase 3 contract item + report-template | Phase 5 1.6.0 fixture + test | additive-minor not mechanically diffed (H2) |
| R5 wrapper plumbing (5 sub-parts) | ✅ | Phase 4 ×5 (config/Click/tmux/_build_prompt/docs) | Phase 5 help/prompt/docs-parity tests | strongest obligation |
| R6 producer eval fixture | ✅ | Phase 5 producer eval cases | grader assertions | distinct from consumer fixtures |
| R7 7 fields + consistency | ✅ | Phase 3 contract item | Phase 5 field-tolerance test | consistency invariants not unit-pinned (H1) |
| R8 bounded cost | ✅ | Phase 3 cost/ops item | Phase 2 stale-string search + Phase 6 semantic lens | prose/search not executable (H3) |
| R9 advisory-only semantic fallback | ✅ | Phase 3 SKILL.md | Phase 5 semantic-fallback-non-routing test | strong |

## Ensemble divergence (what Tier 2 caught)

Three reviewers, three coverage numbers: analyzer 1.00, refactorer 0.92, qa 0.42 (weighted). Calibration resolved the divergence: qa re-scoped "coverage" to *executable-test presence* rather than the protocol's obligation→item definition (§12.1 dim 2). On the protocol's metric all three agree every obligation is addressed → `coverage_pct: 1.0`. Their **convergent** signal is the precise set of obligations whose verification rests on prose/search/eyeball rather than an executable assertion.

## Recommended hardening (advisory — fold into Open Questions, do not block)

- **H1 (R7, medium):** add `test_reachability_consistency_invariants()` pinning the 5 when-then rules (gate_ran⟹skip null + ledger non-null + scanned≥1; unreachable>0 ⟹ real_boot_ran + regression_present + verification_regressions_detected≥unreachable; unproven>0 ⟹ grounding_gaps non-null + needs_human_decision).
- **H2 (R4/R7, medium):** add a field-diff assertion proving the 1.5.0 field set is a strict subset of 1.6.0 (no rename/remove/retype).
- **H3 (R8, low):** add a grader/Testability-Map row asserting the bounded-cost fields present and zero-cost claims absent.
- **H4 (R1, low):** keep the positive real-boot-proven Regression case as an eval-hardening follow-up (spec R6 permits deferral); ensure the negative falsifier is active.

## Evidence-validator

14 citations, 14 re-Read, 0 dropped. The convergent gap claims (no dedicated test for R7 consistency invariants; no additive-minor field-diff) were independently re-verified against Phase 5 of the tasklist on disk — confirmed.

## Notes

`--remediate` not passed, so no Tier-3 corrective tasklist is authored. The four hardening recommendations are surfaced for the operator and appended additively to the tasklist's Open Questions; none blocks execution.
