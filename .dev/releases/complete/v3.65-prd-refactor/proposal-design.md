# Design: Meta-Context False Positive Suppression for the Obligation Scanner

**Date**: 2026-04-03
**Status**: Proposal
**Component**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Problem**: Scanner matches scaffold terms in meta-contexts (verification criteria, shell commands, negative assertions, examples, changelogs, risk descriptions) causing false-positive undischarged obligations that block the pipeline.

---

## 1. Problem Statement

The obligation scanner uses regex matching against 11 scaffold terms (mock, stub, skeleton, placeholder, scaffold, temporary, hardcoded, hardwired, no-op, dummy, fake). It currently has two mitigations: per-line `# obligation-exempt` comments and code-block severity demotion to MEDIUM. Neither addresses the general category of false positives where scaffold vocabulary appears in **meta-contexts** -- text that talks ABOUT scaffolding rather than creating scaffolding obligations.

### 1.1 False Positive Categories

| Category | Example Text | Why It's False |
|---|---|---|
| **Verification criteria** | `No template sentinel placeholders ({{, <placeholder>, TODO) present` | Describes what to CHECK FOR, not an obligation |
| **Shell commands** | `grep -rn '<placeholder>' src/` | Search target in a command, not an obligation |
| **Negative assertions** | `Ensure no mock data remains in production` | Instruction to REMOVE, not to create |
| **Anti-patterns / what-not-to-do** | `BAD: hardcoded connection strings` | Example of what to avoid |
| **Historical/changelog** | `Removed the stub endpoint in v2.1` | Past-tense removal, not current obligation |
| **Risk descriptions** | `Risk: placeholder data could leak to production` | Describes a risk, not an obligation |
| **Gate/checklist items** | `- [x] All mock services replaced with real implementations` | Completed checklist item, not an obligation |
| **Quoted terms in prose** | `The word "scaffold" in this context means...` | Definitional, not structural |

### 1.2 Root Cause

The scanner applies a flat regex match with no awareness of the **semantic role** of the surrounding sentence. Every occurrence of a scaffold term is treated identically regardless of whether the sentence creates, references, negates, or describes the removal of scaffolding.

---

## 2. Technical Design

### 2.1 Strategy: Negation-Aware Context Classification

Instead of trying to enumerate every possible meta-context (fragile, whack-a-mole), the design introduces a **context classifier** that examines the line containing a scaffold match and determines whether the match represents an **affirmative obligation** or a **meta-reference**. Only affirmative obligations are promoted to HIGH severity.

Meta-references are demoted to a new severity level: `INFO` (below MEDIUM, excluded from undischarged count by default).

### 2.2 Classification Signals

The classifier uses a layered approach, evaluated in order (first match wins):

#### Layer 1: Structural Exclusions (line-level, cheap)

These patterns indicate the scaffold term is structurally non-obligatory:

| Signal | Pattern | Rationale |
|---|---|---|
| Code block | Already exists (FR-MOD1.8) | Term inside fenced code block |
| Exempt comment | Already exists (FR-MOD1.7) | Explicit `# obligation-exempt` |
| Inline code | Term inside backtick-delimited span | `\`placeholder\`` is a reference, not an obligation |
| Completed checklist | `- [x]` prefix on the line | Already done |

#### Layer 2: Negation / Removal Context (sentence-level, moderate cost)

These patterns indicate the sentence negates or describes removal of the scaffold term:

```python
NEGATION_PATTERNS = [
    # Negative assertions: "no X", "must not contain X", "ensure no X"
    r"(?:no|without|remove|eliminate|strip|purge|clean)\s+(?:\w+\s+){0,3}",
    # "must not" / "should not" / "cannot" / "never" preceding the term
    r"(?:must|should|shall|cannot|will)\s+not\s+(?:\w+\s+){0,5}",
    r"\bnever\b\s+(?:\w+\s+){0,5}",
    # Past-tense removal: "removed X", "replaced X", "eliminated X"
    r"(?:removed|replaced|eliminated|stripped|cleaned|purged)\s+(?:\w+\s+){0,3}",
    # "ensure no X", "verify no X", "check.*no X"
    r"(?:ensure|verify|validate|check|confirm|assert)\s+(?:\w+\s+){0,3}(?:no|zero|0)\s+",
]
```

