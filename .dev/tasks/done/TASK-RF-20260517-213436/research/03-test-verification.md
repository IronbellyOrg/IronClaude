# Research: Test & Verification — hook-sync-and-matcher-fix
**Topic type:** Test & Verification
**Scope:** New pytest file for verify-sync hook scenarios V1-V7; existing test patterns to mirror; tmp_path mutation strategy
**Status:** Complete
**Date:** 2026-05-17
---

## Section 1: Existing subprocess-based test pattern (`tests/hooks/test_auggie_first.py`)

**File:** `/config/workspace/IronClaude/tests/hooks/test_auggie_first.py` (124 lines, 5 tests)

### Subprocess invocation style

Verbatim from `test_auggie_first.py:26-39`:

```python
def _run_hook(payload: dict, fake_home: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    (fake_home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    (fake_home / ".claude" / "logs").mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        timeout=5,
    )
```

Notable signature decisions:
- `args` is a list (`["bash", str(HOOK)]`) — never shell-strings.
- `input=` is bytes (`json.dumps(...).encode()`), not `text=True`.
- `capture_output=True` (NOT `stdout=PIPE, stderr=PIPE` long form).
- `env=env` after copying `os.environ` and patching `HOME` (NOT `monkeypatch.setenv` — direct env-dict).
- `timeout=5` — every subprocess has a timeout to prevent hangs.
- No `check=True` — tests assert on `result.returncode` explicitly so failures surface in the assertion message.
- No `cwd=` (the HOOK path is absolute; cwd doesn't matter for these hooks).

### Stdout / stderr / exit assertions

Verbatim from `test_auggie_first.py:58-63`:

```python
result = _run_hook(payload, fake_home=home)
assert result.returncode == 0, result.stderr.decode()
assert not _sticky_path(home, sid).exists()
telemetry = (home / ".claude" / "logs" / "auggie-first.jsonl").read_text()
assert '"event":"sticky_cleared"' in telemetry
```

Pattern: `result.returncode == N, result.stderr.decode()` — error message in the assertion is the *decoded stderr*, giving immediate diagnostics on failure.

### tmp_path / HOME redirection

- Uses the built-in `tmp_path: Path` fixture as the only fixture.
- Constructs `home = tmp_path / "home"` inside each test (not in a fixture) — keeps tests self-contained.
- Pre-creates required directories (`.claude/state/auggie-first-pending`, `.claude/logs`) with `mkdir(parents=True, exist_ok=True)`.
- No `monkeypatch` usage at all — environment isolation is done via `env=` dict.

### Test naming and helpers

- 5 tests, all named `test_<behavior_description>` (snake_case, descriptive).
- Module-level constant `HOOK = Path(__file__).resolve().parents[2] / "src" / "superclaude" / "hooks" / "scripts" / "auggie-flag-clear.sh"` (line 16-23) — this is the canonical "find the repo root" pattern. `parents[2]` because the file is at `tests/hooks/test_auggie_first.py` → parent[0]=hooks/, parent[1]=tests/, parent[2]=repo root.
- One private helper `_run_hook(payload, fake_home)` and one private helper `_sticky_path(home, session_id)` for path construction (line 42-43).

---

## Section 2: Existing `install_hooks` test pattern (`tests/cli/test_install_hooks.py`)

**File:** `/config/workspace/IronClaude/tests/cli/test_install_hooks.py` (466 lines, 13 tests)

### Direct Python API calls (no subprocess)

Verbatim from `test_install_hooks.py:29-34`:

```python
from superclaude.cli.install_hooks import (
    _atomic_write_json,
    _backup_path,
    install_hooks,
    validate_session_id,
)
```

Tests directly call `install_hooks(target_path=target_settings, force=False)` and assert on the `(ok, msg)` tuple — much faster than subprocess.

### `tmp_path` fixture composition

The `fake_source_hooks` fixture (lines 41-123) shows the canonical pattern for staging a fake project tree:
- Build `tmp_path / "pkg" / "hooks" / "scripts"` directory hierarchy.
- Write a JSON `hooks.json` with `(hooks_pkg / "hooks.json").write_text(json.dumps(hooks_json, indent=2))`.
- Write shell scripts with one-line `(scripts_pkg / name).write_text("#!/usr/bin/env bash\nexit 0\n")`.
- Use `monkeypatch.setattr("superclaude.cli.install_hooks._get_hooks_source", lambda: hooks_pkg / "hooks.json")` to redirect module-level functions (lines 106-122).

The `target_settings` fixture (lines 127-131) returns a `tmp_path / "home" / ".claude" / "settings.json"` path.

### Real-file regression guard

Lines 438-465 (`test_real_hooks_json_gates_write_in_pre_tool_use`) demonstrate the regression-guard pattern that the new V7 test will mirror:

```python
real_hooks = (
    Path(__file__).resolve().parents[2]
    / "src" / "superclaude" / "hooks" / "hooks.json"
)
assert real_hooks.exists(), real_hooks
data = json.loads(real_hooks.read_text())
pre_tool = data["hooks"]["PreToolUse"]
...
matcher_tools = set(fresh_registrations[0]["matcher"].split("|"))
assert "Edit" in matcher_tools
assert "Write" in matcher_tools
```

This is the parents[2] pattern again — no monkey-patch, just direct read of the real `src/superclaude/hooks/hooks.json` to assert content. **V7 in the new file should follow this same shape but for the post-fix matcher.**

### Teardown / restore patterns

`test_case_6_permission_denied` (line 317) uses an explicit `try/finally` to restore directory permissions:

```python
os.chmod(parent, 0o555)
try:
    ok, msg = install_hooks(...)
    ...
finally:
    os.chmod(parent, 0o755)
```

This is the pattern the new file should use for mutation/restore of real repo files.

---

## Section 3: Invoking `make` from pytest

### Existing usage

`grep -rn '"make"' tests/ 2>/dev/null` and `grep -rn 'subprocess.*make' tests/ 2>/dev/null` BOTH return zero matches. **No existing test invokes `make` via subprocess.**

The new `test_verify_sync_hooks.py` file will pioneer this pattern in the project.

### Locating the project root

The repo-root discovery pattern is well-established at `tests/hooks/test_auggie_first.py:16-23`:

```python
HOOK = (
    Path(__file__).resolve().parents[2]
    / "src" / "superclaude" / "hooks" / "scripts" / "auggie-flag-clear.sh"
)
```

For a test at `tests/cli/test_verify_sync_hooks.py`:
- `Path(__file__).resolve()` → `/config/workspace/IronClaude/tests/cli/test_verify_sync_hooks.py`
- `.parents[0]` → `tests/cli/`
- `.parents[1]` → `tests/`
- `.parents[2]` → `/config/workspace/IronClaude/` (repo root). ✅

The skeleton will use `REPO_ROOT = Path(__file__).resolve().parents[2]` and pass `cwd=REPO_ROOT` to the `subprocess.run(["make", "verify-sync"], ...)` call.

### Proposed make invocation

```python
def _run_verify_sync() -> subprocess.CompletedProcess:
    return subprocess.run(
        ["make", "verify-sync"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,         # str output (we grep stdout for sentinel strings)
        timeout=120,       # verify-sync includes `uv run` cold-boot (~500 ms)
    )
```

Note the deviation from `test_auggie_first.py`: `text=True` is appropriate here because we are searching stdout for sentinel substrings like `"❌ MISSING from _FRESHNESS_SCRIPTS"` (release-spec §9 V3).

---

## Section 4: tmp_path strategy for V3-V7

### `_FRESHNESS_SCRIPTS` definition (V3, V4)

Verbatim from `src/superclaude/cli/install_hooks.py:43-55`:

```python
_FRESHNESS_SCRIPTS = [
    "freshness-session-start.sh",
    "freshness-user-prompt.sh",
    "freshness-pre-edit.sh",
    "freshness-post-read.sh",
    "freshness-file-changed.sh",
    "freshness-subagent-start.sh",
    "freshness-subagent-stop.sh",
    "auggie-flag-clear.sh",
]
```

This is a **module-level Python list** — a true in-process attribute of `superclaude.cli.install_hooks`.

### Why in-memory monkey-patch is INSUFFICIENT for V3/V4

`hook-sync-coverage-spec.md:94-96` (release-spec referenced §4.2 of the coverage spec):

```bash
echo "=== Installer Registration ==="; \
...
registered=$$(uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print('\n'.join(sorted(_FRESHNESS_SCRIPTS)))" 2>/dev/null); \
```

The verify-sync Makefile target shells out via `uv run python -c "..."`. That is a **fresh Python interpreter** — it re-imports `superclaude.cli.install_hooks` and reads `_FRESHNESS_SCRIPTS` from disk, NOT from the running pytest process's memory.

Therefore:
- **Option A — `monkeypatch.setattr(module, "_FRESHNESS_SCRIPTS", new_list)`**: WILL NOT WORK. The mutation is only visible inside the pytest process. The `make verify-sync` subprocess starts a fresh `uv run python -c` interpreter that does its own import from disk and never sees the in-memory mutation.
- **Option B — edit `install_hooks.py` in place with try/finally restore**: WORKS. The fresh subprocess re-reads the file from disk and sees the mutation.

**Recommendation:** Option B. Implement a context-manager helper that mutates the on-disk file inside the editable install (`src/superclaude/cli/install_hooks.py`) and restores it in `finally`.

### V5/V6/V7 — `hooks.json` and `auggie-flag-clear.sh` mutation

These are bytes-on-disk files (JSON and Bash), so all three options below are viable in principle:

- **Option A: mutate real files in repo with try/finally restore.** Simple. Works because `make verify-sync` reads the real files at `src/superclaude/hooks/hooks.json` and `src/superclaude/hooks/scripts/auggie-flag-clear.sh`.
- **Option B: copy entire repo to tmp_path and run make there.** Has a subtle correctness flaw: `make verify-sync` shells out to `uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; ..."`. Because the project is installed as an editable install (per `Makefile:` and CI `uv pip install --system -e ".[dev]"`), `import superclaude.cli.install_hooks` resolves to the OUTER repo's `src/superclaude/cli/install_hooks.py`, NOT the tmp_path copy. So `_FRESHNESS_SCRIPTS` would be read from the outer repo while `hooks.json` would be read from the tmp_path. **Cross-source mismatch — invalidates V3/V4 in tmp_path mode.**
- **Option C: switch on the file type.** Use tmp_path for V5/V6/V7 (hooks.json + auggie-flag-clear.sh) and in-place mutation for V3/V4. Splits the test harness in two — extra complexity for no real benefit.

### Final recommendation

**Mutate real files in repo for ALL scenarios V2-V7** using context-manager helpers, always restoring in `finally`:

```python
@contextmanager
def _temporarily_replace_file(path: Path, new_content: str):
    original = path.read_text()
    path.write_text(new_content)
    try:
        yield
    finally:
        path.write_text(original)


@contextmanager
def _temporarily_mutate_freshness_list(remove: list[str] = (), add: list[str] = ()):
    """Rewrite _FRESHNESS_SCRIPTS in src/superclaude/cli/install_hooks.py."""
    install_hooks_py = REPO_ROOT / "src" / "superclaude" / "cli" / "install_hooks.py"
    original = install_hooks_py.read_text()
    # parse current list, apply remove/add, regenerate the literal block, write back
    new_text = _rewrite_freshness_scripts(original, remove=remove, add=add)
    install_hooks_py.write_text(new_text)
    try:
        yield
    finally:
        install_hooks_py.write_text(original)
```

Rationale:
- All scenarios see a consistent worldview (one repo, one editable install).
- The `make sync-dev` invariant is preserved on test failure because `finally` always restores the original bytes.
- Mirrors the proven `os.chmod` + `try/finally` pattern at `tests/cli/test_install_hooks.py:317-334`.
- The V2 case (`rm .claude/hooks/auggie-flag-clear.sh`) is handled the same way: `_temporarily_replace_file` works fine on missing-file scenarios via a sibling `_temporarily_remove_file` context manager that deletes-then-restores.

**Caveat:** if a test process is hard-killed mid-run (SIGKILL), the original bytes are lost. Recovery: `make sync-dev` re-derives `.claude/` from `src/`, but `src/superclaude/cli/install_hooks.py` itself has no upstream. Mitigation: a hidden `*.bak` sidecar file written before mutation and reaped in `finally`. Acceptable since SIGKILL is rare in pytest.

---

## Section 5: pyproject.toml and conftest.py

### pyproject.toml

`/config/workspace/IronClaude/pyproject.toml:99-120`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "hallucination: Hallucination detection tests",
    "performance: Performance benchmark tests",
    "slow: Slow tests (performance benchmarks, large datasets)",
    "confidence_check: Pre-execution confidence assessment",
    "self_check: Post-implementation validation",
    "reflexion: Error learning and prevention",
    "complexity: Task complexity level (simple, medium, complex)",
    "diagnostic: Sprint diagnostic framework tests",
    ...
]
```

Important: `--strict-markers` is on. Any `@pytest.mark.*` used in the new file must be in the registered list. The new tests should not need custom markers (they're plain integration-style tests); if needed, `@pytest.mark.integration` is already registered.

The pytest plugin auto-discovery is configured at `pyproject.toml:67-68`:

```toml
[project.entry-points.pytest11]
superclaude = "superclaude.pytest_plugin"
```

But none of the auto-loaded plugin's fixtures (`confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`, `pm_context`) are relevant to verify-sync testing.

### conftest.py files

Seven conftest files exist:
- `/config/workspace/IronClaude/tests/conftest.py` — root conftest
- `/config/workspace/IronClaude/tests/roadmap/conftest.py`
- `/config/workspace/IronClaude/tests/sc-roadmap/conftest.py`
- `/config/workspace/IronClaude/tests/sprint/diagnostic/conftest.py`
- `/config/workspace/IronClaude/tests/v3.3/conftest.py`
- `/config/workspace/IronClaude/tests/pipeline/conftest.py`
- `/config/workspace/IronClaude/tests/audit-trail/conftest.py`

Root `tests/conftest.py:11-13` only declares `collect_ignore = ["sprint/test_property_based.py"]` and PM-agent fixtures (`sample_context`, `low_confidence_context`, `sample_implementation`, `failing_implementation`, `temp_memory_dir`). **None of these affect the new test file.**

There is NO `tests/cli/conftest.py` — the new test file lives in a directory without a local conftest. Built-in `tmp_path` is sufficient.

---

## Section 6: CI environment

### Test workflow (`.github/workflows/test.yml`)

Verbatim from `.github/workflows/test.yml:36-48`:

```yaml
- name: Install dependencies
  run: |
    uv pip install --system -e ".[dev]"
    uv pip list --system

