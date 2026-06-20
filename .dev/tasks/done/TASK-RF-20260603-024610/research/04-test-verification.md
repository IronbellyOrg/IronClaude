# R4 — Test & Verification Research: Sprint CLI Per-Task Execution + Handoff Wiring

**Status: Complete**

Researcher: R4 (Test & Verification)
Scope: `tests/sprint/`, `tests/cli/eval/`, `tests/integration/test_sprint_wiring.py`, e2e harness `tests/sprint/e2e_real/`
Date: 2026-06-03

---

## 1. The Sprint Test Framework

### 1a. Pytest layout

- `tests/sprint/` — unit + integration tests of the sprint package (executor, process, models, config, TUI, recovery, rerun). ~70 files.
- `tests/sprint/e2e_real/` — **real-subprocess e2e harness** (no `subprocess.Popen`/`shutil.which` mock; a real `claude` shim is spawned). 4 e2e tests + `conftest.py` + `fake_claude.py` + `fake_claude_sourceedit.py`.
- `tests/sprint/diagnostic/` — leveled diagnostic probes (level_0..3) + own `conftest.py`.
- `tests/cli/eval/` — the eval-runner subsystem (`tests/cli/eval/test_isolation_layers_probe.py` lives here, NOT under tests/sprint).
- `tests/integration/` — cross-cutting wiring: `test_sprint_wiring.py`, `test_wiring_e2e_shadow.py`, `test_wiring_pipeline.py`.

### 1b. The two injection patterns (DOCUMENT FOR NEW TESTS)

There are **two distinct deterministic-subprocess mechanisms**. A new test should choose based on whether it needs to exercise the real spawn chain or just the executor logic.

**Pattern A — `_subprocess_factory` (in-process callable injection, fast, no real spawn).**
`execute_phase_tasks(...)` accepts a `_subprocess_factory` kwarg: a callable `(task, config, phase) -> (exit_code, turns_consumed, output_bytes)`. The executor calls it instead of spawning `claude`. Exact pattern from `tests/sprint/test_wiring_integration.py:200-210`:

```python
def _factory(task, config, phase):
    return (0, turns_per_task, 256)  # (exit_code, turns_consumed, output_bytes)

results, remaining, gate_results = execute_phase_tasks(
    tasks=tasks, config=config, phase=phase,
    ledger=ledger, _subprocess_factory=_factory,
)
```
This is the workhorse for Stage 0–2 unit tests: it returns the `(exit_code, turns, bytes)` triple the executor needs and lets the test assert on `TaskResult`, ledger accounting, and gate routing without a real process. `remediation_log=` is also injectable (`test_wiring_integration.py:288-295`).

**Pattern B — real `claude` shim on `$PATH` (e2e_real harness, slow, real `subprocess.Popen`).**
`tests/sprint/e2e_real/conftest.py` provides two fixtures:
- `claude_shim` (`conftest.py:102-129`) copies `fake_claude.py` to `tmp_path/bin/claude`, chmods +x, prepends `bin` to `$PATH` via monkeypatch, sets `FAKE_CLAUDE_CONTROL` env var, and **asserts `shutil.which("claude") == shim_dst`** so the test proves real PATH resolution. Returns a `ShimHandle` (`conftest.py:69-99`) exposing `set_failures(*task_ids)`, `control()`, `runs()`, `run_log()`.
- `real_release` (`conftest.py:132-144`) seeds a real `tasklist-index.md` + `phase-1-tasklist.md` (three `### T01.NN` per-task headings, T01.02 the transient-fail target) and returns `(config, index)` via `load_sprint_config`.

`fake_claude.py` contract (documented in its own docstring `fake_claude.py:10-41`):
- Reads prompt from **stdin**, extracts `T\d{2}\.\d{2}` id (`fake_claude.py:51,140`).
- stdout is redirected by parent into `phase-N-task-T<id>-output.txt`.
- PASS/FAIL decided purely from **exit code** + last JSON line for non-zero exits:
  - `exit 0` → `TaskStatus.PASS`; `exit 124` → `INCOMPLETE`; non-zero + last-json-line `is_error:true` + `output_tokens==0` → `FAIL_RECOVERABLE`; non-zero otherwise → `FAIL_TERMINAL` (`fake_claude.py:28-33`).