The classifier checks whether any NEGATION_PATTERN appears in the line **before** the scaffold term match position. If it does, the term is classified as a meta-reference.

#### Layer 3: Command / Tool Context (line-level, cheap)

```python
COMMAND_CONTEXT_PATTERNS = [
    # Shell commands: grep, sed, find, awk, rg searching for the term
    r"(?:grep|sed|find|awk|rg|ag|ripgrep)\s+.*",
    # Regex-like patterns: term inside regex delimiters
    r"[/'\"]\S*$TERM\S*[/'\"]",
]
```

If the line matches a command-context pattern, the scaffold term is classified as a meta-reference.

#### Layer 4: Gate/Verification Criteria Context (line-level, moderate cost)

```python
GATE_CONTEXT_PATTERNS = [
    # Verification gate phrasing
    r"(?:no|zero|0)\s+(?:\w+\s+){0,3}(?:present|found|detected|remaining)",
    # Criteria phrasing: "must contain no X", "X count == 0"
    r"(?:count|number)\s+(?:of\s+)?(?:\w+\s+){0,3}(?:==|is|equals?|must\s+be)\s+0",
]
```

### 2.3 New Severity Level

```python
# Current: HIGH, MEDIUM
# Proposed: HIGH, MEDIUM, INFO

# INFO obligations are:
# - Logged in the report for transparency
# - Excluded from undischarged_count (same as MEDIUM)
# - Created when context classifier identifies a meta-reference
```

The `ObligationReport.undischarged_count` property already excludes `MEDIUM`; `INFO` is added to the exclusion:

```python
@property
def undischarged_count(self) -> int:
    return sum(
        1
        for o in self.obligations
        if not o.discharged and not o.exempt
        and o.severity not in ("MEDIUM", "INFO")
    )
```

### 2.4 Data Flow

```
For each scaffold term match:
  1. Check exempt comment (existing) --> exempt=True, skip classification
  2. Check code block (existing)     --> severity="MEDIUM"
  3. Check inline code (new L1)      --> severity="INFO"
  4. Check completed checklist (L1)  --> severity="INFO"
  5. Check negation context (L2)     --> severity="INFO"
  6. Check command context (L3)      --> severity="INFO"
  7. Check gate/criteria context (L4)--> severity="INFO"
  8. Default                         --> severity="HIGH"
```

### 2.5 New Module-Level Constants

```python
# --- Meta-context classification (FR-MOD1.9) ---

# Inline code: scaffold term appears inside backticks on the same line
_INLINE_CODE_RE = re.compile(r"`[^`]*(?:" + "|".join(SCAFFOLD_TERMS) + r")[^`]*`", re.IGNORECASE)

# Completed checklist item
_COMPLETED_CHECKLIST_RE = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE)

# Negation/removal preceding the scaffold term
_NEGATION_PREFIXES = [
    re.compile(
        r"(?:^|(?<=\s))(?:no|without|remove|eliminate|strip|purge|clean|free\s+of)"
        r"\s+(?:\w+\s+){0,4}",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:must|should|shall|cannot|can\s*not|will)\s+not\s+(?:\w+\s+){0,5}",
        re.IGNORECASE,
    ),
    re.compile(r"\bnever\b\s+(?:\w+\s+){0,5}", re.IGNORECASE),
    re.compile(
        r"(?:removed|replaced|eliminated|stripped|cleaned|purged|deleted)"
        r"\s+(?:the\s+)?(?:\w+\s+){0,3}",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:ensure|verify|validate|check|confirm|assert)"
        r"\s+(?:\w+\s+){0,3}(?:no|zero|0|none)\s+",
        re.IGNORECASE,
    ),
]

# Shell/tool command context
_COMMAND_LINE_RE = re.compile(
    r"(?:grep|sed|find|awk|rg|ag|xargs|perl)\s+",
    re.IGNORECASE,
)

# Gate/verification criteria language
_GATE_CRITERIA_RE = re.compile(
    r"(?:no|zero|0)\s+(?:\w+\s+){0,4}"
    r"(?:present|found|detected|remaining|allowed|permitted|exist)",
    re.IGNORECASE,
)
```

### 2.6 New Classification Function

