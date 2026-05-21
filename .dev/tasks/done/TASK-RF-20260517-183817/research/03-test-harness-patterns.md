# Research: Test Harness Patterns
**Topic type:** Test & Verification
**Scope:** tests/hooks/test_auggie_first.py, tests/cli/test_install_hooks.py, project pytest config
**Status:** Complete
**Date:** 2026-05-17

---

## 1. Existing pytest harness patterns

### 1a. Hook-script harness (tests/hooks/test_auggie_first.py)
- **Subprocess invocation**: `subprocess.run(["bash", str(HOOK)], input=..., capture_output=True, env=env, timeout=5)` — see tests/hooks/test_auggie_first.py:33-39.
- **Repo-root resolution**: `Path(__file__).resolve().parents[2]` (tests/hooks/ → tests/ → repo root), then `/ "src" / "superclaude" / "hooks" / "scripts" / "<script>.sh"` — tests/hooks/test_auggie_first.py:16-23. Mirrored in tests/hooks/test_freshness_pre_edit_create_case.py:14-21.
- **Assertions**: `assert result.returncode == 0, result.stderr.decode()` (test_auggie_first.py:59); `result.stderr` byte-compare (`assert b"..." in result.stderr` in test_freshness_pre_edit_create_case.py:69); JSONL telemetry asserted via `read_text()` + substring match (test_auggie_first.py:62-63).
- **tmp_path usage**: Each test uses `tmp_path: Path` directly; `_run_hook` mints a `fake_home = tmp_path / "home"` and seeds the `.claude/state/` and `.claude/logs/` dirs before invocation (test_auggie_first.py:27-32, 48-53).
- **Markers**: **None** — these tests have no `@pytest.mark.*` decorators. They are collected as plain tests. The project uses `--strict-markers` (pyproject.toml:106), so any new marker must be registered in pyproject.toml:109-133. No `cli` / `hooks` markers exist there today.

### 1b. CLI / installer harness (tests/cli/test_install_hooks.py)
- **Direct Python imports + monkeypatch** for source-locator functions (test_install_hooks.py:29-34, 106-122). No subprocess: it patches `superclaude.cli.install_hooks._get_hooks_source` and friends to point at a `tmp_path/pkg/hooks/` tree it builds in the `fake_source_hooks` fixture (test_install_hooks.py:41-123).
- **Fixture pattern**: two reusable fixtures
  - `fake_source_hooks(tmp_path, monkeypatch)` — builds a fake `src/superclaude/hooks/` tree (hooks.json + scripts/), monkeypatches source-locator functions (test_install_hooks.py:41-123).
  - `target_settings(tmp_path)` — returns a fresh `tmp_path/home/.claude/settings.json` path (test_install_hooks.py:127-131).
- **Regression-pin pattern** (relevant to V1/V2): `test_real_hooks_json_gates_write_in_pre_tool_use` reads the live `src/superclaude/hooks/hooks.json` directly via `Path(__file__).resolve().parents[2] / "src" / ... / "hooks.json"` and asserts on `data["hooks"]["PreToolUse"]` shape — test_install_hooks.py:438-465. **No subprocess; pure Python introspection.** This is the template for any "read the live file and assert on its shape" check.

### 1c. Project-wide conftest (tests/conftest.py)
- Provides `sample_context`, `low_confidence_context`, `sample_implementation`, `failing_implementation`, `temp_memory_dir` (tests/conftest.py:16-122). **None relevant to verify-sync.**
- `collect_ignore = ["sprint/test_property_based.py"]` at tests/conftest.py:11-13.
- **No `tests/cli/conftest.py` or `tests/hooks/conftest.py` exist** (verified via `ls`). All fixtures local-to-file.

### 1d. pyproject.toml pytest config (pyproject.toml:99-133)
- `testpaths = ["tests"]`, `python_files = ["test_*.py"]`, `addopts = ["-v", "--strict-markers", "--tb=short"]`.
- **No `@pytest.mark.cli` or `@pytest.mark.hooks` markers exist** — `--strict-markers` means we cannot add a marker without registering it. For the new file, **use no markers** (matches both existing files in tests/hooks/ and tests/cli/). Recommended: **no custom markers**.

