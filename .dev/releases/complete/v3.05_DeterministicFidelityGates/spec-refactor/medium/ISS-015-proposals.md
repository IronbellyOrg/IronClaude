# ISS-015 Refactoring Proposals

**Issue**: spec_parser.py critical path risk not surfaced in spec. FR-1 depends on FR-2; FR-4 depends on FR-1; FR-5 depends on FR-2. Parser robustness against real-world specs is unaddressed in FR-2's acceptance criteria.

**Source**: Compatibility Report Section 7f (spec_parser.py as Critical Path)

**Confirmed facts**:
- `spec_parser.py` does NOT exist in the codebase (verified via glob search)
- FR-2 (lines 115-133) lists spec_parser.py as a genuinely new module -- this is correct
- FR-2 has zero acceptance criteria addressing parser robustness or error handling
- FR-2 has no Dependencies listed ("Dependencies: None") despite being on the critical path
- The spec's own "Key implementation risks" section (line 567) flags "Spec parser robustness -- real specs may deviate from template" as risk #1, but this risk is not reflected in FR-2's acceptance criteria
- No CRITICAL or HIGH proposals address this issue

**Dependency chain**: FR-2 (parser) --> FR-1 (structural checkers) --> FR-4 (semantic layer) --> FR-7 (convergence gate). If the parser fails on a real-world spec, the entire deterministic fidelity pipeline is inoperative.

---

## Proposal #1: Add Robustness ACs to FR-2 + Critical Path Note (RECOMMENDED)

**Rationale**: The most targeted fix. Adds parser robustness acceptance criteria directly to FR-2 and annotates FR-2's dependency status to make the critical path visible. Does not restructure any other FR.

### Exact Spec Text Changes

**File**: `deterministic-fidelity-gate-requirements.md`

**Change 1 -- FR-2 Acceptance Criteria (after line 131)**

BEFORE (lines 121-133):
```
**Acceptance Criteria**:
- [ ] Parses YAML frontmatter from both spec and roadmap
- [ ] Extracts markdown tables by section (keyed by heading path)
- [ ] Extracts fenced code blocks with language annotation
- [ ] Extracts requirement ID families via regex: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- [ ] Extracts Python function signatures from fenced blocks: `def name(params) -> return_type`
- [ ] Extracts file paths from manifest tables (Sec 4.1, 4.2, 4.3)
- [ ] Extracts `Literal[...]` enum values from code blocks
- [ ] Extracts numeric threshold expressions: `< 5s`, `>= 90%`, `minimum 20`
- [ ] Returns structured objects, not raw text

**Dependencies**: None
```

AFTER:
```
**Acceptance Criteria**:
- [ ] Parses YAML frontmatter from both spec and roadmap
- [ ] Extracts markdown tables by section (keyed by heading path)
- [ ] Extracts fenced code blocks with language annotation
- [ ] Extracts requirement ID families via regex: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- [ ] Extracts Python function signatures from fenced blocks: `def name(params) -> return_type`
- [ ] Extracts file paths from manifest tables (Sec 4.1, 4.2, 4.3)
- [ ] Extracts `Literal[...]` enum values from code blocks
- [ ] Extracts numeric threshold expressions: `< 5s`, `>= 90%`, `minimum 20`
- [ ] Returns structured objects, not raw text
- [ ] Graceful degradation: missing or malformed YAML frontmatter returns empty metadata dict (not exception)
- [ ] Graceful degradation: markdown tables with irregular column counts are parsed best-effort with warnings logged
- [ ] Graceful degradation: fenced code blocks with missing language annotations are extracted with `language=None`
- [ ] All parse errors are collected into a `List[ParseWarning]` returned alongside the parsed result (not raised as exceptions)
- [ ] Parser tested against at least 2 real specs from prior releases (v3.0 spec, v3.05 spec) to validate template coverage

**Critical Path Note**: FR-2 is a blocking dependency for FR-1 (structural
checkers), FR-4 (semantic layer via FR-1), and FR-5 (sectional comparison).
Parser failures cascade through the entire fidelity pipeline. Implement and
validate FR-2 before starting FR-1.

**Dependencies**: None (but is a critical-path dependency OF: FR-1, FR-4, FR-5)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-2 Acceptance Criteria + Dependencies line)

### Risk: LOW
- Additive only -- all existing ACs preserved verbatim, new ACs appended.
- The "Critical Path Note" is informational and does not change any FR's behavior.
- No renumbering, no cross-reference breakage.
- The "tested against 2 real specs" AC is concrete and immediately verifiable.

### Requires Code Changes: YES (new code -- spec_parser.py does not exist yet)
- All ACs are for the new `spec_parser.py` module which must be created.
- The robustness ACs (graceful degradation, ParseWarning collection) shape the parser's error-handling contract before implementation begins.

---

## Proposal #2: Add Critical Path Dependency Chain to FR-1 + FR-2 Robustness ACs

**Rationale**: Goes further than Proposal #1 by also modifying FR-1's Dependencies section to make the full chain explicit and adding a "Build Order" annotation. This surfaces the risk not just in FR-2 but at the point where the dependency is consumed.

### Exact Spec Text Changes

**Change 1 -- FR-2 (same as Proposal #1)**: Add all five robustness ACs and the Critical Path Note to FR-2.

**Change 2 -- FR-1 Dependencies line (line 111)**

BEFORE (line 111):
```
**Dependencies**: FR-2 (spec parser), FR-3 (severity rules)
```

AFTER:
```
**Dependencies**: FR-2 (spec parser -- CRITICAL PATH, must be validated before
FR-1 implementation begins), FR-3 (severity rules)