- Shared JSON CONTROL file (`$FAKE_CLAUDE_CONTROL`): `fail_tasks` (transient-fail ids), `runs` (per-id execution counter — proves only rerun target re-ran), `run_log` (ordered id list). Written atomically via tmp+`os.replace` (`fake_claude.py:70-74`).
- stdlib-only (`fake_claude.py:40-41`) so it runs under the spawned interpreter.

**New-test guidance:** Stage 0–2 acceptance tests → Pattern A. Any acceptance test that must prove the *real* spawn→stdin-prompt→stdout-capture→exit-code-classification chain (handoff persistence across a real process boundary) → Pattern B (extend `e2e_real/`, add a new `test_e2e_*.py`, reuse `claude_shim`+`real_release`).

---

## 2. What existing tests ALREADY assert (wiring must keep green / extend)

### 2a. `tests/cli/eval/test_isolation_layers_probe.py` (T02.05 / COMP-012 API pin)
Pure introspection probe (no instance, no subprocess). Pins `IsolationLayers` as a dataclass (`:40-44`), its module path `superclaude.cli.sprint.executor` (`:47-52`), the **exact 4 fields in order** `scoped_work_dir, git_boundary, plugin_dir, settings_dir` all `Path` (`:58-78`), `env_vars` is a `property` returning `dict[str,str]` (`:84-98`), `layers_active` is a `property` returning `list[str]` (`:101-115`), and `setup_isolation(config) -> IsolationLayers` signature (`:121-137`). **Wiring implication:** any new isolation field (e.g. a handoff dir) must keep these 4 fields/order intact or this probe fails loud — the tasklist must update `_EXPECTED_FIELDS` in lockstep if it extends the dataclass.

### 2b. `tests/sprint/test_context_injection.py` (D-0024 — `build_task_context`)
Exercises `build_task_context(prior_results, compress_threshold=…)` in **isolation** (imports it directly from `process.py`). Asserts: all `TaskResult` fields surface (`:73-107`), `### Gate Outcomes` section (`:83`), remediation history only when `reimbursement>0` (`:175-191`), progressive summarization at threshold (`Earlier Tasks (compressed)` / `Recent Tasks`, `:153-214`), bounded growth ratios (`:217-244`), empty-results → `""` (`:300-303`), and `TaskResult.to_context_summary(verbose=…)` shapes (`:305-334`). **Critical gap (DEAD WIRE):** these tests NEVER assert the produced context string is injected into any task prompt — `build_task_context` is not called by the executor (see §5). Stage-1/2 must ADD tests that prove the context reaches the next task's prompt.

### 2c. `tests/sprint/test_state_dir_isolation.py` (FU-001)
Pins `_write_exit_sentinel` writes `.sprint-exitcode` to `state_dir` NOT `release_dir` (3-part assertion, `:62-69`), `git ls-files` has zero tracked sentinels (`:72-102`), default `state_dir` derivation `.dev/sprint-state/<release-name>` (`:105-121`), `SPRINT_STATE_DIR` env propagation through `load_sprint_config` (`:124-151`). **Wiring implication:** any handoff state file the tasklist adds must also live under `state_dir`, never `release_dir`, and must not become git-tracked.

### 2d. `tests/sprint/test_wiring_integration.py` (TurnLedger threading)
- `execute_sprint` constructs a `TurnLedger` with `initial_budget == max_turns * len(active_phases)`, `consumed==0`, passes it to `execute_phase_tasks` (`:66-123`). Patches `shutil.which`, `execute_phase_tasks`, `run_post_phase_wiring_hook`, `notify._notify`, `SprintLogger`, `preflight.execute_preflight_phases`.
- `run_post_phase_wiring_hook` called exactly once per phase, with correct phase numbers (`:129-183`).
- **Budget accounting via `_subprocess_factory`** (`:189-235`): documents the pre-debit-`minimum_allocation`-then-reconcile model — `consumed = num_tasks * min_alloc(5)`, `reimbursed = num_tasks * (min_alloc - actual)`, `available() = budget - consumed + reimbursed`. This is the canonical reference for Stage-2 budget-handoff assertions.
- Shadow-mode findings logged to `DeferredRemediationLog` with `[shadow]` prefix, status unchanged (`:241-311`).

