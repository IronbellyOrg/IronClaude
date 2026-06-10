# Research: CLI Test Patterns

**Status:** Complete
**Date:** 2026-06-08
**Topic:** Test & Verification — CLI test patterns for `superclaude reflect run`
**Scope:** `tests/cli/prd/`, `tests/cli/eval/`, ClaudeProcess monkeypatch patterns, `pyproject.toml` markers, Makefile lint/format/test gates

---

## TL;DR (what the wrapper tests should copy)

1. **CliRunner idiom** — copy `tests/cli/prd/test_cli_smoke.py` verbatim: `CliRunner().invoke(group, [...])` → assert `result.exit_code` / `result.output`. Use a Click `Group` (`reflect_group`) imported from `superclaude.cli.reflect.commands`.
2. **ClaudeProcess stub** — two proven idioms exist; the wrapper should use the **roadmap idiom** (`patch("superclaude.cli.reflect.<module>.ClaudeProcess")` + a `side_effect` factory that returns a `MagicMock` whose `.wait.return_value = <rc>` and whose `output_file`/contract is written as a side effect). This is the cleanest match because the wrapper's spec call shape (§8 line 125) is `ClaudeProcess(prompt=…, …); proc.start(); rc = proc.wait()`.
3. **Fixture contracts** — store `return-contract.yaml` fixtures under `tests/cli/reflect/fixtures/` and load them with the `FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"` pattern (`tests/cli/eval/test_suite_loader.py:49`). The stub's side-effect copies the chosen fixture to `<output>/return-contract.yaml`.
4. **Markers** — `pyproject.toml:113-141` defines `unit`, `integration`, etc. with `--strict-markers` (`pyproject.toml:110`). Wrapper unit tests can run unmarked (the suite does not require a marker); apply `@pytest.mark.integration` only to any test that drives a real subprocess. No new marker is needed.
5. **Gates** — `make lint` runs `ruff check .` (Makefile:48-50) and `make format` runs `ruff format .` (Makefile:53-55). **CI additionally runs `ruff format --check`** (per memory `make lint ≠ CI ruff format`). Before push run BOTH: `uv run ruff check src/ tests/` AND `uv run ruff format --check src/ tests/`. There is **no mypy/type target** in the Makefile.

---

## 1. CliRunner idiom (how existing tests invoke Click commands)

**Canonical source:** `tests/cli/prd/test_cli_smoke.py`. This is the exact template the wrapper tests should mirror.

```python
# tests/cli/prd/test_cli_smoke.py:11-15
from click.testing import CliRunner
from superclaude.cli.prd.commands import prd_group

def _runner() -> CliRunner:
    return CliRunner()
```

Help-surface assertion (`test_cli_smoke.py:22-26`):
```python
result = _runner().invoke(prd_group, ["--help"])
assert result.exit_code == 0
assert "run" in result.output
```

Option-presence assertion (`test_cli_smoke.py:30-43`) loops over a flag list and asserts each appears in `result.output`. **Wrapper analogue:** assert `--tmux`, `--print-command`, `--no-promote`, `--promote`, `--timeout`, `--depth`, `--output`, `--allow-single-vendor`, `--dry-run` are all present (spec §9 "In", line 129).

Dry-run / exit-code assertion (`test_cli_smoke.py:51-54`):
```python
result = _runner().invoke(prd_group, ["run", "test", "--dry-run"])
assert result.exit_code == 0
assert "Dry run" in result.output
```

Invalid-input → non-zero (`test_cli_smoke.py:56-59`): `assert result.exit_code != 0`.

> **Note on exit codes via CliRunner:** Click maps a raised `SystemExit(N)` / `ctx.exit(N)` to `result.exit_code`. The wrapper must call `ctx.exit(10/11/2)` (or `sys.exit`) so CliRunner observes the custom codes. Assert the *exact* code (`== 10`, `== 11`, `== 2`), not just `!= 0`, for the verdict tests below.

---

## 2. Stubbing ClaudeProcess (no real subprocess)

Two proven idioms exist in the repo. Both avoid launching `claude`.

### Idiom A — `unittest.mock.patch` on the executor's imported symbol (RECOMMENDED for the wrapper)

Used by the roadmap suite. Patch the name **as imported into the module under test**, not where it's defined.

```python
# tests/roadmap/test_file_passing.py:58-69
with patch("superclaude.cli.roadmap.executor.ClaudeProcess") as mock_proc:
    instance = MagicMock()
    instance._process = None
    mock_proc.return_value = instance
    mock_proc.side_effect = lambda **kw: _capture_and_return(kw, captured_prompt, instance)
    instance.wait.return_value = 0
    result = roadmap_run_step(step, config, cancel_check=lambda: False)
assert result.status == StepStatus.PASS
```

