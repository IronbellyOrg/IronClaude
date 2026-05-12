# Merged Proposal: Meta-Context False Positive Mitigation for Obligation Scanner

**Date**: 2026-04-03
**Status**: Final Unified Specification
**Component**: `src/superclaude/cli/roadmap/obligation_scanner.py`
**Base**: Variant A (Brainstorm/Composite)
**Hybrid Elements**: Variant B (Design/Classifier), Variant C (Improve/Minimal)

---

## 1. Problem Statement

[Source: Variant A]

The obligation scanner matches scaffold terms (`mock`, `stub`, `placeholder`, `skeleton`, `temporary`, `hardcoded`, `fake`, etc.) in roadmap markdown and requires each to be "discharged" by a corresponding action verb in a later phase. The scanner produces false positives when scaffold vocabulary appears in **meta-contexts** -- text that discusses, checks for, or references scaffolding rather than creating scaffolding obligations.

### 1.1 The Six Meta-Context Categories

| # | Category | Example | Why It's False |
|---|----------|---------|----------------|
| 1 | **Verification/gate criteria** | `No template sentinel placeholders ({{, <placeholder>, TODO) present` | Describes what to *reject*, not what to *create* |
| 2 | **Shell commands** | `grep -rn '<placeholder>' src/` | Search target in a command, not an obligation |
| 3 | **Code block anti-patterns** | `` ```# BAD: mock_data = {...}``` `` | Shows what NOT to do |
| 4 | **Negative assertions** | `must not contain placeholder data` | Instruction to *remove/prevent*, not create |
| 5 | **Historical/changelog refs** | `removed the mock service in v2.1` | Past tense, already resolved |
| 6 | **Risk descriptions** | `risk: placeholder data could leak to production` | Describing a risk, not creating scaffolding |

### 1.2 Current Mitigations and Their Gaps

- **`# obligation-exempt`** -- requires roadmap authors to manually annotate every meta-context line. Fragile; authors forget; new roadmaps don't know to add it. [Source: Variant A]
- **Code block demotion to MEDIUM** -- only applies inside fenced code blocks (```` ``` ````), and only demotes severity. Does not cover inline code, bullet items describing verification criteria, or any of the other five categories. [Source: Variant A]

---

## 2. Technical Design

### 2.1 Strategy: 2-Layer Hybrid Classification

[Source: Variant A, simplified from 3 layers; severity model from Variant C]

Instead of trying to enumerate every possible meta-context (fragile, whack-a-mole), the design introduces a **context classifier** that examines the line containing a scaffold match and determines whether the match represents an **affirmative obligation** or a **meta-reference**. Meta-references are demoted to MEDIUM severity (consistent with existing code block handling), which excludes them from `undischarged_count`.

**Layer 1 -- Structural Exemptions** [Source: Variant B, adapted]:
- Inline code exemption: Scaffold terms inside backtick spans containing scaffold vocabulary
- Completed checklist exemption: Lines starting with `- [x]` (already done)

**Layer 2 -- Negation/Meta-Context Classification** [Source: Variant A + C]:
- Unified regex covering negation, verification, historical, risk, shell commands, and gate criteria
- Positional check: negation word must precede the scaffold term
- Returns `True` for meta-context; caller sets severity to MEDIUM

### 2.2 Module-Level Constants

[Source: Hybrid - scaffold-aware regex from B, consolidated patterns from C + A]

```python
# --- Meta-context classification (FR-MOD1.9) ---

# SCAFFOLD_TERMS assumed to be defined elsewhere in the module
# Example: SCAFFOLD_TERMS = ["mock", "stub", "placeholder", "skeleton", "temporary", 
#                            "hardcoded", "hardwired", "no-op", "dummy", "fake", "scaffold"]

# Layer 1a: Inline code - scaffold term appears inside backticks on the same line
# Uses scaffold-aware matching for precision [Source: Variant B]
_INLINE_CODE_SCAFFOLD_RE = re.compile(
    r"`[^`]*(?:" + "|".join(SCAFFOLD_TERMS) + r")[^`]*`",
    re.IGNORECASE
)

# Layer 1b: Completed checklist item [Source: Variant B]
_COMPLETED_CHECKLIST_RE = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE)