### 2e. `tests/integration/test_sprint_wiring.py` (post-task wiring hook, 4 modes)
`run_post_task_wiring_hook(task, config, result)` and `run_wiring_safeguard_checks(config)`: off→unchanged same object (`:71-92`); shadow→status unchanged + logs (SC-006, `:95-126`); soft→warns on critical, status unchanged (`:129-165`); full→`FAIL_TERMINAL` + `GateOutcome.FAIL` on findings (`:168-204`); safeguards never block/raise (`:207-245`). **Wiring implication:** the per-task wiring hook is the post-task handoff point; new handoff steps must preserve these mode semantics.

### 2f. `tests/sprint/test_executor.py::TestPerTaskOrchestration` (`:596-744`)
The richest per-task `_subprocess_factory` suite. Factories return `(exit, turns, bytes)`: `_pass_factory→(0,3,1024)`, `_fail_factory→(1,5,512)`. Asserts: one spawn per task (`:620-636`), all-pass (`:638-647`), **budget starvation → SKIPPED + remaining task IDs** (`:649-673`), per-task debit/credit `available()==initial-3` (`:675-692`), empty inventory (`:694-702`), fail→`FAIL_TERMINAL`+`exit_code==1` (`:704-713`), `exit 124`→`INCOMPLETE` (`:715-727`), no-ledger always-launch (`:729-744`). Plus `TestSetupIsolation` (`:750-...`) and `TestAggregateTaskResults` (`:813-...`, `total_turns_consumed==8`).

### 2g. `tests/sprint/test_multi_phase.py` (phase-level path — RECONCILIATION SIGNAL)
Uses the **phase-level** mock path, NOT per-task: patches `cli.pipeline.process.subprocess.Popen` with a fake `_Popen` (`poll`/`wait`) and drives the `EXIT_RECOMMENDATION: CONTINUE/HALT` **result-file** protocol (`:48-104` happy path order `[1,2,3]`; `:113-179` halt at phase 3 → `SprintOutcome.HALTED`, `halt_phase==3`, `SystemExit code==1`). Note `os.utime` future-mtime trick (`:144-146`) to satisfy the freshness guard. **Reconciliation:** there are TWO execution paths — phase-level (Popen + result-file) and per-task (`execute_phase_tasks` + `_subprocess_factory`). The tasklist must be explicit about which path it wires; multi-phase tests pin the phase-level halt-propagation contract that must remain green.

### 2h. `tests/sprint/test_backward_compat_regression.py` (T09.02, grace_period=0)
Pins v1.2.1 equivalence: `grace_period==0` default (`:122-132`), zero extra daemon threads (`threading.active_count()`, `:164-202`), per-task `ledger=None` → no budget gating all-pass (`:238-261`), `_determine_phase_status` 8-branch priority chain timeout>error>HALT>CONTINUE>frontmatter>no_report (`:328-374`), `check_budget_guard(None) is None` (`:381-384`), JSONL execution-log has `sprint_start`/`sprint_complete` events (`:469-509`). **TestRerunTasksNoRegressionWhenUnused** (`:589-715`): a clean sprint emits NONE of `phase_rerun_start`/`task_rerun_complete`/`phase_rerun_complete` (`:596-650`), adds zero threads, and `_write_phase_result_json` doesn't break the baseline e2e (reuses `test_e2e_success.TestE2ESuccess`). **Wiring implication:** the strongest backward-compat guardrail — any new handoff event type must be inert/absent on a non-handoff sprint, and add zero daemon threads.

---

## 3. Turn counting / TaskResult assertions today (Stage-0 "correct turn count, not just !=0" gate)

### 3a. THE STAGE-0 DEAD WIRE — turn count is hardcoded `0` in real spawns
`src/superclaude/cli/sprint/executor.py:1117-1118`:
```python
    # Turn counting is wired separately in T02.06
    return (exit_code if exit_code is not None else -1, 0, output_bytes)
```
`_run_task_subprocess` (`executor.py:1079-1118`) spawns the real `ClaudeProcess` with `output_format="stream-json"` (`:1110`), waits, computes `exit_code` and `output_bytes` from the on-disk file — but returns a **literal `0`** for `turns_consumed`. `T02.06` (turn wiring) is unimplemented and referenced ONLY at this line in source (`grep T02.06 src/` → only `executor.py:1117` for sprint; other hits are `cli_portify`). **This is precisely the Stage-0 gate target.**