- name: Verify package installation
  run: |
    python -c "import superclaude; print(f'SuperClaude {superclaude.__version__} installed')"
    python -c "import pytest_cov; print('pytest-cov is installed')"

- name: Run tests
  run: |
    pytest -v --tb=short --color=yes
```

### Tool availability matrix

| Tool | Available in CI? | Evidence |
|---|---|---|
| `uv` | ✅ Yes | `test.yml:28-31` installs from `https://astral.sh/uv/install.sh` |
| `make` | ✅ Yes (default on `ubuntu-latest`) | Implicit — `ubuntu-latest` images ship with `build-essential` |
| `python` | ✅ Yes | `actions/setup-python@v5` matrix `["3.10","3.11","3.12"]` |
| `bash` | ✅ Yes | `ubuntu-latest` default shell |
| `jq` | ⚠ Likely yes but UNVERIFIED | No explicit `apt-get install jq` step in any workflow. `grep -rn jq Makefile .github/workflows/` finds zero hits. The release-spec §11 R1 claim that "jq is already a project prerequisite" rests on hook-script usage at runtime; CI may need to install it. `ubuntu-latest` GitHub-hosted runners DO ship jq by default (per GitHub Actions runner-images repo) but this is implicit, not pinned. |
| `diff` | ✅ Yes | `Makefile:166` uses `diff -rq` already; CI passes today. |