Capture helper (`tests/roadmap/test_file_passing.py`, `_capture_and_return`):
```python
def _capture_and_return(kwargs: dict, store: dict, instance: MagicMock) -> MagicMock:
    store["value"] = kwargs.get("prompt", "")
    store["extra_args"] = kwargs.get("extra_args", [])
    return instance
```

**Why this fits the wrapper:** §8 line 125 says the wrapper does `proc = ClaudeProcess(prompt=…, model=…, timeout_seconds=3600, output_format="stream-json", env_vars=build_env()); proc.start(); rc = proc.wait()`. A `MagicMock` instance with `.wait.return_value = <rc>` and `.start.return_value = None` exactly satisfies that surface. To simulate the contract being written, attach a side-effect that writes the fixture (see §3).

### Idiom B — decorator `@patch` + a factory side_effect that writes the output file (PRD e2e)

The PRD e2e suite patches `PrdClaudeProcess` and uses a factory that writes `output_file` from within `wait()`. This is the **most directly reusable shape** for the wrapper because it both returns an exit code AND writes a file — exactly what the wrapper's contract-consumption flow needs (write `return-contract.yaml` instead of the PRD step output).

```python
# tests/cli/prd/test_e2e.py:261-262
@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_full_prd_creation_standard(mock_synth_mapping, mock_process_cls, ...):
    mock_process_cls.side_effect = _mock_process_factory(default_line_count=120)
```

Factory (`tests/cli/prd/test_e2e.py:224-253`) — the load-bearing pattern:
```python
def _mock_process_factory(*, step_overrides=None, default_line_count=100):
    overrides = step_overrides or {}
    def factory(**kwargs):
        step_id = kwargs["step_id"]
        output_file = kwargs["output_file"]
        mock_proc = MagicMock()
        if step_id in overrides:
            exit_code, output_text = overrides[step_id]
        else:
            exit_code = 0
            output_text = _make_passing_output(step_id, default_line_count)
        mock_proc.start_with_retry.return_value = None
        def write_output_and_return():
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(output_text, encoding="utf-8")
            return exit_code
        mock_proc.wait.side_effect = write_output_and_return
        return mock_proc
    return factory
```

**Wrapper adaptation:** rename the override map to key on nothing (single launch) and have `write_output_and_return` copy a fixture contract:
```python
def factory(**kwargs):
    output_dir = kwargs["output_file"].parent   # or however the wrapper passes paths
    mock = MagicMock()
    mock.start.return_value = None
    def _wait():
        (output_dir / "return-contract.yaml").write_text(FIXTURE_BYTES, encoding="utf-8")
        return rc          # 0 / 124 / etc.
    mock.wait.side_effect = _wait
    return mock
```

### Idiom C — `monkeypatch.setattr` on ClaudeProcess methods (sprint/preflight)

For the rare test that wants the *real* `ClaudeProcess` object but with neutered I/O:
```python
# tests/sprint/test_stage1_wiring.py:80-82
monkeypatch.setattr(pipe.ClaudeProcess, "__init__", _spy_init)
monkeypatch.setattr(sproc.ClaudeProcess, "start", lambda self: None)
monkeypatch.setattr(sproc.ClaudeProcess, "wait", lambda self: None)
```
And `tests/sprint/test_preflight.py:1012` swaps in a tracking subclass:
```python
monkeypatch.setattr(executor_mod, "ClaudeProcess", _TrackingClaudeProcess)
```
Use this only if a test must assert on the *real* `build_command()` / `build_env()` output. For verdict/exit/write-back tests, Idiom A or B is simpler.

### The real-subprocess shim (when you DO want end-to-end Popen)

`tests/cli/eval/test_claude_process_adapter.py:120-150` drops a bash `claude` shim on `PATH` (via `monkeypatch.setenv("PATH", ...)`) that emits deterministic stdout/stderr and `exit 0`. Heavier; only needed for a true integration test of the spawn path. Not recommended for the verdict matrix — keep those as fast mocked unit tests.

---

## 3. Fixture organization & loading the `return-contract.yaml`

**Existing precedent:** `tests/cli/eval/fixtures/` holds `*.yaml` and nested dirs (`coverage_gate/`, `summary_schema/`), plus an `__init__.py`. Loaded via:
```python
# tests/cli/eval/test_suite_loader.py:49
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
# usage: loader.load(FIXTURES_DIR / "valid_suite.yaml")   # :78
```

