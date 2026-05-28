# Research: Patterns & Conventions (integration_contracts.py at PR sha 67ab0af5)
**Topic type:** Patterns & Conventions
**Scope:** integration_contracts.py + a representative test class
**Status:** Complete
**Date:** 2026-05-26
---

## 1. Docstring Style for Private Helpers

All private helpers use **triple-quoted docstrings with a leading summary line** as the first statement of the function body. They are **short (1–3 lines)**, written as **freeform prose** (no `Args:` / `Returns:` blocks), and **cite FR-MOD2.X references inline** when the helper implements a numbered requirement.

### Evidence — `_classify_mechanism` (git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py, line 382)

```python
def _classify_mechanism(matched_text: str) -> str:
    """Classify matched text into a mechanism category."""
    lower = matched_text.lower()
```

Single-line summary docstring. No FR cite. No `Args:`/`Returns:` block.

### Evidence — `_extract_identifiers` (line 412)

```python
def _extract_identifiers(text: str) -> list[str]:
    """Extract UPPER_SNAKE_CASE and PascalCase identifiers from text.

    FR-MOD2.4: Named mechanism identifier matching.
    """
    # UPPER_SNAKE_CASE (likely constants/tables)
    upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
```

Summary line + blank line + FR-MOD2.X cite as freeform prose. Total 4 lines including closing `"""`.

### Evidence — `_signature_subsumed` (line 424)

```python
def _signature_subsumed(
    sig: tuple[str, frozenset[str]],
    seen: dict[tuple[str, frozenset[str]], int],
) -> bool:
    """Subsume sig if same mechanism AND identifier-set ⊆ an existing one
    that shares ≥1 identifier. Empty-identifier signatures dedup by exact
    match only (preserves test_duplicate_lines_deduplicated)."""
    mech, idents = sig
```

Three-line prose docstring, no `Args:`/`Returns:`, references a test name inline. No blank-line separation between summary and continuation.

### Public-function contrast (for reference)

Public functions like `extract_integration_contracts` (line 166) and `check_roadmap_coverage` (line 221) DO use multi-line docstrings with FR-MOD2.X bullets and an explicit "Returns" prose sentence, but **still no `Args:`/`Returns:` Sphinx/Google blocks** — pure freeform prose.

### Recommendation for `_canonicalize_identifiers`

Triple-quoted docstring; 1-line summary OR (summary + blank + FR-MOD2.X cite). No `Args:`/`Returns:` block. Cite the relevant FR if PR A's helper implements a numbered requirement.

---

## 2. Regex Compilation Pattern

**Pre-compile at module scope** is the dominant pattern; **inline `re.findall` / `re.compile` inside function bodies** is used only when the pattern is helper-local. Flags are passed as the **second positional argument** (`re.IGNORECASE`), never inline `(?i)`. Multi-line regexes use **string concatenation across lines** inside `re.compile(...)`.

### Evidence — module-scope pre-compilation (lines 20–82, `DISPATCH_PATTERNS`)

```python
DISPATCH_PATTERNS = [
    # Category 1: Dict dispatch tables
    re.compile(
        r"\b(?:dispatch[_\s]?table|DISPATCH_TABLE|PROGRAMMATIC_RUNNERS|"
        r"RUNNERS|_RUNNERS|HANDLERS|"
        r"routing[_\s]?table|command[_\s]?map|step[_\s]?map|"
        r"plugin[_\s]?registry|"
        ...
        r")\b",
        re.IGNORECASE,
    ),
```

- Pre-compiled into module-level list constant.
- Multi-line raw-string literals (`r"..."`) concatenated across physical lines.
- `re.IGNORECASE` as positional second arg, on its own line.
- Inline comments above each `re.compile(...)` describing the category.

### Evidence — function-local pre-compilation (lines 293–306, inside `check_roadmap_coverage`)

```python
dispatch_family = re.compile(
    r"\b(?:[a-z]+-)?(?:class-priority|named-theme|"
    r"role-keyed|theme|severity-keyed|module-tier|subprocess|gRPC)"
    r"[\s_-]?dispatch(?:\s+table)?\b",
    re.IGNORECASE,
)

impl_verbs = re.compile(
    r"\b(?:implement|configure|add|create|set\s*up|deploy|"
    r"build|integrate|wire|enable|install|bound|attach|"
    r"apply|use|route|log|emit|handle|populate)\b",
    re.IGNORECASE,
)
```

When a regex is only used within one function, it's compiled inline at the top of that function's logical block — still with the multi-line concatenation style and trailing `re.IGNORECASE` arg.

### Evidence — inline `re.findall` (lines 417–420, `_extract_identifiers` body)

```python
# UPPER_SNAKE_CASE (likely constants/tables)
upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
# PascalCase class names
pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
```

For simple one-shot pattern matches with **no flags needed**, inline `re.findall(pattern, text)` is acceptable. Comment above each line explaining what's matched.

### Recommendation for `_canonicalize_identifiers`

If the helper uses regexes that benefit from compilation and are reused across calls, pre-compile at module scope above the helper. If single-use simple ASCII matching, inline `re.findall` is the established idiom. Always trailing-positional `re.IGNORECASE`.

---

## 3. Private-Helper Naming Convention