**Build Order Constraint**: FR-2 must pass its own acceptance criteria
(including robustness tests against real specs) before FR-1 checkers are
implemented. If FR-2 cannot parse a real-world spec reliably, FR-1 checkers
will produce garbage findings that cascade through FR-6, FR-7, and FR-8.
```

**Change 3 -- FR-5 Dependencies line (line 292)**

BEFORE (line 292):
```
**Dependencies**: FR-2 (parser)
```

AFTER:
```
**Dependencies**: FR-2 (parser -- critical path; sectional comparison requires
reliable heading extraction from parser)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-1 Dependencies, FR-2 ACs + Dependencies, FR-5 Dependencies)

### Risk: LOW-MEDIUM
- Three locations edited instead of one.
- The "Build Order Constraint" on FR-1 introduces a process requirement into the spec, which is unusual for functional requirements -- some reviewers may prefer this in a separate implementation plan rather than the spec itself.
- All changes are additive; no existing text is deleted or reworded.

### Requires Code Changes: YES (identical to Proposal #1)

---

## Proposal #3: Add Dedicated FR-2.1 Sub-requirement for Parser Robustness

**Rationale**: Rather than appending robustness ACs to FR-2, create a sub-requirement (FR-2.1) that explicitly addresses parser error handling and real-world spec tolerance. This follows the pattern already established by FR-4.1 (debate protocol) and FR-9.1 (allow-regeneration flag) -- sub-requirements for specific behavioral contracts.

### Exact Spec Text Changes

**File**: `deterministic-fidelity-gate-requirements.md`

**Change 1 -- Insert after FR-2's Dependencies line (after line 133):**

```markdown
#### FR-2.1: Parser Robustness and Error Handling

spec_parser.py is on the critical path: FR-1, FR-4, and FR-5 all depend on
it. Real-world specs deviate from templates (missing frontmatter, irregular
tables, non-standard heading levels, mixed fenced block styles). The parser
must degrade gracefully rather than abort.

**Error handling contract**:

| Input Condition | Parser Behavior | Output |
|-----------------|----------------|--------|
| Missing YAML frontmatter | Skip frontmatter extraction | `metadata={}`, warning logged |
| Malformed YAML (parse error) | Skip frontmatter extraction | `metadata={}`, warning logged |
| Table with irregular column count | Parse available columns | Partial row data, warning logged |
| Fenced block without language tag | Extract block content | `language=None` |
| Heading level inconsistency (## followed by ####) | Treat as sub-section | Heading tree reflects actual nesting |
| Requirement ID in prose (not table) | Extract via regex | Same ID extraction as table context |
| Empty spec file | Return empty parsed result | All fields empty/default, no exception |

**Acceptance Criteria** (FR-2.1):
- [ ] All parse errors collected into `List[ParseWarning]` (dataclass: path, line_number, warning_type, message)
- [ ] `ParseWarning` list returned alongside parsed result (not raised as exceptions)
- [ ] Parser never raises on malformed input -- always returns a (possibly empty) structured result plus warnings
- [ ] Validated against v3.0 spec (`deterministic-fidelity-gate-requirements.md` from the v3.0 release) and v3.05 spec (this document)
- [ ] Validated against at least 1 intentionally malformed spec (missing frontmatter + broken table + empty sections)

**Dependencies**: FR-2 (parent requirement)
```

**Change 2 -- FR-2 Dependencies line (line 133):**

BEFORE:
```
**Dependencies**: None
```

AFTER:
```
**Dependencies**: None (but is a critical-path dependency OF: FR-1, FR-4, FR-5 -- see FR-2.1)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (new FR-2.1 subsection + FR-2 Dependencies annotation)

### Risk: MEDIUM
- Adds a new sub-requirement (FR-2.1), which expands the spec's requirement count.
- The error handling table is prescriptive -- it locks in specific parser behaviors that may need revision during implementation if edge cases emerge.
- The "validated against v3.0 spec" AC assumes the v3.0 spec is available at the expected path -- this needs to be true at implementation time.
- Follows established pattern (FR-4.1, FR-9.1) so is structurally consistent.

### Requires Code Changes: YES (new code)
- `ParseWarning` dataclass (likely in `models.py` or `spec_parser.py`)
- Error collection pathway in all parser extraction methods
- Test fixtures with real and malformed specs

---

## Summary Comparison

| # | Proposal | Disruption | Self-Contained | Critical Path Visibility | Robustness Detail | Risk |
|---|----------|-----------|----------------|--------------------------|-------------------|------|
| 1 | Robustness ACs + critical path note on FR-2 | Low | Yes | FR-2 only | 5 new ACs | LOW |
| 2 | FR-1 + FR-2 + FR-5 dependency annotations | Low-Medium | Yes | FR-1, FR-2, FR-5 | 5 new ACs | LOW-MEDIUM |
| 3 | Dedicated FR-2.1 sub-requirement | Medium | Yes | FR-2 + FR-2.1 | Full error handling table + 5 ACs | MEDIUM |

**Recommendation**: Proposal #1. It addresses the core issue (parser robustness unspecified, critical path invisible) with minimal disruption. The five new ACs are concrete, testable, and directly address the compatibility report's concern. The "Critical Path Note" makes the dependency chain visible without restructuring other FRs.

If the team prefers more prescriptive error-handling contracts (common when multiple implementers may work on the parser), Proposal #3 provides the most complete specification at the cost of a new sub-requirement.

Proposal #2 is best if the implementation plan will be generated directly from the spec's dependency annotations (e.g., via `/sc:tasklist`), as it makes the build-order constraint machine-readable at each consumption point.
