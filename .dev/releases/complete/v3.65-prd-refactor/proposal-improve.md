# Improvement Proposal: Mitigate False Positives in Obligation Scanner

**Target**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Severity**: Gate false-positive blocking valid roadmap pipelines
**Scope**: Scanner regex enhancement + context-aware filtering; backward-compatible

---

## 1. Root Cause Analysis

The obligation scanner uses flat regex matching against SCAFFOLD_TERMS. It has no semantic understanding of whether a scaffold term represents an **actual obligation** ("create a mock runner") vs. a **meta-reference** to scaffold concepts ("ensure no mock data remains").

The false positive categories all share one structural trait: **the scaffold term is being referenced rather than instantiated**. Specifically:

### Category 1: Negation/Rejection Context
Lines that describe the *absence* or *prohibition* of scaffolding:
- "No template sentinel placeholders ({{, <placeholder>}) present"
- "ensure no mock data remains"
- "must not contain stub endpoints"
- "verify no hardcoded values"

**Pattern**: A negation word (no, not, never, without, ensure no, verify no, must not, reject) precedes the scaffold term within the same line.

### Category 2: Shell/Grep Commands
Lines where the scaffold term is a search target, not an obligation:
- `grep -rn '<placeholder>' src/`
- `find . -name '*mock*'`
- `sed -i 's/stub/real/g'`

**Pattern**: The scaffold term appears inside a shell command (grep, find, sed, awk, rg, ag) on the same line. These lines are already inside code blocks, and code blocks already demote to MEDIUM, but the demote-to-MEDIUM path still creates noise in the report.

### Category 3: Code Block Examples (Anti-patterns)
Code showing what NOT to do, or examples of what the scanner itself checks for:
- `# BAD: placeholder_value = "TODO"`

**Pattern**: Already handled by FR-MOD1.8 (code block demotion to MEDIUM, excluded from undischarged count). No further action needed.

### Category 4: Historical/Changelog References
- "removed the mock in v2.1"
- "deprecated the stub endpoint"

**Pattern**: Past-tense verbs (removed, deprecated, eliminated, replaced, deleted) precede or immediately follow the scaffold term. These are already-discharged references and should not create new obligations.

### Category 5: Risk/Warning Descriptions
- "risk: placeholder data could leak to production"

**Pattern**: Appears in lines containing risk/warning vocabulary (risk, warning, caution, danger, caveat, concern). The scaffold term describes a hypothetical, not a commitment.

### Category 6: Gate/Verification Criteria
- "Verification: no placeholder values in config"
- "Gate criterion: all stubs replaced"

**Pattern**: Lines containing verification/gate vocabulary (verification, gate, criterion, check, validate, assert, audit) combined with the scaffold term. These describe what to CHECK FOR, not what to BUILD.

### Why existing mitigations fall short

- `# obligation-exempt` requires the roadmap author to manually annotate every meta-reference line. This is fragile and defeats automation.
- Code block demotion (MEDIUM severity) covers Category 2 and 3 partially, but only when the author wraps commands in fenced blocks. Inline backtick commands are not covered.
- Neither mechanism addresses Categories 1, 4, 5, or 6.

---

## 2. Fix Recommendation: Negation-Aware Context Filter

### What to fix NOW (Phase 1)

Add a **negation/meta-context detection pass** that auto-demotes matches to MEDIUM before the discharge search. This covers Categories 1, 4, 5, and 6 with a single mechanism. Category 2 is already handled by code-block demotion. Category 3 is already handled.

**Implementation**: Add a `_is_meta_context(line: str, match_start: int) -> bool` function that returns True when the scaffold term appears in a meta-reference context. When True, severity is set to MEDIUM (same treatment as code blocks), which excludes it from `undischarged_count`.

```python
# New negation/meta-context patterns (compile once at module level)
_NEGATION_PREFIX_RE = re.compile(
    r"\b(?:no|not|never|without|ensure\s+no|verify\s+no|must\s+not|"
    r"reject|prohibit|forbid|prevent|disallow|eliminate|absent|"
    r"removed?|deprecated?|eliminated?|replaced?|deleted?|"
    r"risk|warning|caution|danger|caveat|concern|"
    r"verificat\w*|gate\s+criteri\w*|check\s+(?:for|that)|"
    r"validate|assert|audit)\b",
    re.IGNORECASE,
)

_SHELL_CMD_RE = re.compile(
    r"(?:grep|find|sed|awk|rg|ag|xargs|git\s+grep)\s+",
    re.IGNORECASE,
)


def _is_meta_context(line: str, term_start_in_line: int) -> bool:
    """Detect if scaffold term appears in a meta/negation context.

    Returns True when the line contains negation, verification,
    historical, risk, or shell-command patterns that indicate the
    scaffold term is being REFERENCED rather than INSTANTIATED.
    """
    # Check for negation/meta prefix anywhere before the term in the line
    prefix = line[:term_start_in_line]
    if _NEGATION_PREFIX_RE.search(prefix):
        return True

    # Check for shell commands on the line
    if _SHELL_CMD_RE.search(line):
        return True

    return False
```