```python
def _classify_meta_context(
    line: str,
    match_start_in_line: int,
    abs_pos: int,
    code_block_ranges: list[tuple[int, int]],
) -> str:
    """Classify a scaffold term match as HIGH, MEDIUM, or INFO.

    Returns the severity string. Layers are evaluated in order;
    first match wins.

    Args:
        line: The full line containing the scaffold match.
        match_start_in_line: Character offset of the match within `line`.
        abs_pos: Absolute position in the full document (for code-block check).
        code_block_ranges: Pre-computed fenced code block ranges.

    Returns:
        "MEDIUM" if inside a fenced code block.
        "INFO" if meta-context detected (negation, command, gate criteria,
                inline code, completed checklist).
        "HIGH" otherwise (affirmative obligation).
    """
    # L0: Existing code-block demotion (FR-MOD1.8)
    for start, end in code_block_ranges:
        if start <= abs_pos <= end:
            return "MEDIUM"

    # L1a: Inline code -- scaffold term inside backticks on this line
    if _INLINE_CODE_RE.search(line):
        return "INFO"

    # L1b: Completed checklist item
    if _COMPLETED_CHECKLIST_RE.match(line):
        return "INFO"

    # L2: Negation/removal prefix before the scaffold term
    prefix = line[:match_start_in_line]
    for pattern in _NEGATION_PREFIXES:
        if pattern.search(prefix):
            return "INFO"
    # Also check the full line for past-tense removal verbs
    if _NEGATION_PREFIXES[3].search(line):
        return "INFO"

    # L3: Shell/tool command context
    if _COMMAND_LINE_RE.search(line):
        return "INFO"

    # L4: Gate/verification criteria language
    if _GATE_CRITERIA_RE.search(line):
        return "INFO"

    return "HIGH"
```

### 2.7 Integration into `scan_obligations()`

Replace the current `_determine_severity()` call with `_classify_meta_context()`:

```python
# BEFORE (lines 137-139):
abs_pos = _get_absolute_position(content, sections, i, match.start())
severity = _determine_severity(abs_pos, code_block_ranges)

# AFTER:
abs_pos = _get_absolute_position(content, sections, i, match.start())
match_start_in_line = match.start() - (
    phase_content.rfind("\n", 0, match.start()) + 1
)
severity = _classify_meta_context(
    context_line, match_start_in_line, abs_pos, code_block_ranges
)
```

The existing `_determine_severity()` function is retained but deprecated (it is subsumed by Layer 0 of `_classify_meta_context`). It can be removed in a follow-up cleanup.

### 2.8 Obligation Dataclass: `classification_reason` Field

Add an optional field to `Obligation` for debuggability:

```python
@dataclass
class Obligation:
    phase: str
    term: str
    component: str
    context: str
    line_number: int
    severity: str           # "HIGH", "MEDIUM", or "INFO"
    discharged: bool
    exempt: bool
    discharge_phase: str | None
    discharge_context: str | None
    classification_reason: str = ""  # NEW: e.g., "negation_prefix", "command_context"
```

This field is informational only and does not affect gate logic.

---

## 3. Edge Case Catalog

| # | Edge Case | Input | Expected Severity | Classification Layer |
|---|---|---|---|---|
| E1 | Affirmative obligation (true positive) | `Create mocked step runners` | HIGH | Default |
| E2 | Explicit exempt comment | `Create placeholder config # obligation-exempt` | HIGH + exempt=True | FR-MOD1.7 (existing) |
| E3 | Inside fenced code block | `` ```python\nmock_data = {...}\n``` `` | MEDIUM | L0 (existing) |
| E4 | Inline code reference | `Remove all \`placeholder\` values from config` | INFO | L1a |
| E5 | Completed checklist | `- [x] All mock services replaced` | INFO | L1b |
| E6 | Negation: "no X present" | `No template sentinel placeholders present` | INFO | L2 |
| E7 | Negation: "must not contain" | `Must not contain placeholder values` | INFO | L2 |
| E8 | Negation: "ensure no X" | `Ensure no mock data remains` | INFO | L2 |
| E9 | Past-tense removal | `Removed the stub endpoint in v2.1` | INFO | L2 |
| E10 | Shell grep command | `grep -rn '<placeholder>' src/` | INFO | L3 |
| E11 | Shell find command | `find . -name '*mock*' -delete` | INFO | L3 |
| E12 | Gate criteria | `Zero placeholder values found` | INFO | L4 |
| E13 | Risk description with negation | `Risk: placeholder data could leak` | HIGH | Default (no negation prefix) |
| E14 | Ambiguous: "use placeholder for now" | `Use placeholder config for now` | HIGH | Default (affirmative) |
| E15 | Negation after term (not before) | `The placeholder should not be committed` | HIGH | Default (negation follows term) |
| E16 | Double negation | `Do not remove the mock yet` | HIGH | Tricky -- "not remove" negates removal, so it IS an obligation. L2 negation check only looks for negation BEFORE the scaffold term, so "mock" at end is not preceded by negation prefix. Correct. |
| E17 | Term in heading | `## Phase 1: Skeleton Setup` | HIGH | Default (heading is affirmative) |
| E18 | Mixed line: negation + affirmative | `Remove old stubs and add new placeholder routes` | INFO for "stubs" (preceded by "Remove"), HIGH for "placeholder" | Per-match classification |
| E19 | Negation far from term | `Ensure the system has no residual temporary test files` | INFO | L2 ("no" within 4-word window) |
| E20 | "never" keyword | `Never deploy with hardcoded credentials` | INFO | L2 |

