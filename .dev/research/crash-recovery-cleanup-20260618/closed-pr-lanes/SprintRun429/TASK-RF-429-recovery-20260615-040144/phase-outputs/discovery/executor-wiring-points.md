# executor.py Wiring-Point Inventory (P3, Step 4.1)

**File:** `src/superclaude/cli/sprint/executor.py` (+ `models.py` for PhaseResult).
**Verified:** 2026-06-15, read directly from current file. Drift from research cites noted.

| Concern | Research cite | Verified line(s) | Drift |
|---------|---------------|------------------|-------|
| `_run_one_task` signature | 963-975 | **963-975** (`*,` block ends `lock=None` at 974) | none |
| subprocess spawn block | 986-993 | **986-993** (`subprocess_factory` else `_run_task_subprocess`) | none |
| status ladder | 999-1015 | **999-1015**: exit0→PASS (999-1000), 124→INCOMPLETE (1001-1002), `:1003` `detect_error_max_turns`+`_task_completed_before_overrun`→PASS_RECOVERED (1003-1011), `_is_transient_failure`→FAIL_RECOVERABLE (1012-1013), else FAIL_TERMINAL (1014-1015) | ~same |
| lock guard | 1017 | **1017** `guard = lock if lock is not None else contextlib.nullcontext()` | none |
| TaskResult construction | 1027-1035 | **1027-1035** (inside `with guard:`) | none |
| K>1 worker `_run_one_task` call | 1134-1145 | **1134-1145** (`lock=lock` at 1144), inside `_worker` in `_execute_phase_tasks_parallel` | none |
| `_execute_phase_tasks_parallel` def | 1048-1141 | **1048-1062** (def + params); local `lock = threading.Lock()` at **1092** | ~same |
| `execute_phase_tasks` (per-phase entry) | — | **1190-1206** def; dispatches to parallel at **1241-1254** (K>1) else sequential loop **1256+** | — |
| K=1 `_run_one_task` call | 1337-1348 | **1337-1348** (`lock=None` at 1347) | none |
| per-task phase-completion block | 1752-1781 | `aggregate_task_results` **1752-1754**; `phase_result = PhaseResult(...)` **1757-1764**; `_write_phase_result_json` **1778** | ~same |
| `_write_phase_result_json` | 2657-2701 | **2657-2701**; `payload` dict **2685-2696** | none |
| `_determine_phase_status` | — | **2751** | — |
| `_is_transient_failure` | 2267-2289 | **2267** | none |
| `_task_completed_before_overrun` | — | **2321** | — |
| executor imports | — | `import contextlib` (5); `from .models import (...)` (28); `from .monitor import OutputMonitor, detect_error_max_turns, detect_prompt_too_long` (44) | — |
| `PhaseResult` dataclass (models.py) | 729-753 | **743-767**; last field `recovery_history` at **767** (insert halt_reason/exhausted_model after) | ~same |

## Decisions for P3

1. **Shared policy construction:** `execute_phase_tasks` (1190) is called once per phase. It will accept a new `reset_policy: SessionResetPolicy | None = None` kwarg; when None, construct `SessionResetPolicy(max_session_resets=getattr(config, "max_session_resets", 8))` ONCE (the `getattr` bridges until P5 adds the `SprintConfig.max_session_resets` field — "defaulting to 8 until P5 lands"). The P3 test injects `reset_policy=` directly. The SAME instance threads to BOTH `_execute_phase_tasks_parallel` (→ K>1 `_run_one_task` at 1144) and the K=1 `_run_one_task` at 1347 → shared `_latch_tripped` across all workers.
2. **Re-spawn loop:** wraps the spawn (986-993) inside `_run_one_task`; latch precheck/trip under `guard` (1017), spawn unlocked. Provider-failure branch inserted ABOVE `_is_transient_failure` (1012), BELOW the `:1003` PASS_RECOVERED gate, guarded by `_task_completed_before_overrun` (edge #1).
3. **TaskResult exhaustion fields** populated from loop-local counters inside the `with guard:` TaskResult(...) call (1027).
4. **PhaseResult halt fields** (`halt_reason`/`exhausted_model`) added after `recovery_history` (767); persisted in `_write_phase_result_json` payload (2696); per-task derivation inserted after `phase_result = PhaseResult(...)` (1764), before `_write_phase_result_json` (1778).
5. **imports:** add `from .recovery_policy import SessionResetPolicy, Action` and extend the `.monitor` import with `detect_provider_failure, ProviderFailure`.