**Recommended layout for the wrapper:**
```
tests/cli/reflect/
├── __init__.py
├── conftest.py                       # shared CliRunner + monkeypatched-ClaudeProcess fixture
├── fixtures/
│   ├── __init__.py
│   ├── pass.yaml                     # tier_reached:2, full diversity, verification_ran:true
│   ├── halted_regression.yaml        # regression_present / drift>0 / status:partial
│   ├── degraded_serena.yaml          # degraded_components ⊇ {serena}
│   ├── degraded_single_vendor.yaml   # t2_vendor_diversity: single
│   ├── blocked_stop.yaml             # STOP / unparseable
│   ├── unknown_major.yaml            # contract_version: 2.0.0
│   └── unknown_field.yaml            # 1.x + extra unrecognised key (tolerance test)
├── test_cli_smoke.py                 # help/flags/dry-run (mirror prd test_cli_smoke.py)
├── test_verdict_mapping.py           # fixture → verdict → exit code matrix
├── test_writeback.py                 # frontmatter atomic write + compare-mismatch sidecar
└── test_no_nesting_guard.py          # NFR-7
```

The conftest fixture mints an output dir (`tmp_path`) and a factory that copies a named fixture into `<output>/return-contract.yaml`. Note `tests/cli/eval/conftest.py` shows the project's conftest convention (module-scoped shared fixtures, yields + cleanup).

---

## 4. Markers that apply to wrapper tests

From `pyproject.toml`:
- `pyproject.toml:106-111` — `addopts = ["-v", "--strict-markers", "--tb=short"]`. **`--strict-markers` means any `@pytest.mark.X` must be declared in `markers`** or collection errors.
- `pyproject.toml:113-141` — declared markers include `unit`, `integration`, `performance`, `slow`, `confidence_check`, `self_check`, `reflexion`, `complexity`, plus many `diagnostic_*` / sprint-specific ones.

**Applicability:**
- Most wrapper tests are plain functions (no marker) — the suite does **not** auto-require markers; `tests/cli/prd/test_cli_smoke.py` uses none. Default to unmarked.
- `@pytest.mark.integration` — apply only to a test that uses the real `claude` shim / real subprocess (the §2 shim path), if one is written.
- Do **not** invent a new marker (would need a `pyproject.toml` entry to pass `--strict-markers`). The brief's "unit/integration/confidence_check/etc." are available but optional; verdict-matrix tests need none.

---

## 5. CI / Makefile gates (exact commands)

From `Makefile`:
```
test:                 # Makefile:13-15
	uv run pytest

lint: lint-architecture   # Makefile:48-50
	uv run ruff check .

format:               # Makefile:53-55
	uv run ruff format .
```

- **No `mypy`/type-check target exists** in the Makefile (grep found none). Type hints are stylistic, not gated.
- `make lint` ALSO runs `lint-architecture` (a prerequisite target) before `ruff check .`. Relevant because `tests/cli/eval/test_ban_import_rule.py` + the adapter test enforce a no-`anthropic`-SDK-import architecture rule under `cli/eval/`. The wrapper lives under `cli/reflect/` (not `cli/eval/`), so that specific ban likely does not apply — **Unverified** whether an analogous import ban covers `cli/reflect/`; check `make lint-architecture` / the ban-import config before assuming.

**CRITICAL CI delta (memory `make lint ≠ CI ruff format`):** `make lint` only runs `ruff check`; it does **not** run `ruff format --check`. CI runs them separately. Before pushing wrapper code, run BOTH:
```
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
```
A green `make lint` does NOT guarantee green CI format.

---

## 6. Concrete test cases the wrapper needs (verdict/exit matrix)

Derived from spec §6 exit table (`merged-requirements.md:78-82`) + FR-5/FR-8/FR-11. Each row = one fixture + one assertion on `result.exit_code` and the written `reflect_post.verdict`.

