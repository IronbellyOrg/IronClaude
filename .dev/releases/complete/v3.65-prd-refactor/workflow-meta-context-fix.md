# Workflow: Meta-Context False Positive Mitigation for Obligation Scanner

**Source**: `adversarial/merged-proposal.md` (same directory)
**Optimized for**: `/sc:task-unified` execution
**Estimated diff**: ~230 lines across 2 files (1 modified, 1 new)

---

## Dependency Graph

```
Task 1 (constants) → Task 2 (Layer 1 integration) → Task 4 (Layer 1 tests)
Task 1 (constants) → Task 3 (_is_meta_context) → Task 5 (Layer 2 integration) → Task 6 (unit tests)
Task 4 + Task 6 → Task 7 (integration tests)
Task 7 → Task 8 (regression tests)
Task 8 → Task 9 (full suite verification)
```

---

## Task 1: Add module-level regex constants to `obligation_scanner.py`

**File**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Depends on**: nothing
**Blocked by**: nothing

### Change

Add the following compiled regex constants at module level, after the existing `SCAFFOLD_TERMS` and `DISCHARGE_TERMS` definitions. These are used by Layers 1 and 2 of the meta-context classifier.

```python
# --- Meta-context classification (FR-MOD1.9) ---

# Layer 1a: Inline code - scaffold term inside backticks (scaffold-aware)
_INLINE_CODE_SCAFFOLD_RE = re.compile(
    r"`[^`]*(?:" + "|".join(SCAFFOLD_TERMS) + r")[^`]*`",
    re.IGNORECASE,
)

# Layer 1b: Completed checklist item
_COMPLETED_CHECKLIST_RE = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE)

# Layer 2: Negation/meta-context prefix patterns
_NEGATION_PREFIX_RE = re.compile(
    r"(?:"
    # Category 1: Negation/verification words
    r"\b(?:no|not?|never|without|ensure\s+no|verify\s+no|check\s+(?:for\s+)?no|"
    r"must\s+not|should\s+not|shall\s+not|cannot|don'?t|reject|prohibit|forbid|prevent|disallow)\b"
    r"|"
    # Category 4: Past-tense removal
    r"\b(?:removed?|replaced?|eliminated?|deleted?|stripped?|cleaned?|purged?|"
    r"swapped\s+out|migrated\s+away\s+from)\b"
    r"|"
    # Category 5: Risk/warning framing
    r"(?:^\s*)(?:risk|warning|caution|danger|caveat|concern)\s*:"
    r"|"
    # Category 6: Gate/verification criteria
    r"\b(?:verification|gate\s+criteri|check\s+(?:for|that)|validate|assert|audit)\b"
    r")",
    re.IGNORECASE,
)

# Shell command detection (Category 2)
_SHELL_CMD_RE = re.compile(
    r"(?:^\s*[$>]?\s*)?(?:grep|sed|awk|find|rg|ag|git\s+grep|xargs)\b",
    re.IGNORECASE,
)

# Risk/warning line detection
_RISK_WARNING_RE = re.compile(
    r"(?:^\s*)(?:risk|warning|caution|danger|caveat|concern)\s*:",
    re.IGNORECASE,
)

# Gate/verification criteria language
_GATE_CRITERIA_RE = re.compile(
    r"(?:no|zero|0)\s+(?:\w+\s+){0,4}"
    r"(?:present|found|detected|remaining|allowed|permitted|exist)",
    re.IGNORECASE,
)
```

### Verification

- `uv run python -c "from superclaude.cli.roadmap.obligation_scanner import _INLINE_CODE_SCAFFOLD_RE, _COMPLETED_CHECKLIST_RE, _NEGATION_PREFIX_RE, _SHELL_CMD_RE, _RISK_WARNING_RE, _GATE_CRITERIA_RE; print('OK')"` — confirms all constants compile and are importable

---

## Task 2: Add Layer 1 integration in `scan_obligations()`

**File**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Depends on**: Task 1
**Blocked by**: Task 1

### Change

In the `scan_obligations()` function, AFTER the existing severity determination (`severity = _determine_severity(...)`) and context line extraction, add Layer 1 checks. These must go AFTER `_determine_severity()` and BEFORE obligation creation:

```python
# Layer 1a: Inline code exemption -- scaffold term inside backtick spans
if severity == "HIGH" and _INLINE_CODE_SCAFFOLD_RE.search(context_line):
    severity = "MEDIUM"

# Layer 1b: Completed checklist exemption -- "- [x]" items
elif severity == "HIGH" and _COMPLETED_CHECKLIST_RE.match(context_line):
    severity = "MEDIUM"
```

