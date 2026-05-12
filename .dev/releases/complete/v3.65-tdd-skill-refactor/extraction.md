---
spec_source: "tdd-refactor-spec.md"
generated: "2026-04-03T00:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 7
nonfunctional_requirements: 4
total_requirements: 11
complexity_score: 0.53
complexity_class: MEDIUM
domains_detected: [skill-architecture, content-migration, build-tooling, quality-assurance]
risks_identified: 5
dependencies_identified: 7
success_criteria_count: 14
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 114.0, started_at: "2026-04-03T03:33:08.140985+00:00", finished_at: "2026-04-03T03:35:02.154353+00:00"}
---

## Functional Requirements

### FR-TDD-R.1: Decomposed SKILL.md under 500 lines with behavioral protocol only

**Priority**: High  
**Type**: Structural refactoring  
**Description**: Refactored SKILL.md retains invocation behavior, Stage A/B control flow, and explicit load directives while removing all phase-specific HOW payloads (agent prompts, checklists, mapping tables, BUILD_REQUEST template, operational guidance).

**Acceptance Criteria**:
- FR-TDD-R.1a: `SKILL.md` is strictly under 500 lines.
- FR-TDD-R.1b: Contains frontmatter, extended metadata comment, Purpose/Input/Tier sections.
- FR-TDD-R.1c: Contains Stage A protocol and Stage B delegation protocol.
- FR-TDD-R.1d: Contains Will Do / Will Not Do boundaries.
- FR-TDD-R.1e: Contains explicit refs loading declarations mapping phases to ref files.

**Dependencies**: FR-TDD-R.2 through FR-TDD-R.6 (content must be relocated before SKILL.md can be reduced).

---

### FR-TDD-R.2: refs/agent-prompts.md with all agent templates (word-for-word)

**Priority**: High  
**Type**: Content migration  
**Description**: Move all agent prompt templates verbatim from canonical source lines 537–959 into a dedicated refs file.

**Acceptance Criteria**:
- FR-TDD-R.2a: File exists at `src/superclaude/skills/tdd/refs/agent-prompts.md`.
- FR-TDD-R.2b: After `make sync-dev`, dev copy exists at `.claude/skills/tdd/refs/agent-prompts.md`.
- FR-TDD-R.2c: Includes all 8 agent prompts: Codebase, Web, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly.
- FR-TDD-R.2d: Diff against source lines 537–959 shows zero textual drift.

**Dependencies**: None.

---

### FR-TDD-R.3: refs/validation-checklists.md with all checklists (word-for-word)

**Priority**: High  
**Type**: Content migration  
**Description**: Move synthesis quality checklist, assembly process, validation checklist, and content rules verbatim from canonical source lines 1106–1245.

**Acceptance Criteria**:
- FR-TDD-R.3a: File exists at `src/superclaude/skills/tdd/refs/validation-checklists.md`.
- FR-TDD-R.3b: After `make sync-dev`, dev copy exists at `.claude/skills/tdd/refs/validation-checklists.md`.
- FR-TDD-R.3c: Contains source lines 1106–1245 content blocks verbatim.
- FR-TDD-R.3d: Numbering and checkbox structure preserved exactly.

**Dependencies**: None.

---

### FR-TDD-R.4: refs/synthesis-mapping.md with mapping table + output structure (word-for-word)

**Priority**: High  
**Type**: Content migration  
**Description**: Move output structure and synthesis mapping table verbatim from canonical source lines 962–1105.

**Acceptance Criteria**:
- FR-TDD-R.4a: File exists at `src/superclaude/skills/tdd/refs/synthesis-mapping.md`.
- FR-TDD-R.4b: After `make sync-dev`, dev copy exists at `.claude/skills/tdd/refs/synthesis-mapping.md`.
- FR-TDD-R.4c: All section headers and tables preserved verbatim.
- FR-TDD-R.4d: No drift in template section numbering.

**Dependencies**: None.

---