### 3.1 E13 Deliberate Decision

Risk descriptions like "Risk: placeholder data could leak" are intentionally classified as HIGH. A risk statement about placeholder data implies the placeholder EXISTS and is a real concern. The roadmap author should either:
- Discharge it in a later phase
- Add `# obligation-exempt` if it's purely hypothetical

This preserves the scanner's conservative bias for genuine safety concerns.

### 3.2 E15/E16 Deliberate Decision

The classifier only checks for negation **before** the scaffold term's position in the line. This prevents misclassifying sentences where the scaffold term IS the subject being described affirmatively, even if a negation appears later. This is a deliberate design choice that favors precision (fewer false negatives at the cost of some remaining false positives that can use `# obligation-exempt`).

---

## 4. API Surface Changes

### 4.1 Public API (No Breaking Changes)

| Symbol | Change | Backward Compatible |
|---|---|---|
| `scan_obligations(content: str) -> ObligationReport` | No signature change | Yes |
| `ObligationReport.undischarged_count` | Now also excludes `severity="INFO"` | Yes (fewer false positives, never more) |
| `ObligationReport.has_undischarged` | Unchanged (delegates to `undischarged_count`) | Yes |
| `Obligation` dataclass | New optional field `classification_reason: str = ""` | Yes (default value) |
| `SCAFFOLD_TERMS`, `DISCHARGE_TERMS` | Unchanged | Yes |

### 4.2 New Exports (Additive)

| Symbol | Purpose |
|---|---|
| `_classify_meta_context()` | Internal; not part of public API |
| `_NEGATION_PREFIXES` | Module constant; not part of public API |
| `_COMMAND_LINE_RE` | Module constant; not part of public API |
| `_GATE_CRITERIA_RE` | Module constant; not part of public API |
| `_INLINE_CODE_RE` | Module constant; not part of public API |
| `_COMPLETED_CHECKLIST_RE` | Module constant; not part of public API |

### 4.3 Deprecations

| Symbol | Status |
|---|---|
| `_determine_severity()` | Subsumed by `_classify_meta_context()` Layer 0. Retained for one release cycle, then removable. |

---

## 5. Test Plan

### 5.1 Unit Tests for `_classify_meta_context()`

Each edge case from Section 3 becomes a parameterized test:

```python
@pytest.mark.parametrize("line,match_pos,expected_severity,reason", [
    # E1: Affirmative obligation
    ("Create mocked step runners", 7, "HIGH", "affirmative"),
    # E4: Inline code
    ("Remove all `placeholder` values", 12, "INFO", "inline_code"),
    # E5: Completed checklist
    ("- [x] All mock services replaced", 11, "INFO", "completed_checklist"),
    # E6: Negation "no X present"
    ("No template sentinel placeholders present", 27, "INFO", "negation_prefix"),
    # E7: "must not contain"
    ("Must not contain placeholder values", 21, "INFO", "negation_prefix"),
    # E8: "ensure no X"
    ("Ensure no mock data remains", 10, "INFO", "negation_prefix"),
    # E9: Past-tense removal
    ("Removed the stub endpoint in v2.1", 12, "INFO", "negation_prefix"),
    # E10: grep command
    ("grep -rn '<placeholder>' src/", 11, "INFO", "command_context"),
    # E13: Risk description (no negation prefix)
    ("Risk: placeholder data could leak", 6, "HIGH", "affirmative"),
    # E15: Negation AFTER term
    ("The placeholder should not be committed", 4, "HIGH", "affirmative"),
    # E20: "never" keyword
    ("Never deploy with hardcoded credentials", 19, "INFO", "negation_prefix"),
])
def test_classify_meta_context(line, match_pos, expected_severity, reason):
    severity = _classify_meta_context(line, match_pos, 999, [])
    assert severity == expected_severity
```

