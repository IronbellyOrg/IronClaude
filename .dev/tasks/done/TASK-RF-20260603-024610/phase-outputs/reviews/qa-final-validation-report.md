# QA Report — Report-Validation (rf-qa STRUCTURAL, CROSS-PHASE)

**Topic:** Wire the Sprint CLI per-task execution path + runner-owned typed HandoffRecord (Stages 0-3 + RC)
**Task:** TASK-RF-SPRINTCLI-WIRE-DEAD-20260603-024610
**Date:** 2026-06-03
**Phase:** report-validation (cross-phase consistency)
**Fix cycle:** N/A
**Stance:** Adversarial. Verified against actual on-disk source/tests (zero-trust).

---

## Overall Verdict: PASS

All four cross-phase consistency dimensions verified against actual on-disk source/tests.
Producer→consumer wirings are signature- and field-consistent across phases; all "ensuring"
clauses spot-checked are satisfied; zero missing outputs; the no-regression claim is
independently confirmed byte-identical to the Phase-1 baseline; `make lint` is green.
One MINOR observation (a spec-mandated-but-uncalled scheduler helper) is recorded — NOT a defect
and NOT fixed (deleting a spec-required deliverable or speculatively wiring it would violate
scope discipline). No fixes were required.

---

## No-Regression Re-Verification (independent)

**Command:** `uv run pytest tests/sprint/ tests/cli/eval/test_isolation_layers_probe.py tests/integration/test_sprint_wiring.py -q`
**Result:** `54 failed, 1075 passed, 20 warnings` (failures expected per baseline).

**Set-diff vs Phase-1 baseline (`pre-change-baseline.md`, 54 failing node-ids):**

- Fresh failing count: **54** — Baseline failing count: **54**
- `comm -23` (fresh NOT in baseline / NEW regressions): **EMPTY**
- `comm -13` (baseline NOT in fresh / changed): **EMPTY**
- Symmetric diff empty BOTH directions → **ZERO regressions, ZERO new failures.**

**Lint:** `make lint` (`uv run ruff check .`) → **All checks passed!** (GREEN).
Per spawn instructions, ruff-FORMAT version skew (local 0.15.14 vs CI) is environmental and NOT a validation failure — `ruff check` is the bar and is green. No blanket `ruff format` introduced.

**Passed count 1039 (baseline) → 1075 (now):** +36 net, consistent with the new Stage-0..3 + RC + qualitative-gate test additions all passing. No baseline-passing test flipped to fail.

**Verdict on no-regression:** CONFIRMED — failing node-id set is byte-identical to baseline.

---

## 1. Cross-Phase Producer→Consumer Wirings (signatures + field names)

Every chain verified by reading the actual `def` and its call site(s), not by trusting the gate verdicts.

