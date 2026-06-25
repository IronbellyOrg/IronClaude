# Research 02: Patterns & Test Conventions for the NEW pytest backtest suite

Status: In Progress

Scope: `tests/cli/eval/` (conftest, fixtures, representative tests), `tests/sprint/test_process.py` subprocess mock seam, project-wide xfail/skipif/importorskip conventions, pytest config (markers).

Goal: Document HOW to wire a new pytest suite at `tests/troubleshoot/backtest/` matching project conventions — fixtures, subprocess mock seam, schema-validation test pattern, and xfail/skip-guarding the NEW=CATCH half until the impl branch lands while OLD=MISS + harness wiring run green now.

---

## TL;DR — Headline Conventions (all evidence-cited below)

1. **There is NO `xfail` in this codebase.** `grep -rn 'pytest.mark.xfail' tests/` → 0 hits. The project's established pattern for "the impl branch hasn't landed yet, so this assertion can't pass" is a **forward-dependency probe + self-clearing `pytest.skip(...)`**. This is the convention to mirror for the NEW=CATCH half. Do NOT introduce `xfail`. Evidence: zero-hit grep; canonical exemplars `tests/cli/eval/test_exit_codes.py:92-123`, `tests/cli/eval/test_no_mcp_skip.py:485-505`.
2. **`--strict-markers` is ON** (`pyproject.toml:111`). Any custom marker MUST be registered in `pyproject.toml [tool.pytest.ini_options] markers = [...]` (`pyproject.toml:114-144`) or collection fails. For the backtest suite you almost certainly do NOT need a new marker — use plain test functions + skip-guards. If you want one (e.g. `backtest`), it must be added to that list.
3. **Schema-validation idiom** = `jsonschema.Draft202012Validator` (dep declared `pyproject.toml:39` `jsonschema>=4.0.0`). Load schema, `check_schema`, build validator as a module-scoped fixture, then `validator.validate(payload)` for valid fixtures and `pytest.raises(ValidationError)` + substring assert for invalid. Exemplar: `tests/cli/eval/test_summary_schema.py`.
4. **Subprocess mock seam** = patch the **module-aliased** subprocess symbol at its import site, e.g. `patch("superclaude.cli.sprint.process._subprocess.run")` (`tests/sprint/test_process.py:399`) and `patch("superclaude.cli.pipeline.process.subprocess.Popen")` (`tests/sprint/test_process.py:206`). Patch where it is *used*, not `subprocess.run` globally.
5. **Scratch-root / tmp fixtures**: stock `tmp_path` for arbitrary scratch; a bespoke `allowlisted_output_dir` fixture in a local `conftest.py` for paths that must satisfy an allowlist (`tests/cli/eval/conftest.py:24-39`).
6. **UV only**: `uv run pytest tests/troubleshoot/backtest/`.

---

## 1. pytest config + markers (pyproject.toml)

There is **no `pytest.ini`** (confirmed absent). All config lives in `pyproject.toml [tool.pytest.ini_options]` (`pyproject.toml:104`):

```toml
[tool.pytest.ini_options]                       # pyproject.toml:104
testpaths = ["tests"]                            # :105  -> tests/troubleshoot/... auto-collected
python_files = ["test_*.py"]                     # :106  -> name files test_*.py
python_classes = ["Test*"]                       # :107
python_functions = ["test_*"]                    # :108
addopts = ["-v", "--strict-markers", "--tb=short"]  # :109-113  -- strict markers!
markers = [ "unit: ...", "integration: ...", ... ]  # :114-144
```

Key consequences for the new suite:
- `testpaths = ["tests"]` means a new dir `tests/troubleshoot/backtest/` is auto-discovered with zero config edits. (`pyproject.toml:105`)
- `--strict-markers` (`pyproject.toml:111`) means an unregistered `@pytest.mark.foo` is a **collection error**, not a warning. The full registered list is `pyproject.toml:114-144` (e.g. `unit`, `integration`, `slow`, `recovery`, `nfr_benchmark`, `p0`...). **No `backtest` marker exists.** Recommendation: the backtest suite needs NO custom marker — it is a directory of plain `test_*` functions. If R6/R7 want a `@pytest.mark.backtest` selector, it MUST be appended to `markers = [...]` in the same change, e.g. `"backtest: differential pre-fix replay backtest (E1-E5)"`.
- **No auto-marker for `tests/troubleshoot/`.** Per CLAUDE.md only `/unit/` and `/integration/` paths get auto-markers (via the pytest plugin), and a grep of the actual `markers` list shows no path-keyed auto-marking for other dirs. So backtest tests will be unmarked unless explicitly decorated.