### 3b. Why no existing test catches it
Every per-task turn assertion goes through `_subprocess_factory`, which returns synthetic turn values (`_pass_factory→3`, `test_wiring_integration` factory→`turns_per_task`). The factory bypasses `_run_task_subprocess` entirely (`executor.py:1003-1009`: `if _subprocess_factory is not None: ... else: _run_task_subprocess(...)`). So `ledger.available()==initial-3` (`test_executor.py:692`) and the budget math in `test_wiring_integration.py:218-235` all assert on **injected** turns, never on the real stdout-derived count. The e2e_real harness fixtures (`test_e2e_rerun_happy_path.py`) seed `turns_consumed: 5` in result JSON and never assert the live count.

### 3c. How TaskResult turns ARE surfaced (for new assertions)
- `TaskResult.turns_consumed` flows into `aggregate_task_results` → `AggregatedPhaseReport.total_turns_consumed = sum(r.turns_consumed …)` (`executor.py:333`), rendered in YAML/markdown (`:239,248,276,279`). `test_executor.py:830` asserts `total_turns_consumed == 8`.
- Budget reconcile uses `actual = max(turns_consumed, 0)` (`executor.py:1028`) then debits/credits the ledger (`:1024-1040`); credit math `int(task_result.turns_consumed * ledger.reimbursement_rate)` (`:883`).
- `to_context_summary(verbose=True)` includes turns (`test_context_injection.py:331` asserts `"15"`).

**Stage-0 new test (Pattern B required):** the `fake_claude.py` PASS transcript already emits a `{"type":"result", …, "output_tokens":88}` line and an assistant `usage` block (`fake_claude.py:86-102`). A Stage-0 acceptance test must make the shim emit a **known, specific turn count** (e.g. N assistant turns) and assert the executor's `_run_task_subprocess` (or `TaskResult.turns_consumed` after a real spawn) equals **exactly N**, not merely `!= 0`. The shim is the right injection vector; the test belongs in `tests/sprint/e2e_real/` (new `test_e2e_turn_count.py`) because only the real-spawn path exercises the hardcoded-`0` line.

---

## 4. Concurrency-test approach available

### 4a. The premise needs correction — the sprint per-task loop is SEQUENTIAL, and there is NO `FileHandoffStore`
- `execute_phase_tasks` is a **strict `for` loop**, one task at a time (`executor.py` around `:960-1040`; the subprocess spawn at `:1002-1011` is inside the per-task loop body). There is **no thread pool / no concurrent writer** in the sprint per-task execution path. So within a single sprint, `_subprocess_factory` is never invoked concurrently.
- There is **no `FileHandoffStore` class anywhere** in `src/superclaude/` (grep for `FileHandoffStore`/`HandoffStore`/`handoff_store` → zero matches in code). The "handoff" surface that actually exists is: (a) per-task output files `phase-N-task-T<id>-output.txt`, (b) the canonical `phase-N-result.json`, (c) the append-only `execution-log.jsonl`, and (d) in-process `build_task_context` (currently uncalled — see §5).
- `_jsonl` is **not a free function** — it is `SprintLogger._jsonl(self, data)` at `src/superclaude/cli/sprint/logging_.py:265-267`: a plain `open(execution_log_jsonl, "a")` + `f.write(json.dumps(...) + "\n")`. **No `fcntl`/`flock`, no `os.replace` atomicity.** (The atomic tmp+`os.replace` pattern exists only in the test shim `fake_claude.py:70-74`, not in production logging.)

### 4b. Can the harness spawn N concurrent `_subprocess_factory` writers?
Not as the sprint runs today — but a **test can construct the concurrency directly**, since `_subprocess_factory` is just an injected callable and `SprintLogger._jsonl` is a public-ish method. The only existing concurrency harness is `tests/cli/eval/test_parallel_15.py`, and it belongs to the **eval orchestrator** (`RunOrchestrator.run(specs, parallel=8)`, thread-pool with `threading.Lock` + `observed_concurrency` tracking, `:222-238`). Critically, that harness **avoids** shared-file contention: each worker gets a unique `HomeIsolation.home_path` and its own **per-eval JSONL** (`test_per_eval_jsonl_contents_are_self_consistent`, `:368-405`; `test_each_eval_*` assert uniqueness, `:247-309`). It is a model for *isolation under parallelism*, not for *contention on one file*.

