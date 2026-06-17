# Patterns & Conventions + Test Verification

Status: Complete

## Scope

- Source under review: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py`
- Test file under review: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py`
- Topic: `_check_verdict_field` markdown/JSON regex behavior, accepted/rejected test conventions, missing edge cases, and validation commands.

## Current verdict regex behavior

### JSON verdicts

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:43-46` accepts JSON-shaped verdicts with exactly uppercase `PASS` or `FAIL` via `"verdict"\s*:\s*"(PASS|FAIL)"`.
- The JSON key is lowercase-only in the current regex at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:44`; the markdown key is case-insensitive, but JSON key matching is not.

### Markdown verdicts

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:47-60` documents the intended markdown behavior: accept decorated verdict lines, keep the colon required, reject repeated colons, reject lowercase values, and reject `PASSING` / `FAILURE` by word boundary.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:61-64` implements the current markdown regex:

```python
r"(?:^|\n)[^\w\n:]*(?i:verdict)[^\w\n:]*:[^\w\n:]*(PASS|FAIL)(?!\w)"
```

- Consequence: only non-word, non-colon decoration is allowed before `Verdict`, between `Verdict` and the colon, and between the colon and `PASS|FAIL`.
- Because Python treats `_` and digits as word characters, the current regex rejects underscore emphasis (`_Verdict_: PASS`, `__Verdict__: PASS`, `Verdict: __PASS__`) and numbered-list prefixes (`1. Verdict: PASS`, `1. **Verdict:** PASS`). This was confirmed by direct `uv run python -c ...` probing.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:65-67` returns `True` on a markdown match, otherwise the error string `No verdict field found (expected 'verdict: PASS' or 'verdict: FAIL')`.

### Gate usage

- `_check_qa_verdict` delegates directly to `_check_verdict_field` at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:296-298`.
- The reusable verdict check is wired into `sufficiency-review` at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:402-413`.
- It is also wired into `verify-task-file` at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:455-466`.
- QA verdict delegation is used for `research-qa`, `synthesis-qa`, `structural-qa`, and `qualitative-qa` at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:480-491`, `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:505-516`, `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:542-553`, and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:555-566`.

## Existing test conventions

### Organization and style

- Tests import private gate helpers directly at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:10-20`.
- Verdict-specific tests live in `class TestCheckVerdictField` at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:91-159`.
- The file uses simple `assert _check_...(...) is True` for accepted cases and `assert result is not True` or `isinstance(result, str)` for rejected/error cases, e.g. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:94-106` and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:130-135`.
- Parametrized shape lists are the established convention for grouped verdict regex cases at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:108-117`, `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:119-135`, and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:137-153`.

### Existing accepted verdict cases

- Basic JSON and markdown accepted cases are covered at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:94-102`.
- Three basic markdown shapes are parameterized at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:108-117`: `Verdict: PASS`, `**Verdict**: PASS`, and `**Verdict:** PASS`.
- Decorated markdown shapes are parameterized at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:137-153`, including bullet prefix, heading prefix, emoji before value, bold-wrapped `PASS`, and uppercase `VERDICT`.

### Existing rejected verdict cases

- Missing verdict text is tested at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:103-106`.
- Malformed shapes are parameterized at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:119-135`: no colon, repeated colons, junk separator, lowercase no-colon shape, `PASSING`, and `FAILURE`.
- A rationale heading without a `PASS|FAIL` value is rejected at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:155-158`.

## Exact edge cases to add

Add these in `TestCheckVerdictField`, following the existing `@pytest.mark.parametrize("shape", [...])` convention.

### New accepted cases

These should become accepted after implementation:

```python
@pytest.mark.parametrize(
    "shape",
    [
        "1. Verdict: PASS",
        "1. **Verdict:** PASS",
        "10. __Verdict__: FAIL",
        "_Verdict_: PASS",
        "__Verdict__: FAIL",
        "Verdict: _PASS_",
        "Verdict: __FAIL__",
        "1. __Verdict__: ✅ __PASS__",
    ],
)
def test_check_verdict_field_accepts_numbered_and_underscore_emphasis(
    self, shape: str
) -> None:
    content = f"## QA Report\n\n{shape}\n\nRationale follows.\n"
    assert _check_verdict_field(content) is True
```

Rationale:

