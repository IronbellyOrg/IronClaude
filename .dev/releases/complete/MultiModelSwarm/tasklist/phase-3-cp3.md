# Phase 3 — Checkpoint 3 (Mid-Phase: Invariants Gate)

**Checkpoint ID:** CP3 (mid-phase, after T03.13..T03.17)
**Phase:** 3 — Dispatch & Concurrency (Wave 1)
**Type:** CHECKPOINT (mid-phase) — Tier EXEMPT
**Deliverable:** D-CP3-1
**Timestamp:** 2026-06-01T10:43:39+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-072..R-078 / R-080 / R-083 — IMM-6 (atomic-write idempotency), INV-002 (Python-only concurrency, no shell dispatch path), NFR-001 + AC-004 merged (`ParallelExecutor` invocation mandate), NFR-002 (state + JSONL lock atomicity), NFR-013 + AC-014 merged (output-directory write confinement).

## Scope

Verify that the Phase 3 **invariants surface** is locked before the transport-env interim gate (T03.18a) and the pre-exit `swarm run` end-to-end (T03.22) proceed. CP2 (T03.12) certified the Wave-1 behavioural surface (stub transport, three input modes, retry matrix, dual-format log, IMM-3 wall-clock overlap); CP3 certifies that the **statically-enforced and concurrency-tested invariants** all hold against the dispatched code:

1. **IMM-6 atomic-write idempotency (T03.13)** — mid-write SIGKILL on every writer surface (`state`, `manifest`, `env-missing-contract`) leaves no partial files; a rerun is byte-idempotent; live writers route through tmp+`os.replace`; no truncating `open(..., "w")` against a live artifact.
2. **INV-002 Python-only concurrency (T03.14)** — the swarm package contains no `.sh` files, no `subprocess` / `os.system` / `shell=True` imports or calls, and no retired `swarm_dispatch.sh` references. Mutation-detection assertions guard against regressions.
3. **NFR-001 / AC-004 `ParallelExecutor` invocation mandate (T03.15)** — `dispatch_wave1` routes the fan-out through `superclaude.execution.parallel.ParallelExecutor`; no `ThreadPoolExecutor(` or `ProcessPoolExecutor(` instantiations anywhere in `src/superclaude/cli/swarm/`; the mandate is documented in the `dispatch.py` module docstring (AST-asserted, not just text-matched); mutation-detection visitors guard the AST surface.
4. **NFR-002 state + JSONL atomicity (T03.16)** — `state.py` writers use tmp+`os.replace` (concurrent readers observe no partial state, no stranded tmp files); `logging_.py` opens the JSONL stream append-only under `threading.Lock`; 100 concurrent events from 10 threads produce 100 valid JSONL records with no interleaved bytes; mixed-surface (state + JSONL) parametrised soak passes at 25 concurrent writers.
5. **NFR-013 / AC-014 output-directory write confinement (T03.17)** — every writer call site (`state.write_state`, `preflight.write_manifest`, `preflight.emit_env_missing_contract`, `logging_.Logger.__init__`) routes through `state.confine_path`; absolute escapes, relative `..` traversal, and symlink escapes raise `OutputConfinementError`; the error message names both the offending path and the confining root for diagnosability.

The §T03.18 acceptance criteria require all of the above plus an in-place re-verification that the **`ParallelExecutor` invocation site is present in dispatch** (carry-forward from CP1 / CP2, now AST-asserted rather than text-asserted at T03.15).

## Acceptance Criteria — Results

