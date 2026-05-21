# F-11: PrdMonitor entirely dead code -- stall_timeout/stall_action unwired

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P2, P4, P8
**Identified by**: D-2
**File:line**: `src/superclaude/cli/prd/monitor.py:1-202` (entire file); `src/superclaude/cli/prd/executor.py:334` (only reference)

## Evidence

```python
# executor.py:334 -- only place PrdMonitor is touched
self._monitor = PrdMonitor()

# grep -rn "self._monitor\." src/superclaude/cli/prd/ returns zero hits
# grep -n "parse_line|check_stall|monitor\." executor.py confirms no call sites
```

## Trace

- **Instantiation**: `PrdMonitor()` is created in `PrdExecutor.__init__`.
- **Zero consumers**: `parse_line`, `check_stall`, `reset`, `get_state` are never called anywhere in the executor.
- **Stream bypass**: Subprocess stdout flows directly into `{step_id}-output.txt` via Popen's `stdout=` redirection. Nothing streams bytes line-by-line. The executor reads the whole file only after `proc.wait()` returns.
- **Consequences**:
  - `PrdMonitor.parse_line` is unreachable.
  - `PrdMonitor.check_stall` is unreachable, so `PrdConfig.stall_timeout` and `stall_action` (models.py:190-191) have no detection path.
  - TUI is updated only on step completion (executor.py:455), never mid-stream.
  - All QA verdict / fix-cycle / research-file-count signal extraction in monitor.py:153-201 produces nothing usable.
  - A subprocess that hangs silently will sit until the 3600s wall-clock timeout with no intermediate stall signal.

## Reproduction sketch

Run any step whose child stalls for 2-3 minutes without writing output. Expected per `stall_timeout=120`: a stall warning/abort. Actual: silence until the 3600s wall-clock timeout fires.

## Confidence (aggregated)

0.98 -- Agent D verified trivially via grep. The instantiation exists but zero API calls follow.

## Cross-agent corroboration

- **Agent D** identified the full dead-code surface: not only is the monitor unused, but the `stall_timeout` and `stall_action` config fields are consequently unwired as well, compounding this into a P2 (knob defined, never consumed) finding.
