# Research Completeness Verification

**Topic:** Remediation of M1-M4 from PR-120 code review (handle-leak, watchdog-unbounded, corrupt-handoff-read, missing-scheduler-test)
**Date:** 2026-06-04
**Files analyzed:** 3 (01-source-fix-points.md, 02-test-patterns-and-seams.md, 03-scheduler-and-template.md)
**Depth tier:** Deep (fix-point identification + contract verification + traced test cases)
**Analyst spot-checks:** executor.py, handoff.py, process.py, scheduler.py, models.py, pyproject.toml, template paths, test-file existence — all read at HEAD on `SprintCLIWireDead`.

---

## Verdict: PASS (0 blocking gaps; 2 minor notes)

The three research files are thorough, evidence-based, and code-traced. Every load-bearing
claim I independently spot-checked against source verified correct. The research is sufficient
to build a per-fix-plus-per-test MDTM tasklist for M1-M4 with no further investigation required.

---

## Per-Question Verdicts (spawn-prompt checklist)

### Q1 — Source fix points with file:line + concrete minimal fix shape for M1, M2, M3? PASS

| Fix | Fix site (research) | Spot-check | Minimal fix shape present? |
|---|---|---|---|
| M1 handle-leak | `executor.py:1514-1520` (`_run_task_subprocess`) wrap `start()`+poll | VERIFIED — `proc.start()` then `_poll_with_stall_watchdog(...)` with no try/finally; `wait()` only runs inside the watchdog | Yes — `try: _poll_...(...) except BaseException: proc.terminate(); raise` (01 §M1(b)), with rationale for `BaseException` over `Exception` (catches KeyboardInterrupt) |
| M2 watchdog-unbounded | `executor.py:1436-1465` (`_poll_with_stall_watchdog`) | VERIFIED — the only `break` is inside the `stall_action=="kill"` block; `warn` mode loop `while underlying.poll() is None:` has no wall-clock bound; `proc.wait()` at tail only reached on loop exit | Yes — add `(time.monotonic() - loop_started) < ceiling` to the `while` guard so the loop falls through to bounded `proc.wait()` (01 §M2(b)) |
| M3 corrupt-handoff | `handoff.py:71` (`FileHandoffStore.read`) | VERIFIED — `return HandoffRecord.from_dict(json.loads(path.read_text()))` is unwrapped | Yes — `try: ... except (json.JSONDecodeError, ValueError): return None` (01 §M3(b)) |

All three fix sites give exact line spans, the current code verbatim, and an explicit minimal-fix
diff shape. The absolute line numbers in 01 are accurate (verified against HEAD).

### Q2 — Fix-safety contracts verified (base terminate()/_close_handles(); M2 ceiling source; M3 caller None-handling)? PASS