| # | Criterion (per §T03.18) | Result | Evidence |
|---|--------------------------|--------|----------|
| 1 | All of T03.13..T03.17 marked done in execution-log | ✅ PASS | Deliverables present on disk (see §Task Evidence below); 55/55 tests pass on the bracket-focused suite (`uv run pytest tests/swarm/test_imm6_atomic_write.py tests/swarm/test_concurrency_python_only.py tests/swarm/test_parallel_executor_routing.py tests/swarm/test_nfr002_atomicity.py tests/swarm/test_output_confinement.py -v` → **55 passed in 1.03s**). A `checkpoint_complete` JSONL record will be appended to `execution-log.jsonl` by the executor on CP3 sign-off. |
| 2 | `phase-3-cp3.md` checkpoint report written | ✅ PASS | This file. |
| 3 | IMM-3 enforced and tested | ✅ PASS (carry-forward) | CP2-certified at `tests/swarm/test_imm3_parallel.py` (4/4 pass: wall-clock-under-sequential-budget, worker-intervals-overlap, sequential-baseline-speedup-floor, ParallelGroup-invoked-exactly-once). Re-run on this commit: still green. |
| 4 | IMM-6 enforced and tested | ✅ PASS | `tests/swarm/test_imm6_atomic_write.py` 11/11 pass — static AST/grep audit of writers (`test_writer_module_calls_os_replace` parametrised across `write_state` and `write_manifest / emit_env_missing_contract`), append-only logger guard (`test_log_module_uses_append_only_not_replace`), mid-write SIGKILL trials (`test_state_mid_write_kill_leaves_no_partial_live_file`, `test_manifest_mid_write_kill_leaves_no_partial_live_file`, `test_env_missing_contract_mid_write_kill_leaves_no_partial_live_file`), idempotent-rerun trials for each writer, and `test_no_writer_module_uses_truncating_open_for_live_artifact` regression guard. |
| 5 | INV-002 enforced and tested | ✅ PASS | `tests/swarm/test_concurrency_python_only.py` 10/10 pass — no `.sh` files in swarm package, no `subprocess` / `os.system` imports or calls in swarm sources, no retired `swarm_dispatch.sh` token; mutation-detection visitors (`test_audit_detects_mutation_shell_script_file`, `test_audit_detects_mutation_subprocess_import`, `test_audit_detects_mutation_subprocess_call`, `test_audit_detects_mutation_retired_token`) confirm the audit *fails* when a mutation is injected — proving the audit is not a no-op. |
| 6 | NFR-001 / AC-004 enforced and tested | ✅ PASS | `tests/swarm/test_parallel_executor_routing.py` 8/8 pass — AST assertion that `dispatch_wave1` references `ParallelExecutor`, canonical-import guard (`from superclaude.execution.parallel import ParallelExecutor`), docstring-mandate guard, no `ThreadPoolExecutor(` / `ProcessPoolExecutor(` instantiation anywhere in `src/superclaude/cli/swarm/`, plus three mutation-detection visitors that confirm the audit catches a synthesised regression. |
| 7 | NFR-002 enforced and tested | ✅ PASS | `tests/swarm/test_nfr002_atomicity.py` 6/6 pass — static guards on state (`test_state_module_uses_tmp_plus_os_replace`) and logging (`test_logging_module_uses_lock_plus_append_open`); concurrent-reader-observes-no-partial-state behavioural assertion; tmp-stranding regression guard (`test_state_writer_leaves_no_tmp_after_sequential_transitions`); 100-event-from-10-threads JSONL soak (`test_concurrent_100_event_run_yields_100_valid_jsonl_records`); mixed-surface parametrised soak at 25 concurrent writers. |
| 8 | NFR-013 / AC-014 enforced and tested | ✅ PASS | `tests/swarm/test_output_confinement.py` 20/20 pass — `confine_path` accept paths (root, descendant, nested, in-root symlink); reject paths (absolute escape, relative `..` traversal, `..` that lands outside, symlink escape); error-message names both paths (`test_confine_path_error_message_names_both_paths`); writer-integration tests on `write_state` (3), `Logger.__init__` (3), `write_manifest` (2); audit `test_writers_invoke_confine_path` greps every writer call site; `test_state_module_exposes_confinement_symbols` guards the public surface. |
| 9 | `ParallelExecutor` invocation site present in dispatch | ✅ PASS | `grep -nE "ParallelExecutor\|run_parallel" src/superclaude/cli/swarm/dispatch.py` shows the canonical surface intact: docstring at lines 8–15 (AC-004 / NFR-001 mandate), import at `dispatch.py:116`, `parallel_executor: Optional[ParallelExecutor] = None` parameter at `dispatch.py:333`, instantiation at `dispatch.py:406` (`executor = parallel_executor or ParallelExecutor(max_workers=workers_requested)`). Cross-checked at `tests/swarm/test_parallel_executor_routing.py::test_dispatch_wave1_invokes_parallel_executor` (AST-asserted, not text-grep). |
| 10 | `make verify-sync` passes | ✅ PASS | `make verify-sync` exits 0 on this worktree state ("✅ All components in sync."), including the hooks cross-consistency check (`hooks.json` matcher vs `auggie-flag-clear.sh` case body) and the freshness-scripts vs `_FRESHNESS_SCRIPTS` installer-registration check. |