## 2. THE xfail/skip-guard convention (CRITICAL for NEW=CATCH half)

**Finding (load-bearing): `pytest.mark.xfail` appears ZERO times in `tests/`.** Verified: `grep -rn 'pytest.mark.xfail' tests/ | wc -l` → `0`.

The codebase instead uses a **"forward-dependency probe + self-clearing skip"** for exactly the situation the backtest faces: a contract test whose passing side depends on an impl symbol that hasn't landed yet. This is the pattern to mirror for NEW=CATCH.

### 2a. Canonical exemplar — `tests/cli/eval/test_exit_codes.py`

Module docstring states the intent verbatim (the same shape the backtest needs): "While those helpers are absent we ``pytest.skip`` those three tests with a self-clearing diagnostic; the skips evaporate once T04.10 lands" (`tests/cli/eval/test_exit_codes.py:38-40`).

The probe + guard (copy-pasteable shape), `tests/cli/eval/test_exit_codes.py:92-123`:

```python
def _t0410_missing() -> list[str]:
    """Return names of forward-dep symbols not yet defined."""
    from superclaude.cli.eval import commands as _commands_mod
    forward_deps = (
        "_new_run_id", "_run_one_spec", "_compute_run_stats",
        "RUN_CLEAN_EXIT_CODE", "RUN_FAILURES_EXIT_CODE", "RUN_INTERRUPTED_EXIT_CODE",
    )
    return [n for n in forward_deps if not hasattr(_commands_mod, n)]

def _skip_unless_t0410_landed() -> None:
    missing = _t0410_missing()
    if missing:
        pytest.skip(
            f"T04.10 forward dependency not yet landed: {missing!r}. "
            "The exit-code-2 path pinned below runs today; the 0 / 1 / 3 "
            "paths un-skip automatically once T04.10 wires the run-loop "
            "closure helpers."
        )
```

Each NEW-side test body calls `_skip_unless_t0410_landed()` first thing; the OLD-side / contract-today tests do NOT, so they run green now.

### 2b. Variant — `try/except ImportError → return False` + source introspection

`tests/cli/eval/test_no_mcp_skip.py:449-505` shows two more reusable shapes:

- **Graceful import probe** (when the *module* may not import yet):
  ```python
  try:
      from superclaude.cli.eval import commands as _commands_mod
  except ImportError:
      return False
  ```
  (`tests/cli/eval/test_no_mcp_skip.py:449-452`)

- **`hasattr` forward-dep probe inside the test body** then skip (`test_no_mcp_skip.py:493-505`):
  ```python
  forward_deps = ("_run_one_spec", "_new_run_id", "_compute_run_stats",
                  "RUN_CLEAN_EXIT_CODE", "RUN_FAILURES_EXIT_CODE")
  missing = [n for n in forward_deps if not hasattr(_commands_mod, n)]
  if missing:
      pytest.skip(
          f"T04.10 forward dependency not yet landed: {missing!r}. "
          "Per-branch closure assertions above still pin the FR-G4 / "
          "TEST-014 contract; this end-to-end pin un-skips once T04.10 "
          "wires the run helpers."
      )
  ```

- **Source-level introspection** to detect a wiring branch that has no importable symbol (e.g. a NEW gate predicate added inside a closure). `inspect.getsource(fn.callback)` + substring check, returning bool (`test_no_mcp_skip.py:466-471`). This is exactly applicable if the NEW gate is a code branch (not a named symbol) — the backtest's NEW=CATCH guard can probe `inspect.getsource(<gate fn>)` for the gate's trigger token and skip until present.

### 2c. Reason-string convention (mirror this exactly)

