# R5 — Data Flow Tracer: executor.py + rerun_tasks.py

**Status: Complete**

> **⚠ CORRECTION (rf-qa research gate, CRITICAL).** This file's §1 headings/Summary
> use the Path A/B letters **INVERTED** relative to the authoritative SYNTHESIS §H1.
> The per-branch technical descriptions are correct; only the A/B *letters* are swapped.
> **Authoritative mapping (use this, ignore the letters below):**
> - **Path A = per-phase single session** = the `else`/fallback branch (`executor.py:1309+`);
>   it is the branch that **sets `CLAUDE_WORK_DIR=isolation_dir/phase-{N}`** (`executor.py:1327-1328`).
> - **Path B = per-task** = the `if tasks:` branch (`executor.py:1265`) → `execute_phase_tasks`
>   → `_run_task_subprocess`; it currently sets **NO env vars** (`executor.py:1101-1111`).
> Always anchor tasklist items on the **symbol + line** (`if tasks:` @1265, `_run_task_subprocess`,
> the fallback `ClaudeProcess` @1309+), never the bare letter.

Scope: trace runtime flows end-to-end with file:line at each hop for Sprint CLI
per-task execution + handoff wiring.

All paths relative to worktree root
`/config/workspace/IronClaude/.claude/worktrees/SprintCLIWireDead`. Module
shorthand:
- `executor.py` = `src/superclaude/cli/sprint/executor.py`
- `rerun_tasks.py` = `src/superclaude/cli/sprint/rerun_tasks.py`
- `models.py` = `src/superclaude/cli/sprint/models.py`

---

## 1. Execution fork: execute_sprint → Path A (per-task) vs Path B (single proc)

### The fork point
`execute_sprint()` (`executor.py:1138`) iterates `config.active_phases`
(`executor.py:1239`; the property is `models.py:550`, filters phases by
`start_phase <= n <= end_phase`). For each phase, after preflight/skip
short-circuits (`executor.py:1245`, `:1249`), the fork is:

```
tasks = _parse_phase_tasks(phase, config)        # executor.py:1264
if tasks:                                          # executor.py:1265  → PATH A
    ...execute_phase_tasks(...)
    continue                                       # executor.py:1307
# else falls through to PATH B (single ClaudeProcess)  executor.py:1309+
```

`_parse_phase_tasks` (`executor.py:1121`) reads the phase file, calls
`parse_tasklist(content, execution_mode=phase.execution_mode)`
(`executor.py:1134`), and returns the `list[TaskEntry]` **or `None`** when the
file has no `### T<PP>.<TT>` headings (`executor.py:1135`). `None`/empty → Path B.

### Path A — per-task delegation (executor.py:1265–1307)
1. `started_at` stamped, `logger.write_phase_start`, TUI activated
   (`executor.py:1266–1269`).
2. Calls `execute_phase_tasks(tasks, config, phase, ledger=ledger,
   shadow_metrics=..., remediation_log=..., tui=..., sprint_result=...)`
   (`executor.py:1270–1279`). Returns
   `(task_results, remaining, phase_gate_results)`.
3. **Phase status synthesis from task results** (`executor.py:1281–1290`):
   ```
   all_passed = all(r.status == TaskStatus.PASS for r in task_results)  # :1281
   status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR        # :1282
   phase_result = PhaseResult(..., exit_code=0 if all_passed else 1,
                              task_results=task_results)                  # :1283-1290
   ```
   NOTE: binary collapse — ANY non-PASS task (incl. SKIPPED from budget
   exhaustion, FAIL_RECOVERABLE, INCOMPLETE) makes the whole phase `ERROR`.
   `remaining` (the budget-exhaustion skip-list) is **discarded** in Path A;
   only `phase_gate_results` is consumed (`executor.py:1280`).
4. Post-phase wiring hook may mutate `phase_result` (`executor.py:1293`).
5. **Persisted to JSON** via `_write_phase_result_json(config, phase,
   phase_result)` (`executor.py:1304`) — this is the handoff WRITE point
   (detail in §2).