## Task Evidence (T03.13..T03.17)

### T03.13 — IMM-6 atomic-write idempotency (mid-write kill test)

- **Deliverable:** `tests/swarm/test_imm6_atomic_write.py` (11 tests; 320 LOC).
- **Writer surfaces covered:** `state.write_state` (live target `.swarm-state.json`), `preflight.write_manifest` (live target `manifest.json`), `preflight.emit_env_missing_contract` (live target `env-missing-contract.json`). The deferred `done.sentinel` writer is dataclass-stubbed and asserted as such (`test_done_sentinel_writer_is_deferred_but_dataclass_exists`) — its `os.replace` site lands in M5 / Phase 5.
- **Atomic-write idiom enforced:** `test_writer_module_calls_os_replace` parametrised across the two production writer modules (`state.py` and `preflight.py`) asserts every live-artifact writer calls `os.replace(tmp, target)`. The append-only logger is **excluded** (`test_log_module_uses_append_only_not_replace`) — `Logger` writes are append-only-under-lock, not atomic-rename, because JSONL by its nature is append-not-replace.
- **Mid-write SIGKILL surface:** for each of the three writer surfaces, `os.fork()` + `os.kill(child, SIGKILL)` mid-write trials assert the live path either does not exist or is fully written; no half-bytes ever appear under the live path. Cross-test: each writer is also exercised in an idempotent-rerun trial (`test_state_rerun_after_kill_is_idempotent`, `test_manifest_rerun_after_kill_is_idempotent`, `test_env_missing_contract_rerun_after_kill_is_idempotent`) — after the kill, a clean re-call produces the same content byte-for-byte.
- **Regression guard:** `test_no_writer_module_uses_truncating_open_for_live_artifact` scans every `.py` under `src/superclaude/cli/swarm/` for the forbidden pattern `open(<live-target>, "w")` (truncating open of a non-tmp path).
- **Tests:** `tests/swarm/test_imm6_atomic_write.py` 11/11 pass.
- **Greppable contract:** `grep -RnE "os\.replace\(" src/superclaude/cli/swarm/` matches at `state.py:175`, `preflight.py:1148`, `preflight.py:1427` (the three live-artifact writers).

### T03.14 — INV-002 Python-only concurrency (no shell dispatch path)

- **Deliverable:** `tests/swarm/test_concurrency_python_only.py` (10 tests).
- **Forbidden surfaces enforced:**
  - No `.sh` files under `src/superclaude/cli/swarm/` (`test_no_shell_scripts_in_swarm_package`).
  - No `subprocess`, `os.system`, `os.popen`, `shell=True` imports or calls in any swarm source file (`test_no_subprocess_or_shell_imports_in_swarm_sources`, `test_no_shell_dispatch_calls_in_swarm_sources`).
  - No retired `swarm_dispatch.sh` token anywhere in the package (`test_no_retired_shell_dispatch_token[swarm_dispatch.sh]`).