# Layer 2: Negation/meta-context prefix before the scaffold term
# Consolidated regex combining patterns from Variant A and C [Source: Hybrid]
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
    re.IGNORECASE
)

# Shell command detection (Category 2) [Source: Variant A]
_SHELL_CMD_RE = re.compile(
    r"(?:^\s*[$>]?\s*)?(?:grep|sed|awk|find|rg|ag|git\s+grep|xargs)\b",
    re.IGNORECASE
)

# Risk warning pattern for lines starting with risk [Source: Variant C]
_RISK_WARNING_RE = re.compile(
    r"(?:^\s*)(?:risk|warning|caution|danger|caveat|concern)\s*:",
    re.IGNORECASE
)

# Gate criteria pattern [Source: Variant B, adapted]
_GATE_CRITERIA_RE = re.compile(
    r"(?:no|zero|0)\s+(?:\w+\s+){0,4}"
    r"(?:present|found|detected|remaining|allowed|permitted|exist)",
    re.IGNORECASE
)
```

### 2.3 Classification Function

[Source: Variant A signature + Variant C implementation approach]

```python
def _is_meta_context(line: str, term_start_in_line: int) -> bool:
    """Determine if a scaffold term on this line is in a meta-context (not an obligation).
    
    Returns True when the scaffold term appears in a negation, verification,
    historical, risk, shell-command, or gate-criteria context. Caller should
    set severity to MEDIUM when this returns True.
    
    Args:
        line: The full line containing the scaffold match.
        term_start_in_line: Character offset of the scaffold term within `line`.
        
    Returns:
        True if the term appears in meta-context (should be MEDIUM severity).
        False if the term appears to be an affirmative obligation (HIGH severity).
    """
    line_lower = line.lower()
    
    # Category 2: Shell command lines are always meta-context
    if _SHELL_CMD_RE.search(line):
        return True
    
    # Category 5: Risk/warning framing at line start
    if _RISK_WARNING_RE.match(line):
        return True
    
    # Category 6: Gate/verification criteria language
    if _GATE_CRITERIA_RE.search(line):
        return True
    
    # Categories 1, 4: Negation/removal/historical prefix before the scaffold term
    prefix = line[:term_start_in_line]
    if _NEGATION_PREFIX_RE.search(prefix):
        return True
    
    # Also check full line for past-tense removal verbs (Category 4)
    # These can appear anywhere in the line for historical references
    if re.search(r"\b(?:removed?|replaced?|eliminated?|deleted?)\b", line_lower):
        return True
    
    return False
```

### 2.4 Integration into `scan_obligations()`

[Source: Variant A integration point + Variant C severity approach]

```python
def scan_obligations(content: str) -> ObligationReport:
    """Scan roadmap content for scaffold obligations."""
    # ... existing setup code ...
    
    for i, (phase_name, phase_content) in enumerate(sections):
        for match in _SCAFFOLD_TERM_RE.finditer(phase_content):
            term = match.group(0)
            abs_pos = _get_absolute_position(content, sections, i, match.start())
            
            # Existing: Code block check [Source: Existing behavior preserved]
            severity = _determine_severity(abs_pos, code_block_ranges)
            
            # Get the line containing the match for context analysis
            line_start = phase_content.rfind("\n", 0, match.start()) + 1
            line_end = phase_content.find("\n", match.start())
            if line_end == -1:
                line_end = len(phase_content)
            context_line = phase_content[line_start:line_end]
            
            # Calculate term position within the line
            term_start_in_line = match.start() - line_start
            
            # Layer 1a: Inline code exemption [Source: Variant B]
            if _INLINE_CODE_SCAFFOLD_RE.search(context_line):
                severity = "MEDIUM"
            
            # Layer 1b: Completed checklist exemption [Source: Variant B]
            elif _COMPLETED_CHECKLIST_RE.match(context_line):
                severity = "MEDIUM"
            
            # Layer 2: Negation/meta-context classification [Source: Variant A + C]
            elif severity == "HIGH" and _is_meta_context(context_line, term_start_in_line):
                severity = "MEDIUM"
            
            # ... rest of obligation creation logic ...
