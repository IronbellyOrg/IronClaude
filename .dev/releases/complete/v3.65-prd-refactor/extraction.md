---
spec_source: "prd-refactor-spec.md"
generated: "2026-04-03T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 7
nonfunctional_requirements: 4
total_requirements: 11
complexity_score: 0.45
complexity_class: MEDIUM
domains_detected: [framework, tooling, skill-architecture]
risks_identified: 7
dependencies_identified: 5
success_criteria_count: 12
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 104.0, started_at: "2026-04-03T03:32:29.901749+00:00", finished_at: "2026-04-03T03:34:13.916368+00:00"}
---

## Functional Requirements

### FR-PRD-R.1: Decomposed SKILL.md Under 500 Lines

**Description**: Refactored SKILL.md contains only behavioral protocol (WHAT/WHEN) content and explicit loading declarations for refs/ files. Total line count 430-500.

**Acceptance Criteria**:
- SKILL.md line count between 430 and 500 lines (430 soft floor, 500 hard ceiling)
- Contains: frontmatter, purpose/header, input section, tier selection, output locations, execution overview, Stage A protocol (A.1-A.6 + A.7 spawning + A.8 verification), Stage B delegation, critical rules, research quality signals, artifact locations, session management, updating an existing PRD
- Does NOT contain agent prompt templates, validation checklists, synthesis mapping tables, assembly process steps, content rules tables, BUILD_REQUEST format, or output structure reference
- Contains explicit loading declarations at A.7 referencing specific refs/ files
- All cross-references formerly pointing to "section in SKILL.md" now point to correct refs/ file paths

**Dependencies**: None

---

### FR-PRD-R.2: refs/agent-prompts.md — All 8 Agent Templates

**Description**: Contains all 8 agent prompt templates moved word-for-word from original SKILL.md lines 553-967.

**Acceptance Criteria**:
- File exists at `.claude/skills/prd/refs/agent-prompts.md`
- Contains header explaining purpose and loading context
- Contains 8 agent prompt templates word-for-word identical to original:
  1. Codebase Research Agent Prompt (lines 558-637)
  2. Web Research Agent Prompt (lines 639-686)
  3. Synthesis Agent Prompt (lines 688-720)
  4. Research Analyst Agent Prompt / rf-analyst Completeness Verification (lines 722-759)
  5. Research QA Agent Prompt / rf-qa Research Gate (lines 761-804)
  6. Synthesis QA Agent Prompt / rf-qa Synthesis Gate (lines 806-846)
  7. Report Validation QA Agent Prompt / rf-qa Report Validation (lines 848-895)
  8. Assembly Agent Prompt / rf-assembler PRD Assembly (lines 897-967)
- Includes "Agent Prompt Templates" section header and introductory paragraph (lines 553-557)
- Includes "Common web research topics for PRDs" list after Web Research prompt (lines 679-686)
- Diff of each prompt template against original shows zero content changes (whitespace normalization permitted)

**Dependencies**: None

---

### FR-PRD-R.3: refs/validation-checklists.md — Checklists + Assembly Process + Content Rules

**Description**: Contains Synthesis Quality Review Checklist, Assembly Process (Steps 8-11), Validation Checklist (18+4 items), and Content Rules table, word-for-word from original lines 1108-1254.

**Acceptance Criteria**:
- File exists at `.claude/skills/prd/refs/validation-checklists.md`
- Contains header explaining purpose and loading context
- Synthesis Quality Review Checklist (9 criteria) word-for-word from lines 1108-1128
- Assembly Process (Steps 8-11) word-for-word from lines 1130-1193
- Validation Checklist (18 structural/semantic + 4 content quality checks) word-for-word from lines 1195-1235
- Content Rules table (10 rows) word-for-word from lines 1237-1254
- Retains all `> **Note:**` reference documentation markers
- Diff against original line ranges shows zero content changes

**Dependencies**: None

---

### FR-PRD-R.4: refs/synthesis-mapping.md — Mapping Table + Output Structure

**Description**: Contains Output Structure reference (PRD section outline) and Synthesis Mapping Table, word-for-word from original lines 969-1106.

