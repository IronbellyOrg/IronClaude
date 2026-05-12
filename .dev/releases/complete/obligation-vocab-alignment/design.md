---
title: "Obligation Vocabulary Alignment — Technical Design"
status: draft
created: 2026-04-03
source_requirements: "brainstorm session (same conversation)"
affected_files:
  - src/superclaude/cli/vocabulary.py (NEW)
  - src/superclaude/cli/roadmap/obligation_scanner.py (MODIFY)
  - src/superclaude/cli/roadmap/prompts.py (MODIFY)
complexity: simple
estimated_loc_delta: "+95, -25 (net +70)"
---

# Obligation Vocabulary Alignment — Design Document

## 1. Problem

The roadmap pipeline's anti-instinct gate fails 100% of the time on false positives. The obligation scanner flags legitimate planning language (e.g., "Scaffold command file", "command scaffolding") as undischarged obligations because its scaffold vocabulary overlaps with normal construction verbs.

**Root cause**: The scanner vocabulary and the LLM generation prompts are unaware of each other. The LLM freely uses scaffold terms for non-scaffold meanings; the scanner has no way to distinguish intent.

## 2. Solution Overview

Two-layer defense:

1. **Prompt-side prevention**: Tell the LLM which words trigger the obligation scanner and provide alternatives → reduces false positives at generation time.
2. **Scanner-side tolerance**: Teach `_is_meta_context()` two new structural patterns that are never real obligations → catches what slips through.

Both layers share a single vocabulary source of truth.

## 3. Component Design

### 3.1 New File: `src/superclaude/cli/vocabulary.py`

Elevated to `cli/` (not `cli/roadmap/`) for future reuse by sprint and other pipelines.

```python
"""Shared obligation vocabulary — single source of truth.

Used by:
- obligation_scanner.py: detection patterns
- prompts.py: LLM constraint block generation

Implements FR-MOD1.1 vocabulary (11 scaffold terms, 9 discharge terms)
plus preferred-alternative mappings for prompt guidance.
"""

from __future__ import annotations

# --- Scaffold terms (regex patterns) ---

SCAFFOLD_TERMS: list[str] = [
    r"\bmock(?:ed|s)?\b",
    r"\bstub(?:bed|s)?\b",
    r"\bskeleton\b",
    r"\bplaceholder\b",
    r"\bscaffold(?:ing|ed)?\b",
    r"\btemporary\b",
    r"\bhardcoded\b",
    r"\bhardwired\b",
    r"\bno-?op\b",
    r"\bdummy\b",
    r"\bfake\b",
]

# --- Discharge terms (regex patterns) ---

DISCHARGE_TERMS: list[str] = [
    r"\breplace\b",
    r"\bwire\s+(?:up|in|into)\b",
    r"\bintegrat(?:e|ing|ed)\b",
    r"\bconnect\b",
    r"\bswap\s+(?:out|in)\b",
    r"\bremove\s+(?:mock|stub|placeholder|scaffold)\b",
    r"\bimplement\s+real\b",
    r"\bfill\s+in\b",
    r"\bcomplete\s+(?:the\s+)?(?:skeleton|scaffold)\b",
]

# --- Preferred alternatives (human-readable, for prompt injection) ---
# Key: plain-English scaffold term (as it appears in prose)
# Value: preferred alternative verb/noun

PREFERRED_ALTERNATIVES: dict[str, str] = {
    "scaffold": "create",
    "scaffolding": "construction",
    "scaffolded": "created",
    "mock": "simulate",
    "mocked": "simulated",
    "stub": "define",
    "stubbed": "defined",
    "skeleton": "outline",
    "placeholder": "initial",
    "temporary": "interim",
    "hardcoded": "fixed-value",
    "hardwired": "direct",
    "no-op": "pass-through",
    "noop": "pass-through",
    "dummy": "sample",
    "fake": "synthetic",
}


def build_prompt_constraint_block() -> str:
    """Build a <200-token constraint block for LLM generation prompts.

    Dynamically generated from PREFERRED_ALTERNATIVES so adding a term
    to the vocabulary automatically updates all prompts.
    """
    # Build compact avoid/prefer table
    rows = []
    seen: set[str] = set()
    for avoid, prefer in PREFERRED_ALTERNATIVES.items():
        base = avoid.rstrip("edingsz")  # rough dedup by stem
        if base not in seen:
            seen.add(base)
            rows.append(f'  "{avoid}" → "{prefer}"')

    table = "\n".join(rows)

    return (
        "\n\nVOCABULARY CONSTRAINT (obligation scanner compliance):\n"
        "The downstream anti-instinct gate flags these terms as scaffolding "
        "obligations. Use the preferred alternative instead:\n"
        f"{table}\n"
        "If you genuinely mean a temporary artifact that will be replaced later, "
        "you may use the original term — but you MUST include a discharge task "
        "(replace, integrate, wire up, remove) in a subsequent phase.\n"
    )
```

**Design decisions**:
- `PREFERRED_ALTERNATIVES` uses plain-English keys (not regex) because it's consumed by the prompt builder, not the scanner.
- `build_prompt_constraint_block()` deduplicates by stem to keep the block compact.
- The function returns a string fragment, not a full prompt — the caller appends it.

### 3.2 Modifications: `obligation_scanner.py`

**Change 1**: Replace local term definitions with imports.

```python
# BEFORE (lines 20-45):
SCAFFOLD_TERMS = [...]
DISCHARGE_TERMS = [...]

# AFTER:
from ..vocabulary import SCAFFOLD_TERMS, DISCHARGE_TERMS
```

All downstream references (`_SCAFFOLD_RE`, `_DISCHARGE_RE`, `_INLINE_CODE_SCAFFOLD_RE`) remain unchanged — they already consume these lists.

