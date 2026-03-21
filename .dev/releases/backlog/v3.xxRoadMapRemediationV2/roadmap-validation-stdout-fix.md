# Roadmap Validation Pipeline: stdout Capture Failure — Root Cause & Remediation

## Problem Summary

The roadmap pipeline's `adversarial-merge` validation step fails silently because the Claude CLI subprocess writes its output via the `Write` tool instead of printing to stdout. When `claude --print --output-format text` is used with `--tools default` and Claude's **last action is a tool_use call** (no trailing text), stdout receives only a single newline character. The STRICT gate then fails on the effectively-empty file, and the pipeline writes a degraded validation report — discarding the actual merge output that exists in a sibling file.

## Root Cause (Empirically Validated)

### Mechanism

```
Claude subprocess (--print --output-format text --tools default)
  └─ Reads embedded reflect reports from prompt
  └─ Produces merge draft → writes to reflect-merge.md via Write tool
  └─ Refines draft → writes to reflect-merged.md via Write tool
  └─ Turn ends after final Write (no trailing text response)
  └─ --output-format text captures only "\n" to stdout
  └─ stdout → validation-report.md (1 byte, effectively empty)
  └─ STRICT gate check: FAIL (empty file)
  └─ _write_degraded_report() overwrites validation-report.md
```

### Evidence

| Evidence Point | Finding |
|---|---|
| `reflect-merge.md` (9,061 bytes) | Full adversarial merge draft with YAML frontmatter, agreement table |
| `reflect-merged.md` (10,291 bytes) | Refined final merge with all 5 blocking issues, 4 warnings |
| `validation-report.md` (830 bytes) | Degraded template (overwritten by `_write_degraded_report()`) |
| `validation-report.err` | Empty (process exited 0 — no subprocess crash) |
| Timestamps | `reflect-merge.md` → 72s → `reflect-merged.md` → 9s → `validation-report.md` (consistent with Write tool → Write tool → degraded overwrite) |
| Empirical test | `claude --print --output-format text --tools Write` ending on a Write tool call outputs exactly 1 byte (newline) to stdout |
| Gate test | `gate_passed()` on a 1-byte file returns `(False, "File empty (0 bytes)")` |

### Why This Wasn't Caught Earlier

1. The reflect steps (which also use `output_format="text"` + `--tools default`) happened to produce text responses as their final action, so stdout captured correctly
2. The merge step has a more complex task (reading 2 reports, categorizing, producing tables) which made Claude more likely to use Write as a working strategy
3. No test covers the interaction between `--output-format text` and tool_use as the final assistant action

## Affected Code Paths

| File | Lines | Role |
|---|---|---|
| `src/superclaude/cli/pipeline/process.py` | 79-80 | Hardcodes `--tools default` for ALL steps |
| `src/superclaude/cli/roadmap/validate_executor.py` | 117-127 | Creates `ClaudeProcess` for validation steps with `output_format="text"` |
| `src/superclaude/cli/roadmap/validate_executor.py` | 252-261 | Builds adversarial-merge step (no tool override) |
| `src/superclaude/cli/roadmap/validate_executor.py` | 229-250 | Builds reflect steps (same vulnerability) |
| `src/superclaude/cli/roadmap/validate_executor.py` | 318-367 | `_write_degraded_report()` overwrites output on partial failure |
| `src/superclaude/cli/pipeline/gates.py` | 20-74 | `gate_passed()` — fails on empty file (correct behavior) |

## Remediation Plan

### Phase 1: Make `tools` configurable per step (Root Cause Fix)

**Goal**: Allow pipeline steps to declare their tool requirements. Steps that only produce text output should run with `--tools ""` (no tools), eliminating the possibility of the stdout-empty failure mode.

#### Step 1.1: Add `tools` parameter to `ClaudeProcess`

**File**: `src/superclaude/cli/pipeline/process.py`

- Add `tools: str = "default"` to `ClaudeProcess.__init__()` parameter list
- Store as `self.tools`
- In `build_command()`, replace hardcoded `"default"` (line 80) with `self.tools`
- If `self.tools` is empty string, emit `--tools ""` (or omit the flag entirely — verify CLI behavior)

```python
# Current (line 79-80):
"--tools",
"default",

# Proposed:
"--tools",
self.tools,
```

**Validation**: Existing test `test_tools_default_in_command` must still pass (default unchanged). Add new test `test_tools_empty_in_command`.

#### Step 1.2: Pass `tools=""` for all validation text-output steps

**File**: `src/superclaude/cli/roadmap/validate_executor.py`

In `validate_run_step()`, pass `tools=""` to `ClaudeProcess()`:

```python
# Line 117-127, add tools parameter:
proc = ClaudeProcess(
    prompt=effective_prompt,
    output_file=step.output_file,
    error_file=step.output_file.with_suffix(".err"),
    max_turns=config.max_turns,
    model=step.model or config.model,
    permission_flag=config.permission_flag,
    timeout_seconds=step.timeout_seconds,
    output_format="text",
    tools="",           # <-- NEW: validation steps need no tools
    extra_args=extra_args,
)
```

**Rationale**: All validation steps (reflect + merge) receive their inputs inline-embedded in the prompt. They only need to produce text output. No filesystem access required.

**Risk**: If a future validation step needs tool access, it will fail silently (Claude will attempt tool use, get an error). Mitigate by: (a) documenting the constraint, (b) adding a `tools` field to the `Step` model so it can be overridden per-step.

#### Step 1.3: Add per-step `tools` to the Step model (recommended)

**File**: `src/superclaude/cli/pipeline/models.py`