```

### 2.5 Data Flow

[Source: Variant B, adapted for 2-layer approach]

```
For each scaffold term match:
  1. Check exempt comment (existing)     --> exempt=True, skip classification
  2. Check code block (existing)         --> severity="MEDIUM" [preserved]
  3. Check inline code (Layer 1a)        --> severity="MEDIUM"
  4. Check completed checklist (Layer 1b)--> severity="MEDIUM"
  5. Check meta-context (Layer 2)        --> severity="MEDIUM" if _is_meta_context()
  6. Default                             --> severity="HIGH"
```

Note: `_determine_severity()` is NOT deprecated. It handles code block detection (step 2).
The new `_is_meta_context()` is called after as an additional check (step 5).

---

## 3. Edge Case Catalog

[Source: Variant B E1-E20, adapted for MEDIUM severity instead of INFO]

| # | Edge Case | Input | Expected Severity | Classification Layer | Notes |
|---|-----------|-------|-------------------|---------------------|-------|
| E1 | Affirmative obligation (true positive) | `Create mocked step runners` | HIGH | Default | [Source: Variant B] |
| E2 | Explicit exempt comment | `Create placeholder config # obligation-exempt` | HIGH + exempt=True | Existing | [Source: Variant B] |
| E3 | Inside fenced code block | `` ```python\nmock_data = {...}\n``` `` | MEDIUM | Existing code block | [Source: Variant B] |
| E4 | Inline code reference | `Remove all \`placeholder\` values from config` | MEDIUM | Layer 1a | [Source: Variant B] |
| E5 | Completed checklist | `- [x] All mock services replaced` | MEDIUM | Layer 1b | [Source: Variant B] |
| E6 | Negation: "no X present" | `No template sentinel placeholders present` | MEDIUM | Layer 2 | [Source: Variant B] |
| E7 | Negation: "must not contain" | `Must not contain placeholder values` | MEDIUM | Layer 2 | [Source: Variant B] |
| E8 | Negation: "ensure no X" | `Ensure no mock data remains` | MEDIUM | Layer 2 | [Source: Variant B] |
| E9 | Past-tense removal | `Removed the stub endpoint in v2.1` | MEDIUM | Layer 2 | [Source: Variant B] |
| E10 | Shell grep command | `grep -rn '<placeholder>' src/` | MEDIUM | Layer 2 | [Source: Variant B] |
| E11 | Shell find command | `find . -name '*mock*' -delete` | MEDIUM | Layer 2 | [Source: Variant B] |
| E12 | Gate criteria | `Zero placeholder values found` | MEDIUM | Layer 2 | [Source: Variant B] |
| E13 | Risk description | `Risk: placeholder data could leak` | MEDIUM | Layer 2 | [CHANGED: Was HIGH in B, demoted per A/C consensus] |
| E14 | Ambiguous: "use placeholder for now" | `Use placeholder config for now` | HIGH | Default | [Source: Variant B] |
| E15 | Negation AFTER term (not before) | `The placeholder should not be committed` | HIGH | Default | [Source: Variant B] |
| E16 | Double negation | `Do not remove the mock yet` | HIGH | Default | [Source: Variant B] |
| E17 | Term in heading | `## Phase 1: Skeleton Setup` | HIGH | Default | [Source: Variant B] |
| E18 | Mixed line: negation + affirmative | `Remove old stubs and add new placeholder routes` | MEDIUM for "stubs", HIGH for "placeholder" | Per-match | [Source: Variant B] |
| E19 | Negation far from term | `Ensure the system has no residual temporary test files` | MEDIUM | Layer 2 | [Source: Variant B] |
| E20 | "never" keyword | `Never deploy with hardcoded credentials` | MEDIUM | Layer 2 | [Source: Variant B] |

### 3.1 E13 Deliberate Decision

[Source: Variant A/C consensus, overriding Variant B]

Risk descriptions like "Risk: placeholder data could leak" are classified as MEDIUM (not HIGH per Variant B's E13, not exempt per Variant A's original proposal). A risk statement about placeholder data describes a hypothetical concern, not an actual obligation to create scaffolding. The MEDIUM severity preserves visibility in reports while excluding from `undischarged_count`.

### 3.2 E15/E16 Deliberate Decision

[Source: Variant B]

The classifier only checks for negation **before** the scaffold term's position in the line. This prevents misclassifying sentences where the scaffold term IS the subject being described affirmatively, even if a negation appears later. This is a deliberate design choice that favors precision (fewer false negatives at the cost of some remaining false positives that can use `# obligation-exempt`).