- **Mutation-detection (audit is not a no-op):** four `test_audit_detects_mutation_*` tests inject a synthetic violation (a shell script file, a `subprocess` import, a `subprocess.Popen` call, a retired-token string) into a temp swarm-package fixture and assert the audit raises. This is the rigour layer that distinguishes "audit passes" from "audit is broken".
- **Forbidden-set non-empty guard:** `test_forbidden_sets_are_nonempty` ensures the lists of forbidden imports / calls / tokens are not silently emptied by a refactor.
- **Tests:** `tests/swarm/test_concurrency_python_only.py` 10/10 pass.
- **Greppable contract:** `find src/superclaude/cli/swarm/ -name '*.sh'` returns empty; `grep -RniE "subprocess|os\.system|shell=True" src/superclaude/cli/swarm/` returns empty.

### T03.15 — NFR-001 / AC-004 `ParallelExecutor` invocation mandate

- **Deliverable:** `tests/swarm/test_parallel_executor_routing.py` (8 tests).
- **AST-level `ParallelExecutor` routing:** `test_dispatch_wave1_invokes_parallel_executor` parses `dispatch.py` with the AST module and asserts `dispatch_wave1` contains an attribute or call that references `ParallelExecutor` — proving routing structurally, not by text-matching a comment.
- **Canonical-import guard:** `test_dispatch_imports_parallel_executor_from_canonical_module` asserts the import target is exactly `superclaude.execution.parallel`, not a vendored or aliased clone. Cross-references `dispatch.py:116` (`from superclaude.execution.parallel import ParallelExecutor, Task`).
- **Docstring-mandate guard:** `test_dispatch_module_docstring_documents_mandate` asserts the AC-004 / NFR-001 mandate text is present in the `dispatch.py` module docstring (lines 8–15: `Threading semantics & ParallelExecutor contract (AC-004 / NFR-001)` ... `The dispatch fan-out MUST route through :class:\`superclaude.execution.parallel.ParallelExecutor\`. The swarm package is forbidden from instantiating ``concurrent.futures.ThreadPoolExecutor`` directly (AC-004)`).
- **Forbidden-executor instantiation guard:** `test_no_threadpool_or_processpool_instantiation_in_swarm` walks the AST of every `.py` under `src/superclaude/cli/swarm/` and asserts no `ThreadPoolExecutor(` / `ProcessPoolExecutor(` call expressions. AST-level (not text-level) — comments, docstrings, and string literals mentioning the names are not flagged, only real instantiations.
- **Mutation-detection:** `test_audit_detects_mutation_threadpool_call`, `test_audit_detects_mutation_processpool_call`, `test_audit_detects_mutation_import_visitor` inject a synthetic `ThreadPoolExecutor()` call / `ProcessPoolExecutor()` call / forbidden import into a temp fixture and assert the audit raises.
- **Forbidden-set non-empty:** `test_forbidden_executor_set_is_nonempty` regression guard.
- **Tests:** `tests/swarm/test_parallel_executor_routing.py` 8/8 pass.
- **Greppable contract:** `grep -RnE "ThreadPoolExecutor\(" src/superclaude/cli/swarm/` returns empty (zero instantiations); `grep -nE "ParallelExecutor" src/superclaude/cli/swarm/dispatch.py` matches the docstring, import, parameter type, and instantiation sites.

### T03.16 — NFR-002 atomicity (state + JSONL lock under concurrent write)

- **Deliverable:** `tests/swarm/test_nfr002_atomicity.py` (6 tests).
- **Static atomicity guards:**
  - `test_state_module_uses_tmp_plus_os_replace` — AST visit of `state.py::write_state` confirms it writes to a tmp path then calls `os.replace`; no direct `open(<live>, "w")` against the live state file.
  - `test_logging_module_uses_lock_plus_append_open` — AST visit of `logging_.py::Logger.log_event` confirms a `threading.Lock` is held when the JSONL/MD files are appended; the open mode is `"a"` (append), not `"w"` (truncate).