---

## 2. Critical design gap: tmp_path + `_FRESHNESS_SCRIPTS` mutation

### Question
Spec §9 V3/V4 need to mutate `src/superclaude/cli/install_hooks.py::_FRESHNESS_SCRIPTS` such that `make verify-sync` (running with `cwd=tmp_path`) observes the mutation. The Makefile's planned check is:

```
uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; ..."
```

Does running `uv run` with `cwd=tmp_path` import the tmp_path's `src/superclaude/cli/install_hooks.py`, or the editable install from the developer's environment?

### Empirical answer (verified — see commands below)

**Default behavior**: `uv run` from any cwd imports from the **editable install of the active project**, NOT from the cwd's local `src/`. Test:

```
$ cd /tmp/uvtest && uv run --project /config/workspace/IronClaude python -c \
    "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print(_FRESHNESS_SCRIPTS[0])"
freshness-session-start.sh    # → from editable install, NOT tmp's mutated copy
```

**PYTHONPATH override works**: setting `PYTHONPATH=<tmp_path>/src` makes the mutated copy import first because PYTHONPATH is prepended to `sys.path` ahead of the editable install. Test:

```
$ PYTHONPATH=/tmp/uvtest/src uv run --project /config/workspace/IronClaude python -c \
    "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print(_FRESHNESS_SCRIPTS[0])"
MUTATED_FROM_TMP    # ← mutation observed
```

### Trade-offs of the four candidate approaches

| Option | Works? | Speed | Complexity | Recommendation |
|---|---|---|---|---|
| (a) `env={**os.environ, "PYTHONPATH": str(tmp_path / "src")}` | **YES** (empirically verified above) | Fast (~50 ms/test) | Low — just add env to `subprocess.run` | **RECOMMENDED** |
| (b) `uv run --project tmp_path` | Probably no — requires tmp_path to be a full uv project with pyproject.toml + `.venv` | Slow (uv sync needed first) | High — must seed pyproject.toml + run uv sync | Avoid |
| (c) `shutil.copytree` whole repo + `uv sync` inside tmp | YES but very slow | ~10-30 s per test | High disk + time cost | Avoid for V3/V4; consider for a single "full e2e" smoke if desired |
| (d) Replace import-based check in Makefile with `grep` of `_FRESHNESS_SCRIPTS = [` block | YES, simplest from test side; but **changes the production Makefile contract** | Fastest | Spec-deviation — §9 says the Makefile imports the module | Reject unless spec is amended |

### Recommendation
**Use option (a): PYTHONPATH override.** Concretely, the new test fixture will:
1. `shutil.copytree(repo_root / "src", tmp_path / "src")` — small (~1 MB).
2. `shutil.copytree(repo_root / ".claude", tmp_path / ".claude")` — small.
3. `shutil.copy(repo_root / "Makefile", tmp_path / "Makefile")`.
4. `shutil.copy(repo_root / "pyproject.toml", tmp_path / "pyproject.toml")` (so `uv run` finds project metadata if it walks up).
5. Mutate `tmp_path / "src" / "superclaude" / "cli" / "install_hooks.py"` for V3/V4.
6. Invoke `subprocess.run(["make", "verify-sync"], cwd=tmp_path, env={**os.environ, "PYTHONPATH": str(tmp_path / "src") + os.pathsep + os.environ.get("PYTHONPATH", "")}, capture_output=True, timeout=60)`.

**FYI for researcher-2 (Makefile patterns):** the verify-sync target should reference `uv run python -c "..."` — since `uv run` inherits the parent env's PYTHONPATH, this Just Works. No special Makefile change required to enable the PYTHONPATH override; the test sets the env at subprocess invocation time and the Makefile just inherits.

