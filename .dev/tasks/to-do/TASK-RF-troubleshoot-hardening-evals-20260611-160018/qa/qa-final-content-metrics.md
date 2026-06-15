# QA Report — Final Content/Metrics Review (catch-rate arithmetic)

**Topic:** troubleshoot-hardening-evals — catch-rate model/writer/schema/aggregation arithmetic
**Date:** 2026-06-12
**Phase:** report-qualitative (numeric/metrics adversarial pass)
**Fix cycle:** N/A (report-only, `fix_authorization: false`)
**Stance:** Adversarial — premise asserted ≥5 NUMBER/METRIC errors.

---

## Overall Verdict: PASS

All four VERIFY items hold. The asserted "≥5 number errors" premise does **not** materialize: every count relation, the rate formula, the zero-guard, the `backtest_status` derivation, the anti-vacuity tightening, and cross-artifact count consistency are arithmetically correct. I did not manufacture findings to satisfy the adversarial framing (honest-report rule).

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `catch_rate == caught/total` (0.0 when total==0) | PASS | `catch_rate.py:247` `catch_rate = (caught / total) if total else 0.0`; runtime probe: empty→0.0, 1-of-5→0.2, 5/5→1.0 |
| 1 | `caught + missed == total_escapes` | PASS | `catch_rate.py:245-246` (`missed = total - caught`, balance by construction); `__post_init__` guard `catch_rate.py:168-172`; writer guard `catch_rate_report.py:75-82`; all 5 fixtures balance |
| 2 | `backtest_status` derivation matches §5.4 | PASS | `_derive_backtest_status` `catch_rate.py:119-130`: empty→`not_run`; `all(is_fully_caught)`→`complete`; else→`partial`. Matches research §5.4 (lines 84-93): all-5→complete / some→partial / none→not_run |
| 2 | complete ⟺ all 5 CATCH AND negative_witness AND non-null card_path | PASS | `is_fully_caught` `catch_rate.py:107-113` — exactly the 3 conjuncts; `__post_init__` re-checks `catch_rate.py:179-201` |
| 2 | partial ⟺ replay ran but not-all-3-for-all | PASS | non-empty + not all fully-caught → `partial` (`catch_rate.py:128-130`); incl. all-MISS-non-empty→partial (probe), 1-catch→partial |
| 2 | not_run ⟺ no escapes | PASS | `catch_rate.py:126-127` `if not escapes: return STATUS_NOT_RUN`; aggregation empties on zero refs `test_catch_rate_aggregation.py:65-66` |
| 3 | anti-vacuity: CATCH count alone never reaches complete | PASS | all-CATCH/missing-witness fixture→partial (`all_catch_missing_witness.json` + schema test:201-214); all-CATCH/null-card→partial (schema test:217-231); complete-claim+null-card raises (`catch_rate.py:189-201`, test:234-252) |
| 4 | total_escapes==5 non-empty; waiver excluded | PASS | `REPLAY_ESCAPES` = exactly 5 (E1-E5) `git_replay.py:48-56`; aggregation pins `== 5` `test_catch_rate_aggregation.py:136,194,272`; waiver excluded by docstring+omission `test_catch_rate_aggregation.py:16-17`, schema desc `catch_rate.schema.json:41` |
| 4 | counts consistent model↔writer↔schema↔aggregation | PASS | model guards (`catch_rate.py:168,174`), writer `_check` (`catch_rate_report.py:75-89`), schema `required`+enums (`catch_rate.schema.json:7-18,73-77,104-108`), schema-test pins (`test_catch_rate_schema.py:100-124`) all agree |

## Summary
- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Numeric cross-checks performed (no sampling)
- All 5 fixtures programmatically verified: `caught+missed==total`, `catch_rate==caught/total` (or 0.0), `caught==count(CATCH)`, `len(escapes)==total`. All True.
- `test_backtest_render_output_validates_against_schema` (schema test:76-95): E1=MISS,E2/E3/E5=CATCH,E4=MISS → `caught==3, missed==2`, status `partial`. Arithmetic + derivation correct.
- Live derivation probes: empty→not_run(cr0.0); all-MISS-non-empty→partial(0/5,cr0.0); 1-catch→partial(1/4,cr0.2); all-CATCH-null-card→partial(missing={E1}). All correct.
- `uv run pytest` on both modules: 17 passed, 5 skipped (skips = ref-gated `not_run` arm, expected today).

## Definitional nuance (NOT a defect — flagged for awareness)
`caught` / `catch_rate` count the `verdict==CATCH` dimension; `backtest_status` uses the tighter 3-conjunct `is_fully_caught`. So a report can legitimately show `caught=5, catch_rate=1.0` AND `backtest_status=partial` (all-CATCH but one missing witness/card). The markdown headline renders `{caught}/{total} ({backtest_status})` together (`catch_rate_report.py:107-110`), so "5/5 (partial)" cannot be misread as complete. This is the intended anti-vacuity separation, arithmetically sound.

## Self-Audit
1. Factual claims independently verified against source: 9 checks + 5-fixture programmatic sweep + 4 live derivation probes + a full test run — every numeric relation re-computed, not read.
2. Files read: `catch_rate.py`, `catch_rate_report.py`, `test_catch_rate_aggregation.py`, `test_catch_rate_schema.py`, `git_replay.py`, `catch_rate.schema.json`, all 5 `fixtures/catch_rate/*.json`, research `04-spec-contract-deepdive.md` §5.4.
3. Why trust a PASS with 0 issues: I ran the arithmetic independently (programmatic fixture sweep + 4 edge-case derivation probes + pytest), not just inspected source. The adversarial premise was actively probed at the anti-vacuity boundary (all-MISS-non-empty, null-card, missing-witness) where a seeded error would most plausibly hide — none found.
4. Web research: none required (all checks local-source-bound); Tavily not invoked.

**Tool engagement:** Read: 9 | Grep: 1 | Glob: 0 | Bash: 3

## QA Complete
