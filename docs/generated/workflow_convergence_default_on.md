# Workflow: Enable Convergence Engine as Default for Spec-Fidelity

**Generated**: 2026-04-03
**Strategy**: Systematic
**Source Plan**: `.claude/plans/crystalline-stirring-meadow.md`
**Branch**: `feat/tdd-spec-merge` (current)

---

## Context

The roadmap pipeline's `spec-fidelity` step runs as a single-shot LLM check. On failure the pipeline halts, requiring 3-4 manual `--resume` reruns. A convergence engine (v3.05) exists in code but `convergence_enabled` defaults to `False` with no CLI flag to expose it. An adversarial debate concluded: **default ON** with `--no-convergence` escape hatch. Neither backlog release conflicts.

---

## Phase 1: Flip the Default

### Task 1.1 — Change `convergence_enabled` default to `True`
- **File**: `src/superclaude/cli/roadmap/models.py:112`
- **Action**: Change `convergence_enabled: bool = False` to `convergence_enabled: bool = True`
- **Rationale**: The convergence engine code is complete; the single-shot path is the broken UX
- **Risk**: Low — all existing tests that construct `RoadmapConfig()` without explicit `convergence_enabled` will now get `True`. Task 3.1 updates the one test that asserts the old default.
- **Checkpoint**: `uv run pytest tests/roadmap/test_remediation.py::TestAllowRegeneration::test_convergence_enabled_default_false -v` should FAIL (expected — old assertion)

---

## Phase 2: Add `--no-convergence` CLI Flag

### Task 2.1 — Add Click option decorator
- **File**: `src/superclaude/cli/roadmap/commands.py`
- **Insert after**: `--allow-regeneration` option block (line ~94)
- **Code**:
  ```python
  @click.option(
      "--no-convergence",
      is_flag=True,
      default=False,
      help="Disable the spec-fidelity convergence engine (use single-shot LLM check instead).",
  )
  ```

### Task 2.2 — Add parameter to `run()` function signature
- **File**: `src/superclaude/cli/roadmap/commands.py:134-151`
- **Action**: Add `no_convergence: bool` parameter after `allow_regeneration`

### Task 2.3 — Wire flag into `config_kwargs`
- **File**: `src/superclaude/cli/roadmap/commands.py:210-223`
- **Action**: Add `"convergence_enabled": not no_convergence` to `config_kwargs` dict
- **Checkpoint**: `uv run pytest tests/roadmap/test_cli_contract.py -v` should still pass (existing CLI contract tests unaffected)

---

## Phase 3: Update Tests

### Task 3.1 — Update default assertion test
- **File**: `tests/roadmap/test_remediation.py:15-18`
- **Action**: Rename `test_convergence_enabled_default_false` to `test_convergence_enabled_default_true`, change assertion from `assert field.default is False` to `assert field.default is True`
- **Checkpoint**: `uv run pytest tests/roadmap/test_remediation.py -v` passes

### Task 3.2 — Verify existing convergence dispatch tests still pass
- **File**: `tests/roadmap/test_convergence.py:935-993`
- **Action**: Read-only verification. Both `test_convergence_gate_none_when_enabled` and `test_legacy_gate_when_disabled` pass explicit `convergence_enabled` values, so they should be unaffected by the default change.
- **Checkpoint**: `uv run pytest tests/roadmap/test_convergence.py::TestDispatch -v` passes

### Task 3.3 — Add `--no-convergence` CLI integration test
- **File**: `tests/roadmap/test_convergence_wiring.py` (append new test class)
- **Tests to add**:
  1. `test_default_config_convergence_enabled` — `RoadmapConfig()` has `convergence_enabled=True`
  2. `test_no_convergence_flag_disables` — simulate CLI invocation with `--no-convergence`, assert `config.convergence_enabled is False`
  3. `test_no_flag_means_convergence_on` — simulate CLI invocation without flag, assert `config.convergence_enabled is True`
- **Pattern**: Follow existing `test_cli_contract.py` patterns (direct `RoadmapConfig` construction + `_build_steps` assertions)
- **Checkpoint**: `uv run pytest tests/roadmap/test_convergence_wiring.py -v` passes

---

## Phase 4: Full Suite Verification

### Task 4.1 — Run full roadmap test suite
- **Command**: `uv run pytest tests/roadmap/ -v`
- **Expected**: All tests green. Any failures indicate tests that implicitly depended on `convergence_enabled=False` default and need explicit `convergence_enabled=False` added.

### Task 4.2 — Scan for implicit default dependencies
- **Action**: If Task 4.1 surfaces failures, grep for `RoadmapConfig()` constructions in test files that don't set `convergence_enabled` explicitly, and assess whether they need the old behavior.
- **Fix pattern**: Add `convergence_enabled=False` to test configs that test non-convergence behavior.

---

## Phase 5: Reflection

### Task 5.1 — Run `/sc:reflect --type session --validate`
- **Action**: Execute session reflection to validate the implementation
- **Checkpoint**: Reflection passes with no critical findings

---

## Dependency Map

```
Task 1.1 (flip default)
    ├── Task 2.1 (click option)    [parallel]
    ├── Task 2.2 (fn signature)    [depends on 2.1]
    └── Task 2.3 (wire kwargs)     [depends on 2.2]
         ├── Task 3.1 (update default test)     [parallel]
         ├── Task 3.2 (verify dispatch tests)   [parallel]
         └── Task 3.3 (add CLI flag tests)      [parallel]
              └── Task 4.1 (full suite)
                   └── Task 4.2 (fix implicit deps)
                        └── Task 5.1 (reflect)
```

## Files Modified (Summary)

| File | Change |
|------|--------|
| `src/superclaude/cli/roadmap/models.py` | 1 line: default `False` → `True` |
| `src/superclaude/cli/roadmap/commands.py` | ~8 lines: option + param + kwarg |
| `tests/roadmap/test_remediation.py` | Rename + flip assertion |
| `tests/roadmap/test_convergence_wiring.py` | Add 3 new tests |