Add an optional `tools` field to the `Step` dataclass:

```python
@dataclass
class Step:
    id: str
    prompt: str
    output_file: Path
    # ... existing fields ...
    tools: str | None = None  # None = use ClaudeProcess default ("default")
```

Then in `validate_run_step()`, use `step.tools or "default"` when constructing `ClaudeProcess`. This allows the step definitions in `_build_multi_agent_steps()` and `_build_single_agent_steps()` to declare tool requirements explicitly.

#### Step 1.4: Empirical validation

Before merging, verify that `["--tools", ""]` works correctly when passed through Python's `subprocess.Popen`:

```python
# Test script:
import subprocess
result = subprocess.run(
    ["claude", "--print", "--output-format", "text",
     "--no-session-persistence", "--dangerously-skip-permissions",
     "--tools", "", "--max-turns", "1",
     "-p", "Say exactly: hello"],
    capture_output=True, text=True
)
assert result.stdout.strip() == "hello"
assert result.returncode == 0
```

#### Step 1.5: Add tests

**File**: `tests/cli/pipeline/test_process.py`

```python
def test_tools_empty_in_command():
    """Verify --tools '' disables all tools in build_command()."""
    proc = ClaudeProcess(
        prompt="test", output_file=Path("/tmp/test.md"),
        error_file=Path("/tmp/test.err"), tools=""
    )
    cmd = proc.build_command()
    idx = cmd.index("--tools")
    assert cmd[idx + 1] == ""

def test_tools_default_unchanged():
    """Verify default tools value remains 'default'."""
    proc = ClaudeProcess(
        prompt="test", output_file=Path("/tmp/test.md"),
        error_file=Path("/tmp/test.err")
    )
    cmd = proc.build_command()
    idx = cmd.index("--tools")
    assert cmd[idx + 1] == "default"
```

### Phase 2: Diagnostic improvement for empty-output detection

**Goal**: When a step's stdout output is empty but sibling files were written during execution, produce a descriptive error instead of a cryptic gate failure.

#### Step 2.1: Add empty-output diagnostic in `validate_run_step()`

**File**: `src/superclaude/cli/roadmap/validate_executor.py`

After the subprocess exits successfully (exit_code == 0) but before returning, check if the output file is effectively empty:

```python
# After _sanitize_output(step.output_file) on line 167:
if step.output_file.exists():
    content = step.output_file.read_text(encoding="utf-8")
    if len(content.strip()) == 0:
        # Scan for candidate files written during this step
        candidates = [
            f for f in step.output_file.parent.glob("*.md")
            if f != step.output_file
            and f.stat().st_mtime >= started_at.timestamp()
        ]
        if candidates:
            best = max(candidates, key=lambda f: f.stat().st_mtime)
            _log.warning(
                "Step '%s' produced empty stdout but found candidate output: %s (%d bytes). "
                "This typically means Claude used the Write tool instead of printing to stdout. "
                "Consider running this step with tools='' to prevent tool use.",
                step.id, best, best.stat().st_size,
            )
```

**Important**: This is diagnostic logging ONLY. It does NOT auto-copy the candidate file. The gate check still runs normally and fails on the empty file. The log message tells the operator exactly what happened and how to fix it.

#### Step 2.2: No auto-recovery (Option A rejected)

Auto-copying a candidate file risks silent data corruption if the wrong file is selected. The pipeline should fail loudly and let the operator decide. This was validated through adversarial debate.

### Phase 3: Documentation and future-proofing

#### Step 3.1: Document the `--output-format text` + tool_use interaction

Add a comment block in `process.py` near the `tools` parameter:

```python
# IMPORTANT: When output_format="text", Claude CLI outputs only the final
# text response. If Claude's last action is a tool_use call (no trailing
# text), stdout receives only a newline. Steps that capture output via
# stdout (output_format="text") should set tools="" unless they genuinely
# need tool access. See: roadmap-validation-stdout-fix.md
```

#### Step 3.2: Consider systemic fix (future ticket)

The underlying issue is that `--output-format text` silently drops tool_use content. A more robust long-term approach would be:
- Use `--output-format stream-json` for all steps and extract text post-hoc
- Or fix the CLI to emit tool_use content as text in `--output-format text` mode

This is out of scope for the immediate fix but should be tracked.

## File Change Summary

| File | Change Type | Lines Changed (est.) |
|---|---|---|
| `src/superclaude/cli/pipeline/process.py` | Modify | ~5 (add `tools` param, use in `build_command()`) |
| `src/superclaude/cli/pipeline/models.py` | Modify | ~2 (add `tools` field to `Step`) |
| `src/superclaude/cli/roadmap/validate_executor.py` | Modify | ~15 (pass `tools=""`, add diagnostic logging) |
| `tests/cli/pipeline/test_process.py` | Modify | ~15 (add 2 new tests) |

**Total estimated change**: ~37 lines across 4 files.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| `["--tools", ""]` behaves differently in subprocess vs shell | Low | High | Step 1.4 empirical validation before merge |
| Future validation step needs tools | Low | Medium | Per-step `tools` field in Step model (Step 1.3) |
| Reflect steps also affected | Already mitigated | — | Phase 1 applies `tools=""` to all validation steps |
| Empty-output diagnostic false positive | Very low | Low | Diagnostic only, no auto-action (Phase 2) |

## Hotfix Applied

As an immediate unblock, `reflect-merged.md` was copied to `validation-report.md` on 2026-03-20. The ADVERSARIAL_MERGE_GATE passes on the copied content. This is a one-time manual intervention; the code fix in Phase 1 prevents recurrence.
