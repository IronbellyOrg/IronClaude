---
title: "Unwired Components Remediation — Execution Tasklist"
date: 2026-03-25
source_audit: docs/generated/cli-unwired-components-audit.md
p3_proposal: docs/generated/p3-unified-proposal.md
p4_proposal: docs/generated/p4-unified-proposal.md
status: ready
executor: sc:task-unified
---

# Unwired Components Remediation — Execution Tasklist

## Overview

Four priority items from the CLI unwired components audit. P1 and P2 are direct deletions/reclassifications. P3 and P4 are architectural changes with approved unified proposals.

**Execution order:** P1 → P2 → P4 → P3 (P4 before P3 because P4 is a deletion that simplifies the tree; P3 is additive and benefits from a cleaner baseline.)

---

## P1: Remove Phantom Callable Params (`halt_fn`, `kill_fn`)

**Risk: None. Zero test coverage, zero production callers.**

### Task P1.1: Remove `halt_fn` from roadmap executor

- **File:** `src/superclaude/cli/roadmap/executor.py`
- **Action:**
  1. Read `_check_remediation_budget()` (around line 1179)
  2. Remove the `halt_fn` parameter from the function signature
  3. Remove the `if halt_fn is not None: halt_fn(...)` branch (lines 1210-1211)
  4. Keep the `_print_terminal_halt()` call as the sole code path (it's the existing default fallback)
  5. Remove any docstring references to `halt_fn`
- **Verify:** `uv run pytest tests/roadmap/ -v` — no tests reference `halt_fn`

### Task P1.2: Remove `kill_fn` from cli_portify monitor

- **File:** `src/superclaude/cli/cli_portify/monitor.py`
- **Action:**
  1. Read `OutputMonitor.__init__()` (around line 206) and `update()` (around line 233)
  2. Remove `kill_fn: Optional[callable] = None` from `__init__` signature
  3. Remove `self._kill_fn = kill_fn` assignment (line 211)
  4. Remove the `if self._kill_fn is not None: self._kill_fn()` branch (lines 233-234)
  5. The stall detection logic should remain — only the injectable kill hook is removed. If the stall condition triggers, it should simply log or raise (check what the surrounding code does when `kill_fn` is None — that becomes the only path)
- **Verify:** `uv run pytest tests/cli_portify/ -v` — no tests inject `kill_fn`

### Task P1.3: Verify P1 changes

- **Action:** Run full test suite for affected modules
  ```bash
  uv run pytest tests/roadmap/ tests/cli_portify/ -v --tb=short
  ```
- **Expected:** All tests pass. No test references `halt_fn` or `kill_fn`.

---

## P2: Reclassify `step_runner` and `reclassify_fn` as Intentional Test Seams

**Risk: None. Documentation-only change.**

### Task P2.1: Update the audit document

- **File:** `docs/generated/cli-unwired-components-audit.md`
- **Action:**
  1. In Category 1 table, add a **Status** column
  2. Mark items 1 (`reclassify_fn`) and 4 (`step_runner`) as `RECLASSIFIED: intentional test seam`
  3. Mark items 2 (`halt_fn`) and 3 (`kill_fn`) as `RESOLVED: removed`
  4. Mark items 5-11 (`process_runner` x7) as `RESOLVED: removed`
  5. Update the **Assessment** paragraph at line 30 to note:
     - `step_runner` is actively used by 7+ tests in `tests/cli_portify/test_executor.py` as the primary executor test seam
     - `reclassify_fn` is actively used by 2 tests in `tests/audit/test_spot_check.py` (lines 132, 150)
     - Both are intentional dependency injection points, not phantom params
  6. Update the Severity Summary table: Medium count changes from 11 to 0 (all resolved or reclassified)

### Task P2.2: Verify test seam usage is current

- **Action:** Confirm the test seams are still actively used
  ```bash
  uv run pytest tests/cli_portify/test_executor.py -v --tb=short
  uv run pytest tests/audit/test_spot_check.py -v --tb=short
  ```
- **Expected:** Tests pass and actively exercise `step_runner` and `reclassify_fn` injection.

---

## P4: Delete Audit Gate Modules with Resurrection Contract

**Risk: Medium — must decouple `test_ac_validation.py` before deletion.**

**Reference:** `docs/generated/p4-unified-proposal.md`

### Task P4.1: Decouple test_ac_validation.py from evidence_gate imports

- **File:** `tests/audit/test_ac_validation.py`
- **Action:**
  1. Read the full file, focusing on the four import sites (lines 167, 181, 204, 218)
  2. Each of these is a local import: `from superclaude.cli.audit.evidence_gate import check_delete_evidence` or `check_keep_evidence`
  3. Replace each usage with inline assertions against `ClassificationResult` fields directly:
     - **AC4 (DELETE evidence):** Replace `gate = check_delete_evidence(result); assert gate.passed` with:
       ```python
       assert result.action == V2Action.DELETE
       has_zero_ref = any("zero" in e.lower() and "ref" in e.lower() for e in result.evidence)
       assert has_zero_ref, f"AC4: DELETE for {result.file_path} lacks zero-reference evidence"
       ```
     - **AC5 (KEEP evidence):** Replace `gate = check_keep_evidence(result); assert gate.passed` with:
       ```python
       has_ref = any("ref" in e.lower() for e in result.evidence)
       assert has_ref, f"AC5: KEEP for {result.file_path} lacks reference evidence"
       ```
       **Important:** Do NOT wrap in an `if` guard. Each test method already constructs a KEEP/TIER_1 fixture — an `if` guard would silently pass when evidence is missing, defeating the test. For `test_keep_tier1_without_imports_fails`, the replacement becomes:
       ```python
       has_ref = any("ref" in e.lower() for e in result.evidence)
       assert not has_ref  # AC5: KEEP without reference evidence should fail
       ```
       (The original `check_keep_evidence` returned `passed=False` for this case — the replacement must assert the negative.)
  4. Remove all `from superclaude.cli.audit.evidence_gate import ...` lines
  5. Ensure `ClassificationResult`, `V2Action`, `V2Tier` are imported from `audit/classification.py` (likely already imported)
- **Verify:** `uv run pytest tests/audit/test_ac_validation.py -v`

### Task P4.2: Delete source and test files

- **Action:** Delete these four files:
  ```bash
  rm src/superclaude/cli/audit/evidence_gate.py
  rm src/superclaude/cli/audit/manifest_gate.py
  rm tests/audit/test_evidence_gate.py
  rm tests/audit/test_manifest_gate.py
  ```
- **Verify:** No remaining imports reference these files:
  ```bash
  uv run python -c "from superclaude.cli.audit import evidence_gate" 2>&1 | grep -q "ModuleNotFoundError" && echo "OK: evidence_gate removed"
  uv run python -c "from superclaude.cli.audit import manifest_gate" 2>&1 | grep -q "ModuleNotFoundError" && echo "OK: manifest_gate removed"
  ```

### Task P4.3: Check for any other imports of deleted modules

- **Action:** Search entire codebase for remaining references:
  ```bash
  grep -r "evidence_gate\|manifest_gate" src/ tests/ --include="*.py" -l
  ```
- **Expected:** Zero results (or only this tasklist/docs). If any source/test files still import, fix them before proceeding.

### Task P4.4: Create resurrection contract

- **File:** `.dev/resurrection-contracts/audit-v2-gates.md` (create directory if needed)
- **Action:**
  1. Run `git log --oneline -1` to capture the current HEAD commit hash (the last commit BEFORE deletion)
  2. Create the file with content from the P4 unified proposal (Step 3), substituting the real commit hash
  3. Include the review-by date: 2026-06-25
- **Verify:** File exists and contains valid commit hash

### Task P4.5: Run audit module tests

- **Action:**
  ```bash
  uv run pytest tests/audit/ -v --tb=short
  ```
- **Expected:** All remaining audit tests pass. No import errors from deleted modules.

---

## P3: Wire cli_portify Gate Enforcement (Two-Layer System)

**Risk: Medium — defaulting to shadow mode mitigates pipeline breakage.**

**Reference:** `docs/generated/p3-unified-proposal.md`

### Task P3.1: Add PortifyGateMode enum and GateEvaluation dataclass to models.py

- **File:** `src/superclaude/cli/cli_portify/models.py` (NOT executor.py — see rationale below)
- **Rationale:** `executor.py` imports from `gates.py` (line 36: `get_gate_criteria`). If `gates.py` imports `PortifyGateMode` from `executor.py`, that creates a circular import (`executor → gates → executor`). Placing these types in `models.py` avoids this entirely — both `executor.py` and `gates.py` already import from `models.py` with no reverse dependency.
- **Action:**
  1. Read `models.py`, find the existing enum/dataclass section (after `PortifyStatus` at line 137)
  2. Add `from enum import IntEnum` to imports if not present
  3. Add `PortifyGateMode(IntEnum)` with values `SHADOW=0, SOFT=1, FULL=2`
  4. Add `GateEvaluation` dataclass with fields: `step_id: str`, `gate_id: str`, `tier: str`, `passed: bool`, `reason: str | None`, `effective_mode: PortifyGateMode`, `blocked: bool`, `failure: GateFailure | None = None`
  5. Note: `GateFailure` is defined in `gates.py`. To avoid a circular import from `models.py → gates.py`, use `from __future__ import annotations` (likely already present) and use a string annotation or `TYPE_CHECKING` guard for `GateFailure`
- **Verify:** `uv run python -c "from superclaude.cli.cli_portify.models import PortifyGateMode, GateEvaluation; print('OK')"`

### Task P3.2: Add PortifyGatePolicy class to executor.py

- **File:** `src/superclaude/cli/cli_portify/executor.py`
- **Action:**
  1. Add imports: `from superclaude.cli.cli_portify.models import PortifyGateMode, GateEvaluation` (add to existing models import line)
  2. Add `from superclaude.cli.pipeline.gates import gate_passed` to imports
  3. Add `PortifyGatePolicy` class BEFORE `PortifyExecutor`
  4. Constructor: `__init__(self, global_mode: PortifyGateMode = PortifyGateMode.SHADOW)`
  5. Method: `evaluate(self, step_id, output_file, min_enforce_mode) -> GateEvaluation`
     - Computes `effective = max(global_mode, min_enforce_mode)`
     - Calls `get_gate_criteria(step_id)` (catches KeyError for unregistered steps)
     - Calls `gate_passed(output_file, criteria)` when output_file exists
     - Sets `blocked = (not passed) and (effective == FULL)`
     - Creates `GateFailure` instance when not passed
     - Returns `GateEvaluation` with all fields populated
  6. Implementation matches the code in the P3 unified proposal exactly
- **Verify:** `uv run python -c "from superclaude.cli.cli_portify.executor import PortifyGatePolicy; print('OK')"`

### Task P3.3: Add GATE_MIN_ENFORCE mapping

- **File:** `src/superclaude/cli/cli_portify/gates.py`
- **Action:**
  1. Read the current file, find the end of `GATE_REGISTRY` and `get_gate_criteria()`
  2. Add `from superclaude.cli.cli_portify.models import PortifyGateMode` to imports (safe — `gates.py` does not import from `models.py` currently, and `models.py` does not import from `gates.py` at runtime)
  3. After `get_gate_criteria()`, add the `GATE_MIN_ENFORCE` dictionary:
     ```python
     GATE_MIN_ENFORCE: dict[str, PortifyGateMode] = {
         "validate-config": PortifyGateMode.FULL,
         "discover-components": PortifyGateMode.SOFT,
         "brainstorm-gaps": PortifyGateMode.SOFT,
         "models-gates-design": PortifyGateMode.SOFT,
     }
     ```
  4. STRICT gates are intentionally omitted (default to SHADOW via `.get()` in executor)
- **Verify:** `uv run python -c "from superclaude.cli.cli_portify.gates import GATE_MIN_ENFORCE; print(GATE_MIN_ENFORCE)"`

### Task P3.3a: Add `gate_mode` field to PortifyConfig

- **File:** `src/superclaude/cli/cli_portify/models.py`
- **Action:**
  1. Read the `PortifyConfig` dataclass definition
  2. Add field: `gate_mode: str = "shadow"`
  3. This field is set by the CLI flag (P3.6) and read by `run_portify()` (P3.4a) to construct the executor
- **Verify:** `uv run python -c "from superclaude.cli.cli_portify.models import PortifyConfig; print(PortifyConfig.__dataclass_fields__['gate_mode'].default)"`

### Task P3.4: Wire PortifyGatePolicy into PortifyExecutor

- **File:** `src/superclaude/cli/cli_portify/executor.py`
- **Action:**
  1. Add `gate_mode: PortifyGateMode = PortifyGateMode.SHADOW` parameter to `PortifyExecutor.__init__`
  2. Create `self._gate_policy = PortifyGatePolicy(global_mode=gate_mode)` in constructor
  3. Replace the consultation block at lines ~500-511 with the enforcement block from the proposal:
     - Lookup `GATE_MIN_ENFORCE.get(step.step_id, PortifyGateMode.SHADOW)`
     - Call `self._gate_policy.evaluate(step.step_id, step.output_file, gate_min)`
     - Log via `self._execution_log.gate_eval()`
     - If not passed: SOFT mode → `self._tui.gate_warning()`, FULL mode → `self._diagnostics.record_gate_failure()` + return `PortifyStatus.HALT`
     - Shadow mode: no action beyond logging
  4. Ensure `step_runner` path (lines 472-485) remains UNTOUCHED — gate evaluation only on the production dispatch path
  5. Import `GATE_MIN_ENFORCE` from `cli_portify.gates`
- **Verify:** `uv run pytest tests/cli_portify/test_executor.py -v` — all 7+ existing tests must pass unchanged

### Task P3.4a: Update run_portify() to pass gate_mode through

- **File:** `src/superclaude/cli/cli_portify/executor.py`
- **Action:**
  1. Read `run_portify()` (around line 651) — this function constructs `PortifyExecutor`
  2. Convert `config.gate_mode` string to enum: `gate_mode_enum = PortifyGateMode[config.gate_mode.upper()]`
  3. Pass to constructor: `PortifyExecutor(steps, workdir, config=config, ..., gate_mode=gate_mode_enum)`
  4. This bridges the CLI flag (string in PortifyConfig) to the executor (enum)
- **Verify:** `uv run python -c "from superclaude.cli.cli_portify.executor import run_portify; print('OK')"`

### Task P3.5: Add gate_warning() to PortifyTUI

- **File:** `src/superclaude/cli/cli_portify/tui.py`
- **Codebase context:** `PortifyTUI` wraps `TuiDashboard` via `self._dashboard` (line 293). `TuiDashboard` creates a `Console()` internally at line 230 but does not expose it as a public attribute. `PortifyTUI` has no direct `self._console`.
- **Action:**
  1. Read the file, find the `PortifyTUI` class (line 281)
  2. Add `from rich.console import Console` to the file's imports (it's already imported at line 17 inside a try/except block — verify and add to the same block if needed)
  3. Add method to `PortifyTUI`:
     ```python
     def gate_warning(self, step_id: str, reason: str | None) -> None:
         """Emit a visible warning for a soft-mode gate failure."""
         console = Console(stderr=True)
         console.print(f"[yellow]GATE WARNING[/yellow] {step_id}: {reason or 'unknown'}")
     ```
     Using a local `Console(stderr=True)` is consistent with how `TuiDashboard.__init__` creates its own console. Stderr ensures warnings appear even when stdout is redirected.
