# Research Track 2: Test & Verification (Test Fixtures)

**Task**: TASK-RF-track-2-20260518-231708 (FU-002: reflexion writer test pollution)
**Scope**: `tests/conftest.py`, `tests/unit/test_reflexion.py`, `tests/integration/test_pytest_plugin.py`, `src/superclaude/pytest_plugin.py`
**Status**: Complete
**Date**: 2026-05-18

---

## 1. Existing `reflexion_pattern` fixture

The `reflexion_pattern` fixture is **not** defined in `tests/conftest.py`. It lives in the SuperClaude pytest plugin module and is auto-loaded via the `pytest11` entry point declared in `pyproject.toml`.

**Definition** — `src/superclaude/pytest_plugin.py:71-81`:

```python
@pytest.fixture
def reflexion_pattern():
    """
    Fixture for reflexion error learning pattern

    Usage:
        def test_example(reflexion_pattern):
            reflexion_pattern.record_error(...)
            solution = reflexion_pattern.get_solution(error_signature)
    """
    return ReflexionPattern()
```

**Key facts**:
- **Scope**: default `function` (no `scope=` kwarg → per-test instance).
- **Return**: a bare `ReflexionPattern()` constructed with **no arguments**.
- **Side effect**: `ReflexionPattern.__init__` (`src/superclaude/pm_agent/reflexion.py:56-74`) defaults `memory_dir = Path.cwd() / "docs" / "memory"` and **creates `mistakes_dir = memory_dir.parent / "mistakes"`** via `mkdir(parents=True, exist_ok=True)`. Running tests from the repo root therefore creates `docs/memory/` and `docs/mistakes/` inside the repo working tree.

**Adjacent (related) fixtures in `tests/conftest.py`** — these already use `tmp_path` and serve as the template for the fix:
- `temp_memory_dir(tmp_path)` — `tests/conftest.py:101-121` — builds `tmp_path/docs/memory/` and seeds the four memory files (including `reflexion.jsonl`).
- `pm_context(tmp_path)` — `src/superclaude/pytest_plugin.py:105-133` — builds `tmp_path/docs/memory/` and seeds three memory files (no `reflexion.jsonl`).

The `reflexion_pattern` fixture is the **only** plugin fixture that touches reflexion state and the **only** one that does **not** route through `tmp_path`. This is the root cause of test pollution.

**Hook also creates an unscoped ReflexionPattern** — `src/superclaude/pytest_plugin.py:160-184`:

```python
def pytest_runtest_makereport(item, call):
    if call.when == "call":
        marker = item.get_closest_marker("reflexion")
        if marker and call.excinfo is not None:
            reflexion = ReflexionPattern()   # <-- also no memory_dir override
            ...
            reflexion.record_error(error_info)
```

This hook bypasses the fixture entirely and **also** writes to repo-root `docs/memory/` if any `@pytest.mark.reflexion`-marked test fails. Any fix must cover both code paths.

---

## 2. Reflexion test files inventory — `tests/unit/test_reflexion.py`

Nine tests total. All instances that invoke `record_error` are listed; those flagged "POLLUTES" cause writes to the live repo today.

| # | Test (line) | Purpose | record_error? | Pollutes repo? |
|---|---|---|---|---|
| 1 | `test_initialization` (15) | Asserts `ReflexionPattern()` has `record_error`/`get_solution` attrs | no | `__init__` `mkdir` only |
| 2 | `test_record_error_basic` (23) | Records error with no `solution`/`root_cause` | yes (35) | `solutions_learned.jsonl` only (no mistake doc — `_create_mistake_doc` is gated at `reflexion.py:127` on `root_cause`/`solution`) |
| 3 | `test_record_error_with_solution` (37) | Records `test_database_connection` error **with** `solution` field | yes (48) | **YES** — writes both `solutions_learned.jsonl` AND `docs/mistakes/test_database_connection-YYYY-MM-DD.md` |
| 4 | `test_get_solution_for_known_error` (50) | Records `ImportError` with solution, then queries | yes (61) | **YES** — writes `solutions_learned.jsonl` + `docs/mistakes/test_get_solution_for_known_error-...md` (uses default `test_name` from `error_info`? — actually `test_name` is absent, so falls back to `"unknown"` at `reflexion.py:256`, producing `docs/mistakes/unknown-YYYY-MM-DD.md`) |
| 5 | `test_error_pattern_matching` (71) | Records two `TypeError` entries with solutions | yes (90) | **YES** — `solutions_learned.jsonl` + `docs/mistakes/unknown-...md` (overwritten twice) |
| 6 | `test_reflexion_memory_persistence` (98) | **Already uses `temp_memory_dir` fixture** — clean | yes (109) | **No** — passes `memory_dir=temp_memory_dir` |
| 7 | `test_error_learning_across_sessions` (111) | Records `FileNotFoundError` with solution | yes (128) | **YES** — `solutions_learned.jsonl` + `docs/mistakes/unknown-...md` |
| 8 | `test_reflexion_marker_integration` (139) | Uses `reflexion_pattern` fixture, records error (no solution) | yes (156) | `solutions_learned.jsonl` only |
| 9 | `test_reflexion_with_real_exception` (159) | Catches `ZeroDivisionError`, records with solution | yes (180) | **YES** — `solutions_learned.jsonl` + `docs/mistakes/test_reflexion_with_real_exception-...md` |

