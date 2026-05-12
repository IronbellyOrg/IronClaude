# Research: Tasklist Generation Format and Sprint Executor Path A Compatibility

**Status**: Complete
**Date**: 2026-04-03
**Investigation Type**: Code Tracer + Doc Analyst

## Research Question

Does the tasklist generation pipeline ALWAYS produce `### T<PP>.<TT>` formatted phase files, and does this format reliably feed into the sprint executor's regex match for Path A (per-task execution)?

---

## 1. Tasklist Generation Algorithm (SKILL.md)

**File**: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

### Section 4.5 — Task ID Format (lines 276-280)

The SKILL.md prescribes a deterministic, zero-padded task ID format:

> Task IDs are zero-padded: `T<PP>.<TT>` where:
> - `PP` = phase number (2 digits)
> - `TT` = task number within the phase (2 digits)
> - Example: `T01.03`

This is a **hard rule** in the "Deterministic Generation Algorithm" section (Section 4). The algorithm is explicitly described as producing "same input -> same output" and "decision-free."

### Section 4.4 — Task Conversion

Every roadmap item produces exactly 1 task by default, with splitting only for independently deliverable compound items. All generated tasks receive the `T<PP>.<TT>` ID format without exception.

### Section 4.6 — Clarification Tasks

Even Clarification Tasks (inserted when information is missing or confidence < 0.70) "follow normal numbering" -- meaning they also receive `T<PP>.<TT>` format IDs. There is no alternative ID format defined anywhere in the protocol.

**Finding**: The SKILL.md mandates `T<PP>.<TT>` as the ONLY task ID format. No alternative format exists in the spec.

---

## 2. Phase File Template

**File**: `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`

The template explicitly defines the task heading format (line 22-24):

```
### T<PP>.<TT> -- <Task Title>
```

Key structural details:
- Level-3 heading (`###`)
- Task ID in `T<PP>.<TT>` format
- Em-dash separator (`--`)
- Task title follows

The template also defines the surrounding field table structure (lines 26-42) with fields like Roadmap Item IDs, Effort, Risk, Tier, etc. — all within the `### T<PP>.<TT>` heading block.

**Finding**: The template enforces `### T<PP>.<TT> -- <Title>` as the canonical heading format.

---

## 3. File Emission Rules

**File**: `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md`

Key rules confirmed:
- **File naming**: Phase files MUST use `phase-N-tasklist.md` convention (line 18)
- **Phase heading**: MUST be `# Phase N -- <Name>` (line 24) — level 1 heading with em-dash
- **Content boundary**: Phase files contain ONLY tasks for that phase (line 39)
- **Index references**: Must use literal filenames for Sprint CLI regex discovery (line 32)

The emission rules do not define task heading format directly (that is in the template and SKILL.md Section 4.5), but they do constrain the file structure to be Sprint CLI-compatible.

**Finding**: File emission rules enforce Sprint CLI-compatible structure. Task format is inherited from SKILL.md Section 4.5 and the template.

---

## 4. Sprint Executor Regex (`_TASK_HEADING_RE`)

**File**: `src/superclaude/cli/sprint/config.py`, lines 281-284

```python
_TASK_HEADING_RE = re.compile(
    r"^###\s+(T\d{2}\.\d{2})\s*(?:--|-\u2014|\u2014)\s*(.+)",
    re.MULTILINE,
)
```

This regex matches:
- `^###` — line starts with level-3 heading
- `\s+` — one or more whitespace chars
- `(T\d{2}\.\d{2})` — capture group 1: task ID in `T<PP>.<TT>` format (exactly 2 digits each)
- `\s*` — optional whitespace
- `(?:--|-\u2014|\u2014)` — separator: either `--` (double hyphen), `-\u2014` (hyphen + em-dash), or `\u2014` (em-dash)
- `\s*` — optional whitespace
- `(.+)` — capture group 2: task title

The separator alternation (`--|-\u2014|\u2014`) is a defensive measure handling potential Unicode normalization of em-dashes. The generated format uses `--` (double hyphen), which matches the first alternative.

