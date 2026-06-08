# QA Report — Research Gate

**Topic:** Fix M1 (file-handle leak), M2 (unbounded warn-mode poll loop), M3 (corrupt handoff JSON), M4 (scheduler tests)
**Date:** 2026-06-04
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Assigned files:** 01-source-fix-points.md, 02-test-patterns-and-seams.md, 03-scheduler-and-template.md

---

## Overall Verdict: PASS

All three assigned research files are dense, evidence-based, and accurate. Every spot-checked file:line anchor resolves to the claimed code. The M2 ceiling-source reasoning is correct. All 6 M4 expected wave outputs were independently traced **by executing the real `topological_launch_order`** and match exactly. The template-path claim is correct. No CRITICAL or IMPORTANT issues found. Two MINOR line-range drifts (cosmetic, non-blocking) noted below.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory + Status:Complete | PASS | All 3 files end "Status: Complete"; each has Summary/seam-summary tables |
| 2 | M1 source anchors (executor.py _run_task_subprocess) | PASS | def at executor.py:1468; `proc.start()` L1514; `_poll_with_stall_watchdog(...)` L1518-1520; `timeout_seconds=config.max_turns*120+300` L1506 — all read and confirmed |
| 3 | M2 source anchors (_poll_with_stall_watchdog) | PASS | def L1402; disabled path L1424-1426; `while underlying.poll() is None` L1439; warn `elif` L1446; kill `break` L1464; tail `proc.wait()` L1465 — all exact |
| 4 | M2 ceiling-source claim (proc.timeout_seconds vs config) | PASS | process.py:162 `wait(timeout=self.timeout_seconds)`; `timeout_seconds` set process.py:61; SprintConfig has NO `timeout_seconds` field (models.py:536/544/545 = max_turns/startup_stall_timeout/stall_action) → `config.timeout_seconds` is genuinely the WRONG source. Claim correct. |
| 5 | M3 source anchors (handoff.py read) | PASS | `read` def handoff.py:62; `json.loads(path.read_text())` unwrapped L71; `json` import L18; `HandoffRecord` import L20 — exact |
| 6 | M3 JSONDecodeError ⊂ ValueError | PASS | Runtime: `issubclass(json.JSONDecodeError, ValueError) is True` confirmed |
| 7 | M3 from_dict does NOT validate enums | PASS | models.py:329-359 `from_dict` uses `data.get(key, default)` for every field, no `GateOutcome(...)`/`TaskStatus(...)` calls → no ValueError on bad enum string. Claim accurate. |
| 8 | M3 caller guards (None ⇒ re-run) | PASS | Parallel: executor.py:1103-1104 `_prior = read(...)` then `if _prior is not None and is_validated_success(_prior):`. Sequential: executor.py:1277-1278 identical. Both gated by `(config.results_dir / "handoff").exists()` (:1101/:1275). Exact. |
| 9 | M3 is_validated_success swallows ValueError | PASS | handoff.py:36-40 `try: GateOutcome(...).is_success except ValueError: return False` — confirmed |
| 10 | M4 scheduler API surface (research 03) | PASS | scheduler.py read in full (120 lines): CycleError(ValueError) L27-38; dependencies_of L41-71; topological_launch_order L74-104; is_task_satisfied L107-119 — all signatures + line refs accurate |
| 11 | M4 Case 1 diamond expected output | PASS | **Executed** real code → `[['A'],['B','C'],['D']]` == research claim |
| 12 | M4 Case 2 chain | PASS | **Executed** → `[['A'],['B'],['C']]` == claim |
| 13 | M4 Case 3 independent + permuted | PASS | **Executed** → `[['A','B','C']]` and permuted `[['C','A','B']]` == claim |
| 14 | M4 Case 4 cycle | PASS | **Executed** → raises CycleError, `.unresolved == ['A','B','C']`, str == `"dependency cycle detected among tasks: A, B, C"` == claim |
| 15 | M4 Case 5 self-edge | PASS | **Executed** → `[['A'],['B']]`, `dependencies_of("A",{"A":te("A",["A"])}) == []` == claim |
| 16 | M4 Case 6 unknown/cross-set dep | PASS | **Executed** → `[['A'],['B']]`, `dependencies_of("A", ...) == []` == claim |
| 17 | M4 extras (dedup, recorded-union, is_task_satisfied) | PASS | **Executed** → dedup `['B','C']`; recorded-union `['B','C']`; sat `None`/`True`/`False` for empty/PASS/FAIL == claims |
| 18 | TaskStatus.is_success values | PASS | models.py:57-58 `return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)` — matches research (PASS + PASS_RECOVERED only) |
| 19 | Template path claim (src canonical, .claude unsynced) | PASS | `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` exists (85KB); `.claude/templates/workflow/02_mdtm_template_complex_task.md` → "No such file or directory". Claim correct. |
| 20 | M1/M2 process.py contract facts | PASS | wait() 159-171 (timeout L162, terminate→124 L163-165, _close_handles L170); terminate() 173-214 (early-return+close L175-177, close L214); _close_handles() 238-244 guarded+try/except; __init__ None-inits L69-71; start() opens handles L120/122/123 — all exact |
| 21 | Test seam test_executor.py:1904-1963 (M1) | PASS | `test_run_task_subprocess_uses_task_output_file` read: imports `_run_task_subprocess`, `capture_init` sets `_process`/`_stdout_fh=None`/`_stderr_fh=None`, patches base `__init__`/`start`/`wait` — matches research-02 sketch |
| 22 | conftest autouse + strict-markers (research 02) | PASS | conftest.py:32+ `_stub_phase_narrative` autouse with `_NARRATIVE_TEST_MODULES` opt-out (25-29); pyproject `--strict-markers` + `unit`/`integration`/`slow` registered |
| 23 | test_handoff_store helpers (M3 seam) | PASS | `_config` (17-29), `_record` (32-46), on-disk key `results_dir/handoff/phase-1-task-T01.01.json` (:78-80) — exact |
| 24 | new-file template (test_turn_ledger_concurrency.py) | PASS | Header 1-16: defect-class docstring, `from __future__ import annotations`, `import pytest`, sprint import — matches |
| 25 | Evidence density / unsupported assertions | PASS | Every claim carries a file:line or a runtime check. No bare "the system handles X" assertions. Both R1/R2 end "Nothing left Unverified." |
| 26 | Coverage — each fix has a test design + each M4 case has exact output | PASS | M1/M2/M3 each have a seam + setup sketch + assertions in R2; M4 all 6 cases + extras have EXACT expected outputs in R3 |
| 27 | Gaps & Questions severity | PASS | No CRITICAL/IMPORTANT/MINOR gaps left open by the research; the "edge beyond scope" notes (M3 wrong-shape JSON, M2 fallback) are correctly flagged as deliberate builder decisions, not unresolved gaps |

