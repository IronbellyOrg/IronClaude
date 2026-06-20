# QA Report — task-qualitative (MERGED: partition 1 + partition 2)

**Topic:** MDTM tasklist — Sprint CLI per-task execution + handoff (Stages 0–3)
**Date:** 2026-06-03
**Phase:** task-qualitative
**Partitions:** P1 = Phases 1-3 (rf-qa-qualitative agent); P2 = Phases 4-6 (orchestrator inline after 2 subagent API crashes); plus cross-phase merge.

---

## Overall Verdict: PASS (1 CRITICAL found + fixed in-place; 0 unfixable)

The tasklist is operationally executable. One CRITICAL self-contradiction was caught and fixed during review; all other operational pressure-tests pass.

## Partition 1 (Phases 1-3) — rf-qa-qualitative agent → FAIL→FIXED

Full detail: `qa-qualitative-review-p1.md`.

- **CRITICAL (FIXED in-place):** Step 2.1 added `scope: str=""` to `setup_isolation`, but `tests/cli/eval/test_isolation_layers_probe.py::test_setup_isolation_signature_pin` hard-asserts `tuple(params.keys()) == ("config",)` — Stage 0 would have failed at its first gate (the probe runs in PG0.1/PG0.2/2.11) with no remediation in the plan. Fix appended to Step 2.1: re-pin the probe to `("config","scope")` (scope KEYWORD_ONLY, default "") in the SAME edit, IsolationLayers field-order assertions untouched. (Verified present in task file Step 2.1.)
- Signature-widening ripple: `execute_phase_tasks` call site is all-keyword; `_run_task_subprocess` callers = prod@1009 + 1 test — new trailing/keyword params are safe. No broken call site.
- Turn-count: confirmed NO `num_turns` parser exists in src/ — Step 2.6's grep-first "reuse if found" premise is honest; Step 2.10 must edit `fake_claude.py` (MINOR — implied not named).
- Path A/B isolation edit correct-direction; HandoffRecord-before-store ordering correct; write_task_complete no ledger fork; handoff=off legacy-exact. 3 MINOR (gate_outcome dict|None under-spec, unnamed shim edit, empty output_path) — faithful spec relays, non-blocking.

## Partition 2 (Phases 4-6) — orchestrator inline review → PASS

(Two rf-qa-qualitative subagents crashed on transient API/network errors mid-run — `Unexpected end of JSON input` and `connection timed out` — after extensive reads but before writing findings/edits; task file confirmed un-corrupted. Phases 4-6 reviewed inline against live source + the task items.)

Pressure-tests (all PASS):
1. **_jsonl-lock-BEFORE-parallelism (CRITICAL ordering):** Step 5.2 (lock `_jsonl`) and 5.3/5.4 (TurnLedger lock + atomic `try_launch`) are sequenced BEFORE Step 5.7 (wire K>1 concurrent execution) and Step 5.8 (race test). Concurrent writers cannot reach a lock-free `_jsonl`. CORRECT.
2. **Race test exercises real concurrency:** Step 5.8 spins ≥4 threads calling the guarded `_jsonl` directly in a tight loop (≥1000 writes), independent of executor-loop parallelism; asserts line-count + per-line parse + payload multiset; designed to FAIL unguarded / PASS locked. Valid.
3. **Resume skip predicate = validated success:** Step 4.1 `is_validated_success` ANDs `status==PASS` with gate-success; Step 4.2 places the skip at loop-top BEFORE `can_launch`/debit (no budget debit for skipped); Step 4.6 tests every non-success state (FAIL_TERMINAL/FAIL_RECOVERABLE/INCOMPLETE/SKIPPED + PASS-gate-fail) is NOT skipped. Correct.
4. **walk_dependencies reuse + topo wrapper:** Step 5.5 reuses `_dependencies_of` edge primitive (no fresh parser), explicitly adds a topological/closure wrapper noting the existing walk is single-level, with cycle detection surfaced. Correct.
5. **TurnLedger TOCTOU:** Step 5.3 adds atomic `try_launch` (check+debit under one lock); 5.4 switches the gate; 5.9 asserts exactly-N succeed under thread stress. Correct.
6. **Back-compat:** Step 4.5/4.8 — missing `handoff/` degrades to phase-granular with no error, lazy-create on write only; Step 5.7 keeps the `task_parallelism==1` path byte-identical (with a logged escape hatch if K>1 refactor is unsafe); `test_backward_compat_regression.py` is in the Stage-2 (4.9) and Stage-3 (5.12) validation runs. Correct.

MINOR (non-blocking, shared with P1): Step 4.1 defers `gate_outcome is None` handling to "the documented decision" — acceptable (item flags it; impl picks None→success-or-not with a test).

## Cross-phase merge (orchestrator)

- Signature-widening ripple (Phase 3 origin) × call sites (all phases): verified safe by P1.
- _jsonl writer (added Stage 0/1) → lock (Stage 3 Step 5.2): the M2 ordering dependency is honored — Stages 0-2 rely on the documented sequential single-writer invariant; Step 5.2 explicitly covers `write_task_complete` + `write_task_rerun_complete`.
- Probe (T02.05) kept green across 2.1(fixed)/2.11/PG0.2/5.12; T02.06 superseded by 2.7 (not duplicated).

## Self-Audit (INV-019)

Relied on rf-qa A.10 PASS for: frontmatter/template_schema_doc, item 5-field shape, TB-Add-1..8 structural gates, item-DAG acyclicity. Where A.10 PASS was INSUFFICIENT and own tool work was required: A.10 verified Step 2.1 changes `setup_isolation`'s signature as structurally well-formed, but only the qualitative pass (reading `test_isolation_layers_probe.py`'s actual assertion) revealed the signature change CONTRADICTS the frozen probe — a runtime-execution failure invisible to structural validation. That is the CRITICAL this gate exists to catch.

## VERDICT: PASS
