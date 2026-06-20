# Research 03: Test & Verification Patterns for M1 + M2 Unit Tests

**Status: Complete**

**Scope:**
- `/config/workspace/IronClaude/tests/roadmap/test_cosmetic_remediator.py` (357 lines)
- `/config/workspace/IronClaude/tests/roadmap/test_executor.py` (1162 lines)
- Reference patterns: `/config/workspace/IronClaude/tests/pipeline/test_executor.py`, `tests/pipeline/test_gates.py`

**Goal:** Identify existing conventions to author two new tests:
- M1: fenced-block helper test (cosmetic_remediator)
- M2: Remediator exception swallowed → executor still FAILs with original gate reason (executor)

---

## Part A — `test_cosmetic_remediator.py` (M1)

### A.1 Import block (verbatim, lines 1-14)

```python
"""Unit tests for the cosmetic-failure auto-remediation lane.

Covers the classifier (cosmetic vs semantic) and the deterministic transforms
(C1-C10) defined in superclaude.cli.roadmap.cosmetic_remediator. Every test
is hermetic -- markdown is built inline, no fixture files required.
"""

from __future__ import annotations

from superclaude.cli.roadmap.cosmetic_remediator import (
    Classification,
    apply_cosmetic_remediations,
    classify_gate_failure,
)
```

What's already imported (`test_cosmetic_remediator.py:10-14`):
- `Classification` (the dataclass)
- `apply_cosmetic_remediations`
- `classify_gate_failure`

**What the new M1 test needs:** Import the fenced-block helper from the same module. The current source-side helper is `_is_in_fenced_block(lines, idx) -> bool` at `src/superclaude/cli/roadmap/cosmetic_remediator.py:204-210`. The task narrative refers to a new `_compute_fenced_indices(lines) -> set[int]` introduced by the M1 fix. The new test will add a single underscore-prefixed import — keep the existing tuple import shape:

```python
from superclaude.cli.roadmap.cosmetic_remediator import (
    Classification,
    _compute_fenced_indices,   # NEW (added by the M1 fix)
    apply_cosmetic_remediations,
    classify_gate_failure,
)
```

Note: M1 source-side researcher will confirm exact symbol name. If it stays `_is_in_fenced_block` plus a new `_compute_fenced_indices`, both can be imported. If the fix keeps only `_is_in_fenced_block` but caches via tuple-arg memoization, the test still imports `_is_in_fenced_block` and asserts membership by calling it across all indices.

### A.2 Module-level helpers (signature + usage)

Only one helper at module level: `_content_with_milestone` at `test_cosmetic_remediator.py:21-37`.

**Signature (lines 21-27):**
```python
def _content_with_milestone(
    subsections: list[str],
    *,
    mid: str = "1",
    frontmatter: str = "---\nspec_source: epics.md\n---\n",
    extras: str = "",
) -> str:
    """Assemble a minimal roadmap-ish markdown with one milestone."""
```

**3-line example of call inside a test (`test_cosmetic_remediator.py:99-105`):**
```python
content = _content_with_milestone(
    [
        "### Integration Points -- M1",
        "### Milestone Dependencies -- M1",
        "### Risk Assessment",  # alias, no suffix either
    ]
)
```

Also a module-level constant at `test_cosmetic_remediator.py:40`:
```python
_GATE = "template_sections_present"
```

### A.3 Representative existing test (full body) — `test_c1_stem_alias_classified_and_fixed`

`test_cosmetic_remediator.py:97-110` (full body, 14 lines including signature):

```python
def test_c1_stem_alias_classified_and_fixed(self):
    # "Risk Assessment" instead of "Risk Assessment and Mitigation"
    content = _content_with_milestone(
        [
            "### Integration Points -- M1",
            "### Milestone Dependencies -- M1",
            "### Risk Assessment",  # alias, no suffix either
        ]
    )
    cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
    assert cl.is_pure_cosmetic is True
    new, transforms = apply_cosmetic_remediations(content, cl)
    assert "### Risk Assessment and Mitigation -- M1" in new
    assert any("Risk Assessment and Mitigation" in t for t in transforms)
```

**Assertion idiom:** inline `is True`/`is False` for booleans, `in` for substring membership, and `any(...)` over a transforms list for fuzzy matching. No `pytest.raises`, no parametrize, no fixtures. Tests are method on a `TestX` class with one classifier call and one apply call.

### A.4 Recommended test name + sketched body (M1)