**Acceptance Criteria**:
- File exists at `.claude/skills/prd/refs/synthesis-mapping.md`
- Contains header explaining purpose and loading context
- Output Structure section word-for-word from lines 969-1085 (full PRD section outline "1. Executive Summary" through "Document Approval")
- Synthesis Mapping Table word-for-word from lines 1087-1106 (9-row table)
- Retains all `> **Note:**` reference documentation markers
- Diff against original line ranges shows zero content changes

**Dependencies**: None

---

### FR-PRD-R.5: refs/build-request-template.md — BUILD_REQUEST Format

**Description**: Contains complete BUILD_REQUEST format block from original lines 347-508, with SKILL CONTEXT FILE references updated to refs/ paths.

**Acceptance Criteria**:
- File exists at `.claude/skills/prd/refs/build-request-template.md`
- Contains header explaining purpose and loading context
- Complete BUILD_REQUEST format block word-for-word from lines 347-508
- SKILL CONTEXT FILE references updated:
  - `"Agent Prompt Templates" section` → `refs/agent-prompts.md`
  - `"Synthesis Mapping Table" section` → `refs/synthesis-mapping.md`
  - `"Synthesis Quality Review Checklist" section` → `refs/validation-checklists.md`
  - `"Assembly Process" section` → `refs/validation-checklists.md`
  - `"Validation Checklist" section` → `refs/validation-checklists.md`
  - `"Content Rules" section` → `refs/validation-checklists.md`
  - `"Tier Selection" section` remains referencing SKILL.md
- All other content word-for-word identical
- Diff shows only the documented SKILL CONTEXT FILE path changes
- Phase 2 task file references updated: `from SKILL.md` → `from refs/agent-prompts.md` (and similar)

**Dependencies**: FR-PRD-R.2, FR-PRD-R.3, FR-PRD-R.4 (destination file paths must be known)

---

### FR-PRD-R.6: Per-Phase Loading Declarations in SKILL.md

**Description**: Refactored SKILL.md contains explicit instructions declaring which refs/ files to load at which phase.

**Acceptance Criteria**:
- Stage A.7 section contains loading declaration block distinguishing orchestrator from builder loading:
  - **Orchestrator loads**: `refs/build-request-template.md`
  - **Builder subagent loads** (referenced within BUILD_REQUEST): `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`
- Loading declaration uses concrete inline reference format (following sc-adversarial-protocol `See refs/...` pattern)
- No other phase loads refs/ files (A.1-A.6 use SKILL.md only; Stage B delegates to /task)
- Orchestrator context loads at most 2 refs simultaneously (SKILL.md + build-request-template.md)

**Dependencies**: FR-PRD-R.1

---

### FR-PRD-R.7: Fidelity Verification — Zero Content Loss

**Description**: Every line of instructional content from the original 1,373-line SKILL.md appears in either the refactored SKILL.md or one of the 4 refs/ files. Zero content dropped, zero semantic drift, zero paraphrasing.