### FR-TDD-R.5: refs/build-request-template.md with BUILD_REQUEST format (word-for-word)

**Priority**: High  
**Type**: Content migration with controlled path-reference updates  
**Description**: Move Stage A.7 BUILD_REQUEST template from canonical source lines 341–492. Body retained verbatim except for an explicitly allowlisted set of path-reference updates required by the decomposition.

**Acceptance Criteria**:
- FR-TDD-R.5a: File exists at `src/superclaude/skills/tdd/refs/build-request-template.md`.
- FR-TDD-R.5b: After `make sync-dev`, dev copy exists at `.claude/skills/tdd/refs/build-request-template.md`.
- FR-TDD-R.5c: BUILD_REQUEST body retained verbatim except path-reference updates per Section 12.2 allowlist.
- FR-TDD-R.5d: SKILL CONTEXT references updated to refs file paths per the cross-reference map:
  - "Agent Prompt Templates section" → `refs/agent-prompts.md`
  - "Synthesis Mapping Table section" → `refs/synthesis-mapping.md`
  - "Synthesis Quality Review Checklist section" → `refs/validation-checklists.md`
  - "Assembly Process section" → `refs/validation-checklists.md`
  - "Validation Checklist section" → `refs/validation-checklists.md`
  - "Content Rules section" → `refs/validation-checklists.md`
  - "Tier Selection section" → remains in SKILL.md (no update needed)

**Dependencies**: FR-TDD-R.2, FR-TDD-R.3, FR-TDD-R.4 (destination files must exist for references to resolve).

---

### FR-TDD-R.6: Explicit per-phase loading declarations in SKILL.md

**Priority**: High  
**Type**: Architectural contract  
**Description**: SKILL.md declares exactly which refs files load at each phase and by which actor (orchestrator vs builder). Enforces phase isolation via forbidden-load declarations.

**Acceptance Criteria**:
- FR-TDD-R.6a: Stage A.7 declaration for `refs/build-request-template.md` load by orchestrator is explicit.
- FR-TDD-R.6b: Builder load dependencies for `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` are explicit.
- FR-TDD-R.6c: No phase loads unnecessary refs (conformance to phase contract matrix in spec Section 5.3).
- FR-TDD-R.6d: Contract validation rules enforced: `declared_loads ∩ forbidden_loads = ∅` and `runtime_loaded_refs ⊆ declared_loads` for every phase.

**Dependencies**: FR-TDD-R.1.

---

### FR-TDD-R.7: Fidelity verification — zero content loss, zero semantic drift

**Priority**: Critical  
**Type**: Quality gate  
**Description**: Every instructional block from the original TDD skill (all 1,364 lines) is mapped to a destination file with checksum markers and verified against an explicit transformation allowlist.

**Acceptance Criteria**:
- FR-TDD-R.7a: Fidelity index covers all source lines 1–1364.
- FR-TDD-R.7b: Every block has destination + checksum markers (first 10 words, last 10 words).
- FR-TDD-R.7c: Allowed transformations limited exclusively to path-reference rewrites listed in Section 12.2 and the appendix allowlist.
- FR-TDD-R.7d: Forbidden transformations enforced: no wording edits, header renames, numbering changes, checklist reorder, markdown table schema changes.
- FR-TDD-R.7e: Normalized diff policy explicit: line-ending and trailing-whitespace normalization allowed; all other textual diffs fail.
- FR-TDD-R.7f: No template sentinel placeholders remain in any output files.

**Dependencies**: FR-TDD-R.1 through FR-TDD-R.6 (all migrations must complete before full fidelity can be verified).

---

### Implicit Functional Requirements (extracted from spec context)

### FR-TDD-R.8 (implicit): refs/operational-guidance.md with operational content (word-for-word)

**Priority**: High  
**Type**: Content migration  
**Description**: Move critical rules, quality signals, artifact locations, PRD-to-TDD pipeline, update/session guidance verbatim from canonical source lines 1246–1364. This file is required to achieve the <500 line SKILL.md budget while maintaining full fidelity (per Section 2.1 and Architecture Section 4.1).