### Path A does NOT build _phase_env_vars or an isolation_dir
Important asymmetry for edit-seam mapping: the per-task path spawns
subprocesses inside `_run_task_subprocess` (`executor.py:1079`) which calls
`ClaudeProcess.__new__` + `_Base.__init__(...)` (`executor.py:1096–1111`)
with **no `env_vars`** and **no isolation copy**. There is no
`CLAUDE_WORK_DIR`, no `.isolation/phase-N/` dir, no `shutil.copy2`. Each task's
prompt is built inline (`executor.py:1090–1094`: task_id + title + phase.file +
description) and its transcript goes to `config.task_output_file(phase, task)`
(`executor.py:1104`, = `results_dir/phase-N-task-<id>-output.txt`, `models.py:561`).

### Path B — single ClaudeProcess with isolation (executor.py:1309–1330)
Only Path B builds these:
```
isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"  # :1310
isolation_dir.mkdir(parents=True, exist_ok=True)                              # :1311
shutil.copy2(phase.file, isolation_dir / phase.file.name)                     # :1312
...
_phase_env_vars = {"CLAUDE_WORK_DIR": str(isolation_dir)}                     # :1327-1329
proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)         # :1330
```
Path B then runs a poll loop (`executor.py:1346`), classifies exit_code at
`executor.py:1469` (124→timeout) / `:1471`, recovers via
`_classify_from_result_file` / checkpoint verify, and at `executor.py:1612`
ALSO calls `_write_phase_result_json` — but its `task_results` list is empty
for true single-proc phases (a synthetic per-phase `TaskResult` is built
separately at `executor.py:779`).

### execute_phase_tasks loop — per-task TaskResult construction (executor.py:972–1076)
Per iteration `i, task` (`executor.py:972`):
- **Budget gate** (`executor.py:976`): `if ledger and not ledger.can_launch()`
  → mark this+remaining tasks `TaskStatus.SKIPPED`, populate `remaining`
  list, `break` (`executor.py:978–988`).
- **Pre-debit** minimum allocation (`executor.py:991-992`):
  `ledger.debit(ledger.minimum_allocation)`.
- **Spawn**: `_subprocess_factory` (test) or `_run_task_subprocess`
  (real) → `(exit_code, turns_consumed, output_bytes)`
  (`executor.py:1003–1011`).
- **Status classification from exit code** (`executor.py:1016–1023`):
  ```
  if exit_code == 0:                                    status = PASS          # :1017
  elif exit_code == 124:                                status = INCOMPLETE    # :1019  (timeout)
  elif _is_transient_failure(config.task_output_file(phase, task)):
                                                        status = FAIL_RECOVERABLE  # :1021
  else:                                                 status = FAIL_TERMINAL # :1023
  ```
  `_is_transient_failure` (`executor.py:1782`): True if transcript has
  `api_retry`/`ConnectionRefused`, OR final JSON line has `is_error: true` AND
  `output_tokens == 0` (`executor.py:1793–1803`). Note: `turns_consumed` from
  `_run_task_subprocess` is hardcoded `0` today (`executor.py:1117–1118`,
  "Turn counting is wired separately in T02.06").
- **Budget reconcile** (`executor.py:1026–1033`): actual vs pre-allocated;
  `debit` the excess or `credit` the unused.
- **TaskResult built** (`executor.py:1035–1043`): carries `task, status,
  turns_consumed, exit_code, started_at, finished_at, output_bytes`.
- **Hooks may mutate result** then append: `run_post_task_wiring_hook`
  (`executor.py:1046`), `run_post_task_anti_instinct_hook`
  (`executor.py:1056`), `results.append(result)` (`executor.py:1066`).
- Returns `(results, remaining, gate_results)` (`executor.py:1076`).

---

## TaskResult.status enumeration (the canonical status vocabulary)