Skip reason strings in this repo are **self-documenting + self-clearing**: they (1) name the missing dependency (`{missing!r}`), (2) say what still runs today, (3) state the un-skip trigger ("un-skips automatically once X lands"). See `test_exit_codes.py:118-123` and `test_no_mcp_skip.py:499-505`. For the backtest, the NEW=CATCH reason should read like:
> `"NEW gate <name> not yet implemented (forward-dep {missing!r}); OLD=MISS replay + harness wiring assertions above run today; this CATCH assertion un-skips once the impl branch lands the gate."`

### 2d. `importorskip` (for genuinely-optional 3rd-party deps only)

`pytest.importorskip("click")` (`test_no_mcp_skip.py:486`), `pytest.importorskip("pexpect")` (`test_signal_handling.py:657`), `pytest.importorskip("hypothesis")` (`test_structural_checkers_properties.py:19`, module-level). Use ONLY for optional external packages — NOT for first-party impl symbols (those use the `hasattr` probe above). `jsonschema` is a *declared* dep (`pyproject.toml:39`) so it does NOT need importorskip.

### 2e. `skipif` (environment/capability gates)

Module-level `pytestmark = pytest.mark.skipif(...)` (`test_claude_process_adapter.py:507`, `test_e2e_real_proxy.py:73`) and per-test `@pytest.mark.skipif(cond, reason=...)` (`test_pty_driver.py:349`, `test_spec_parser.py:458` for `not REAL_SPEC_PATH.exists()`). Use `skipif` for *environment* preconditions (tmux present, real spec on disk, OS), NOT for "impl not landed" — that is the inline `pytest.skip` probe.

**Decision matrix for the backtest suite:**
| Situation | Mechanism | Cite |
|---|---|---|
| NEW gate impl symbol/branch not yet landed | inline `pytest.skip` after `hasattr`/`getsource` probe | test_exit_codes.py:115-123 |
| Replay commit / git fixture missing on disk | `@pytest.mark.skipif(not PATH.exists(), reason=...)` | test_spec_parser.py:458 |
| `jsonschema` for report validation | nothing — it's a declared dep | pyproject.toml:39 |
| Selecting backtest tests as a group | register `backtest` marker first (strict!) | pyproject.toml:114-144 |

## 3. conftest.py + fixture conventions

### 3a. Root conftest (`tests/conftest.py`) — auto-applies to the backtest suite

The root conftest is **automatically inherited** by `tests/troubleshoot/backtest/`. Two autouse fixtures will fire on every backtest test (be aware, not necessarily a problem):
- `_pollution_snapshot` (session, autouse) — asserts the test session does not add files to `docs/mistakes/` or grow `docs/memory/solutions_learned.jsonl` (`tests/conftest.py:30-93`). **Implication for the backtest**: if the harness writes its catch-rate report under the repo's `docs/` tree it could trip this guard. Write reports to `tmp_path` or a scratch dir, NOT under `docs/`.
- `_redirect_reflexion_writes` (function, autouse) — sets `REFLEXION_OUTPUT_DIR=<tmp_path>/docs/memory` (`tests/conftest.py:95-135`). Harmless for backtest.
- `collect_ignore = ["sprint/test_property_based.py"]` (`tests/conftest.py:11-13`) shows the convention for excluding an optional-dep test module at the root level — model to follow if any backtest module needs a hard optional-dep exclude (alternative to `importorskip`).

### 3b. Suite-local conftest pattern (`tests/cli/eval/conftest.py`)

The eval suite keeps a small local conftest with **suite-specific fixtures** (`tests/cli/eval/conftest.py`). The whole file is the model for the backtest's own `tests/troubleshoot/backtest/conftest.py`:

```python
# tests/cli/eval/conftest.py:24-39  -- allowlisted scratch root fixture
@pytest.fixture
def allowlisted_output_dir() -> Path:
    root = Path("/tmp/eval-runs") / f"pytest-{uuid.uuid4().hex[:12]}"
    root.mkdir(parents=True, exist_ok=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)
```

