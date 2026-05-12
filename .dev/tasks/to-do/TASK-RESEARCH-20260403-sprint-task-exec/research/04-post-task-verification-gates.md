# Post-Task Verification Gates — Deep Analysis

**Status**: Complete
**Date**: 2026-04-03
**Investigation Type**: Code Tracer
**Research Question**: What do the two post-task hooks (wiring gate and anti-instinct gate) actually check? Are they task-specific or generic? Could they be extended to check acceptance criteria?

---

## 1. Hook #1: `run_post_task_wiring_hook()`

**File**: `src/superclaude/cli/sprint/executor.py`, lines 450-611
**Signature**:
```python
def run_post_task_wiring_hook(
    task: TaskEntry,
    config: SprintConfig,
    task_result: TaskResult,
    ledger: TurnLedger | None = None,
    remediation_log: DeferredRemediationLog | None = None,
) -> TaskResult:
```

### 1.1 What It Receives

| Input | Source | Task-Specific? |
|-------|--------|----------------|
| `task` (TaskEntry) | The task that just completed | Yes — has `task_id`, `title`, `description` |
| `config` (SprintConfig) | Sprint-level config | No — sprint-wide |
| `task_result` (TaskResult) | Subprocess exit status, timing, output bytes | Yes — result of this task |
| `ledger` (TurnLedger) | Turn budget tracker | No — sprint-wide |
| `remediation_log` | Deferred findings log | No — sprint-wide |

### 1.2 What It Actually Checks

The wiring hook delegates to `run_wiring_analysis()` in `src/superclaude/cli/audit/wiring_gate.py` (line 674). This function runs **three static analysis passes** against `config.release_dir` (the entire release directory, NOT the individual task output):

1. **G-001 — Unwired Callable Analysis** (`analyze_unwired_callables`, line 314):
   - Parses all Python files via AST
   - Finds constructor parameters typed `Optional[Callable]` with default `None`
   - Cross-references all call sites to see if anyone provides that parameter
   - If zero providers found, emits `unwired_callable` finding (severity: critical)

2. **G-002 — Orphan Module Analysis** (`analyze_orphan_modules`, line 394):
   - Scans provider directories (convention-named dirs like `providers/`)
   - For each Python file in provider dirs, checks if any external file imports it
   - Optionally checks AST references (dual evidence rule)
   - Zero importers AND zero references = `orphan_module` (severity: major)

3. **G-003 — Registry Analysis** (`analyze_registries`, line 554):
   - Scans for module-level dict assignments matching registry patterns
   - For each dict entry, verifies the value references an importable callable
   - Unresolved references = `unwired_registry` finding

**Critical observation**: The wiring analysis scans `config.release_dir` — the **entire release directory**, not the individual task's output file. It is a global structural integrity check on the codebase, not a per-task semantic verification.

### 1.3 Mode Behavior

The mode is resolved via `_resolve_wiring_mode()` (line 475) using `GateMode`:

| Mode | Behavior | Can Fail Task? |
|------|----------|---------------|
| `off` | Skip entirely | No |
| `shadow` | Run analysis, log findings, no status change. Shadow findings appended to `DeferredRemediationLog` | No |
| `soft` | Run analysis, warn on critical findings, no status change | No |
| `full` | Run analysis, block on critical+major findings. Sets `TaskStatus.FAIL` and `GateOutcome.FAIL`. Attempts remediation if budget allows | **Yes** |

### 1.4 Remediation Path (full mode only)

When blocking findings exist in `full` mode (line 552-609):
1. Checks `ledger.can_remediate()` for budget
2. Formats a remediation prompt via `_format_wiring_failure()` — a plain text summary of blocking findings
3. Debits `config.remediation_cost` from the ledger
4. Rechecks wiring via `_recheck_wiring()` — re-runs the entire analysis
5. If recheck passes, restores `TaskStatus.PASS`

**Note**: The remediation prompt is formatted but **never actually sent to a subprocess** in the current code. The `_format_wiring_failure()` function returns a string, and the code debits the budget and rechecks, but there is no subprocess invocation between format and recheck. This appears to be a stub for v3.3's `attempt_remediation()`.

### 1.5 What It Returns