`TaskStatus(Enum)` — `models.py:45–60`. Wire values (the strings persisted in
`phase-N-result.json` via `.value`):

| Enum member | `.value` (wire) | Set by (exit code) | `is_success` | `is_failure` |
|---|---|---|---|---|
| `TaskStatus.PASS` | `"pass"` | exit_code 0 (`executor.py:1017`) | **True** | False |
| `TaskStatus.FAIL_TERMINAL` | `"fail"` | non-zero, non-transient (`:1023`) | False | True |
| `TaskStatus.FAIL_RECOVERABLE` | `"fail_recoverable"` | non-zero + transient marker (`:1021`) | False | True |
| `TaskStatus.INCOMPLETE` | `"incomplete"` | exit_code 124 / timeout (`:1019`) | False | True |
| `TaskStatus.SKIPPED` | `"skipped"` | budget exhausted, not launched (`:983`); also TaskResult default (`models.py:174`) | False | False |

`is_success` is `== PASS` only (`models.py:54-56`). `is_failure` is the set
`{FAIL_TERMINAL, FAIL_RECOVERABLE, INCOMPLETE}` (`models.py:58-60`) — note
**SKIPPED is neither success nor failure**.

**"Validated successful" for handoff/resume = `tr.status.is_success` i.e.
`status == TaskStatus.PASS` (wire `"pass"`).** Two existing consumers already
encode this contract:
- `_rerun_targets_passed` requires every target's wire status `== "pass"`
  (`rerun_tasks.py:1182`).
- `walk_dependencies._is_satisfied` returns `tr.status.is_success`
  (`rerun_tasks.py:459`).

The gate dimension is independent: `TaskResult.gate_outcome: GateOutcome`
(`models.py:180`; enum `models.py:63`, values pass/fail/deferred/pending).
A task can be `status=PASS` with `gate_outcome=FAIL/DEFERRED`. A
"validated successful" handoff predicate that wants gate-clean too must AND
`status.is_success` with `gate_outcome.is_success` (`models.py:71-73`).

---

## 2. Handoff / resume data flow (target state)

### WRITE side (exists today)
The single persisted artifact per phase is `phase-N-result.json`, written by
`_write_phase_result_json` (`executor.py:2053`) at the end of BOTH paths
(`executor.py:1304` Path A, `:1612` Path B). Payload shape (`executor.py:2059–2067`):
```
{ "phase", "status", "exit_code", "started_at", "finished_at",
  "task_results": [tr.to_dict() ...], "recovery_history" }
```
Each `tr.to_dict()` (`models.py:184–210`) embeds the full `task` block
(task_id, title, description, **dependencies**, command, classifier) plus
`status` (wire), `turns_consumed`, `exit_code`, timestamps, `output_bytes`,
`gate_outcome`, `reimbursement_amount`, `output_path`. Atomic tmp+rename
(`executor.py:2070–2072`).

**Target-state handoff WRITE seam:** a per-task handoff record (declared
upstream → downstream fan-in, validated-success flag) would be written
immediately after each `TaskResult` is finalized — i.e. inside
`execute_phase_tasks` right after `results.append(result)` (`executor.py:1066`),
OR derived during `_write_phase_result_json` since the full `task_results`
list with `status` + `task.dependencies` is already serialized there. The
JSON already carries everything a handoff needs except an explicit
"handoff/resume ledger" structure.

### READ side (exists today, phase-granular only)
- `select_default_recoverable_tasks(phase_result_json)`
  (`rerun_tasks.py:1100`): reads the JSON, returns task_ids whose wire
  `status == "fail_recoverable"` (`rerun_tasks.py:1121`). This is the closest
  existing "what should I re-run" selector — defaults to FAIL_RECOVERABLE only.
- `_load_phase_result_view(phase_result_json)` (`rerun_tasks.py:1148`):
  rehydrates real `TaskResult` objects via `TaskResult.from_dict`
  (`rerun_tasks.py:1163`) so `status.is_success` / `turns_consumed` /
  `task.dependencies` all work downstream.
