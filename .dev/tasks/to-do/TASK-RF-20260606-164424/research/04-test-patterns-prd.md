# Research
Topic type: Test & Verification — existing tests/cli/prd/ patterns
Scope: /config/workspace/IronClaude/tests/cli/prd/ (test_prompts.py, test_resolve_step_content.py, test_gates.py, test_executor.py, test_e2e.py; conftest/fixtures from others)
Status: Complete
Date: 2026-06-06

---

## Directory facts (verified)

- `tests/cli/prd/__init__.py` EXISTS, empty (0 bytes). Package import works.
- NO `conftest.py` in `tests/cli/prd/`. Only top-level `tests/conftest.py` applies.
- Test invocation: `uv run pytest tests/cli/prd/ -q` (confirmed valid path with __init__.py).
- File sizes (lines): test_e2e.py=574, test_executor.py=139, test_gates.py=243,
  test_prompts.py=276, test_resolve_step_content.py=112.

---

## CRITICAL: which AC-referenced symbols EXIST vs. are NET-NEW

Verified by grep over `src/superclaude/cli/prd/` (executor.py, gates.py):

| Symbol (from ACs) | Status in source TODAY | Where |
|---|---|---|
| `_resolve_step_content(step_id, task_dir, ndjson_text)` | EXISTS | executor.py:266 |
| `_STEP_ARTIFACT_FILES` (dict) | EXISTS | executor.py:252 |
| `_determine_status(self, exit_code, output, step_id)` | EXISTS | executor.py:645 |
| `_persist_step_artifact(self, step_id, output_text)` | EXISTS | executor.py:1145 |
| `_detect_sentinel(output)` | EXISTS (used in test_executor) | executor.py |
| `_artifact_path_for_step` (AC2) | **DOES NOT EXIST** — net-new | — |
| `_pick_best_candidate` (AC4) | **DOES NOT EXIST** — net-new | — |
| `_check_no_truncation_marker` (AC9) | **DOES NOT EXIST** — net-new | gates.py has no such fn |
| variant-name recovery via WHERE / INV-005 bounded WHERE | **NOT PRESENT** — net-new | `_resolve_step_content` globs `task_dir`+`task_dir.parent` only; no WHERE scan, no `..`/symlink containment |

**Implication for the task-builder:** ACs 1-10 are tests for functionality the BUILD_REQUEST INTRODUCES. Tests for `_artifact_path_for_step`, `_pick_best_candidate`, `_check_no_truncation_marker`, WHERE-recovery, and INV-005 containment will FAIL on current `master` until the impl lands — red-first acceptance tests, not regression guards over existing code. The existing tests below are the STYLE templates to mirror, not behavior to preserve verbatim.

Current `_resolve_step_content` shape (executor.py:266-345, verified): special-case branches for `build-task-file` (globs `task_dir/TASK-PRD-*.md`, largest wins) and `assembly` (globs `results/`,`task_dir`,`task_dir.parent` for `*prd*.md`), then `_STEP_ARTIFACT_FILES.get(step_id)` static-name lookup over task_dir+parent, else returns `ndjson_text`. **No WHERE-list param today.** AC3's call `_resolve_step_content("scope-discovery", task_dir, "<ndjson>")` is still 3-arg — so WHERE must be read INTERNALLY from `task_dir/parsed-request.json`, not passed as a 4th arg. **Flag for R5 cross-validation: confirm the intended signature/where-source.**

---

## 1. Framework, style, imports (per file)

All 5 files: **pytest**, `from __future__ import annotations`, no unittest.TestCase. Mix of bare functions and grouping `class TestX:` (no inheritance). No custom markers in these files. Imports pull directly from `superclaude.cli.prd.*`.

- **test_resolve_step_content.py** (functions only): `from superclaude.cli.prd.executor import _resolve_step_content`. Local helper `_write_lines(path, n_lines, prefix)`.
- **test_executor.py** (functions only): `from superclaude.cli.prd.config import resolve_config`; `from superclaude.cli.prd.executor import PrdExecutor, _detect_sentinel`; `from superclaude.cli.prd.models import PrdStepStatus`.
- **test_prompts.py** (classes): `from superclaude.cli.prd.models import PrdConfig`; bulk import of ~19 `build_*` builders + `_read_file` from `superclaude.cli.prd.prompts`.
- **test_gates.py** (classes): imports `_check_*` privates + `_safe_check` from `superclaude.cli.prd.gates`.
- **test_e2e.py** (functions, `@patch`-decorated): `from unittest.mock import MagicMock, patch`; `resolve_config`, `PrdExecutor`, `from ...models import ExistingWorkState, PrdStepStatus`.