**Name suggestion:** `TestFencedBlockHelper::test_fenced_indices_excludes_delimiters` (or as a module-level free function `test_fenced_indices_helper_marks_inside_lines_only` if no class is desired — both class-based and the bare function don't currently exist for helpers, but the class style matches the rest of this file).

**Per spec the test must assert:** `_compute_fenced_indices(lines)` returns a set containing all in-fence line indices and excluding the fence-delimiter lines themselves.

**Sketched body — minimal markdown with 3-4 fenced regions:**

```python
class TestFencedBlockHelper:
    def test_compute_fenced_indices_excludes_delimiters(self):
        # Indices: 0  1            2          3  4
        #         5  6 7
        #         8  9            10         11 12 13 14
        #         15 16           17         18
        markdown = "\n".join([
            "para before",            # 0  outside
            "```",                    # 1  fence open (excluded)
            "code line A",            # 2  inside
            "```",                    # 3  fence close (excluded)
            "between fences",         # 4  outside
            "```python",              # 5  fence open (excluded)
            "x = 1",                  # 6  inside
            "```",                    # 7  fence close (excluded)
            "more text",              # 8  outside
            "```",                    # 9  fence open (excluded)
            "looks ``` nested",       # 10 inside (literal backticks inside body)
            "still inside",           # 11 inside
            "and inside",             # 12 inside
            "```",                    # 13 fence close (excluded)
            "tail line",              # 14 outside
            "```",                    # 15 fence open (excluded)
            "single-line body",       # 16 inside
            "```",                    # 17 fence close (excluded)
            "after",                  # 18 outside
        ])
        lines = markdown.splitlines()
        inside = _compute_fenced_indices(lines)

        # In-fence lines included
        for idx in (2, 6, 10, 11, 12, 16):
            assert idx in inside, f"line {idx} should be inside a fence"

        # Fence delimiter lines themselves excluded
        for idx in (1, 3, 5, 7, 9, 13, 15, 17):
            assert idx not in inside, f"line {idx} is a delimiter, must be excluded"

        # Outside-of-any-fence lines excluded
        for idx in (0, 4, 8, 14, 18):
            assert idx not in inside, f"line {idx} is outside, must be excluded"
```

**Why this design satisfies the M1 spec:**
- 4 fenced regions (matches "3-4 fenced regions").
- Includes content before, between, and after fences ("content before/after fences").
- Region 3 includes a line whose body contains literal ` ``` ` characters but does not start with the fence — that's the "nested-looking content" check (the helper at `cosmetic_remediator.py:208` keys off `lstrip().startswith("```")` so a line where ``` appears mid-line is not treated as a fence).
- The minimal-region check (lines 15-17) catches off-by-one bugs where an "open + immediate close" might leak.

**If the imported symbol is `_is_in_fenced_block` (current API, no new helper added):** replace `_compute_fenced_indices(lines)` with a comprehension and adjust:
```python
inside = {idx for idx in range(len(lines)) if _is_in_fenced_block(lines, idx)}
```
The assertion shape is unchanged.

---

## Part B — `test_executor.py` (M2)

### B.1 Existing pattern: construct a `Step` with a failing gate and run a single iteration

The most directly representative pattern is **not** in `tests/roadmap/test_executor.py` (which has no per-step failing-gate fixtures — only full-pipeline tests via `failing_runner` at `tests/roadmap/test_executor.py:296-323`). The cleanest single-step-failing-gate pattern lives in `tests/pipeline/test_executor.py:91-110`:

```python
class TestRetryLogic:
    def test_retry_on_gate_failure(self, tmp_path):
        cfg = PipelineConfig(work_dir=tmp_path)
        gate = GateCriteria(required_frontmatter_fields=["title"], min_lines=5)
        step = Step(
            id="s1",
            prompt="p",
            output_file=tmp_path / "missing.md",
            gate=gate,
            timeout_seconds=60,
            retry_limit=1,
        )

        runner, calls = _make_runner(write_output=False)
        results = execute_pipeline(steps=[step], config=cfg, run_step=runner)
        assert len(results) == 1
        assert results[0].status == StepStatus.FAIL
        assert results[0].attempt == 2  # tried twice
        assert "File not found" in results[0].gate_failure_reason
        assert calls == ["s1", "s1"]  # called twice
```

Helper `_make_runner` is defined in the same file (`tests/pipeline/test_executor.py:21-40`):
```python
def _make_runner(write_output=True, status=StepStatus.PASS):
    """Create a mock StepRunner that optionally writes output files."""
    calls = []

    def runner(step, config, cancel_check):
        calls.append(step.id)
        if write_output and step.gate is not None:
            step.output_file.write_text(
                "---\ntitle: T\nversion: 1.0\n---\n" + "\n".join(["line"] * 20)
            )
        return StepResult(
            step=step,
            status=status,
            attempt=1,
            gate_failure_reason=None,
            started_at=_now(),
            finished_at=_now(),
        )

    return runner, calls
```