- `discover_failed_tasks_from_transcripts` (`rerun_tasks.py:601`): legacy
  fallback when the JSON is missing — classifies each
  `phase-N-task-<id>-output.txt` transcript via `_classify_transcript`
  (`rerun_tasks.py:550`).

### Where the resume SKIP decision would live (target state)
There is **no per-task resume/skip-list today**. Resume is phase-granular:
`config.start_phase`/`end_phase` (`models.py:419-420`) drive `active_phases`
(`models.py:550-553`); `build_resume_output` (`models.py:844`) only emits a
**string** resume command (`superclaude sprint run ... --resume <halt_task_id>
--budget N`, `models.py:877`) — nothing reads `--resume` back into a per-task
skip set. The HALT `halt_task_id` is "the first uncompleted task ID"
(`models.py:861`) but is not consumed programmatically.

**Target-state skip decision seam:** the natural home is inside
`execute_phase_tasks` at the top of the per-task loop (`executor.py:972`),
before the budget gate (`:976`) — a guard like *"if task_id already recorded
`is_success` in the loaded prior `phase-N-result.json`, append a SKIPPED-but-
satisfied result and `continue`"*. The data to make that decision
(`prior_result.task_results` keyed by `task.task_id`, each with `status`) is
exactly what `_load_phase_result_view` already produces and what
`walk_dependencies` already keys via `result_by_id` (`rerun_tasks.py:424-426`).
The declared-upstream fan-in for resume is `task.dependencies` (read via the
same `_dependencies_of` shape in §3).

---

## 3. Dependency walk shape (reusable for a Stage-3 DAG scheduler)

Lives in `rerun_tasks.py` Section C (`rerun_tasks.py:353–531`). Public entry
`walk_dependencies(phase_tasklist, target_ids, *, phase_result=None,
results_dir=None, include_transitive=False, ignore_deps=False)`
(`rerun_tasks.py:368`). Returns `(resolved_target_ids, warnings)`.

### Inputs / sources (two declared-dependency sources, unioned)
- Parsed source tasklist → `entry_by_id` map of `TaskEntry`
  (`rerun_tasks.py:420`), giving `entry.dependencies`.
- Persisted `phase_result.task_results` → `result_by_id` map of `TaskResult`
  (`rerun_tasks.py:423-426`), giving `tr.task.dependencies` + `tr.status`.

### `_dependencies_of` — the exact shape (rerun_tasks.py:438–451)
```python
def _dependencies_of(task_id: str) -> list[str]:
    # Union of both declared-dependency sources — the parsed source tasklist
    # and the persisted result snapshot — so a dependency recorded in either
    # is checked (the two should agree; union is the safe superset if a
    # format quirk makes one incomplete). Order-preserving, de-duplicated.
    deps: list[str] = []
    entry = entry_by_id.get(task_id)
    if entry is not None:
        deps.extend(entry.dependencies)
    tr = result_by_id.get(task_id)
    if tr is not None:
        deps.extend(tr.task.dependencies)
    seen: set[str] = set()
    return [d for d in deps if not (d in seen or seen.add(d))]
```
Shape facts a DAG scheduler must know:
- **Direct only, NOT transitive** by default. `_dependencies_of` returns one
  hop. Transitivity is *not* computed as a closure — instead
  `include_transitive` *auto-adds* unsatisfied direct deps to `resolved`
  (`rerun_tasks.py:510-513`) but does **not** recurse into the added dep's own
  deps (the outer loop only iterates the original `target_ids`,
  `rerun_tasks.py:478`). So as written it is a **single-level expand**, not a
  full transitive closure, despite the docstring's "transitive" wording.