### CI risk for the new test

The new test will invoke `make verify-sync` via subprocess. `make verify-sync` itself uses `diff`, `uv run python -c`, and (per the new spec's Part 3 cross-consistency section) `jq`. The Part 3 §5.1 cross-consistency block at `release-spec.md:181` is the only consumer of `jq`. If CI runners ever stop bundling jq, V5/V6/V7 will fail with an unhelpful "command not found".

**Mitigation:** the new test should sanity-check `jq` presence at module collection time via:

```python
import shutil
_HAS_JQ = shutil.which("jq") is not None
pytestmark = pytest.mark.skipif(
    not _HAS_JQ,
    reason="jq required by =Hooks Cross-Consistency= section in Makefile verify-sync",
)
```

**IMPORTANT — module-level scope required:** the new `=== Hooks Cross-Consistency ===`
section in `make verify-sync` invokes `jq` on EVERY invocation, including the
V1 clean-tree case. Therefore the `_HAS_JQ` skipif MUST apply at MODULE scope,
not just V5/V6/V7. If jq is missing, the entire `make verify-sync` target
would fail loudly in its cross-consistency block (per release-spec §5.1) —
that failure would propagate to V1's `returncode == 0` assertion too. Apply
the skip module-wide; do not scope it per-test to V5/V6/V7.

---

## Section 7: Proposed `test_verify_sync_hooks.py` skeleton

Estimated LOC: **~120-140** (including helpers and module preamble).

```python
"""verify-sync hook coverage tests (V1-V7 per release-spec §9).

WARNING: these tests mutate real files in src/superclaude/hooks/ and
src/superclaude/cli/install_hooks.py via try/finally context managers.
Do NOT run with pytest-xdist — concurrent mutation will race and
corrupt files. Run with pytest's default in-process serial mode.

Covers release-spec §9 scenarios V1-V7 for the hook-sync-and-matcher-fix
release. Each scenario mutates real repo files via context-manager helpers
that always restore in `finally`, ensuring a hard-killed test cannot leave
the developer's tree dirty (modulo SIGKILL — see §4 of the research notes).

Pattern is borrowed from:
- tests/hooks/test_auggie_first.py (subprocess-based hook tests)
- tests/cli/test_install_hooks.py (real-file regression guard at line 438)
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_JSON = REPO_ROOT / "src" / "superclaude" / "hooks" / "hooks.json"
AUGGIE_FLAG_CLEAR = (
    REPO_ROOT / "src" / "superclaude" / "hooks" / "scripts" / "auggie-flag-clear.sh"
)
INSTALL_HOOKS_PY = REPO_ROOT / "src" / "superclaude" / "cli" / "install_hooks.py"
CLAUDE_HOOKS_DIR = REPO_ROOT / ".claude" / "hooks"

_HAS_JQ = shutil.which("jq") is not None
_HAS_MAKE = shutil.which("make") is not None

# Module-level skip: the new `=== Hooks Cross-Consistency ===` section in
# Makefile verify-sync invokes `jq` on EVERY run including the V1 clean-tree
# case. Therefore jq is required for ALL tests in this module, not just
# V5/V6/V7. Per-test skipif on jq has been removed (made redundant by this).
pytestmark = [
    pytest.mark.skipif(
        not _HAS_MAKE, reason="make required for verify-sync tests"
    ),
    pytest.mark.skipif(
        not _HAS_JQ,
        reason="jq required by =Hooks Cross-Consistency= section in Makefile verify-sync",
    ),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_verify_sync() -> subprocess.CompletedProcess:
    """Invoke `make verify-sync` at the repo root. Returns CompletedProcess."""
    return subprocess.run(
        ["make", "verify-sync"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )


@contextmanager
def _temporarily_replace_file(path: Path, new_content: str):
    """Overwrite `path` with `new_content`, restore in finally."""
    original = path.read_text()
    path.write_text(new_content)
    try:
        yield
    finally:
        path.write_text(original)


@contextmanager
def _temporarily_remove_file(path: Path):
    """Move `path` aside, restore in finally."""
    backup = path.with_suffix(path.suffix + ".pytestbak")
    path.rename(backup)
    try:
        yield
    finally:
        backup.rename(path)


@contextmanager
def _temporarily_mutate_freshness_list(*, remove: tuple[str, ...] = (), add: tuple[str, ...] = ()):
    """Rewrite the _FRESHNESS_SCRIPTS literal in install_hooks.py, restore in finally.

    # Fragility note: regex assumes no `.sh` literals appear inside inline
    # comments within the _FRESHNESS_SCRIPTS list. Today (install_hooks.py:43-55)
    # only `freshness-file-changed.sh` has an inline comment and the comment
    # does not contain `.sh` literals. If a future entry adds a `.sh` in its
    # comment, switch to AST parsing (ast.parse + module-level Assign extraction).
    """
    original = INSTALL_HOOKS_PY.read_text()
    # Single-source-of-truth regex: the literal list spans install_hooks.py:43-55
    pattern = re.compile(r"_FRESHNESS_SCRIPTS = \[.*?\]", re.DOTALL)
    match = pattern.search(original)
    assert match, "Could not locate _FRESHNESS_SCRIPTS literal in install_hooks.py"
    # Parse current entries
    current = re.findall(r'"([^"]+\.sh)"', match.group())
    new_list = [s for s in current if s not in remove] + list(add)
    new_literal = "_FRESHNESS_SCRIPTS = [\n" + "".join(
        f'    "{s}",\n' for s in new_list
    ) + "]"
    INSTALL_HOOKS_PY.write_text(pattern.sub(new_literal, original, count=1))
    try:
        yield
    finally:
        INSTALL_HOOKS_PY.write_text(original)


# ---------------------------------------------------------------------------
# Scenarios V1-V7
# ---------------------------------------------------------------------------

def test_V1_clean_tree_exits_zero():
    """Clean tree: verify-sync exits 0, stdout shows `=== Hooks ===` block."""
    result = _run_verify_sync()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "=== Hooks ===" in result.stdout
    assert "✅" in result.stdout  # at least one passing entry


def test_V2_missing_claude_hook_detected():
    """Delete .claude/hooks/auggie-flag-clear.sh → MISSING error, exit != 0."""
    claude_hook = CLAUDE_HOOKS_DIR / "auggie-flag-clear.sh"
    with _temporarily_remove_file(claude_hook):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "MISSING in .claude/hooks/: auggie-flag-clear.sh" in result.stdout


def test_V3_missing_from_freshness_scripts():
    """Remove one entry from _FRESHNESS_SCRIPTS → MISSING-from-installer error."""
    with _temporarily_mutate_freshness_list(remove=("auggie-flag-clear.sh",)):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "MISSING from _FRESHNESS_SCRIPTS" in result.stdout


def test_V4_stale_in_freshness_scripts():
    """Add a fake entry to _FRESHNESS_SCRIPTS → STALE-installer error."""
    with _temporarily_mutate_freshness_list(add=("ghost-hook.sh",)):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "STALE in _FRESHNESS_SCRIPTS" in result.stdout


def test_V5_matcher_drift_detected():
    """hooks.json matcher loses one prefix; case body unchanged → DRIFT."""
    # Mutate the matcher at hooks.json:60 (PostToolUse → auggie-flag-clear)
    new_data = json.loads(HOOKS_JSON.read_text())
    for reg in new_data["hooks"]["PostToolUse"]:
        for h in reg.get("hooks", []):
            if "auggie-flag-clear" in h.get("command", ""):
                reg["matcher"] = reg["matcher"].replace("|mcp__auggie-mcp__.*", "")
    # JSON round-trip is acceptable because verify-sync parses the
    # matcher value (via jq), not the full file bytes.
    with _temporarily_replace_file(HOOKS_JSON, json.dumps(new_data, indent=2)):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "DRIFT" in result.stdout
    assert "auggie-flag-clear.sh" in result.stdout


def test_V6_case_body_drift_detected():
    """auggie-flag-clear.sh case body loses one prefix; matcher unchanged → DRIFT."""
    original = AUGGIE_FLAG_CLEAR.read_text()
    mutated = original.replace("|mcp__auggie-mcp__*", "")
    with _temporarily_replace_file(AUGGIE_FLAG_CLEAR, mutated):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "DRIFT" in result.stdout


def test_V7_regression_to_master():
    """Both files reverted to current-master matcher gap → DRIFT, root cause = matcher gap."""
    # Mirror release-spec §12: master HEAD 516bb46 has matcher = "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"
    # i.e. WITHOUT mcp__auggie-mcp__* — that's the gap.
    new_data = json.loads(HOOKS_JSON.read_text())
    for reg in new_data["hooks"]["PostToolUse"]:
        for h in reg.get("hooks", []):
            if "auggie-flag-clear" in h.get("command", ""):
                reg["matcher"] = "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"
    bash_original = AUGGIE_FLAG_CLEAR.read_text()
    bash_mutated = bash_original.replace(
        "|mcp__auggie-mcp__*", ""
    )  # also strip from case body to match release-spec V7
    # JSON round-trip is acceptable because verify-sync parses the
    # matcher value (via jq), not the full file bytes.
    with _temporarily_replace_file(HOOKS_JSON, json.dumps(new_data, indent=2)):
        with _temporarily_replace_file(AUGGIE_FLAG_CLEAR, bash_mutated):
            result = _run_verify_sync()
    assert result.returncode != 0
    assert "DRIFT" in result.stdout
```

### Notes on the skeleton

- **No pytest fixtures** are required from the new file — built-in `tmp_path` is unused because all mutations are on the real repo via context managers.
- **Module-level constants** (`REPO_ROOT`, `HOOKS_JSON`, `AUGGIE_FLAG_CLEAR`, `INSTALL_HOOKS_PY`, `CLAUDE_HOOKS_DIR`) are computed once.
- **`pytestmark`** is a LIST of two module-level skipifs (both `_HAS_MAKE` and `_HAS_JQ`). If either binary is missing every test in the module is skipped with a clear reason instead of erroring. Note that jq is module-wide (NOT per-test on V5/V6/V7) because the new `=== Hooks Cross-Consistency ===` Makefile section invokes jq on EVERY verify-sync run including the V1 clean-tree case.
- The `_temporarily_mutate_freshness_list` helper uses a regex against `re.DOTALL`-flagged matching of `_FRESHNESS_SCRIPTS = \[.*?\]`. This is the same pattern the spec's `=== Installer Registration ===` block at `hook-sync-coverage-spec.md:94-112` uses semantically, just expressed in Python instead of shell.
- The skeleton does NOT call `make sync-dev` after restoration because the context managers restore the exact original bytes; no drift is introduced. (If a test failed catastrophically between mutate and restore, the user can re-run `make sync-dev` or `git checkout`.)

---

## Summary

**Chosen tmp_path strategy:** mutate real files in the repo via context-manager helpers (`_temporarily_replace_file`, `_temporarily_remove_file`, `_temporarily_mutate_freshness_list`) with `try/finally` restoration. This is the only viable approach because `make verify-sync` shells out to `uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS"` (per `hook-sync-coverage-spec.md:94-96`), and the editable install resolves to `src/superclaude/cli/install_hooks.py` in the OUTER repo — a tmp_path copy of the repo would NOT be picked up by the subprocess import. The restore-in-finally pattern mirrors the proven `os.chmod` teardown at `tests/cli/test_install_hooks.py:317-334`.

**Helpers the new test file needs:**
- `REPO_ROOT = Path(__file__).resolve().parents[2]` (module constant)
- `_run_verify_sync()` — wraps `subprocess.run(["make","verify-sync"], cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)`
- `_temporarily_replace_file(path, new_content)` — context manager
- `_temporarily_remove_file(path)` — context manager (uses `Path.rename` for atomic move-aside)
- `_temporarily_mutate_freshness_list(*, remove=(), add=())` — regex-based rewriter for the `_FRESHNESS_SCRIPTS = [...]` literal at `install_hooks.py:43-55`
- Module-level `_HAS_JQ` and `_HAS_MAKE` guards via `shutil.which`

**CI risks:**
- **jq not pinned in any workflow** — `grep -rn jq .github/workflows/ Makefile` returns zero matches. `ubuntu-latest` GitHub runners do bundle jq by default, but the release-spec §11 R1 claim that "jq is already a project prerequisite" is true only at hook runtime, not pinned by CI. Mitigation: MODULE-LEVEL `pytestmark = pytest.mark.skipif(not shutil.which("jq"), ...)` (NOT per-test on V5/V6/V7) keeps CI green if the runner image ever drops jq — required because the new `=== Hooks Cross-Consistency ===` Makefile section invokes jq on EVERY verify-sync run including the V1 clean-tree case.
- **`uv run` cold-boot overhead** (~200-500 ms per `make verify-sync` invocation per `hook-sync-coverage-spec.md:165`) means the 7 tests add ~2-4 s of wall-clock to the CI suite. Acceptable.
- **SIGKILL during a mutation window** would leave `src/superclaude/cli/install_hooks.py` or `src/superclaude/hooks/hooks.json` in a mutated state. The dev's recovery path is `git checkout src/superclaude/cli/install_hooks.py src/superclaude/hooks/`. Not catastrophic but worth a comment in the test docstring.
- **No `tests/cli/conftest.py` exists** — the new file at `tests/cli/test_verify_sync_hooks.py` will only inherit fixtures from `tests/conftest.py` (PM-agent fixtures, unused here) and the auto-loaded `superclaude` pytest plugin. Built-in `tmp_path` is enough; no new conftest needed.
