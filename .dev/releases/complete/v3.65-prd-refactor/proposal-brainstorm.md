# Brainstorm: Mitigating False Positives in the Obligation Scanner

**Date**: 2026-04-03
**Scanner**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Gate**: `_no_undischarged_obligations` in `src/superclaude/cli/roadmap/gates.py`
**Branch**: `feat/tdd-spec-merge`

---

## Problem Statement

The obligation scanner matches scaffold terms (`mock`, `stub`, `placeholder`, `skeleton`, `temporary`, `hardcoded`, `fake`, etc.) in roadmap markdown and requires each to be "discharged" by a corresponding action verb in a later phase. The scanner produces false positives when scaffold vocabulary appears in **meta-contexts** -- text that discusses, checks for, or references scaffolding rather than creating scaffolding obligations.

### The Six Meta-Context Categories

| # | Category | Example | Why It's False |
|---|----------|---------|----------------|
| 1 | **Verification/gate criteria** | `No template sentinel placeholders ({{, <placeholder>, TODO) present` | Describes what to *reject*, not what to *create* |
| 2 | **Shell commands** | `grep -rn '<placeholder>' src/` | Search target in a command, not an obligation |
| 3 | **Code block anti-patterns** | `` ```# BAD: mock_data = {...}``` `` | Shows what NOT to do |
| 4 | **Negative assertions** | `must not contain placeholder data` | Instruction to *remove/prevent*, not create |
| 5 | **Historical/changelog refs** | `removed the mock service in v2.1` | Past tense, already resolved |
| 6 | **Risk descriptions** | `risk: placeholder data could leak to production` | Describing a risk, not creating scaffolding |

### Current Mitigations and Their Gaps

