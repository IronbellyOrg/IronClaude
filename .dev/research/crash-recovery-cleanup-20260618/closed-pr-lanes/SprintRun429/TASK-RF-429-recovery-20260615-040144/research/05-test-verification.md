# Research: Test & Verification

**Status:** Complete
**Date:** 2026-06-15
**Researcher:** R5 (Test & Verification)
**Scope:** EXCLUSIVE on tests — `tests/sprint/` tree, subprocess_factory seam, fixtures, doc⇆CLI parity, back-compat round-trip. (R1 inventory / R2 idioms / R3 wiring / R4 data flow / R6 template cover the rest.)

---

## 0. TL;DR for the builder

- Sprint test home: **`tests/sprint/`** (flat dir, one `test_<concept>.py` per module; `conftest.py` autouse-stubs the narrative subprocess). UV only: `uv run pytest tests/sprint/ -v`.
- **No fixtures dir exists yet under `tests/sprint/`.** Create **`tests/sprint/fixtures/exhaustion/`** (new). Convention across the repo is `tests/<area>/fixtures/<group>/` (e.g. `tests/audit/fixtures/...`, `tests/swarm/fixtures/...`, `tests/cli/eval/fixtures/...`). The 6 `.jsonl` files go there.
- **The executor seam is a factory that returns `(exit_code, turns_consumed, output_bytes)` AND writes the transcript to `config.task_output_file(phase, task)` itself.** The status ladder then reads that path. To drive the re-spawn loop, the factory must write a **different transcript per call** keyed off a call counter (the "scripted per-attempt transcript factory").
- **`detect_provider_failure` unit tests** mirror `TestDetectErrorMaxTurns` in `tests/sprint/test_monitor.py` exactly: `out = tmp_path/"output.txt"; out.write_text(<json lines>); assert detect_provider_failure(out) == <signal>`.
- **doc⇆CLI parity** has a gold-standard template: `tests/cli/reflect/test_docs_cli_parity.py`. Mirror it for `--max-session-resets` against `docs/guides/sprint-cli-tools-release-guide.md` + the Click `run` command. There is ALSO a lighter `--help`-string parity test (`tests/sprint/test_cli_contract.py`) — author BOTH (help-surface + guide-vs-Click).
- **Back-compat round-trip**: `TaskResult.from_dict` is **hard-keyed today** (`models.py:218-240`); the new `failure_class`/`session_resets`/`exhausted_model` fields MUST be read with `.get(default)`. Test = load an OLD dict (no new fields) → `TaskResult.from_dict` succeeds + new fields default; AND a NEW dict round-trips `to_dict→from_dict` preserving them.
- **Resume-safety** template: `tests/sprint/test_resume.py::TestResumePlanner` — write `results/phase-N-result.json` with `task_results:[{task:{task_id},status:"fail_provider_exhausted"}]`, then `ResumePlanner().plan(index)` and assert the exhausted id IS in `plan.rerun_task_ids` and the phase is NOT COMPLETE.

---

## 1. Sprint test layout & conventions (VERIFIED)

`tests/sprint/` is a **flat** directory (~90 `test_*.py` files); subfolders only for `e2e_real/` and `diagnostic/`. One `test_<concept>.py` per production module. The new-test ownership map for this feature:

| New production surface | Test file to extend / create | Why |
|---|---|---|
| `detect_provider_failure` / `_provider_failure_from_text` / `ProviderFailure` (monitor.py) | **`tests/sprint/test_monitor.py`** (extend) | Detector siblings already tested here (`TestDetectErrorMaxTurns`, `tests/sprint/test_monitor.py:137-183`). |
| `TaskStatus.FAIL_PROVIDER_EXHAUSTED` + is_failure; `PhaseStatus.PROVIDER_EXHAUSTED`; `TaskResult` new fields back-compat; `build_account_exhaustion_halt` | **`tests/sprint/test_models.py`** (extend) | Enum membership/property + serialization tests live here (`tests/sprint/test_models.py:35-123`). |
| `_classify_transcript` 429 branch alignment (rerun_tasks.py) | **`tests/sprint/test_rerun_tasks.py`** (extend) | `discover_failed_tasks_from_transcripts` classifier tests are here (`tests/sprint/test_rerun_tasks.py:280-328`). |
| Per-task re-spawn loop / latch / persistence (executor.py) | **`tests/sprint/test_executor.py`** (extend `TestPerTaskOrchestration`) | All `_subprocess_factory` scenarios are here (`tests/sprint/test_executor.py:601-889`+). |
| Single-session phase re-spawn (executor.py P4) | **`tests/sprint/test_executor.py`** (`TestExecuteSprintIntegrationCoverage`, `:335`) OR `test_multi_phase.py` | Single-session `execute_sprint` path patches `subprocess.Popen` directly (`:336-381`). |
| `SessionResetPolicy.decide` truth table (recovery_policy.py NEW) | **`tests/sprint/test_recovery_policy.py`** (NEW) | New module ⇒ new test file (mirrors `test_recovery.py` ↔ `recovery.py`). |
| `aienv.py` `suggest_alternate_model` (NEW) | **`tests/sprint/test_aienv.py`** (NEW) | New module ⇒ new test file. |
| `--max-session-resets` doc⇆CLI parity | **`tests/sprint/test_cli_contract.py`** (help surface) + **`tests/sprint/test_sprint_docs_cli_parity.py`** (NEW, guide-vs-Click) | Two layers: see §6. |
| Resume re-runs exhausted task | **`tests/sprint/test_resume.py`** (extend `TestResumePlanner`) | `ResumePlanner().plan` tests here (`:100-153`). |