**Acceptance Criteria**:
- FR-TDD-R.8a: File exists at `src/superclaude/skills/tdd/refs/operational-guidance.md`.
- FR-TDD-R.8b: After `make sync-dev`, dev copy exists at `.claude/skills/tdd/refs/operational-guidance.md`.
- FR-TDD-R.8c: Contains source lines 1246–1364 verbatim.
- FR-TDD-R.8d: Zero textual drift from source.

**Dependencies**: None.

> **Note**: This requirement is explicitly described in Sections 2.1, 4.1, and 4.6 (step 5) but lacks a dedicated FR-TDD-R.x identifier in Section 3. It is functionally equivalent in specification detail to FR-TDD-R.2 through FR-TDD-R.5.

---

## Non-Functional Requirements

### NFR-TDD-R.1: Invocation token efficiency

**Category**: Performance  
**Target**: Remove phase-specific payload from baseline invocation token footprint.  
**Measurement**: Compare pre-refactor vs post-refactor SKILL.md token count. Post-refactor SKILL.md should be significantly smaller (target: <500 lines vs original 1,364 lines — roughly 63% reduction in baseline load).  
**Rationale**: Content needed only during specific phases (A.7 builder context) should not be loaded at invocation time.

### NFR-TDD-R.2: Deterministic fidelity

**Category**: Correctness / Integrity  
**Target**: Zero textual drift in migrated verbatim blocks.  
**Measurement**: Block-wise diff checks against original source line ranges. Only line-ending and trailing-whitespace normalization permitted. All other diffs are failures.  
**Rationale**: Prevents semantic drift that could subtly alter agent behavior or checklist outcomes.

### NFR-TDD-R.3: Loading discipline

**Category**: Architectural integrity  
**Target**: No unnecessary refs loaded outside declared phases.  
**Measurement**: Contract conformance audit per phase contract matrix (spec Section 5.3). Verify `runtime_loaded_refs ⊆ declared_loads` and `declared_loads ∩ forbidden_loads = ∅`.  
**Rationale**: Lazy loading is the architectural driver; violating phase boundaries negates the refactor's purpose.

### NFR-TDD-R.4: Maintainability

**Category**: Maintainability  
**Target**: Clear file ownership by concern with auditable source-to-destination mapping.  
**Measurement**: Each refs file has a single well-defined concern. Fidelity index provides traceable mapping from every source line to its destination.  
**Rationale**: Future edits to specific concerns (e.g., agent prompts) should require touching only one file.

---

## Complexity Assessment

**Score**: 0.53  
**Class**: MEDIUM

**Scoring Rationale**:

| Factor | Weight | Score | Notes |
|--------|--------|-------|-------|
| Scope breadth | 0.15 | 0.4 | Single skill, contained within tdd/ directory |
| Technical depth | 0.20 | 0.5 | Content migration with strict fidelity constraints, but no algorithmic complexity |
| Integration surface | 0.15 | 0.4 | Touches build pipeline (make sync-dev/verify-sync) and phase loading contracts |
| Risk of regression | 0.20 | 0.7 | Strict verbatim fidelity requirement means any drift is a defect; BUILD_REQUEST cross-references must resolve correctly |
| Number of new artifacts | 0.15 | 0.6 | 5 new refs files + modified SKILL.md + sync validation |
| Novelty | 0.15 | 0.4 | Follows established pattern (sc-adversarial-protocol refs/ decomposition) |

**Composite**: ~0.53 — firmly MEDIUM. The task is procedural (extract, relocate, verify) but carries meaningful fidelity risk and requires disciplined execution across multiple artifacts.

---

## Architectural Constraints

1. **Source of truth is `src/superclaude/`**: All edits MUST be made to canonical files under `src/superclaude/skills/tdd/`. Dev copies under `.claude/skills/tdd/` are produced only via `make sync-dev`.