| # | Producer (phase) | Consumer (phase) | Verification | Result |
|---|------------------|------------------|--------------|--------|
| 1 | `setup_isolation(config, *, scope="")` — `executor.py:172` (Stage 0) | `_task_env(task,config,phase)` `executor.py:1368` → returns `setup_isolation(...).env_vars`; consumed by Path B `_Base(env_vars=_task_env(...))` `executor.py:1494` + `_env_capture` seam at `:1115` (parallel) and `:1310` (sequential) | kwarg-only `scope` default `""` preserves K=1/Path-A serial behavior; both env-capture sites call the same helper | PASS |
| 2 | `HandoffRecord.from_task_result(result, *, phase, produced_artifacts, consumed_upstreams)` — `models.py:348` (Stage 1) | Call sites `executor.py:1137` (parallel `_run_one_task`) + `executor.py:1349` (sequential) | Both call sites pass positional `result` + the 3 keyword fields verbatim — signature match exact | PASS |
| 3 | `FileHandoffStore.write/read(*, phase, task)` — `handoff.py:49/62` (Stage 1) | `handoff_store.write(record, phase=phase, task=task)` `:1143/:1355`; `handoff_store.read(phase=phase, task=task)` in resume skip `:1085/:1259` | kwargs match; `read` returns `HandoffRecord \| None` consumed by `is_validated_success` | PASS |
| 4 | `SprintLogger.write_task_complete(phase,task_id,status,turns,duration_sec)` — `logging_.py:226` (Stage 1) | Call site `executor.py:1129` passes `(phase.number, task.task_id, result.status.value, result.turns_consumed, result.duration_seconds)` | 5 positional args align; `result.duration_seconds` is a real `@property` (`models.py:238`) | PASS |
| 5 | `write_task_complete` → `self._jsonl(...)` `logging_.py:239` (Stage 1) | Stage-3 locked `_jsonl` — `logging_.py:295-300` acquires `self._jsonl_lock` (`threading.Lock()` `:31`) | The Stage-1 writer routes through the Stage-3 lock — concurrency-safe under K>1 | PASS |
| 6 | `SprintConfig.handoff_file(phase,task)` — `models.py:694` (Stage 1) | Resume skip-check + handoff write key `handoff/phase-{N}-task-{id}.json` | phase-qualified key (H5 item 2) mirrors `task_output_file` builder | PASS |
| 7 | `is_validated_success(record)` — `handoff.py:23` (Stage 2) | Resume skip-check `executor.py:1086` (parallel) + `:1260` (sequential), gated on `config.resume_task_id` and `handoff/` dir existence | reads Stage-1 `HandoffRecord`; ANDs `status==PASS` + `GateOutcome(...).is_success`; no None branch (H4 schema fix honored) | PASS |
| 8 | Resume skip records `TaskResult(status=PASS, gate_outcome=GateOutcome.PASS)` — `executor.py:1264` (Stage 2) | `aggregate_task_results` counts `tasks_passed += (status==PASS)` `executor.py:354`; `AggregatedPhaseReport.status` returns `"PASS"` iff `tasks_passed==tasks_total` `:248` | A fully-resumed phase aggregates to PASS — the resume-skip-as-PASS decision is consistent with RC.1 aggregation (a SKIPPED status would mis-report FAIL). Operationally REQUIRED, verified from source. | PASS |
| 9 | `aggregate_task_results(phase_number, task_results, remaining_task_ids=None, budget_remaining=0)` — `executor.py:327` (RC.1) | Call site `executor.py:1713` passes `phase.number` positional-first + `remaining_task_ids=remaining` (NO `phase=` kwarg); consumer reads `phase_report.status == "PASS"` `:1716` | Signature/call-site exact (RC.1's explicit "positional-first, no `phase=`" constraint honored). `.status` is `str` not enum → `== "PASS"` type-correct. Formerly-dead aggregator now live. | PASS |
| 10 | `topological_launch_order(tasks)` + `CycleError` — `scheduler.py:74/27` (Stage 3) | `executor.py:52` import; `:1063` `waves = topological_launch_order(tasks)` in `_execute_phase_tasks_parallel` | scheduler consumed live; `dependencies_of` mirrors `rerun_tasks._dependencies_of` (H6 reuse, not re-derive) | PASS |
| 11 | `TurnLedger.try_launch(allocation=None)` atomic — `models.py:947` (Stage 3) | budget gate `executor.py:1282` `if ledger is not None and not ledger.try_launch():` | replaces the `can_launch()`-then-`debit()` TOCTOU; RLock-reentrant; K=1 math identical | PASS |
| 12 | `count_turns_from_stream_json(output_path)` — `process.py:32` (Stage 0) | `executor.py:1510` `turns = max(count_turns_from_stream_json(output_path), 0)` in `_run_task_subprocess` | replaces hard-coded `turns_consumed=0`; `output_path` is the same `task_output_file` | PASS |
| 13 | `_poll_with_stall_watchdog(proc,config,...)` — `executor.py:1384` (RC.2) | `executor.py:1500` inside `_run_task_subprocess` (per-task wait) → one independent timer per worker slot (RC.3 by construction) | per-task path no longer stall-blind; function-local timer state = per-worker isolation | PASS |

**Three-layer flag plumbing (M4) — click → load_sprint_config → SprintConfig, defaults agree:**

| Flag | click dest / default (`commands.py`) | `load_sprint_config` kwarg / default (`config.py`) | `SprintConfig` field / default (`models.py`) |
|------|--------------------------------------|----------------------------------------------------|----------------------------------------------|
| `--handoff/--no-handoff` | `handoff_enabled` / `True` (`:191-194`) | `handoff_enabled=True` (`:295`) → forwarded `:366` | `handoff_enabled: bool = True` (`:574`) |
| `--resume` | `resume_task_id` / `""` (`:197-200`) | `resume_task_id=""` (`:296`) → forwarded `:367` | `resume_task_id: str = ""` (`:581`) |
| `--task-parallelism` | `task_parallelism` / `1` (`:202-208`) | `task_parallelism=1` (`:297`) → forwarded `:368` | `task_parallelism: int = 1` (`:585`) |

All three flags' defaults agree across all three layers. K=1 / handoff-on / resume-off defaults preserve legacy behavior.

**Conclusion (Dimension 1):** No signature, field-name, or default mismatch found across any cross-phase chain. PASS.

## 2. "Ensuring..." Acceptance Clauses (spot-checked across ALL phases)

| Clause (phase) | Verification | Result |
|----------------|--------------|--------|
| Stage 0: IsolationLayers 4-field order unchanged, probe green | `test_isolation_layers_probe.py` → **13 passed**; field order `scoped_work_dir, git_boundary, plugin_dir, settings_dir` intact (`executor.py:129+`) | PASS |
| Stage 0: Path A KEEPS phase-scoped `CLAUDE_WORK_DIR`, ADDS only settings/plugin keys | Verified in qualitative verdict + source (`executor.py` Path-A merge); probe + smoke tests green | PASS |
| Stage 0: `turns_consumed` is real parse (no hard-coded 0) | `executor.py:1510` consumes `count_turns_from_stream_json`; exact-count e2e test present | PASS |
| Stage 1: `HandoffRecord` H4-verbatim, `gate_outcome` = enum `.value` str (NOT dict/None) | `models.py:272+`, `from_task_result` derives `result.gate_outcome.value` (`:369`) | PASS |
| Stage 1: `FileHandoffStore` atomic temp+replace, `read(missing)→None` | `handoff.py` write/read; `test_handoff_store.py` (no `.tmp` left behind) green | PASS |
| Stage 1: `write_task_complete` mirrors `task_rerun_complete` field set/order | `logging_.py:226-249` identical field set `event,phase,task_id,status,turns,duration_sec,timestamp` | PASS |
| Stage 1: `build_task_context` reaches the per-task prompt | qualitative verdict cap #3; `test_stage1_wiring.py` asserts context string in prompt — green | PASS |
| Stage 1: M6 probe warn-only, `_TASK_HEADING_RE` NOT widened | `config.py:386` regex unchanged; M6 probe is a separate regex in executor (comment `:63`) | PASS |
| Stage 1: `--handoff=off` legacy-exact (no records, no events) | store + logger both gated on `handoff_enabled`; `test_handoff_backward_compat.py` green | PASS |
| Stage 2: skip predicate ANDs PASS + gate-success; no skip on any non-success state | `is_validated_success` `handoff.py:23`; `test_resume_contract.py` per-state — green | PASS |
| Stage 2: resume skip happens BEFORE budget debit | skip block `:1260-1273` precedes `try_launch` gate `:1282` | PASS |
| Stage 2: missing `handoff/` dir degrades to phase-granular, no error | skip-check guarded on `(results_dir/"handoff").exists()` `:1257`; back-compat test green | PASS |
| Stage 2: crash-consistency — handoff file (not JSONL) authoritative | `test_handoff_crash_consistency.py` green | PASS |
| Stage 3: `_jsonl` lock covers `write_task_complete` | `logging_.py:295-300` lock acquired; writer at `:239` routes through it | PASS |
| Stage 3: `TurnLedger` lock excluded from serialization; `try_launch` atomic | `_lock` non-field attr in `__post_init__` (`:923`); excluded from `__eq__`/asdict | PASS |
| Stage 3: K=1 byte-identical (dispatch guard) | guard requires `task_parallelism>1 AND len(tasks)>1` (`:1222`); else sequential path | PASS |
| Stage 3: DAG scheduler REUSES `_dependencies_of` shape, cycles surfaced | `scheduler.dependencies_of` mirrors `rerun_tasks._dependencies_of`; `CycleError` raised not silent | PASS |
| RC.1: `aggregate_task_results` now has a live caller; counts reflect remaining | call site `:1713` live; `remaining_task_ids` counted into `tasks_total` → non-PASS when budget left tasks | PASS |
| RC.4: `_write_preliminary_result` true `O_EXCL` (not exists-check TOCTOU) | `os.open(O_CREAT\|O_EXCL\|O_WRONLY)` `executor.py:2500`; `FileExistsError`→preserve | PASS |
| L5 docs: all 3 flags + `task_complete` + `handoff/` key documented | CHANGELOG.md + docs/sprint-cli-deep-dive.md both cover `--handoff`/`--resume`/`--task-parallelism`/`task_complete`/`phase-{N}-task` | PASS |

**Conclusion (Dimension 2):** All spot-checked "ensuring" clauses across Stages 0–3 + RC + Post-Completion-relevant L5 are satisfied. PASS.

## 3. Orphaned / Missing Outputs

**Missing outputs:** NONE among executed phases. All checklist-named artifacts verified present via filesystem check:
- Discovery: `symbol-anchors.md`, `shared-state-inventory.md` ✓
- Test summaries + raw: `stage0..3-tests.{md,txt}`, `rc-tests.{md,txt}` ✓
- Gate inputs + verdicts: `stage0..3-gate-{input,verdict}.md` ✓
- Reports: `final-quality-report.md`, `final-qualitative-verdict.md`, `stage4-teardown-checklist.md` ✓
- New source modules: `handoff.py`, `scheduler.py` ✓
- All 13 new test files under `tests/sprint/` + `tests/sprint/e2e_real/` ✓ (collected + passing, 27/27 on the new-file subset, NOT skipped)

**`final-verification.md` (Post-Completion item 2 output): absent — but legitimately so.** The 4 Post-Completion items are still `- [ ]` (status `🟠 Doing`, `completion_date: ""`). This rf-qa final-validation gate runs as part of / immediately before Post-Completion; `final-verification.md` is produced by Post-Completion item 2, which is gated on this verdict and has not yet executed. This is pending downstream work, NOT a missing output of an executed phase. The task is correctly NOT marked Done.

**Orphaned outputs:** ONE MINOR. `scheduler.is_task_satisfied` (`scheduler.py:109`) is defined but has zero live callers in `src/` or `tests/`. Step 5.5 explicitly required building "a completion oracle mirroring `_is_satisfied`" as part of the scheduler-module deliverable, so its existence satisfies the literal item; the live parallel path drives waves purely from `topological_launch_order` (which uses `dependencies_of`). Classification: spec-mandated public helper, not wired live. NOT a producer→consumer break, NOT fixed (removing a spec-required deliverable or speculatively wiring it would violate scope discipline). Recorded as a MINOR observation for the maintainer.

**Conclusion (Dimension 3):** Zero missing outputs in executed phases; one MINOR spec-mandated-but-uncalled helper. PASS.

## 4. Source/Test Integrity

- All 8 sprint modules import cleanly (`executor, process, models, logging_, handoff, scheduler, commands, config`) — verified by `importlib.import_module`. ✓
- Cross-cutting signatures agree: `execute_phase_tasks` params threaded from call site; `_run_one_task`/`_execute_phase_tasks_parallel` present (full K>1, not a logged gap); `load_sprint_config` kwargs ↔ `SprintConfig` fields ↔ click options all aligned (table in Dimension 1). ✓
- New modules consumed live (`FileHandoffStore`/`is_validated_success` imported `executor.py:26`; `topological_launch_order`/`CycleError` imported `:52`). ✓

**Conclusion (Dimension 4):** PASS.

---

## Items Reviewed (Confidence Gate)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Producer→consumer signatures/fields (13 chains) | [x] PASS | Read each def + call site (Dimension 1 table) |
| 2 | Three-layer flag plumbing defaults agree | [x] PASS | grep all 3 layers for 3 flags (defaults True/""/1) |
| 3 | "Ensuring" clauses across all phases (20 clauses) | [x] PASS | Read source + ran probe/subset tests (Dimension 2) |
| 4 | Missing outputs | [x] PASS | filesystem check of every checklist-named artifact |
| 5 | Orphaned outputs | [x] PASS (1 MINOR) | grep callers of scheduler/handoff exports |
| 6 | Modules import cleanly | [x] PASS | `importlib.import_module` on 8 modules |
| 7 | No-regression node-id set == baseline 54 | [x] PASS | `comm` set-diff empty both directions |
| 8 | `make lint` green | [x] PASS | `ruff check .` All checks passed |
| 9 | New test files collected + passing (not skipped) | [x] PASS | 27/27 on new-file subset; full suite 1075 passed |
| 10 | Frontmatter/Post-Completion state consistent | [x] PASS | status `🟠 Doing`, 4 Post-Completion items pending (correct — gated on this verdict) |

## Summary
- Checks passed: 10 / 10 (1 with a MINOR non-blocking observation)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `src/superclaude/cli/sprint/scheduler.py:109` | `is_task_satisfied` defined but uncalled in src/ + tests | NONE — spec-mandated deliverable (Step 5.5 "completion oracle"); deleting or speculatively wiring it would violate scope. Maintainer may wire or prune in a future cleanup. |

## Actions Taken
None. No cross-phase inconsistency, broken wiring, unmet "ensuring" clause, or missing output was found that required a fix. The K=1 path was not touched (and was verified byte-identical via the dispatch guard + green K=1 tests).

## Recommendations
- Proceed to Post-Completion: the executor may now run the 4 pending Post-Completion items (produce `final-verification.md`, write the Task Summary, and flip status to `🟢 Done`), since this gate's no-regression + qualitative PASS preconditions are met.
- Optional future cleanup: wire or prune `scheduler.is_task_satisfied` (MINOR).
- Before pushing: honor the existing High follow-up (ruff-FORMAT CI-version parity) — do NOT blanket-reformat with local 0.15.14.

## Confidence
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep/Bash: 16 | Glob: 0 (No web research required — review was local source/test bound; Tavily-first N/A.)

## QA Complete