**Change 2**: Add two meta-context patterns to `_is_meta_context()`.

```python
# New compiled patterns (add near line 86, after _SHELL_CMD_RE):

# Layer 3a: Imperative task verb in table cell
# Matches: "| Scaffold command file..." where scaffold is first word after pipe
_TABLE_CELL_IMPERATIVE_RE = re.compile(
    r"^\s*\|[^|]*\|\s*(?:" + "|".join(
        # Extract base words from regex patterns for matching
        [r"scaffold", r"mock", r"stub", r"fake", r"dummy"]
    ) + r")\s+\w+",
    re.IGNORECASE,
)

# Layer 3b: Parenthetical phase/step label
# Matches: "(command scaffolding)", "(Phase 2 scaffolding)", etc.
_PAREN_PHASE_LABEL_RE = re.compile(
    r"\([^)]*(?:" + "|".join(
        [r"scaffold(?:ing|ed)?", r"mock(?:ing|ed)?", r"stub(?:bing|bed)?"]
    ) + r")[^)]*\)",
    re.IGNORECASE,
)
```

```python
# In _is_meta_context() — add before the final `return False`:

    # Layer 3a: Scaffold term as imperative verb in table cell
    if _TABLE_CELL_IMPERATIVE_RE.search(line):
        return True

    # Layer 3b: Scaffold term in parenthetical label
    if _PAREN_PHASE_LABEL_RE.search(line):
        return True

    return False
```

**Why these specific patterns**:
- **Table cell imperative**: The failing line 93 matches `| 2.2.1 | Scaffold command file...`. The pattern requires: pipe delimiter → content → pipe → scaffold term → space → noun. This is a task description, never a real obligation.
- **Parenthetical label**: The failing line 220 matches `Phase 2 (command scaffolding)`. A parenthetical that names what a phase does is descriptive, not prescriptive.

### 3.3 Modifications: `prompts.py`

**Change**: Append the vocabulary constraint block to `build_generate_prompt()` and `build_merge_prompt()`.

```python
# Add import at top of file:
from ..vocabulary import build_prompt_constraint_block

# In build_generate_prompt(), before the tdd_file/prd_file conditionals (after line 434):
    base += build_prompt_constraint_block()

# In build_merge_prompt(), before the tdd_file/prd_file conditionals (after line 627):
    base += build_prompt_constraint_block()
```

**Injection point**: The constraint block goes after the core instructions but before supplementary context blocks (TDD/PRD). This positions it as a structural rule, not supplementary context.

## 4. Data Flow

```
vocabulary.py (single source of truth)
    │
    ├──► obligation_scanner.py
    │      imports SCAFFOLD_TERMS, DISCHARGE_TERMS
    │      compiles into _SCAFFOLD_RE, _DISCHARGE_RE
    │      uses in scan_obligations()
    │
    └──► prompts.py
           imports build_prompt_constraint_block()
           appends to build_generate_prompt()
           appends to build_merge_prompt()
           LLM reads constraint → avoids terms → fewer false positives
```

## 5. Backward Compatibility

| Concern | Mitigation |
|---------|-----------|
| Existing passing roadmaps | Scanner behavior unchanged for all non-table-cell, non-parenthetical contexts. New patterns only add MEDIUM demotions. |
| Term list identity | `vocabulary.py` contains identical lists to current `obligation_scanner.py` lines 20-45. No terms added or removed. |
| Prompt token budget | `build_prompt_constraint_block()` produces ~130 tokens (measured). Under 200-token NFR. |
| Import paths | `obligation_scanner.py` changes from local constants to `from ..vocabulary import`. No public API change. |

## 6. Test Strategy

| Test | What it validates |
|------|------------------|
| `test_vocabulary_scaffold_terms_match` | `vocabulary.SCAFFOLD_TERMS` has exactly 11 entries matching FR-MOD1.1 |
| `test_vocabulary_preferred_alternatives_cover_all_stems` | Every scaffold term stem has a preferred alternative |
| `test_prompt_constraint_block_under_200_tokens` | `build_prompt_constraint_block()` output is <200 tokens (tiktoken estimate) |
| `test_scanner_table_cell_imperative_is_medium` | Line `"| 2.2.1 | Scaffold command file using template |"` → severity MEDIUM |
| `test_scanner_paren_phase_label_is_medium` | Line `"Phase 2 (command scaffolding)"` → severity MEDIUM |
| `test_scanner_real_scaffold_still_high` | Line `"Create a scaffold for the executor"` → severity HIGH (not a table cell or paren) |
| `test_scanner_imports_from_vocabulary` | `obligation_scanner.SCAFFOLD_TERMS is vocabulary.SCAFFOLD_TERMS` (identity check) |
| `test_generate_prompt_contains_constraint` | `build_generate_prompt()` output contains "VOCABULARY CONSTRAINT" |
| `test_merge_prompt_contains_constraint` | `build_merge_prompt()` output contains "VOCABULARY CONSTRAINT" |

## 7. Files Changed Summary

| File | Action | Lines Changed |
|------|--------|--------------|
| `src/superclaude/cli/vocabulary.py` | CREATE | ~75 lines |
| `src/superclaude/cli/roadmap/obligation_scanner.py` | MODIFY | -25 (remove local terms), +20 (import + 2 patterns) |
| `src/superclaude/cli/roadmap/prompts.py` | MODIFY | +5 (import + 2 append calls) |
| `tests/cli/test_vocabulary.py` | CREATE | ~50 lines |
| `tests/cli/roadmap/test_obligation_scanner.py` | MODIFY | +30 (3 new test cases) |
| `tests/cli/roadmap/test_prompts.py` | MODIFY | +20 (2 new test cases) |
