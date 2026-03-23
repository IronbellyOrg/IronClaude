# ISS-018 Refactoring Proposals

**Issue**: Section splitter for chunked comparison does not exist. FR-5 requires splitting spec/roadmap by headings for per-section checker input, but only `_truncate_to_budget()` exists in `semantic_layer.py` — no section-splitting logic.

**Severity**: MEDIUM (spec omits something that matters)

**Source**: Compatibility Report Section 4 (Genuinely New Code to Build); issues-classified.md ISS-018

**Affected Spec Section**: FR-5 (Sectional/Chunked Comparison), lines 278-293

**Cross-references**:
- FR-2 (Spec & Roadmap Parser) — FR-5 depends on FR-2 for heading extraction
- FR-4 (Semantic Layer) — consumes section objects via `SemanticCheckRequest.spec_sections` / `roadmap_sections`
- Resolved Question #5 — specifies cross-section reference handling (bidirectional linking, supplementary sections)
- `semantic_layer.py` — already expects `SpecSection` objects with `.heading` and `.content` attributes (lines 198-203)

**Existing code inventory**:
- `_truncate_to_budget()` at `semantic_layer.py:145-168` — truncates content to byte budget on line boundaries; NOT a section splitter
- `build_semantic_prompt()` at `semantic_layer.py:171-234` — already consumes `request.spec_sections` and `request.roadmap_sections` as lists of objects with `.heading`/`.content` attributes
- `SemanticCheckRequest` dataclass at `semantic_layer.py:133-140` — defines `spec_sections: list[Any]` and `roadmap_sections: list[Any]`
- `spec_parser.py` — does NOT exist yet (genuinely new module per FR-2)
- `TRUNCATION_MARKER` at `semantic_layer.py:28` — missing heading name (separate issue: ISS-017)

**No CRITICAL or HIGH proposals address this issue.** ISS-009 (severity rule tables) and ISS-015 (spec_parser critical path) are related but do not cover the section-splitting gap itself.

---

## Proposal #1: Add Section Splitter Specification to FR-5 with Implementation Location in spec_parser.py (RECOMMENDED)

**Rationale**: FR-5 describes the requirement ("split by headings") but provides no specification of the splitting algorithm, output data structure, or where the code lives. Since FR-5 depends on FR-2 (parser), the section splitter belongs in `spec_parser.py` as a parser output. This proposal adds the missing specification to FR-5 and defines the `SpecSection` dataclass that `semantic_layer.py` already expects.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Before** (FR-5, lines 278-293):
```markdown
### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only.

**Acceptance Criteria**:
- [ ] Spec is split by `## N. Section Name` headings into named chunks
- [ ] Roadmap is split by phase/task headings into named chunks
- [ ] Each checker receives only the sections relevant to its dimension
- [ ] No single prompt contains both full documents inline
- [ ] Prompt size per checker call is bounded (configurable, default ~30KB)
- [ ] Section mapping is deterministic: dimension -> spec sections -> roadmap sections

**Dependencies**: FR-2 (parser)
```

**After**:
```markdown
### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only. The section splitter is a
parser-layer function in `spec_parser.py` (FR-2) that produces typed
`SpecSection` objects consumed by both structural checkers (FR-1) and
the semantic layer (FR-4).

**Section Splitter Specification**:

The splitter operates on raw markdown and produces a list of `SpecSection`
objects. It is deterministic: same input always produces the same sections
in the same order.

*Data structure* (to be defined in `spec_parser.py`):

```python
@dataclass(frozen=True)
class SpecSection:
    heading: str          # e.g., "3. Functional Requirements"
    heading_level: int    # 1-6 (from # count)
    content: str          # body text under this heading (up to next same-or-higher level heading)
    byte_size: int        # len(content.encode('utf-8'))
    source: str           # "spec" or "roadmap"
    cross_refs: list[str] # requirement IDs referenced in this section (e.g., ["FR-1", "NFR-3"])
```

*Splitting rules*:
1. Split on `## N. Section Name` headings for spec (H2 = top-level sections)
2. Split on `## Phase N:` or `## M-N:` headings for roadmap
3. Nested headings (H3, H4) remain within their parent H2 section
4. YAML frontmatter is extracted separately (FR-2) and excluded from sections
5. Content between document start and first heading is captured as section with `heading="preamble"`