**Live pollution evidence** (re-verified via `Bash` 2026-05-18 gap-fill pass):
- `docs/mistakes/` contains **84 files** — predominantly `test_database_connection-<date>.md`, one per day this test has run.
- `docs/memory/solutions_learned.jsonl` has **588 lines** (re-measured; previously cited 292 — drift between research-authoring time and gap-fill).
- **NOTE for regression-test design**: these are *current snapshot* values for the baseline cleanse decision in Phase 1 (see Track 01 OQ-3). The regression test itself MUST use a **dynamic pre-fix snapshot** captured at fixture-start (via `stat`/`glob` counts inside a session-scoped fixture), NOT hard-coded values like "84" or "588" — those will drift the moment any developer runs the test suite locally.

**Root cause for the 7 bare-constructor tests** (gap-fill re-verified count, 2026-05-18 via `grep -n "ReflexionPattern()" tests/unit/test_reflexion.py`): **7 of 9 tests** call `ReflexionPattern()` directly (L17, L25, L39, L52, L73, L118, L165). Only L100 uses `memory_dir=temp_memory_dir`, and L139 consumes the `reflexion_pattern` fixture. The 7 bare-constructor tests are the ones that pollute when no env-var override is in place; they write into `Path.cwd() / "docs" / "memory"` which is the repo working tree when `uv run pytest` is invoked from repo root.

---

## 3. Integration tests touching reflexion — `tests/integration/test_pytest_plugin.py`

Two tests reference the reflexion fixture; **neither writes**:

- `test_reflexion_pattern_fixture_available(self, reflexion_pattern)` — line 25-29 — only `hasattr` checks; no `record_error` call.
- `test_all_fixtures_work_together(..., reflexion_pattern, ...)` — line 45-90 — comment at line 89 says "If there were errors, reflexion would record them (no errors in this happy path test)"; **no call** to `record_error`.

**But**: both tests still instantiate `ReflexionPattern()` via the fixture, which triggers `__init__` → `mkdir(docs/memory)` and `mkdir(docs/mistakes)` in repo cwd. This creates the directories but no files. Once the fix is applied via the fixture, this side effect is also redirected to `tmp_path`.

---

## 4. Exact monkeypatching needed — Recommended fix

### Recommendation: **Option C (Both)** — defense-in-depth, scoped per-test

The fix has two seams that **must both** be covered, because the plugin has two production paths instantiating `ReflexionPattern()`:

1. **Fixture path** (`pytest_plugin.py:81`) — tests that take `reflexion_pattern`.
2. **Bare constructor path** — tests in `test_reflexion.py` (tests #2-#5, #7, #9 above) that call `ReflexionPattern()` directly inside the test body, bypassing the fixture.

Option A alone fixes only path (1). Option B alone (env var) is fragile because `ReflexionPattern.__init__` (`reflexion.py:64-66`) currently has **no env-var resolver** — adding one is a track-1 production code change. Option C composes the fixture upgrade with an autouse monkeypatch that catches direct `ReflexionPattern()` constructions.

### Concrete patch

**Track-1 prerequisite** (`src/superclaude/pm_agent/reflexion.py`) — add env-var resolver so plugin's `pytest_runtest_makereport` hook also redirects:

```python
import os
# ...
def __init__(self, memory_dir: Optional[Path] = None):
    if memory_dir is None:
        env_override = os.environ.get("REFLEXION_OUTPUT_DIR")
        if env_override:
            memory_dir = Path(env_override)
        else:
            memory_dir = Path.cwd() / "docs" / "memory"
    # ... rest unchanged
```

**Track-2 fixture upgrade** (`src/superclaude/pytest_plugin.py:71-81`):

```python
@pytest.fixture
def reflexion_pattern(tmp_path, monkeypatch):
    """
    Fixture for reflexion error learning pattern.

    Writes are redirected to tmp_path/docs/memory/ to prevent
    repo pollution. The env-var override also catches any
    ReflexionPattern() constructed without the fixture (e.g. the
    pytest_runtest_makereport hook and tests that instantiate
    ReflexionPattern() directly in the test body).
    """
    memory_dir = tmp_path / "docs" / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("REFLEXION_OUTPUT_DIR", str(memory_dir))
    return ReflexionPattern(memory_dir=memory_dir)
```

**Autouse safety net** (new fixture in `tests/conftest.py` — covers tests that don't take the `reflexion_pattern` fixture but call `ReflexionPattern()` directly):

```python
@pytest.fixture(autouse=True)
def _redirect_reflexion_writes(tmp_path, monkeypatch):
    """
    Defense-in-depth: redirect any bare ReflexionPattern() construction
    in test code or in the pytest_runtest_makereport hook to tmp_path,
    so no test can pollute docs/memory/ or docs/mistakes/.
    """
    monkeypatch.setenv(
        "REFLEXION_OUTPUT_DIR",
        str(tmp_path / "reflexion_memory"),
    )
```

### Rationale

- **Why not Option A alone**: 7 of 9 tests in `test_reflexion.py` call `ReflexionPattern()` directly, not the fixture (re-verified 2026-05-18: bare `ReflexionPattern()` at L17, L25, L39, L52, L73, L118, L165). Fixing only the fixture leaves the bulk of pollution untouched.
- **Why not Option B alone**: Requires the prerequisite production change anyway; without the fixture upgrade, the *explicit* `reflexion_pattern` fixture still constructs `ReflexionPattern()` before any `monkeypatch.setenv` in the consuming test runs.
- **Why Option C wins**: The fixture upgrade makes the intent explicit and self-documenting; the autouse env-var monkeypatch is the safety net for everything else, including future tests. Cost is a single `Path.cwd()` resolution + one `setenv` per test — negligible.

---

## 5. Regression test design

Add a session-scoped guard in `tests/conftest.py` (or `tests/unit/test_reflexion.py`) that asserts no pollution leaked. Two complementary forms:

### 5a. Per-test assertion (autouse, fast)

```python
@pytest.fixture(autouse=True)
def _assert_no_repo_reflexion_writes(_redirect_reflexion_writes):
    """
    Run after each test: assert no new files appeared in the live
    docs/mistakes/ or new lines in docs/memory/solutions_learned.jsonl.
    Relies on _redirect_reflexion_writes having shifted writes to tmp_path.
    """
    import subprocess
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[1]  # tests/ → repo
    mistakes = repo_root / "docs" / "mistakes"
    solutions = repo_root / "docs" / "memory" / "solutions_learned.jsonl"

    pre_count = len(list(mistakes.glob("*.md"))) if mistakes.exists() else 0
    pre_size = solutions.stat().st_size if solutions.exists() else 0

    yield

    post_count = len(list(mistakes.glob("*.md"))) if mistakes.exists() else 0
    post_size = solutions.stat().st_size if solutions.exists() else 0

    assert post_count == pre_count, (
        f"Test polluted docs/mistakes/: {post_count - pre_count} new file(s)"
    )
    assert post_size == pre_size, (
        f"Test polluted docs/memory/solutions_learned.jsonl: "
        f"{post_size - pre_size} new bytes"
    )
```

### 5b. Session-end git-status guard (single, definitive)

Add as the **last** test in `tests/unit/test_reflexion.py` (alphabetical ordering or explicit `pytest.mark.order(-1)`):

```python
def test_no_reflexion_pollution_in_repo(tmp_path):
    """
    Regression for FU-002: assert git working tree shows no untracked
    or modified reflexion artifacts after the test session.

    Runs only inside a git repo; skipped otherwise.
    """
    import subprocess

    repo_root = Path(__file__).resolve().parents[2]  # tests/unit/ → repo
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain",
             "docs/mistakes/", "docs/memory/solutions_learned.jsonl"],
            cwd=repo_root, capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("git unavailable or not a git repo")

    polluted = [
        line for line in result.stdout.splitlines()
        if line.strip()
        # Allow pre-existing modifications unrelated to this session.
        # The test was clean as of FU-002 landing; new pollution = test failure.
    ]
    assert not polluted, (
        "Reflexion writes leaked to repo paths:\n"
        + "\n".join(polluted)
        + "\nFix: ensure all ReflexionPattern() instantiations honor "
          "REFLEXION_OUTPUT_DIR or pass memory_dir=tmp_path."
    )
```

**Note on baseline**: At FU-002 landing time, the regression test should run *after* a `git restore docs/memory/solutions_learned.jsonl` and `git clean -fd docs/mistakes/` to clear the existing 84-file backlog + **588 polluted JSONL lines** (re-measured 2026-05-18). Otherwise the baseline is dirty and the assertion needs a `pre_state` snapshot taken in a session-scoped fixture.

**Strongly preferred approach (gap-fill recommendation)**: Use the **dynamic snapshot** form regardless. Do NOT hard-code "84" or "588" anywhere in the regression test. Capture `pre_count = len(list(mistakes.glob("*.md")))` and `pre_size = solutions.stat().st_size` at the start of an autouse session-scoped fixture, yield, then assert `post_count == pre_count` and `post_size == pre_size`. This is robust to (a) different developers having different local pollution levels, (b) the Phase 1 baseline cleanse landing at a different sha than the regression test, and (c) any future deliberate edit to those files.

### 5c. Alternative — file-name fingerprint check

For environments where shelling out to git is undesirable (CI sandbox, hermetic runners):

```python
def test_no_dated_mistake_files_created_today():
    """No test_*-<today>.md files should appear in docs/mistakes/."""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    repo_root = Path(__file__).resolve().parents[2]
    mistakes = repo_root / "docs" / "mistakes"
    if not mistakes.exists():
        return  # nothing to check
    today_files = list(mistakes.glob(f"test_*-{today}.md"))
    today_files += list(mistakes.glob(f"unknown-{today}.md"))
    assert not today_files, (
        f"Reflexion test pollution detected: {[f.name for f in today_files]}"
    )
```

This is the cheapest check and the most diagnostic — it pinpoints exactly the pollution signature observed today (`test_database_connection-2026-05-18.md`, `unknown-2026-05-18.md`).

---

## Summary

- The `reflexion_pattern` fixture is defined in `src/superclaude/pytest_plugin.py:71-81` (function-scoped) and returns a bare `ReflexionPattern()`, which defaults to writing into `Path.cwd() / "docs" / "memory"` and creating `docs/mistakes/` as a sibling. Running pytest from repo root → 84 polluted files in `docs/mistakes/` and **588 polluted lines** in `docs/memory/solutions_learned.jsonl` today (re-measured 2026-05-18).
- Of 9 reflexion tests, **7 instantiate `ReflexionPattern()` directly** (bypassing the fixture; re-verified 2026-05-18 at L17, L25, L39, L52, L73, L118, L165), so fixing only the fixture is insufficient.
- The `pytest_runtest_makereport` hook in `pytest_plugin.py:173` also instantiates `ReflexionPattern()` directly, providing a third pollution vector for any failing `@pytest.mark.reflexion`-marked test.
- **Recommended fix: Option C** — (a) production code reads env-var `REFLEXION_OUTPUT_DIR`, (b) the `reflexion_pattern` fixture upgrades to `tmp_path` + `monkeypatch.setenv`, (c) an autouse fixture in `tests/conftest.py` sets the env var unconditionally as a safety net.
- **Regression**: combine 5a (per-test guard) + 5c (fingerprint check) for hermetic CI; add 5b for local dev with git available. Baseline must be cleaned before introducing 5b; the regression test itself must use a **dynamic** pre-fix snapshot, not hard-coded "84"/"588".

---

## Gaps and Questions (gap-fill 2026-05-18)

Open Questions surfaced during research re-verification — flagged for the builder to resolve in the generated task file, not blocking research handoff:

1. **OQ-1 (resolved): Canonical env-var name** — `REFLEXION_OUTPUT_DIR`. See Track-2 `01-file-inventory.md` top section for the precedent evidence (no `SUPERCLAUDE_*` namespace exists in `src/superclaude/cli/` or `src/superclaude/pm_agent/`). All references in this file were updated in the same gap-fill pass.

2. **OQ-2: Preserve cwd default? (recommended: YES)** — duplicate of Track-2 `01-file-inventory.md` OQ-2; the answer is the same: keep `Path.cwd() / "docs" / "memory"` as fallback so external consumers calling `ReflexionPattern()` with no args and no env var keep working.

3. **OQ-3 (load-bearing): Should Phase 1 include the baseline cleanse?** — recommended: **YES.** The 84 mistake files + 588 jsonl lines are the bulk of the polluted baseline; the regression test in §5 depends on `pre_count == post_count` semantics, which means either (a) cleanse to zero before the test lands, OR (b) capture dirty baseline at fixture-start. Option (a) is cleaner for review history. Option (b) is more developer-friendly for local runs. The recommended Phase 1 ordering is: (1) Apply production env-var resolver, (2) Apply fixture + autouse env-var safety net, (3) Cleanse baseline (`git rm` polluted mistake files + restore `solutions_learned.jsonl` from a clean sha), (4) Add regression test with **dynamic** snapshot — even after cleanse, the test still uses dynamic snapshots so it doesn't break on the first failing run.

4. **OQ-4: Dynamic regression snapshot — confirmed.** No hard-coded "84" or "588" anywhere in the test code; use `stat`/`glob` at fixture-start. See §5 strongly-preferred-approach note.