2. **SKILL.md must stay under 500 lines**: Hard budget constraint. Behavioral protocol (WHAT/WHEN) stays; HOW content moves to refs/.

3. **Verbatim migration — no semantic edits**: All content blocks must be migrated word-for-word. The only permitted transformation is path-reference updates per the Section 12.2 allowlist.

4. **refs/ lazy-loading pattern**: Follows Developer Guide Sections 5.6, 9.3, 9.7. Refs files are loaded per-phase, not at invocation.

5. **Phase isolation contracts**: Each phase has declared loads and forbidden loads (Section 5.3). No phase may load refs outside its declared set.

6. **Implementation order is prescribed**: Steps 0–9 in Section 4.6 must be followed in sequence.

7. **Sync/verify pipeline**: `make sync-dev` followed by `make verify-sync` is mandatory after all canonical edits.

8. **No behavioral changes**: External skill interface, Stage A/B semantics, and `/task` execution semantics remain unchanged.

9. **Existing pattern conformance**: Decomposition follows the proven pattern established by `sc-adversarial-protocol/refs/`.

10. **Line count anchoring**: Fidelity accounting anchors to actual in-repo line count (1,364), not the prompt-cited count (1,387). Discrepancy is acknowledged in GAP-TDD-01.

---

## Risk Inventory

1. **Content loss during decomposition** — Severity: **HIGH**  
   Probability: Medium. Impact: High (lost instructions alter agent behavior silently).  
   Mitigation: Word-for-word fidelity index with block-level checksum markers (first 10 / last 10 words). Fidelity index covers all 1,364 lines. Block-wise diff tests in CI.

2. **Cross-reference breakage in BUILD_REQUEST** — Severity: **HIGH**  
   Probability: Medium. Impact: High (builder cannot locate refs, Stage A.7 fails).  
   Mitigation: Explicit cross-reference update matrix (Section 12.2) with grep validation. Only 7 reference updates in a closed allowlist.

3. **Wrong loading order** — Severity: **MEDIUM**  
   Probability: Low. Impact: Medium (builder spawned without required context).  
   Mitigation: Phase-to-ref contract with explicit load ordering (Section 5.3). Contract validation rules prevent intersection of declared and forbidden loads.

4. **Semantic drift in quality gates** — Severity: **HIGH**  
   Probability: Low. Impact: High (altered checklists produce different validation outcomes).  
   Mitigation: Checklist numbering and content diff validation. Forbidden transformation list explicitly bans numbering changes and checklist reorder.

5. **Source length discrepancy (1,387 vs 1,364) causes mapping ambiguity** — Severity: **MEDIUM**  
   Probability: Medium. Impact: Medium (fidelity index may reference wrong lines).  
   Mitigation: Anchor all mapping to actual in-repo line count (1,364). Discrepancy documented in GAP-TDD-01.

---

## Dependency Inventory

| # | Dependency | Type | Used By | Notes |
|---|-----------|------|---------|-------|
| 1 | `make sync-dev` | Build tooling | FR-TDD-R.2–R.5, FR-TDD-R.8 | Propagates canonical `src/` files to `.claude/` dev copies |
| 2 | `make verify-sync` | Build tooling | FR-TDD-R.7 | Validates src↔dev parity; CI-friendly |
| 3 | `/task` skill | Runtime dependency | Stage B delegation | Executes generated task files; must not require SKILL.md refs at runtime |
| 4 | `rf-task-builder` | Runtime dependency | Stage A.7 | Spawned by BUILD_REQUEST; consumes refs files |
| 5 | Developer Guide (Sections 5.6, 9.3, 9.7) | Architectural standard | FR-TDD-R.1, FR-TDD-R.6 | Mandates refs/ lazy-loading pattern |
| 6 | `sc-adversarial-protocol/refs/` | Structural pattern reference | Architecture | Provides proven decomposition pattern to follow |
| 7 | Fidelity index companion file | Artifact dependency | FR-TDD-R.7 | Located at `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md` |

---

## Success Criteria

