---
title: "Obligation Vocabulary Alignment — Implementation Workflow"
design_source: ".dev/releases/current/obligation-vocab-alignment/design.md"
branch: feat/v3.65-prd-tdd-Refactor
created: 2026-04-03
compliance_tier: STANDARD
total_steps: 6
estimated_effort: "45-60 minutes"
affected_files:
  - src/superclaude/cli/vocabulary.py
  - src/superclaude/cli/roadmap/obligation_scanner.py
  - src/superclaude/cli/roadmap/prompts.py
test_files:
  - tests/roadmap/test_vocabulary.py
  - tests/roadmap/test_obligation_scanner_meta_context.py
  - tests/roadmap/test_prompts.py
---

# Obligation Vocabulary Alignment — Workflow

## Execution Order

```
[0: Test baseline] → [1: Create vocabulary.py] → [2: Rewire obligation_scanner.py]
    → [3: Wire prompts.py] → [4: Write all tests] → [5: Verify suite + pipeline]
```

---

## Step 0: Capture test baseline

**Action**: VERIFY
**Purpose**: TFEP compliance — record pre-implementation test state

```bash
uv run pytest tests/roadmap/test_obligation_scanner.py tests/roadmap/test_obligation_scanner_meta_context.py tests/roadmap/test_prompts.py --collect-only -q
```

**Acceptance**: All listed tests are in PASSED or COLLECTED state. No pre-existing failures in the affected test files.

---

## Step 1: Create shared vocabulary module

**Action**: CREATE
**File**: `src/superclaude/cli/vocabulary.py`
**FR**: FR-1
**Design ref**: Section 3.1

### Changes

Create file containing:

1. Module docstring referencing FR-MOD1.1 and listing consumers (`obligation_scanner.py`, `prompts.py`)
2. `SCAFFOLD_TERMS: list[str]` — exactly 11 regex patterns, copied verbatim from `obligation_scanner.py` lines 20-32
3. `DISCHARGE_TERMS: list[str]` — exactly 9 regex patterns, copied verbatim from `obligation_scanner.py` lines 36-45
4. `PREFERRED_ALTERNATIVES: dict[str, str]` — 16 entries mapping plain-English scaffold terms to preferred alternatives:
   - scaffold→create, scaffolding→construction, scaffolded→created
   - mock→simulate, mocked→simulated
   - stub→define, stubbed→defined
   - skeleton→outline, placeholder→initial, temporary→interim
   - hardcoded→fixed-value, hardwired→direct
   - no-op→pass-through, noop→pass-through
   - dummy→sample, fake→synthetic
5. `build_prompt_constraint_block() -> str` — function that:
   - Iterates `PREFERRED_ALTERNATIVES`, deduplicates by stem
   - Builds rows of `"avoid" → "prefer"` pairs
   - Returns a string block starting with `\n\nVOCABULARY CONSTRAINT (obligation scanner compliance):\n`
   - Ends with instruction: if scaffold term is genuinely needed, MUST include discharge task in later phase
   - Total output must be under 800 chars (~200 tokens)

### Acceptance

- `from superclaude.cli.vocabulary import SCAFFOLD_TERMS, DISCHARGE_TERMS, PREFERRED_ALTERNATIVES, build_prompt_constraint_block` succeeds
- `len(SCAFFOLD_TERMS) == 11`
- `len(DISCHARGE_TERMS) == 9`
- `len(PREFERRED_ALTERNATIVES) == 16`
- `"VOCABULARY CONSTRAINT" in build_prompt_constraint_block()`
- `len(build_prompt_constraint_block()) < 800`

---

## Step 2: Rewire obligation_scanner.py

**Action**: MODIFY
**File**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**FR**: FR-1 (import rewire), FR-3 (meta-context patterns)
**Design ref**: Section 3.2

### Change 2a: Replace local terms with import

**Location**: Lines 18-45 (the `SCAFFOLD_TERMS` and `DISCHARGE_TERMS` list definitions)

- Delete the local `SCAFFOLD_TERMS = [...]` block (lines 20-32)
- Delete the local `DISCHARGE_TERMS = [...]` block (lines 36-45)
- Delete the comment lines above each block (lines 18-19, 34-35)
- Add after existing imports (`from dataclasses import dataclass`):
  ```python
  from ..vocabulary import SCAFFOLD_TERMS, DISCHARGE_TERMS
  ```
- Leave `_SCAFFOLD_RE`, `_DISCHARGE_RE`, `_INLINE_CODE_SCAFFOLD_RE` compiled patterns unchanged — they reference the module-level names which are now imported

### Change 2b: Add meta-context regex patterns

**Location**: After `_SHELL_CMD_RE` definition (near line 86 in current file)

Add two compiled patterns:

```python
# Layer 3a: Imperative task verb in table cell
_TABLE_CELL_IMPERATIVE_RE = re.compile(
    r"^\s*\|[^|]*\|\s*(?:scaffold|mock|stub|fake|dummy)\s+\w+",
    re.IGNORECASE,
)

# Layer 3b: Parenthetical phase/step label
_PAREN_PHASE_LABEL_RE = re.compile(
    r"\([^)]*(?:scaffold(?:ing|ed)?|mock(?:ing|ed)?|stub(?:bing|bed)?)[^)]*\)",
    re.IGNORECASE,
)
```

### Change 2c: Wire patterns into `_is_meta_context()`

**Location**: `_is_meta_context()` function, before the final `return False`

Add:
```python
    # Layer 3a: Scaffold term as imperative verb in table cell
    if _TABLE_CELL_IMPERATIVE_RE.search(line):
        return True

    # Layer 3b: Scaffold term in parenthetical label
    if _PAREN_PHASE_LABEL_RE.search(line):
        return True
```

### Acceptance

- `from superclaude.cli.roadmap.obligation_scanner import SCAFFOLD_TERMS` succeeds
- `SCAFFOLD_TERMS is vocabulary.SCAFFOLD_TERMS` (identity, not equality)
- `_is_meta_context("| 2.2.1 | Scaffold command file using template | FR-001 |", 10)` returns `True`
- `_is_meta_context("Phase 2 (command scaffolding)", 20)` returns `True`
- `_is_meta_context("Create a scaffold for the executor", 9)` returns `False`

---

## Step 3: Wire prompts.py

**Action**: MODIFY
**File**: `src/superclaude/cli/roadmap/prompts.py`
**FR**: FR-2
**Design ref**: Section 3.3

### Change 3a: Add import

**Location**: Top of file, with other imports

```python
from ..vocabulary import build_prompt_constraint_block
```

### Change 3b: Inject into `build_generate_prompt()`

**Location**: After the `"If the extraction uses FR-EVAL-001.1..."` line (end of base string, before `if tdd_file is not None:`)

```python
    base += build_prompt_constraint_block()
```

### Change 3c: Inject into `build_merge_prompt()`

**Location**: After the `"Do not duplicate heading text at H2 or H3 level."` line (end of base string, before `if tdd_file is not None:`)

```python
    base += build_prompt_constraint_block()
```

### Acceptance

- `"VOCABULARY CONSTRAINT" in build_generate_prompt(agent_mock, Path("/tmp/e.md"))`
- `"VOCABULARY CONSTRAINT" in build_merge_prompt(Path("/tmp/b.md"), Path("/tmp/a.md"), Path("/tmp/b.md"), Path("/tmp/d.md"))`

---

## Step 4: Write all tests

**Action**: CREATE + MODIFY
**Files**:
  - `tests/roadmap/test_vocabulary.py` (CREATE)
  - `tests/roadmap/test_obligation_scanner_meta_context.py` (MODIFY)
  - `tests/roadmap/test_prompts.py` (MODIFY)

### 4a: Create `tests/roadmap/test_vocabulary.py`

```python
"""Tests for shared obligation vocabulary module."""

from __future__ import annotations

import pytest

from superclaude.cli.vocabulary import (
    DISCHARGE_TERMS,
    PREFERRED_ALTERNATIVES,
    SCAFFOLD_TERMS,
    build_prompt_constraint_block,
)


class TestScaffoldTerms:
    def test_has_exactly_11_entries(self):
        assert len(SCAFFOLD_TERMS) == 11

    def test_all_entries_are_word_boundary_regex(self):
        for term in SCAFFOLD_TERMS:
            assert term.startswith(r"\b"), f"{term} missing word boundary"


class TestDischargeTerms:
    def test_has_exactly_9_entries(self):
        assert len(DISCHARGE_TERMS) == 9


class TestPreferredAlternatives:
    def test_has_16_entries(self):
        assert len(PREFERRED_ALTERNATIVES) == 16

    def test_covers_all_scaffold_stems(self):
        base_words = [
            "mock", "stub", "skeleton", "placeholder", "scaffold",
            "temporary", "hardcoded", "hardwired", "no-op", "dummy", "fake",
        ]
        for word in base_words:
            matches = [k for k in PREFERRED_ALTERNATIVES if word in k or k in word]
            assert matches, f"No alternative for scaffold term '{word}'"


class TestBuildPromptConstraintBlock:
    def test_output_under_800_chars(self):
        block = build_prompt_constraint_block()
        assert len(block) < 800, f"Block is {len(block)} chars, likely >200 tokens"

    def test_contains_vocabulary_constraint_header(self):
        block = build_prompt_constraint_block()
        assert "VOCABULARY CONSTRAINT" in block

    def test_contains_at_least_one_alternative(self):
        block = build_prompt_constraint_block()
        assert "\u2192" in block


class TestVocabularyIdentity:
    """Verify obligation_scanner imports from vocabulary (not local copies)."""

    def test_scanner_scaffold_terms_is_same_object(self):
        from superclaude.cli.roadmap.obligation_scanner import (
            SCAFFOLD_TERMS as scanner_terms,
        )
        assert scanner_terms is SCAFFOLD_TERMS

    def test_scanner_discharge_terms_is_same_object(self):
        from superclaude.cli.roadmap.obligation_scanner import (
            DISCHARGE_TERMS as scanner_terms,
        )
        assert scanner_terms is DISCHARGE_TERMS
```