---

## 4. API Surface

### 4.1 Public API (No Breaking Changes)

[Source: Variant B, adapted - no INFO severity, no dataclass changes]

| Symbol | Change | Backward Compatible |
|--------|--------|---------------------|
| `scan_obligations(content: str) -> ObligationReport` | No signature change | Yes [Source: Variant C] |
| `ObligationReport.undischarged_count` | Unchanged (already excludes MEDIUM) | Yes [Source: Variant C] |
| `ObligationReport.has_undischarged` | Unchanged (delegates to `undischarged_count`) | Yes [Source: Variant B] |
| `Obligation` dataclass | **No changes** | Yes [Source: Variant C] |
| `SCAFFOLD_TERMS`, `DISCHARGE_TERMS` | Unchanged | Yes [Source: Variant B] |

### 4.2 New Internal Symbols (Not Public API)

[Source: Hybrid]

| Symbol | Purpose |
|--------|---------|
| `_INLINE_CODE_SCAFFOLD_RE` | Scaffold-aware inline code detection [Source: Variant B] |
| `_COMPLETED_CHECKLIST_RE` | Completed checklist item detection [Source: Variant B] |
| `_NEGATION_PREFIX_RE` | Consolidated negation/meta-context patterns [Source: Hybrid] |
| `_SHELL_CMD_RE` | Shell command detection [Source: Variant A] |
| `_RISK_WARNING_RE` | Risk/warning line detection [Source: Variant C] |
| `_GATE_CRITERIA_RE` | Gate/verification criteria detection [Source: Variant B] |
| `_is_meta_context()` | Meta-context classification function [Source: Variant A + C] |

### 4.3 No Deprecations