| # | Criterion | Threshold | Measurement Method |
|---|-----------|-----------|-------------------|
| 1 | SKILL.md line count | Strictly < 500 lines | `wc -l` on canonical file |
| 2 | All 5 refs files exist in canonical location | 5/5 files present | `ls src/superclaude/skills/tdd/refs/` |
| 3 | All 5 refs files synced to dev location | 5/5 files present after `make sync-dev` | `ls .claude/skills/tdd/refs/` |
| 4 | `make verify-sync` passes | Exit code 0, zero drift | CI pipeline execution |
| 5 | Fidelity index covers lines 1–1364 | 100% coverage, zero unmapped lines | Fidelity index audit |
| 6 | Zero textual drift in verbatim blocks | Block-wise diff = empty (after normalization) | Diff tests against source line ranges |
| 7 | Only allowlisted transformations applied | All diffs match Section 12.2 cross-reference map | Transformation allowlist test |
| 8 | No template sentinel placeholders | Zero matches for `{{`, `<placeholder>`, etc. | Grep sentinel test across all output files |
| 9 | Phase contract conformance | All phases satisfy `declared_loads ∩ forbidden_loads = ∅` | Phase loading matrix test |
| 10 | BUILD_REQUEST references resolve | All 6 updated references point to existing refs files | Grep + file existence check |
| 11 | 8 agent prompts present in refs/agent-prompts.md | 8/8 identified | Content audit |
| 12 | Checklist numbering preserved | Exact match with original | Structural diff |
| 13 | Stage A/B behavioral parity | No execution semantic changes | Functional parity dry run |
| 14 | Invocation token reduction | Post-refactor SKILL.md tokens < pre-refactor | Token count comparison |

---

## Open Questions

| # | Question | Impact | Status |
|---|----------|--------|--------|
| OQ-1 | **Line count discrepancy**: The master prompt cites 1,387 lines while the in-repo file is 1,364 lines (GAP-TDD-01). Which count was used to determine the source line ranges in the spec (e.g., "lines 537–959")? If the ranges were determined from the 1,387-line version, they may be off by up to 23 lines against the actual file. | High — incorrect line ranges would cause content to be migrated to wrong refs files | **Needs verification**: Line ranges should be validated against the actual canonical file before implementation begins. |
| OQ-2 | **Operational guidance source range**: Section 4.6 step 5 assigns lines 1246–1364 to `refs/operational-guidance.md`, but Section 4.1 doesn't specify source line ranges for this file (unlike the other refs files which have explicit ranges in Section 3). Is 1246–1364 the correct and complete range? | Medium — could miss content or duplicate content from validation-checklists.md (lines 1106–1245) | **Needs verification**: Confirm no gap or overlap between validation-checklists (1106–1245) and operational-guidance (1246–1364). |
| OQ-3 | **Missing FR for operational-guidance.md**: Section 3 defines FR-TDD-R.1 through FR-TDD-R.7 but has no dedicated FR for `refs/operational-guidance.md`, despite it being listed as a required file in Sections 2.1, 4.1, and 4.6. Was this an oversight or is it intentionally covered under FR-TDD-R.1? | Low — the file is well-specified elsewhere but lacks a formal acceptance criteria block | Extracted as implicit FR-TDD-R.8 in this document. |
| OQ-4 | **Frontmatter block (lines 1–~15)**: The spec's content block inventory (B01–B34) is in an external fidelity index file. Does the fidelity index account for the YAML frontmatter block at the top of SKILL.md? Frontmatter must be preserved in the refactored SKILL.md but could be overlooked if not explicitly inventoried. | Low — likely covered but worth confirming | **Needs verification** against fidelity-index.md. |
| OQ-5 | **Lines 493–536 disposition**: The spec maps lines 341–492 (BUILD_REQUEST) and 537–959 (agent prompts) but does not explicitly assign lines 493–536. What content occupies this range and where does it migrate? | Medium — potential unmapped content gap | **Needs verification** against actual file and fidelity index. |