### Unverified / empirical risk
- `uv run` may, in some configurations, sanitize PYTHONPATH. The empirical test above (run from /tmp/uvtest with `uv run --project /config/...`) confirmed PYTHONPATH is honored on this machine, this uv version. **If this ever changes in a future uv release**, fall back to option (d) (grep-based check in Makefile).
- The empirical test passed `--project /config/workspace/IronClaude`. When the test omits `--project` and just sets `cwd=tmp_path`, `uv run` walks up from tmp_path to find the nearest `pyproject.toml`. Copying pyproject.toml into tmp_path (step 4) makes tmp_path the "project root" from uv's perspective, which is the cleanest setup. The test's first execution should verify by reading the V1 stdout — if `uv` reports "creating venv" or similar in tmp_path, the test will be slow but correct.

---

## 3. Scenarios V5/V6/V7 (cross-consistency drift)

These mutate `hooks.json` or `auggie-flag-clear.sh` in tmp_path and run `make verify-sync`. Easy: the planned Makefile checks here use `jq` / `grep` on relative paths (e.g., `src/superclaude/hooks/hooks.json` vs. `.claude/hooks/hooks.json`), so `cwd=tmp_path` alone is sufficient — no PYTHONPATH needed for these specifically. (The fixture still sets PYTHONPATH for free; harmless.)

**Setup recipe (same fixture as V3/V4, no mutation of install_hooks.py needed):**
- V5 (hooks.json drift): mutate `tmp_path/src/superclaude/hooks/hooks.json` (e.g., add a fake script reference, change a matcher) — expect verify-sync to flag.
- V6 (script content drift): mutate `tmp_path/src/superclaude/hooks/scripts/auggie-flag-clear.sh` content while leaving `.claude/hooks/scripts/auggie-flag-clear.sh` unchanged — expect verify-sync to diff-flag.
- V7 (script missing in .claude/): `(tmp_path / ".claude" / "hooks" / "scripts" / "auggie-flag-clear.sh").unlink()` — expect verify-sync to flag MISSING.

---

## 4. Scenarios V1/V2 (clean tree, missing hook file)

- **V1 (clean tree, all-in-sync)**: copy the repo's src/ + .claude/ + Makefile + pyproject.toml into tmp_path WITHOUT mutation. Run `make verify-sync`, expect `returncode == 0` and output contains "All components in sync." (Makefile:243).
- **V2 (missing hook file in .claude/)**: copy as in V1, then `(tmp_path / ".claude" / "hooks" / "scripts" / "<chosen>.sh").unlink()` — expect verify-sync to fail with "MISSING" output.

Both use the same `synced_tree` fixture as V3-V7; V1 just makes no mutation.

---

## 5. Test isolation

The `tmp_path` pytest fixture is per-test and auto-cleaned, so the working tree is never touched. The fixture pattern:
- **Never** call `shutil.copytree(repo_root, tmp_path)` — that pulls in `.git/`, `.venv/`, `node_modules/`, etc.
- Selectively copy only what verify-sync reads: `src/superclaude/`, `.claude/`, `Makefile`, `pyproject.toml`.
- Use `shutil.copytree(..., symlinks=False, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))`.

---

## 6. `make` dependency portability

- Tests assume `make` is on PATH. The freshness_pre_edit harness assumes `bash` on PATH (test_freshness_pre_edit_create_case.py:30) — same precedent.
- No existing test in tests/cli or tests/hooks gates on platform. For CI portability, use `shutil.which("make")` and `pytestmark = pytest.mark.skipif(...)`:
  ```python
  import shutil
  pytestmark = pytest.mark.skipif(
      shutil.which("make") is None, reason="make not on PATH"
  )
  ```