- **M1 base-class contract:** `_close_handles()` (process.py:238-244) is idempotent + exception-swallowing; `terminate()` (process.py:173-214) early-returns and still calls `_close_handles()` when `self._process is None or self._process.poll() is not None`. **Spot-checked process.py:159-244 — exactly as documented.** Double-close-is-safe and terminate-on-exited-child-is-safe both confirmed. The "happy path's `proc.wait()` already closes handles, new except only fires on exception" reasoning is correct.
- **M2 ceiling source:** `proc.timeout_seconds` (set to `config.max_turns * 120 + 300` in `_Base.__init__`, and the value `proc.wait()` already enforces at process.py:162). **Spot-checked: `self.timeout_seconds = timeout_seconds` at process.py:61; `self._process.wait(timeout=self.timeout_seconds)` at process.py:162.** Research correctly rejects `config.timeout_seconds` (doesn't exist on SprintConfig) and recommends `getattr(proc, "timeout_seconds", <fallback>)` for the duck-typed `proc`. Sound.
- **M3 caller None-handling:** both resume-skip call sites guard `if _prior is not None and is_validated_success(_prior):` (executor.py:1104 parallel `_worker`, :1278 sequential loop), so `None` ⇒ task re-runs — the correct degrade for a corrupt record. Research also verified `json.JSONDecodeError ⊂ ValueError` at runtime and that `is_validated_success` already swallows enum `ValueError` (handoff.py:36-40). Thorough.

### Q3 — Test seams concrete enough to write per-fix unit tests (M1/M2/M3) + new M4 file? PASS

- **M1 seam:** direct call of `_run_task_subprocess`, modeled on the proven harness at `test_executor.py:1904-1963`; patch base `ClaudeProcess.__init__/start/terminate`, force `executor._poll_with_stall_watchdog` to raise `KeyboardInterrupt`, assert `pytest.raises(KeyboardInterrupt)` + `terminate` spy fired. Full runnable sketch provided (02 §M1).
- **M2 seam:** pure unit test with a hand-rolled fake `proc` calling `_poll_with_stall_watchdog` directly; patch `executor.time.sleep`/`time.monotonic` with an advancing clock so the ceiling trips deterministically. Research correctly identifies that `test_watchdog.py` exercises the *phase-level* monitor (`MonitorState`/`OutputMonitor`), a DIFFERENT surface, and is the wrong seam — a non-obvious, valuable distinction. Full sketch + companion kill-mode + disabled-path guidance (02 §M2).
- **M3 seam:** extend `test_handoff_store.py` (`_config`/`_record` helpers, `config.handoff_file(phase, task)` path); write truncated/empty/garbage bytes, assert `read(...) is None`. Plus optional resume-rerun integration in `test_handoff_crash_consistency.py`. Full sketch (02 §M3).
- **M4 new file:** `tests/sprint/test_scheduler.py` — **confirmed it does NOT yet exist** (correct: it is the file to be created). Import surface, `te()`/`TaskResult` factories, and template all provided (03 §A.0, §A.5).

### Q4 — M4 scheduler cases have EXACT inputs + EXACT expected outputs traced from real code? PASS

Spot-checked the scheduler algorithm at `scheduler.py:74-104` against all 6 traced cases:
- Wave algorithm: `wave = [tid for tid in remaining if all(d in satisfied for d in deps[tid])]`, within-wave order = `remaining` (declared) order, `raise CycleError(remaining)` on empty-wave-with-remaining. **Matches the trace exactly.**
- Case 1 diamond → `[["A"], ["B","C"], ["D"]]`: correct.
- Case 2 chain → `[["A"], ["B"], ["C"]]`: correct.
- Case 3 independent → `[["A","B","C"]]` + permuted-order determinism check: correct (within-wave = declared order, confirmed).
- Case 4 cycle → `CycleError`, `.unresolved == ["A","B","C"]`, exact `str()`: correct (`raise CycleError(remaining)`, `remaining == ordered_ids` on first iteration).
- Case 5 self-edge → dropped (`dep != task_id` filter, scheduler.py:58): correct.
- Case 6 unknown dep → filtered (`dep in entry_by_id`, scheduler.py:58): correct.

Each case lists EXACT `te(...)` inputs and EXACT expected list-of-waves output, with per-wave
`deps`/`satisfied` reasoning. Inputs and outputs are derived from the real algorithm, not assumed.
The "A→B means B depends on A" convention is stated explicitly to avoid edge-direction ambiguity.

### Q5 — New-test-file conventions documented (markers, imports, header) + verification commands? PASS

- **Conventions:** autouse narrative stub auto-covers new sprint modules (conftest.py:32-55, and correctly notes NOT to add the new module to `_NARRATIVE_TEST_MODULES`); `--strict-markers` means use only registered markers — **spot-checked pyproject.toml:109 `--strict-markers`, :113 `unit`, :114 `integration`, :117 `slow` all registered**; new-file header template modeled on `test_turn_ledger_concurrency.py` (defect-class docstring, `from __future__ import annotations`, `import pytest`, `from superclaude...import`, `-> None` typed tests). Marker guidance: `@pytest.mark.unit` for M1/M2/M3/M4, `integration` for the optional resume-rerun. Correct.
- **Verification commands:** per-fix focused `uv run pytest ...`, regression sweep, full suite, AND the CLAUDE.md-mandated `uv run ruff format --check src/ tests/` (separate from `ruff check`). Matches the project's known "make lint ≠ CI ruff format" rule. UV-only, no `python -m pytest`. Complete.

### Q6 — MDTM template rules documented with the CORRECT template path? PASS

- **Path correctness:** research 03 §B explicitly flags that the requested `.claude/templates/workflow/02_mdtm_template_complex_task.md` does NOT exist in this worktree and that the canonical SoT is `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`. **Spot-checked: the `src/` file exists (85583 bytes); the `.claude/` mirror returns "No such file or directory" — exactly as documented.** This is the single most important "gotcha" for the builder and the research caught it.
- **Rules coverage:** A3 granular breakdown, A4 iterative 3-step structure, B2 6-element self-contained-item pattern, Section E checklist structure (flat `- [ ]`, no nesting), F1 loop + delegation/parallel-spawn rules, L1-L7 handoff patterns, I15-I16 phase-gate QA + fix-cycle limits, I17 post-completion validation, I18 testing requirement. Comprehensive and line-cited.

### Q7 — Granularity sufficient for per-fix checklist items (each fix + its test = its own item)? PASS

The research is partitioned so each fix maps to: (1) a source-edit item with exact file:line + diff
shape (from 01), and (2) a test item with a runnable seam + sketch + placement + marker (from 02),
plus M4's dedicated test file with 6 traced cases (from 03). Combined with the A3/A4 granular-breakdown
and B2 self-contained-item rules surfaced in 03 §B, a builder can emit one item per fix and one item
per test (4 fixes + their tests) without inventing or assuming any detail. Test placements are explicit
(M1 → append to test_executor.py; M2 → new test_poll_watchdog_ceiling.py; M3 → append to
test_handoff_store.py; M4 → new test_scheduler.py).

### Q8 — Unresolved ambiguities documented (not silently assumed)? PASS

Ambiguities are surfaced rather than buried:
- M1: `terminate()` vs `_close_handles()` choice presented with tradeoffs (terminate also reaps a live child on KeyboardInterrupt) — builder decision, not silently made.
- M2: ceiling-approach vs review's "always terminate after warning" alternative explicitly compared (the latter would convert `warn`→`kill` semantics); `getattr` fallback flagged for the duck-typed proc.
- M3: the valid-JSON-but-wrong-shape edge (top-level list → `AttributeError`/`TypeError` NOT caught by `(JSONDecodeError, ValueError)`) is explicitly called out as beyond the review's stated scope, with the broader-except option flagged as a deliberate-not-silent decision.
- M4: edge-direction convention ("A→B means B depends on A") stated up front; duplicate-task_id and unique-id caveats noted.

---

## Coverage Audit (scope → research)

| Scope item (from track goal) | Covered by | Status |
|---|---|---|
| `executor.py` M1 handle-leak fix point | 01 §M1 | COVERED |
| `executor.py` M2 watchdog-unbounded fix point | 01 §M2 | COVERED |
| `handoff.py` M3 corrupt-handoff-read fix point | 01 §M3 | COVERED |
| M1/M2/M3 unit-test seams | 02 §M1/§M2/§M3 | COVERED |
| New `tests/sprint/test_scheduler.py` (M4) | 03 §A | COVERED |
| Scheduler API surface | 03 §A.0-A.5 | COVERED |
| MDTM template build rules + correct path | 03 §B | COVERED |
| Verification commands (pytest + ruff format) | 02 "Verification commands" | COVERED |
| Base-class fix-safety contracts | 01 "Quick contract facts" + per-fix (c) | COVERED |

No scope item is uncovered.

## Evidence Quality

| Research file | Evidence character | Rating |
|---|---|---|
| 01-source-fix-points.md | Every claim has file:line; current code quoted verbatim; runtime confirmation of `JSONDecodeError ⊂ ValueError`; caller line-cited | Strong |
| 02-test-patterns-and-seams.md | Seams cite proven existing harnesses (test_executor.py:1904-1963); runnable sketches; marker/conftest facts line-cited | Strong |
| 03-scheduler-and-template.md | Every scheduler fn cited at scheduler.py:NN; 6 cases traced through the real algorithm; template path discrepancy verified | Strong |

## Documentation Staleness

No doc-sourced architectural claims requiring `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]`
tags — all three files are code-traced, not doc-derived. The MDTM-template content in 03 §B IS sourced
from the template `.md`, but the template is a build-instruction artifact (process spec), not a claim
about system architecture, and its path was independently verified. No staleness flags.

## Completeness

| Research file | Status | Summary | Gaps/Ambiguities surfaced | Key takeaways | Rating |
|---|---|---|---|---|---|
| 01 | Complete | Y (summary table) | Y (per-fix (d) Risk/regression) | Y | Complete |
| 02 | Complete | Y (seam summary table) | Y (guardrails per fix) | Y | Complete |
| 03 | Complete | Y (per-section) | Y (edge-direction, dup ids, scope edges) | Y | Complete |

## Contradictions Found

None between the three files. They are cleanly partitioned (01 = source fix points, 02 = test seams,
03 = scheduler API + template) and cross-reference each other consistently (02 cites "per Researcher 1"
fix sites that match 01 exactly).

## Compiled Gaps

### Critical Gaps (block tasklist build)
- None.

### Important Gaps (affect quality)
- None.

### Minor Notes (non-blocking; builder may carry as-is)
1. **Enum-name typo in 03 §A.6 "extra coverage":** the suggested `is_task_satisfied` coverage note writes "PASS_RECORDED→True", but the real enum is `PASS_RECOVERED` (models.py:50). The authoritative §A.4 uses the correct `PASS_RECOVERED`; only the informal extra-coverage bullet has the typo. **Spot-checked models.py:49-58.** Trivial — the builder should write the test against `TaskStatus.PASS_RECOVERED`. Not a blocking gap.
2. **M2 `<fallback>` value left to builder:** 01/02 recommend `getattr(proc, "timeout_seconds", <fallback>)` but leave the concrete fallback unspecified (a deliberate builder decision, correctly flagged as such). The builder should pick a concrete sane fallback (e.g. a large constant or `timeout * N`) and the M2 test's fake `proc` already supplies `timeout_seconds`, so the fallback path is exercised only by the optional missing-attr guard. Documented, not silently assumed — listed here only for builder visibility.

## Depth Assessment

**Expected depth:** Deep — fix-point identification with exact line spans, base-class contract
verification, traced test cases with exact I/O, and build-rule documentation.
**Actual depth achieved:** Deep. All fixes have verbatim current code + minimal diff shape +
contract proof + risk notes; all test seams have runnable sketches anchored to existing proven
harnesses; all 6 M4 cases are traced through the real wave algorithm; the template path gotcha was
caught and verified.
**Missing depth elements:** None.

## Recommendations

1. Proceed to MDTM tasklist build for M1-M4. The research is sufficient; no gap-fill round needed.
2. Builder: write the M4 scheduler `is_task_satisfied` coverage against `TaskStatus.PASS_RECOVERED` (not the typo'd "PASS_RECORDED" in 03 §A.6 extra-coverage).
3. Builder: choose a concrete M2 `timeout_seconds` getattr-fallback and reference `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (NOT the non-existent `.claude/` mirror) as the template.
4. Structure as one source-edit item + one test item per fix (M1, M2, M3) plus the M4 new-file item, per the A3/A4/B2 granular rules surfaced in 03 §B, with a phase-gate QA checkpoint (I15) before any consolidation phase.

---

VERDICT: PASS

No blocking gaps. All 8 spawn-prompt questions PASS with independently spot-checked evidence.
Two minor, non-blocking builder notes (enum typo in an informal coverage bullet; M2 fallback value
left as an explicit builder decision). Research is ready for tasklist generation.