- `1. Verdict: PASS` and `1. **Verdict:** PASS` lock numbered-list support.
- `10. __Verdict__: FAIL` prevents a single-digit-only implementation.
- `_Verdict_: PASS` and `__Verdict__: FAIL` lock underscore emphasis around the label.
- `Verdict: _PASS_` and `Verdict: __FAIL__` lock underscore emphasis around the value.
- `1. __Verdict__: ✅ __PASS__` combines numbered list, underscore label emphasis, emoji decoration, and underscore value emphasis.

### Rejected cases that must stay rejected

Keep or add these regression cases to preserve colon/value strictness:

```python
@pytest.mark.parametrize(
    "shape",
    [
        "1. Verdict PASS",
        "1. Verdict::: PASS",
        "1. Verdict: PASSING",
        "1. Verdict: pass",
        "__Verdict__ PASS",
        "__Verdict__::: FAIL",
        "Verdict: _PASSING_",
        "Verdict: __FAILURE__",
    ],
)
def test_check_verdict_field_rejects_numbered_and_underscore_malformed_shapes(
    self, shape: str
) -> None:
    content = f"## QA Report\n\n{shape}\n\nDetails follow.\n"
    result = _check_verdict_field(content)
    assert result is not True
```

Rationale:

- Numbered-list support must not make the colon optional.
- Underscore emphasis support must not allow missing or repeated separators.
- Value matching must remain exactly uppercase `PASS` or `FAIL`, allowing emphasis/decor around the token but not lowercase, `PASSING`, or `FAILURE`.

## Proposed implementation constraints

Implementation should be narrow and preserve the current strictness documented in `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:47-60`.

Required behavior:

1. Accept current JSON verdicts unchanged.
2. Accept current markdown/bold/bullet/heading/emoji cases unchanged.
3. Add support for numbered-list prefixes before the verdict label, e.g. `1. Verdict: PASS` and `10. **Verdict:** FAIL`.
4. Add support for underscore emphasis around the label and value, e.g. `_Verdict_: PASS`, `__Verdict__: FAIL`, `Verdict: _PASS_`, and `Verdict: __FAIL__`.
5. Preserve colon strictness: reject `Verdict PASS`, `1. Verdict PASS`, `Verdict::: PASS`, and `1. Verdict::: PASS`.
6. Preserve value strictness: reject lowercase `pass`, `PASSING`, `FAILURE`, `_PASSING_`, and `__FAILURE__`.
7. Keep the match line-anchored so `PASS` buried in prose does not satisfy the gate.
8. Avoid broadening decoration to arbitrary word characters; only the specific new forms needed for numbered-list prefixes and underscore emphasis should be allowed.

## Validation already run

From repository root `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473`:

```bash
uv run pytest tests/cli/prd/test_gates.py -q
```

Result: `37 passed in 0.17s`.

Direct probe command used for missing edge cases:

```bash
uv run python -c "from superclaude.cli.prd.gates import _check_verdict_field; cases=['1. **Verdict:** PASS','1. Verdict: PASS','__Verdict__: PASS','_Verdict_: PASS','Verdict: __PASS__','Verdict: _PASS_','Verdict PASS','Verdict::: PASS','Verdict: PASSING','Verdict: pass']; [print(repr(c), '=>', _check_verdict_field(c)) for c in cases]"
```

Observed current behavior: all probed numbered-list and underscore-emphasis cases currently return `No verdict field found (expected 'verdict: PASS' or 'verdict: FAIL')`; malformed strictness cases also return that error.

## Exact UV validation commands for implementer

Run these from `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473` after updating source and tests:

```bash
uv run pytest tests/cli/prd/test_gates.py -q
```

```bash
uv run pytest tests/cli/prd/test_gates.py::TestCheckVerdictField -q
```

Optional broader regression check for PRD CLI tests:

```bash
uv run pytest tests/cli/prd/ -q
```

If Python formatting/lint changes are made, also run:

```bash
uv run ruff format --check src/ tests/
```

```bash
make lint
```

## Evidence artifact coverage

- `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/tier1-observation.md` provides the canonical reproducer output for this task and should be treated as read-only evidence for the failing numbered-list and underscore-emphasis shapes.
- `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/evidence-validation.md` confirms the report's local citations survived validation; the task does not need to re-validate those citations, but it must validate the actual code change with pytest/ruff after editing.

## Summary

The current tests are stable and the missing coverage is precise: add accepted cases for numbered-list prefixes and underscore emphasis around the verdict label/value, and optionally add malformed variants to prevent over-broad regex matching. The implementation should keep JSON behavior unchanged, keep markdown matching line-anchored, and preserve strict colon plus exact uppercase `PASS|FAIL` semantics.