Returns the `TaskResult`, possibly modified:
- `task_result.status` changed to `TaskStatus.FAIL` (only in `full` mode with blocking findings)
- `task_result.gate_outcome` changed to `GateOutcome.FAIL` or `GateOutcome.PASS`

---

## 2. Hook #2: `run_post_task_anti_instinct_hook()`

**File**: `src/superclaude/cli/sprint/executor.py`, lines 787-909
**Signature**:
```python
def run_post_task_anti_instinct_hook(
    task: TaskEntry,
    config: SprintConfig,
    task_result: TaskResult,
    ledger: TurnLedger | None = None,
    shadow_metrics: ShadowGateMetrics | None = None,
) -> tuple[TaskResult, TrailingGateResult | None]:
```

### 2.1 What It Receives

| Input | Source | Task-Specific? |
|-------|--------|----------------|
| `task` (TaskEntry) | The task that just completed | Yes |
| `config` (SprintConfig) | Sprint-level config | No |
| `task_result` (TaskResult) | Result including `output_path` | Yes |
| `ledger` (TurnLedger) | Turn budget tracker | No |
| `shadow_metrics` (ShadowGateMetrics) | Metrics collector for shadow mode | No |

### 2.2 What It Actually Checks

The anti-instinct hook reads the task's **output file** (`task_result.output_path`) and validates it against the `ANTI_INSTINCT_GATE` criteria defined in `src/superclaude/cli/roadmap/gates.py` (line 1043).

The validation is performed by `gate_passed()` from `src/superclaude/cli/pipeline/gates.py` (line 20). This is a tiered validation function:

#### Gate Criteria: `ANTI_INSTINCT_GATE`

```python
ANTI_INSTINCT_GATE = GateCriteria(
    required_frontmatter_fields=[
        "undischarged_obligations",
        "uncovered_contracts",
        "fingerprint_coverage",
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[...],  # 3 checks
)
```

#### `gate_passed()` Validation Tiers (pipeline/gates.py)

For STRICT tier, the checks cascade:

1. **File exists** — `output_file.exists()`
2. **File non-empty** — `len(content.strip()) > 0`
3. **Minimum line count** — `len(lines) >= 10`
4. **YAML frontmatter fields present** — Must contain `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`
5. **Semantic checks** (3 pure-Python functions):

| Check | Function | What It Validates |
|-------|----------|-------------------|
| `no_undischarged_obligations` | `_no_undischarged_obligations()` | Frontmatter `undischarged_obligations` must parse as int and equal 0 |
| `integration_contracts_covered` | `_integration_contracts_covered()` | Frontmatter `uncovered_contracts` must parse as int and equal 0 |
| `fingerprint_coverage_check` | `_fingerprint_coverage_check()` | Frontmatter `fingerprint_coverage` must parse as float and be >= 0.7 |

All three semantic checks are **fail-closed**: missing frontmatter, missing field, or unparseable value = False.

**Critical observation**: The anti-instinct gate validates the task's **output file** specifically. However, it checks for **roadmap-pipeline-specific frontmatter fields** (`undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`). These fields are specific to roadmap anti-instinct audit artifacts, NOT general-purpose task outputs.

### 2.3 Vacuous Pass on Missing Output

If `task_result.output_path` is empty or the file does not exist, the gate **passes vacuously** (line 828-830):
```python
if output_path is not None and output_path.exists():
    passed, failure_reason = gate_passed(output_path, ANTI_INSTINCT_GATE)
else:
    # No output artifact to evaluate — gate passes vacuously
    passed = True
    failure_reason = None
```

This means any task that does not produce an output file with the expected frontmatter structure will silently pass the anti-instinct gate. For sprint tasks (which produce code changes, not markdown audit artifacts), this gate is effectively a no-op.

### 2.4 Mode Behavior

| Mode | Behavior | Can Fail Task? |
|------|----------|---------------|
| `off` | Return immediately, no evaluation | No |
| `shadow` | Evaluate, record metrics via `ShadowGateMetrics`, no behavioral impact | No |
| `soft` | Evaluate + credit on PASS / mark `GateOutcome.FAIL` on fail (status unchanged) | No |
| `full` | Evaluate + credit on PASS / mark `GateOutcome.FAIL` + `TaskStatus.FAIL` on fail | **Yes** |