| # | Scenario | Fixture / stub setup | Assert exit_code | Assert verdict | Spec cite |
|---|----------|----------------------|------------------|----------------|-----------|
| 1 | pass | `pass.yaml` (tier_reached:2, full diversity, verification_ran:true), `wait→0` | `0` | `pass` | §6 (the only exit-0 path), FR-8 line 28 |
| 2 | halted (deviations) | fixture with `regression_present` / `drift>0` / `status: partial` / `needs_human_decision`, `wait→0` | `10` | `halted` | line 82 |
| 3 | degraded (lost Tier-2) | fixture `degraded_components ⊇ {serena}` (or `tier_reached==1` when T2 expected, or `t2_model_class_diversity != full`) | `11` | `degraded` | line 81, FR-11 line 31 |
| 4 | blocked — missing/unparseable contract | stub `wait→0` but writes NO `return-contract.yaml` (or garbage) | `2` | `blocked` | line 79, FR-5 line 25 |
| 5 | blocked — timeout | stub `wait→124` | `2` | `blocked` (reason: timeout) | line 80, NFR-5 line 40 |
| 6 | blocked — child crash | stub `wait→1` (non-0, non-124) with no usable contract | `2` | `blocked` | line 79 |
| 7 | frontmatter write-back success | pass fixture + a real tasklist md w/ `reflect_post:` stub block in `tmp_path`; assert the file's frontmatter now has the §6 structured `reflect_post` block, body bytes unchanged | `0` | n/a | FR-6 line 26 |
| 8 | compare-mismatch → sidecar + non-zero | simulate concurrent edit: monkeypatch the read→replace window so on-disk bytes differ at compare; assert NO overwrite, `<output>/wrapper-result.yaml` sidecar written, exit non-zero | `!= 0` | n/a | FR-6 line 26 |
| 9 | dry-run → no launch | `--dry-run`; assert `ClaudeProcess` mock **never called** (`mock_proc.assert_not_called()`), exit `0`, "Dry run" in output | `0` | n/a | §9 line 129, mirror prd `test_cli_smoke.py:51` |
| 10 | unknown major contract_version → blocked | `unknown_major.yaml` (`contract_version: 2.0.0`) | `2` | `blocked` (fail-loud) | FR-5 line 25, §11 line 133 |
| 11 | unknown-field tolerance (1.x) | `unknown_field.yaml` (`contract_version: 1.9.0` + extra key) → still maps to `pass` | `0` | `pass` | FR-5 "1.x tolerant" line 25 |
| 12 | single-vendor halts unless flag | `degraded_single_vendor.yaml` (`t2_vendor_diversity: single`): without `--allow-single-vendor` → `degraded`/`11`; with the flag → `pass`/`0` | `11` then `0` | `degraded` then `pass` | FR-11 line 31, §11 line 138 |
| 13 | print-command → no launch | `--print-command`: assert the composed `claude` command string is printed and `ClaudeProcess` never spawned | `0` | n/a | §9 line 129 |

**Mock-call assertions available:** with Idiom A/B you get `mock_proc.assert_not_called()` (cases 9, 13) and `mock_proc.assert_called_once()` (cases 1-6, 11, 12) for free.

**Write-back specifics (case 7/8):** FR-6 mechanism is read bytes → parse frontmatter → inject only `reflect_post` → yamllint-safe dump → temp in same dir → **compare on-disk bytes == bytes read** → `os.replace()`. Test 7 asserts the happy path (body byte-preserved — read the body bytes before and after, assert equal). Test 8 forces the compare to fail (e.g. monkeypatch `Path.read_bytes` to return a different value on the second read, or write a different byte to the file between read and replace) and asserts the sidecar-and-bail branch.

---

## 7. No-nesting guard (NFR-7) — concrete, testable assertion

**Spec:** NFR-7 (line 42): "The item invokes the wrapper as a **Bash shell-out**, never via Agent/Task; a guard test documents this (V1 R-4)." Risk line 136: "**Wired via Agent/Task (re-introduces nesting bug):** template says Bash shell-out; guard test + SKILL note."

The guard is **document/template-level**, not a runtime behaviour of the Python module (the module just spawns a subprocess; it has no Agent surface to inspect). So the testable artifact is the **POST_REFLECT_MODE template branch** that the tasklist item emits. Two layers:

### Layer A — template/string assertion (the load-bearing guard)
Locate the opt-in `POST_REFLECT_MODE: wrapper` template branch (spec §9 line 129; R06 covers the template file — **Unverified path**, likely under `src/superclaude/skills/.../templates/` or the tasklist template). Assert it shell-outs and does not mention Agent/Task:
```python
def test_post_reflect_wrapper_branch_is_bash_shellout():
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    branch = _extract_wrapper_branch(text)              # the POST_REFLECT_MODE: wrapper block
    # POSITIVE: it invokes the CLI as a shell command
    assert "superclaude reflect run" in branch
    # NEGATIVE: it must NOT route through the Agent/Task tool surface
    for forbidden in ("Task(", "subagent_type", "Agent tool", "via Agent", "Task tool"):
        assert forbidden not in branch, f"NFR-7 violation: nesting via {forbidden!r}"
```
This is the canonical assertion to propose: **positive match on the `Bash`/CLI invocation string + negative match on Agent/Task tokens.**