- **Verify:** `uv run python -c "from superclaude.cli.cli_portify.tui import PortifyTUI; t = PortifyTUI(); t.gate_warning('test-step', 'test reason')"`

### Task P3.6: Wire --gate-mode CLI flag

- **File:** `src/superclaude/cli/cli_portify/commands.py`
- **Action:**
  1. Read the file, find the portify Click command definition
  2. Add option:
     ```python
     @click.option(
         "--gate-mode",
         type=click.Choice(["shadow", "soft", "full"], case_sensitive=False),
         default="shadow",
         help="Gate enforcement mode: shadow (log only), soft (warn), full (block).",
     )
     ```
  3. Add `gate_mode` parameter to the command function signature
  4. Set `config.gate_mode = gate_mode` when constructing `PortifyConfig` (the field was added in P3.3a)
  5. Do NOT convert to enum here — `run_portify()` handles the conversion (P3.4a)
- **Verify:** `superclaude portify --help` should show `--gate-mode` option

### Task P3.7: Verify PortifyStatus.HALT exists (pre-resolved)

- **File:** `src/superclaude/cli/cli_portify/models.py`
- **Status:** PRE-RESOLVED. `PortifyStatus.HALT = "halt"` confirmed at models.py:146. No action needed.
- **Action:** Verification only — confirm the enum member exists:
  ```bash
  uv run python -c "from superclaude.cli.cli_portify.models import PortifyStatus; print(PortifyStatus.HALT)"
  ```