### 2.5 Credit/Debit Economics

On PASS (soft/full modes):
- Credits `task_result.turns_consumed * ledger.reimbursement_rate` turns back to the ledger
- Sets `task_result.reimbursement_amount`

On FAIL (soft/full modes):
- Checks `ledger.can_remediate()` — if budget exhausted, marks FAIL and returns
- Otherwise marks `GateOutcome.FAIL` (and `TaskStatus.FAIL` in full mode)
- **No actual remediation subprocess** is invoked (deferred to v3.2 per SPEC-DEVIATION BUG-009)

### 2.6 What It Returns

Returns a tuple:
- `TaskResult` — possibly modified status/gate_outcome
- `TrailingGateResult` — with `step_id`, `passed`, `evaluation_ms`, `failure_reason`

---

## 3. The `gate_passed()` Function — Shared Validation Engine

**File**: `src/superclaude/cli/pipeline/gates.py`, lines 20-74

This is the pure-Python gate validation engine shared by all pipeline gates. It implements tiered validation:

| Tier | Checks |
|------|--------|
| EXEMPT | Always passes |
| LIGHT | File exists + non-empty |
| STANDARD | + min lines + YAML frontmatter field presence |
| STRICT | + semantic checks (arbitrary `Callable[[str], bool]` functions) |

The `GateCriteria` dataclass (`pipeline/models.py`, line 68) is the configuration object:
```python
@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
```

`SemanticCheck` is a named callable wrapper:
```python
@dataclass
class SemanticCheck:
    name: str
    check_fn: Callable[[str], bool]
    failure_message: str
```

**Extension point**: New semantic checks can be added to any `GateCriteria` instance by appending `SemanticCheck` objects. The `gate_passed()` function iterates over them generically.

---

## 4. Assessment: Task-Specific vs. Generic

### Wiring Gate — GENERIC (codebase-level)

- Scans `config.release_dir`, not individual task output
- Checks structural integrity of Python code: unwired callables, orphan modules, broken registries
- Does NOT reference anything from the task's description, acceptance criteria, or expected output
- Identical analysis regardless of which task just ran
- **Verdict**: Purely generic structural quality gate. Not task-aware.

### Anti-Instinct Gate — DOMAIN-SPECIFIC (roadmap pipeline artifacts)

- Reads the individual task's `output_path` — so it IS task-specific in terms of which file it checks
- But the criteria it applies (`ANTI_INSTINCT_GATE`) are hardcoded for roadmap anti-instinct audit artifacts
- Expects specific frontmatter fields: `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`
- For sprint tasks that produce code (not markdown audit artifacts), the gate passes vacuously because the output file either doesn't exist or doesn't have the expected frontmatter
- **Verdict**: Domain-specific to roadmap pipeline. Task-specific in file selection but generic in criteria. Not suitable for verifying arbitrary task acceptance criteria.

---

## 5. Could These Gates Be Extended to Check Acceptance Criteria?

### Extension Path A: New GateCriteria per Task

The `gate_passed()` function is fully generic. It accepts any `GateCriteria` instance. To check task-specific acceptance criteria:

1. Parse `TaskEntry` acceptance criteria into a `GateCriteria` instance
2. Generate `SemanticCheck` callables from acceptance criteria text
3. Call `gate_passed(output_path, task_specific_criteria)` instead of `ANTI_INSTINCT_GATE`

**Challenge**: Acceptance criteria are natural-language descriptions (e.g., "function handles edge cases correctly"). Converting these to deterministic `Callable[[str], bool]` checks requires either:
- LLM evaluation (violates the pure-Python constraint of `gate_passed`)
- Pre-defined check templates that map criteria patterns to check functions

### Extension Path B: Add a Third Hook

The executor's `execute_phase_tasks()` function (line 912+) calls the two hooks sequentially. A third hook `run_post_task_acceptance_hook()` could be added at the same call site with the same pattern:

```python
# Existing pattern:
task_result = run_post_task_wiring_hook(task, config, task_result, ...)
task_result, gate_result = run_post_task_anti_instinct_hook(task, config, task_result, ...)
# New:
task_result = run_post_task_acceptance_hook(task, config, task_result, ...)
```