- **Cross-phase aware.** `dep_phase = _phase_number_from_task_id(dep)`
  (`rerun_tasks.py:482`; helper `:72`, parses the `PP` from `T<PP>.<TT>`).
  A cross-phase unsatisfied dep (`dep_phase != this_phase`,
  `rerun_tasks.py:486`) falls back to checkpoint-file existence via
  `_cross_phase_checkpoints_ok(dep_phase)` (`rerun_tasks.py:462-476`, globs
  `phase-{dep_phase}-cp*.md` and calls `verify_checkpoint_files`).
- **`ignore_deps`** downgrades a fatal unsatisfied-dep `ClickException`
  (`rerun_tasks.py:520`) to a non-fatal warning (`rerun_tasks.py:516-518`).

### `_is_satisfied` — completion oracle (rerun_tasks.py:453–460)
```python
def _is_satisfied(dep: str) -> Optional[bool]:
    """True=satisfied, False=recorded-but-failed, None=no record/unknown."""
    if dep in target_set:
        return True
    tr = result_by_id.get(dep)
    if tr is not None:
        return tr.status.is_success
    return None
```
Ternary contract a DAG scheduler can reuse directly: True (in-rerun-set OR
recorded PASS), False (recorded non-PASS), None (no record → triggers
cross-phase checkpoint fallback at `rerun_tasks.py:486-489`).

### Main resolution loop (rerun_tasks.py:478–531)
For each `target_id`, for each `dep` in `_dependencies_of(target_id)`: skip if
in `target_set` (`:480`); else classify via `_is_satisfied`; if not satisfied
and not cross-phase-checkpoint-ok, either auto-include (transitive, with a
**50%-of-phase-cost ceiling** computed from summed `tr.turns_consumed`,
`rerun_tasks.py:432-436`, `:501-509`), warn (ignore_deps), or abort.

**Reuse verdict for Stage-3 DAG scheduler:** `_dependencies_of` (union shape)
and `_is_satisfied` (PASS-oracle) are directly reusable as the edge-source and
node-completion primitives. The gap is that the current loop is single-level
(no recursive closure) and is *targets-driven* (validates a given rerun set)
rather than *scheduler-driven* (topological emit of a launch order). A DAG
scheduler would wrap these two helpers in a real topo sort / closure walk.

---

## 4. TurnLedger flow around each task launch (execute_phase_tasks)

`TurnLedger` defined `models.py:758`; constructed once per sprint at
`executor.py:1203-1206` with `initial_budget = config.max_turns *
len(config.active_phases)`, `reimbursement_rate=0.8`. Passed into
`execute_phase_tasks(..., ledger=ledger, ...)` (`executor.py:1274`).

Per-task lifecycle inside the loop (`executor.py:972-1066`):

1. **can_launch** (gate) — `executor.py:976`:
   `if ledger is not None and not ledger.can_launch():` → SKIP this + remaining
   (`:978-988`), `break`. `can_launch()` = `available() >= minimum_allocation`
   (`models.py:798-800`), `available() = initial_budget - consumed + reimbursed`
   (`models.py:782-784`), default `minimum_allocation=5` (`models.py:774`).
2. **debit (pre-allocation)** — `executor.py:991-992`:
   `ledger.debit(ledger.minimum_allocation)`. `debit` adds to `consumed`,
   rejects negatives (`models.py:786-790`).
3. **launch subprocess** → `turns_consumed` (`executor.py:1003-1011`).
4. **reconcile** — `executor.py:1026-1033`:
   ```
   actual = max(turns_consumed, 0)
   pre_allocated = ledger.minimum_allocation
   if actual > pre_allocated:  ledger.debit(actual - pre_allocated)
   elif actual < pre_allocated: ledger.credit(pre_allocated - actual)
   ```
   `credit` adds to `reimbursed` (`models.py:792-796`). NOTE: because
   `turns_consumed` is currently hardcoded `0` (`executor.py:1118`), every task
   today credits back the full `minimum_allocation` — net-zero burn per task
   from the launch path (real burn comes only from wiring/gate hooks below).