- **Expected:** Prints `PortifyStatus.HALT`. If this fails, add `HALT = "halt"` to the enum.

### Task P3.8: Write gate policy unit tests

- **File:** `tests/cli_portify/test_gate_policy.py` (new file)
- **Action:** Create tests covering:
  1. `PortifyGatePolicy` in SHADOW mode — evaluates gates, never blocks
  2. `PortifyGatePolicy` in SOFT mode — evaluates gates, never blocks, returns failure info
  3. `PortifyGatePolicy` in FULL mode — blocks on gate failure
  4. Per-gate promotion: SHADOW global + FULL min_enforce → effective FULL
  5. Per-gate promotion: FULL global + SHADOW min_enforce → effective FULL (max wins)
  6. Unregistered step (KeyError) → passes with tier="NONE"
  7. Missing output file (None) → passes without calling gate_passed()
  8. `GateFailure` is populated correctly on failure
- **Verify:** `uv run pytest tests/cli_portify/test_gate_policy.py -v`

### Task P3.9: Run full cli_portify test suite

- **Action:**
  ```bash
  uv run pytest tests/cli_portify/ -v --tb=short
  ```
- **Expected:** All existing tests pass (step_runner seam untouched) + new gate policy tests pass.

---

## Final Verification

### Task FINAL.1: Run complete affected test suites

```bash
uv run pytest tests/roadmap/ tests/cli_portify/ tests/audit/ tests/sprint/ -v --tb=short
```

**Expected:** All tests pass across all four affected module areas.

### Task FINAL.2: Update audit document severity summary

- **File:** `docs/generated/cli-unwired-components-audit.md`
- **Action:** Update the Severity Summary table (line 106-111) to reflect all changes:
  - **High (was 4 subsystems):** `SprintGatePolicy` chain → RESOLVED (previously wired). `evidence_gate` module → RESOLVED (deleted). `manifest_gate` module → RESOLVED (deleted). `cli_portify` gate registry → RESOLVED (wired via P3).
  - **Medium (was 11):** All 11 → RESOLVED (7 `process_runner` removed, `halt_fn`/`kill_fn` removed, `step_runner`/`reclassify_fn` reclassified)
  - **Low (was 5):** `resolve_gate_mode`/`GateScope` → RESOLVED (wired). `PROMPT_BUILDERS`/`FAILURE_HANDLERS` accessors → check if still unwired. `DEVIATION_ANALYSIS_GATE` → check if still orphaned.
  - Update total: "Total unwired components: 32 symbols" → updated count

### Task FINAL.3: Lint and format

```bash
make lint && make format
```
