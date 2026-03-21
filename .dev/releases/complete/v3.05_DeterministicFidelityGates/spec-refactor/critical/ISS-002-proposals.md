# ISS-002: semantic_layer.py Listed as CREATE but Already Exists

**Issue**: The v3.05 spec treats `semantic_layer.py` as a greenfield module to build, but it already exists (v3.0, 337 lines) with prompt budget constants, `build_semantic_prompt()`, debate scoring (`RubricScores`, `score_argument`, `judge_verdict`), and debate-registry wiring.

**Affected Spec Section**: FR-4 (Residual Semantic Layer with Adversarial Validation), FR-4.1, FR-4.2

**Source of Truth**: `src/superclaude/cli/roadmap/semantic_layer.py` at commit `f4d9035`

---

## Proposal #1: Reclassify FR-4 from "Build" to "Complete" (Minimal Spec Text Changes)

**Approach**: Change FR-4's framing from building a new module to completing the existing one. Add an "Existing Baseline" note to FR-4 and mark already-satisfied acceptance criteria as done. No structural reorganization of the spec.

### Spec Text Changes

**Change 1 — FR-4 description (lines 172-178)**

BEFORE:
```
### FR-4: Residual Semantic Layer with Adversarial Validation

**Description**: After structural checkers complete, a residual LLM pass
handles the ~30% of checks that require semantic judgment (prose sufficiency,
spec contradiction resolution, additive-but-benign assessment). When the
semantic layer assigns HIGH severity, it does NOT auto-accept. Instead, it
triggers a lightweight adversarial debate to validate the rating.
```

AFTER:
```
### FR-4: Residual Semantic Layer with Adversarial Validation

**Existing baseline**: `semantic_layer.py` (337 lines) already implements:
prompt budget constants (FR-4.2), `build_semantic_prompt()` with budget
enforcement, debate scoring (`RubricScores`, `score_argument`, `judge_verdict`),
prosecutor/defender templates, and `wire_debate_verdict()`. This FR specifies
the **remaining orchestration** to complete: `validate_semantic_high()` and
`run_semantic_layer()` entry points, plus one modification (TRUNCATION_MARKER
must include heading name).

**Description**: After structural checkers complete, a residual LLM pass
handles the ~30% of checks that require semantic judgment (prose sufficiency,
spec contradiction resolution, additive-but-benign assessment). When the
semantic layer assigns HIGH severity, it does NOT auto-accept. Instead, it
triggers a lightweight adversarial debate to validate the rating.
```

**Change 2 — FR-4.2 acceptance criteria (lines 266-272)**

BEFORE:
```
**Acceptance Criteria** (FR-4.2):
- [ ] `MAX_PROMPT_BYTES = 30_720` as configurable module constant
- [ ] Budget ratios are module-level constants, overridable via config
- [ ] Oversized sections are tail-truncated on line boundaries with visible markers
- [ ] `assert` before LLM call confirms prompt <= budget
- [ ] Template exceeding 5% allocation raises `ValueError`
- [ ] Empty sections produce a valid prompt without errors
```

AFTER:
```
**Acceptance Criteria** (FR-4.2):
- [x] `MAX_PROMPT_BYTES = 30_720` as configurable module constant *(v3.0: semantic_layer.py:20)*
- [x] Budget ratios are module-level constants, overridable via config *(v3.0: semantic_layer.py:23-26)*
- [x] Oversized sections are tail-truncated on line boundaries with visible markers *(v3.0: `_truncate_to_budget()`)*
- [x] `assert` before LLM call confirms prompt <= budget *(v3.0: semantic_layer.py:230)*
- [x] Template exceeding 5% allocation raises `ValueError` *(v3.0: semantic_layer.py:192)*
- [ ] Empty sections produce a valid prompt without errors
- [ ] TRUNCATION_MARKER includes heading name: `[TRUNCATED: N bytes omitted from '<heading>']`
```

**Change 3 — FR-4.1 acceptance criteria (lines 234-239), add baseline acknowledgment**