---

## Summary
- Checks passed: 27 / 27
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: N/A (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 03-scheduler-and-template.md L131 (cites "models.py:329-350"), L262/L263 | `HandoffRecord.from_dict` actually spans models.py:329-359 (return block ends ~358); cited as 329-350. Off-by-~8 on the end bound. Does not affect any conclusion — `from_dict` semantics (`.get`, no enum validation) verified correct. | Optional: update end line to 359. Non-blocking. |
| 2 | MINOR | 01-source-fix-points.md L205 (cites "models.py:329-350") | Same end-bound drift as #1 (from_dict end line). Substance accurate. | Optional: 329-359. Non-blocking. |

Neither issue changes a fix recommendation, a test design, or an M4 expected output. They are line-range cosmetics on a correctly-characterized function.

## Notes on Adversarial Spot-Checks (what I tried to break)

- **M2 ceiling source** — I specifically tried to falsify the "use `proc.timeout_seconds`, not `config.timeout_seconds`" claim by grepping `models.py` for a `timeout_seconds` field on SprintConfig. There is none (only `max_turns`/`startup_stall_timeout`/`stall_action`). The research is right that `config.timeout_seconds` would be an AttributeError and that `proc.timeout_seconds` (= `max_turns*120+300`, the value `wait()` already enforces) is the coherent ceiling. The `getattr(proc, "timeout_seconds", <fallback>)` recommendation is also justified because `_poll_with_stall_watchdog` is duck-typed (no annotation on `proc`, executor.py:1403).
- **M4 traces** — I did not trust the hand-traces. I executed `topological_launch_order`, `dependencies_of`, and `is_task_satisfied` against the real module under `uv run` (project deps) and compared every output byte-for-byte. All 10 traced expectations (6 cases + 4 extras) matched. The cycle case's `.unresolved` ordering (`['A','B','C']` = declared order) and exact `str()` message both confirmed.
- **M3 raise analysis** — Confirmed `from_dict` does NOT call enum constructors (so the realistic raise is `json.loads` → JSONDecodeError ⊂ ValueError, runtime-verified), and that the research correctly flags the wrong-shape-JSON edge (top-level list → AttributeError/TypeError uncaught by `(JSONDecodeError, ValueError)`) as an explicit out-of-scope builder decision rather than silently asserting full coverage.
- **Template path** — Verified `.claude/templates/...` genuinely absent in this worktree and `src/` present; the SoT reasoning matches CLAUDE.md.

## Confidence
**Verified: 27/27 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

All 27 checks carry direct tool evidence (Read of the cited source region, Bash grep of the field/symbol, or live execution of the scheduler). No item was marked VERIFIED on the basis of another report's claim — every anchor was opened against HEAD source.

**Tool engagement:** Read: 7 | Grep: 3 | Glob: 0 | Bash: 5 (3 of which executed real code / verified runtime facts: JSONDecodeError subclass, M4 trace, template-path existence)

No web research was required (all claims are intrinsically local source-truth, not external/URL/standards-bound), so no Tavily/WebSearch engagement.

## Recommendations

- **Green light for synthesis / builder.** The research is accurate and complete enough to drive the M1/M2/M3/M4 implementation without re-investigation.
- Builder should carry forward the research's own explicit deliberate-decision flags as written: (a) M1 use `except BaseException` not `except Exception` (to catch KeyboardInterrupt) and re-raise; (b) M2 use `getattr(proc, "timeout_seconds", <fallback>)` not a bare attribute access; (c) M3 keep the except narrow to `(json.JSONDecodeError, ValueError)` matching the review, treating wrong-shape JSON as an explicit opt-in if desired.
- The two MINOR from_dict line-range drifts need no fix to proceed.

## QA Complete