### Layer B — runtime guard (the module never imports an Agent surface)
A lighter complementary check that the wrapper module spawns only a subprocess and imports no agent/Task machinery:
```python
def test_wrapper_module_has_no_agent_imports():
    src = (REPO_ROOT / "src/superclaude/cli/reflect/runner.py").read_text(encoding="utf-8")
    # the wrapper launches reflect ONLY via ClaudeProcess (subprocess), never an Agent/Task API
    assert "ClaudeProcess" in src
    for banned in ("import anthropic", "from anthropic", "subagent", "Task("):
        assert banned not in src
```
Precedent for an "import-ban over a subtree" test: `tests/cli/eval/test_ban_import_rule.py` and `tests/cli/eval/test_claude_process_adapter.py:1-40` (greps the `cli/eval/` subtree for `from anthropic`/`import anthropic`). The wrapper can copy that grep-over-subtree shape for `cli/reflect/`.

**Recommendation:** ship **Layer A** as the primary NFR-7 guard (it tests the actual artifact that wires the gate — the template) and **Layer B** as a cheap defensive backstop. Layer A is what the spec's "guard test documents this" refers to.

---

## 8. Supporting precedents & notes

- **Resume/idempotent skip** (FR §7 line 111 "re-run idempotent at frontmatter; optional `--resume` skips a still-clean HEAD"): `tests/cli/prd/test_resume_skip.py` is the precedent. It monkeypatches `executor._execute_step` to record calls and asserts skip behaviour (`test_resume_skip.py:44-62`). The wrapper's `--resume` test can monkeypatch the HEAD-clean check and assert `ClaudeProcess` is not spawned.
- **Dry-run sets a sentinel outcome:** `src/superclaude/cli/prd/executor.py:509-510` (`if self._config.dry_run: result.outcome = "dry_run"`). Wrapper dry-run should similarly short-circuit before `proc.start()`.
- **`ClaudeProcess.__init__` is keyword-only** (`src/superclaude/cli/pipeline/process.py:37-54`, leading `*`): `prompt`, `output_file`, `error_file`, `model`, `timeout_seconds`, `output_format`, `env_vars` etc. Stubs must accept `**kwargs` (both PRD and roadmap factories do). The spec's call (§8 line 125) uses `timeout_seconds=3600` and `output_format="stream-json"`, matching this signature.
- **`make verify-sync`** is a separate gate for `src/` ↔ `.claude/` skill/template drift (per CLAUDE.md). Any template/SKILL edit for the POST_REFLECT branch must be made in `src/superclaude/` then `make sync-dev` — not in `.claude/`. The guard test (Layer A) should read the **`src/superclaude/`** copy of the template, not the `.claude/` mirror, so it tests the source of truth.

---

## Summary

The wrapper test suite under `tests/cli/reflect/` should be built from three existing, proven patterns: (1) `tests/cli/prd/test_cli_smoke.py`'s `CliRunner().invoke(group, [...])` → `exit_code`/`output` idiom for help/flags/dry-run; (2) the roadmap/PRD `patch("...reflect....ClaudeProcess")` + `side_effect` factory idiom where a `MagicMock` returns the desired `wait()` rc and writes a fixture `return-contract.yaml` into the output dir (matching the spec's `proc.start(); rc = proc.wait()` shape); and (3) `tests/cli/eval`'s `FIXTURES_DIR = Path(__file__).parent / "fixtures"` loading for the contract fixtures. The verdict matrix needs 13 cases mapping fixtures → `{pass:0, halted:10, degraded:11, blocked:2}` per spec §6, plus contract-version gating (unknown major→blocked, 1.x unknown-field→tolerant), write-back success + compare-mismatch→sidecar, dry-run/print-command no-launch, and single-vendor halt-unless-flag. The NFR-7 no-nesting guard is best implemented as a **template string assertion** (positive: `"superclaude reflect run"` present; negative: no `Task(`/`subagent`/`Agent tool` tokens) over the `src/superclaude/` template, backed by a lighter module import-ban test modeled on `tests/cli/eval/test_ban_import_rule.py`. Gates: `make lint` (`ruff check .`) + the CI-only `ruff format --check src/ tests/` (run both manually), `uv run pytest`; no mypy target exists. Tests need no new pytest marker — default unmarked, `@pytest.mark.integration` only for any real-subprocess shim test.
