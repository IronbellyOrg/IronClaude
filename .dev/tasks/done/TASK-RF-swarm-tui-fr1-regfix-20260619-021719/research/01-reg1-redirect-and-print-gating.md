# Research: REG-1 — armed Live redirect + worker-thread print() gating

**Topic type:** File Inventory + Patterns & Conventions
**Scope:** `src/superclaude/cli/swarm/tui.py`, `src/superclaude/execution/parallel.py`, `src/superclaude/cli/swarm/dispatch.py`, `tests/swarm/test_run_tui_integration.py` (frozen-sig)
**Status:** Complete
**Date:** 2026-06-19

---

## REG-1 finding (CODE-VERIFIED)

FR-1 ("single-writer Console topology") is substantively violated. Two co-causes:

### Cause 1 — armed Live redirect (`tui.py:218-228`)

```python
def start(self) -> Live:
    self._started_at = time.time()
    self._live = Live(
        self.render(self._state, self._events),
        console=self.console,
        refresh_per_second=self._refresh,
        screen=False,
    )                          # <-- NO redirect_stdout=/redirect_stderr= args
    self._live.start()
    return self._live
```

`rich.live.Live` defaults to `redirect_stdout=True, redirect_stderr=True`. With the dashboard active, any stdout/stderr write — including writes from the **background `swarm-wave1` worker thread** — is funneled through the Live/Console machinery, re-arming the exact #181/#182/#184 cross-thread render crash class the feature exists to kill.

**Fix:** add `redirect_stdout=False, redirect_stderr=False,` to the `Live(...)` constructor at `tui.py:221`. This makes the Console no longer intercept worker stdout.

### Cause 2 — unconditional worker-thread prints (`parallel.py`)

`ParallelExecutor.plan()` / `execute()` / `_execute_group()` emit unconditional `print()`:

| line | call |
|------|------|
| 110, 111 | `print("⚡ Parallel Executor: Planning ...")`, `print("="*60)` |
| 164, 165 | `print(plan)`, `print("="*60)` |
| 176, 177 | `print("🚀 Executing ...")`, `print("="*60)` |
| 183, 191 | `print(f"📦 {group}")`, `print("Completed in ...")` |
| 196-200 | summary block prints |
| 225, 232 | per-task `✅`/`❌` prints |

Disabling the redirect alone (Cause 1) stops the crash but lets these worker prints corrupt/scramble the dashboard frame (the PR#181 *medium*). So both halves are required.

## FROZEN-SIGNATURE CONSTRAINT (load-bearing design decision)

`tests/swarm/test_run_tui_integration.py:666-669` (`test_frozen_signatures_unchanged`) asserts:

```python
init_sig = inspect.signature(ParallelExecutor.__init__)
init_names = list(init_sig.parameters)
assert init_names == ["self", "max_workers"]
assert init_sig.parameters["max_workers"].default == 10
```

→ **Adding a `quiet=` kwarg to `__init__` WOULD break this test.** Also `frozen_signatures_confirmed.parallel_executor` in the register is "pinned by test_frozen_signatures_unchanged".

### Signature-preserving silencing mechanism (the fix shape)

Use a **class attribute default** + per-call-site instance flip (NOT a constructor param):

```python
class ParallelExecutor:
    quiet: bool = False          # class-attr default; __init__ signature UNCHANGED
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
    def plan(self, tasks):
        if not self.quiet:
            print("⚡ Parallel Executor: Planning ...")
            print("=" * 60)
        ...
        if not self.quiet:
            print(plan); print("=" * 60)
        return plan
    # same `if not self.quiet:` guard around every print in execute()/_execute_group()
```

At the **swarm dispatch call site only** (`dispatch.py:424`), flip the flag on the instance:

```python
executor = parallel_executor or ParallelExecutor(max_workers=workers_requested)
executor.quiet = True   # FR-1: swarm dispatch path is silent (filesystem-only output)
```

- `__init__` params remain exactly `["self", "max_workers"]` → frozen-sig test stays green.
- Other callers (`execution/__init__.py:108,200`, `parallel.py` convenience fns) are untouched → keep their prints by default.
- The injected-executor test paths (`test_imm3_parallel.py`, `test_dispatch.py`) pass their own `ParallelExecutor`; if dispatch flips `.quiet=True` on whatever instance it gets, those tests stay silent too (acceptable; they assert results, not stdout). Verify they don't assert on captured stdout.

**Alternative considered & rejected:** routing prints through `logging` would also preserve the signature but is a larger behavioral change for non-swarm callers and loses the explicit "swarm dispatch path" gating the user asked for. The class-attr + call-site flip is the minimal, literal match.

## Acceptance evidence to reproduce post-fix
- `tui.py:221` carries `redirect_stdout=False, redirect_stderr=False`.
- `parallel.py` prints all guarded by `if not self.quiet:`; `ParallelExecutor.quiet` class default is `False`.
- `dispatch.py:424` sets `executor.quiet = True`.
- `test_frozen_signatures_unchanged` still passes (`__init__` == `["self","max_workers"]`).