### 4b: Append to `tests/roadmap/test_obligation_scanner_meta_context.py`

Add new class at end of file:

```python
class TestLayer3StructuralPatterns:
    """Layer 3: Table-cell imperatives and parenthetical labels."""

    def test_table_cell_imperative_scaffold_is_medium(self):
        """Scaffold as first word in table task cell -> MEDIUM."""
        content = textwrap.dedent("""\
            ## Phase 2: Create Artifacts
            | Sub-step | Task | Requirements |
            |----------|------|-------------|
            | 2.2.1 | Scaffold command file using template | FR-001 |

            ## Phase 3: Verify
            - Run validation checks
        """)
        report = scan_obligations(content)
        scaffold_obs = [o for o in report.obligations if "scaffold" in o.term.lower()]
        assert scaffold_obs, "Expected scaffold obligation to be detected"
        assert all(o.severity == "MEDIUM" for o in scaffold_obs)

    def test_parenthetical_phase_label_is_medium(self):
        """Scaffold term in parenthetical phase label -> MEDIUM."""
        content = textwrap.dedent("""\
            ## Phase 4: Dependencies
            | Dependency | Required By | Risk |
            |-----------|------------|------|
            | adversarial.md | Phase 2 (command scaffolding) | LOW |

            ## Phase 5: Wrap-up
            - Final checks
        """)
        report = scan_obligations(content)
        scaffold_obs = [o for o in report.obligations if "scaffolding" in o.term.lower()]
        assert scaffold_obs, "Expected scaffolding obligation to be detected"
        assert all(o.severity == "MEDIUM" for o in scaffold_obs)

    def test_plain_scaffold_not_in_table_stays_high(self):
        """Scaffold in regular prose (not table cell, not parens) -> HIGH."""
        content = textwrap.dedent("""\
            ## Phase 1: Build
            - Create a scaffold for the executor module

            ## Phase 2: Test
            - Run tests
        """)
        report = scan_obligations(content)
        scaffold_obs = [o for o in report.obligations if "scaffold" in o.term.lower()]
        assert scaffold_obs, "Expected scaffold obligation to be detected"
        assert any(o.severity == "HIGH" for o in scaffold_obs)
```

### 4c: Append to `tests/roadmap/test_prompts.py`

Add import of `build_generate_prompt` and `build_merge_prompt` to existing import block, then add new class:

```python
class TestVocabularyConstraintInjection:
    """Verify vocabulary constraint block is injected into generation prompts."""

    def test_generate_prompt_contains_constraint(self):
        from unittest.mock import MagicMock
        agent = MagicMock()
        agent.persona = "software architect"
        prompt = build_generate_prompt(agent, Path("/tmp/extraction.md"))
        assert "VOCABULARY CONSTRAINT" in prompt

    def test_merge_prompt_contains_constraint(self):
        prompt = build_merge_prompt(
            Path("/tmp/base.md"),
            Path("/tmp/a.md"),
            Path("/tmp/b.md"),
            Path("/tmp/debate.md"),
        )
        assert "VOCABULARY CONSTRAINT" in prompt
```

### Acceptance

- `uv run pytest tests/roadmap/test_vocabulary.py -v` — all pass
- `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -v` — all pass (including new Layer 3 tests)
- `uv run pytest tests/roadmap/test_prompts.py -v` — all pass (including new injection tests)

---

## Step 5: Verify suite + pipeline

**Action**: VERIFY

### 5a: Full test suite regression check

```bash
uv run pytest tests/ -v --tb=short
```

**Acceptance**: Zero failures. All pre-existing tests from Step 0 baseline still pass. All new tests pass.

### 5b: End-to-end verification against failing roadmap

```bash
uv run python -c "
from superclaude.cli.roadmap.obligation_scanner import scan_obligations
from pathlib import Path
content = Path('.dev/releases/backlog/prd-skill-refactor/roadmap.md').read_text()
report = scan_obligations(content)
print(f'Undischarged (HIGH only): {report.undischarged_count}')
for o in report.obligations:
    if not o.discharged:
        print(f'  L{o.line_number} [{o.severity}]: {o.term} -- {o.context[:60]}')
"
```

**Acceptance**: `undischarged_count` is `0`. Lines 93 and 220 appear as MEDIUM severity, not HIGH.

### 5c: Resume roadmap pipeline

```bash
superclaude roadmap run .dev/releases/backlog/prd-skill-refactor/prd-refactor-spec-v2.md --resume
```

**Acceptance**: `anti-instinct` step passes.

---

## Post-Workflow

After Step 5c passes, the original pipeline failure is resolved and the vocabulary alignment feature is complete.
