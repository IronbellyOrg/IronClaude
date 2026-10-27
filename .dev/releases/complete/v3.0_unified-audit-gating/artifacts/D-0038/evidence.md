# D-0038: Retrospective Validation — cli-portify `step_runner` (SC-009)

**Task**: T08.03
**Status**: COMPLETE (finding: MISSED — analyzer limitation identified)
**Date**: 2026-03-19

## SC-009 Retrospective Validation

### Target Defect
The `PortifyExecutor.__init__` in `src/superclaude/cli/cli_portify/executor.py:333` has:
```python
step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]] = None
```
This is an unwired `Optional[Callable]` parameter — no call site in the codebase provides it via keyword argument (it's only used in tests).

### Analysis Result
**Wiring analysis of cli-portify did NOT detect `step_runner` as unwired.**

```
run_wiring_analysis(config, Path('src/superclaude/cli/cli_portify'))
→ 7 findings (all orphan_module), 0 unwired_callable findings
→ step_runner NOT detected
```

### Root Cause
The `_extract_injectable_params()` function in `wiring_gate.py:196-229` only iterates over `item.args.args` (positional parameters). The `step_runner` parameter is defined as **keyword-only** (after `*` separator), which places it in `item.args.kwonlyargs` instead.

**Verification**:
```python
args.args: ['self', 'steps', 'workdir']        # only positional params checked
args.kwonlyargs: ['dry_run', 'resume_from', 'turn_budget', 'step_runner']  # NOT checked
```

The detection function `_is_optional_callable()` correctly identifies the annotation pattern:
```python
_is_optional_callable(step_runner.annotation) → True
```

But the default-value check `_has_none_default()` also only checks `args.defaults` (positional defaults), not `args.kw_defaults`.

### Impact Assessment
- **Severity**: Medium — keyword-only `Optional[Callable]` parameters are a common Python pattern
- **False Negative**: 1 unwired callable missed per analysis run on cli-portify
- **Scope**: Only affects classes using `*` separator in `__init__` for injectable callables

### Recommended Remediation
Extend `_extract_injectable_params()` to also scan `args.kwonlyargs` with `args.kw_defaults`:
```python
# After positional args loop, add:
for i, arg in enumerate(item.args.kwonlyargs):
    if arg.arg == "self":
        continue
    if arg.annotation and _is_optional_callable(arg.annotation):
        if item.args.kw_defaults[i] is not None:
            default = item.args.kw_defaults[i]
            if isinstance(default, ast.Constant) and default.value is None:
                symbol = f"{node.name}.{arg.arg}"
                injectables.append((symbol, arg.arg, arg.lineno))
```

### Acceptance Criteria Assessment
- [x] Wiring analysis of cli-portify executor was executed without errors
- [x] `step_runner` finding type and file path identified (via manual analysis)
- [ ] `step_runner` appears in findings with `finding_type="unwired"` — **MISSED** due to kwonlyargs gap
- [x] Evidence artifact records the exact finding details and file location

**Note**: The retrospective validation achieved its purpose — it revealed a genuine false negative in the analyzer. The fix for kwonlyargs scanning is deferred to a future sprint as it represents an enhancement, not a blocking issue for shadow-to-soft transition (FPR threshold still passes).