---

## 2. Fixtures & PrdConfig / task_dir construction

`tmp_path` is the universal base. NO conftest in tests/cli/prd/; only `tests/conftest.py` is inherited — none PRD-specific (PM-agent/reflexion fixtures + two autouse pollution guards `_pollution_snapshot`, `_redirect_reflexion_writes`, both transparent).

**Two PrdConfig construction idioms:**

(a) **Direct `PrdConfig(...)` kwargs** (test_prompts.py:107-115) — full control with real on-disk `task_dir`+`skill_refs_dir`:
```python
return PrdConfig(
    user_message="Create a PRD for TestProduct",
    product_name="TestProduct",
    product_slug="test-product",
    tier="standard",
    task_dir=task_dir,
    skill_refs_dir=skill_refs,
    output_path=task_dir / "output.md",
)
```

(b) **`resolve_config(...)` then patch `.task_dir`** (test_executor.py:27-35, test_e2e.py:44-57) — dominant idiom for executor tests:
```python
config = resolve_config(
    "Create PRD for SuperClaude CLI",
    product="superclaude-cli", tier="standard",
    output=str(e2e_task_dir.parent), max_turns=1000, dry_run=False,
)
config.task_dir = e2e_task_dir
config.work_dir = e2e_task_dir.parent
```
For pure-unit executor tests (no FS), `resolve_config(..., dry_run=True)` + `PrdExecutor(prd_config)` suffices (test_executor.py:27-41).

The `task_dir` fixture in test_prompts.py:41-90 pre-creates `research/`,`synthesis/`,`qa/` and writes `parsed-request.json`, `scope-discovery-raw.md`, `TASK-PRD-test-product.md`, `research-notes.md`. **Reusable for AC3 — already writes `parsed-request.json` with `"WHERE": ["src/"]` at line 53.**

**monkeypatch path-isolation idiom (test_path_resolution.py:32-44)** — relevant to AC5 containment & cwd/home pinning:
```python
def _isolate_paths(monkeypatch, *, cwd, home):
    monkeypatch.setattr(Path, "cwd", classmethod(lambda cls: cwd))
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
```

---

## 3. Subprocess / agent-output mocking (CRITICAL for AC3/AC7/AC10)

### test_executor.py — NO subprocess mock
The 5 tests bypass subprocess: call `executor._determine_status(exit_code, output, step_id)` with a hand-written `output` string, or `_detect_sentinel(output)` directly. **AC7 mirrors `test_determine_status_pass` (test_executor.py:49-59):**
```python
def test_determine_status_pass(executor):
    output = (
        "Some subprocess output here...\n"
        "Analysis complete.\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )
    status = executor._determine_status(exit_code=0, output=output, step_id="parse-request")
    assert status == PrdStepStatus.PASS
```
QA_FAIL variant (test_executor.py:81-87): `output = 'QA Review Results:\n"verdict": "FAIL"\n...'` → `assert status == PrdStepStatus.QA_FAIL`. AC7's CONTINUE / verdict:FAIL map 1:1.

### test_e2e.py — subprocess mocked via `@patch` on `PrdClaudeProcess` + factory (THE mechanism for AC10)
`superclaude.cli.prd.executor.PrdClaudeProcess` is patched; `mock_process_cls.side_effect = _mock_process_factory(...)`. Factory returns a `MagicMock` whose `.wait.side_effect` WRITES the fake output then returns exit code (test_e2e.py:224-253):
```python
def factory(**kwargs):
    step_id = kwargs["step_id"]; output_file = kwargs["output_file"]
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
```
`_make_passing_output(step_id, line_count)` (test_e2e.py:81-221) builds gate-satisfying text per step (section headers + min lines + trailing `EXIT_RECOMMENDATION: CONTINUE`).

