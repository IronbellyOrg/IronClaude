# QA Report — Structural Lens: Template Conformance (P6 / Phase 7 gate)

**Verdict: PASS**

**Topic:** P6 — execution-log events + nominator exclusion (429 recovery)
**Date:** 2026-06-18
**Phase:** report-validation (structural lens, P6 deliverables)
**Lens:** template-conformance ONLY
**Fix authorization:** false (report-only)
**Stance:** adversarial / zero-trust — every claim re-verified against source.

---

## Overall Verdict: PASS

All three template-conformance sub-checks pass against the actual source files.
No `DriftNominator` was invented. No new lock was introduced. All four emit sites
are None-guarded. Both new logging methods mirror `write_task_complete`'s
dict-build + `self._jsonl(...)` idiom exactly.

> Note: this file previously held a STALE P5-era report (aienv import /
> build_account_exhaustion_halt / --max-session-resets — a different lens scope).
> Overwritten with the current P6 template-conformance run (the three lenses
> assigned: logging_ methods, executor emit-site guards, rerun_tasks nominator
> exclusion).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `write_session_reset` mirrors `write_task_complete` idiom | PASS | `logging_.py:251-271` — dict literal `{event, phase, task_id, attempt, exhausted_model, timestamp}` then `self._jsonl(...)`. Same shape as `write_task_complete` (`:239-249`). |
| 2 | `write_account_exhaustion_halt` mirrors idiom | PASS | `logging_.py:273-294` — dict literal `{event, phase, task_id, exhausted_model, session_resets, timestamp}` → `self._jsonl(...)`. |
| 3 | Event names present | PASS | `"session_reset"` (`logging_.py:264`); `"account_exhaustion_halt"` (`logging_.py:287`). |
| 4 | Timestamp present in both | PASS | `datetime.now(timezone.utc).isoformat()` at `logging_.py:269` and `:292` — identical to `write_task_complete:247`. |
| 5 | Thread-safe via existing `_jsonl_lock`, NO new lock | PASS | Only one `threading.Lock()` in file, at `logging_.py:31` (pre-existing `_jsonl_lock`), acquired in `_jsonl` at `:353`. Both new methods route through `self._jsonl` and add no lock. grep: exactly 1 `Lock()`. |
| 6 | Executor emit sites use `if logger is not None:` guard (all 4) | PASS | Per-task loop: `executor.py:1074` guards `write_session_reset` (`:1075`); `:1094` guards `write_account_exhaustion_halt` (`:1095`). Single-session loop: `:2130` guards `write_session_reset` (`:2131`); `:2142` guards `write_account_exhaustion_halt` (`:2143`). |
| 7 | Exactly 4 emit sites, no double-emit | PASS | `grep -c`: `write_session_reset` = 2, `write_account_exhaustion_halt` = 2. Per-task halt emit (`:1094`) fires only on the latch-tripping worker — latch precheck `:1019-1028` breaks before reaching emit on sibling workers. |
| 8 | `logger=logger` threaded at both `_run_one_task` call sites | PASS | K>1 site `executor.py:1245` → `lock=lock, ..., logger=logger` (`:1257`). K=1 site `:1461` → `lock=None, ..., logger=logger` (`:1473`). `_run_one_task` signature accepts `logger=None` (`:984`). |
| 9 | Nominator exclusion targets REAL symbols | PASS | `rerun_tasks.py` imports `ManualNominator` (`:48`), `ReflectReportNominator` (`:51`) from `recovery.py`; `select_default_recoverable_tasks` defined `:1159`. All real in `recovery.py` (`Nominator` Protocol `:143`, `ManualNominator` `:149`, `ReflectReportNominator` `:164`). |
| 10 | NO invented `DriftNominator` | PASS | `grep -rn "DriftNominator" src/superclaude/cli/sprint/` → NONE FOUND. Manifest's "NO `DriftNominator`" claim is accurate. |
| 11 | Exclusion guard present in `select_default_recoverable_tasks` | PASS | `rerun_tasks.py:1188` — `if entry.get("failure_class") == "provider_exhaustion": continue`. Realistic-leak completion in `run_rerun_tasks` fallback `:1468-1474` filters `FAIL_PROVIDER_EXHAUSTED` from transcript-discovered ids. |

---

## Summary

- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None for this lens.

### Adversarial probes (sought >=5 errors; found 0 in-lens)

1. **Invented nominator class** — sought a `DriftNominator` or any nominator not
   defined in `recovery.py`. Grep across the whole sprint dir: none. All three
   referenced nominator symbols resolve to real `recovery.py` definitions.
2. **New lock** — sought a second `threading.Lock()` / per-method lock that would
   violate "thread-safe via the existing `_jsonl_lock`". Only the pre-existing
   `_jsonl_lock` at `logging_.py:31` exists; both new methods reuse `self._jsonl`.
3. **Missing None-guard** — checked all 4 emit sites individually (not just a
   count); every one is wrapped in `if logger is not None:`.
4. **Idiom drift** — both new methods use a dict literal + `self._jsonl`, not
   `open(...).write(...)` or a divergent builder. Field order + timestamp match.
5. **Unthreaded call site** — both `_run_one_task` call sites (K>1 `:1245`, K=1
   `:1461`) thread `logger=logger`; neither drops it silently.

## Confidence

Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 6 | Grep: 0 (tool unavailable this session) | Glob: 0 | Bash: 3 (grep via Bash — DriftNominator sweep, nominator symbol resolution, emit-site count, lock count, call-site enumeration)

Note: the `Grep` tool was unavailable; all content searches ran via `grep`
through Bash. Tool calls map 1:1 to checklist items — no padding.

## Recommendations

- Green light on the template-conformance lens. No remediation required.
- Out-of-lens observation (NOT a finding): `logger.write_phase_interrupt` at
  `executor.py:2157` is called WITHOUT a `if logger is not None:` guard. This is
  pre-existing code outside the three assigned 429-emit lenses; flagged only so a
  broader None-safety lens can decide whether it matters.

## QA Complete
