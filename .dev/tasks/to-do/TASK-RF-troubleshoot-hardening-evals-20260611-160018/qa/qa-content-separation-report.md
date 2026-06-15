# QA Report — Content Separation Invariant (backtest_status vs run-level verdict)

**Topic:** backtest_status separation invariant — production signoff stays advisory until complete
**Date:** 2026-06-12
**Phase:** task-qualitative (adversarial content-separation audit)
**Fix authorization:** false (report-only; no source modified)

---

## Overall Verdict: PASS

All 5 verification requirements hold. Adversarial mutation reasoning confirms the assertions
are non-tautological. The harness test is a faithful analogue of the spec-named governing test.
23/23 backtest tests pass.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | backtest_status SEPARATE from run-level verdict; signoff advisory unless complete | PASS | `catch_rate.py:191-193` — `production_signoff` returns `run_level_verdict` ONLY when `backtest_status == STATUS_COMPLETE`, else `"advisory"`. Matches spec §5.4 truth table (RELEASE-SPEC:417-421). |
| 2 | Signoff stays advisory at not_run/partial even when verdict would pass | PASS | Test `test_..._keeps_signoff_advisory_until_complete:38` asserts `production_signoff("pass")=="advisory"` at not_run; `test_..._partial_exposes_missing_escape_ids:53` asserts same at partial. Both feed `_RUN_LEVEL_PASS="pass"`. |
| 3 | partial surfaces the missing escape ids | PASS | `test_..._partial:51-52` asserts `backtest_status=="partial"` and `"E1" in missing_escape_ids()`. Backed by `catch_rate.py:117-119,179-181`. |
| 4 | Only complete permits signoff to mirror run-level verdict | PASS | `test_..._complete:68` asserts mirror=="pass" at complete; `:70` asserts `production_signoff("blocked")=="blocked"` — proves the mirror returns the ACTUAL verdict (one-directional gating), not a hardcoded "pass". |
| 5 | Assertions exercise the invariant (non-tautological); faithful analogue of spec test name | PASS | Mutation reasoning (below) shows each assertion catches a plausible broken impl. Docstring `:6-7` cites spec name `test_backtest_status_keeps_pipeline_health_advisory_until_complete`; spec §8.2 RELEASE-SPEC:568 confirms it. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Confidence: Verified 5/5 | Unverifiable 0 | Unchecked 0 | Confidence 100%
- Tool engagement: Read 4 | Grep/Bash 5 | pytest runs 2 (3-test + 23-test suites, all green)

## Adversarial Mutation Analysis (proof of non-tautology)

The adversarial mandate was to assume the invariant is wrong/untested in ≥3 places. I probed
4 distinct attack surfaces; each is genuinely covered:

- **Attack A — "signoff hardcoded to verdict (no gating)":** If `production_signoff` returned
  `run_level_verdict` unconditionally, line 38 (`=="advisory"` at not_run) and line 53
  (at partial) would FAIL. Covered. NOT tautological.
- **Attack B — "mirror hardcoded to 'pass' at complete":** This is the subtlest. If the impl
  did `if complete: return "pass"` (a plausible shortcut), line 68 (`=="pass"`) would still
  pass — a tautology trap. But line 70 asserts `production_signoff("blocked")=="blocked"`,
  which a hardcoded-"pass" impl FAILS. The test author closed this trap explicitly
  (`test_...:69-70` comment: "separation is one-directional gating only"). This is the
  strongest assertion in the suite.
- **Attack C — "partial-vs-pass confusion (missing-ids only proven via MISS)":** The
  separation test's partial case (`:43`) flips only ONE conjunct (`verdict=MISS, card=None`),
  so on its own it under-proves the 3-conjunct anti-vacuity rule. HOWEVER the companion suite
  `test_catch_rate_schema.py` independently covers each conjunct: all-CATCH+missing-witness→partial
  (`:200-213`), all-CATCH+null-card→partial (`:216-230`), and complete-claim+null-card→raises
  (`:233-251`). Separation coverage is therefore complete across both files; no gap.
- **Attack D — "competing/duplicate signoff model":** `grep` surfaced a second module
  `catch_rate_report.py` referencing signoff terms. Read confirms it is a pure RENDERER that
  IMPORTS `CatchRateReport` from `catch_rate.py` (`:17-20`); it defines no competing
  `production_signoff`. Single source of truth intact.

## Spec-Fidelity Cross-Check
- Spec §5.4 truth table (RELEASE-SPEC:417-421) reproduced EXACTLY by the model: not_run→advisory
  even if verdict=pass; partial→advisory + missing ids; complete→may mirror. ✓
- Spec §5.5 schema (RELEASE-SPEC:433): `backtest_status` enum `{not_run,partial,complete}`,
  default not_run, non-null, "Missing ⇒ treat signoff as advisory" — matched by
  `catch_rate.py:29-37` + the schema fixture tests. ✓
- Anti-vacuity tightening (CATCH+witness+card, beyond the spec's bare "all 5 pass") is grounded,
  not invented: `research/07-mdtm-template-and-report-model.md:137` defines complete as
  "all 5 replayed AND all verdict==CATCH AND all have negative_witness AND a cited card_path",
  and spec H1 (RELEASE-SPEC:139-140) requires a negative witness per contract. ✓

## Test-Name Analogue Faithfulness (VERIFY-5)
- Governing spec test: `test_backtest_status_keeps_pipeline_health_advisory_until_complete`
  (RELEASE-SPEC:568, §8.2).
- Harness test: `test_backtest_status_keeps_signoff_advisory_until_complete`
  (`test_backtest_status_separation.py:27`).
- "signoff" (harness) and "pipeline_health" (spec) name the SAME concept — spec §5.4's column
  header is literally "Production-Facing Pipeline-Health Signoff". The docstring `:6-7` cites the
  spec name verbatim. Faithful analogue, not a drifted rename.

## Issues Found
None. No CRITICAL, IMPORTANT, or MINOR issues.

## Self-Audit
**(a) Reliance list — items relied upon without independent re-derivation:**
- None. This was a standalone content audit (no inherited structural verdict in prompt); every
  claim was independently verified.

**(b) Independent semantic checks (≥1 required):**
- Re-read `production_signoff` impl (`catch_rate.py:191-193`) and traced its sole gate condition
  (`== STATUS_COMPLETE`) against spec §5.4 — verified by Read.
- Ran both test suites live (3-test separation + 23-test backtest), all green — verified by pytest.
- Cross-checked the anti-vacuity 3-conjunct rule against `research/07:137` and spec H1
  (RELEASE-SPEC:139-140) to confirm it is spec-grounded, not invented — verified by Grep + Read.
- Probed Attack-B tautology trap (`:70` blocked-mirror) by mutation reasoning — the assertion
  catches a hardcoded-"pass" impl.

## QA Complete
