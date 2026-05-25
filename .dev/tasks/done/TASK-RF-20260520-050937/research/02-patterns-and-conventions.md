# Research: Patterns & Conventions

**Topic type:** Patterns & Conventions
**Scope:** Python test conventions in `tests/cli/prd/`, edit style for `src/superclaude/cli/prd/`, project-level commands per CLAUDE.md
**Status:** Complete
**Date:** 2026-05-20

---

## Python test file conventions (verified by reading `test_gates.py` and `test_prompts.py`)

- **Module docstring** at line 1, single-line or multi-line, no triple-quoted prose paragraph. Example: `"""Unit tests for superclaude.cli.prd.gates. Section 8.1 test plan: 8 tests."""` (test_gates.py:1-4).
- **Future imports**: `from __future__ import annotations` on the first import line (test_gates.py:6, test_prompts.py:10). Required for forward-reference type hints.
- **Import grouping**: stdlib first, then third-party (pytest), then project (`from superclaude.cli.prd...`). One blank line between groups. Verified at test_gates.py:6-17.
- **No `__all__`, no constants block at the top** in test files — tests jump straight from imports to fixtures/classes.
- **Class-based grouping**: `class TestCheckXxxx:` with a docstring, no inheritance. Tests are methods on the class. Verified at test_gates.py:20 (TestCheckParsedRequestFields), test_gates.py:47 (TestCheckResearchNotesSections), test_gates.py:88 (TestCheckVerdictField).
- **Method signatures**: `def test_xxx(self) -> None:` for fixture-less tests; `def test_xxx(self, fixture_name: PrdConfig) -> None:` with type annotations when fixtures are used.
- **Fixture pattern**: `@pytest.fixture()` decorator (with parentheses), returns a `Path` or domain object. Verified at test_prompts.py:93-115.
- **Assertion style**:
  - Boolean expected: `assert x is True`, `assert x is False` (NOT `assert x` or `assert not x`).
  - String contained in message: `assert "Substring" in result`.
  - Type check: `assert isinstance(result, str)`.
  - All these patterns visible at test_gates.py:27, 41-44, 73, 84-85.
- **Multi-line raw strings** for fixture content: use triple-quoted strings with explicit `\n` only when needed; otherwise raw indent-preserving form. Verified at test_gates.py:51-72.
- **No emoji in test files**.

## Edit style for `src/superclaude/cli/prd/gates.py`

- **Module organization**: `# ---` divider comments mark sections (`Layer 1: Reusable semantic checks`, `Layer 2: PRD-specific semantic checks`, `Safe wrapper`, `Gate Criteria Table`). Verified at gates.py:31-33, 78-80, 244-246, 276-278.
- **Multi-line list literals**: trailing comma on the last element (e.g., `gates.py:108`: `"Suggested Phases",`). Required for ruff format compliance — DO NOT remove the trailing comma when rewriting the list.
- **Module-level constants in `_UPPER_SNAKE_CASE` with leading underscore for module-private**. The constant `_RESEARCH_REQUIRED_SECTIONS` follows this. Same pattern in `_PRD_CRITICAL_SECTIONS` at gates.py:215.
- **Regex compilation style**: inline `re.compile(rf"...", re.MULTILINE | re.IGNORECASE)` inside the consuming function — not module-level constants. Verified at gates.py:118-121 and 129-138.
- **`re.escape(section)`** is used inside f-string regex patterns to safely include user-provided section names — preserves literal-character safety. The change at line 134-138 does NOT touch the `re.escape` pattern; it touches a hand-written regex that has no `re.escape` (this is the regex with the underscore bug).
- **Double quotes** preferred over single quotes throughout.
- **No type stubs on private helpers** — `_check_xxxx(content: str) -> bool | str` is the canonical signature for semantic checks (gates.py:21 NFR-PRD.2).

## Project-level commands (from CLAUDE.md)

- **All Python operations use UV**:
  - Tests: `uv run pytest tests/cli/prd/ -v`
  - Single file: `uv run pytest tests/cli/prd/test_gates.py -v`
  - Coverage: `uv run pytest --cov=superclaude`
  - Marker: `uv run pytest -m confidence_check`
- **Make targets**:
  - `make test` — full test suite
  - `make lint` — ruff linter
  - `make format` — ruff format
  - `make verify-sync` — confirm `src/superclaude/` matches `.claude/` (NOT relevant here — we're not editing skill/agent/command files; gates.py is non-distributable Python).
- **Editable install**: edits to `src/superclaude/` take effect on next invocation. **Do NOT run `pip install -e` or `make dev` mid-task.**
- **Branch policy**: feature branches only; never commit directly to master/main (the user has not asked for a commit; the task file should END before any git operation unless explicitly requested).

## Failure modes to avoid when applying these edits

- **`Edit` tool semantics**: requires the file to have been Read at least once in the conversation. The execution side of this task file (run by `/task`) will need to Read `gates.py` and `test_gates.py` before editing. The Edit tool errors if `old_string` is not unique — for both edits in `gates.py`, the surrounding context is unambiguous because of the unique constant name and unique regex pattern. The test_gates.py edit's `old_string` is also unique (class name + first method body is distinctive). No ambiguity risk for any of the 4 edits.
- **Whitespace/indent preservation**: when rewriting `test_check_research_notes_sections`, preserve the exact indent of the triple-quoted string content (the content sits at column 0, NOT indented under the function — verified at test_gates.py:51-72).
- **Trailing commas**: keep them on multi-line list literals.
- **No accidental `**Suggested Phases**` bold-form heading**: the consuming check (`_check_research_notes_sections` regex `bold_pat` on gates.py:121) also matches `**SUGGESTED_PHASES**` bold form, so a future agent emitting bold-style won't break the gate. No action needed; documented for awareness.

## Summary

- Use class-based pytest patterns with `def test_xxx(self) -> None:` signatures and `assert X is True` / `assert "substring" in result` assertions.
- Preserve trailing commas in multi-line list literals when rewriting `_RESEARCH_REQUIRED_SECTIONS`.
- Use `uv run pytest tests/cli/prd/ -v` for verification — never bare `pytest` or `python -m pytest`.
- Use `make lint` for the lint gate.
- Editable install — no rebuild step required between edits and verification.