- **`# obligation-exempt`** -- requires roadmap authors to manually annotate every meta-context line. Fragile; authors forget; new roadmaps don't know to add it.
- **Code block demotion to MEDIUM** -- only applies inside fenced code blocks (```` ``` ````), and only demotes severity. Does not cover inline code, bullet items describing verification criteria, or any of the other five categories.

---

## Alternative Solutions

### Alternative A: Negation-Context Regex Pre-Filter

**Approach**: Before recording a scaffold match, check whether the matched term appears within a negation context on the same line. Define a set of negation patterns that indicate meta-usage.

```python
_NEGATION_PREFIXES = [
    r"(?:no|not?|never|without|remove|reject|ensure\s+no|verify\s+no|check\s+(?:for\s+)?no)",
    r"(?:must\s+not|should\s+not|shall\s+not|cannot|don'?t)",
    r"(?:grep|sed|awk|find|rg)\s+.*",       # shell commands
    r"(?:removed|eliminated|replaced|deleted)",  # past-tense resolution
    r"(?:risk|warning|caution|danger)\s*:",      # risk descriptions
]
_NEGATION_CONTEXT_RE = re.compile(
    r"(?:" + "|".join(_NEGATION_PREFIXES) + r")\s+.*\b(?:" + "|".join(SCAFFOLD_TERMS) + r")",
    re.IGNORECASE,
)
```

If the line matches a negation context, mark the obligation as `exempt=True` (or skip recording it entirely).

**Pros**:
- Zero author burden -- fully automatic
- Covers categories 1, 2, 4, 5, 6 with one mechanism
- Pure regex, no new dependencies
- Backward-compatible -- only suppresses false positives, never blocks new true positives

**Cons**:
- Regex complexity grows over time as new negation patterns emerge
- Risk of over-suppression if negation patterns are too broad (e.g., "no" is common)
- Cannot handle multi-line negation contexts ("The following must not exist:\n- placeholder data")
- Fragile against natural language variation

**Estimated diff**: ~40 lines in obligation_scanner.py + ~30 lines of tests

---

### Alternative B: Sentence-Level Semantic Classification

**Approach**: For each line containing a scaffold term, classify the surrounding sentence as either "obligation-creating" (imperative future: "create a mock", "add placeholder") or "meta-reference" (negation, verification, historical). Use a lightweight heuristic classifier based on verb tense and sentence structure.

```python
def _is_obligation_creating(line: str, term_match: re.Match) -> bool:
    """Classify whether a scaffold term creates an obligation or is meta-context."""
    line_lower = line.lower()

    # Category 4+1: Negation/verification context
    if re.search(r"\b(no|not|never|without|ensure|verify|check|reject|must\s+not)\b", line_lower):
        # Term appears after a negation -- meta-context
        neg_match = re.search(r"\b(no|not|never|without|ensure|verify|check|reject)\b", line_lower)
        if neg_match and neg_match.start() < term_match.start():
            return False

    # Category 5: Past-tense resolution
    if re.search(r"\b(removed|replaced|eliminated|deleted|swapped|migrated)\b", line_lower):
        return False

    # Category 2: Shell command context
    if re.search(r"^\s*(?:grep|sed|awk|find|rg|ag|git\s+grep)\b", line_lower):
        return False
    if re.search(r"[`$]\s*(?:grep|sed|awk|find|rg)", line_lower):
        return False

    # Category 6: Risk/warning framing
    if re.search(r"^\s*(?:risk|warning|caution|note|caveat)\s*:", line_lower):
        return False

    return True  # Default: assume obligation-creating
```

**Pros**:
- More precise than pure prefix matching -- considers positional relationship between negation and scaffold term
- Extensible classification function with clear per-category logic
- Each category maps to a named, testable condition
- Fail-open default (assume obligation-creating) preserves safety

**Cons**:
- Still heuristic -- English is ambiguous
- Positional check (negation before term) can be fooled by complex sentences
- Does not handle cross-line contexts
- Moderate complexity

**Estimated diff**: ~60 lines in obligation_scanner.py + ~50 lines of tests

---

### Alternative C: Line-Level Context Tags (Structured Markdown Convention)

**Approach**: Define a lightweight markdown convention where roadmap authors can tag lines or sections with context markers that the scanner recognizes.

```markdown
<!-- context: verification -->
- No placeholder data remains in production config
<!-- /context -->

## Phase 3: Verification Gate
<!-- obligation-scope: none -->
- Verify all mocks have been replaced
- Ensure no stub endpoints remain
```

The scanner would parse these HTML comments and skip scaffold-term detection within tagged regions.

**Pros**:
- Explicit and unambiguous -- no heuristic guessing
- Authors can tag entire sections (verification gates, changelogs)
- Composable with existing `# obligation-exempt` for single lines
- Zero false-positive risk within tagged regions

**Cons**:
- Requires author discipline (same problem as `# obligation-exempt`, just at section level)
- Adds visual noise to roadmaps
- New roadmaps from LLM prompts won't include these tags unless the prompt template adds them
- Doesn't solve the problem for existing roadmaps without migration

**Estimated diff**: ~30 lines in obligation_scanner.py + ~20 lines of tests + prompt template updates

---

### Alternative D: Code Block Full Exemption + Inline Code Exemption

**Approach**: Upgrade the existing code block demotion (MEDIUM severity) to full exemption, and also exempt scaffold terms that appear inside inline backtick spans (`` `placeholder` ``). This handles categories 2 and 3 fully, and partially handles category 1 when authors use backticks in verification criteria.

```python
_INLINE_CODE_RE = re.compile(r"`[^`]+`")

def _is_inside_inline_code(line: str, match_start: int, match_end: int) -> bool:
    for m in _INLINE_CODE_RE.finditer(line):
        if m.start() <= match_start and match_end <= m.end():
            return True
    return False
```

Change `_determine_severity` to return `"EXEMPT"` instead of `"MEDIUM"` for code blocks, and add inline code detection.

**Pros**:
- Simple, minimal change
- Code block exemption is clearly correct -- code examples are never obligations
- Inline code exemption handles many verification criteria (e.g., `No \`placeholder\` values`)
- No heuristic language analysis needed

**Cons**:
- Only fully covers categories 2 and 3
- Categories 1, 4, 5, 6 remain unaddressed unless authors happen to use backticks
- Incomplete solution -- would need to be combined with another approach

**Estimated diff**: ~15 lines in obligation_scanner.py + ~15 lines of tests

---

### Alternative E: Prompt-Side Prevention (Roadmap Generation Template Fix)

**Approach**: Instead of fixing the scanner, fix the roadmap generator prompts so that LLM-generated roadmaps either (a) use `# obligation-exempt` annotations on meta-context lines, or (b) avoid scaffold vocabulary in verification/gate sections entirely.

Add to the roadmap generation prompt:
```
IMPORTANT: When writing verification criteria or gate checks, do NOT use scaffold
vocabulary (mock, stub, placeholder, skeleton, etc.) directly. Instead use phrasing
like "no sentinel values remain" or "all temporary constructs have been replaced".
Alternatively, append `# obligation-exempt` to any line that references scaffold
terms in a meta/verification context.
```

**Pros**:
- Zero scanner changes needed
- Addresses root cause (the roadmap content itself)
- Works for all future roadmaps

**Cons**:
- Does not fix existing roadmaps
- LLMs may not consistently follow the instruction
- Fragile -- prompt changes can regress
- Transfers the burden to prompt engineering, which is harder to test
- Does not help with manually-written roadmaps

**Estimated diff**: ~10 lines in prompt templates, 0 lines in scanner

---

### Alternative F: Composite Approach (Recommended)

**Approach**: Combine the strongest elements of A, B, and D into a layered defense:

**Layer 1 -- Code Context Exemption** (from D): Fully exempt scaffold terms inside fenced code blocks and inline backtick spans. These are never obligations.

**Layer 2 -- Negation-Aware Classification** (from B, refined): For remaining matches, apply a lightweight classifier that checks whether the scaffold term appears in a negation/meta context on the same line. Use positional awareness (negation word must precede the scaffold term).

**Layer 3 -- Existing Escape Hatches**: Keep `# obligation-exempt` as the manual override for edge cases that escape Layers 1-2.

Implementation sketch:

```python
# New: patterns that indicate meta-context (not obligation-creating)
_META_CONTEXT_INDICATORS = [
    # Negation/verification: "no placeholder", "must not contain mock"
    re.compile(r"\b(?:no|not?|never|without|ensure\s+no|verify\s+no|must\s+not|should\s+not|shall\s+not|check\s+(?:for\s+)?no|reject)\b", re.IGNORECASE),
    # Past-tense resolution: "removed the mock", "replaced placeholder"
    re.compile(r"\b(?:removed|replaced|eliminated|deleted|swapped out|migrated away from)\b", re.IGNORECASE),
    # Risk/warning framing
    re.compile(r"^\s*(?:risk|warning|caution|note|caveat)\s*:", re.IGNORECASE),
]

# Shell command line detection
_SHELL_CMD_RE = re.compile(
    r"(?:^\s*[$>]?\s*)?(?:grep|sed|awk|find|rg|ag|git\s+grep|xargs)\b",
    re.IGNORECASE,
)

def _is_meta_context(line: str, term_start_in_line: int) -> bool:
    """Determine if a scaffold term on this line is in a meta-context (not an obligation)."""
    # Shell command lines are always meta-context
    if _SHELL_CMD_RE.search(line):
        return True

    # Check if a negation/meta indicator PRECEDES the scaffold term on this line
    for pattern in _META_CONTEXT_INDICATORS:
        m = pattern.search(line)
        if m and m.start() < term_start_in_line:
            return True

    return False
```

Integration point in `scan_obligations()`: after the existing exempt/severity checks, add:

```python
# Layer 1: Code context exemption (upgrade from MEDIUM demotion)
if severity == "MEDIUM":  # inside code block
    exempt = True

# Layer 1b: Inline code exemption
if _is_inside_inline_code(context_line, ...):
    exempt = True

# Layer 2: Negation-aware meta-context detection
if _is_meta_context(context_line, term_position_in_line):
    exempt = True
```

**Pros**:
- Covers all six meta-context categories automatically
- Layered defense: each layer is simple and testable independently
- Code block exemption is 100% precise (no false negatives)
- Negation check uses positional awareness to avoid over-suppression
- Preserves manual override for edge cases
- Backward-compatible -- only suppresses false positives
- Pure function, no I/O, no new dependencies
- Fail-safe default: if no meta-context detected, term is treated as obligation

**Cons**:
- More code than any single alternative (~80 lines)
- Negation heuristic still imperfect for complex English
- Multi-line negation contexts remain unhandled (acceptable trade-off)

**Estimated diff**: ~80 lines in obligation_scanner.py + ~80 lines of tests

---

## Edge Cases Considered

### 1. Double negation: "do not skip the placeholder replacement step"
- "not" precedes "placeholder" -- would the classifier wrongly exempt it?
- **Mitigation**: The phrase "placeholder replacement step" describes an action to TAKE, and the negation "do not skip" reinforces it. However, the classifier checks if negation precedes the scaffold term positionally. This WOULD be a false negative (missed true obligation).
- **Severity**: Low. This phrasing is rare in roadmaps. The `# obligation-exempt` inverse (no annotation = obligation) handles it correctly by default since the classifier is fail-safe.
- **Accepted risk**: The classifier only marks meta-context; default is obligation-creating. A double negation keeps the term as an obligation, which is the safe direction.

Wait -- re-reading the logic: "do not skip the placeholder replacement step" -- "not" appears before "placeholder". The classifier would mark this as meta-context. This IS a false negative.

**Fix**: Require the negation word to be within N tokens (say 3 words) of the scaffold term, not just anywhere before it on the line. This would exclude "do not skip the placeholder" because "not" is 3+ words away from "placeholder". Refine:

```python
# Only match if negation is within 4 words of the scaffold term
words_before = line[:term_start_in_line].split()
recent_words = words_before[-4:] if len(words_before) >= 4 else words_before
if any(neg_re.search(w) for w in recent_words):
    return True
```

### 2. Scaffold term in a heading: "## Phase 3: Replace Mock Services"
- "Replace Mock" -- this IS a discharge action, not an obligation. The scanner already handles this because the discharge term "replace" would appear in a later phase section.
- But "Mock" here would also be detected as a scaffold term in Phase 3 itself. Since there's no later phase to discharge it, it would be flagged.
- **Mitigation**: The heading describes a DISCHARGE action. The classifier should recognize "replace mock" as a discharge context, not an obligation context. Add discharge verbs to the meta-context indicators.

### 3. Mixed line: "Create placeholder config, then verify no placeholder values leak"
- Two occurrences: first is a real obligation, second is meta-context.
- **Handling**: The classifier runs per-match, checking the position of each match against preceding negation words. First "placeholder" has no negation before it (obligation). Second "placeholder" has "no" before it (meta-context). Correctly classified.

### 4. Inline code in verification: "Ensure `mock_service` is not in the import list"
- The backtick span exempts "mock" (Layer 1b). Correct -- this is a check instruction, not an obligation.

### 5. Ambiguous: "temporary workaround for auth flow"
- No negation, no code block, no shell command. Classified as obligation. This IS a real obligation -- temporary workarounds should be discharged. Correct.

### 6. Changelog in roadmap: "v2.0: removed all stub implementations"
- "removed" (past tense) precedes "stub". Layer 2 detects past-tense resolution. Correctly exempted.

### 7. Risk section: "Risk: hardcoded credentials could be exposed"
- "Risk:" prefix detected by the risk/warning pattern. Correctly exempted.

### 8. Quoted scaffold term: `"placeholder"` (in regular text, not backticks)
- Not inside backticks or code block. Would need the negation layer to catch it. If the line is `Reject any values matching "placeholder"`, the word "Reject" would be caught by the negation indicator. Works.

### 9. Term at line start: "Placeholder config file created in Phase 1"
- No negation precedes it. Classified as obligation. Correct -- this IS an obligation.

### 10. Scanner self-reference in a generated audit: "Obligation scanner found 3 mock references"
- The audit file is a DIFFERENT file from the roadmap. The scanner only runs on roadmap content, not on its own output. Not a concern.

---

## Recommendation

**Alternative F (Composite Approach)** is the recommended solution.

### Rationale

1. **Coverage breadth**: It handles all six meta-context categories, not just a subset.
2. **Safety**: Fail-safe default (assume obligation) means false negatives only occur in the narrow double-negation edge case, which can be further mitigated with proximity-based negation matching.
3. **Layered testability**: Each layer (code exemption, negation classification, manual override) can be unit-tested independently.
4. **No author burden**: Unlike alternatives C and E, authors don't need to learn new conventions or modify existing roadmaps.
5. **Backward compatibility**: Existing roadmaps that pass today will still pass. Existing roadmaps that fail due to false positives will now pass (the desired outcome).
6. **Incremental deployment**: Layer 1 (code block full exemption) can ship independently as a quick win, with Layer 2 following in the same or next release.

### Implementation Order

1. **Quick win** (~15 lines): Upgrade code block handling from severity demotion to full exemption + add inline code exemption. This alone fixes categories 2 and 3.
2. **Full fix** (~65 additional lines): Add `_is_meta_context()` classifier for categories 1, 4, 5, 6.
3. **Refinement** (optional, ~10 lines): Add proximity-based negation matching to handle double-negation edge case.

### Total Estimated Diff

- `obligation_scanner.py`: +80 lines (new functions + integration)
- `tests/roadmap/test_obligation_scanner.py` (new or extended): +80 lines
- Total: ~160 lines changed/added