BEFORE:
```
**Acceptance Criteria** (FR-4.1):
- [ ] Prosecutor and defender execute in parallel (2 LLM calls, not sequential)
- [ ] Judge is deterministic Python -- same scores always produce the same verdict
- [ ] Conservative tiebreak: margin within +/-0.15 always produces CONFIRM_HIGH
- [ ] Debate output YAML written per finding with rubric scores, margin, and verdict
- [ ] Registry updated with `debate_verdict` and `debate_transcript` reference after each debate
```

AFTER:
```
**Acceptance Criteria** (FR-4.1):
- [ ] Prosecutor and defender execute in parallel (2 LLM calls, not sequential)
- [x] Judge is deterministic Python -- same scores always produce the same verdict *(v3.0: `score_argument()` + `judge_verdict()`)*
- [x] Conservative tiebreak: margin within +/-0.15 always produces CONFIRM_HIGH *(v3.0: `judge_verdict()` line 302-308)*
- [ ] Debate output YAML written per finding with rubric scores, margin, and verdict
- [x] Registry updated with `debate_verdict` and `debate_transcript` reference after each debate *(v3.0: `wire_debate_verdict()`)*
- [ ] `validate_semantic_high()` orchestrator function exists and is callable
- [ ] `run_semantic_layer()` top-level entry point exists and is callable
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-4, FR-4.1, FR-4.2 sections)

### Risk: **LOW**
Only adds clarifying text and marks existing work as done. Does not change any acceptance criteria semantics or remove any requirements. The spec remains the single source of truth for what MUST be built; it simply stops claiming already-built things as TODO.

### Requires Code Changes: **YES (minor)**
- `semantic_layer.py` line 28: Change `TRUNCATION_MARKER = "[TRUNCATED: {} bytes omitted]"` to `TRUNCATION_MARKER = "[TRUNCATED: {} bytes omitted from '{}']"` and update `_truncate_to_budget()` signature to accept a heading name parameter.

---

## Proposal #2: Add a "v3.0 Baseline" Section to the Spec Preamble

**Approach**: Instead of scattering baseline acknowledgments across individual FRs, add a single new section (Section 2.5 or similar) that documents ALL pre-existing modules, then reference it from FR-4. This is the compatibility report's Priority 2 recommendation.

### Spec Text Changes

**Change 1 — Insert new section after Section 2 (after line 83)**

INSERT:
```
## 2.5 Existing v3.0 Baseline

The following modules were implemented during v3.0 and are already present in
`src/superclaude/cli/roadmap/`. The v3.05 requirements extend these modules
rather than creating them from scratch.

| Module | Lines | Already Implements | v3.05 Adds |
|--------|-------|--------------------|------------|
| convergence.py | 323 | DeviationRegistry lifecycle, compute_stable_id(), ConvergenceResult, _check_regression(), temp dir isolation + atexit | execute_fidelity_with_convergence(), handle_regression() |
| semantic_layer.py | 337 | Prompt budget constants (FR-4.2), build_semantic_prompt(), debate scoring (FR-4.1 rubric), wire_debate_verdict(), prosecutor/defender templates | validate_semantic_high(), run_semantic_layer(), TRUNCATION_MARKER heading fix |
| remediate_executor.py | 563 | Snapshot create/restore/cleanup | MorphLLM patch format, threshold 50->30%, per-file rollback |

All FR acceptance criteria satisfied by existing code are marked `[x]` with
source references. Only unchecked `[ ]` items require implementation.
```

**Change 2 — FR-4 description (lines 172-173)**

BEFORE:
```
### FR-4: Residual Semantic Layer with Adversarial Validation
```

AFTER:
```
### FR-4: Residual Semantic Layer with Adversarial Validation *(extends existing semantic_layer.py — see Section 2.5)*
```

**Change 3** — Same FR-4.1 and FR-4.2 acceptance criteria changes as Proposal #1.

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (new Section 2.5, FR-4 header, FR-4.1, FR-4.2)

### Risk: **LOW-MEDIUM**
Slightly more invasive than Proposal #1 because it adds a new section and shifts section numbering conceptually. However, it solves ISS-002 AND the parallel issues with convergence.py (ISS-001) and remediate_executor.py (ISS-003) in one structural change. Risk of introducing inconsistency with existing section cross-references.

### Requires Code Changes: **YES (same minor change as Proposal #1)**
- TRUNCATION_MARKER heading name fix in `semantic_layer.py`.

---

## Proposal #3: Split FR-4 into FR-4-existing and FR-4-new Subsections

**Approach**: Restructure FR-4 internally into "inherited from v3.0" and "new for v3.05" subsections, making the implementation delta explicit within the FR itself.

### Spec Text Changes

**Change 1 — Restructure FR-4 (replace lines 172-274)**

BEFORE: FR-4 as a flat section with FR-4.1 and FR-4.2 as subsections.

AFTER:
```
### FR-4: Residual Semantic Layer with Adversarial Validation

