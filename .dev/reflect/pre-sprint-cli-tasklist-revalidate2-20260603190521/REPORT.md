# /sc:reflect — UC-1 Re-Validation #2 (Tier 1): M-A / M-D closure + no-regression

**Tasklist:** TASK-RF-20260603-024610 · **Spec:** SYNTHESIS.md · **Mode:** pre · **Depth:** standard (Tier 1, independent gpt-5.5 reviewer)
**Date:** 2026-06-03 · Validates the M-A + M-D remediation (commit 167e22a7) + the M-A anchor fix.

## Verdict: PASS (substantive)

| Item | Status | Evidence |
|---|---|---|
| **M-A** real concurrent-spawn gate | ✅ CLOSED | Step 2.9 now has 3 assertions: env-uniqueness, positive `ThreadPoolExecutor(≥4)` repro (per-worker `setup_isolation(scope=…)` settings dir + shared baseline byte-identical/never-written), negative control. Deterministic + non-destructive (tmp_path). |
| **M-D** `--resume` docs | ✅ CLOSED | Step 4.3a between 4.3/4.4 documents flag + arg + `--start/--end` composition + pre-Stage-1 degradation. |
| **No regression** | ✅ | H-A semantic contract intact (gate_outcome `str` + `GateOutcome(...).is_success` across spec H4 + Steps 3.1/3.2/4.1); H-B Step 2.6 supersede intact; H-C RC.1 correct signature + RC.2/3/4 intact; Step 4.3a did not shift 4.4+ numbering. |

**All 6 M-A source anchors independently resolved** by the reviewer:
`test_home_isolation_extend.py:39,209` (imports + `ThreadPoolExecutor(max_workers=8)`), `test_home_isolation.py:44,418`, `e2e_real/conftest.py:103` (`claude_shim`), `test_state_dir_isolation.py:33`.

## On the reviewer's literal "FAIL"

The reviewer returned FAIL solely because my no-regression instruction said "0 occurrences of 'dict or None' anywhere," but Step 3.2 (line 226) contains "**NOT a dict or None**" — the *intentional* clarification added during the H-A fix telling the executor that `gate_outcome` is the `GateOutcome.value` string, NOT a dict/None. This is correct, desirable text — a false positive on an over-literal lexical check, not a regression. The reviewer explicitly states "the semantic contract remains consistent." No fix warranted.

## Process note (the anchor catch)

The original M-A edit cited `ThreadPoolExecutor in test_perf_resource_bounds.py:215` — but that line is a *docstring about concurrency*, not a `ThreadPoolExecutor` usage. Pre-flight grep caught it; corrected to `test_home_isolation_extend.py:209` / `test_home_isolation.py:418` (ThreadPoolExecutor tests *specifically for settings/home-dir isolation under concurrency* — a strictly better analog). This is the 3rd self-authored mis-anchor an independent/pre-flight check has caught across the remediation rounds — the validation loop is doing its job.

## Status

4 of 4 in-scope reflect MEDIUMs targeted this session are now resolved on the §3-roadmap axis is 1.00 and **M-A + M-D closed**. Remaining open: **M-B** (declared-upstream fan-in injection) and **M-C** (per-stage full-suite regression + call-site sweep) — not in this round's scope. The tasklist is ready for `/task` execution.
