# QA Report — Report Validation (Completeness Structural Lens)

**Topic:** FR-RH2 R6 — adversarial seam returns/threads AdversarialResult object into build_reflect_contract + I12 regression test
**Date:** 2026-06-22
**Phase:** report-validation (completeness lens, final QA gate)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed at least one GOAL field silently dropped; hunted for it.

---

## Overall Verdict: PASS

Every GOAL field is wired end-to-end (param + dict key + threaded source), and the I12 regression test contains every required assertion (NOT PASS, HALTED, exit_code==10, reason=="regression") plus provenance and a DEGRADE-not-masking guard. No GOAL field is silently dropped. The 3 `_const_score` injection sites are all covered transitively by the single widened helper.

---

## Coverage Checklist (each GOAL field, wired yes/no, file:line evidence)

| # | GOAL field / requirement | Wired? | Evidence (file:line) |
|---|--------------------------|--------|----------------------|
| 1 | `deviation_count_by_class` threaded into build_reflect_contract (param + dict key) | YES | param: `ensemble.py:469` (`deviation_count_by_class: dict[str, int] \| None = None`); dict key emitted: `ensemble.py:509` (`"deviation_count_by_class": deviation_count_by_class`); threaded at call site: `ensemble.py:307`; sourced from result: `ensemble.py:290-294`. None→default backfill at `ensemble.py:493-499`. |
| 2 | `regression_present` threaded | YES | param: `ensemble.py:467`; dict key: `ensemble.py:520` (`"regression_present": regression_present`); call site: `ensemble.py:304`; sourced: `ensemble.py:275-279`. Was hard-coded `False` pre-R6 (diff line 267→271). |
| 3 | `unauthorized_deviation_present` threaded | YES | param decl: `ensemble.py:467` (`unauthorized_deviation_present: bool = False`); dict key: `ensemble.py:521`; call site: `ensemble.py:305`; sourced: `ensemble.py:280-284`. |
| 4 | `needs_human_decision` threaded | YES | param: `ensemble.py:468`; dict key: `ensemble.py:522`; call site: `ensemble.py:306`; sourced: `ensemble.py:285-289`. |
| 5 | adversarial `report_path` wired (preferred when present via `_select_report_path`) | YES | param: `ensemble.py:470` (`adversarial_report_path`); passed to selector: `ensemble.py:488-492`; preference logic: `ensemble.py:617-618` (`if adversarial_report_path: return adversarial_report_path` — FIRST in chain, before swarm_merged_path); sourced from result: `ensemble.py:295-297`; extractor `_extract_adversarial_report_path`: `ensemble.py:442-457`; populated LIVE in scorer: `ensemble.py:352`. |
| 6 | `user_decision_required` mirror handled (mirrors needs_human_decision) | YES | `ensemble.py:523` (`"user_decision_required": needs_human_decision`) — explicitly mirrors the needs_human_decision local, not a separate hard-coded literal. Was hard-coded `False` pre-R6 (diff line 270). Consumed by contract: `contract.py:321,359` (`user_decision_required is True` → HALTED). |
| 7 | I12 regression test exists + asserts NOT PASS, sharpened to HALTED/exit_code==10/reason=="regression" | YES | `test_ensemble_stub_integration.py:474` (`test_i12_seam_regression_does_not_pass`). Assertions: NOT PASS `:520`; `is Verdict.HALTED` `:522`; `exit_code == 10` `:523`; `reason == "regression"` `:524`. Provenance `contract["regression_present"] is True` `:528`. DEGRADE-not-masking guard `:530-531`. Injects `regression_present=True` via `_regression_score` seam fn `:488-503`. |
| 8 | `_const_score` stub updated to return AdversarialResult, covering 3 injection sites (~93/331/356) | YES | helper widened: `test_ensemble_stub_integration.py:43-60` (return type `-> AdversarialResult`, returns `AdversarialResult(...)`). Injection sites all route through `_const_score`: `_run` helper `:114` (used by I1/I2/I3/I4/I5/I6), `test_i8` `:351`, `test_i9` `:377`. Single helper covers all 3 transitively (comment `:47`). Import added `:29-33`. |
| 9 | `deviation_count_by_class` is a 4-key int dict (authorized/necessary/drift/regression) | YES | dataclass default factory: `ensemble.py:91-98` (4 keys, int 0). Builder None-backfill: `ensemble.py:493-499` (same 4 keys). I12 injects `{authorized:0, necessary:0, drift:0, regression:1}` `:496-501`. Contract `_DEVIATION_KEYS` matches: `contract.py:40` (`("authorized", "necessary", "drift", "regression")`). I7 asserts `set(dev) >= {4 keys}` `:336`. |

### Cross-file behavioral verification (beyond presence)

The I12 assertions are not just structurally present — they assert against REAL routing behavior, independently verified via Bash/grep on contract.py + models.py:

- `regression_present is True` → `_halted_reason` returns `"regression"`: `contract.py:315-316`.
- HALTED routing path: `contract.py:227-231` (HALTED rung consumes `_halted_reason`).
- `Verdict.HALTED.exit_code == 10`: `models.py:46` (`Verdict.HALTED: 10`), confirmed by U6 `test_ensemble_unit.py:182`.
- `user_decision_required` / `needs_human_decision` are genuinely consumed (not write-only): `contract.py:319-321,357-361`.
- `deviation_count_by_class.regression > 0` is ALSO a halt trigger: `contract.py:324-325` — so I12's `regression:1` is independently halt-worthy even if the boolean were dropped (belt-and-suspenders; both wired).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AdversarialResult dataclass defines all 6 fields | PASS | `ensemble.py:72-99`: convergence_score, regression_present, unauthorized_deviation_present, needs_human_decision, deviation_count_by_class (4-key factory), report_path |
| 2 | AdversarialScoreFn alias widened to return AdversarialResult | PASS | `ensemble.py:103` (`Callable[[list[str], Path], AdversarialResult \| None]`) |
| 3 | run_adversarial_scorer return type widened + LIVE convergence_score+report_path | PASS | `ensemble.py:319` return type; `ensemble.py:350-353` constructs AdversarialResult with both LIVE fields |
| 4 | run_tier2_ensemble destructures result → 5 locals | PASS | `ensemble.py:275-297` (regression/unauthorized/needs_human/devcount/report_path), None-guarded |
| 5 | All 5 new kwargs passed at build call site | PASS | `ensemble.py:304-308` |
| 6 | build_reflect_contract signature gains 5 keyword-only params | PASS | `ensemble.py:467-470` |
| 7 | Hard-coded clean literals REPLACED by threaded values | PASS | `ensemble.py:509,520-523` now reference params (diff: lines 253-258,267-270 deleted; 259,271-274 added) |
| 8 | _select_report_path prefers adversarial path FIRST | PASS | `ensemble.py:607-618` — adversarial_report_path checked before swarm_merged_path |
| 9 | I12 test present with full sharpened assertion set | PASS | `test_ensemble_stub_integration.py:474-531` |
| 10 | U11 companion unit test threads kwargs in isolation | PASS | `test_ensemble_unit.py:294-334` (flagged + clean-default both asserted) |
| 11 | _const_score widened, all 3 injection sites covered | PASS | `test_ensemble_stub_integration.py:43-60`; sites `:114,:351,:377` |
| 12 | deviation_count_by_class is 4-key int dict everywhere | PASS | `ensemble.py:91-98,493-499`; `contract.py:40`; tests `:496-501,:53-58` |
| 13 | Contract-side halt routing verified (not just test presence) | PASS | `contract.py:315-316,227-231`; `models.py:46` |

## Summary

- Checks passed: 13 / 13
- Checks failed: 0
- GOAL fields wired: 9 / 9
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| — | — | — | None. No GOAL field silently dropped; no I12 assertion missing. | — |

### Adversarial residual-risk note (no findings, but disclosed)

I actively hunted for a dropped field by tracing each of the 9 GOAL items from dataclass → local → call-site kwarg → emitted contract dict key → downstream consumer. The most likely silent-drop vectors were checked and are CLEAN:

- **`user_decision_required` mirror** (item 6): a plausible drop would be leaving it hard-coded `False` while only wiring `needs_human_decision`. Verified at `ensemble.py:523` it mirrors the local. NOT dropped.
- **`deviation_count_by_class` None-vs-default** (item 1/9): destructure passes `None` when no result (`ensemble.py:290-294`), and the builder backfills the 4-key default (`ensemble.py:493-499`) — so a `None` cannot leak into the contract as a non-dict. NOT dropped.
- **report_path preference order** (item 5): the GOAL says "preferred when present" — verified adversarial path is FIRST in `_select_report_path` (`ensemble.py:617`), not appended after swarm fallback. Correct ordering.
- **I12 masking risk**: a regression HALT could be masked by a DEGRADE (lower precedence). I12 explicitly guards this with `t2_model_class_diversity == "full"` (`:530`) and `is not Verdict.DEGRADED` (`:531`), and uses non-None convergence (0.86) to avoid the null-convergence DEGRADE. Guard present.

## Confidence Gate

**Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 2

All 4 in-scope source files were Read in full (ensemble.py, both test files, qa-input-surface.md; +1 Read of this report for the freshness hook). 2 Bash/grep passes independently verified the contract-side routing (contract.py halt logic + models.py exit_code map) so the I12 assertions are confirmed against REAL behavior, not just asserted in isolation. Tool calls mapped one-to-one to specific verifications; no padding. No external/web lookup required (all claims are local source-truth).

## Recommendations

- Green light. Every GOAL field is wired and I12 carries all required assertions. No remediation needed.

## QA Complete
