---
phase: phase-2 aggregation for PG-2 rf-qa gate
captured: 2026-05-19
workspace: /config/workspace/IronClaude-T1-sprint
branch: feat/sprint-state-migration
---

# Phase 2 Aggregation Report — for rf-qa PG-2 task-integrity gate

This report is the single artifact rf-qa MUST read to assess Phase 2. All six source-change diffs are extracted from the current working-tree state via `git diff` and cross-referenced against the Step 2.1–2.6 descriptions in the task file. Test results are summarized from `phase-outputs/test-results/baseline-summary.md` and `phase-outputs/test-results/phase2-summary.md`.

---

## File 1 — `src/superclaude/cli/sprint/models.py` (Step 2.1)

Hunk A (after `total_tasks: int = 0` at line 397): add `state_dir` field + `_derive_tasklist_id()` helper method.

```python
+    # Transient runtime state directory (e.g. .sprint-exitcode sentinel). Default resolved in __post_init__; override via SPRINT_STATE_DIR env var or --state-dir CLI flag.
+    state_dir: Path = field(default_factory=lambda: Path(""))
+
+    def _derive_tasklist_id(self) -> str:
+        """Derive a stable tasklist identifier for the default state_dir path.
+
+        Preference order: release_dir.name (when meaningful) -> index_path.parent.name
+        (when meaningful) -> index_path.stem -> "default".
+        """
+        release_name = self.release_dir.name
+        if self.release_dir != Path(".") and release_name not in ("", "."):
+            return release_name
+        parent_name = self.index_path.parent.name
+        if parent_name not in ("", "."):
+            return parent_name
+        return self.index_path.stem or "default"
```

Hunk B (end of `__post_init__`, after the `wiring_gate_mode` derivation block around line 458): append the empty-Path sentinel derivation block.

```python
+        # Derive default state_dir from a tasklist-id when the field is the
+        # empty-Path sentinel. The sentinel is Path("") (NOT Path(".")) so we
+        # don't collide with release_dir's default and break test isolation.
+        if self.state_dir == Path(""):
+            object.__setattr__(
+                self,
+                "state_dir",
+                Path(".dev/sprint-state") / self._derive_tasklist_id(),
+            )
```

**Notes for QA**: `PipelineConfig` (parent) has NO `__post_init__` (verified by reading `src/superclaude/cli/pipeline/models.py:180`), so no `super().__post_init__()` call is needed. Mutation uses `object.__setattr__` consistent with the existing `work_dir` mirror.

---

## File 2 — `src/superclaude/cli/sprint/config.py` (Step 2.2)

Hunk A (`load_sprint_config()` signature, end of kwargs at line 288): add `state_dir: Path | None = None`.

```python
+    state_dir: Path | None = None,
 ) -> SprintConfig:
-    """Load and validate a complete sprint configuration."""
+    """Load and validate a complete sprint configuration.
+
+    ``state_dir``: optional override for transient sprint state directory
+    (default derived from release_dir.name in SprintConfig.__post_init__).
+    """
```

Hunk B (`SprintConfig(...)` construction call, after `total_tasks=total_tasks,`): thread the param.

```python
         total_tasks=total_tasks,
+        state_dir=state_dir if state_dir is not None else Path(""),
     )
```

---

## File 3 — `src/superclaude/cli/sprint/commands.py` (Step 2.3)

Hunk A (after the `--release-dir` `@click.option` decorator block at lines 175–181): add `--state-dir` decorator.

```python
+@click.option(
+    "--state-dir",
+    "state_dir_override",
+    type=click.Path(file_okay=False, path_type=Path),
+    default=None,
+    help="Transient state directory for .sprint-exitcode and other runtime artifacts (default: $SPRINT_STATE_DIR or .dev/sprint-state/<tasklist-id>/).",
+)
```

Hunk B (`run()` signature after `release_dir_override: Path | None,`): add the new param.

```python
     release_dir_override: Path | None,
+    state_dir_override: Path | None,
 ):
```

Hunk C (before the `load_sprint_config(...)` call): resolve env var.

```python
+    state_dir = state_dir_override or (
+        Path(os.environ["SPRINT_STATE_DIR"])
+        if os.environ.get("SPRINT_STATE_DIR")
+        else None
+    )
+
     config = load_sprint_config(
         ...
+        state_dir=state_dir,
     )
```

Hunk D (inside the `if release_dir_override is not None:` block, AFTER the existing `object.__setattr__(config, "release_dir", resolved)` and `object.__setattr__(config, "work_dir", resolved)` lines): re-derive state_dir.

```python
     if release_dir_override is not None:
+        original_release_dir_name = config.release_dir.name
         resolved = Path(release_dir_override).resolve()
         object.__setattr__(config, "release_dir", resolved)
         object.__setattr__(config, "work_dir", resolved)
+        # Re-derive state_dir under the new release name when no explicit
+        # state_dir was provided AND the current state_dir matches the
+        # original auto-derivation. This resolves OQ-1 by keeping the
+        # default factory consistent with the post-override release_dir.
+        if (
+            state_dir is None
+            and config.state_dir
+            == Path(".dev/sprint-state") / original_release_dir_name
+        ):
+            object.__setattr__(
+                config,
+                "state_dir",
+                Path(".dev/sprint-state") / resolved.name,
+            )
```

**Notes for QA**: `original_release_dir_name` is captured BEFORE the `release_dir` mutation, so the comparison against the pre-mutation default factory works. `work_dir` is intentionally not mirrored to `state_dir` per the work_dir parallel note in Step 2.3 (work_dir is per-sprint scratch; state_dir is dedicated exit-code state).

