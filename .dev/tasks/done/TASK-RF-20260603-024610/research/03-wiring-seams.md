# R3 — Integration Points / Wiring Seams (executor.py + process.py)

**Status: Complete**

Scope: `src/superclaude/cli/sprint/executor.py` (2203 lines) and `src/superclaude/cli/sprint/process.py` (385 lines).
For each wiring point: exact current code (file:line), what must change, cross-effects.

All paths relative to worktree root `/config/workspace/IronClaude/.claude/worktrees/SprintCLIWireDead/`.

> **Path A / Path B naming (per SYNTHESIS §6 H1).** **Path A = per-phase single session** = the *freeform fallback* branch in `execute_sprint` (`executor.py:1309+`), which sets `CLAUDE_WORK_DIR=<isolation_dir>`. **Path B = per-task** = the `if tasks:` branch (`executor.py:1265`) → `execute_phase_tasks` → `_run_task_subprocess`, which sets **no** env. Path selection is the heading-regex fork at `executor.py:1264`. This is the opposite of intuitive lettering (A is the *fallback*, B is the *primary task path*), so every seam below states which concrete branch it touches.

> **Cross-cutting seam (affects #2, #3, #5).** `SprintLogger` is constructed in `execute_sprint` (`executor.py:1164`) and is **NOT** passed into `execute_phase_tasks` (verified: signature `executor.py:928-941` has no `logger` param; `logger.*` calls only appear in `execute_sprint`, never inside `execute_phase_tasks`). Any per-task ledger write (write_task_complete), context build, or turn-capture that needs the logger or sprint-level state must EITHER thread `logger` (and `start_commit`) into `execute_phase_tasks`, OR be done in `execute_sprint` after the call returns (which loses per-task ordering interleave). Researcher R5 owns the data-flow tradeoff; this report flags the seam.

---

## 1. setup_isolation per-path merge (H1)

### (a) Path A `_phase_env_vars` — what CLAUDE_WORK_DIR does it set?

`execute_sprint`, freeform-fallback branch — `executor.py:1309-1330`:

```python
# Per-phase isolation directory: exactly one file (the phase file)
isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"   # 1310
isolation_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(phase.file, isolation_dir / phase.file.name)
...
# Launch claude with isolation env vars (CLAUDE_WORK_DIR → isolation_dir)
_phase_env_vars = {                                # 1327
    "CLAUDE_WORK_DIR": str(isolation_dir),         # 1328  <-- PHASE-SCOPED copy dir
}
proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)   # 1330
```

So Path A's `CLAUDE_WORK_DIR` = `<results_dir>/.isolation/phase-{N}` — a **per-phase copy dir** containing exactly one file (the phase file, copied at line 1312). It is NOT the release dir.

### (b) What does setup_isolation / IsolationLayers.env_vars return for CLAUDE_WORK_DIR?

`setup_isolation` — `executor.py:151-183`. It returns `IsolationLayers(scoped_work_dir=config.release_dir, git_boundary=config.release_dir, plugin_dir=base/"plugins", settings_dir=base/"settings")` where `base = config.results_dir / ".isolation"` (`executor.py:169`, `178-183`).

`IsolationLayers.env_vars` — `executor.py:127-134`:

```python
return {
    "CLAUDE_WORK_DIR": str(self.scoped_work_dir),       # 130  == config.release_dir  (WHOLE release dir)
    "GIT_CEILING_DIRECTORIES": str(self.git_boundary),  # 131  == config.release_dir
    "CLAUDE_PLUGIN_DIR": str(self.plugin_dir),          # 132  == .isolation/plugins
    "CLAUDE_SETTINGS_DIR": str(self.settings_dir),      # 133  == .isolation/settings
}
```

**CONFLICT confirmed (the crux of H1):** `setup_isolation`'s `CLAUDE_WORK_DIR` = `config.release_dir` (the **whole** release dir), but Path A needs `CLAUDE_WORK_DIR` = `<.isolation/phase-{N}>` (the **per-phase copy**). A naive `_phase_env_vars.update(setup_isolation(config).env_vars)` would **clobber** Path A's phase scoping. Also note `setup_isolation` creates `plugins/` and `settings/` but those dirs are **empty** — no settings.json is seeded into `settings_dir` (only `mkdir`, `executor.py:175-176`); H2 gate 1 must verify the seed/merge policy or the isolated child gets no project hooks/MCP at all.

### (c) Path B `_run_task_subprocess` — confirm NO env_vars

`_run_task_subprocess` — `executor.py:1096-1111` builds the `ClaudeProcess` via `_Base.__init__` with `prompt / output_file / error_file / max_turns / model / permission_flag / timeout_seconds / output_format` — **no `env_vars=` kwarg**. Confirmed: Path B passes nothing, so the child inherits the parent env verbatim (no isolation, no per-task `CLAUDE_SETTINGS_DIR`). This is the unmitigated-corruption path.

### How to wire WITHOUT clobbering (the required edit)

**Path A (`executor.py:1327-1328`):** build the isolation layers, then merge ONLY the two new keys, preserving the phase-scoped work dir:

```python
_layers = setup_isolation(config)                 # or a per-phase-parameterized variant
_phase_env_vars = {
    "CLAUDE_WORK_DIR": str(isolation_dir),         # KEEP phase-scoped (do NOT take _layers' value)
    "CLAUDE_SETTINGS_DIR": _layers.env_vars["CLAUDE_SETTINGS_DIR"],
    "CLAUDE_PLUGIN_DIR": _layers.env_vars["CLAUDE_PLUGIN_DIR"],
    # GIT_CEILING_DIRECTORIES optional — release_dir boundary is safe to add
}
```

Equivalent merge-then-restore form: `_phase_env_vars = {**_layers.env_vars, "CLAUDE_WORK_DIR": str(isolation_dir)}` (the trailing key wins, re-pinning phase scope). Either is correct; the explicit-subset form is clearer about intent.

**Path B (`_run_task_subprocess`, `executor.py:1101-1111`):** add `env_vars=` to the `_Base.__init__` call, injecting the FULL set. Because Path B has no phase-copy work dir today, the simplest correct wiring is the whole `setup_isolation(config).env_vars`:

```python
_Base.__init__(
    proc,
    prompt=prompt,
    output_file=config.task_output_file(phase, task),
    ...
    output_format="stream-json",
    env_vars=setup_isolation(config).env_vars,    # NEW — full 4-layer set
)
```

**Per-phase/per-task parameterization (H1 "likely needs"):** `setup_isolation(config)` currently has a single `settings_dir = base / "settings"` shared across all phases/tasks (`executor.py:175`). For Path A that is acceptable serially, but Stage 3 parallelism needs a **per-slot** settings dir. Recommend adding an optional discriminator param, e.g. `setup_isolation(config, scope: str = "")` → `settings_dir = base / "settings" / scope` (scope = `f"phase-{N}"` for A, `f"task-{task_id}"` or `f"worker-{k}"` for B/parallel). This keeps Path A's serial behavior (`scope=""`) while making per-worker isolation a one-arg change later.

**Cross-effects:**
- Startup cleanup `shutil.rmtree(config.results_dir / ".isolation", ...)` (`executor.py:1229`) already wipes the whole `.isolation` tree per run — `setup_isolation`'s `base = results_dir/.isolation` lives under it, so no orphan accumulation, but note Path A's `phase-{N}` dirs ALSO live under `.isolation` (`executor.py:1310`). Adding `settings/` + `plugins/` siblings is compatible with that cleanup.
- `build_env` (`process.py:97-112`) merges `env_vars` with `os.environ.copy()` override semantics AFTER popping `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`. So injected keys cleanly override inherited ones. No change needed in `build_env`.

---

## 2. build_task_context wiring point

`build_task_context(prior_results, *, start_commit="", compress_threshold=3) -> str` — `process.py:257-319`. Confirmed dead (zero external callers per R1/grounding). It consumes `list[TaskResult]` and emits a markdown "## Prior Task Context" block (status, gate outcomes, remediation history, optional git diff).

**Where `results` accumulate (Path B loop):** `execute_phase_tasks`, `executor.py:965` declares `results: list[TaskResult] = []`; each iteration appends at `executor.py:1066` (`results.append(result)`). So at the **top of iteration `i`**, `results` already holds the `i` prior TaskResults — exactly `build_task_context`'s input.

**Where it would be called + fed into the per-task prompt:** the per-task prompt is built inside `_run_task_subprocess` (`executor.py:1090-1094`):

```python
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n"
    f"Description: {task.description}\n"
)
```

`_run_task_subprocess(task, config, phase)` does **not currently receive `results`** (signature `executor.py:1079-1083`). Two wiring options:

- **(Recommended) Thread prior context as a param.** Change signature to `_run_task_subprocess(task, config, phase, prior_context: str = "")` and at the call sites (`executor.py:1009-1011`) pass `prior_context=build_task_context(results, start_commit=...)` computed in the loop *before* the spawn (after the budget/TUI block, before line ~1002). Then append `prior_context` to `prompt`. `build_task_context` runs in the parent (executor) process — it does NOT need the logger, only `results` (already in scope) and an optional `start_commit`. `start_commit` is NOT currently available in `execute_phase_tasks`; if git-diff context is wanted it must be threaded from `execute_sprint`, else pass `""` (the diff section is simply skipped — `process.py:314-318`).
- (Alt) Compute inside `_subprocess_factory`/`_run_task_subprocess` — rejected: `results` lives in the loop, not in the subprocess fn; passing the whole list down is leakier than passing the rendered string.

**Cross-effect:** This is the Stage-1 "replace thin per-task prompt" work (SYNTHESIS §6 M3). M3's per-task prompt-composition table governs WHAT goes in the prompt; `build_task_context` supplies the "Sprint Context (prior-phase dirs) → narrowed to upstreams" + "Prior Task Context" sections. The `consumed_upstreams` narrowing (H4 field) is NOT yet implemented in `build_task_context` — it dumps ALL prior results, not just declared upstreams; narrowing is a Stage-1/2 enhancement, not present today.

---

## 3. write_task_complete call site

There is **no** `write_task_complete` method today (confirmed — `logging_.py` grep shows `write_task_rerun_complete` @205, `write_phase_rerun_complete` @221, `write_summary` @245, but no `write_task_complete`). The closest sibling is `write_task_rerun_complete` (`logging_.py:205-219`), emitting `event:"task_rerun_complete"` with `{phase, task_id, status, turns, duration_sec, timestamp}` via `self._jsonl(...)`.

**Exact slot for the per-task journaling call:** inside `execute_phase_tasks`, the `TaskResult` is fully built (after both post-task hooks) at `executor.py:1035-1064`, and appended at `executor.py:1066`:

```python
results.append(result)              # 1066  <-- write_task_complete(result) + handoff write slot here
```

The new `logger.write_task_complete(...)` + `HandoffStore.write(record)` would slot **immediately after line 1066** (or just before, after `result` is final at 1064), inside the loop, once per task.

**BLOCKER for this slot — the logger is not in scope here.** As flagged in the cross-cutting seam: `execute_phase_tasks` has no `logger` param. To write at `executor.py:1066`, the cleanest wiring is to add `logger: SprintLogger | None = None` to the `execute_phase_tasks` signature (`executor.py:928-941`) and pass it from the call site at `executor.py:1270-1279` (which already has `logger` in scope). The handoff store would be passed the same way (a new `handoff_store=` param). The alternative — journaling in `execute_sprint` after `execute_phase_tasks` returns `task_results` (loop over the returned list near `executor.py:1280`) — keeps the signature unchanged but loses real-time interleaving and any per-task `started_at/finished_at` that isn't already on `TaskResult` (it IS: `TaskResult.started_at/finished_at`, set at `executor.py:1040-1041`, so the post-hoc loop is viable). **Recommended: thread the logger in** so Stage 0's writer and Stage 1's handoff write share one site and the same single-writer discipline (M2).

**Schema reconciliation (H3):** the new writer must NOT silently fork. Preferred: `event:"task_complete"` for first-run, mirroring the existing `task_rerun_complete` field set `{phase, task_id, status, turns, duration_sec, timestamp}` (use `result.turns_consumed` for `turns`, `(finished_at-started_at).total_seconds()` for `duration_sec`, `result.status.value` for `status`). Freeze both schemas side-by-side.

**Cross-effect (M2/L3):** `_jsonl` (`logging_.py:265-267`) is a bare lock-free `open(path,"a"); f.write(...)` — safe ONLY under the sequential single-writer invariant that Stages 0-2 rely on. The handoff file write (atomic temp+replace) and the `_jsonl` append are two separate operations; a crash between them yields a completed task with no journal event (L3) — resume must treat the handoff file, not the JSONL, as authoritative.

---

## 4. _subprocess_factory env-capture seam (H6)

**How `_run_task_subprocess` builds the ClaudeProcess** — `executor.py:1096-1112`. It uses `ClaudeProcess.__new__` + `_Base.__init__` (the pipeline base, imported at `executor.py:1099`) and — critically — passes **no `env_vars`** (see #1c). It then `proc.start(); proc.wait()` and returns `(exit_code, 0, output_bytes)` (`executor.py:1118`).

**Why `_subprocess_factory` bypasses env_vars:** the factory is a test seam (`execute_phase_tasks` param `_subprocess_factory=None`, `executor.py:934`). When provided, the loop calls it at `executor.py:1004-1006`:

```python
exit_code, turns_consumed, output_bytes = _subprocess_factory(task, config, phase)
```

It returns the result tuple **directly**, never constructing a `ClaudeProcess`, so the env layer (`build_env` / `env_vars`) is entirely skipped. Consequently a unit test that injects `_subprocess_factory` can assert exit-code/turns/bytes behavior but **cannot** observe what `CLAUDE_SETTINGS_DIR` each worker would receive — the env-merge logic lives in `_run_task_subprocess` → `_Base.__init__(env_vars=...)` → `build_env`, none of which the factory path touches.

**Minimal `_env_builder`/`_env_capture` injection point (proposed):** extract env construction into a small pure helper and make it the seam:

```python
def _task_env(task, config, phase) -> dict[str, str]:
    """Per-task isolation env. Unit-testable in isolation."""
    return setup_isolation(config, scope=f"task-{task.task_id}").env_vars   # H1 parameterization
```

Then:
- `_run_task_subprocess` calls `env_vars=_task_env(task, config, phase)` in its `_Base.__init__` (the #1 Path-B edit).
- Add an optional `_env_capture: list | Callable | None = None` param to `execute_phase_tasks` (sibling to `_subprocess_factory`, `executor.py:934`). When set, the loop records `_task_env(task, config, phase)` per iteration **before** the spawn (regardless of whether the real subprocess or the factory runs). A test then asserts each captured dict carries a **distinct** `CLAUDE_SETTINGS_DIR`.

This gives the H6 testable seam without coupling it to the (non-env) `_subprocess_factory` test path — the two seams stay orthogonal (factory = behavior/turns; env_capture = isolation correctness).

**Cross-effect:** `_task_env` becoming the single source of per-task env means Path B's #1 wiring and the H6 test seam are the SAME edit — implement once.

---

## 5. turns_consumed=0 (Stage 0)

**Exact return line** — `_run_task_subprocess`, `executor.py:1114-1118`:

```python
exit_code = proc._process.returncode if proc._process else -1
output_path = config.task_output_file(phase, task)
output_bytes = output_path.stat().st_size if output_path.exists() else 0
# Turn counting is wired separately in T02.06        # 1117  <-- existing-task reference (F-B / §6 Reconciliation note)
return (exit_code if exit_code is not None else -1, 0, output_bytes)   # 1118  <-- hardcoded 0
```

The middle element of the returned tuple is the literal `0`. The loop consumes it at `executor.py:1004/1009` as `turns_consumed`, feeds it into budget reconciliation (`executor.py:1028 actual = max(turns_consumed, 0)` → debit/credit at 1030-1033) and into `TaskResult(turns_consumed=turns_consumed)` (`executor.py:1038`). So the hardcoded `0` means **every task credits back its full `minimum_allocation`** (5 turns) at `executor.py:1032-1033` (since `0 < 5`) — the budget model is currently a no-op for per-task consumption, and `AggregatedPhaseReport.total_turns_consumed` (`executor.py:208,333`) under-reports.

**How real turn count would be captured:** the child runs with `--output-format stream-json` (`executor.py:1110`) and stdout is written to `config.task_output_file(phase, task)` (the `_stdout_fh`, `process.py:122`). Claude's stream-json emits a terminal `result` event carrying `num_turns` (and usage). The capture is: after `proc.wait()`, parse the output file for the final `result`-type JSON line and extract its turn count, e.g.

```python
turns = _parse_turns_from_stream_json(output_path)   # read last result event's num_turns
return (exit_code if exit_code is not None else -1, max(turns, 0), output_bytes)
```

A parser may already exist for the monitor/summarizer path (the `OutputMonitor`/`SummaryWorker` re-parse the same stream-json file — `executor.py:1166,1183`); R5/R1 should confirm whether `superclaude.cli.sprint.summarizer` or `OutputMonitor` already extracts `num_turns` to avoid duplicating a parser. **Reconciliation (F-B / §6 LOW):** the `# T02.06` comment at `executor.py:1117` references an existing turn-counting task — Stage 0's fix must fold into / supersede T02.06, and the acceptance test must assert the *correct* count, not merely `!= 0`.

---

## 6. TurnLedger thread-safety surface

`TurnLedger` is a plain `@dataclass` (`models.py:757-758`) with **no lock**. Mutating methods and the shared state they touch:

| Method | Line | Mutates | Read-modify-write? |
|---|---|---|---|
| `debit(turns)` | `models.py:786-790` | `self.consumed += turns` | yes (`+=`) |
| `credit(turns)` | `models.py:792-796` | `self.reimbursed += turns` | yes (`+=`) |
| `can_launch()` | `models.py:798-800` | reads `available()` = `initial_budget - consumed + reimbursed` | read-only but races a concurrent debit |
| `debit_wiring(turns)` | `models.py:806-818` | `consumed` (via debit) + `wiring_turns_used`, `wiring_analyses_count`, `wiring_budget_exhausted` | yes (multiple fields) |
| `credit_wiring(turns, rate)` | `models.py:820-835` | `reimbursed` (via credit) + `wiring_turns_credited` | yes |
| `available()` | `models.py:782-784` | read-only | — |
| `can_remediate()` / `can_run_wiring_gate()` | `models.py:802-804 / 837-841` | read-only | races concurrent mutators |

**Race surface under K>1:** the loop's check-then-act at `executor.py:976` (`if not ledger.can_launch()`) → `executor.py:992` (`ledger.debit(minimum_allocation)`) is a classic TOCTOU: two workers can both pass `can_launch()` then both `debit`, over-committing the budget. Plus the reconciliation `debit`/`credit` at `executor.py:1030-1033`. **Minimal fix for Stage 3:** add a `threading.Lock` (or `RLock`) to `TurnLedger` and guard `debit`/`credit`/`debit_wiring`/`credit_wiring`, AND make the **check-launch-debit a single atomic op** (e.g. a `try_launch() -> bool` method that locks, checks `can_launch`, debits `minimum_allocation`, returns success) — guarding the individual methods is NOT sufficient because the TOCTOU spans two calls. Stages 0-2 are safe via the sequential single-writer invariant (must be stated as a precondition per M2).

---

## 7. heading-regex router (M6)

**The regex** — `config.py:380-383`:

```python
_TASK_HEADING_RE = re.compile(
    r"^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)",
    re.MULTILINE,
)
```

Matches `### T<PP>.<TT>` at heading level exactly 3 (`###`), with a `--` / `-—` / `—` separator. Near-misses that silently FAIL to match (→ B→A demotion): `####` (level 4), `:` separator, en-dash only, missing the two-digit zero-pad, extra leading whitespace before `###` (anchored `^###` with `\s+` only AFTER `###`).

**Where it's used (parse):** `parse_tasklist`, `config.py:426`:

```python
headings = list(_TASK_HEADING_RE.finditer(content))
if not headings:
    _logger.warning("No task headings (### T<PP>.<TT>) found in tasklist content")  # 428
    return []                                                                        # 429
```

`parse_tasklist` returns `[]` when nothing matches.

**Where the fork decision is made (the global-routing change point)** — two layers:

1. `_parse_phase_tasks` — `executor.py:1121-1135`: calls `parse_tasklist(content, ...)` (`executor.py:1134`) and returns `tasks if tasks else None` (`executor.py:1135`). An empty list (no heading match) collapses to `None`.
2. `execute_sprint` fork — `executor.py:1264-1265`: `tasks = _parse_phase_tasks(phase, config)` then `if tasks:` → Path B (per-task), `else` (falls through to `executor.py:1309+`) → Path A (single session). **This `if tasks:` at `executor.py:1265` IS the fork**; `_parse_phase_tasks` returning `None`/`[]` is what silently routes a heading-typo phase to Path A (the B→A demotion hazard).

**M6 change point (warn-only, no reclassification):** the fix belongs in `_parse_phase_tasks` (`executor.py:1121-1135`) — after `parse_tasklist` returns empty, run a **looser near-miss probe** (e.g. a relaxed regex matching `#{2,5}\s*T\d{1,2}[._]\d{1,2}` or `T\d\d` followed by any separator) over the same content; if the strict regex found 0 but the loose probe finds ≥1, emit a LOUD `WARN` (heading-format near-miss → this phase will run as Path A single-session) but **return `None` unchanged** (do NOT auto-reroute). This is a global routing surface: it runs for **every** phase, so the regression corpus (M6 acceptance) must include existing Path-A freeform phases and confirm zero reclassification + zero false-positive warnings on legitimately freeform phases.

**Cross-effect:** because `_TASK_HEADING_RE` is also the parser's task-extraction regex (`config.py:426`), tightening/loosening the STRICT regex itself would change which blocks become `TaskEntry`s — so M6 must add a SEPARATE diagnostic probe, never widen `_TASK_HEADING_RE` in place.

---

## Summary of seams (one-liner per wiring point)

1. **H1 isolation merge** — Path A env at `executor.py:1327-1328` (`CLAUDE_WORK_DIR=isolation_dir`, phase-scoped); `setup_isolation`/`IsolationLayers.env_vars` (`executor.py:127-134, 151-183`) return `CLAUDE_WORK_DIR=release_dir` (CONFLICTS) + `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR`. Path B (`_run_task_subprocess`, `executor.py:1101-1111`) passes NO env. Fix: Path A merge ADD-only the 2 settings keys + re-pin `CLAUDE_WORK_DIR=isolation_dir`; Path B inject full `setup_isolation(config).env_vars`; parameterize `setup_isolation(config, scope=...)` for per-slot dirs. `build_env` (`process.py:97-112`) needs no change.
2. **build_task_context** — dead fn `process.py:257-319`; `results` accumulate in `execute_phase_tasks` (`executor.py:965` decl, `1066` append); thin prompt built in `_run_task_subprocess` (`executor.py:1090-1094`). Wire by threading `prior_context=build_task_context(results, ...)` as a new `_run_task_subprocess` param; runs in parent (no logger needed); `start_commit` not in scope (pass "").
3. **write_task_complete** — no such method (closest `write_task_rerun_complete`, `logging_.py:205-219`); call site slot = `executor.py:1066` (after `results.append`). BLOCKER: `SprintLogger` not passed into `execute_phase_tasks` — thread `logger=` param (call site `executor.py:1270-1279` has it) or post-hoc loop in `execute_sprint`. Emit `event:"task_complete"` mirroring rerun schema; `_jsonl` (`logging_.py:265-267`) lock-free.
4. **_subprocess_factory env seam** — factory returns tuple directly (`executor.py:1004-1006`), bypassing `build_env`. Real path's env lives in `_run_task_subprocess`→`_Base.__init__(env_vars=...)`. Extract `_task_env(task,config,phase)` helper + add `_env_capture` param to `execute_phase_tasks` (sibling to `_subprocess_factory` @934) so a test asserts per-worker distinct `CLAUDE_SETTINGS_DIR`. Same edit as #1 Path B.
5. **turns_consumed=0** — literal in return tuple `executor.py:1118`; comment `# T02.06` @1117 references existing turn task. Capture by parsing the stream-json output file (`config.task_output_file`) final `result` event's `num_turns` after `proc.wait()`. Check `summarizer`/`OutputMonitor` for an existing parser.
6. **TurnLedger thread-safety** — plain `@dataclass` (`models.py:757`), no lock. RMW mutators: `debit` (@786), `credit` (@792), `debit_wiring` (@806), `credit_wiring` (@820). Check-then-act TOCTOU spans `can_launch()` (@798, executor `976`) → `debit` (executor `992`); needs an atomic `try_launch()` + a lock, not just per-method guards.
7. **heading router (M6)** — `_TASK_HEADING_RE` (`config.py:380-383`) used in `parse_tasklist` (`config.py:426`); fork decision = `if tasks:` at `executor.py:1265` (via `_parse_phase_tasks` `executor.py:1121-1135` returning `None`/`[]`). M6 warn-only fix belongs in `_parse_phase_tasks`: add a SEPARATE near-miss probe, WARN but do NOT reroute; never widen `_TASK_HEADING_RE` in place (it's also the extraction regex).

**Two edits collapse into one each:** #1-PathB and #4 are the same `_task_env` injection; #2, #3, #5 all want `logger`/`results`/context threaded into `execute_phase_tasks` (or `_run_task_subprocess`), so the cleanest Stage-0/1 change is to widen those two signatures once and route logger + prior-results + handoff-store through them.