**Pytest conventions (VERIFIED `pyproject.toml:111-131`):**
- `--strict-markers` is ON. Registered markers include `unit`, `integration`, `backward_compat` (`pyproject.toml:114-131`). Use `@pytest.mark.backward_compat` for the TaskResult round-trip test; `@pytest.mark.unit` for the pure detector/policy tests; `@pytest.mark.integration` for the factory-driven executor scenarios (they exercise the orchestration loop).
- Tests use **`tmp_path`** throughout; module-level `_helper()` functions (NOT fixtures) for setup — see `tests/sprint/test_rerun_tasks.py:74-92`, `test_executor.py:35-54`.
- No `conftest` fixture is required for the new tests; the autouse `_stub_phase_narrative` (`tests/sprint/conftest.py:32-55`) already neutralises the narrative-subprocess leak for the whole suite.
- **Command:** `uv run pytest tests/sprint/test_monitor.py tests/sprint/test_executor.py -v` (never bare `pytest`/`python -m`).

---

## 2. The subprocess_factory / _subprocess_factory seam (THE crux — VERIFIED)

**Production signature** (`src/superclaude/cli/sprint/executor.py:963-993`):
```python
def _run_one_task(task, config, phase, *, started_at, prior_context="",
                  ledger=None, subprocess_factory=None, shadow_metrics=None,
                  remediation_log=None, lock=None) -> tuple[TaskResult, TrailingGateResult|None]:
    if subprocess_factory is not None:
        exit_code, turns_consumed, output_bytes = subprocess_factory(task, config, phase)
    ...
    task_output_path = config.task_output_file(phase, task)   # <- ladder reads THIS path
    if exit_code == 0: status = PASS
    elif exit_code == 124: status = INCOMPLETE
    elif detect_error_max_turns(path) and _task_completed_before_overrun(path): status = PASS_RECOVERED
    elif _is_transient_failure(path): status = FAIL_RECOVERABLE
    else: status = FAIL_TERMINAL
```

**Two seam entry points** (both kwargs):
- `execute_phase_tasks(tasks, config, phase, *, ledger=None, _subprocess_factory=None, ...)` — the public entry the tests call (`executor.py:1190-1219`).
- `_execute_phase_tasks_parallel(..., _subprocess_factory=None)` (`executor.py:1048-1141`) — for K>1; passes `subprocess_factory=_subprocess_factory` into `_run_one_task`.

**The contract that matters for authoring tests (VERIFIED against `test_executor.py`):**
1. The factory is called as `factory(task, config, phase)` and **returns a 3-tuple** `(exit_code, turns_consumed, output_bytes)`.
   - Simple factories that don't need a transcript just return the tuple: `_pass_factory` returns `(0, 3, 1024)`; `_fail_factory` returns `(1, 5, 512)` (`test_executor.py:615-623`).
2. **The status ladder reads `config.task_output_file(phase, task)`** = `results_dir/phase-{N}-task-{task_id}-output.txt` (VERIFIED `models.py:693-694`). So when the classification depends on transcript CONTENT (which it does for 429 detection), the factory MUST **write that exact file** before returning. The existing pattern (`test_executor.py:743-755`):
```python
out = config.task_output_file(phase, tasks[0])
out.parent.mkdir(parents=True, exist_ok=True)   # results_dir does NOT pre-exist under release_dir=tmp_path
out.write_text('{"type":"content","text":"working..."}\n'
               '{"type":"result","subtype":"success","is_error":false}\n'
               '{"type":"result","subtype":"error_max_turns","is_error":true,"num_turns":101}\n')
def overran_after_completion_factory(task, config, phase):
    return (1, 101, out.stat().st_size)
results, _, _gate = execute_phase_tasks(tasks, config, phase,
                                        _subprocess_factory=overran_after_completion_factory)
assert results[0].status == TaskStatus.PASS_RECOVERED
```

**Worked example — the scripted per-attempt transcript factory (for the re-spawn LOOP, P3):**

The re-spawn loop will call `_run_one_task`/the factory MULTIPLE times for the same task. To script per-attempt behaviour, the factory keys off a call counter and writes a DIFFERENT transcript each call:

```python
def _make_scripted_factory(config, phase, scripts):
    """scripts: list of (exit_code, transcript_text). One entry consumed per spawn.
    Writes config.task_output_file(phase, task) each call so the detector/ladder
    sees the per-attempt transcript. Returns (factory, calls) so tests assert spawn count."""
    calls = {"n": 0}
    def factory(task, config_, phase_):
        i = calls["n"]
        exit_code, text = scripts[min(i, len(scripts) - 1)]
        out = config_.task_output_file(phase_, task)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        calls["n"] += 1
        return (exit_code, 5, out.stat().st_size)
    return factory, calls

# single-429 → clean ⇒ PASS, session_resets==1
factory, calls = _make_scripted_factory(config, phase, [
    (1, SINGLE_ACCOUNT_429_TEXT),   # attempt 1: re-route
    (0, CLEAN_PASS_TEXT),           # attempt 2: success
])
results, _, _ = execute_phase_tasks(tasks, config, phase, _subprocess_factory=factory,
                                    reset_policy=SessionResetPolicy(max_session_resets=8))  # NEW param (P3)
assert calls["n"] == 2
assert results[0].status == TaskStatus.PASS
assert results[0].session_resets == 1   # persisted on TaskResult
```

