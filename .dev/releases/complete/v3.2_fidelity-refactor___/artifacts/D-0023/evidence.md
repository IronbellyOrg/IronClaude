# D-0023: Retrospective Validation Against cli_portify

## Task: T04.03
## SC-010 Real-Code Detection Validation

### Analysis Run
```
Source: src/superclaude/cli/cli_portify/
Config: WiringConfig(exclude_patterns=['test_*.py', 'conftest.py', '__init__.py'], rollout_mode='shadow')
```

### Results
```
Files analyzed: 29
Files skipped: 2
Total findings: 7
  Unwired callables: 0
  Orphan modules: 7
  Unwired registries: 0
Scan duration: 0.1014s
step_runner findings: 0
```

### Analysis: Why step_runner Not Detected

The real `PortifyExecutor.__init__` uses **keyword-only** syntax:

```python
class PortifyExecutor:
    def __init__(
        self,
        steps: list[PortifyStep],
        workdir: Path,
        *,  # <--- keyword-only boundary
        step_runner: Optional[Callable[...]] = None,
    ) -> None:
```

The current analyzer (`_extract_injectable_params`) iterates `item.args.args`
(positional parameters) but NOT `item.args.kwonlyargs` (keyword-only parameters).
Because `step_runner` appears after `*`, it resides in `kwonlyargs` and is not
scanned.

### AST Evidence
```
Class: PortifyExecutor
  args.args: ['self', 'steps', 'workdir']
  args.kwonlyargs: ['dry_run', 'resume_from', 'turn_budget', 'step_runner']
```

### Disposition

**Partial SC-010 compliance**: The analyzer correctly detects the defect pattern
(Optional[Callable] with default None, never wired) when the parameter is
positional — validated by the fixture test (T04.01, D-0021). The keyword-only
argument gap is a known limitation documented here.

**Recommended enhancement** (future release): Extend `_extract_injectable_params`
to also iterate `item.args.kwonlyargs` and check `item.args.kw_defaults` for
None defaults. This would enable detection of the real cli-portify defect.

### Fallback Allowed
Yes (per task T04.03 tier: STANDARD, Fallback Allowed: Yes)