**For AC10** (mocked subprocess writes a VARIANT filename → no HALT → no leftover variant files): inside `write_output_and_return`, ALSO write a variant-named file (e.g. `task_dir/.dev/specs/scope-discovery.md`) so `_resolve_step_content` recovery runs end-to-end. Every e2e test carries TWO `@patch` decorators and monkeypatches `_build_prompt`:
```python
@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_...(mock_synth_mapping, mock_process_cls, <config_fixture>):
    mock_process_cls.side_effect = _mock_process_factory(default_line_count=120)
    mock_synth_mapping.return_value = [{"synth_file": "section-overview.md"}, ...]
    executor = PrdExecutor(config)
    executor._build_prompt = lambda builder_name, step_id=None: f"Mock prompt for {builder_name}"
    result = executor.run()
    assert result.outcome == "success"
```
HALT assertion (test_e2e.py:558): `assert result.outcome == "halt"`. So AC10 "no HALT" = `assert result.outcome == "success"`. "No variant files left in WHERE dir" = `assert not list(where_dir.glob("scope-discovery*"))` / `glob("research-notes*")` after `run()`.

### overrides mechanism (force a specific step's output)
`_mock_process_factory(step_overrides={"scope-discovery": (0, "<24-line ndjson>")})` injects exact `(exit_code, output_text)` per step — directly usable to feed AC3/AC10 a short NDJSON while a variant file sits on disk.

---

## 4. `_resolve_step_content` invocation template (for AC3-AC6)

test_resolve_step_content.py: plain functions, `tmp_path: Path`, local `_write_lines` helper, direct call + equality assert. **Full template (lines 25-38) for AC3-AC6:**
```python
def _write_lines(path: Path, n_lines: int, prefix: str = "line") -> str:
    content = "\n".join(f"{prefix} {i}" for i in range(n_lines)) + "\n"
    path.write_text(content, encoding="utf-8")
    return content

def test_build_task_file_returns_disk_content_not_ndjson(tmp_path: Path) -> None:
    task_dir = tmp_path / "prd-fake"
    task_dir.mkdir()
    task_file = task_dir / "TASK-PRD-fake.md"
    on_disk = _write_lines(task_file, 450)
    ndjson_text = "short assistant commentary\nfewer than 20 lines"
    result = _resolve_step_content("build-task-file", task_dir, ndjson_text)
    assert result == on_disk
    assert result != ndjson_text
    assert len(result.splitlines()) >= 400
```
- **AC3 (variant recovery)**: write a ≥50-line `scope-discovery.md` into a WHERE dir under task_dir + `parsed-request.json` with `WHERE=[".dev/specs"]`, pass a 24-line ndjson → assert result is the disk doc (`len(result.splitlines()) >= 50`). Mirror this template; add the parsed-request.json setup from test_prompts.py:51-57.
- **AC4 (freshness tiebreak INV-006)**: write stale-LONGER file in WHERE dir with older mtime (`os.utime(path, (t, t))`), fresher-SHORTER correct file in task_dir → assert the task_dir file wins. (Note `_pick_best_candidate` is net-new; this test drives its introduction.)
- **AC5 (bounded WHERE INV-005)**: WHERE entry escaping repo via `..`/symlink NOT added; benign in-repo WHERE IS. Use the `monkeypatch` cwd/home or a real symlink under tmp_path; assert escaped-dir content is NOT returned.
- **AC6 (zero-match)**: mirror `test_build_task_file_falls_back_to_ndjson_when_no_match` (lines 76-85): empty task_dir → `assert result == ndjson_text`, no crash.
- Existing `test_known_static_step_id_still_resolves_from_disk` (lines 103-112) using `step_id="research-notes"` is the closest analog to AC3's scope-discovery case.

---

## 5. Prompt-string assertion template (for AC1-AC2)

