# F-25: Subprocess lifecycle gaps -- exit codes collapse, SIGINT/SIGTERM not relayed

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P4, P7, P8
**Identified by**: D-6, D-7
**File:line**: `src/superclaude/cli/prd/executor.py:562-585` (`_determine_status`); `src/superclaude/cli/pipeline/process.py:159-171` (`wait()`)

## Evidence

```python
# executor.py:563-568
if exit_code == 124:
    return PrdStepStatus.TIMEOUT
if exit_code != 0:
    return PrdStepStatus.ERROR  # all non-zero, non-124 codes collapse to ERROR

# pipeline/process.py:159-165
def wait(self) -> int:
    try:
        self._process.wait(timeout=self.timeout_seconds)
    except subprocess.TimeoutExpired:
        self.terminate()
        return 124
```

## Trace

**Exit code collapse** (D-6):
- Exit codes recognized: only `124` (TIMEOUT) and `0` (success). Every other code -- `130` (SIGINT/user Ctrl-C), `137` (SIGKILL/OOM), `143` (SIGTERM), `-N` (signal-killed), `1` (generic error), `2` (usage error) -- all fold into `PrdStepStatus.ERROR`.
- `_TRANSIENT_EXIT_CODES` at process.py:37 includes `137` (SIGKILL), claiming it is retryable, but it is immediately surfaced as ERROR.
- Real cause of failure is invisible in `execution-log.jsonl`.

**Signal not relayed** (D-7):
- `PrdSignalHandler` (executor.py:176-203) sets `shutdown_requested=True` but never propagates the signal to the running child.
- `terminate()` override (5s grace) only fires via the wall-clock timeout path, not via operator Ctrl-C or SIGTERM.
- User hits Ctrl-C, parent sets flag, child runs to completion (or until TTY process group propagation).

## Reproduction sketch

Ctrl-C during a step: pipeline reports ERROR, not "user-interrupted." OOM-kill the child: same ERROR. Send SIGTERM to parent: parent sets flag but does not relay; child continues.

## Confidence (aggregated)

0.80 -- Agent D verified both aspects. The signal-relay gap depends on TTY process group behavior.

## Cross-agent corroboration

- **Agent D** identified both the exit-code collapse (meaningful codes invisible) and the signal-not-relayed gap (operator interrupt does not reach the child process), noting they compound: the user cannot cleanly interrupt and cannot diagnose why a step failed.