**Note for M2 placement:** The cosmetic-remediation block is inside `pipeline/executor.py`, so the natural home for an M2 test is `tests/pipeline/test_executor.py`, not `tests/roadmap/test_executor.py`. The task asks for both, but no roadmap-executor tests touch `cosmetic_remediator=` today (confirmed by `grep -rn cosmetic_remediator tests/` → only matches in `tests/roadmap/test_cosmetic_remediator.py`). **Recommendation:** add the M2 test in `tests/pipeline/test_executor.py` next to the other `execute_pipeline`-based tests; if the task requires it in `tests/roadmap/test_executor.py`, mirror the pattern from `tests/pipeline/test_executor.py:91-110` and import `GateCriteria`/`SemanticCheck`/`PipelineConfig` from `superclaude.cli.pipeline.models`.

### B.2 Pattern for injecting test-double remediators into `PipelineConfig.cosmetic_remediator`

**No existing test does this** — `grep -rn "cosmetic_remediator\|allow_cosmetic_remediation" tests/` returns matches only inside `tests/roadmap/test_cosmetic_remediator.py` (the docstring + import). The M2 test will be the first to exercise the `PipelineConfig.cosmetic_remediator` plug-point.

The field signatures from `src/superclaude/cli/pipeline/models.py:230-234`:
```python
allow_cosmetic_remediation: bool = True
cosmetic_remediator: Optional[CosmeticRemediator] = None
```
And the executor calls it at `src/superclaude/cli/pipeline/executor.py:309-314`:
```python
remediated_ok, transforms = config.cosmetic_remediator(
    gate_target,
    gate_name,
    reason or "",
    step_id=step.id,
)
```
So the test double signature must be `(path: Path, gate_name: str, reason: str, *, step_id: str) -> tuple[bool, list[str]]`.