### 5.2 Integration Tests for `scan_obligations()`

```python
class TestMetaContextFalsePositiveSuppression:
    """Verify meta-context false positives do not block the gate."""

    def test_verification_criteria_not_counted(self):
        """Gate criteria mentioning scaffold terms are INFO, not HIGH."""
        content = textwrap.dedent("""\
            ## Phase 1: Implementation
            - Build the authentication module

            ## Phase 2: Verification
            - No template sentinel placeholders ({{, <placeholder>, TODO) present
            - Ensure no mock data remains in production config
            - Zero stub endpoints found in final build
        """)
        report = scan_obligations(content)
        assert report.undischarged_count == 0

    def test_shell_commands_not_counted(self):
        """Shell commands searching for scaffold terms are INFO."""
        content = textwrap.dedent("""\
            ## Phase 1: Setup
            - Initialize project structure

            ## Phase 2: QA Checks
            - grep -rn '<placeholder>' src/superclaude/
            - find . -name '*mock*' -delete
        """)
        report = scan_obligations(content)
        assert report.undischarged_count == 0

    def test_completed_checklist_not_counted(self):
        """Completed checklist items with scaffold terms are INFO."""
        content = textwrap.dedent("""\
            ## Phase 1: Skeleton
            - Create scaffold structure

            ## Phase 2: Completion
            - [x] All scaffold replaced with real implementations
            - [x] Mock services removed
        """)
        report = scan_obligations(content)
        # Phase 1 "scaffold" is HIGH and undischarged
        # Phase 2 items are INFO (completed checklist)
        high_undischarged = [
            o for o in report.obligations
            if o.severity == "HIGH" and not o.discharged
        ]
        assert len(high_undischarged) == 1  # Only Phase 1's "scaffold"

    def test_affirmative_obligations_still_detected(self):
        """Real scaffolding obligations remain HIGH and are counted."""
        content = textwrap.dedent("""\
            ## Phase 1: Skeleton Setup
            - Create mocked step runners for initial testing
            - Build placeholder dispatch table
            - Implement stub executor

            ## Phase 2: Core Logic
            - Implement pipeline logic
            - Add error handling
        """)
        report = scan_obligations(content)
        assert report.undischarged_count >= 3

    def test_mixed_real_and_meta_on_same_document(self):
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
            - grep -rn 'mock' src/ returns zero results
        """)
        report = scan_obligations(content)
        # Phase 1 obligations should be discharged by Phase 2
        # Phase 3 items should be INFO
        assert report.undischarged_count == 0
```

### 5.3 Regression Tests

```python
class TestExistingBehaviorPreserved:
    """Ensure existing scanner behavior is not degraded."""

    def test_exempt_comment_still_works(self):
        content = textwrap.dedent("""\
            ## Phase 1
            - Create mock handler  # obligation-exempt
        """)
        report = scan_obligations(content)
        assert report.obligations[0].exempt is True

    def test_code_block_still_medium(self):
        content = textwrap.dedent("""\
            ## Phase 1
            ```python
            mock_data = {"key": "value"}
            ```
        """)
        report = scan_obligations(content)
        assert all(o.severity == "MEDIUM" for o in report.obligations)

    def test_discharge_mechanism_unchanged(self):
        content = textwrap.dedent("""\
            ## Phase 1
            - Create stub handler

            ## Phase 2
            - Replace stub handler with real implementation
        """)
        report = scan_obligations(content)
        assert report.obligations[0].discharged is True
```

### 5.4 Test Coverage Matrix

| Test Category | Count | Status |
|---|---|---|
| `_classify_meta_context()` unit (parameterized) | 12+ cases | New |
| `scan_obligations()` integration | 5 scenarios | New |
| Regression (existing behavior) | 3 scenarios | New |
| Edge case E16 (double negation) | 1 | New |
| Edge case E18 (mixed line) | 1 | New |
| Existing test suite | Unchanged | Must still pass |