test_prompts.py: `class TestX:` groups, builders called with config or dynamic kwargs, substring asserts. **Full template (lines 123-139) for AC1:**
```python
class TestInvestigationPromptStalenessProtocol:
    def test_build_investigation_prompt_includes_staleness_protocol(self) -> None:
        prompt = build_investigation_prompt(
            topic="Auth system", agent_type="Feature Analyst",
            files=["src/auth.py", "src/middleware.py"],
            product_root="src/", output_path=Path("research/01-auth.md"),
        )
        assert "Documentation Staleness Protocol" in prompt
        assert "[CODE-VERIFIED]" in prompt
        assert "EXIT_RECOMMENDATION: CONTINUE" in prompt
```
- **AC1 (each of 4 builders' prompt contains `config.task_dir / <canonical>` + "do not write elsewhere")**: build with the `config` fixture (test_prompts.py:93-115), then `assert str(config.task_dir / "scope-discovery-raw.md") in prompt` and `assert "do not write" in prompt.lower()` (or the exact instruction string — R1 should supply the canonical wording). The "4 builders" → likely `build_scope_discovery_prompt`, `build_research_notes_prompt`, `build_task_file_prompt`, and one more (confirm via R1). Use `@pytest.mark.parametrize` over (builder, canonical_filename) for compactness — matches the parametrize style already in test_gates.py:107-128.
- **AC2 (`_artifact_path_for_step` dict == `_STEP_ARTIFACT_FILES`)**: this is `_artifact_path_for_step` (net-new) — likely a function mapping step_id→path. Test imports BOTH from executor and asserts key-set / value parity: `assert set(_artifact_path_for_step_keys) == set(_STEP_ARTIFACT_FILES)`. Mirror the direct-equality style of test_executor; no fixture needed. **Confirm the exact net-new symbol name/shape with R2.**

For AC2's "named `test_prompt_executor_mapping_sync`" — file placement: the AC routes it to test_prompts.py, but the symbols (`_artifact_path_for_step`, `_STEP_ARTIFACT_FILES`) live in executor.py. Importing executor internals into test_prompts.py is consistent with the repo's "import privates directly" convention; acceptable.

---

## 6. Gate `_check_*` unit-test template (for AC9)

test_gates.py: `class TestX:` groups, call `_check_foo(content)`, assert `is True` for pass / `isinstance(result, str)` + substring for fail. **Full template (lines 213-228) for AC9:**
```python
class TestCheckNoPlaceholders:
    def test_check_no_placeholders(self) -> None:
        clean = "This is a clean document with proper content throughout."
        assert _check_no_placeholders(clean) is True
        with_todo = "This needs TODO: complete later."
        result = _check_no_placeholders(with_todo)
        assert isinstance(result, str)
        assert "TODO" in result
```
- **AC9 (`_check_no_truncation_marker`)** — net-new gate fn. Mirror exactly: `assert _check_no_truncation_marker("clean full content") is True`; for `"...stuff [TRUNCATED — file exceeds 50KB]"` and trailing `"...content ..."` → `assert isinstance(result, str)` (failure string). Note the existing truncation MARKER text is verified at test_prompts.py:252: `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"` (em-dash `—`) — use the SAME marker string so the gate detects what `_read_file` emits.
- The `_safe_check` wrapper convention (test_gates.py:231-243): crashed checks return error strings; if `_check_no_truncation_marker` is registered as a gate, it must follow the `bool | str` return contract (True=pass, str=failure reason).
- `@pytest.mark.parametrize` shapes (test_gates.py:107-128) are the idiom for testing multiple truncation patterns (`[TRUNCATED`, trailing `...`, mid-`…`) compactly.

---

## 7. E2E pipeline-drive + no-HALT / filesystem assertions (for AC10)

The harness IS section 3 above. Drive = build config (resolve_config + patch task_dir/work_dir) → `PrdExecutor(config)` → patch `_build_prompt` lambda → `result = executor.run()`. Assertions available on `result` (verified in test_e2e.py):
- `result.outcome` ∈ {"success","halt"} — AC10 no-HALT = `== "success"` (line 291); HALT = `== "halt"` (line 558).
- `result.step_results` (list; each `.status.is_terminal`, `.status == PrdStepStatus.SKIPPED|PASS|...`).
- `result.research_agent_count`, `.web_agent_count`, `.synthesis_agent_count`, `.halt_step`, `.halt_reason`, `.resume_command()`, `.suggested_resume_budget`, `.finished_at`.
- Filesystem checks use plain `Path.glob` on tmp dirs (test_e2e.py:484 writes, inventory asserts). For AC10 "no scope-discovery*/research-notes* left in WHERE dir": after `run()`, `assert not list(where_dir.glob("scope-discovery*"))` and `assert not list(where_dir.glob("research-notes*"))`. (Implies recovery MOVES/cleans the variant, not just copies — confirm intended cleanup semantics with R2/R5.)

The existing `_make_passing_output` covers `scope-discovery`(min 50), `research-notes`(100), `build-task-file`(400), assembly(800), etc. — reuse as-is; only inject the variant-file write via a custom factory or `step_overrides` for the targeted step.

---

## 8. conftest.py inventory

- **tests/cli/prd/**: none.
- **tests/conftest.py** (verified, 226 lines): `_pollution_snapshot` (session autouse), `_redirect_reflexion_writes` (autouse, sets `REFLEXION_OUTPUT_DIR`), `sample_context`, `low_confidence_context`, `sample_implementation`, `failing_implementation`, `temp_memory_dir`. `collect_ignore = ["sprint/test_property_based.py"]`. None PRD-specific; the two autouse fixtures fire for PRD tests but are transparent (they only redirect reflexion writes to tmp_path and assert no docs/mistakes pollution).

---

## 9. Invocation & __init__

- `uv run pytest tests/cli/prd/ -q` — VALID. `tests/cli/prd/__init__.py` EXISTS (0 bytes). `tests/cli/__init__.py` — present? Verified `tests/cli/prd/__init__.py` exists; standard collection works (existing files run today). No `pytest.ini`/marker registration needed for these tests (they use no custom markers).

---

## Summary

**Status: Complete.**

The five key files give clean, copy-ready templates for all 10 ACs. The single most important finding: **AC2/AC4/AC9 reference symbols (`_artifact_path_for_step`, `_pick_best_candidate`, `_check_no_truncation_marker`) and WHERE-recovery/INV-005 behavior that DO NOT yet exist in source** — these are red-first acceptance tests the BUILD_REQUEST introduces, authored alongside the R1/R2/R3 implementation, not regressions over existing code. `_resolve_step_content` is currently 3-arg with `build-task-file`/`assembly` glob special-cases and NO WHERE param — AC3's WHERE must be read internally from `parsed-request.json` (flag to R5).

### AC → file → existing-pattern mapping

| AC | Target file | Existing pattern to mirror (file:line) | Notes |
|---|---|---|---|
| AC1 | test_prompts.py | `TestInvestigationPromptStalenessProtocol` (123-139) + `config` fixture (93-115) | substring asserts on `str(config.task_dir/<canonical>)` + "do not write"; parametrize over 4 builders. R1 supplies exact wording. |
| AC2 | test_prompts.py | direct-equality style (test_executor.py:49-59) | net-new `_artifact_path_for_step` vs `_STEP_ARTIFACT_FILES`; assert key/value parity. Import from executor. Confirm symbol w/ R2. |
| AC3 | test_resolve_step_content.py | `test_build_task_file_returns_disk_content_not_ndjson` (25-38) + parsed-request.json setup (test_prompts.py:51-57) | net-new WHERE recovery; assert `len(splitlines())>=50`. |
| AC4 | test_resolve_step_content.py | same template + `os.utime` for mtime | drives net-new `_pick_best_candidate`; fresher task_dir file wins. |
| AC5 | test_resolve_step_content.py | `_isolate_paths` monkeypatch (test_path_resolution.py:32-44) + symlink | INV-005 containment; escaped dir NOT added. |
| AC6 | test_resolve_step_content.py | `test_build_task_file_falls_back_to_ndjson_when_no_match` (76-85) | `result == ndjson_text`, no crash. EXISTING behavior — true regression guard. |
| AC7 | test_executor.py | `test_determine_status_pass` (49-59) + qa_fail (81-87) | CONTINUE→PASS, verdict:FAIL→QA_FAIL from output_text. EXISTING behavior. |
| AC8 | test_executor.py | (no direct existing test of `_persist_step_artifact`) — build from `executor` fixture (27-41) + tmp task_dir | assert canonical-name write + resume disk-probe. New test of mostly-existing fn. |
| AC9 | test_gates.py | `TestCheckNoPlaceholders` (213-228) + parametrize (107-128) | net-new `_check_no_truncation_marker`; use marker `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"` (test_prompts.py:252). |
| AC10 | test_e2e.py | full `@patch` harness + `_mock_process_factory` (224-253) + `test_e2e_full_prd_creation_standard` (261-316) | inject variant-file write in factory; `assert result.outcome=="success"`; `assert not list(where_dir.glob(...))`. |