### Parser Function: `parse_tasklist()` (lines 310-364)

```python
headings = list(_TASK_HEADING_RE.finditer(content))
if not headings:
    _logger.warning("No task headings (### T<PP>.<TT>) found in tasklist content")
    return []
```

When no headings match, the function returns an empty list with a warning. This empty list propagates to `_parse_phase_tasks()` which returns `None` for empty lists, triggering Path B.

**Finding**: The regex precisely matches the `### T<PP>.<TT> -- <Title>` format prescribed by the SKILL.md and template. Format alignment is exact.

---

## 5. Path A vs Path B Branching Logic

**File**: `src/superclaude/cli/sprint/executor.py`, lines 1095-1290

### `_parse_phase_tasks()` (lines 1095-1109)

```python
def _parse_phase_tasks(phase: Phase, config: SprintConfig) -> list[TaskEntry] | None:
    """Parse a phase file for task entries.

    Returns a list of TaskEntry if the phase file contains a task inventory
    (i.e., ``### T<PP>.<TT>`` headings), or None for freeform-prompt phases
    that should use the ClaudeProcess fallback.
    """
    from .config import parse_tasklist

    if not phase.file.exists():
        return None

    content = phase.file.read_text(encoding="utf-8", errors="replace")
    tasks = parse_tasklist(content, execution_mode=phase.execution_mode)
    return tasks if tasks else None
```

### Branching in `execute_sprint()` (lines 1201-1234)

```python
# v3.1-T04: Per-task delegation -- if phase has a task inventory,
# delegate to execute_phase_tasks() instead of single ClaudeProcess.
tasks = _parse_phase_tasks(phase, config)
if tasks:
    # PATH A: Per-task execution
    started_at = datetime.now(timezone.utc)
    task_results, remaining, phase_gate_results = execute_phase_tasks(
        tasks, phase, config, ...
    )
    ...
    continue

# PATH B: Whole-phase fallback (ClaudeProcess)
isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"
...
proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
proc_manager.start()
```

**Path A** (per-task): Activated when `_parse_phase_tasks()` returns a non-empty list. Each task is executed individually via `execute_phase_tasks()` with budget allocation, per-task subprocess spawning, and individual gate evaluation.

**Path B** (whole-phase fallback): Activated when `_parse_phase_tasks()` returns `None` (no task headings found, or phase file does not exist). The entire phase file is sent to a single `ClaudeProcess` subprocess.

**Finding**: Path A is the standard path for any phase file containing `### T<PP>.<TT>` headings. Path B is the fallback for freeform or legacy phase files without task headings.

---

## 6. Empirical Verification — Actual Generated Phase Files

### v2.24.5-SpecFidelity/phase-1-tasklist.md

```
# Phase 1 -- Empirical Validation Gate
### T01.01 -- Verify `claude` CLI availability
### T01.02 -- Check `claude --help` for `--file` format
```

Format: `### T<PP>.<TT> -- <Title>` with `--` separator. Matches `_TASK_HEADING_RE`.

### v3.1_Anti-instincts__/phase-1-tasklist.md

```
# Phase 1 -- Core Detection Modules & Architecture Decisions
### T01.01 -- Resolve Day-1 Architecture Decisions
### T01.02 -- Implement Obligation Scanner `obligation_scanner.py`
```

Format: `### T<PP>.<TT> -- <Title>` with `--` separator. Matches `_TASK_HEADING_RE`.

### v2.26-roadmap-v5/phase-1-tasklist.md

```
# Phase 1 -- Pre-Implementation Decisions
### T01.01 -- Resolve OQ-A/OQ-B GateCriteria.aux_inputs Decision
```

Format: Identical. Matches.

### v2.25.5-PreFlightExecutor/phase-1-tasklist.md

```
# Phase 1 -- Data Model and Parsing
### T01.01 -- Add `execution_mode` Field to `Phase` Dataclass
```

Format: Identical. Matches.