> **IMPORTANT for the builder:** the re-spawn loop adds a **new shared param** (`reset_policy`/latch) to `_run_one_task` AND `execute_phase_tasks`/`_execute_phase_tasks_parallel` (spec §4 Layer 3, `executor.py:963-975`). The factory-driven tests will pass that param explicitly. If P3 chooses to keep the loop INSIDE `_run_one_task`, the factory's call-counter still observes every re-spawn because the spawn delegates to the factory each iteration. Confirm the exact param name with R3's wiring notes before writing the test signature.

**Spawn-count assertions** use the call-counter pattern already in the suite: `spawn_count = [0]; def counting_factory(...): spawn_count[0]+=1; ...; assert spawn_count[0] == 3` (`test_executor.py:625-639`).

---

## 3. The 6 fixtures — exact target dir + minimal JSON (from spec §2 verbatim)

**Target dir (NEW):** `tests/sprint/fixtures/exhaustion/`
**Shape:** stream-json NDJSON, one JSON object per line, matching the subprocess `--output-format stream-json` transcript. The detector parses the **LAST `{"type":"result"}` event** and keys on `is_error` + `api_error_status` + the `result` body string. **Never key on `subtype`** (it is `"success"` even when `is_error` is true — spec §2, edge case #10).

> **Note (verbatim sourcing):** spec §2 lists the real Octodive transcripts (`results/phase-3-task-T03.14-output.txt` etc.) as fixture sources, but they are **NOT reachable from this IronClaude worktree** (spec §2 lines 98-103). Author the `.jsonl` fixtures **from the verbatim JSON in spec §2** (the 3 event types + 2 body strings). The minimal forms below are sufficient for unit detection; the `all_account_cooldown` fixture SHOULD additionally carry a few real prior-token `assistant` lines so the "after real work (num_turns=25)" shape is represented.

### 3.1 `single_account_429.jsonl` → `ProviderFailure.SINGLE_ACCOUNT_LIMIT`
```jsonl
{"type":"system","subtype":"api_retry","error_status":429,"error":"rate_limit","attempt":3,"max_retries":10}
{"type":"assistant","message":{"model":"<synthetic>"},"error":"rate_limit"}
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"result":"API Error: Request rejected (429) · This request would exceed your account's rate limit. Please try again later."}
```

### 3.2 `all_account_cooldown.jsonl` → `ProviderFailure.ALL_ACCOUNT_COOLDOWN` (+ resolved model captured)
```jsonl
{"type":"assistant","message":{"usage":{"output_tokens":256}}}
{"type":"assistant","message":{"usage":{"output_tokens":312}}}
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"result":"API Error: Request rejected (429) · All credentials for model claude-opus-4-8 are cooling down via provider claude"}
```
> The resolved-model capture group (`_RE_ALL_ACCOUNT` named group `model`) must extract `claude-opus-4-8`. Add ≥1 prior `output_tokens` line so a num_turns>0 / "real prior work" assertion is available.

### 3.3 `operation_timeout.jsonl` → `ProviderFailure.OPERATION_TIMEOUT` (distinct class, NOT exhaustion)
```jsonl
{"type":"assistant","message":{"usage":{"output_tokens":64}}}
{"type":"result","subtype":"success","is_error":true,"api_error_status":null,"result":"API Error: The operation timed out."}
```
> Discriminator: `is_error==true && api_error_status==null && result=="API Error: The operation timed out."` (spec §2 line 91). Must NOT be classified as a 429 signal.

### 3.4 `api_retry_maxed.jsonl` → in-session retry already burned (`attempt==max_retries==10`)
```jsonl
{"type":"system","subtype":"api_retry","error_status":429,"error":"rate_limit","attempt":10,"max_retries":10}
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"result":"API Error: Request rejected (429) · This request would exceed your account's rate limit. Please try again later."}
```
> Asserts the detector still returns `SINGLE_ACCOUNT_LIMIT` (the `api_retry attempt==max_retries` is corroborating context for "sprint-level in-session retry is pointless" — edge case #6 — but the LOAD-BEARING classification is the last result event).

### 3.5 `task_failure_real.jsonl` → `ProviderFailure.NONE` (genuine task failure, no 429 body)
```jsonl
{"type":"assistant","message":{"usage":{"output_tokens":512}}}
{"type":"result","subtype":"error_during_execution","is_error":true,"result":"Tool execution failed: pytest exited 1"}
```
> `is_error==true` but **no `api_error_status==429` and no 429 body** ⇒ detector returns NONE; the existing FAIL_TERMINAL/FAIL_RECOVERABLE ladder must still apply (NO re-spawn). This is the false-positive guard.

### 3.6 `clean_pass.jsonl` → `ProviderFailure.NONE` (success envelope)
```jsonl
{"type":"assistant","message":{"usage":{"output_tokens":256}}}
{"type":"result","subtype":"success","is_error":false,"api_error_status":null,"result":"Task complete."}
```

---

## 4. How fixtures are loaded (VERIFIED conventions)

Two equally-valid loaders are used in the repo; pick **(A)** for the new detector/classifier unit tests because the detector reads a **path**:

**(A) Path-based (for `detect_provider_failure(output_path)`):** copy/point the detector at the fixture file. Resolve the fixtures dir relative to the test file (CWD-agnostic), mirroring `test_docs_cli_parity.py:26`:
```python
from pathlib import Path
_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "exhaustion"

def test_single_account_detected():
    sig = detect_provider_failure(_FIXTURES / "single_account_429.jsonl")
    assert sig.kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT
```

**(B) Text-based (for `_provider_failure_from_text(text)` and `_classify_transcript(text)`):** read the fixture and pass the string:
```python
text = (_FIXTURES / "all_account_cooldown.jsonl").read_text(encoding="utf-8")
assert _provider_failure_from_text(text).kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN
assert _classify_transcript(text) is TaskStatus.FAIL_PROVIDER_EXHAUSTED   # P2 alignment
```

> The `rerun_tasks._classify_transcript` test (P2) reuses the SAME fixtures via the text loader — this is the "single source of truth" assertion the spec wants (one fixture set proving live-detector and offline-classifier agree, preventing the PR #160 doc⇆code seam drift).

**Inline alternative (also valid, used heavily in `test_monitor.py`):** small `tmp_path` transcripts written inline with `out.write_text(...)` — appropriate for negative/edge cases (truncated, empty, missing file, `subtype`-trap) where a named fixture file would be overkill. Mirror `test_monitor.py:158-183`:
```python
def test_truncated_degrades_to_none(tmp_path):
    out = tmp_path / "output.txt"; out.write_text('{"type":"result","api_err')
    assert detect_provider_failure(out).kind is ProviderFailure.NONE   # OSError/parse-tolerant
def test_ignores_subtype_success_trap(tmp_path):
    out = tmp_path / "output.txt"
    out.write_text('{"type":"result","subtype":"success","is_error":true,"api_error_status":429,'
                   '"result":"API Error: Request rejected (429) · This request would exceed your account\\'s rate limit."}\n')
    assert detect_provider_failure(out).kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT
def test_missing_file(tmp_path):
    assert detect_provider_failure(tmp_path / "nope.txt").kind is ProviderFailure.NONE
```
**Recommendation:** 6 named fixtures for the canonical positive cases (shared across detector+classifier+executor tests); inline `tmp_path` writes for the tolerance/trap edges.

---

## 5. Per-test-item checklist (one file/fixture per item — A3 granularity)

### P1 — Detector unit tests (extend `tests/sprint/test_monitor.py`)
New class `TestDetectProviderFailure` (mirror `TestDetectErrorMaxTurns:137-183`). One assertion-test per row of the four-way discrimination + tolerance edges:
1. `single_account_429.jsonl` → `SINGLE_ACCOUNT_LIMIT`
2. `all_account_cooldown.jsonl` → `ALL_ACCOUNT_COOLDOWN` + resolved model `claude-opus-4-8` captured
3. `operation_timeout.jsonl` → `OPERATION_TIMEOUT` (NOT a 429 signal)
4. `task_failure_real.jsonl` → `NONE`
5. `clean_pass.jsonl` → `NONE`
6. `api_retry_maxed.jsonl` → `SINGLE_ACCOUNT_LIMIT`
7. truncated/empty/missing-file → `NONE` (parse/OSError tolerance)
8. `subtype:"success"` + `is_error:true` + `api_error_status:429` → still `SINGLE_ACCOUNT_LIMIT` (subtype-trap)
9. 429 with neither body regex → `SINGLE_ACCOUNT_LIMIT` (conservative default, spec §4 Layer 1 line 159)
10. `_provider_failure_from_text` (the text-core) returns the same signal as the path wrapper for one shared fixture (proves the shared core)

### P2 — Taxonomy + serialization (extend `tests/sprint/test_models.py`) + classifier alignment (extend `tests/sprint/test_rerun_tasks.py`)
- `TaskStatus.FAIL_PROVIDER_EXHAUSTED` exists, `.value == "fail_provider_exhausted"`, `.is_failure is True`, `.is_success is False` (mirror `TestTaskStatus` membership tests, `test_models.py:35-123`).
- `PhaseStatus.PROVIDER_EXHAUSTED` exists; assert its `is_terminal`/`is_success`/`is_failure` placement (mirror `test_models.py:38-110`).
- **Back-compat round-trip** (`@pytest.mark.backward_compat`) — see §7.
- `build_account_exhaustion_halt(...)` golden-string — see §8.
- **Classifier alignment** (`test_rerun_tasks.py`, mirror `test_discover_failed_tasks_via_is_error:280-301`): feed the cooldown + single-429 fixtures through `discover_failed_tasks_from_transcripts` (or `_classify_transcript` directly) and assert the result is `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (today it would be FAIL_TERMINAL — this is the RED→GREEN). Also assert `task_failure_real.jsonl` → still `FAIL_TERMINAL` (no over-capture).

### P3/P4 — Executor factory scenarios (extend `tests/sprint/test_executor.py::TestPerTaskOrchestration`)
See §6 for the full enumeration (6 loop scenarios + single-session).

### P5 — `recovery_policy` (NEW `test_recovery_policy.py`), `aienv` (NEW `test_aienv.py`), CLI/doc parity, UX golden-string
See §8 + §9.

---

## 6. Policy truth-table + executor loop scenarios

### 6.1 `SessionResetPolicy.decide` truth table (NEW `tests/sprint/test_recovery_policy.py`)
Pure unit test, no subprocess. Parametrize over (signal × attempt):
```python
import pytest
from superclaude.cli.sprint.recovery_policy import SessionResetPolicy, Action
from superclaude.cli.sprint.monitor import ProviderFailure

@pytest.mark.unit
@pytest.mark.parametrize("signal,attempt,expected", [
    (ProviderFailure.ALL_ACCOUNT_COOLDOWN, 0, Action.HALT_MODEL_SWITCH),   # fast path on FIRST attempt
    (ProviderFailure.ALL_ACCOUNT_COOLDOWN, 5, Action.HALT_MODEL_SWITCH),
    (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 0, Action.RETRY_NEW_SESSION),
    (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 7, Action.RETRY_NEW_SESSION),   # attempt < cap(8)
    (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 8, Action.HALT_MODEL_SWITCH),   # attempt == cap → halt
    (ProviderFailure.OPERATION_TIMEOUT, 0, Action.CONTINUE),
    (ProviderFailure.NONE, 0, Action.CONTINUE),
])
def test_decide_truth_table(signal, attempt, expected):
    assert SessionResetPolicy(max_session_resets=8).decide(signal, attempt) is expected
```
> Confirm the exact `decide` boundary (`attempt < max` vs `<=`) against spec §4 Layer 3 line 217 (`attempt < self.max_session_resets`) — at `attempt == cap` it halts.

### 6.2 Executor re-spawn loop scenarios (spec §6 "Executor" block — VERIFIED authoring path)
Use the scripted per-attempt factory from §2. Each is one test in `TestPerTaskOrchestration` (or a sibling `TestProviderExhaustionRecovery` class):

| # | Scenario | Scripted attempts | Asserts |
|---|---|---|---|
| 1 | single-429 → clean ⇒ PASS | `[(1,SINGLE_429),(0,CLEAN)]` | `calls==2`; `status==PASS`; `result.session_resets==1` |
| 2 | cooldown on attempt 1 ⇒ fast-path halt, **0 extra spawns** | `[(1,COOLDOWN)]` | `calls==1`; `status==FAIL_PROVIDER_EXHAUSTED`; `result.exhausted_model=="claude-opus-4-8"` |
| 3 | single-429 × cap ⇒ halt | `[(1,SINGLE_429)]*999` | `calls==cap` (default 8); `status==FAIL_PROVIDER_EXHAUSTED`; persisted `halt_reason=="provider_exhaustion"` |
| 4 | single-429 → real failure ⇒ 2nd attempt classified normally, no further re-spawn | `[(1,SINGLE_429),(1,TASK_FAILURE_REAL)]` | `calls==2`; `status==FAIL_TERMINAL` (NOT exhausted) |
| 5 | K>1 all-429 ⇒ single latch halt; **total spawns < K×cap AND ≤ cap+(K−1)** | each worker `[(1,SINGLE_429)]*999` | global latch trips once; assert `total_spawns < K*cap` and `<= cap + (K-1)` (edge case #3 — NOT strictly ≤ cap) |
| 6 | always-429 single ⇒ exactly `cap` spawns (no infinite loop) | `[(1,SINGLE_429)]*999`, cap small (e.g. 3) | `calls==3` exactly (infinite-loop guard, edge case #9) |

**Scenario 5 (K>1 latch) authoring:** drive via `_execute_phase_tasks_parallel(..., _subprocess_factory=...)` with a shared, thread-safe call counter (use a `threading.Lock` around the counter in the test factory; the suite already has K>1 parallel tests — see `test_handoff_concurrency.py`, `test_turn_ledger_concurrency.py` for the concurrency harness idiom). Pass a shared `SessionResetPolicy` carrying the `_latch_tripped` flag. The assertion is a **bound**, not equality: `assert cap <= total <= cap + (K-1)` and `assert total < K * cap`.

**Persistence assertions (P3):** after a halt scenario, read `config.results_dir/phase-{N}-result.json` and assert top-level `halt_reason == "provider_exhaustion"` and `exhausted_model` present (`_write_phase_result_json`, executor.py:2657-2701 per research-notes). The `TaskResult` for the halted task carries `session_resets`/`failure_class`/`exhausted_model` (assert on the in-memory `results[0]` AND on the reloaded json).

**Single-session path (P4, `tests/sprint/test_executor.py::TestExecuteSprintIntegrationCoverage`):** mirror `test_execute_sprint_halt:383-434` — patch `subprocess.Popen` with a factory that writes the cooldown transcript to `config.output_file(phase)` (note: single-session uses `output_file`, NOT `task_output_file`), then assert `captured[0].phase_results[0].status == PhaseStatus.PROVIDER_EXHAUSTED` and `outcome == SprintOutcome.HALTED`.

---

## 7. Back-compat round-trip (extend `tests/sprint/test_models.py`)

**VERIFIED problem:** `TaskResult.from_dict` (`src/superclaude/cli/sprint/models.py:218-240`) is **hard-keyed** for all result-level fields (`data["status"]`, `data["turns_consumed"]`, …). New fields `failure_class`/`session_resets`/`exhausted_model` MUST be added with `.get(<default>)` (the `HandoffRecord` forward-compat `.get()` idiom, research-notes line 24). Test both directions:

```python
import pytest
from datetime import datetime, timezone
from superclaude.cli.sprint.models import TaskEntry, TaskResult, TaskStatus, GateOutcome

@pytest.mark.backward_compat
def test_taskresult_from_dict_old_payload_round_trips():
    """A v4.3.0 phase-N-result.json (no exhaustion fields) must still load,
    new fields defaulting — guards the hard-keyed→.get() migration."""
    old = {
        "task": {"task_id": "T03.14", "title": "t", "description": "",
                 "dependencies": [], "command": "", "classifier": ""},
        "status": "fail_terminal", "turns_consumed": 5, "exit_code": 1,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "output_bytes": 100, "gate_outcome": "pending",
        "reimbursement_amount": 0, "output_path": "",
        # NOTE: no failure_class / session_resets / exhausted_model
    }
    tr = TaskResult.from_dict(old)          # must NOT KeyError
    assert tr.failure_class == ""
    assert tr.session_resets == 0
    assert tr.exhausted_model == ""

@pytest.mark.backward_compat
def test_taskresult_new_fields_round_trip():
    """to_dict→from_dict preserves the new exhaustion fields."""
    tr = TaskResult(
        task=TaskEntry(task_id="T03.14", title="t"),
        status=TaskStatus.FAIL_PROVIDER_EXHAUSTED,
        failure_class="provider_exhaustion", session_resets=3,
        exhausted_model="claude-opus-4-8",
    )
    back = TaskResult.from_dict(tr.to_dict())
    assert back.status is TaskStatus.FAIL_PROVIDER_EXHAUSTED
    assert back.failure_class == "provider_exhaustion"
    assert back.session_resets == 3
    assert back.exhausted_model == "claude-opus-4-8"
```
> Field names/defaults per spec §4 Layer 2 (lines 199-201): `failure_class: str = ""`, `session_resets: int = 0`, `exhausted_model: str = ""`.

---

## 8. UX golden-string + `aienv` tests

### 8.1 `build_account_exhaustion_halt` golden-string (extend `tests/sprint/test_models.py`)
Mirror the existing resume-output tests (`test_models.py:367-389` `test_resume_command_when_halted`). Assert the **single-line** resume command (terminal cannot paste multi-line — `feedback_no_multiline_paste`), the named exhausted model, the distinct suggested model, and the CLIProxyAPI rationale:
```python
def test_account_exhaustion_halt_is_single_line_actionable(tmp_path):
    config = _make_config(tmp_path)   # reuse the test_executor _make_config idiom
    msg = build_account_exhaustion_halt(
        config, halt_task_id="T03.14", exhausted_model="claude-opus-4-8",
        suggested_model="sonnet", remaining_tasks=["T03.14","T03.15"], ledger=None)
    # single-line resume command (no embedded newline in the command line itself)
    resume_lines = [l for l in msg.splitlines() if "--resume" in l]
    assert len(resume_lines) == 1
    assert "--resume T03.14" in resume_lines[0]
    assert "--model sonnet" in resume_lines[0]
    assert "claude-opus-4-8" in msg            # names the exhausted model
    assert "CLIProxyAPI" in msg or "route" in msg.lower()   # rationale present
```
> Also a None-safe case: no alternate alias ⇒ message must NOT fabricate one (edge case #7) — assert it shows the exhausted model + generic guidance and the suggested-model field is absent/empty.

### 8.2 `aienv.py` (NEW `tests/sprint/test_aienv.py`)
Parse a **fixture `~/.aienv`** (write to `tmp_path`, point the parser at it — do NOT read the real `~/.aienv`). `suggest_alternate_model` returns the next distinct alias:
```python
@pytest.mark.unit
def test_suggest_alternate_for_opus(tmp_path):
    aienv = tmp_path / ".aienv"
    aienv.write_text(
        'export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8\n'
        'export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5\n'
        'export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5\n')
    assert suggest_alternate_model("claude-opus-4-8", aienv_path=aienv) == "sonnet"  # or the sonnet resolved id

@pytest.mark.unit
def test_suggest_alternate_for_proxy_alias(tmp_path):
    aienv = tmp_path / ".aienv"
    aienv.write_text('export IC_ALIASES="T0Model01 T0Model02 T0Model03"\n')   # confirm real format w/ R1
    assert suggest_alternate_model("T0Model01", aienv_path=aienv) == "T0Model02"

@pytest.mark.unit
def test_no_alternate_returns_none_safe(tmp_path):
    aienv = tmp_path / ".aienv"
    aienv.write_text('export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8\n')
    assert suggest_alternate_model("claude-opus-4-8", aienv_path=aienv) is None  # only slot → no alt
```
> **Builder must confirm with R1/R3** the real `~/.aienv` export names (`T*Model0N` vs `IC_ALIASES`) and the `suggest_alternate_model` signature (whether it takes an `aienv_path` kwarg for testability — it SHOULD, so the test never touches the real home file). Per memory `feedback_aienv_only_proxy_contract`, the proxy contract is `:4000/cli` + models `T2Model01..NN`; the fixture should reflect that naming.

---

## 9. doc⇆CLI parity for `--max-session-resets` (TWO layers)

### 9.1 Help-surface layer (extend `tests/sprint/test_cli_contract.py::TestCLIContract`)
Cheapest guard — assert the flag appears in `sprint run --help` (mirror `test_run_help:31-43`):
```python
from click.testing import CliRunner
from superclaude.cli.sprint.commands import sprint_group

def test_run_help_exposes_max_session_resets():
    result = CliRunner().invoke(sprint_group, ["run", "--help"])
    assert result.exit_code == 0
    assert "--max-session-resets" in result.output
```

### 9.2 Guide-vs-Click parity layer (NEW `tests/sprint/test_sprint_docs_cli_parity.py`)
**Mirror `tests/cli/reflect/test_docs_cli_parity.py` exactly** (the canonical pattern that closed the PR #160 doc⇆code drift). Key adaptations:
- Click command source: `from superclaude.cli.sprint.commands import run` (confirm the run command symbol name with R3 — the group is `sprint_group`; the subcommand callback may be `run`).
- Guide path: `Path(__file__).resolve().parents[2] / "docs" / "guides" / "sprint-cli-tools-release-guide.md"` (VERIFIED this guide exists). **NOTE depth:** `test_sprint_docs_cli_parity.py` lives at `tests/sprint/<file>` ⇒ `parents[2]` == repo root (the reflect template is at `tests/cli/reflect/<file>` ⇒ `parents[3]`). Adjust the `parents[N]` index for the shallower path.
- Reuse the two test bodies: `test_documented_flags_match_cli_flags` (guide option bullets == Click `--long` flag set) and `test_documented_defaults_match_cli_defaults` (the `--max-session-resets` default `8` stated as ``Default: `8` `` in the guide — spec §7 P5).

> **Builder action (doc):** P5 must ADD a `### Key options` (or equivalent option-bullet) entry for `--max-session-resets` to `docs/guides/sprint-cli-tools-release-guide.md` stating `Default: `8``, or the new parity test's `missing = cli - documented` assertion fails. This is the doc⇆CLI parity contract from `feedback_doc_fanout_facts_sheet` (CLI docs get a doc⇆CLI parity test). Verify whether the sprint guide already has a `### Key options`-style section before reusing the reflect test's section-slicing logic; if its option list uses a different heading/format, adapt `_key_options_section()` / `_OPTION_BULLET_RE` to the sprint guide's actual structure (UNVERIFIED: the sprint guide's internal heading layout was not inspected — builder must Read it before writing the slicer).

---

## 10. Resume-safety test (extend `tests/sprint/test_resume.py::TestResumePlanner`)

Mirror `test_resume_task_level_recoverable:120-153`. Write a `phase-N-result.json` with the new status string, then assert the planner re-runs it:
```python
def test_resume_reruns_provider_exhausted_task(self, tmp_path):
    results = tmp_path / "results"; results.mkdir()
    for n in (1, 2, 3):
        (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
    index = _write_index(tmp_path, (1, 2, 3))
    events = _complete_phase(results, 1) + _complete_phase(results, 2)
    (results / "phase-3-result.json").write_text(json.dumps({
        "phase": 3, "status": "provider_exhausted",
        "task_results": [
            {"task": {"task_id": "T03.01"}, "status": "pass"},
            {"task": {"task_id": "T03.02"}, "status": "fail_provider_exhausted"},
        ]}))
    events += [{"event": "phase_start", "phase": 3},
               {"event": "phase_complete", "phase": 3, "status": "provider_exhausted"}]
    _write_log(tmp_path, events)

    plan = ResumePlanner().plan(index)
    assert "T03.02" in plan.rerun_task_ids        # exhausted task IS re-run
    assert plan.granularity is Granularity.TASK
```
> VERIFIED the planner re-runs any task whose persisted status is not `is_success` (research-notes line 39, `planner.py:160-164`); since `FAIL_PROVIDER_EXHAUSTED` is added to `is_failure` (P2), `_coerce_task_status("fail_provider_exhausted") → TaskStatus(...)` auto-resolves and it's re-run. No separate planner edit. The test PROVES this end-to-end. Reuse the module-level `_task_block` / `_write_index` / `_complete_phase` / `_write_log` helpers already in `test_resume.py` (do NOT re-derive them).

---

## 11. Verification commands (UV only — copy-ready, single-line)

```
uv run pytest tests/sprint/test_monitor.py -v
uv run pytest tests/sprint/test_models.py -v
uv run pytest tests/sprint/test_rerun_tasks.py -v
uv run pytest tests/sprint/test_executor.py -v
uv run pytest tests/sprint/test_recovery_policy.py tests/sprint/test_aienv.py -v
uv run pytest tests/sprint/test_resume.py tests/sprint/test_cli_contract.py tests/sprint/test_sprint_docs_cli_parity.py -v
uv run pytest tests/sprint/ -v
uv run pytest -m backward_compat -v
uv run pytest -m unit -m integration
uv run ruff format --check src/ tests/
uv run ruff check src/ tests/
```
> Per-phase gate per the MDTM plan: P1 → `test_monitor.py`; P2 → `test_models.py` + `test_rerun_tasks.py` + `-m backward_compat`; P3/P4 → `test_executor.py`; P5 → `test_recovery_policy.py` + `test_aienv.py` + `test_cli_contract.py` + `test_sprint_docs_cli_parity.py`. ALWAYS finish with full `uv run pytest tests/sprint/` + `uv run ruff format --check src/ tests/` (memory `reference_make_lint_vs_ci_ruff_format`: green `make lint` ≠ green CI format). Then `make sync-dev` is N/A here (no `.claude/` skill/agent/command edits in this feature — all edits are `src/superclaude/cli/sprint/` Python + `tests/` + `docs/`), but `make verify-sync` should still pass unchanged.

---

## 12. Citations index (file:line verified this session)

| Claim | Evidence |
|---|---|
| Sprint tests live in flat `tests/sprint/` | `find tests/sprint` (90+ files) |
| No `fixtures/` dir under `tests/sprint/` yet | `find tests/sprint -name fixtures` → empty |
| Factory contract: `factory(task,config,phase)`→`(exit,turns,bytes)`; writes `task_output_file` | `tests/sprint/test_executor.py:615-623, 743-762, 986-993` |
| Status ladder reads `config.task_output_file(phase,task)` | `src/superclaude/cli/sprint/executor.py:998-1015` |
| `task_output_file` = `phase-{N}-task-{id}-output.txt`; single-session `output_file` = `phase-{N}-output.txt` | `src/superclaude/cli/sprint/models.py:687-694` |
| Detector unit-test template | `tests/sprint/test_monitor.py:137-183` |
| `count_turns_from_output` is the real export (spec's `count_turns_from_stream_json` name is WRONG) | `src/superclaude/cli/sprint/monitor.py:223`; `tests/sprint/test_monitor.py:10,186-231` |
| `detect_error_max_turns` sibling detector | `src/superclaude/cli/sprint/monitor.py:37` |
| `_classify_transcript` classifier test template | `tests/sprint/test_rerun_tasks.py:280-328` |
| `_write_transcript` helper (NDJSON fixture writer) | `tests/sprint/test_rerun_tasks.py:269-277` |
| `TaskResult.from_dict` HARD-keyed (back-compat risk real) | `src/superclaude/cli/sprint/models.py:218-240` |
| Resume planner test template | `tests/sprint/test_resume.py:100-153` |
| doc⇆CLI parity gold-standard | `tests/cli/reflect/test_docs_cli_parity.py:1-121` |
| help-surface parity template | `tests/sprint/test_cli_contract.py:31-54` |
| Sprint CLI guide path | `docs/guides/sprint-cli-tools-release-guide.md` (exists) |
| No existing `max_session_resets` refs (net-new) | `grep -rn max_session_resets src/ docs/ tests/` → 0 |
| Pytest markers `unit`/`integration`/`backward_compat`, `--strict-markers` | `pyproject.toml:111-131` |
| conftest autouse narrative stub | `tests/sprint/conftest.py:32-55` |
| `_run_one_task` shared-param + UNLOCKED spawn (latch goes here) | `src/superclaude/cli/sprint/executor.py:963-993` |
| K>1 concurrency harness idiom | `tests/sprint/test_handoff_concurrency.py`, `test_turn_ledger_concurrency.py` |
| Single-session `execute_sprint` halt test template | `tests/sprint/test_executor.py:383-434` |

**UNVERIFIED (builder must close):**
- Exact `decide` boundary `<` vs `<=` at cap (spec says `attempt < max` → halt at `==`; confirm in P3 impl).
- Real `~/.aienv` export format (`T*Model0N` vs `IC_ALIASES`) + `suggest_alternate_model` signature (whether it takes `aienv_path` for testability) — R1/R3 territory; tests assume an injectable path.
- The `run` Click subcommand symbol name in `src/superclaude/cli/sprint/commands.py` (group is `sprint_group`; the parity test imports the subcommand object — confirm name).
- The sprint guide's internal heading/option-bullet structure (whether it has a `### Key options`-style section the reflect slicer can reuse) — Read `docs/guides/sprint-cli-tools-release-guide.md` before writing the slicer.
- New `reset_policy`/latch param NAME on `execute_phase_tasks`/`_run_one_task` (R3 wiring) — factory tests pass it explicitly.

---

## SUMMARY

The sprint test suite is `tests/sprint/` (flat, one `test_<module>.py` per source module, `tmp_path` + module-level `_helpers`, `--strict-markers` with `unit`/`integration`/`backward_compat`, UV-only `uv run pytest`). The new tests slot in cleanly: **extend** `test_monitor.py` (detector), `test_models.py` (enums + serialization + halt UX), `test_rerun_tasks.py` (classifier alignment), `test_executor.py` (re-spawn loop via the factory seam), `test_resume.py` (resume-safety), `test_cli_contract.py` (help parity); and **create** `test_recovery_policy.py`, `test_aienv.py`, `test_sprint_docs_cli_parity.py`, plus the new fixtures dir `tests/sprint/fixtures/exhaustion/` with the 6 `.jsonl` files authored from spec §2 verbatim JSON.

The load-bearing seam is the `_subprocess_factory` (`executor.py:963-993`): it returns `(exit_code, turns, bytes)` AND writes `config.task_output_file(phase, task)`; the status ladder reads that path. For the re-spawn loop, a **scripted per-attempt factory** keyed off a call counter writes a different transcript each spawn (worked example in §2), and a thread-safe counter drives the K>1 latch/no-storm bound (`cap ≤ total ≤ cap+(K−1)`, `< K×cap`). The doc⇆CLI parity pattern is `tests/cli/reflect/test_docs_cli_parity.py` (mirror for `--max-session-resets` against `docs/guides/sprint-cli-tools-release-guide.md`, adjusting `parents[N]` for the shallower path). Back-compat is a real risk: `TaskResult.from_dict` is hard-keyed (`models.py:218-240`), so the new fields need `.get()` defaults — tested both directions (old payload loads with defaults; new payload round-trips). One spec inaccuracy to flag: monitor exports `count_turns_from_output`, NOT `count_turns_from_stream_json`.
