# D-0006: `_parse_routing_list()` Module Placement Decision

**Task:** T01.06
**Date:** 2026-03-16
**Status:** RESOLVED

---

## Function Background

`_parse_routing_list()` is a new function to be created in v2.26. It does not currently exist in the codebase (search returned zero matches across all of `src/superclaude/cli/`).

The function parses a routing list (likely a structured list of task IDs or step identifiers from step output frontmatter or body content).

---

## Import Graph Analysis

### Option A: Place in `remediate.py`

**`src/superclaude/cli/roadmap/remediate.py` current imports:**
```python
from .models import Finding
```

**Impact of adding `_parse_routing_list()` to remediate.py:**
- No new imports required if the function takes `str` or `list[str]` as input
- `remediate.py` is a roadmap-layer module — within appropriate layer
- No circular import risk: remediate.py only imports from roadmap.models, not from gates.py or executor.py

**Risk:** LOW — remediate.py has minimal imports, clean boundary

### Option B: Extract to new `parsing.py`

**New file: `src/superclaude/cli/roadmap/parsing.py`**

**Impact:**
- Requires creating a new file
- Other modules that call `_parse_routing_list()` would import from `roadmap.parsing`
- Pure utility: no circular import risk
- But: adds a new file for a single function (violates simplicity preference unless more parsing functions are expected)

**Risk:** LOW (no circular imports) but adds unnecessary file proliferation

### Option C: Place in `gates.py`

**`src/superclaude/cli/roadmap/gates.py` current imports:**
```python
from ..pipeline.models import GateCriteria, SemanticCheck
```

**Impact of adding `_parse_routing_list()` to gates.py:**
- gates.py already imports `re` locally within semantic check functions
- Parsing utilities fit near gate semantic check lambdas
- If `_parse_routing_list()` is used by gate semantic checks, co-locating makes sense

**Risk:** LOW — gates.py has only pipeline.models import, no circular risk

---

## Decision

**Chosen placement: `remediate.py`**

**Rationale:**
1. `_parse_routing_list()` is used during remediation step construction — it parses routing data to determine which tasks need remediation steps built
2. `remediate.py` is the natural home: it contains `filter_findings()`, `generate_remediation_tasklist()` — all routing/filtering logic lives here
3. No new external dependencies required — the function is pure string/list parsing
4. No circular import introduced: remediate.py → roadmap.models only (verified)
5. Tie-breaker rule applied: "prefer remaining in remediate.py (no new external dependencies)"
6. Creating a new `parsing.py` for a single function violates scope discipline (build only what's needed)

**Import graph with chosen placement — no new dependencies:**
```
remediate.py imports:
  from .models import Finding    (existing)
  # _parse_routing_list() needs no new imports
```

---

## Phase 2 T02.03 Action

Add `_parse_routing_list()` to `src/superclaude/cli/roadmap/remediate.py` as a module-level private function. No new file creation required.

**Planned signature:**
```python
def _parse_routing_list(content: str) -> list[str]:
    """Parse a routing list from step output content, returning task IDs."""
```

---

## Summary

| Option | Placement | Circular Risk | New File | Chosen |
|--------|-----------|--------------|----------|--------|
| A | `remediate.py` | None | No | **YES** |
| B | new `parsing.py` | None | Yes | No |
| C | `gates.py` | None | No | No |