**Integration point** in `scan_obligations()`, after line 139 (severity determination):

```python
# NEW: Meta-context demotion (covers negation, verification, historical, risk)
if severity == "HIGH":
    term_start_in_line = context_line.lower().find(term.lower())
    if term_start_in_line >= 0 and _is_meta_context(context_line, term_start_in_line):
        severity = "MEDIUM"
```

This slots in after the existing code-block check and before the discharge search. The logic is: if the code-block check already set MEDIUM, skip; otherwise, check for meta-context.

### What to defer (Phase 2)

1. **Whole-line semantic scoring**: Instead of binary meta-context detection, assign a confidence score to each match. Scaffold terms with low confidence (many meta-context signals) get demoted. This would be more nuanced but adds complexity.

2. **Configurable term lists**: Allow roadmap authors to extend SCAFFOLD_TERMS and DISCHARGE_TERMS via frontmatter. Useful for domain-specific vocabulary, but out of scope for the false-positive fix.

3. **Full-sentence NLP parsing**: Use dependency parsing to determine whether the scaffold term is the *object* of a creation verb vs. a negation verb. Requires an NLP dependency; not justified for a gate scanner.

---

## 3. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Over-filters: real obligation demoted to MEDIUM | Low | Medium | Negation prefix must appear BEFORE the term on the same line. "Create a mock that has no tests" would match "no" before "tests", not before "mock" -- the positional constraint prevents this. |
| Under-filters: novel meta-context pattern missed | Medium | Low | The `# obligation-exempt` escape hatch still works. New patterns can be added to the regex incrementally. |
| Regex performance degradation | Very Low | Very Low | Single compiled regex, checked once per match (already O(N) in match count). |
| Backward compatibility break | Very Low | High | The change only DEMOTES severity from HIGH to MEDIUM. No existing MEDIUM or exempt behavior changes. Roadmaps that previously passed will still pass. Roadmaps that previously failed due to meta-context false positives will now pass. |

**Key safety property**: The fix can only REDUCE false positives (by demoting to MEDIUM). It cannot introduce false negatives because it never marks an obligation as discharged -- it only changes severity classification.

---

## 4. Estimated Diff Size

| File | Change | Lines |
|------|--------|-------|
| `obligation_scanner.py` | Add `_NEGATION_PREFIX_RE`, `_SHELL_CMD_RE`, `_is_meta_context()`, integration in `scan_obligations()` | +35-40 |
| `tests/roadmap/test_anti_instinct_integration.py` | Add test class for meta-context demotion (6-8 test cases covering each category) | +80-100 |
| Total | | ~120-140 lines |

No changes to `gates.py`, `pipeline/gates.py`, or `pipeline/models.py`. The fix is entirely contained within the scanner module and its tests.

---

## 5. Test Plan

New test cases to add:

1. **Negation prefix**: "No placeholder values in config" -- term should be MEDIUM
2. **Ensure-no pattern**: "ensure no mock data remains" -- term should be MEDIUM
3. **Must-not pattern**: "must not contain stub endpoints" -- term should be MEDIUM
4. **Past-tense historical**: "removed the mock in v2.1" -- term should be MEDIUM
5. **Risk context**: "risk: placeholder data could leak" -- term should be MEDIUM
6. **Verification context**: "Verification: no placeholder values" -- term should be MEDIUM
7. **Shell command**: "grep -rn 'placeholder' src/" (inside code block) -- term should be MEDIUM
8. **True positive preserved**: "Create mock step runners" -- term should remain HIGH
9. **Positional safety**: "Build mock that has no fallback" -- "mock" should remain HIGH (the negation "no" comes AFTER "mock", before "fallback")
10. **Full pipeline**: Roadmap with only meta-context scaffold terms should pass the gate