### 4c. How a "≥4 concurrent writers, zero corruption over ≥1000 runs" race test would be structured
Because the production sprint loop is sequential, a Stage-3 race test is only meaningful if the tasklist **introduces** a shared handoff writer (e.g. makes `_jsonl` or a new handoff-store the concurrency point). Two viable structures:
1. **Direct-writer stress** (recommended, minimal deps): spin up ≥4 `threading.Thread` workers (or `ThreadPoolExecutor(max_workers≥4)`) each calling the handoff write API (`SprintLogger._jsonl` or the new store) in a tight loop; run the whole scenario ≥1000 times (parametrize / loop). After each batch, read the JSONL back line-by-line with `json.loads` and assert: (a) line count == expected total writes (no lost/torn writes), (b) every line parses (no interleaved/corrupt JSON), (c) the multiset of payloads == what was written. **This test will FAIL against the current lock-free `_jsonl`** under real concurrency — which is the point of the Stage-3 gate; wiring must add `fcntl.flock` or a lock/queue. Model the thread-pool + `threading.Lock` observation scaffolding on `test_parallel_15.py:222-238`.
2. **Factory-driven** (closer to sprint reality): a `_subprocess_factory` that, when invoked, writes a handoff record; drive ≥4 of them via threads sharing one `SprintLogger`. Same readback assertions.

### 4d. Timing / benchmark harness for the Stage-3 wall-clock gate
Two existing patterns the tasklist should reuse:
- `tests/sprint/test_nfr_benchmarks.py` (`@pytest.mark.nfr_benchmark`) — p95-over-N-iterations with `time.perf_counter()`, sub-threshold assertion + a determinism test asserting ≥95% pass rate (`:96-115`); also O(1) ratio tests (per-op at 1000 within 2× of per-op at 10, `:128-229`) and absolute `<1ms` after 10000 ops (`:231-255`). Best template for a per-task / per-handoff wall-clock budget.
- `tests/sprint/test_wiring_performance.py` (`@pytest.mark.slow`, `@pytest.mark.performance`) — 20 iterations, sorted p95 at index 18, `< 5.0s` threshold, with all timings dumped on failure (`:273-304`). Best template for a coarser end-to-end wall-clock gate.

**New concurrency/perf test files for Stage-3:** `tests/sprint/test_handoff_concurrency.py` (race/corruption, §4c) and either extend `test_nfr_benchmarks.py` or add `tests/sprint/test_handoff_performance.py` (wall-clock). Use marks `nfr_benchmark` / `slow` + `performance` consistent with the existing suites.

---

## 5. Existing references to T02.05 / T02.06 (and the dead-wire reconciliation signal)

- **T02.05** — `tests/cli/eval/test_isolation_layers_probe.py:1` ("COMP-012 probe … Task T02.05"); re-verified by `tests/cli/eval/test_home_isolation_extend.py:7,21,29,513-518`. The probe is the frozen `IsolationLayers` API pin (§2a). The HomeIsolation extension chain (COMP-006) is T02.07 (`test_home_isolation_extend.py:1`) and T02.11 (`test_home_isolation.py:1`, `test_parallel_15.py:14`). These are an **eval-subsystem** lineage, distinct from the sprint per-task wiring — but they share the `executor.IsolationLayers` dataclass, so a sprint-side handoff field change ripples into these probes.
- **T02.06** — appears as a **source dead-wire marker** at `src/superclaude/cli/sprint/executor.py:1117` (`# Turn counting is wired separately in T02.06`). The other `T02.06` hits are unrelated subsystems: `cli_portify/failures.py:12,138` (timeout steps), `tests/cli_portify/`, `tests/pipeline/test_fmea_domains.py:3`, and `tests/sprint/diagnostic/test_instrumentation.py:394` (a CLI-options section header, NOT turn counting). `tests/sprint/test_models.py:1077-1088` uses `T02.05`/`T02.06` only as sample task IDs for `TaskEntry.task_output_file` naming (`phase-2-task-T02.05-output.txt`), not as feature references.
- **Reconciliation takeaway:** the task IDs `T02.05`/`T02.06` in *this* tasklist's lineage map to (a) the isolation API pin (already-green, must stay green) and (b) the **unimplemented turn-counting wire** (the Stage-0 target). The tasklist should NOT reuse `T02.06` as a fresh task ID without noting it already names the dead wire it is closing.

---

## 6. Per-stage extend/add map (0/1/2/3)