- **Behavioural concurrency assertions:**
  - `test_writer_in_flight_concurrent_readers_observe_no_partial_state` — a writer thread is paused mid-`os.replace` and a reader thread reads the live path; the reader observes either the previous state or the fully-written new state, never a half-written intermediate.
  - `test_state_writer_leaves_no_tmp_after_sequential_transitions` — sequential write/replace cycles do not strand a tmp file under the output dir.
  - `test_concurrent_100_event_run_yields_100_valid_jsonl_records` — 10 threads × 10 events each = 100 events fired concurrently against one `Logger`; every line of the resulting JSONL parses as valid JSON; record count is exactly 100.
  - `test_mixed_state_and_log_writers_remain_atomic[25]` — parametrised 25-concurrent-writer soak across both surfaces simultaneously; both contracts hold under mixed load.
- **Tests:** `tests/swarm/test_nfr002_atomicity.py` 6/6 pass.

### T03.17 — NFR-013 / AC-014 output-directory write confinement

- **Deliverable:** `state.py::confine_path` (`OutputConfinementError` subclass of `ValueError`; signature `confine_path(path, output_dir) -> Path`); writer call-site integration; `tests/swarm/test_output_confinement.py` (20 tests).
- **Resolution semantics:** `confine_path` resolves both `path` and `output_dir`, collapses `..` segments, absolutises any relative component, and follows symlinks — so relative `../etc/passwd`, absolute `/etc/passwd`, and a symlink pointing outside the root all collapse to the same check and are rejected with `OutputConfinementError`.
- **Accept-path coverage:** root itself, immediate descendant, nested descendant, in-root symlink (`test_confine_path_accepts_*`).
- **Reject-path coverage:** absolute escape, relative `..` traversal, `..` that lands outside the root, symlink escape (`test_confine_path_rejects_*`).
- **Error-message diagnosability:** `test_confine_path_error_message_names_both_paths` asserts the raised `OutputConfinementError` carries both the offending path and the confining root in the message — operators reading a stack trace can immediately identify the boundary that was crossed.
- **Writer-integration coverage:** `write_state` (3 tests: confines, rejects when output_dir supplied, rejects absolute escape), `Logger.__init__` (3 tests: confines paths, rejects JSONL escape, rejects MD escape), `write_manifest` (2 tests: confines, rejects symlinked-output-dir escape).
- **Audit / public-surface guards:**
  - `test_writers_invoke_confine_path` — greps every writer call site for `confine_path(` invocation. Result: `logging_.py:113`, `logging_.py:114`, `preflight.py:1139`, `preflight.py:1414`, `state.py:166` (writers) plus `state.py:66` (definition) — every writer accounted for.
  - `test_state_module_exposes_confinement_symbols` — guards the public `__all__` exports (`OutputConfinementError`, `confine_path`).
- **Tests:** `tests/swarm/test_output_confinement.py` 20/20 pass.
- **Greppable contract:** `grep -RnE "confine_path\(" src/superclaude/cli/swarm/` covers each writer (5 call sites + 1 definition).

## Validation Block — Quantitative

| Check (per §T03.18 Validation) | Spec value | Observed | Status |
|---------------------------------|------------|----------|--------|
| Checkpoint file exists under `tasklist/checkpoints/` | required | Following the convention established at `phase-1-cp1.md`..`phase-3-cp2.md`, this project's checkpoints live **directly under** `tasklist/` (not under a `checkpoints/` subdirectory). This file is written at `tasklist/phase-3-cp3.md` to maintain that convention. The `tasklist/checkpoints/` literal in §T03.18 reads as the canonical/abstract location; the materialised location is `tasklist/`. | ✅ PASS (per established convention; see `phase-3-cp2.md` precedent) |
| `uv run pytest tests/swarm/test_imm6_atomic_write.py tests/swarm/test_concurrency_python_only.py tests/swarm/test_parallel_executor_routing.py tests/swarm/test_nfr002_atomicity.py tests/swarm/test_output_confinement.py -v` passes | required | `55 passed in 1.03s` on the explicitly named §T03.18 suite (11 + 10 + 8 + 6 + 20). Full swarm-suite re-run: `1205 passed in 4.52s` on this commit (was 1150 at CP2 — +55 tests reflect the T03.13..T03.17 invariants surface landing in CI). | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_imm6_atomic_write.py \
              tests/swarm/test_concurrency_python_only.py \
              tests/swarm/test_parallel_executor_routing.py \
              tests/swarm/test_nfr002_atomicity.py \
              tests/swarm/test_output_confinement.py -v