**`_<lowercase_snake>`** is the consistent convention. All three existing private helpers follow this exactly.

### Full list of `def _` declarations in the file

| Line | Declaration |
|------|-------------|
| 382  | `def _classify_mechanism(matched_text: str) -> str:` |
| 412  | `def _extract_identifiers(text: str) -> list[str]:` |
| 424  | `def _signature_subsumed(` |

(Search performed via `git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py | grep -n '^def _'`.)

The "Internal helpers" section is delimited by the comment `# --- Internal helpers ---` (line 379) at the **end** of the file. New helpers should be appended within this section, after `_signature_subsumed`.

### Recommendation for `_canonicalize_identifiers`

Name matches convention. Append definition after `_signature_subsumed` (under the `# --- Internal helpers ---` banner).

---

## 4. Test Naming Convention

Test classes use **PascalCase `Test<FeatureName>`** with a one-line docstring citing FR-MOD2.X. Test methods use **`test_<lowercase_snake>`** with no docstrings, just inline assertions on real fixtures (no mocks).

### Evidence — representative class signature (git show 67ab0af5:tests/roadmap/test_integration_contracts.py)

```python
class TestDispatchPatternDetection:
    """FR-MOD2.1: 7-category dispatch pattern detection."""

    def test_category1_dispatch_table(self):
        contracts = extract_integration_contracts(DISPATCH_TABLE_SPEC)
        assert len(contracts) >= 1
```

- Class: `TestDispatchPatternDetection` — PascalCase, `Test` prefix, no `unittest.TestCase` inheritance (pytest style).
- Docstring: single line citing FR-MOD2.X.
- Methods: `test_category1_dispatch_table` (snake_case, `test_` prefix), no docstring.
- Fixtures are **module-level string constants** (e.g., `DISPATCH_TABLE_SPEC`, `BAD_ROADMAP`, `TUIBBS_HUB_SPEC`) — no `@pytest.fixture` decorators. The module docstring states "All tests use real content fixtures, no mocks."

### Recommendation for `_canonicalize_identifiers` tests

If PR A adds tests, group them in a new pytest class `TestCanonicalizeIdentifiers` (or extend an existing class if scope-adjacent), with module-level string fixtures and snake_case `test_<scenario>` methods.

---

## 5. Type Hint Convention

**Modern PEP 585 / PEP 604 syntax** — `list[str]`, `frozenset[str]`, `dict[K, V]`, `tuple[str, frozenset[str]]`. NO `typing.List` / `typing.FrozenSet` / `typing.Dict` imports. Enabled by `from __future__ import annotations` (line 13).

### Evidence

- Line 13: `from __future__ import annotations`
- Line 132: `mechanism_signature: tuple[str, frozenset[str]] = field(...)`
- Line 152: `contracts: list[IntegrationContract] = field(default_factory=list)`
- Line 166: `def extract_integration_contracts(spec_text: str) -> list[IntegrationContract]:`
- Line 177: `seen_signatures: dict[tuple[str, frozenset[str]], int] = {}`
- Line 412: `def _extract_identifiers(text: str) -> list[str]:`
- Line 425–426:
  ```python
  sig: tuple[str, frozenset[str]],
  seen: dict[tuple[str, frozenset[str]], int],
  ```

The `typing` module is **not imported anywhere** in the file. Only `re` and `dataclasses` (`dataclass`, `field`) are imported.

### Recommendation for `_canonicalize_identifiers`

Use lowercase built-in generics: `list[str]`, `frozenset[str]`, `tuple[...]`, `dict[K, V]`. Do NOT import from `typing`.

---

## Summary

## Correction Note (gap-fill round 1, applied 2026-05-26T11:14:00Z)

Original R2 line citations had a systematic drift (-7 to -12 lines) against PR sha `67ab0af5` — flagged CRITICAL by rf-qa research gate (round 1). Orchestrator verified ground truth via `git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py | grep -n` and corrected all 11 affected citations in-place. R2's substantive pattern descriptions (docstring style, regex compilation strategy, naming convention, type-hint syntax) were verified correct and unchanged. R1's PR-sha line numbers remain the canonical source for any conflict (rf-qa Issue #2).

---

The new `_canonicalize_identifiers` helper (PR A) must match the file's conventions:

1. **Docstring:** triple-quoted, 1–3 lines of freeform prose, optional FR-MOD2.X cite. No `Args:`/`Returns:` blocks.
2. **Regex:** if reused, pre-compile at module scope with multi-line `r"..."` concatenation and trailing positional `re.IGNORECASE`; if single-use simple, inline `re.findall`. Never inline `(?i)` flags.
3. **Naming:** `_canonicalize_identifiers` (lowercase snake with leading underscore) — matches `_classify_mechanism` / `_extract_identifiers` / `_signature_subsumed` pattern. Place definition under the `# --- Internal helpers ---` banner near end of file, after `_signature_subsumed`.
4. **Tests:** add a pytest class `TestCanonicalizeIdentifiers` with docstring `"""FR-MOD2.X: ..."""`, module-level string fixtures, snake_case `test_<scenario>` methods with no docstrings.
5. **Type hints:** lowercase built-in generics only (`list[str]`, `frozenset[str]`, `tuple[...]`) — file already has `from __future__ import annotations` and zero `typing` imports.