**Acceptance Criteria**:
- Fidelity index at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` maps every content block with line ranges and destination files
- Diff of each of 8 agent prompt templates shows zero content changes
- Diff of each checklist/table shows zero content changes
- Diff of output structure and synthesis mapping table shows zero content changes
- Diff of BUILD_REQUEST shows only documented SKILL CONTEXT FILE path changes
- All behavioral content in refactored SKILL.md matches original line-for-line (except removal of moved blocks and addition of loading declarations)
- Combined line count of SKILL.md + all refs/ files is between 1,370 and 1,400 lines

**Dependencies**: FR-PRD-R.1 through FR-PRD-R.6

---

## Non-Functional Requirements

### NFR-PRD-R.1: SKILL.md Token Budget
- **Target**: <= 2,000 tokens on invocation
- **Measurement**: 430-480 lines at ~4.5 tokens/line = ~1,935-2,160 tokens
- **Note**: Upper bound slightly exceeds 2,000; acceptable given the soft nature of token estimation

### NFR-PRD-R.2: Per-Phase Token Overhead
- **Target**: Max 2 refs loaded by orchestrator at any point
- **Measurement**: Count refs loaded per phase in loading declarations

### NFR-PRD-R.3: Session Start Cost
- **Target**: ~50 tokens (name + description only)
- **Measurement**: Unchanged from current — frontmatter stays the same

### NFR-PRD-R.4: Zero Behavioral Regression
- **Target**: Identical execution behavior before and after refactoring
- **Measurement**: End-to-end test — invoke skill on test product and compare output structure

---

## Complexity Assessment

**Score**: 0.45 / 1.0
**Class**: MEDIUM

**Rationale**:
- **Content volume** (+0.15): 1,373 lines to decompose across 5 files with zero content loss — significant but mechanical
- **Cross-reference updates** (+0.10): BUILD_REQUEST contains multiple section references that must be precisely updated to refs/ paths; error-prone but well-documented in the spec's cross-reference map
- **Fidelity constraint** (+0.10): Word-for-word preservation requirement with diff-based verification raises the precision bar above a typical refactoring
- **Architectural simplicity** (-0.10): The decomposition pattern is well-established (sc-adversarial-protocol reference implementation exists); no novel design decisions required
- **Scope containment** (-0.10): Purely internal restructuring, no external interface changes, no behavioral changes, single-commit rollback possible
- **Gap simplicity** (-0.05): Only 2 gaps identified (GAP-01 duplicate table merge, GAP-02 section reference updates), both with clear resolutions
- **Low integration risk** (-0.05): No files outside `prd/` directory are modified; downstream `/task` skill reads task files not SKILL.md

---

## Architectural Constraints

1. **500-line SKILL.md ceiling**: Hard ceiling per Developer Guide Section 9.3. Soft floor at 430 lines.
2. **refs/ lazy-loading pattern**: Must follow the `sc-adversarial-protocol` refs/ architecture pattern (SKILL.md for behavioral flow, refs/ for HOW content loaded per-wave)
3. **Max 2-3 refs loaded concurrently**: Developer Guide guidance; spec targets max 2 in orchestrator context
4. **Word-for-word content preservation**: Zero paraphrasing, zero semantic drift — only structural relocation and documented cross-reference path updates
5. **Component sync workflow**: Edits to `.claude/skills/prd/` must be synced to `src/superclaude/skills/prd/` via `make sync-dev` and verified via `make verify-sync`
6. **Single commit implementation**: All changes in one commit on feature branch for atomic rollback
7. **Relative refs/ paths**: Builder subagent is spawned from the SKILL.md directory; all refs/ paths are relative to the skill directory
8. **No external interface changes**: Command invocation, inputs, and outputs remain identical
9. **B30/B05 merge strategy**: Append B30's 6 specific QA paths to B05's table; preserve B05's naming convention; do not resolve B30's cosmetic `[NN]-[topic].md` inconsistency

---

## Risk Inventory

1. **Content loss during decomposition** — Severity: HIGH, Probability: Low
   - Agent prompt word or line dropped during move
   - *Mitigation*: Word-for-word fidelity audit using diff against original line ranges; fidelity index provides first/last 10-word markers per block

2. **Cross-reference breakage** — Severity: HIGH, Probability: Medium
   - BUILD_REQUEST still references prose section names instead of refs/ paths
   - *Mitigation*: Explicit cross-reference map in fidelity index; grep for "section" references in BUILD_REQUEST post-refactoring

3. **Loading order wrong** — Severity: MEDIUM, Probability: Low
   - Refs loaded at wrong phase or not loaded at all
   - *Mitigation*: Phase-to-ref dependency matrix in Section 5.3; only one phase (A.7) loads refs

4. **Builder subagent can't find refs/ files** — Severity: MEDIUM, Probability: Low
   - Path resolution failure when builder attempts to read refs/
   - *Mitigation*: Builder spawned from SKILL.md directory; paths relative to skill directory; test by spawning builder and verifying reads

5. **Duplicate Artifact Locations table merged incorrectly** — Severity: LOW, Probability: Low
   - B30 entries lost or B05 entries corrupted during merge
   - *Mitigation*: Keep B05 intact, append B30's unique QA paths; explicit merge strategy documented in GAP-01

6. **refs/ file missing or renamed after refactoring** — Severity: MEDIUM, Probability: Low
   - File-not-found at runtime
   - *Mitigation*: Builder fails explicitly with file-not-found; rollback via `git revert`; failure is obvious and self-diagnosing

7. **Spec freshness — SKILL.md modified between spec creation and implementation** — Severity: MEDIUM, Probability: Low
   - Line ranges in fidelity index become stale
   - *Mitigation*: Implement before any content changes; re-verify fidelity index line ranges if SKILL.md changes

---

## Dependency Inventory

1. **sc-adversarial-protocol skill** (`.claude/skills/sc-adversarial-protocol/`) — Reference implementation of refs/ decomposition pattern; used as architectural template, not runtime dependency
2. **SuperClaude Developer Guide** (`docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`) — Defines the 500-line SKILL.md guidance, refs/ pattern, and lazy-loading rules that motivate this refactoring
3. **Fidelity index** (`.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`) — Content block inventory and cross-reference map required for implementation; must exist before implementation begins
4. **rf-task-builder subagent** — Runtime consumer of refs/ files during A.7; must be able to resolve relative refs/ paths from the skill directory
5. **`/task` skill** — Downstream executor (Stage B); reads task files not SKILL.md — no changes needed, but validates that decomposition is transparent to consumers
6. **`make sync-dev` / `make verify-sync`** — Build tooling required post-implementation to propagate changes from `.claude/` to `src/superclaude/` and verify sync

---

## Success Criteria

1. **SKILL.md line count**: 430-500 lines (hard ceiling at 500)
2. **refs/ file count**: Exactly 4 files in `refs/` directory
3. **Combined line count**: All 5 files total between 1,370 and 1,400 lines
4. **Agent prompt fidelity**: Diff of all 8 prompts against original shows zero content changes
5. **Checklist fidelity**: Diff of all checklists/tables against original shows zero content changes
6. **BUILD_REQUEST fidelity**: Diff shows only the 6 documented SKILL CONTEXT FILE path changes
7. **Zero stale section references**: `grep` for prose section references (e.g., `"Agent Prompt Templates section"`) in SKILL.md returns 0 matches
8. **Loading declarations present**: `grep 'refs/'` in SKILL.md shows declarations at A.7
9. **Cross-references updated in BUILD_REQUEST**: `grep 'refs/agent-prompts.md'` in build-request-template.md returns match
10. **Token budget**: SKILL.md estimated at <= 2,000 tokens on invocation
11. **Max concurrent refs**: Orchestrator loads at most 2 refs simultaneously
12. **Behavioral regression**: E2E invocation produces identical execution behavior (Stage A completes, task file created with all prompts baked in, Stage B completes with PRD written to expected output location)

---

## Open Questions

1. **NFR-PRD-R.1 token ceiling precision**: The spec targets <= 2,000 tokens but estimates 430-480 lines at ~4.5 tokens/line = ~1,935-2,160. The upper bound of the line range (480 lines) may exceed 2,000 tokens. Is 2,000 a hard ceiling or a guideline? If hard, the line count ceiling may need to drop from 500 to ~444.
   - *Spec's own answer*: The spec states 500 is the hard ceiling for lines and 2,000 is the token target. These two constraints may conflict at the margin. Clarify which takes precedence.

2. **B30 merge cosmetic inconsistency**: GAP-01 notes that B30 uses `[NN]-[topic].md` while B05 uses `[NN]-[topic-name].md`. The spec says "should NOT be resolved during this refactoring." Confirm this means both naming conventions will coexist in the merged table.

3. **Fidelity index existence**: FR-PRD-R.7 requires the fidelity index at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`. The spec references it throughout but does not define its creation as a functional requirement. Is it assumed to already exist, or is its creation an implicit prerequisite?

4. **Whitespace normalization scope**: FR-PRD-R.2 permits "whitespace normalization" in diffs. Clarify what is permitted — trailing whitespace removal only, or also indentation changes, blank line consolidation, or line-ending normalization?