Key constraints:
- Only run when severity is still HIGH (don't re-classify MEDIUM code-block matches)
- Order matters: inline code check before checklist check
- Use `search()` for inline code (can appear anywhere), `match()` for checklist (must be at line start)

### Verification

- `uv run python -c "from superclaude.cli.roadmap.obligation_scanner import scan_obligations; print('OK')"` — confirms no syntax/import errors

---

## Task 3: Add `_is_meta_context()` classification function

**File**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Depends on**: Task 1 (uses the regex constants)
**Blocked by**: Task 1

### Change

Add the `_is_meta_context()` function after the regex constants from Task 1. This is a pure function with no side effects.

```python
def _is_meta_context(line: str, term_start_in_line: int) -> bool:
    """Determine if a scaffold term on this line is in a meta-context.

    Returns True when the scaffold term appears in a negation, verification,
    historical, risk, shell-command, or gate-criteria context. Caller should
    set severity to MEDIUM when this returns True.

    Args:
        line: The full line containing the scaffold match.
        term_start_in_line: Character offset of the scaffold term within ``line``.

    Returns:
        True if the term appears in meta-context (should be MEDIUM severity).
        False if the term appears to be an affirmative obligation (HIGH severity).
    """
    # Category 2: Shell command lines are always meta-context
    if _SHELL_CMD_RE.search(line):
        return True

    # Category 5: Risk/warning framing at line start
    if _RISK_WARNING_RE.match(line):
        return True

    # Category 6: Gate/verification criteria language
    if _GATE_CRITERIA_RE.search(line):
        return True

    # Categories 1, 4: Negation/removal/historical prefix BEFORE the scaffold term
    prefix = line[:term_start_in_line]
    if _NEGATION_PREFIX_RE.search(prefix):
        return True

    # Category 4 supplement: Past-tense removal verbs anywhere on the line
    if re.search(
        r"\b(?:removed?|replaced?|eliminated?|deleted?)\b",
        line,
        re.IGNORECASE,
    ):
        return True

    return False
```

### Verification

- `uv run python -c "from superclaude.cli.roadmap.obligation_scanner import _is_meta_context; print(_is_meta_context('No placeholder values', 3))"` — should print `True`
- `uv run python -c "from superclaude.cli.roadmap.obligation_scanner import _is_meta_context; print(_is_meta_context('Create mock runner', 7))"` — should print `False`

---

## Task 4: Write Layer 1 unit tests

**File**: `tests/roadmap/test_obligation_scanner_meta_context.py` (NEW)
**Depends on**: Task 1, Task 2
**Blocked by**: Task 2

### Change

Create a new test file with tests for Layer 1 features (inline code + completed checklist).

```python
"""Meta-context false positive suppression tests for obligation scanner.

Tests the 2-layer meta-context classification system (FR-MOD1.9):
- Layer 1: Structural exemptions (inline code, completed checklists)
- Layer 2: Negation/meta-context classification (_is_meta_context)

Each test uses the edge case catalog from the merged proposal (E1-E20).
"""

from __future__ import annotations

import textwrap

import pytest

from superclaude.cli.roadmap.obligation_scanner import (
    _is_meta_context,
    scan_obligations,
)


class TestLayer1InlineCode:
    """Layer 1a: Scaffold terms inside backtick spans are MEDIUM."""

    def test_inline_code_scaffold_term_is_medium(self):
        """E4: Inline code reference demoted to MEDIUM."""
        content = textwrap.dedent("""\
            ## Phase 1: Implementation
            - Build the auth module

            ## Phase 2: Verification
            - Remove all `placeholder` values from config
        """)
        report = scan_obligations(content)
        phase2_obs = [o for o in report.obligations if "placeholder" in o.term.lower()]
        assert all(o.severity == "MEDIUM" for o in phase2_obs)

    def test_inline_code_does_not_affect_plain_text(self):
        """E1: Plain scaffold term without backticks stays HIGH."""
        content = textwrap.dedent("""\
            ## Phase 1: Setup
            - Create placeholder config files
        """)
        report = scan_obligations(content)
        assert any(o.severity == "HIGH" for o in report.obligations)


class TestLayer1CompletedChecklist:
    """Layer 1b: Completed checklist items are MEDIUM."""

    def test_completed_checklist_is_medium(self):
        """E5: Completed checklist items demoted to MEDIUM."""
        content = textwrap.dedent("""\
            ## Phase 1: Setup
            - Create scaffold structure

            ## Phase 2: Completion
            - [x] All scaffold replaced with real implementations
            - [x] Mock services removed
        """)
        report = scan_obligations(content)
        phase2_obs = [
            o for o in report.obligations
            if o.severity == "MEDIUM" and "phase 2" in (o.phase or "").lower()
        ]
        # At least the completed checklist items should be MEDIUM
        assert len(phase2_obs) >= 1

    def test_unchecked_checklist_stays_high(self):
        """Unchecked checklist items stay HIGH."""
        content = textwrap.dedent("""\
            ## Phase 1: Setup
            - [ ] Create mock handler
        """)
        report = scan_obligations(content)
        assert any(o.severity == "HIGH" for o in report.obligations)
```

### Verification

- `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -v -k "Layer1"` — all Layer 1 tests pass

---

## Task 5: Add Layer 2 integration in `scan_obligations()`

**File**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Depends on**: Task 2 (Layer 1 integration), Task 3 (`_is_meta_context()`)
**Blocked by**: Task 2, Task 3

### Change

In the `scan_obligations()` function, AFTER the Layer 1 checks from Task 2, add the Layer 2 meta-context check:

```python
# Layer 2: Negation/meta-context classification
elif severity == "HIGH":
    term_start_in_line = match.start() - line_start
    if _is_meta_context(context_line, term_start_in_line):
        severity = "MEDIUM"
```

Key constraints:
- The `elif` chains from Layer 1's `if`/`elif` — Layer 2 only runs if Layer 1 didn't already classify
- Only applies when severity is still HIGH
- Requires `line_start` variable (the start of the current line within `phase_content`) — verify this is already computed or compute it as: `line_start = phase_content.rfind("\n", 0, match.start()) + 1`
- `term_start_in_line` is the offset of the match within the current line: `match.start() - line_start`

### Verification

- `uv run python -c "from superclaude.cli.roadmap.obligation_scanner import scan_obligations; r = scan_obligations('## Phase 1\n- No placeholder values present\n'); print(r.undischarged_count)"` — should print `0`

---

## Task 6: Write Layer 2 unit tests (`_is_meta_context` parameterized)

**File**: `tests/roadmap/test_obligation_scanner_meta_context.py` (append)
**Depends on**: Task 3, Task 5
**Blocked by**: Task 5

### Change

Append to the test file from Task 4:

```python
class TestIsMetaContext:
    """Parameterized tests for _is_meta_context() classification."""

    @pytest.mark.parametrize("line,term_pos,expected,reason", [
        # E1: Affirmative obligation
        ("Create mocked step runners", 7, False, "affirmative"),
        # E6: Negation "no X present"
        ("No template sentinel placeholders present", 27, True, "negation_prefix"),
        # E7: "must not contain"
        ("Must not contain placeholder values", 21, True, "negation_prefix"),
        # E8: "ensure no X"
        ("Ensure no mock data remains", 10, True, "negation_prefix"),
        # E9: Past-tense removal
        ("Removed the stub endpoint in v2.1", 12, True, "past_tense"),
        # E10: grep command
        ("grep -rn '<placeholder>' src/", 11, True, "shell_command"),
        # E11: find command
        ("find . -name '*mock*' -delete", 17, True, "shell_command"),
        # E12: Gate criteria
        ("Zero placeholder values found", 5, True, "gate_criteria"),
        # E13: Risk description
        ("Risk: placeholder data could leak", 6, True, "risk_description"),
        # E14: Ambiguous affirmative
        ("Use placeholder config for now", 4, False, "affirmative"),
        # E15: Negation AFTER term
        ("The placeholder should not be committed", 4, False, "negation_after_term"),
        # E16: Double negation
        ("Do not remove the mock yet", 22, False, "double_negation"),
        # E17: Term in heading
        ("## Phase 1: Skeleton Setup", 15, False, "heading_affirmative"),
        # E18a: Mixed line first term (preceded by "Remove")
        ("Remove old stubs and add new placeholder", 11, True, "negation_prefix"),
        # E18b: Mixed line second term (not preceded by negation)
        ("Remove old stubs and add new placeholder", 33, False, "affirmative_second_term"),
        # E19: Negation with word gap
        ("Ensure the system has no residual temporary files", 38, True, "negation_prefix"),
        # E20: "never" keyword
        ("Never deploy with hardcoded credentials", 19, True, "negation_prefix"),
    ])
    def test_is_meta_context(self, line, term_pos, expected, reason):
        result = _is_meta_context(line, term_pos)
        assert result == expected, f"Failed for {reason}: {line!r}"
```

### Verification

- `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -v -k "TestIsMetaContext"` — all parameterized tests pass

---

## Task 7: Write integration tests for `scan_obligations()`

**File**: `tests/roadmap/test_obligation_scanner_meta_context.py` (append)
**Depends on**: Task 4 (Layer 1 tests), Task 6 (Layer 2 tests)
**Blocked by**: Task 4, Task 6

### Change

Append to the test file:

```python
class TestMetaContextFalsePositiveSuppression:
    """Integration: meta-context false positives do not block the gate."""

    def test_verification_criteria_not_counted(self):
        """Gate criteria mentioning scaffold terms are MEDIUM, not HIGH."""
        content = textwrap.dedent("""\
            ## Phase 1: Implementation
            - Build the authentication module

            ## Phase 2: Verification
            - No template sentinel placeholders present
            - Ensure no mock data remains in production config
            - Zero stub endpoints found in final build
        """)
        report = scan_obligations(content)
        assert report.undischarged_count == 0

    def test_shell_commands_not_counted(self):
        """Shell commands searching for scaffold terms are MEDIUM."""
        content = textwrap.dedent("""\
            ## Phase 1: Setup
            - Initialize project structure

            ## Phase 2: QA Checks
            - grep -rn 'placeholder' src/superclaude/
        """)
        report = scan_obligations(content)
        assert report.undischarged_count == 0

    def test_affirmative_obligations_still_detected(self):
        """Real scaffolding obligations remain HIGH and counted."""
        content = textwrap.dedent("""\
            ## Phase 1: Skeleton Setup
            - Create mocked step runners for initial testing
            - Build placeholder dispatch table
            - Implement stub executor

            ## Phase 2: Core Logic
            - Implement pipeline logic
        """)
        report = scan_obligations(content)
        assert report.undischarged_count >= 3
        high_count = len([o for o in report.obligations if o.severity == "HIGH"])
        assert high_count >= 3

    def test_mixed_real_and_meta_same_document(self):
        """Real obligations counted, meta-references excluded, in same doc."""
        content = textwrap.dedent("""\
            ## Phase 1: Bootstrap
            - Create placeholder config files
            - Build skeleton API layer

            ## Phase 2: Implement
            - Replace placeholder config with real values
            - Wire skeleton into production router

            ## Phase 3: Verify
            - Ensure no placeholder values remain
        """)
        report = scan_obligations(content)
        assert report.undischarged_count == 0
```

### Verification

- `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -v -k "TestMetaContextFalsePositiveSuppression"` — all integration tests pass

---

## Task 8: Write regression tests for existing behavior

**File**: `tests/roadmap/test_obligation_scanner_meta_context.py` (append)
**Depends on**: Task 7
**Blocked by**: Task 7

### Change

Append to the test file:

```python
class TestExistingBehaviorPreserved:
    """Regression: existing scanner behavior is not degraded."""

    def test_exempt_comment_still_works(self):
        content = textwrap.dedent("""\
            ## Phase 1
            - Create mock handler  # obligation-exempt
        """)
        report = scan_obligations(content)
        exempt_obs = [o for o in report.obligations if o.exempt]
        assert len(exempt_obs) >= 1

    def test_code_block_still_medium(self):
        content = "## Phase 1\n```python\nmock_data = {}\n```\n"
        report = scan_obligations(content)
        code_obs = [o for o in report.obligations if o.severity == "MEDIUM"]
        assert len(code_obs) >= 1

    def test_discharge_mechanism_unchanged(self):
        content = textwrap.dedent("""\
            ## Phase 1
            - Create stub handler

            ## Phase 2
            - Replace stub handler with real implementation
        """)
        report = scan_obligations(content)
        discharged = [o for o in report.obligations if o.discharged]
        assert len(discharged) >= 1
```

### Verification

- `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -v -k "TestExistingBehaviorPreserved"` — all regression tests pass

---

## Task 9: Full test suite verification

**Depends on**: Task 8
**Blocked by**: Task 8

### Change

No code changes. Verification only.

### Verification

- `uv run pytest tests/roadmap/ -v` — all roadmap tests pass (new + existing)
- `uv run pytest tests/ -v --tb=short` — full suite passes with no NEW failures (pre-existing failures are acceptable)
- `make lint` — no lint errors introduced
- `make format` — no formatting changes needed (or apply them)

### Acceptance criteria

- 0 new test failures introduced
- All 18+ parameterized `_is_meta_context` tests pass
- All 4 integration tests pass
- All 3 regression tests pass
- All 4 Layer 1 tests pass
- `make lint` clean