Conventions to copy:
- `from __future__ import annotations` at top of every test/conftest module (`conftest.py:15`, every eval test file).
- Unique scratch subdir via `uuid.uuid4().hex[:12]` to avoid cross-test collisions (`conftest.py:34`).
- `try/finally` + `shutil.rmtree(root, ignore_errors=True)` for best-effort teardown (`conftest.py:36-39`).
- Fixture has a docstring explaining WHY it exists (the allowlist rationale) — strongly idiomatic here (`conftest.py:26-32`).

For the backtest, the analogous fixture is a **git-replay scratch root** (a tmp clone/worktree dir for checking out pre-fix commits). Same shape: mint unique dir, `yield`, `rmtree` in `finally`. If R3/R5 provide a git-clone helper, wrap it in such a fixture.

### 3c. tmp fixtures

- Stock `tmp_path` is used everywhere for per-test scratch (`test_schema_validate.py:115`, `test_summary_schema.py` fixtures, `test_process.py:187`). Default for the backtest's report-output dir and any git scratch that has no allowlist constraint.
- `Path(__file__).resolve().parent / "fixtures"` is the standard fixtures-dir locator (`test_schema_validate.py:40`, `test_summary_schema.py:43`). REPO_ROOT via `Path(__file__).resolve().parents[N]` — note `parents[3]` from `tests/cli/eval/` (`test_exit_codes.py:58`), so from `tests/troubleshoot/backtest/` REPO_ROOT = `Path(__file__).resolve().parents[3]` as well (tests/troubleshoot/backtest → parents: [0]=backtest dir's parent... actually `parents[3]` = repo root since file is 3 dirs deep under repo: tests/troubleshoot/backtest/test_x.py → parents[0]=backtest, [1]=troubleshoot, [2]=tests, [3]=repo root). **Verify by counting at impl time.**

## 4. Subprocess mock seam (git replay / `git checkout`, `git log`)

This is the seam for the backtest's git operations (checkout pre-fix commit, diff, etc.). The project's convention is **patch-where-used at the module-aliased import site**.

### 4a. The `_subprocess.run` alias seam (the one the prompt flagged)

`tests/sprint/test_process.py:399`:
```python
with patch("superclaude.cli.sprint.process._subprocess.run") as mock_run:
    mock_run.return_value = MagicMock(returncode=0, stdout=" file1.py | 10 ++++\n...")
    ctx = build_task_context(results, start_commit="abc123")
```
Note: the production module imports subprocess **aliased as `_subprocess`** (`from ... import subprocess as _subprocess` style), so the patch target is `<module>._subprocess.run`, NOT `subprocess.run`. The mock returns a `MagicMock(returncode=..., stdout=...)` mimicking `CompletedProcess`. Same seam reused at `test_process.py:434, 446, 451`.

**For the backtest**: whatever module runs `git` (R3's git helpers), patch its subprocess symbol at *that module's* path. If R3 names the helper `superclaude.<x>.git.run` or aliases subprocess, the patch string is `"<that module>.<alias>.run"`. Determine the exact dotted path from R3's findings — the seam is **the import site in the helper module**, never the stdlib global.

### 4b. The `Popen` seam (for long-running / streamed subprocess)

`tests/sprint/test_process.py:206`: `patch("superclaude.cli.pipeline.process.subprocess.Popen")`. Here subprocess is imported plainly (not aliased), so target is `<module>.subprocess.Popen`. The `tests/sprint/conftest.py` docstring (lines 1-30) documents the gotcha: patching `subprocess.Popen` at the shared-module level mutates the GLOBAL attribute, so a *real* `claude` subprocess elsewhere can consume a call-count-indexed fake — that's why they stub the narrative step. **Lesson for the backtest**: prefer patching the narrowest module-level alias (`_subprocess.run`) over a broad `subprocess.Popen` global to avoid cross-talk; if you must, mirror the autouse-stub-leak guard pattern from `tests/sprint/conftest.py:32-72`.

### 4c. `MagicMock` CompletedProcess shape

`MagicMock(returncode=0, stdout="...")` is the idiom for faking `subprocess.run` results (`test_process.py:400-403`). For git, set `returncode`, `stdout`, and `stderr` as needed. Import: `from unittest.mock import MagicMock, patch` (`test_process.py:7`).

## 5. Schema-validation test pattern (for the machine-readable catch-rate report)

The backtest must "emit machine-readable catch-rate report setting `backtest_status`." The project has a mature, copy-pasteable convention for *contract-testing a JSON report against a JSON Schema* — mirror `tests/cli/eval/test_summary_schema.py` + `tests/cli/eval/test_run_report.py` (D-0053/D-0054).

### 5a. Validator fixtures (module-scoped) — `test_summary_schema.py:53-65`

```python
import json
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

@pytest.fixture(scope="module")
def schema() -> dict:
    return dict(load_summary_schema())        # or json.loads(SCHEMA_PATH.read_text())

@pytest.fixture(scope="module")
def validator(schema: dict) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)  # assert the schema itself is well-formed
    return Draft202012Validator(schema)
```
(`jsonschema` is a declared dep — `pyproject.toml:39`, `jsonschema>=4.0.0`. No importorskip needed.)

### 5b. Valid-fixture assert — just `.validate()` (raises on failure)

```python
def test_valid_minimal_fixture_validates(validator):     # test_summary_schema.py:139
    payload = _load_fixture("valid_minimal.json")
    validator.validate(payload)                           # no assert needed; raises if invalid
```

### 5c. Invalid-fixture assert — `pytest.raises(ValidationError)` + substring

```python
def test_invalid_bad_status_fails(validator):            # test_summary_schema.py:166
    payload = _load_fixture("invalid_bad_status.json")
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(payload)
    assert "BOGUS" in str(exc_info.value)                # name the offending token
```

### 5d. Required-field-set pins (catches schema drift) — `test_summary_schema.py:88-101`

```python
def test_schema_required_top_level_fields(schema):
    expected = ["run_id", "started_at", ..., "evals"]
    assert schema["required"] == expected                # order-sensitive equality
```
For the backtest report schema, pin the required set (incl. `backtest_status`) and the `backtest_status` enum the same way (`test_summary_schema.py:131-137` shows the enum pin: `assert tuple(enum) == EVAL_STATUSES`). If there's a runtime constant for the status enum, mirror the "enum matches runtime model verbatim" test.

### 5e. Round-trip: model `.to_dict()` validates against schema — `test_run_report.py:7-9, 40-46`

`test_run_report.py` validates that the *emitter's actual output* (`render_summary_json` / `RunSummary.to_dict()`) validates against `summary.schema.json`. This is the strongest contract — for the backtest, after the harness emits the report, load it and run it through the validator in a test. Also note `test_run_report.py` pins **byte-stable / deterministic output** by hashing two independent renders (`hashlib`, `test_run_report.py:26`) — useful if the catch-rate report must be reproducible.

### 5f. Fixtures-dir layout for schema tests

`tests/cli/eval/fixtures/summary_schema/` holds `valid_minimal.json`, `valid_full.json`, `invalid_bad_status.json`, `invalid_missing_counts_subfield.json`, `invalid_missing_required.json`. Mirror this: `tests/troubleshoot/backtest/fixtures/<report_schema>/` with valid + invalid catch-rate report fixtures. Schema file itself lives under `src/superclaude/.../schemas/<name>.schema.json` and is loaded via `importlib.resources` (`load_summary_schema`, `test_summary_schema.py:36-38`) — the canonical-path-exists test is `test_summary_schema.py:73-76` (`assert SCHEMA_PATH.is_file()`).

## 6. OLD=MISS-green-now vs NEW=CATCH-skip-until-landed — recommended file split

To satisfy "OLD=MISS + harness wiring run green now, NEW=CATCH guarded until impl lands," mirror the `test_exit_codes.py` strategy of **mixing always-run and skip-guarded tests in the same module with explicit comments**:

- **Always-green now** (no skip guard):
  - Harness wiring tests: replay-runner constructs, git-checkout helper is patched, report schema is well-formed (`check_schema`), valid/invalid report fixtures validate.
  - OLD=MISS assertions: replaying E1–E5 against the pre-fix commit with the OLD (no-gate) logic yields MISS — this is provable today because the OLD code exists.
- **Skip-guarded (un-skip when impl lands)** — gate body with `_new_gate_missing()` probe:
  - NEW=CATCH assertions: replaying the same E1–E5 with the NEW gate yields CATCH. Guard with a `hasattr`/`inspect.getsource` forward-dep probe against the NEW gate symbol/branch (per §2), `pytest.skip(...)` with a self-clearing reason.
  - The catch-rate-report `backtest_status` assertion that depends on CATCH outcomes.

Module docstring should state the split explicitly, exactly like `test_exit_codes.py:29-44` does ("While those helpers are absent we `pytest.skip`... the skips evaporate once X lands").

## 7. Misc idioms to carry over

- `from __future__ import annotations` first line of every module (universal here).
- Module + test docstrings cross-link the spec/deliverable IDs (e.g. "FR-RPT1 / D-0054 / T03.11", `test_run_report.py:1`). Backtest tests should cite E1–E5 / the spec/deliverable IDs from R4.
- Comment WHY a skip exists and WHEN it clears — never a bare `pytest.skip("todo")`.
- No `unittest.TestCase` classes for new suites; plain `test_*` functions (eval suite is all functions). `Test*` classes are allowed (`pyproject.toml:107`) and used in `tests/sprint/test_process.py`, but functions are the dominant style in the newest (eval) suite.
- Run command: `uv run pytest tests/troubleshoot/backtest/ -v` (UV only; `-v` already in addopts).

---

## Unverified / Hand-off notes

- **Exact git-helper patch target**: depends on R3's git-helper module path + whether it aliases `subprocess`. The *pattern* (patch-where-used at the module's import-site alias) is verified (`test_process.py:399`); the exact dotted string must come from R3. (Unverified here.)
- **Whether the NEW gate is a named symbol vs a closure branch**: determines `hasattr` probe (§2a) vs `inspect.getsource` probe (§2b). R6 owns the NEW-gate seam — pick the probe to match. (Unverified here.)
- **REPO_ROOT `parents[N]` depth** from `tests/troubleshoot/backtest/`: reasoned to be `parents[3]` but count at impl time. (Reasoned, not executed.)
- **Backtest report schema location/loader**: follow the `src/superclaude/.../schemas/*.schema.json` + `importlib.resources` convention; R7 owns the report model. (Convention verified; specific file is R7's.)

Status: Complete

### Summary
The project has NO `xfail` (0 occurrences); the established convention for guarding assertions whose impl hasn't landed is a **forward-dependency probe (`hasattr` on the impl module, or `inspect.getsource` substring for closure branches) + self-clearing `pytest.skip(...)`** with a reason string that names the missing dep and states the un-skip trigger (canonical: `tests/cli/eval/test_exit_codes.py:92-123`, `tests/cli/eval/test_no_mcp_skip.py:485-505`). `--strict-markers` is ON (`pyproject.toml:111`) so any new marker (likely unnecessary) must be registered in `pyproject.toml:114-144`; `testpaths=["tests"]` auto-collects `tests/troubleshoot/backtest/`. Schema-validation idiom is `jsonschema.Draft202012Validator` (declared dep `pyproject.toml:39`) via module-scoped `schema`/`validator` fixtures, `.validate()` for valid + `pytest.raises(ValidationError)`+substring for invalid, with `valid_*`/`invalid_*` JSON fixtures under a `fixtures/<schema>/` dir (`tests/cli/eval/test_summary_schema.py`, `test_run_report.py`). Subprocess mock seam = patch the module-aliased import site, e.g. `patch("superclaude.cli.sprint.process._subprocess.run")` returning `MagicMock(returncode=, stdout=)` (`tests/sprint/test_process.py:399`), preferring the narrow alias over global `subprocess.Popen` to avoid the cross-talk documented in `tests/sprint/conftest.py:1-30`. Fixtures: stock `tmp_path` plus a suite-local `conftest.py` mirroring `allowlisted_output_dir` (`tests/cli/eval/conftest.py:24-39`, uuid scratch dir + `try/finally rmtree`). Recommended OLD=MISS/NEW=CATCH split: one module mixing always-green wiring+OLD=MISS tests with skip-guarded NEW=CATCH tests, docstring stating the split, exactly like `test_exit_codes.py:29-44`. Avoid writing reports under `docs/` (root `_pollution_snapshot` guard, `tests/conftest.py:30-93`).
