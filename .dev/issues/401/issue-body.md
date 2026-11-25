<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Bug Summary

`run_with_timeout` in the CLI Portify executor does not raise promptly when a worker exceeds its limit. Production step dispatch also does not call the helper, so the registered SC-001 and SC-002 limits are not enforced through it.

## Environment (OS, version)

- OS: Not known yet
- Version: Python 3.10; branch `ci/parallel-python310-tests`.

## Current Behavior

A 0.1-second limit raised `TimeoutError` only after 3.0 seconds when the worker blocked for 3 seconds. Four timeout tests each took 10.00 seconds in CI when their blocker waited 10 seconds; the current branch has shortened the blocker.

## Expected Behavior

The timeout should be reported near its configured limit rather than after a blocked worker finishes. The production validation and discovery steps should respect their respective 30- and 60-second budgets.

## Steps to Reproduce

1. Run `uv run python`, import `threading` and `run_with_timeout` from `superclaude.cli.cli_portify.executor`, and time this exact call: `run_with_timeout(lambda: threading.Event().wait(3), timeout_s=0.1)`.

## Impact Assessment (Severity, Blast Radius)

- Severity: medium — a hung CLI Portify step can leave the pipeline waiting beyond its declared limit.
- Blast Radius: Direct helper callers and CLI Portify production steps with registered timeout budgets, including validation and component discovery.

## Error Messages

```text
TimeoutError: Operation timed out after 0.1s
```

Raised 3.0 seconds after the call, when the blocked worker returned, not at 0.1 seconds.

## Codebase Context (from `/sc:analyze`)

- `src/superclaude/cli/cli_portify/executor.py:191` defines the helper; `:211`–`:216` uses a thread-pool context manager that waits for its worker on exit after a future timeout.
- `src/superclaude/cli/cli_portify/executor.py:107`–`:118` registers 30- and 60-second budgets, and `:819`–`:824` copies them to steps; `:577`–`:587` invokes production step functions directly without `run_with_timeout`, and no code under `src/superclaude/cli/cli_portify/` reads a step's `timeout_seconds`. Search found helper calls only in `tests/cli_portify/test_executor.py:518`–`:580`, not production code. Thus neither limit is enforced through this helper.
- `tests/cli_portify/test_executor.py:504`–`:566` uses a two-second blocker on the current branch and checks timeout exceptions, including one message match, but does not assert elapsed time.
- Codegraph and Auggie tools were unavailable; the quick pass used Grep and Read.

## Related Issues

Not known yet

## Testing Notes

Add an elapsed-time assertion for a blocked helper call and a production-dispatch test demonstrating that the configured validation and discovery budgets are enforced. Preserve successful return and exception propagation coverage; account for the lifecycle of work that outlives a timeout.

<!-- sc:issue:create template=issue-bug-simple -->