| Stage | Existing tests that EXTEND (must stay green) | New test file(s) the tasklist should ADD |
|---|---|---|
| **0 — turn count correctness** | `test_executor.py::TestPerTaskOrchestration` (`:596-744`, factory turn math); `test_wiring_integration.py` budget math (`:189-235`); `test_backward_compat_regression.py` `total_turns_consumed`/`aggregate` | `tests/sprint/e2e_real/test_e2e_turn_count.py` (Pattern B: shim emits known N turns, assert `TaskResult.turns_consumed == N` exactly, killing `executor.py:1118` hardcoded `0`). Optionally a `process.py` unit test for a new `_count_turns(stdout)` parser. |
| **1 — context injection wired into prompt** | `test_context_injection.py` (all `build_task_context` shape assertions, `:64-334`) | New unit test asserting `_run_task_subprocess` (or its prompt builder) **calls** `build_task_context(prior_results)` and the returned string appears in the spawned prompt (Pattern A spy on prompt, or Pattern B asserting the shim received prior-context on stdin via the CONTROL file). Extend `e2e_real/` to prove cross-task handoff reaches stdin. |
| **2 — handoff persistence / budget across tasks** | `test_wiring_integration.py` (TurnLedger threading, post-phase hook); `test_sprint_wiring.py` (4-mode post-task hook); `test_state_dir_isolation.py` (state_dir, not release_dir); `test_multi_phase.py` (phase-level halt path) | `tests/sprint/test_handoff_store.py` (if a store is introduced) + extend `test_state_dir_isolation.py` for any new handoff state file; an `e2e_real` test proving result-JSON/handoff round-trips across a real rerun (model on `test_e2e_rerun_happy_path.py`). |
| **3 — concurrency + wall-clock NFR** | `test_nfr_benchmarks.py`, `test_wiring_performance.py`, `test_parallel_15.py` (isolation-under-parallelism model) | `tests/sprint/test_handoff_concurrency.py` (≥4 writers, ≥1000 runs, JSONL readback corruption check — §4c) + `tests/sprint/test_handoff_performance.py` or extend `test_nfr_benchmarks.py` (p95 wall-clock, §4d). |

Backward-compat guardrail spanning ALL stages: `test_backward_compat_regression.py::TestRerunTasksNoRegressionWhenUnused` (`:589-715`) — every new handoff event/thread must be inert on a non-handoff sprint.

---

## 7. Summary

- **Two dead wires drive this work, both confirmed at source:** (1) **turn counting** is hardcoded `return (..., 0, ...)` at `executor.py:1117-1118` (`# … wired separately in T02.06`) — Stage-0 target; (2) **`build_task_context`** (`process.py:257`) is fully implemented and unit-tested in isolation but **never called by the executor** — Stage-1/2 target. No existing test catches either, because per-task tests inject synthetic turns via `_subprocess_factory` and context tests never assert injection into a prompt.
- **There is NO `FileHandoffStore`.** The real handoff surfaces are per-task output files, `phase-N-result.json`, and the append-only `execution-log.jsonl` written by `SprintLogger._jsonl` (`logging_.py:265-267`) — which is **lock-free and non-atomic**. The sprint per-task loop is **sequential**, so production never writes concurrently; a Stage-3 race test is only meaningful if wiring introduces a shared concurrent writer, and it would expose the missing lock in `_jsonl`.
- **Two injection patterns for new tests:** Pattern A = `_subprocess_factory` callable returning `(exit, turns, bytes)` (fast, in-process; canonical refs `test_executor.py:610-618`, `test_wiring_integration.py:200-210`); Pattern B = real `claude` shim on `$PATH` via `e2e_real/conftest.py` `claude_shim` + `real_release` fixtures (real spawn; required for Stage-0 turn-count and any real-process-boundary handoff proof).
- **Concurrency/perf harness templates exist:** thread-pool + `threading.Lock` observation in `test_parallel_15.py:222-238`; p95/determinism/O(1) timing in `test_nfr_benchmarks.py`; coarse p95 wall-clock in `test_wiring_performance.py`.
- **Task-ID reconciliation:** `T02.05` = frozen isolation API pin (keep green); `T02.06` = the turn-counting dead wire (`executor.py:1117`). Do not silently re-use `T02.06`.
- **Strongest guardrail:** `test_backward_compat_regression.py` — grace_period=0 v1.2.1 equivalence, zero daemon threads, and rerun events absent on clean sprints.

**Status: Complete**