This is the cleanest extension point. The new hook would:
- Receive `task.description` and/or `task.acceptance_criteria` (if the TaskEntry model is extended)
- Read `task_result.output_path`
- Invoke an LLM subprocess to evaluate acceptance (since pure-Python checks are insufficient for semantic criteria)
- Return modified `TaskResult`

### Extension Path C: Dynamic SemanticChecks in Anti-Instinct Gate

Replace the hardcoded `ANTI_INSTINCT_GATE` with a factory function:

```python
def build_task_gate(task: TaskEntry) -> GateCriteria:
    checks = [...]  # generate from task.acceptance_criteria
    return GateCriteria(
        required_frontmatter_fields=[...],
        min_lines=1,
        enforcement_tier="STRICT",
        semantic_checks=checks,
    )
```

This reuses the existing `gate_passed()` engine but parameterizes the criteria per task.

---

## 6. Where These Hooks Are Called

The hooks are called from `execute_phase_tasks()` at `src/superclaude/cli/sprint/executor.py` line 912+. After each task subprocess completes and produces a `TaskResult`, both hooks run sequentially:

1. `run_post_task_wiring_hook()` — may set FAIL on structural issues
2. `run_post_task_anti_instinct_hook()` — may set FAIL on audit artifact issues

There is also a phase-level adapter `run_post_phase_wiring_hook()` (line 735) that wraps the task-level wiring hook for phase-level execution by creating a synthetic `TaskEntry`.

---

## Gaps and Questions

1. **Anti-instinct gate is effectively a no-op for sprint tasks**: Since sprint tasks produce code changes (not markdown audit artifacts with specific frontmatter), `output_path` either doesn't have the expected content or doesn't exist. The gate passes vacuously. This makes the anti-instinct hook meaningless in the sprint context unless tasks are specifically producing roadmap-style audit artifacts.

2. **Wiring gate checks the entire codebase, not task output**: It scans `config.release_dir` regardless of what the specific task changed. While this catches global breakage, it can't distinguish issues introduced by the current task from pre-existing issues.

3. **No remediation subprocess is actually invoked**: Both hooks format remediation prompts but neither sends them to a Claude subprocess. The wiring hook's `_format_wiring_failure()` returns a string that is never used as a subprocess prompt. The anti-instinct hook's FAIL path has a comment explicitly deferring `attempt_remediation()` to v3.2.

4. **`TaskEntry` has no `acceptance_criteria` field**: The current `TaskEntry` model has `task_id`, `title`, and `description`. There is no structured acceptance criteria field that a verification gate could consume.

5. **Turn budget dependency**: Both hooks are budget-guarded via `TurnLedger`. If budget is exhausted, wiring analysis is skipped entirely (line 481-486). This means verification quality degrades under budget pressure.

6. **The `GateCriteria` + `gate_passed()` pattern is well-designed for extension**: The tiered validation with pluggable semantic checks is a clean interface. Adding new gate types requires only new `GateCriteria` instances and `SemanticCheck` callables.

---

## Summary

The two post-task verification gates serve fundamentally different purposes but share a key limitation: **neither verifies task-specific acceptance criteria**.

**Wiring gate** (`run_post_task_wiring_hook`): A codebase-level structural integrity check using Python AST analysis. It detects unwired callables, orphan modules, and broken registries across the entire release directory. It is completely task-agnostic — it doesn't know or care what the task was supposed to accomplish. It answers: "Did this task break the codebase's wiring?"

**Anti-instinct gate** (`run_post_task_anti_instinct_hook`): A file-level validation of the task's output artifact against the `ANTI_INSTINCT_GATE` criteria. However, those criteria are hardcoded for roadmap pipeline audit artifacts (checking `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage` frontmatter). For sprint tasks producing code changes, this gate passes vacuously because the output doesn't match the expected format.

**Neither gate verifies whether the task accomplished what it was supposed to accomplish.** They are quality signals (structural integrity and artifact format compliance), not semantic completion checks.

**Extension is feasible** via three paths: (A) parameterized `GateCriteria` per task, (B) a new third hook specifically for acceptance criteria, or (C) a factory function replacing the hardcoded `ANTI_INSTINCT_GATE`. Path B is cleanest because acceptance criteria verification likely requires LLM evaluation, which doesn't fit the pure-Python constraint of `gate_passed()`.