5. **hook-driven debit/credit** (within the appended hooks):
   - `run_post_task_wiring_hook` (`executor.py:459`) calls
     `ledger.debit_wiring(config.wiring_analysis_turns)` (`executor.py:499`;
     `models.py:806`) and `ledger.credit_wiring(...)`
     (`executor.py:544,560,599,622`; `models.py:820`, floors `int(turns*rate)`).
     May also `ledger.debit(config.remediation_cost)` (`executor.py:584`).
   - `run_post_task_anti_instinct_hook` (`executor.py:804`) calls
     `ledger.credit(credit_amount)` and sets
     `task_result.reimbursement_amount = credit_amount` (`executor.py:884-885`).

So the ledger touch order per task is:
`can_launch → debit(min) → [launch] → debit/credit(reconcile) →
debit_wiring/credit_wiring (wiring hook) → credit (anti-instinct hook)`.
There is **no `credit`/`debit` keyed to the handoff/resume decision** today —
a resume-skip path (§2) would want to **not** debit at all for already-PASS
tasks (skip before step 2).

---

## Summary

- **Fork:** `execute_sprint` (`executor.py:1138`) → `_parse_phase_tasks`
  (`:1121`) returns `list[TaskEntry]` (Path A, per-task) or `None` (Path B,
  single proc). Path A = `execute_phase_tasks` (`:928`), `continue` at `:1307`.
  **Only Path B** builds `isolation_dir` + `_phase_env_vars`/`CLAUDE_WORK_DIR`
  (`:1310-1330`); Path A's `_run_task_subprocess` (`:1079`) spawns with no env
  isolation. Per-task `TaskResult` is built at `executor.py:1035-1043`; status
  classified from exit code at `:1016-1023` (0→PASS, 124→INCOMPLETE,
  transient→FAIL_RECOVERABLE, else FAIL_TERMINAL).
- **Status enum:** `TaskStatus` (`models.py:45`) = PASS/FAIL_TERMINAL/
  FAIL_RECOVERABLE/INCOMPLETE/SKIPPED. **"Validated successful" == `is_success`
  == `status == PASS`** (`models.py:54-56`); SKIPPED is neither success nor
  failure. Gate-clean is a separate `gate_outcome` dimension (`models.py:180`).
- **Handoff:** WRITE = `_write_phase_result_json` (`executor.py:2053`, called
  `:1304`/`:1612`) → `phase-N-result.json` with full `task_results`
  (`tr.to_dict`, `models.py:184`, incl. `task.dependencies` + wire `status`).
  READ = `select_default_recoverable_tasks` (`rerun_tasks.py:1100`) /
  `_load_phase_result_view` (`:1148`). **No per-task resume skip-list exists**
  — resume is phase-granular (`start_phase`/`end_phase`, `models.py:419`);
  `build_resume_output` (`models.py:844`) emits only a string. Target-state
  skip decision belongs at the top of the `execute_phase_tasks` loop
  (`executor.py:972`) before the budget gate.
- **Dependency walk:** `walk_dependencies` (`rerun_tasks.py:368`) with
  `_dependencies_of` (`:438`, union of `entry.dependencies` +
  `tr.task.dependencies`, order-preserving dedup) and `_is_satisfied`
  (`:453`, ternary PASS-oracle). **Cross-phase aware** (`:482-489`, checkpoint
  fallback) but **single-level expand, not full transitive closure**;
  `ignore_deps` downgrades aborts. Reusable as edge-source + completion oracle
  for a Stage-3 DAG scheduler; would need a real topo/closure wrapper.
- **TurnLedger:** per task — `can_launch` gate (`executor.py:976`) →
  `debit(minimum_allocation)` (`:992`) → reconcile debit/credit (`:1026-1033`)
  → wiring `debit_wiring`/`credit_wiring` + anti-instinct `credit`
  (hooks at `:1046`,`:1056`). `turns_consumed` hardcoded 0 today
  (`executor.py:1118`), so launch path is net-zero; real burn is hook-driven.

**Status: Complete**