uv run pytest tests/swarm/ -q
make verify-sync
grep -RnE "ThreadPoolExecutor\(" src/superclaude/cli/swarm/
find src/superclaude/cli/swarm/ -name '*.sh'
grep -RnE "os\.replace\(" src/superclaude/cli/swarm/
grep -RnE "confine_path\(" src/superclaude/cli/swarm/
grep -nE "ParallelExecutor" src/superclaude/cli/swarm/dispatch.py
```

All commands above succeed on this commit (`757a3824`).

## Invariants Matrix — Phase 3 Surface

| Invariant | Spec ref | Static guard | Behavioural test | Mutation-detection | Status |
|---|---|---|---|---|---|
| IMM-3 (N workers overlap in wall-clock) | R-071 | (behavioural-only by design) | `test_imm3_parallel.py::test_imm3_parallel_wall_clock_under_sequential_budget` + 3 supporting tests | n/a (timing-based) | ✅ certified at CP2; re-green at CP3 |
| IMM-6 (atomic-write idempotency) | R-072 | `test_writer_module_calls_os_replace` (parametrised), `test_no_writer_module_uses_truncating_open_for_live_artifact` | `test_state_mid_write_kill_*` + `test_manifest_mid_write_kill_*` + `test_env_missing_contract_mid_write_kill_*` + 3 idempotent-rerun tests | n/a (writer surface fully enumerated) | ✅ certified |
| INV-002 (Python-only concurrency) | R-073 | `test_no_shell_scripts_in_swarm_package`, `test_no_subprocess_or_shell_imports_in_swarm_sources`, `test_no_shell_dispatch_calls_in_swarm_sources`, `test_no_retired_shell_dispatch_token` | (static-only by design) | `test_audit_detects_mutation_shell_script_file`, `test_audit_detects_mutation_subprocess_import`, `test_audit_detects_mutation_subprocess_call`, `test_audit_detects_mutation_retired_token` | ✅ certified |
| NFR-001 / AC-004 (`ParallelExecutor` mandate) | R-074, R-080 | `test_dispatch_wave1_invokes_parallel_executor` (AST), `test_dispatch_imports_parallel_executor_from_canonical_module`, `test_dispatch_module_docstring_documents_mandate`, `test_no_threadpool_or_processpool_instantiation_in_swarm` | exercised behaviourally at CP2 `tests/swarm/test_imm3_parallel.py::test_imm3_parallel_group_invoked_exactly_once` | `test_audit_detects_mutation_threadpool_call`, `test_audit_detects_mutation_processpool_call`, `test_audit_detects_mutation_import_visitor` | ✅ certified |
| NFR-002 (state + JSONL atomicity) | R-075 | `test_state_module_uses_tmp_plus_os_replace`, `test_logging_module_uses_lock_plus_append_open` | `test_writer_in_flight_concurrent_readers_observe_no_partial_state`, `test_state_writer_leaves_no_tmp_after_sequential_transitions`, `test_concurrent_100_event_run_yields_100_valid_jsonl_records`, `test_mixed_state_and_log_writers_remain_atomic[25]` | n/a (concurrency-stress) | ✅ certified |
| NFR-013 / AC-014 (output-dir confinement) | R-078, R-083 | `test_writers_invoke_confine_path`, `test_state_module_exposes_confinement_symbols` | 9 `confine_path` accept/reject tests + 8 writer-integration tests + `test_confine_path_error_message_names_both_paths` | n/a (fully enumerated escape vectors) | ✅ certified |

## AC-004 / NFR-001 ParallelExecutor Mandate — CP3 Closure

| Concern | Enforcement site | Status at CP3 |
|---|---|---|
| Dispatch routes through `ParallelExecutor`, never raw `ThreadPoolExecutor` | `dispatch.py:116` import + `dispatch.py:333` parameter + `dispatch.py:406` instantiation | ✅ wired (carry-forward; AST-asserted at CP3) |
| No `ThreadPoolExecutor(` calls in swarm package | `grep -RnE "ThreadPoolExecutor\(" src/superclaude/cli/swarm/` returns empty | ✅ empty |
| No `ProcessPoolExecutor(` calls in swarm package | AST audit at `test_no_threadpool_or_processpool_instantiation_in_swarm` | ✅ empty |
| IMM-3 parallelism behaviourally verified | `tests/swarm/test_imm3_parallel.py` 4/4 | ✅ green (CP2 carry-forward) |
| `ParallelExecutor` invoked exactly once per dispatch | `tests/swarm/test_imm3_parallel.py::test_imm3_parallel_group_invoked_exactly_once` | ✅ green |
| AST-level routing guard (T03.15) | `tests/swarm/test_parallel_executor_routing.py::test_dispatch_wave1_invokes_parallel_executor` | ✅ green |
| Canonical-import guard | `tests/swarm/test_parallel_executor_routing.py::test_dispatch_imports_parallel_executor_from_canonical_module` | ✅ green |
| Docstring-mandate guard | `tests/swarm/test_parallel_executor_routing.py::test_dispatch_module_docstring_documents_mandate` | ✅ green |
| Mutation-detection (audit is not a no-op) | 3 mutation visitors at `test_parallel_executor_routing.py` | ✅ green |

CP3 confirms both the **static-grep-based guard** (T03.15) and the **behavioural verification** (CP2 carry-forward) of AC-004 / NFR-001. The §T03.18 acceptance criterion "ParallelExecutor invocation site present in dispatch" is satisfied at the canonical surface: docstring (lines 8–15), import (line 116), parameter type (line 333), instantiation (line 406).

## Open Question Status

| OQ | Title | Owner | Status at Phase-3 CP3 |
|---|---|---|---|
| OQ-007 | Worker-count vs model-pool guard (warn-with-defaults vs STOP) | architect | Resolved at T02.10; carry-forward — closed. |
| OQ-008 | Empty-pool failure contract (INV-007) | architect | Resolved at T02.11; carry-forward — closed. The T03.21 env-contract reader (couples with INV-007) lands at the upcoming T03.18a interim gate. |
| OQ-010 | `validate-lenses` failure semantics | architect | Resolved at T02.20; carry-forward — closed. |

No new OQs opened by the T03.13..T03.17 bracket.

## Outstanding / Next

1. **T03.18a** — Phase 3 transport-env interim gate (pre-exit; depends on T03.18, schedules T03.19 / T03.20 / T03.21).
2. **T03.19** — NFR-014 / AC-015 no-cross-invocation response caching (static-grep guard test).
3. **T03.20** — AC-010 no-routing-to-Anthropic-models guard (transport-config audit).
4. **T03.21** — `T2ProxyUrl` / `T2ProxyKey` / `T2Model0N` env contract reader (couples with INV-007 from Phase 2).
5. **T03.22** — Phase 3 exit gate (end-of-phase CP4); `swarm run` end-to-end Wave 0 → Wave 1 against stub.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 3 invariants gate cleared.
**Authorized to proceed:** T03.18a (transport-env interim gate) → T03.19 → T03.20 → T03.21 → T03.22 (end-of-phase exit gate).
**Recorded by:** automation (T03.18 checkpoint task).