*Dimension-to-section mapping* (deterministic, defined as a module-level dict):

| Dimension (FR-1) | Primary Spec Sections | Supplementary Sections |
|-------------------|----------------------|----------------------|
| Signatures | 3. Functional Requirements | 4. Non-Functional Requirements (for threshold sigs) |
| Data Models | 4.1/4.2/4.3 manifest tables | 3. (for dataclass refs) |
| Gates | 3. (gate-related FRs) | 5. User Stories (for gate behavior) |
| CLI Options | 5.1 CLI table | 3. (for config refs) |
| NFRs | 4. Non-Functional Requirements | 6. Resolved Questions (for threshold context) |

The mapping is extensible: new dimensions add rows without changing existing mappings.

**Acceptance Criteria**:
- [ ] `SpecSection` dataclass defined in `spec_parser.py` with fields: heading, heading_level, content, byte_size, source, cross_refs
- [ ] `split_into_sections(text: str, source: str) -> list[SpecSection]` function in `spec_parser.py`
- [ ] Spec is split by `## N. Section Name` headings into named chunks
- [ ] Roadmap is split by phase/task headings into named chunks
- [ ] Splitter is deterministic: same input -> same output (no randomness, no LLM)
- [ ] Each checker receives only the sections relevant to its dimension via a `DIMENSION_SECTION_MAP`
- [ ] Cross-references (requirement IDs) extracted per section and available as `cross_refs` field
- [ ] Supplementary sections included when cross-references link to them (Resolved Question #5)
- [ ] No single prompt contains both full documents inline
- [ ] Prompt size per checker call is bounded (configurable, default ~30KB)
- [ ] Section mapping is deterministic: dimension -> spec sections -> roadmap sections
- [ ] Empty documents produce an empty section list without errors

**Dependencies**: FR-2 (parser provides heading extraction and ID regex)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-5 section, expanded)

### Risk: **LOW-MEDIUM**
Additive expansion. Original 6 acceptance criteria are preserved (some reworded). New criteria specify the splitter algorithm and data structure. Risk that the `SpecSection` dataclass definition in the spec may drift from implementation, but since `spec_parser.py` does not exist yet, the spec text IS the authoritative definition.

### Requires Code Changes: **Yes** (this is the point)
`spec_parser.py` must be created with `SpecSection` and `split_into_sections()`. The `SemanticCheckRequest` in `semantic_layer.py:137-138` should be updated from `list[Any]` to `list[SpecSection]` once the type is available.

---

## Proposal #2: Minimal FR-5 Patch — Add Splitter Function Signature and Location Only

**Rationale**: The lightest possible fix. Acknowledges the gap by naming the function, its location, and its return type, without specifying the full algorithm. Leaves implementation details to the implementer. Best if the team prefers spec-as-intent over spec-as-design.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Before** (FR-5 Description, lines 280-282):
```markdown
**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only.
```

**After**:
```markdown
**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only.

**Implementation**: The section splitter is `split_into_sections()` in
`spec_parser.py` (FR-2). It returns a list of section objects with at
minimum `heading: str` and `content: str` fields, matching the interface
already expected by `SemanticCheckRequest` in `semantic_layer.py`.
Currently no section-splitting logic exists; `_truncate_to_budget()` in
`semantic_layer.py` handles byte-budget enforcement but does not split
by heading structure.
```

Also add one new acceptance criterion:

**Before** (last AC line):
```markdown
- [ ] Section mapping is deterministic: dimension -> spec sections -> roadmap sections
```

**After**:
```markdown
- [ ] Section mapping is deterministic: dimension -> spec sections -> roadmap sections
- [ ] `split_into_sections(text: str, source: str)` implemented in `spec_parser.py` and used by all checkers and the semantic layer
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-5 Description paragraph + one AC line)

### Risk: **LOW**
Two small additions. No existing text changed. Does not specify the data structure, which means `semantic_layer.py`'s existing `list[Any]` typing remains unresolved.

### Requires Code Changes: **Yes**
`spec_parser.py` must be created with `split_into_sections()`.

---

## Proposal #3: Relocate Section Splitting to semantic_layer.py as Private Helper

**Rationale**: An alternative architecture. Instead of placing the splitter in `spec_parser.py` (which does not exist yet), add it as a private function in `semantic_layer.py` where the consumer already lives. This avoids creating a dependency on an unbuilt module and lets the semantic layer self-contain its chunking logic. The splitter can be extracted to `spec_parser.py` later when FR-2 is implemented.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Before** (FR-5, lines 278-293, entire section):
```markdown
### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only.