---

## File 4 — `src/superclaude/cli/sprint/executor.py` (Step 2.4)

Hunk A (sentinel writer at line 1751–1756): migrate from `release_dir` to `state_dir`, add `mkdir(parents=True, exist_ok=True)`, preserve `try/except OSError: pass`.

```python
-    # Write sentinel exit code file so tmux caller can read the outcome
+    # Write sentinel exit code file in state_dir (non-tracked transient path) so tmux caller can read the outcome
     _exitcode = 0 if sprint_result.outcome == SprintOutcome.SUCCESS else 1
     try:
-        (config.release_dir / ".sprint-exitcode").write_text(str(_exitcode))
+        state_dir = config.state_dir
+        state_dir.mkdir(parents=True, exist_ok=True)
+        (state_dir / ".sprint-exitcode").write_text(str(_exitcode))
     except OSError:
         pass  # best-effort; do not mask the real exit
```

**Notes for QA**: No other `config.release_dir` references in `executor.py` were modified — the ~10 other `release_dir` reads at archive-related lines remain legitimate archive-path uses.

---

## File 5 — `src/superclaude/cli/sprint/tmux.py` (Step 2.5)

Hunk A (sentinel reader at line 166): single-line change.

```python
-    sentinel = config.release_dir / ".sprint-exitcode"
+    sentinel = config.state_dir / ".sprint-exitcode"
```

**Notes for QA**: The other `release_dir` reads in `tmux.py` (used for `session_name()` hashing at ~line 60 and ~87) are intentionally NOT changed.

---

## File 6 — `tests/sprint/test_tmux.py` (Step 2.6)

Hunk A (fixture in `TestThreePaneLayout::test_launch_creates_three_panes` at line ~100): migrate fixture path + add `mkdir`.

```python
         # Make the sentinel read succeed with exit 0 so launch returns cleanly.
-        sentinel = config.release_dir / ".sprint-exitcode"
+        config.state_dir.mkdir(parents=True, exist_ok=True)
+        sentinel = config.state_dir / ".sprint-exitcode"
         sentinel.write_text("0\n")
```

---

## Ruff + Pytest deltas vs. baseline

From `phase-outputs/test-results/baseline-summary.md` and `phase-outputs/test-results/phase2-summary.md`:

| Metric | Baseline | Phase 2 | Delta |
|---|---|---|---|
| Ruff errors total | 11 | 11 | 0 |
| Ruff errors in modified files | 0 | 0 | 0 |
| Pytest failed | 57 | 57 | 0 |
| Pytest passed | 1350 | 1350 | 0 |
| Pytest skipped | 1 | 1 | 0 |
| New regressions (was PASS, now FAIL) | n/a | 0 | 0 |
| test_tmux.py — all 11 pass | yes | yes | ✓ |

All 57 pytest failures share root cause `AttributeError: '<FakePopen-class> object' has no attribute 'stdin'` and predate this task. Identical failing-test set vs. baseline.

---

## Acceptance Criteria for PG-2 (what rf-qa must verify)

- **AC1** — `SprintConfig` in `src/superclaude/cli/sprint/models.py` has a `state_dir: Path` field with empty-Path sentinel default (`field(default_factory=lambda: Path(""))`) AND `__post_init__` derives `Path(".dev/sprint-state") / self._derive_tasklist_id()` when the sentinel is detected, using `object.__setattr__`.
- **AC2** — `load_sprint_config()` in `src/superclaude/cli/sprint/config.py` accepts an optional `state_dir: Path | None = None` and forwards it to the `SprintConfig(...)` construction call as `state_dir=state_dir if state_dir is not None else Path("")`.
- **AC3** — `commands.py::run` has a `--state-dir` Click option (with `state_dir_override` dest), resolves `SPRINT_STATE_DIR` env var, threads it through to `load_sprint_config(..., state_dir=...)`, AND the `--release-dir` post-construction override re-derives `state_dir` when `state_dir` was auto-derived AND the current `state_dir` still equals `Path(".dev/sprint-state") / original_release_dir_name`.
- **AC4** — `executor.py` writer uses `config.state_dir / ".sprint-exitcode"` with a preceding `state_dir.mkdir(parents=True, exist_ok=True)`; `tmux.py` reader uses `config.state_dir / ".sprint-exitcode"`. Both are wrapped in their original `try/except` blocks.
- **AC5** — `tests/sprint/test_tmux.py:~100` fixture writes to `state_dir` (with a preceding `mkdir(parents=True, exist_ok=True)`) instead of `release_dir`.
- **AC6** — Ruff and pytest deltas vs. baseline are both zero (no NEW errors, no NEW failing tests). All 11 tests in `tests/sprint/test_tmux.py` pass.

---

## File paths for rf-qa cross-check

- Modified source: `src/superclaude/cli/sprint/models.py`, `src/superclaude/cli/sprint/config.py`, `src/superclaude/cli/sprint/commands.py`, `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/tmux.py`, `tests/sprint/test_tmux.py`
- Baseline: `.dev/tasks/to-do/TASK-RF-track-1-20260518-231708/phase-outputs/test-results/baseline-summary.md`
- Phase 2 results: `.dev/tasks/to-do/TASK-RF-track-1-20260518-231708/phase-outputs/test-results/phase2-summary.md`
- Phase 2 raw ruff: `.dev/tasks/to-do/TASK-RF-track-1-20260518-231708/phase-outputs/test-results/phase2-ruff.txt`
- Phase 2 raw pytest: `.dev/tasks/to-do/TASK-RF-track-1-20260518-231708/phase-outputs/test-results/phase2-pytest.txt`
