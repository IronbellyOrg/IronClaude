# QA Report — Report Validation (Structural Test-Green Verification)

**Topic:** pytest backtest suite green-verdict integrity (TASK-RF-troubleshoot-hardening-evals-20260611-160018)
**Date:** 2026-06-12
**Phase:** report-validation (test-result attestation)
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Stance:** Adversarial — assumed ≥3 misreports; independently re-ran the suite.

---

## Overall Verdict: PASS

The pytest backtest result was NOT misreported. The summary, the verdict file, and the raw
output are mutually consistent and match an independent re-run. All 11 skips are correctly
attributed to designed guards; zero are collection errors or accidental OLD=MISS skips. The
5 OLD=MISS unit tests (`test_backtest_e1..e5` OLD halves) genuinely RAN and PASSED on this
full clone.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Raw output shows 0 failed AND 0 errored | PASS | `pytest-backtest-output.txt:88` → `32 passed, 11 skipped in 10.00s`. No `failed`/`error` token; `grep -ciE "error\|cannot collect\|importerror"` over raw output = **0**. |
| 2 | Independent re-run reproduces counts | PASS | My `uv run pytest tests/troubleshoot/backtest/ -q` → `32 passed, 11 skipped in 10.01s`. Per-test `-v` count: 32 PASSED / 11 SKIPPED (grep-counted). |
| 3 | Summary counts match raw EXACTLY | PASS | `pytest-backtest-summary.md:10-13` (passed 32 / skipped 11 / failed 0 / errored 0) == raw `:88` == verdict `pytest-verdict.md:6`. |
| 4 | All 11 skips designed, not collection/accidental | PASS | 5 NEW=CATCH proxies (`@requires_impl_ref`), 5 catch-rate aggregation parametrize (`pytest.skip` not_run), 1 waiver_regreen (`@requires_impl_ref`). Maps 1:1 to summary table `:21-25`. |
| 5 | Skip guards key on genuinely-absent impl refs | PASS | `ls` of `src/superclaude/skills/sc-troubleshoot-protocol/refs/` shows NONE of the 6 gating refs (runtime-entrypoint-verification, unmask-and-sweep, contract-enumeration, effective-input-proof, hardening-output-contract, pipeline-hardening-closure). Skips are legitimately expected. |
| 6 | OLD=MISS halves RAN + PASSED (not skipped) | PASS | `-v` output shows `test_backtest_e{1..5}_old_protocol_misses_*` all **PASSED** (output lines 11,18,24,30,37 in pytest-backtest-output.txt; reproduced in my run). |
| 7 | OLD=MISS halves carry real assertions (non-vacuous) | PASS | `test_backtest_e1.py:62,65,75` assert `emits_local_file is True`, `--file in argv`, `verdict==MISS and negative_witness`. e2-e5 carry analogous real assertions (`halted is True`, source-text asserts). |
| 8 | Module-level `pytestmark` skipif did NOT silently skip OLD halves | PASS | `test_backtest_e1.py:26` gates OLD half on `not is_git_worktree() OR missing_replay_commits([prefix_sha])` (shallow-CI guard). On this full clone it evaluated **False** → OLD halves ran (item 6). This was the highest misattribution risk; cleared. |

---

## Summary

- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Adversarial Findings (3 misreport hypotheses tested → all REFUTED)

| # | Hypothesized misreport | Outcome | Refutation evidence |
|---|------------------------|---------|---------------------|
| H1 | An OLD=MISS test was silently SKIPPED (via module `pytestmark` skipif) but reported as if the suite is clean | REFUTED | All 5 OLD halves show PASSED in both the recorded output and my independent re-run; skipif is the shallow-clone guard, False here. |
| H2 | A skip masks a collection/import error (broken proxy import counted as benign skip) | REFUTED | `grep -ciE "error\|cannot collect\|importerror\|no module"` over raw output = 0; collected 43 items cleanly; impl-ref guards use file-existence skipif, not import probes. |
| H3 | Summary counts drifted from raw (inflated pass / hidden fail) | REFUTED | 32/11/0/0 identical across raw `:88`, summary `:10-13`, verdict `:6`, and my re-run `32 passed, 11 skipped`. |

## Actions Taken

None — report-only (fix_authorization: false). No source file modified.

## Recommendations

- None blocking. The GREEN verdict is sound and may proceed. The 11 skips are self-clearing:
  they un-skip automatically once `feat/troubleshoot-pipeline-hardening` lands the 6 refs.

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 4 | Glob: 0 | Bash: 6 (incl. 1 independent pytest re-run)
- Every checklist item maps to a specific tool call (Read of the 3 artifacts; Bash re-run + grep
  of test bodies, skip guards, refs dir, collection-error scan). Tool calls ≥ checklist items.

## QA Complete