**Acceptance Criteria**:
- [ ] Spec is split by `## N. Section Name` headings into named chunks
- [ ] Roadmap is split by phase/task headings into named chunks
- [ ] Each checker receives only the sections relevant to its dimension
- [ ] No single prompt contains both full documents inline
- [ ] Prompt size per checker call is bounded (configurable, default ~30KB)
- [ ] Section mapping is deterministic: dimension -> spec sections -> roadmap sections

**Dependencies**: FR-2 (parser)
```

**After**:
```markdown
### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only.

**Implementation strategy**: The section splitter has two implementation
phases:

1. **Phase 1 (immediate)**: `_split_by_headings()` private function in
   `semantic_layer.py`, co-located with `_truncate_to_budget()` and
   `build_semantic_prompt()`. Splits markdown by H2 headings using regex.
   Returns list of `(heading: str, content: str)` tuples.

2. **Phase 2 (when FR-2 ships)**: Extract to `spec_parser.py` as public
   `split_into_sections()` with full `SpecSection` dataclass, cross-ref
   extraction, and dimension mapping. `semantic_layer.py` imports from
   `spec_parser` instead of using its private helper.

**Current gap**: `_truncate_to_budget()` (semantic_layer.py:145) handles
byte-budget enforcement via tail-truncation but does NOT split by heading
structure. `SemanticCheckRequest.spec_sections` and `.roadmap_sections`
(semantic_layer.py:137-138) expect pre-split section objects, but no code
produces them.

**Acceptance Criteria**:
- [ ] Spec is split by `## N. Section Name` headings into named chunks
- [ ] Roadmap is split by phase/task headings into named chunks
- [ ] Section splitter function exists (initially in `semantic_layer.py`, migrates to `spec_parser.py` with FR-2)
- [ ] Each checker receives only the sections relevant to its dimension
- [ ] No single prompt contains both full documents inline
- [ ] Prompt size per checker call is bounded (configurable, default ~30KB)
- [ ] Section mapping is deterministic: dimension -> spec sections -> roadmap sections
- [ ] Splitting is pure Python (no LLM calls) and deterministic

**Dependencies**: None for Phase 1. FR-2 (parser) for Phase 2 migration.
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-5 section, restructured)

### Risk: **MEDIUM**
Changes the FR-5 dependency from "FR-2 required" to "FR-2 optional (Phase 2)." This unblocks FR-5 implementation before FR-2 exists, which may be desirable since `spec_parser.py` is on the critical path (ISS-015). However, it creates a temporary private function that must be migrated later, adding a refactoring step.

### Requires Code Changes: **Yes**
Add `_split_by_headings()` to `semantic_layer.py`. Later extract to `spec_parser.py`.

---

## Ranking Summary

| Rank | Proposal | Disruption | Completeness | Unblocks Implementation | Recommendation |
|------|----------|-----------|--------------|------------------------|----------------|
| 1 | #1 (Full splitter spec in FR-5) | Medium | Highest | Yes, after FR-2 | Best if FR-2 will be built first or concurrently |
| 2 | #3 (Phase 1/2 in semantic_layer) | Medium | High | Yes, immediately | Best if FR-5 must ship before FR-2 (mitigates ISS-015 critical path risk) |
| 3 | #2 (Minimal function signature) | Low | Partial | Yes, after FR-2 | Best if the team prefers minimal spec changes |

**Recommended approach**: **Proposal #1**. It provides the complete specification that an implementer needs (data structure, splitting rules, dimension mapping), aligns with the spec's existing pattern of detailed acceptance criteria, and matches the architecture implied by `SemanticCheckRequest` which already expects typed section objects. The `SpecSection` dataclass belongs in `spec_parser.py` alongside the other parser outputs (FR-2).

If the critical path concern from ISS-015 is acute (FR-2 may be delayed), fall back to **Proposal #3** which decouples FR-5 from FR-2 via a phased approach.