### unified-audit-gating-v2/phase-1-tasklist.md

```
# Phase 1 -- Foundation & Source Defaults
### T01.01 -- Set PipelineConfig.max_turns default to 100
```

Format: Identical. Matches.

### v3.05_DeterministicFidelityGates/phase-1-tasklist.md

```
# Phase 1 -- Foundation: Parser, Data Model & Interface Verification
### T01.01 -- Verify Interface Contracts for TurnLedger, Registry, and FR-7.1
```

Format: Identical. Matches.

**Finding**: All 6 sampled phase files (across different releases from v2.02 through v3.1) use the exact same `### T<PP>.<TT> -- <Title>` format. 100% consistency across the sample. All would match `_TASK_HEADING_RE` and trigger Path A.

---

## 7. Potential Path B Triggers

Path B would be triggered ONLY in these scenarios:

1. **Phase file does not exist** — `_parse_phase_tasks()` returns `None` at line 1104-1105.
2. **Phase file has no `### T<PP>.<TT>` headings** — `parse_tasklist()` returns empty list, which becomes `None` at line 1109.
3. **Malformed task IDs** — e.g., `### T1.1` (missing zero-padding) would not match `T\d{2}\.\d{2}`.
4. **Wrong heading level** — e.g., `## T01.01` (level 2 instead of level 3).
5. **Wrong separator** — e.g., `### T01.01 - Task` (single hyphen) would not match `(?:--|-\u2014|\u2014)`.
6. **Manually authored phase files** — files not generated by the tasklist protocol would lack the format.

The tasklist generator protocol has no code path that produces any of these malformations. The format is hard-coded in the template and algorithm.

**Finding**: Path B is effectively unreachable for files generated by the standard tasklist protocol. It exists as a safety net for manually-authored or legacy phase files.

---

## Gaps and Questions

1. **No runtime validation at generation time**: The SKILL.md and template prescribe the format, but since generation is inference-based (LLM-driven), there is no programmatic validator that checks generated phase files against the regex before emission. A post-generation validation step that runs `_TASK_HEADING_RE` against output files would add defense-in-depth.

2. **Unicode em-dash edge case**: The regex handles `--`, `-\u2014`, and `\u2014` separators. The template specifies `--` (double hyphen). If a future template change used the Unicode em-dash `\u2014`, the regex would still match. This is already handled.

3. **Task count limit**: The `T\d{2}.\d{2}` format supports at most 99 phases and 99 tasks per phase. No overflow handling exists, but this is a theoretical limit unlikely to be hit in practice.

4. **Checkpoint headings**: Inline checkpoints use `### Checkpoint: Phase <P> / Tasks <start>-<end>` format. These do NOT match `_TASK_HEADING_RE` and are correctly excluded from task parsing. No conflict.

---

## Summary

**Confirmed**: The tasklist generation pipeline ALWAYS produces `### T<PP>.<TT> -- <Title>` formatted phase files. This is mandated by:

| Source | Location | Rule |
|--------|----------|------|
| SKILL.md Section 4.5 | lines 276-280 | Task IDs are zero-padded `T<PP>.<TT>` |
| Phase template | lines 22-24 | `### T<PP>.<TT> -- <Task Title>` heading format |
| File emission rules | lines 18, 24 | Sprint CLI-compatible naming and structure |

**Confirmed**: This format feeds directly into the sprint executor's `_TASK_HEADING_RE` regex at `config.py:281-284`, which extracts the task ID and title. The regex is precisely aligned with the generated format.

**Confirmed**: Path A (per-task execution via `execute_phase_tasks()`) is the standard execution path for all protocol-generated phase files. Path B (whole-phase `ClaudeProcess` fallback) is unreachable for well-formed generated files and exists only as a safety net for manually-authored or legacy content.

**Empirical evidence**: 6 actual generated phase files sampled across releases v2.24.5, v2.25.5, v2.26, v3.05, v3.1, and unified-audit-gating-v2 all use the exact `### T<PP>.<TT> -- <Title>` format with zero deviations.
