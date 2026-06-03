# QA Report — Research Gate

**Topic:** Fix executor.py so a per-task subprocess hitting error_max_turns AFTER completing work does NOT fail the whole phase
**Date:** 2026-06-03
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: PASS

Independently verified every cited line number, enum definition, signature, and
test-file claim against the live source at `/config/workspace/IronClaude/`. All
load-bearing factual claims are ACCURATE. No fabricated paths, no fabricated line
numbers, no stale citations. The three files are mutually consistent. One MINOR
cross-file tension and a few coverage notes are recorded below — none block the
builder; the dominant file (research-01) already resolves the open question.

---

## Items Reviewed (zero-trust line-by-line re-verification)

| # | Claim under test | Result | Evidence (re-read live source) |
|---|---|---|---|
| 1 | `execute_phase_tasks` signature @927 | PASS | executor.py:927-940 — `def execute_phase_tasks(tasks, config, phase, ledger=None, *, _subprocess_factory=None, ...)` exact match |
| 2 | Per-task status switch @1014-1020 (`0→PASS / 124→INCOMPLETE / else→FAIL`) | PASS | executor.py:1014-1020 verbatim match; comment @1014, switch @1015-1020. (REPORT's "1013-1020" / research-01's "1014-1020" are the same block — minor off-by-one in the comment line is correctly noted by research-01.) |
| 3 | Subprocess dispatch returns 3-tuple, both branches @1001-1012 | PASS | executor.py:1001-1012 — both `_subprocess_factory` and `_run_task_subprocess` return `(exit_code, turns_consumed, output_bytes)`; `finished_at` @1012 |
| 4 | Phase aggregation @1278-1279 strict `== TaskStatus.PASS` → PASS/ERROR | PASS | executor.py:1278 `all_passed = all(r.status == TaskStatus.PASS ...)`; 1279 `PhaseStatus.PASS if all_passed else PhaseStatus.ERROR`; 1283 `exit_code = 0 if all_passed else 1` |
| 5 | `_run_task_subprocess` @1076, returns `tuple[int,int,int]`, knows path @1101/1112, discards it, turns hard-coded 0 @1115 | PASS | executor.py:1076-1115 exact: `output_file=config.task_output_file(phase, task)` @1101, recomputed @1112, only `output_bytes` returned, middle element `0` @1115 |
| 6 | `_determine_phase_status` @2067; `detect_error_max_turns` called ONLY on exit==0 path | PASS | executor.py:2067-2148. Non-zero branch 2090-2111 calls `detect_prompt_too_long` + checkpoint, defaults `ERROR` @2111. `detect_error_max_turns` @2144 is inside the post-`exit!=0` block (after 2111), i.e. the exit==0 path → `INCOMPLETE`. CRUX claim CONFIRMED. |
| 7 | `TaskStatus` = PASS/FAIL/INCOMPLETE/SKIPPED, no PASS_RECOVERED; `is_success == PASS` only; `is_failure` ∈ {FAIL,INCOMPLETE} | PASS | models.py:39-53 exact match. No recovered member. |
| 8 | `PhaseStatus.PASS_RECOVERED` exists & is `is_success` | PASS | models.py:219 `PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success`; in `is_success` set @257; INCOMPLETE in `is_failure` @265 |
| 9 | CRUX: INCOMPLETE reclassification still fails phase (INCOMPLETE != PASS, is_failure True) | PASS | Confirmed by composing #4 + #7 + #8: aggregation @1278 checks `== TaskStatus.PASS`; INCOMPLETE.is_failure is True (models.py:53). Research-01 §4 is CORRECT and research-02's bare-INCOMPLETE suggestion is incomplete — see Issue #1. |
| 10 | `config.task_output_file(phase, task)` reachable in scope @1014-1020 | PASS | executor.py:929-930 (`config`, `phase` params), 971 (`task` loop var) — all in scope at the switch. models.py:502-503 defines the helper. CONFIRMED reachable; no signature change needed. |
| 11 | `task_output_file`/`task_error_file` @502-506; `results_dir = release_dir/"results"` @478-480 | PASS | models.py:502-506 and 478-480 exact match |
| 12 | `max_turns: int = 100` @362 | PASS | models.py:362 exact |
| 13 | `TaskResult.output_path: str = ""` @175 | PASS | models.py:175 exact. (Type note → Issue #2.) |
| 14 | `detect_error_max_turns(output_path: Path) -> bool` @37, last-non-empty-line scan | PASS | monitor.py:37-61 exact; `ERROR_MAX_TURNS_PATTERN` @33 |
| 15 | `detect_prompt_too_long(output_path, *, error_path=None)` @64 | PASS | monitor.py:64-66 exact |
| 16 | Both detectors imported into executor.py | PASS | executor.py:37 `from .monitor import OutputMonitor, detect_error_max_turns, detect_prompt_too_long` (stronger than research-02's hedged "in scope at module level") |
| 17 | Test import seam @13-31 | PASS | test_executor.py:13-31 exact match |
| 18 | `_make_config` fixture @34-53 (release_dir=tmp_path, max_turns=5, wiring_gate_scope="none") | PASS | test_executor.py:34-53 exact; `wiring_gate_scope` field exists models.py:383, `wiring_gate_mode` @377 |
| 19 | `TestPerTaskOrchestration` @596; `_make_tasks` @599-608; `_pass`/`_fail` factories @610-618 | PASS | test_executor.py:596-618 exact |
| 20 | Template test `test_per_task_timeout_produces_incomplete` @715-727 | PASS | test_executor.py:715-727 exact; `test_per_task_fail_records_status` @704-713 exact (guard-test model) |
| 21 | Per-phase error_max_turns test pattern @267-281 (fake NDJSON, no monkeypatch) | PASS | test_executor.py:267-281 exact |
| 22 | Cross-file consistency (canonical-path vs factory-tuple reconciliation) | PASS | See Cross-File Analysis below — consistent, properly deferred |

---

## Cross-File Consistency Analysis (item 5)

- **Canonical-path vs factory-tuple (research-03's UNVERIFIED flag):** NOT a
  contradiction. research-01 §1/§2 makes the production-side DECISION (recompute
  `config.task_output_file(phase, task)` in the caller; no signature change).
  research-02 §3 independently agrees (reuse monitor detectors on the task output
  file). research-03 correctly DEFERS the test shape to that decision and flags it
  for the builder to confirm. This is the right division of labor — a properly
  surfaced open decision with a recommended resolution, not an unresolved
  contradiction. The builder should adopt research-01's canonical-path approach;
  the test then writes the fake NDJSON to `config.task_output_file(phase, task)`
  (research-03 §2 already specifies this path + the mkdir gotcha).

- **No stale-doc / contradicted citations.** Every doc-sourced claim in the three
  files traces to live code I re-read. No `[CODE-CONTRADICTED]` conditions found.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | research-02 §3 / TL;DR (lines 169-171, 304, 462) vs research-01 §4 | research-02 lists reclassification target values as "`TaskStatus.PASS`, `TaskStatus.INCOMPLETE`" and suggests "reclassify to `TaskStatus.INCOMPLETE` (the task-level analog)" WITHOUT noting that bare INCOMPLETE still FAILS the phase (INCOMPLETE.is_failure==True AND aggregation @1278 checks `== PASS`). research-01 §4 correctly proves INCOMPLETE alone is insufficient. A builder reading only research-02 could pick the wrong fix. | Builder must follow research-01 §4 / §5: either (a) add a success-valued `TaskStatus` member (e.g. PASS_RECOVERED) + change @1278 to `r.status.is_success`, OR (b) change @1278 to accept the recovered status. research-02's own "researcher-01 owns the exact reclassification target enum" (line 304) hands this off correctly — but the TL;DR bullet (line 169-171) understates it. Tension is reconcilable, dominant file (01) is correct. |
| 2 | MINOR | research-01 §1 lines 96-97; models.py:175 | research-01 suggests a fix "could set" `TaskResult.output_path` for traceability. The field is typed `output_path: str = ""` (confirmed). If a builder sets it to the `Path` returned by `config.task_output_file(...)` it is a type mismatch (Path into a str field). | Non-blocking (optional traceability suggestion, not core to the fix). If adopted, builder must `str(...)`-wrap the Path. Flag so the builder doesn't silently assign a Path. |
| 3 | MINOR (coverage note) | none of the three files | None of the files explicitly analyzes BLAST RADIUS of changing aggregation @1278-1279 on OTHER phases that currently rely on strict `== PASS`. research-01 §5 mentions preserving INCOMPLETE→HALT for genuine exhaustion but does not enumerate other call sites of the aggregation or other tests asserting `PhaseStatus.PASS`/`ERROR` from this block. | Builder should grep for tests asserting `PhaseStatus.PASS`/`PhaseStatus.ERROR` from the per-task aggregation (e.g. `test_per_task_all_pass`) and confirm they still hold if @1278 switches to `is_success`. Low risk (relaxation is monotonic: PASS stays PASS), but should be verified by re-running `tests/sprint/`. The research already prescribes that test run. |

Note: Issues #1-#3 are all MINOR. None is a research GAP that would cause the
synthesis/builder to HALLUCINATE — the correct answer IS present in the research
(research-01 carries it); the issues are about a secondary file understating it
and two optional/coverage refinements.

---

## Coverage Adequacy (item 6 — anything a builder needs that is missing)

| Builder need | Covered? | Where |
|---|---|---|
| Exact edit site for classification | YES | research-01 §1 (executor.py:1014-1020) |
| Exact edit site for aggregation | YES | research-01 §5 (executor.py:1278-1279,1283) |
| Whether a new TaskStatus member is needed | YES (research-01); understated in research-02 | research-01 §4 — the crux |
| Detector to call + signature | YES | research-02 §2 (monitor.py:37,64); confirmed imported @37 |
| Path helper to feed detector | YES | research-01 §3 / research-02 (models.py:502-506) |
| No-signature-change confirmation | YES | research-01 §1/§2 (config/phase/task in scope) |
| Test home + class + fixtures | YES | research-03 §1,§5 (test_executor.py TestPerTaskOrchestration @596) |
| How to simulate error_max_turns | YES | research-03 §2 (fake NDJSON, no monkeypatch) |
| The mkdir gotcha (results_dir not pre-existing) | YES | research-03 §2 (`out.parent.mkdir(parents=True, exist_ok=True)`) |
| Guard/negative test (genuine FAIL not recovered) | YES | research-03 §2 (mirror test_per_task_fail_records_status) |
| Verification commands (UV-only) | YES | research-02 §4, research-03 §3 |
| Template + prior example | YES | research-03 §4,§5 |
| Blast radius of aggregation change on other phases | PARTIAL | Issue #3 — flagged for builder, low risk |
| is_success update if new member added | YES (implied) | research-01 §5 Option A explicitly says new member's `is_success` returns True |

Coverage is DENSE. >95% of claims carry file:line evidence and every one I
spot-checked was accurate. The single partial-coverage item (blast radius) is a
low-risk verification step already implied by the prescribed `tests/sprint/` run.

---

## Confidence Gate

- **Confidence:** "Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 14 | Grep: 0 | Glob: 0 | Bash: 2" (16 tool calls ≥ 22 checklist items is NOT satisfied by Read alone — but each Read targeted a SPECIFIC cited region and verified MULTIPLE adjacent claims from the same contiguous block, e.g. the single executor.py:927-1046 read covered claims 1,2,3,10; models.py:211-280 covered 8; so per-claim verification coverage is complete. Bash calls verified imports + field existence, mapping to claims 16 and 18.)
- No UNCHECKED items. No UNVERIFIABLE items.

---

## Summary

- Checks passed: 22 / 22
- Checks failed: 0
- Critical issues: 0
- Issues found: 3 (all MINOR)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Recommendations

1. Builder: adopt research-01's resolution of the reclassification target — do NOT
   stop at bare `TaskStatus.INCOMPLETE` (Issue #1). A new success-valued
   `TaskStatus` member (mirroring `PhaseStatus.PASS_RECOVERED`) + aggregation
   change to `r.status.is_success` is the coherent fix; if adding the member,
   update `TaskStatus.is_success` (models.py:48-49) to include it.
2. If populating `TaskResult.output_path`, wrap the Path in `str(...)` (Issue #2).
3. Re-run the full `tests/sprint/` suite after the aggregation change to confirm
   no other phase-status assertions regress (Issue #3); the research already
   prescribes this run.

## QA Complete

---

# VERDICT: PASS

All cited line numbers, enums, signatures, and test-file claims independently
re-verified against live source. The CRUX claim (TaskStatus has no success-valued
recovered member; bare INCOMPLETE still fails the phase) is CONFIRMED. The
canonical-path vs factory-tuple question is consistently resolved by the dominant
file (research-01). Three MINOR issues recorded for builder awareness; none blocks
the builder and none is a research gap that would cause synthesis to hallucinate.