[Source: Variant C, rejecting Variant B's deprecation]

| Symbol | Status |
|--------|--------|
| `_determine_severity()` | **Retained** - still handles code block detection. NOT deprecated. [Source: Variant C] |

---

## 5. Test Plan

### 5.1 Unit Tests for `_is_meta_context()`

[Source: Variant B, adapted for MEDIUM severity expectations]

```python
@pytest.mark.parametrize("line,term_pos,expected,reason", [
    # E1: Affirmative obligation
    ("Create mocked step runners", 7, False, "affirmative"),
    # E4: Inline code (handled at scan level, not in _is_meta_context)
    # E5: Completed checklist (handled at scan level)
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
    # E13: Risk description [CHANGED: now True per hybrid decision]
    ("Risk: placeholder data could leak", 6, True, "risk_description"),
    # E14: Ambiguous affirmative
    ("Use placeholder config for now", 4, False, "affirmative"),
    # E15: Negation AFTER term
    ("The placeholder should not be committed", 4, False, "affirmative"),
    # E16: Double negation
    ("Do not remove the mock yet", 18, False, "affirmative"),
    # E17: Term in heading
    ("## Phase 1: Skeleton Setup", 13, False, "affirmative"),
    # E18: Mixed line (first term)
    ("Remove old stubs and add new placeholder", 10, True, "negation_prefix"),
    # E18: Mixed line (second term)
    ("Remove old stubs and add new placeholder", 34, False, "affirmative"),
    # E19: Negation with word gap
    ("Ensure the system has no residual temporary files", 32, True, "negation_prefix"),
    # E20: "never" keyword
    ("Never deploy with hardcoded credentials", 19, True, "negation_prefix"),
])
def test_is_meta_context(line, term_pos, expected, reason):
    result = _is_meta_context(line, term_pos)
    assert result == expected, f"Failed for {reason}: {line}"
```

### 5.2 Integration Tests for `scan_obligations()`

[Source: Variant B, adapted]

```python
class TestMetaContextFalsePositiveSuppression:
    """Verify meta-context false positives do not block the gate."""

    def test_verification_criteria_not_counted(self):
        """Gate criteria mentioning scaffold terms are MEDIUM, not HIGH."""
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
        # Verify they were recorded as MEDIUM
        medium_obligations = [o for o in report.obligations if o.severity == "MEDIUM"]
        assert len(medium_obligations) == 3

    def test_shell_commands_not_counted(self):
        """Shell commands searching for scaffold terms are MEDIUM."""
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
        """Completed checklist items with scaffold terms are MEDIUM."""
        content = textwrap.dedent("""\
            ## Phase 1: Skeleton
            - Create scaffold structure

            ## Phase 2: Completion
            - [x] All scaffold replaced with real implementations
            - [x] Mock services removed
        """)
        report = scan_obligations(content)
        # Phase 1 "scaffold" is HIGH and undischarged
        # Phase 2 items are MEDIUM (completed checklist)
        high_undischarged = [
            o for o in report.obligations
            if o.severity == "HIGH" and not o.discharged
        ]
        assert len(high_undischarged) == 1  # Only Phase 1's "scaffold"
        medium_count = len([o for o in report.obligations if o.severity == "MEDIUM"])
        assert medium_count == 2  # The completed checklist items

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
        high_count = len([o for o in report.obligations if o.severity == "HIGH"])
        assert high_count >= 3

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
        # Phase 3 items should be MEDIUM
        assert report.undischarged_count == 0
```

### 5.3 Regression Tests

[Source: Variant B]

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

[Source: Variant B, adapted]

| Test Category | Count | Status |
|---------------|-------|--------|
| `_is_meta_context()` unit (parameterized) | 18+ cases | New |
| `scan_obligations()` integration | 5 scenarios | New |
| Regression (existing behavior) | 3 scenarios | New |
| Edge case E18 (mixed line) | 2 (both terms) | New |
| Existing test suite | Unchanged | Must still pass |

---

## 6. Migration / Backward Compatibility

[Source: Variant B, simplified]

### 6.1 Zero Migration Required

- **No configuration changes**: The classifier is built into the scanner; no user-facing settings. [Source: Variant B]
- **No new frontmatter fields**: The `undischarged_obligations` count in the audit report simply becomes more accurate. [Source: Variant B]
- **No API signature changes**: `scan_obligations()` signature is unchanged. `Obligation` dataclass is unchanged. [Source: Variant C]
- **Monotonically fewer false positives**: The change can only reduce `undischarged_count`, never increase it. Roadmaps that passed before will still pass. Roadmaps that failed due to meta-context false positives may now pass. [Source: Variant B]

### 6.2 Existing `# obligation-exempt` Comments

[Source: Variant B]

Users who added `# obligation-exempt` to work around false positives can leave them in place. The exempt mechanism is checked before the classifier, so exempt comments are a no-op on lines that would already be classified as MEDIUM. No cleanup required.

### 6.3 Audit Report Format

[Source: Variant B, adapted]

The audit report will continue to show MEDIUM-severity obligations in its listing (for transparency), and the `undischarged_obligations` frontmatter count excludes them. Gate logic is unchanged.

### 6.4 Risk: Over-Suppression

[Source: Variant B, adapted]

The classifier could theoretically suppress a genuine obligation if:
- The line happens to contain a shell command keyword (`grep`) unrelated to the scaffold term
- The line has a negation word that coincidentally precedes an affirmative scaffold use

Mitigation: The `# obligation-exempt` escape hatch works in reverse—there is no `# obligation-force` tag. However, the positional negation check (negation must precede term) and the fail-safe default (assume obligation) minimize this risk.

---

## 7. Implementation Sequence

[Source: Variant A, explicit 2-phase plan]

### Phase 1: Quick Win (~25 lines)

1. Add `_INLINE_CODE_SCAFFOLD_RE` constant (scaffold-aware regex) [Source: Variant B]
2. Add `_COMPLETED_CHECKLIST_RE` constant [Source: Variant B]
3. Add Layer 1 integration in `scan_obligations()`
4. Write unit tests for Layer 1
5. Run `make lint && make format`

**Deliverable**: Inline code and completed checklist items are demoted to MEDIUM.

### Phase 2: Full Fix (~65 lines)

1. Add `_NEGATION_PREFIX_RE`, `_SHELL_CMD_RE`, `_RISK_WARNING_RE`, `_GATE_CRITERIA_RE` constants [Source: Hybrid]
2. Add `_is_meta_context()` function [Source: Variant A + C]
3. Add Layer 2 integration in `scan_obligations()`
4. Write parameterized unit tests for `_is_meta_context()` (adapted E1-E20) [Source: Variant B]
5. Write integration tests [Source: Variant B]
6. Run full test suite
7. Run `make lint && make format`

**Deliverable**: All 6 meta-context categories are demoted to MEDIUM.

---

## 8. Estimated Diff Size

[Source: Hybrid, updated for 2-layer approach]

| File | Lines Added | Lines Modified | Lines Removed |
|------|-------------|----------------|---------------|
| `obligation_scanner.py` | ~60 (new constants + `_is_meta_context()`) | ~15 (integration) | 0 |
| `tests/roadmap/test_obligation_scanner_meta_context.py` | ~150 (new test file) | 0 | 0 |
| `tests/roadmap/test_anti_instinct_integration.py` | ~5 (optional: add meta-context scenario) | 0 | 0 |
| **Total** | ~215 | ~15 | 0 |

Net diff: approximately **230 lines** (mostly tests). Core logic addition is ~75 lines.

---

## 9. Alternatives Considered

[Source: Summary of adversarial debate decisions]

### 9.1 INFO Severity Level (from Variant B)

**Rejected**: Variant B introduced a new `INFO` severity level below `MEDIUM`. This would expand the API surface and require changes to `undischarged_count` logic. The hybrid uses existing `MEDIUM` for all meta-context, maintaining consistency. [Source: Variant C approach adopted]

### 9.2 Full Exemption for Meta-Context (from Variant A)

**Rejected**: Variant A originally proposed setting `exempt=True` for meta-context, which would hide obligations entirely from reports. The hybrid uses `severity="MEDIUM"` to preserve visibility while excluding from `undischarged_count`. [Source: Variant C approach adopted]

### 9.3 `classification_reason` Dataclass Field (from Variant B)

**Rejected**: Variant B added an optional `classification_reason: str = ""` field to `Obligation`. While useful for debugging, this is technically an API change. The hybrid prioritizes zero API changes. [Source: Variant C approach adopted]

### 9.4 Risk Descriptions as HIGH (from Variant B's E13)

**Rejected**: Variant B deliberately classified risk descriptions as HIGH, arguing they imply the placeholder exists. The adversarial debate overruled this—risk descriptions are meta-references describing hypothetical concerns, not actual obligations. The hybrid demotes them to MEDIUM. [Source: Variant A/C consensus]

### 9.5 Deprecation of `_determine_severity()` (from Variant B)

**Rejected**: Variant B proposed deprecating `_determine_severity()` because it was "subsumed" by the classifier. However, `_determine_severity()` still handles code block detection. The hybrid keeps it and adds `_is_meta_context()` as an additional check. [Source: Variant C approach adopted]

### 9.6 NLP-Based Classification (from Variant B's Alternatives Considered)

**Rejected**: Variant B considered and rejected NLP-based approaches. The hybrid maintains this rejection—regex-based classification is sufficient for the pattern set and avoids heavy dependencies. [Source: Variant B rejection adopted]

### 9.7 Multi-Line Context Analysis (deferred from A/B)

**Deferred**: Both A and B acknowledged multi-line negation contexts as a limitation. The hybrid also defers this—single-line analysis covers >95% of observed false positives. Multi-line can be added as a future enhancement if needed. [Source: Variant B rationale adopted]

---

## Provenance Summary

| Section | Primary Source | Key Adaptations |
|---------|---------------|-----------------|
| Problem Statement (6 categories) | Variant A | None |
| 2-Layer Architecture | Variant A | Simplified from 3 layers |
| MEDIUM Severity Model | Variant C | Applied to all meta-context |
| Scaffold-Aware Inline Code | Variant B | Used as-is |
| Completed Checklist Detection | Variant B | Added to Layer 1 |
| Consolidated Negation Regex | Hybrid | C's structure + A's patterns |
| `_is_meta_context()` | Variant A + C | A's signature, C's implementation |
| Edge Case Catalog E1-E20 | Variant B | Severity changed to MEDIUM |
| Test Plan (parameterized) | Variant B | Adapted severity expectations |
| Integration Test Class | Variant B | Used as structure |
| No Dataclass Changes | Variant C | Rejected B's `classification_reason` |
| No Deprecations | Variant C | Retained `_determine_severity()` |
| 2-Phase Implementation | Variant A | Kept as-is |
| Risk Demoted to MEDIUM | Variant A/C | Rejected B's HIGH decision |
| Migration/Compatibility | Variant B | Simplified (no INFO severity) |
