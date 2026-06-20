# QA Report — Post-Deletion-Coverage Lens (Phase Gate 5, content-QA)

**Topic:** sc-bare-review M8/M9 migration — does the parity gate still ASSERT after `t2_normalize.py` deletion, or did it silently SKIP?
**Date:** 2026-06-16
**Phase:** report-qualitative (content-QA / independent re-run lens)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9`

---

## Overall Verdict: PASS

**One-line justification:** Adversarial hypothesis (gate silently SKIPPED on deletion) is DISPROVEN — I re-ran the gate myself post-deletion (`t2_normalize.py` is gone from disk AND git index) and all 27 bare-review parity+recipe tests RAN and PASSED with 0 SKIPPED, the full swarm suite is 2212/0-failed with the delta exactly accounted for, and the parity file contains zero executable `skipif`/`LEGACY_SCRIPT`/`.exists()` skip guards (docstring-only).

---

## Adversarial Hypothesis Under Test

> "Assume the parity gate silently SKIPPED after deletion instead of asserting. Prove it."

This is the migration's headline safety property. The OLD gate used `skipif(LEGACY_SCRIPT.exists())` — a whole-module guard that would evaporate parity coverage the instant `t2_normalize.py` was deleted (the script gone ⇒ guard true ⇒ module skipped ⇒ green CI that asserts nothing). The migration's entire point is to replace that with a CLI-vs-frozen-golden gate that needs no legacy script at runtime. If the hypothesis were TRUE, I would observe SKIPPED bare-review parity tests in a real post-deletion run.

**Result: hypothesis FALSE.** Direct evidence below.

---

## Items Reviewed
| # | Check | Result | Evidence (independently observed) |
|---|-------|--------|----------|
| 1 | `t2_normalize.py` genuinely deleted (real post-deletion run) | PASS | `ls scripts/t2_normalize.py` → "No such file or directory" (exit 2); `git ls-files scripts/t2_normalize.py` → empty (not tracked). This is a REAL post-deletion run, not a simulation. |
| 2 | Every parity+recipe test RAN and PASSED, NONE skipped | PASS | `pytest test_bare_review_parity.py test_recipe_bare_review.py -v` → **27 passed in 0.37s**, zero `SKIPPED` in verbose per-test output. 16 parity + 11 recipe. |
| 3 | No new regressions vs baseline | PASS | `pytest tests/swarm/ -q` → **2212 passed, 27 skipped, 0 failed in 11.41s**. Baseline = 2212 passed / 26 skipped / 0 failed. Every baseline-passing test still passes; 0 failed. |
| 4 | Intentional delta accounted for (5 legacy A/B tests removed) | PASS | `pytest --collect-only \| grep legacy_vs_recipe_byte_identical` → no matches (exit 1 = not collected, not merely skipped). Recipe file collects exactly 11 tests (was 16). Truly deleted, not renamed/skipped. |
| 5 | Parity gate has no `skipif`/`LEGACY_SCRIPT` that could skip post-deletion | PASS | `grep -nE "pytest.mark.skip\|skipif\|pytestmark\|LEGACY_SCRIPT\|.exists()"` on parity file → **0 matches (exit 1)**. All `t2_normalize` mentions (lines 13,15,19,46) are inside the module docstring. Docstring-only = fine per spec. |
| 6 | Recipe file `.exists()` is not a skip guard | PASS | Only `.exists()` in recipe file is line 260 `assert not Path(worker.final_path).exists()` — a positive assertion about worker output, NOT a module/function skip guard. No `skipif`/`LEGACY_SCRIPT`/`pytestmark`. |
| 7 | Skip-count reconciliation (baseline 26 → now 27) | PASS | The +1 skip is the new env-gated regen helper `test_bare_review_golden_regen.py::test_regenerate_frozen_golden` (SKIPPED unless `REGEN_GOLDEN=1`). Confirmed by direct run. This is a deliberate human-blessed regen tool, not a parity test that evaporated — the 16 parity tests all RUN. |

---

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: FALSE)

### Raw re-run pytest summaries (the actual counts I observed)

**Gate run (parity + recipe, verbose):**
```
27 passed in 0.37s
  - tests/swarm/test_bare_review_parity.py  : 16 passed, 0 skipped
  - tests/swarm/test_recipe_bare_review.py  : 11 passed, 0 skipped
  (zero SKIPPED across all 27 — verified per-test in -v output)
```

**Full swarm suite:**
```
2212 passed, 27 skipped, 0 failed in 11.41s
```

**Baseline comparison:**
| run | passed | skipped | failed |
|-----|--------|---------|--------|
| baseline (pre-migration, from baseline-summary.md) | 2212 | 26 | 0 |
| **WS-C post-deletion (MY re-run)** | **2212** | **27** | **0** |

Reconciliation arithmetic (independently checked): WS-B 2217 − 5 removed legacy A/B parity tests = 2212 passed (matches). Skipped 26 → 27 = +1 from the env-gated golden-regen helper (matches; confirmed it is `test_regenerate_frozen_golden`, env-gated on `REGEN_GOLDEN=1`). 0 failed at baseline AND post-deletion.

---

## Cross-check vs the input summaries
Both input artifacts (`ws-c-gate-summary.md`, `baseline-summary.md`) are CORROBORATED by my independent re-run — no discrepancies found:
- ws-c-gate-summary claim "27 passed, 0 skipped, 0 failed" for parity+recipe → **confirmed** (I observed 27 passed in 0.37s, 0 skipped).
- ws-c-gate-summary claim "16 parity + 11 recipe" → **confirmed** by `--collect-only` (16 and 11).
- ws-c-gate-summary claim "2212 passed, 27 skipped, 0 failed" full suite → **confirmed** (2212/27/0).
- ws-c-gate-summary claim "removed the 5 parametrized `test_legacy_vs_recipe_byte_identical[*]`" → **confirmed** (not collected, exit 1).
- baseline-summary claim "26 skipped pre-migration" and "+1 = regen helper" → **confirmed** by collect + regen run.

---

## Self-Audit
**(a) Reliance list — items where I relied on a prior structural verdict and skipped re-checking:**
- None. I re-ran every assertion from scratch rather than trusting the WS-C summary. This lens is defined as an independent post-deletion re-run, so reliance was deliberately zero.

**(b) Independent semantic checks (≥1 required):**
- Disproved the "silent SKIP" hypothesis by running `pytest -v` and reading every per-test status line for SKIPPED — verified by direct tool output (27 passed, 0 skipped).
- Verified the absence of skip guards via `grep -nE "skipif|LEGACY_SCRIPT|pytestmark|.exists()"` on the parity file (0 executable matches; docstring-only hits confirmed by line numbers 13/15/19/46 against the file body I Read).
- Verified deletion is real, not simulated: `ls` + `git ls-files` both confirm `t2_normalize.py` absent from disk and index.
- Verified the 5-test delta is a true deletion not a skip/rename via `--collect-only | grep` (exit 1 = uncollected).
- Verified the +1 skip delta semantically (it is the env-gated regen tool, not an evaporated parity test) by running the regen file directly.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 3 | Glob: 0 | Bash: 7
**Web research performed:** None (this lens is entirely local-file / test-execution bound; no external lookup required, so no Tavily/fallback engagement).

---

## Recommendations
- None blocking. The post-deletion-coverage safety property is proven: the rebuilt CLI-vs-frozen-golden gate keeps asserting after `t2_normalize.py` deletion where the legacy `skipif(LEGACY_SCRIPT.exists())` gate would have silently evaporated. Green light for this phase gate.

## QA Complete