**Description**: [unchanged]

**Semantic/structural boundary**: [unchanged]

#### FR-4-existing: v3.0 Baseline (no implementation work)

The following are already implemented in `semantic_layer.py` (337 lines, commit f4d9035):

| Component | Location | Spec Requirement Satisfied |
|-----------|----------|---------------------------|
| MAX_PROMPT_BYTES = 30_720 | Line 20 | FR-4.2 AC-1 |
| Budget ratio constants | Lines 23-26 | FR-4.2 AC-2 |
| _truncate_to_budget() | Lines 145-168 | FR-4.2 AC-3 |
| build_semantic_prompt() | Lines 171-234 | FR-4.2 AC-4, AC-5 |
| RubricScores dataclass | Lines 46-63 | FR-4.1 (judge determinism) |
| score_argument() | Lines 237-281 | FR-4.1 (rubric scoring) |
| judge_verdict() | Lines 284-308 | FR-4.1 (verdict + tiebreak) |
| wire_debate_verdict() | Lines 313-337 | FR-4.1 AC-5 (registry update) |
| Prosecutor/Defender templates | Lines 68-128 | FR-4.1 (prompt generation) |

#### FR-4-new: v3.05 Implementation Work

**New functions to add to semantic_layer.py**:
1. `validate_semantic_high(finding, registry, output_dir)` — orchestrates parallel prosecutor/defender via ClaudeProcess, parses YAML, calls score_argument + judge_verdict, writes debate YAML, calls wire_debate_verdict
2. `run_semantic_layer(request, config)` — top-level entry point: builds prompt, calls LLM, parses findings, triggers validate_semantic_high for HIGHs

**Modification**:
- TRUNCATION_MARKER: add heading name parameter

#### FR-4.1: Lightweight Debate Protocol
[unchanged content]

#### FR-4.2: Prompt Budget Enforcement (NFR-3)
[unchanged content, but with [x] marks per Proposal #1]
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-4 internal restructure)

### Risk: **MEDIUM**
Adds new subsection numbering (FR-4-existing, FR-4-new) which is non-standard relative to the rest of the spec's naming convention. Any external references to "FR-4" remain valid, but tooling or tasklist generators that parse FR numbering may need adjustment.

### Requires Code Changes: **YES (same minor change as Proposal #1)**
- TRUNCATION_MARKER heading name fix.

---

## Proposal #4: Replace FR-4 "Build" Language with Explicit Delta Spec

**Approach**: Rewrite FR-4's acceptance criteria to be purely delta-based — each criterion is prefixed with its action verb (KEEP, MODIFY, ADD) so an implementer knows exactly what to do vs. what to leave alone.

### Spec Text Changes

**Change 1 — FR-4 acceptance criteria (lines 185-192)**

BEFORE:
```
**Acceptance Criteria**:
- [ ] Semantic layer receives only dimensions/aspects not covered by structural checkers
- [ ] Semantic layer uses chunked input (per-section, not full-document inline)
- [ ] When semantic layer assigns HIGH: pipeline pauses, spawns adversarial debate
- [ ] Adversarial debate produces a verdict: CONFIRM_HIGH, DOWNGRADE_TO_MEDIUM, or DOWNGRADE_TO_LOW
- [ ] Verdict is recorded in the deviation registry with debate transcript reference
- [ ] Semantic MEDIUM and LOW findings are accepted without debate
- [ ] Semantic layer prompt includes the structural findings as context (to avoid re-checking what's already checked)
- [ ] All semantic findings are tagged with `source_layer="semantic"` (see FR-6)
```