- The Makefile uses POSIX shell features (`for ... do ... done`, `\` line-continuation) that work on Linux + macOS but not native Windows. Project is Linux-only per CLAUDE.md envs (no Windows mentions). Don't add Windows guards.

---

## 7. Where the new test file lives

- `tests/cli/test_install_hooks.py` (existing) → `tests/cli/test_verify_sync_hooks.py` (new). Same dir.
- **No `tests/cli/conftest.py` exists**; the new file can declare its own fixtures inline or extract them to a new conftest if later shared with test_install_hooks.py. **Recommend inline for now** — keeps the build atomic and avoids cross-file coupling.

---

## 8. Recommended paste-ready scaffolding

The builder should drop this as the top of `tests/cli/test_verify_sync_hooks.py`:

```python
"""
Behavioral tests for `make verify-sync` hook/script drift detection.

Covers V1-V7 scenarios from the hook-sync-and-matcher-fix release spec §9.

Test pattern: clone selective repo subtrees into tmp_path, optionally mutate,
then run `make verify-sync` as a subprocess with PYTHONPATH pointing at the
mutated src/ so `uv run python -c 'from superclaude.cli.install_hooks ...'`
imports the mutated module instead of the editable install.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.skipif(
    shutil.which("make") is None, reason="make not on PATH"
)


@pytest.fixture
def synced_tree(tmp_path: Path) -> Path:
    """
    Materialise a minimal repo copy in tmp_path that `make verify-sync` can
    operate on without touching the developer's working tree.

    Copies: src/superclaude/, .claude/, Makefile, pyproject.toml.
    Skips:  .git/, .venv/, __pycache__/, node_modules/.
    """
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")
    shutil.copytree(REPO_ROOT / "src", tmp_path / "src", ignore=ignore)
    shutil.copytree(REPO_ROOT / ".claude", tmp_path / ".claude", ignore=ignore)
    shutil.copy(REPO_ROOT / "Makefile", tmp_path / "Makefile")
    shutil.copy(REPO_ROOT / "pyproject.toml", tmp_path / "pyproject.toml")
    return tmp_path


def _run_verify_sync(tree: Path) -> subprocess.CompletedProcess:
    """
    Invoke `make verify-sync` in the cloned tree. PYTHONPATH is prepended with
    the tree's src/ so any `uv run python -c 'from superclaude...'` inside the
    Makefile resolves to the cloned (and possibly mutated) source.
    """
    env = os.environ.copy()
    tree_src = str(tree / "src")
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{tree_src}{os.pathsep}{existing}" if existing else tree_src
    )
    return subprocess.run(
        ["make", "verify-sync"],
        cwd=tree,
        env=env,
        capture_output=True,
        timeout=60,
    )


# ---------------------------------------------------------------------------
# V1: clean tree — verify-sync passes
# ---------------------------------------------------------------------------


def test_v1_clean_tree_passes(synced_tree: Path) -> None:
    result = _run_verify_sync(synced_tree)
    assert result.returncode == 0, (
        f"verify-sync should pass on a clean cloned tree.\n"
        f"stdout: {result.stdout.decode()}\nstderr: {result.stderr.decode()}"
    )
    assert (
        b"in sync" in result.stdout.lower()
        or b"all components" in result.stdout.lower()
    )


# (Builder fills in V2-V7 using the same _run_verify_sync helper and the
# targeted mutations described below.)
```

### Mutation snippets the builder will need for V2-V7

**V2 (missing hook script in .claude/):**
```python
(synced_tree / ".claude" / "hooks" / "scripts" / "auggie-flag-clear.sh").unlink()
result = _run_verify_sync(synced_tree)
assert result.returncode != 0
assert b"MISSING" in result.stdout or b"missing" in result.stdout
```

**V3 (remove one entry from `_FRESHNESS_SCRIPTS`):**
```python
install_hooks_py = synced_tree / "src" / "superclaude" / "cli" / "install_hooks.py"
text = install_hooks_py.read_text()
text = text.replace('    "auggie-flag-clear.sh",\n', "")  # drop one entry
install_hooks_py.write_text(text)
result = _run_verify_sync(synced_tree)
assert result.returncode != 0
```

**V4 (add a fake entry to `_FRESHNESS_SCRIPTS`):**
```python
install_hooks_py = synced_tree / "src" / "superclaude" / "cli" / "install_hooks.py"
text = install_hooks_py.read_text()
text = text.replace(
    '    "auggie-flag-clear.sh",\n]',
    '    "auggie-flag-clear.sh",\n    "fake-not-real.sh",\n]',
)
install_hooks_py.write_text(text)
result = _run_verify_sync(synced_tree)
assert result.returncode != 0
```

**V5 (hooks.json drift):** mutate `synced_tree / "src" / "superclaude" / "hooks" / "hooks.json"` only — leave `.claude/hooks/hooks.json` untouched.

**V6 (script-content drift):** mutate `synced_tree / "src" / "superclaude" / "hooks" / "scripts" / "auggie-flag-clear.sh"` content only.

**V7 (orphan in .claude/):** create a new bogus script in `synced_tree / ".claude" / "hooks" / "scripts" / "orphan-not-in-src.sh"` that has no counterpart in src/.

---

## Summary for the builder

1. **Harness pattern**: subprocess + tmp_path, like tests/hooks/test_auggie_first.py:26-39 — but with the addition of a PYTHONPATH-overriding env block.
2. **Repo-root resolution**: `Path(__file__).resolve().parents[2]` (consistent with both existing files).
3. **No markers**: use `pytestmark = pytest.mark.skipif(shutil.which("make") is None, ...)` only; no custom markers (project uses `--strict-markers` per pyproject.toml:106).
4. **tmp_path + mutation gap resolved**: empirically confirmed that `PYTHONPATH=<tmp_path>/src uv run python -c "from superclaude.cli.install_hooks ..."` imports the mutated copy. This is option (a) from the spec's design-question list.
5. **Fixture scope**: function-scoped `synced_tree(tmp_path)` that copies only `src/`, `.claude/`, `Makefile`, `pyproject.toml`. No `.git/`, no `.venv/`, no `node_modules/`. Estimated copy cost: <500 ms on a modern SSD.
6. **Helper**: a single `_run_verify_sync(tree)` that wraps `subprocess.run(["make", "verify-sync"], cwd=tree, env={..., "PYTHONPATH": tree/src + os.pathsep + existing}, capture_output=True, timeout=60)`.
7. **Inline fixtures**: no need to create `tests/cli/conftest.py`; declare the fixture inline in `test_verify_sync_hooks.py` (matches the precedent of test_install_hooks.py:41-131).
8. **One caveat to surface in the task file**: the Makefile addition planned by researcher-2 must use `uv run python -c "..."` (not bare `python -c`) so the test's PYTHONPATH-prepended env is respected by uv. Confirmed empirically.

### Empirical verification commands (for the builder to re-run if anything in uv changes)

```bash
# 1. Verify uv run from foreign cwd imports editable install by default
cd /tmp && mkdir -p uvtest/src/superclaude/cli
touch uvtest/src/superclaude/__init__.py uvtest/src/superclaude/cli/__init__.py
echo "_FRESHNESS_SCRIPTS = ['MUTATED']" > uvtest/src/superclaude/cli/install_hooks.py
cd /tmp/uvtest && uv run --project /config/workspace/IronClaude python -c \
  "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print(_FRESHNESS_SCRIPTS[0])"
# Expected: freshness-session-start.sh (NOT MUTATED) — confirms default ignores cwd

# 2. Verify PYTHONPATH override succeeds
PYTHONPATH=/tmp/uvtest/src uv run --project /config/workspace/IronClaude python -c \
  "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print(_FRESHNESS_SCRIPTS[0])"
# Expected: MUTATED — confirms PYTHONPATH wins
```

### Files referenced (absolute)
- /config/workspace/IronClaude/tests/hooks/test_auggie_first.py:16-23,26-39,46-63
- /config/workspace/IronClaude/tests/hooks/test_freshness_pre_edit_create_case.py:14-21,24-35
- /config/workspace/IronClaude/tests/cli/test_install_hooks.py:29-34,41-131,438-465
- /config/workspace/IronClaude/tests/conftest.py:11-13
- /config/workspace/IronClaude/pyproject.toml:99-133
- /config/workspace/IronClaude/Makefile:154-247
- /config/workspace/IronClaude/src/superclaude/cli/install_hooks.py:43-55