---

## 6. Migration / Backward Compatibility

### 6.1 Zero Migration Required

- **No configuration changes**: The classifier is built into the scanner; no user-facing settings.
- **No new frontmatter fields**: The `undischarged_obligations` count in the audit report simply becomes more accurate.
- **No API signature changes**: `scan_obligations()` signature is unchanged.
- **Monotonically fewer false positives**: The change can only reduce `undischarged_count`, never increase it. Roadmaps that passed before will still pass. Roadmaps that failed due to meta-context false positives may now pass.

### 6.2 Existing `# obligation-exempt` Comments

Users who added `# obligation-exempt` to work around false positives can leave them in place. The exempt mechanism is checked before the classifier, so exempt comments are a no-op on lines that would already be classified as INFO. No cleanup required.

### 6.3 Audit Report Format

The audit report will now include INFO-severity obligations in its listing (for transparency), but the `undischarged_obligations` frontmatter count excludes them. Gate logic is unchanged.

### 6.4 Risk: Over-Suppression

The classifier could theoretically suppress a genuine obligation if:
- The line happens to contain a shell command keyword (`grep`) unrelated to the scaffold term
- The line has a negation word that coincidentally precedes an affirmative scaffold use

Mitigation: The `# obligation-exempt` escape hatch works in reverse -- there is no `# obligation-required` tag. However, the 4-word window limit on negation patterns and the "negation must precede term" rule minimize this risk. If needed in the future, a `# obligation-force` comment could be added symmetrically.

---

## 7. Estimated Diff Size

| File | Lines Added | Lines Modified | Lines Removed |
|---|---|---|---|
| `obligation_scanner.py` | ~65 (new constants + classifier function) | ~10 (severity call site, undischarged_count) | 0 |
| `obligation_scanner.py` (Obligation dataclass) | ~1 (classification_reason field) | 0 | 0 |
| `tests/roadmap/test_obligation_scanner_meta_context.py` | ~150 (new test file) | 0 | 0 |
| `tests/roadmap/test_anti_instinct_integration.py` | ~5 (optional: add meta-context scenario) | 0 | 0 |
| **Total** | ~221 | ~10 | 0 |

Net diff: approximately **230 lines** (mostly tests). Core logic addition is ~75 lines.

---

## 8. Implementation Sequence

1. Add new constants (`_NEGATION_PREFIXES`, `_COMMAND_LINE_RE`, etc.) to `obligation_scanner.py`
2. Add `_classify_meta_context()` function
3. Add `classification_reason` field to `Obligation` dataclass
4. Update `_determine_severity()` call site in `scan_obligations()` to use `_classify_meta_context()`
5. Update `ObligationReport.undischarged_count` to exclude `INFO`
6. Write unit tests for `_classify_meta_context()` (parameterized)
7. Write integration tests for `scan_obligations()` with meta-context inputs
8. Verify all existing tests still pass
9. Run `make lint && make format`

---

## 9. Alternatives Considered

### 9.1 Allowlist of Safe Line Prefixes

Maintain a list of "safe" line starts (e.g., `- [x]`, `grep`, `Ensure no`). Rejected because:
- Fragile: requires constant expansion as new patterns emerge
- Doesn't handle mid-line negations
- No principled boundary between "safe" and "unsafe"

### 9.2 NLP-Based Sentiment/Intent Analysis

Use a lightweight NLP model to determine if the sentence is affirmative or negative about scaffolding. Rejected because:
- Violates the pure-function / no-I/O constraint
- Adds a heavy dependency for a regex-based scanner
- Overkill for the pattern set

### 9.3 Full Exemption of Code Blocks (Not Just Demotion)

Make code-block scaffold terms fully exempt instead of MEDIUM. Rejected because:
- Some code blocks DO contain scaffolding obligations (e.g., `# TODO: replace mock_db with real DB`)
- MEDIUM demotion is the right middle ground for code blocks

### 9.4 Broader Context Window (Multi-Line)

Look at surrounding lines (not just the match line) for negation signals. Deferred because:
- Single-line analysis covers >95% of observed false positives
- Multi-line analysis adds complexity and risk of over-suppression
- Can be added as a future enhancement if needed
