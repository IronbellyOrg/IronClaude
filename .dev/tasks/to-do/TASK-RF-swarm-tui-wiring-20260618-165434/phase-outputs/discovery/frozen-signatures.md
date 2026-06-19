# Frozen Signatures Baseline (C3 / AC-004 / NFR-001)

**Captured:** 2026-06-18 (Step 1.3), verbatim from source. These signatures MUST NOT change.
**Audit base (start_commit):** `300c06a6d53287893a446db8e859f5f1bc5434d8`

## Baseline swarm suite (pre-change)

`uv run pytest tests/swarm/ -q` → **2217 passed, 27 skipped** (fully green, no pre-existing failures).
Full capture: `phase-outputs/test-results/baseline-swarm-suite.txt`.

## `dispatch_wave1` — `src/superclaude/cli/swarm/dispatch.py:334-343`

```python
def dispatch_wave1(
    preflight_result: PreflightResult,
    transport: Optional[Transport] = None,
    *,
    transport_for_slot: Optional[Callable[[int], Transport]] = None,
    prompt: str = "",
    parallel_executor: Optional[ParallelExecutor] = None,
    worker_spec: Optional[WorkerSpec] = None,
    logger: Optional[Logger] = None,
) -> list[WorkerResult]:
```

- Positional: `preflight_result`
- Positional-or-keyword w/ default: `transport=None`
- Keyword-only (after `*`): `transport_for_slot=None`, `prompt=""`, `parallel_executor=None`, `worker_spec=None`, `logger=None`
- Return: `list[WorkerResult]`

## `ParallelExecutor` — `src/superclaude/execution/parallel.py`

```python
class ParallelExecutor:                                   # :80
    def __init__(self, max_workers: int = 10):            # :100
    def plan(self, tasks: List[Task]) -> ExecutionPlan:   # :103
    def execute(self, plan: ExecutionPlan) -> Dict[str, Any]:  # :169
```

## Verification plan

- Step 3.8 pins these via `inspect.signature(...)`.
- Step 4.4 proves no signature-line change via `git diff <start_commit> -- dispatch.py parallel.py`.
- The poll loop lives in `run_cmd` (the caller), NEVER inside `dispatch_wave1`.
