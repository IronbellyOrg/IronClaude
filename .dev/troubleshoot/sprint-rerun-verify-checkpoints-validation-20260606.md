# Spec — Fix `sprint rerun-tasks` → `verify-checkpoints` option mismatch

**Date:** 2026-06-06
**Status:** validated (pre-execution reflection PASS) — ready to implement
**Scope:** localized CLI wiring + test-gap fix (NOT a design change)

## Problem (confirmed root cause)

After a successful `superclaude sprint rerun-tasks <index> --phase N --tasks T..`
merge-back, the post-merge auto-verify step emits:

```
Usage: superclaude sprint verify-checkpoints [OPTIONS] OUTPUT_DIR
Error: No such option '--phase'. Did you mean '--help'?
```

**Cause (verified against `src/`):**

- `src/superclaude/cli/sprint/rerun_tasks.py:1449-1462` shells out to
  `uv run superclaude sprint verify-checkpoints --recover --phase <n> --quiet`
  — **no positional `OUTPUT_DIR`**, and `--phase` / `--quiet` are passed.
- `src/superclaude/cli/sprint/commands.py:387-403` defines `verify-checkpoints`
  with a **required positional `output_dir`** and only `--recover` / `--json`.
  No `--phase`, no `--quiet`.
- Empirically reproduced via `CliRunner` against the real command:
  `Error: No such option: --phase` (and `--quiet` independently rejected).
- `subprocess.run(..., check=False)` → the exit-2 child only prints Usage/Error;
  the rerun still returns success. Net effect: the **post-merge checkpoint
  manifest/recovery is silently skipped on every rerun**.

## Decision (remediated by pre-execution reflection)

Two fix approaches were considered:

- **Approach A (in-process)** — replace the subprocess with
  `build_manifest(config.index_path, config.release_dir)` +
  `recover_missing_checkpoints(...)` + `write_manifest(...)`.
  **REJECTED for v1** by the pre-execution audit: `config.release_dir` resolves
  to the **grandparent** in the `sc:tasklist` subdir layout (`_resolve_release_dir`,
  `config.py:242-278`), while checkpoint files physically live in the `tasklist/`
  **subdir** alongside the index. Feeding `build_manifest` the grandparent as
  `release_dir` resolves checkpoint paths to a directory where they do not exist.
  Layout-dependent correctness risk; defer to a future refactor.

- **Approach B (minimal subprocess argv fix)** — **SELECTED.** Keep the subprocess;
  drop `--phase` / `--quiet`; pass `config.index_path.parent` as the positional.
  Reuses the already-tested `verify_checkpoints` CLI code path, which derives
  index-dir, checkpoint-dir, and artifacts-dir all from the one positional that is
  **guaranteed to contain `tasklist-index.md`** (`index_path.parent`). Empirically
  proven argv shape (`test_checkpoints.py:560` exercises `[dir, "--recover"]` → exit 0).
  Smallest safe change; sidesteps the grandparent-vs-subdir question entirely.

`--phase` is intentionally NOT added to `verify-checkpoints` — the command verifies
the whole-sprint manifest across all phases; there is no per-phase mode.

## Implementation

### File: `src/superclaude/cli/sprint/rerun_tasks.py` (~1449-1462)

Replace the argv list inside the existing `try` / `except OSError` block:

```python
subprocess.run(
    [
        "uv", "run", "superclaude", "sprint",
        "verify-checkpoints",
        str(config.index_path.parent),   # positional OUTPUT_DIR (contains tasklist-index.md)
        "--recover",
    ],
    check=False,
)
```

Remove `--phase`, `str(phase)`, and `--quiet`. Keep `check=False` and the
`except OSError` guard (verify failures stay non-fatal).

### Tests

1. `tests/sprint/test_checkpoints.py` → `TestVerifyCheckpointsCLI` — add
   `test_phase_option_is_rejected`: `runner.invoke(verify_checkpoints,
   [str(tmp_path), "--recover", "--phase", "13"])` → `exit_code == 2` and
   `"No such option" in result.output`. Contract-lock that documents the bug.

2. `tests/sprint/test_rerun_tasks_e2e.py:287-294` — replace the mocked-argv
   substring assertions with a **round-trip**: strip the
   `uv run superclaude sprint` prefix from the captured argv and feed it to
   `CliRunner().invoke(verify_checkpoints, stripped_argv)`; assert
   `result.exit_code == 0`. This closes the blind spot (the mocked test never
   round-tripped the argv through the real parser, which is why the bug shipped).

## Acceptance criteria

- AC1: `rerun_tasks.py` post-merge argv contains the positional
  `config.index_path.parent` and `--recover`, and contains neither `--phase`
  nor `--quiet`.
- AC2: `test_phase_option_is_rejected` passes (exit 2 + "No such option").
- AC3: e2e round-trip test asserts the built argv parses (exit 0) against the
  real `verify_checkpoints` command.
- AC4: `uv run pytest tests/sprint -q` green.
- AC5: `uv run ruff check` + `uv run ruff format --check` clean on the edited file.

## Commands (UV only)

```
uv run pytest tests/sprint/test_checkpoints.py tests/sprint/test_rerun_tasks_e2e.py tests/sprint/test_rerun_tasks.py tests/sprint/test_rerun_tasks_failure_modes.py -v
uv run pytest tests/sprint -q
uv run ruff check src/superclaude/cli/sprint/rerun_tasks.py && uv run ruff format --check src/superclaude/cli/sprint/rerun_tasks.py
```

## Risk / backward-compat

- Low. The block is already best-effort (`check=False`) and currently a silent
  no-op (the child always exit-2s before doing work). The fix **restores intended
  behavior**; nothing depended on the no-op.
- No `commands.py` change (the command contract is correct as-is).
- No `.claude/` sync needed — CLI is pure `src/` Python, not a synced
  skill/agent/command.