AFTER:
```
**Acceptance Criteria**:
- [ ] **ADD** `run_semantic_layer()`: receives only dimensions/aspects not covered by structural checkers
- [x] **KEEP** Semantic layer uses chunked input (per-section, not full-document inline) *(v3.0: `build_semantic_prompt()` with `SemanticCheckRequest.spec_sections`)*
- [ ] **ADD** `validate_semantic_high()`: when semantic layer assigns HIGH, pipeline pauses, spawns adversarial debate
- [x] **KEEP** Adversarial debate produces a verdict: CONFIRM_HIGH, DOWNGRADE_TO_MEDIUM, or DOWNGRADE_TO_LOW *(v3.0: `judge_verdict()`)*
- [x] **KEEP** Verdict is recorded in the deviation registry with debate transcript reference *(v3.0: `wire_debate_verdict()`)*
- [ ] **ADD** Semantic MEDIUM and LOW findings are accepted without debate (logic in `run_semantic_layer()`)
- [x] **KEEP** Semantic layer prompt includes the structural findings as context *(v3.0: `build_semantic_prompt()` structural_findings param)*
- [ ] **ADD** All semantic findings are tagged with `source_layer="semantic"` (see FR-6)
```

**Change 2** — Apply same KEEP/MODIFY/ADD pattern to FR-4.1 and FR-4.2 acceptance criteria (same substantive marks as Proposal #1).

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-4, FR-4.1, FR-4.2 acceptance criteria)

### Risk: **MEDIUM**
Introduces a new convention (KEEP/MODIFY/ADD prefixes) not used elsewhere in the spec. If adopted, should be applied consistently to all FRs with existing baselines (FR-7, FR-9), which expands scope. Mixing conventions within one spec is worse than not having them.

### Requires Code Changes: **YES (same minor change as Proposal #1)**
- TRUNCATION_MARKER heading name fix.

---

## Proposal #5: Introduce a Separate "Implementation Delta" Companion Document

**Approach**: Leave the spec itself unchanged (it describes the desired end-state). Create a companion document that maps each spec requirement to its implementation status and specifies only the delta work.

### Spec Text Changes

**Change 1 — Add reference in FR-4 (after line 274)**

INSERT after FR-4.2 Dependencies line:
```
**Implementation delta**: See `spec-refactor/implementation-delta.md` for
line-by-line mapping of FR-4 requirements to existing code in semantic_layer.py.
Only items marked DELTA require implementation.
```

**Change 2 — Create companion document** at:
`v3.05_DeterministicFidelityGates/spec-refactor/implementation-delta.md`

Content would include the full mapping table from the compatibility report Section 2, extended with exact line references and DONE/DELTA/MODIFY status per acceptance criterion.

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (one-line reference addition per FR)
- New file: `spec-refactor/implementation-delta.md`

### Risk: **MEDIUM-HIGH**
Creates a second source of truth that can drift from the spec. Requires discipline to keep both in sync. The spec remains ambiguous on its own — a reader must consult two documents to understand what needs building. This is the least self-contained option.

### Requires Code Changes: **NO** (spec unchanged; delta doc is advisory)
- The TRUNCATION_MARKER fix would be documented in the delta doc but not enforced by spec text.

---

## Ranking Summary

| Rank | Proposal | Disruption | Correctness | Completeness | Recommendation |
|------|----------|-----------|-------------|--------------|----------------|
| 1 | **#1: Reclassify FR-4** | Minimal | High | FR-4 only | **Best for ISS-002 in isolation** |
| 2 | **#2: Baseline section** | Low-Medium | High | All 3 modules | **Best if resolving ISS-001/002/003 together** |
| 3 | **#3: Split FR-4** | Medium | High | FR-4 only | Good but non-standard subsection naming |
| 4 | **#4: KEEP/MODIFY/ADD** | Medium | High | FR-4 only | Good but requires spec-wide convention adoption |
| 5 | **#5: Companion doc** | Medium-High | Medium | All FRs | Avoid: dual source of truth risk |

**Recommended path**: Proposal #1 for immediate ISS-002 fix. If ISS-001 and ISS-003 are being resolved concurrently, adopt Proposal #2 instead (covers all three in one structural change).