**Recommended injection idiom (modeled on the project's plain-function-as-callable style):**
```python
def boom_remediator(_path, _gate_name, _reason, *, step_id):
    raise RuntimeError("test: remediator exploded")

cfg = PipelineConfig(
    work_dir=tmp_path,
    allow_cosmetic_remediation=True,
    cosmetic_remediator=boom_remediator,
)
```

### B.3 `caplog` usage in `tests/roadmap/test_executor.py`

`grep -n caplog` against `tests/roadmap/test_executor.py` yields **one** usage in the file: `TestT1bConsistencyCheck::test_pure_unclassified_registry_passes_check` at `tests/roadmap/test_executor.py:1126` and `:1156-1162`. Full snippet:

```python
def test_pure_unclassified_registry_passes_check(self, tmp_path, caplog):
    ...
    import logging

    with caplog.at_level(logging.WARNING, logger="superclaude.roadmap.executor"):
        res = _run_deviation_analysis(step, config, _now())
    assert res.status.value == "PASS"
    assert not any(
        "cross-field consistency check failed" in record.getMessage()
        for record in caplog.records
    ), "T1b: pure-UNCLASSIFIED registry must not trip the consistency check"
```

**Key idiom:**
- Inject `caplog` as a fixture argument.
- `import logging` inside the test method.
- Scope with `with caplog.at_level(logging.WARNING, logger="<full-dotted-logger-name>")`.
- Iterate `caplog.records` (each is a `LogRecord`) and use `record.getMessage()`.

**Pipeline-executor logger name (verified at `src/superclaude/cli/pipeline/executor.py:38`):**
```python
_log = logging.getLogger("superclaude.pipeline.executor")
```
So the M2 caplog scope is `logger="superclaude.pipeline.executor"` (NOT `superclaude.roadmap.executor`).

### B.4 Minimal `PipelineConfig` with `allow_cosmetic_remediation=True` + failing `semantic_checks`

No existing test wires this exact combination (see B.2). Closest patterns:

- `PipelineConfig(work_dir=tmp_path)` — `tests/pipeline/test_executor.py:45`. `allow_cosmetic_remediation` defaults to `True` (`pipeline/models.py:233`), so passing nothing explicit is sufficient for the flag; only `cosmetic_remediator` must be assigned.
- `GateCriteria` with `semantic_checks=[SemanticCheck(...)]` — `tests/pipeline/test_gates.py:117-137`:

```python
gc = GateCriteria(
    required_frontmatter_fields=["title"],
    min_lines=3,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="has_heading",
            check_fn=lambda c: "# " in c,
            failure_message="No heading found",
        )
    ],
)
```

Combine the two for M2 — the runner writes an output file that satisfies frontmatter/min-lines but fails `semantic_checks` (so the executor enters the cosmetic-remediation branch at `pipeline/executor.py:286-290` because `step.gate.semantic_checks` is non-empty and `gate_name` is populated at L302).

### B.5 Recommended test name + sketched body (M2)

**Name suggestion:** `TestCosmeticRemediation::test_remediator_exception_falls_through_to_fail_with_original_reason`
(File: `tests/pipeline/test_executor.py` — new class at the end.)

**Skeleton:**

```python
import logging

from superclaude.cli.pipeline.executor import execute_pipeline
from superclaude.cli.pipeline.models import (
    GateCriteria,
    PipelineConfig,
    SemanticCheck,
    Step,
    StepResult,
    StepStatus,
)


class TestCosmeticRemediation:
    def test_remediator_exception_falls_through_to_fail_with_original_reason(
        self, tmp_path, caplog
    ):
        # Runner writes output that PASSES frontmatter/min-lines but FAILS
        # the semantic_check; that drives the executor into the cosmetic
        # remediation branch.
        def runner(step, config, cancel_check):
            step.output_file.write_text(
                "---\ntitle: T\n---\n" + "\n".join(["body"] * 10)
            )
            return StepResult(
                step=step,
                status=StepStatus.PASS,
                attempt=1,
                gate_failure_reason=None,
                started_at=_now(),
                finished_at=_now(),
            )

        def boom_remediator(_path, _gate_name, _reason, *, step_id):
            raise RuntimeError("simulated remediator crash")

        gate = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STRICT",
            semantic_checks=[
                SemanticCheck(
                    name="has_heading",
                    check_fn=lambda c: "# " in c,           # body has no "# "
                    failure_message="No heading found",
                )
            ],
        )
        step = Step(
            id="s_boom",
            prompt="p",
            output_file=tmp_path / "out.md",
            gate=gate,
            timeout_seconds=60,
            retry_limit=0,           # no retry -> single iteration
        )
        cfg = PipelineConfig(
            work_dir=tmp_path,
            allow_cosmetic_remediation=True,
            cosmetic_remediator=boom_remediator,
        )

        with caplog.at_level(
            logging.WARNING, logger="superclaude.pipeline.executor"
        ):
            results = execute_pipeline(steps=[step], config=cfg, run_step=runner)

        assert len(results) == 1
        r = results[0]
        # M2 contract: remediator exception is swallowed, executor still FAILs
        # using the ORIGINAL gate-failure reason (not the exception text).
        assert r.status == StepStatus.FAIL
        assert r.gate_failure_reason, "gate_failure_reason must not be empty"
        assert "has_heading" in r.gate_failure_reason or \
               "No heading found" in r.gate_failure_reason
        assert "simulated remediator crash" not in (r.gate_failure_reason or "")
        # Optional: WARNING captured with the exception class name.
        assert any(
            "RuntimeError" in rec.getMessage() for rec in caplog.records
        ), "expected a WARNING mentioning the swallowed exception class"
```

**Why this satisfies the M2 contract from the task:**
- Forces a non-empty `gate_name` so the cosmetic branch is reached (`pipeline/executor.py:286-307`).
- The injected remediator raises before returning — exercising the try/except the M2 fix adds around `pipeline/executor.py:309-341`.
- `r.status == StepStatus.FAIL` and `r.gate_failure_reason` carrying the ORIGINAL `reason` are exactly what the FAIL fall-through at `pipeline/executor.py:355-363` produces.
- The optional `caplog` assertion only fires when the M2 fix's `_log.warning(...)` includes the exception class (a reasonable convention given `_log = logging.getLogger("superclaude.pipeline.executor")` at L38). If the fix logs the exception with `exc_info=True`, the same assertion still passes because the formatted traceback contains `RuntimeError`. If we want stricter coupling-free coverage, drop the caplog assertion and rely on the FAIL + original-reason assertions alone.

---

## Summary

1. **M1 test belongs in** `tests/roadmap/test_cosmetic_remediator.py`, follows the `TestX` class style + inline-markdown idiom, adds one underscore-prefixed import, and uses the multi-fence sample above to assert delimiters are excluded and inside-content is included.
2. **M2 test belongs in** `tests/pipeline/test_executor.py` (no existing roadmap-side test wires `PipelineConfig.cosmetic_remediator`), models its construction on `TestRetryLogic.test_retry_on_gate_failure` (`tests/pipeline/test_executor.py:91-110`) + `TestStrictTier.test_semantic_check_fails` (`tests/pipeline/test_gates.py:117-137`), and uses the existing `caplog` idiom from `tests/roadmap/test_executor.py:1126,1156-1162` with logger name `"superclaude.pipeline.executor"` (verified at `src/superclaude/cli/pipeline/executor.py:38`).
3. **No `cosmetic_remediator=` injection precedent exists**; the M2 test will be the first — sig per `pipeline/executor.py:309-314` is `(path, gate_name, reason, *, step_id) -> tuple[bool, list[str]]`.
