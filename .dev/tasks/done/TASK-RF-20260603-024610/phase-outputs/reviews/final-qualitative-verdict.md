# rf-qa-qualitative OPERATIONAL Verdict — TASK-RF-20260603-024610 (Sprint CLI per-task wiring)

**Verdict:** **PASS**
**Phase:** task-qualitative (OPERATIONAL, executed task)
**Date:** 2026-06-03
**Stance:** Adversarial. Evaluated against ACTUAL on-disk outputs vs SYNTHESIS §6 (H1–H6) + §7 (M2–M7, L2–L5).
**fix_authorization:** true — **1 fix applied** (test-coverage gap for capability #2), re-verified.

PASS is issued AFTER fixing one real operational gap (missing turn-count acceptance test,
which §6 Reconciliation note explicitly requires). The six target capabilities are all
operationally coherent end-to-end on disk; the failing-test set is provably baseline-identical
(zero regressions, independently recomputed); `make lint` is green.

---

## Operational-coherence statement — the 6 target capabilities

| # | Capability | Coherent? | Load-bearing evidence (verified on disk) |
|---|-----------|-----------|------------------------------------------|
| 1 | Per-subprocess isolation (own `CLAUDE_SETTINGS_DIR`) | **YES** | Path B: `_run_task_subprocess` injects `_task_env(task,...)` = `setup_isolation(config, scope=f"task-{task.task_id}").env_vars` (executor.py:1381,1494) → each task gets its OWN `settings/<task-id>` + `plugins/<task-id>` (executor.py:202-206). Path A (H1 merge) KEEPs phase-scoped `CLAUDE_WORK_DIR` and ADDs only settings/plugin keys, deliberately NOT clobbering with setup_isolation's release-dir work-dir (executor.py:1768-1773) — matches §6 H1 table verbatim. |
| 2 | Turn count from real stream-json | **YES (test gap fixed)** | `count_turns_from_stream_json` (process.py:32-76) parses terminal `{"type":"result"}` event's `num_turns`, last-result-wins, rejects bool, tolerates malformed lines, 0 on missing/absent. Wired at `_run_task_subprocess` (`turns = max(count_turns_from_stream_json(output_path), 0)`, executor.py:1510) — supersedes the hard-coded-0. **Gap found+fixed:** zero direct acceptance test existed (only a fixture reference). Added `TestCountTurnsFromStreamJson` (7 cases incl. exact-count, last-wins, bool-reject) per §6 Reconciliation note ("assert the CORRECT turn count, not merely != 0"). |
| 3 | Prior-task context injected into prompt | **YES** | `build_task_context(results,...)` rendered in the PARENT (executor.py:1315 sequential / :1156 parallel per wave) and threaded as `prior_context` → appended to the single-task directive in `_run_task_subprocess` (process.py:1472-1473). Progressive compression beyond 3 prior tasks (process.py:338, compress_context_summary). |
| 4 | `task_complete` event + typed `HandoffRecord` | **YES** | `SprintLogger.write_task_complete` emits `event:"task_complete"` with field set IDENTICAL to the pre-existing `task_rerun_complete` (logging_.py:226-249) — H3 side-by-side discriminator honored. `HandoffRecord` (models.py:272-301) is H4-verbatim (12 fields, same order, `gate_outcome` = enum `.value` str). `FileHandoffStore.write` = atomic temp+replace (handoff.py:56-60). Both gated by `handoff_enabled` (executor.py:1340-1355 / 1128-1143). |
| 5 | Resume skips ONLY validated-success (recorded so downstream sees satisfied) | **YES** | Skip predicate `is_validated_success` = `status==PASS AND GateOutcome(gate_outcome).is_success` (handoff.py:23-40) — H5 item 1. Skipped task recorded as **PASS** (not SKIPPED) with the prior record's `output_path` (executor.py:1260-1273 / 1086-1100). **This is operationally REQUIRED:** `TaskStatus.is_success == (self==PASS)` (models.py:56-57) and `AggregatedPhaseReport.status` needs `tasks_passed==tasks_total` for PASS (executor.py:244-252) — a SKIPPED record would zero `tasks_passed` and mis-report a fully-resumed phase as FAIL. Key is phase-qualified `handoff/phase-{N}-task-{id}.json` (models.py:694-700) — H5 item 2. Back-compat: NO `handoff/` dir ⇒ no skipping, degrades to phase-granular (executor.py:1254-1257). |
| 6 | Concurrency-safe under K>1 | **YES** | `_jsonl` lock (logging_.py:31,295-301) covers `write_task_complete`; `TurnLedger.try_launch` atomic check-and-debit under RLock (models.py:947-962) — collapses the TOCTOU; DAG waves via `topological_launch_order` (scheduler.py:74-106, cycle-safe); per-worker independent stall timers (`_poll_with_stall_watchdog`, executor.py:1500, RC.3); handoff writes target distinct per-task files. Wall-clock win real: SPAWN runs UNLOCKED (`_run_one_task`, the slow part), only reconcile/hooks/TUI serialized under `lock` (executor.py:999-1027). K=1 byte-identical: dispatch guard `task_parallelism>1 AND len(tasks)>1` (executor.py:1222); sequential calls `_run_one_task(lock=None)`→`nullcontext` (executor.py:999,1329). |

---

## Items Reviewed (15-item task-qualitative checklist, OPERATIONAL)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Gate/command dry-run | PASS | `make lint` GREEN (ruff check). `uv run pytest tests/sprint/` runs; per-task wiring tests (36) + new turn tests (7) green. |
| 2 | Project-convention compliance | PASS | CLI source under `src/superclaude/cli/sprint/` — sync-dev/verify-sync correctly N/A (not skills/agents). Bar = `make lint`+pytest, met. No `.claude/` staging implied. |
| 3 | Intra-phase execution-order sim | PASS | Sequential loop: resume-skip→budget-gate(try_launch)→env-capture→context→`_run_one_task`→journal/handoff→TUI; each step's inputs produced by prior steps. Parallel: waves emit deps-first; prior-wave results feed `build_task_context`. |
| 4 | Function-signature verification | PASS | `HandoffRecord.from_task_result(result,*,phase,produced_artifacts,consumed_upstreams)` matches call site (executor.py:1349-1354). `write_task_complete(phase,task_id,status,turns,duration_sec)` matches (executor.py:1341-1347). `_task_env(task,config,phase)` matches both call sites. `setup_isolation(config,*,scope="")` matches all 3 callers. |
| 5 | Module-context analysis | PASS | `TurnLedger._lock` created in `__post_init__` as NON-field attr → excluded from dataclass `__eq__`/`asdict`; RLock allows `try_launch`→`debit` reentry. `_jsonl_lock` created once per logger, covers every `_jsonl` route. `IsolationLayers.env_vars` 4-key contract consumed correctly per-path. |
| 6 | Downstream-consumer analysis | PASS | New `task_complete` consumed by log analysis (sibling of `task_rerun_complete`). `HandoffRecord` consumed by `is_validated_success` on resume + aggregation. Resume-skip PASS record consumed by `AggregatedPhaseReport.status` (PASS requires all-pass) AND `_is_satisfied`/`is_task_satisfied` (`status.is_success`) — both keys verified compatible with PASS, incompatible with SKIPPED. |
| 7 | Test validity | PASS (after fix) | Handoff concurrency (4×300=1200 writes, asserts line-count + parse + multiset), TOCTOU (400 try_launch on 20-budget → exactly 20 granted), wall-clock (<0.5× serial @K=4), in-flight-dep resume ordering — all real-behavior, not stubs. **Added** real turn-count assertions (capability #2 was unasserted). |
| 8 | Test coverage of primary use case | PASS (after fix) | Per-task path covered end-to-end (stage1_wiring, resume_contract/semantics, handoff_*). Scheduler DAG covered via handoff_performance's 2-task dep graph (`launched.index` ordering). **Gap closed:** turn count now has primary-use-case + edge tests. |
| 9 | Error-path coverage | PASS | `count_turns` 0 on missing/no-result/non-int/bool. `FileHandoffStore.read` typed `None` on absent. `is_validated_success` defensive `except ValueError`→False on bad enum. Cycle→`CycleError` (never silent drop), parallel falls back to single declared-order set. Stall watchdog warn/kill. |
| 10 | Runtime-failure-path trace | PASS | input→parse(`_parse_phase_tasks`, M6 warn-only near-miss)→[K=1 seq | K>1 waves]→spawn(isolated env)→classify(exit_code→TaskStatus)→reconcile(locked under K>1)→journal+handoff→aggregate→PhaseResult. No step emits output a downstream gate can't consume; `--handoff=off` short-circuits store+logger cleanly. |
| 11 | Completion-scope honesty | PASS | Zero Open Questions across 4 stage gates. Two scoping decisions are HONEST: (a) RC.2 left Path-A monitor-based watchdog intact (Path A uses `monitor.reset/start` at executor.py:1754-1755; the new `_poll_with_stall_watchdog` is wired ONLY into Path B — Path A's watchdog was never the gap); (b) ruff-format version skew recorded as follow-up, `ruff check` (the bar) green. |
| 12 | Ambient-dependency completeness | PASS | 3-layer flag plumbing complete for all 3 flags: click option (commands.py:190-209) → `run()` param (228-230) → `build_config(...)` (267-269) → `SprintConfig` field (config.py:295-297→366-368→models.py:574,581,585). Imports (`FileHandoffStore`, `is_validated_success`, `build_task_context`, `count_turns_from_stream_json`, scheduler) all present at executor.py:26,49-50. |
| 13 | Kwarg-sequencing red flags | PASS | No "add kwarg before add param" pattern. `try_launch(allocation=None)`, `setup_isolation(scope="")`, `_run_one_task(lock=None)` all keyword-only with defaults; every call site passes compatible args. |
| 14 | Function-existence claims | PASS (grep-verified) | All claimed-new symbols exist: `count_turns_from_stream_json`, `build_task_context`, `HandoffRecord`, `TurnLedger.try_launch`, `write_task_complete`, `FileHandoffStore`, `is_validated_success`, `topological_launch_order`, `_poll_with_stall_watchdog`, `_task_env`, `aggregate_task_results`, `_run_one_task`, `_execute_phase_tasks_parallel` — all confirmed via grep + Read. |
| 15 | Cross-reference accuracy | PASS | H1/H3/H4/H5/H6 + M2/M4/M6 + L3 spec cross-refs in code comments match SYNTHESIS §6/§7. HandoffRecord field set matches H4 codeblock exactly. Resume key matches H5 item 2. |

---

## Adversarial probes performed

1. **Resume-skip status: PASS vs SKIPPED.** Confirmed PASS is REQUIRED, not arbitrary: `_is_satisfied`/`AggregatedPhaseReport.status`/`TaskStatus.is_success` all key success on `==PASS`; a SKIPPED record would mis-report a fully-resumed phase as FAIL and break downstream dependency satisfaction. The chosen design is the only correct one.
2. **K=1 byte-identical.** Dispatch guard requires BOTH `task_parallelism>1` AND `len(tasks)>1`; K=4-single-task and K=1 both take the unchanged sequential path with `lock=None`→`nullcontext`. No locking on the K=1 hot path.
3. **Parallel shared-mutation audit.** Spawn UNLOCKED (wall-clock win); ledger via locked `try_launch`/`debit`/`credit`; journal via locked `_jsonl`; handoff via distinct per-task files; env-capture/TUI under a local `threading.Lock`. No unguarded shared write found.
4. **`--handoff=off` legacy-exact.** Both `_handoff_store` and `_handoff_logger` gated by `handoff_enabled` (executor.py:1687-1692) → zero records AND zero `task_complete` events when off.
5. **Cross-flag composition.** `--resume`+`--start/--end`: phase selection and per-task resume-skip are orthogonal (skip check independent of phase range); help text documents composition. `--task-parallelism`+handoff: concurrency-safe per probe 3.
6. **Scheduler authenticity.** `dependencies_of` mirrors `rerun_tasks._dependencies_of` (declared∪recorded, order-preserving, de-duped, self-edges dropped, intra-set filtered) rather than a fresh parse — H6 "reuse, don't re-derive" honored.
7. **count_turns coverage (the real defect).** Found NO direct assertion test for the authoritative turn-count function — a load-bearing capability the §6 Reconciliation note explicitly requires an acceptance test for. **Fixed.**

---

## Issues Found

| # | Severity | Location | Issue | Resolution |
|---|----------|----------|-------|-----------|
| 1 | IMPORTANT | `tests/sprint/` (missing) | `count_turns_from_stream_json` (capability #2, supersedes the hard-coded-0 turn count) had ZERO direct acceptance test — only an incidental fixture reference in `e2e_real/fake_claude.py`. SYNTHESIS §6 Reconciliation note REQUIRES the acceptance test to "assert the CORRECT turn count, not merely != 0." A regression-fragile load-bearing function was unguarded. | **FIXED** — added `TestCountTurnsFromStreamJson` (7 cases: exact count, last-result-wins, missing-file→0, no-result→0, no-num_turns→0, bool-rejected→0, malformed-lines-tolerated). All pass. |

No CRITICAL issues. No other IMPORTANT/MINOR operational defects found.

## Actions Taken (fix_authorization: true)

- Added `count_turns_from_stream_json` to the `process` import block in `tests/sprint/test_process.py`.
- Added `class TestCountTurnsFromStreamJson` (7 tests) asserting correct turn extraction + all documented edge cases. Exercises the `not isinstance(num_turns, bool)` guard and last-result-wins semantics that production reconcile depends on.
- Wrote the new string literals in ruff-0.15.14-canonical single-line form so the addition is **format-clean under BOTH the CI ruff and local 0.15.14** — introducing ZERO new `ruff format` debt and NOT touching the documented version-skew follow-up. Did NOT run blanket `ruff format`. Did NOT weaken the K=1 path.
- **Verified:** `uv run ruff check tests/sprint/test_process.py` → All checks passed; `ruff format --check` → already formatted (my lines neutral); 7/7 new tests pass.
- **Re-verified no regression:** full `tests/sprint/` failing-node-id set recomputed = **54, byte-identical to `pre-change-baseline.txt` (empty symmetric diff both directions)**; passed 1041→1048 (+7 my tests). Whole-repo `make lint` GREEN.

## Self-Audit

**(a) Reliance list — structural items taken as machine-verified (NOT re-checked structurally):**
- Relied on stage{0,1,2,3}-gate-verdict PASS for section/criteria presence and the baseline node-id capture.

**(b) Independent semantic checks (≥1 required, INV-019) — own tool engagement:**
- Re-ran the FULL `tests/sprint/` suite myself and recomputed the regression set-diff with `comm` against `pre-change-baseline.txt` (did not trust the report's "ZERO regressions" claim) → independently confirmed empty symmetric diff.
- Read `AggregatedPhaseReport.status` + `TaskStatus.is_success` source to PROVE the resume-skip-records-PASS decision is operationally required (semantic, not structural — the gate verdicts asserted correctness; I verified the why from source).
- Independently found the `count_turns_from_stream_json` test-coverage gap (no gate flagged it) by grepping `tests/` for the symbol and confirming only a non-asserting fixture reference — then fixed it.
- Read `setup_isolation` + both Path-A and Path-B call sites to verify the H1 per-path merge semantics byte-for-byte, not merely that `CLAUDE_SETTINGS_DIR` "is set somewhere."

## Confidence

Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 10 | Grep/Bash: 14 | Glob: 0
(No web research required — review was local-file + executed-test bound; Tavily-first N/A.)

## QA Complete
