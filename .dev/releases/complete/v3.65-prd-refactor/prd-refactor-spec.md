# PRD Skill Refactoring — Release Specification

```yaml
---
title: "Decompose monolithic PRD skill into SKILL.md + refs/ architecture"
version: "1.0.0"
status: revised
feature_id: FR-PRD-REFACTOR
parent_feature: null
spec_type: refactoring
complexity_score: 0.45
complexity_class: MEDIUM
target_release: v3.8
authors: [user, claude]
created: 2026-04-02
quality_scores:
  clarity: 9.5
  completeness: 9.5
  testability: 9.5
  consistency: 9.5
  overall: 9.5
---
```

## 1. Problem Statement

The PRD skill at `.claude/skills/prd/SKILL.md` is a 1,373-line monolithic file that violates the SuperClaude Developer Guide's skill architecture best practices. When invoked, the entire file loads into context (~5,000+ tokens), including agent prompt templates, validation checklists, synthesis mapping tables, and assembly process instructions that are only needed during specific phases of execution. This wastes context budget on content the executing agent will never use in a given phase, and is inconsistent with the decomposition pattern established by the `sc-adversarial-protocol` skill (which uses `SKILL.md` for behavioral flow + `refs/` for detailed HOW content loaded per-wave).

The Developer Guide (Section 9.3) states: "Keep SKILL.md under 500 lines (behavioral intent only)" and "Move algorithms and templates to refs/ for lazy loading." The PRD skill violates both rules. The anti-pattern table (Section 9.7) explicitly lists "Monolithic SKILL.md" as a problem with the solution "Split into SKILL.md + refs/".

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| SKILL.md is 1,373 lines — 2.7x the 500-line guidance | `.claude/skills/prd/SKILL.md` | ~5,000+ tokens loaded on every invocation regardless of phase |
| 8 agent prompt templates embedded inline (~415 lines total) | Lines 553-967 of SKILL.md | Loaded even when executing scope discovery (Stage A) which never uses them |
| Validation checklists, assembly process, content rules embedded inline (~127 lines) | Lines 1108-1254 of SKILL.md | Loaded during Stage A when only Stage B Phase 6 needs them |
| BUILD_REQUEST template embedded inline (~165 lines) | Lines 344-508 of SKILL.md | Only needed during A.7 but loaded for all phases |
| Output structure + synthesis mapping embedded inline (~137 lines) | Lines 969-1106 of SKILL.md | Only needed during Phase 5-6 but loaded for all phases |
| Developer Guide Section 9.7 anti-pattern | `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 1155 | Explicitly identifies this pattern as an anti-pattern with solution |
| sc-adversarial-protocol demonstrates the correct refs/ pattern | `.claude/skills/sc-adversarial-protocol/` | Reference implementation of the refs/ lazy-loading decomposition pattern (4 refs/ files). Note: the adversarial SKILL.md itself is 2,935 lines — the reference is specifically to its refs/ architecture, not its SKILL.md size compliance. |

### 1.2 Scope Boundary

**In scope**:
- Decomposing the PRD SKILL.md into SKILL.md (~430-480 lines) + 4 refs/ files
- Updating internal cross-references (BUILD_REQUEST section references to SKILL.md become refs/ file paths)
- Adding explicit per-phase loading declarations in SKILL.md
- Word-for-word preservation of all agent prompts, checklists, tables, and content rules

**Out of scope**:
- Modifying the PRD skill's pipeline logic, phase structure, or execution behavior
- Changing agent prompt content, validation criteria, or content rules
- Adding new features or capabilities to the PRD skill
- Modifying any files outside the `prd/` skill directory
- Changing the PRD skill's external interface (command invocation, inputs, outputs)

## 2. Solution Overview

Decompose the monolithic `prd/SKILL.md` (1,373 lines) into a properly architected multi-file skill following the `sc-adversarial-protocol` pattern:

```
.claude/skills/prd/
  SKILL.md                        (~430-480 lines — behavioral protocol only)
  refs/
    agent-prompts.md              (~415 lines — all 8 agent prompt templates)
    build-request-template.md     (~165 lines — BUILD_REQUEST format)
    synthesis-mapping.md          (~137 lines — output structure + mapping table)
    validation-checklists.md      (~127 lines — checklists + assembly process + content rules)
```

The refactored SKILL.md retains all WHAT/WHEN content (behavioral protocol, Stage A scope discovery flow, Stage B delegation, critical rules, quality signals) and adds explicit loading declarations for each refs/ file at the point where it is needed. The refs/ files contain all HOW content (agent prompts, checklists, tables, templates) moved verbatim from the original.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Number of refs/ files | 4 files | 8 files (one per agent prompt), 2 files (prompts + everything else) | 4 files groups content by usage phase and keeps each ref at 127-415 lines (within the 500-1500 token guidance). 8 files would be too granular; 2 files would still load unnecessary content per phase. |
| Agent prompts in single file | All 8 prompts in `refs/agent-prompts.md` | Separate file per agent prompt | Agent prompts are always loaded together during A.7 (BUILD_REQUEST construction), and the task builder needs all of them at once to embed in checklist items. Splitting would require 8 separate load declarations for a single phase. |
| BUILD_REQUEST as separate ref | Dedicated `refs/build-request-template.md` | Keep in SKILL.md, merge with agent-prompts.md | The BUILD_REQUEST is the largest single block (~165 lines), only needed during A.7, and is a complete template that the task builder reads as a unit. Keeping it separate enables loading it only when spawning the builder. |
| Validation content in single file | Checklists + assembly process + content rules in one ref | Separate files for each | All validation content is loaded together during Phase 5-6 (synthesis QA + assembly + report validation). Splitting would require multiple load declarations for tightly coupled content. |
| Behavioral blocks stay in SKILL.md | Critical Rules, Research Quality Signals, Session Management | Move to refs/ | These are behavioral rules that apply across ALL phases and should be immediately available on skill invocation. Moving them to refs/ would require loading them at every phase, defeating the purpose. |

### 2.2 Workflow / Data Flow

```
Skill Invocation
  |
  v
SKILL.md loaded (~430-480 lines, ~2000 tokens)
  Contains: purpose, input, tier selection, output locations,
            execution overview, Stage A protocol (A.1-A.6),
            Stage B delegation, critical rules, quality signals,
            session management, update flow
  |
  v
Stage A: Scope Discovery (A.1 through A.6)
  No refs/ loaded — all behavioral content in SKILL.md
  |
  v
Stage A.7: Build Task File
  Load: refs/agent-prompts.md (~415 lines)
  Load: refs/build-request-template.md (~165 lines)
  [Builder reads prompts + BUILD_REQUEST template, creates task file]
  |
  v
Stage A.8: Verify Task File
  Unload refs/ from A.7 (no longer needed)
  |
  v
Stage B: Delegate to /task skill
  /task executes from task file (which has agent prompts baked in)
  |
  [When /task reaches Phase 5-6, the task file's embedded prompts
   reference validation criteria that were baked in during A.7
   from refs/validation-checklists.md and refs/synthesis-mapping.md]
```

**Loading budget compliance**: At most 2 refs are loaded simultaneously (during A.7: agent-prompts.md + build-request-template.md). This complies with the Developer Guide's "at most 2-3 refs loaded at any point" guidance.

**Note on refs/synthesis-mapping.md and refs/validation-checklists.md**: These files are read by the task builder during A.7 (as referenced in the BUILD_REQUEST's SKILL CONTEXT FILE section), not during Phase 5-6 directly. The builder bakes their content into the task file's self-contained checklist items. During actual Phase 5-6 execution, `/task` reads the task file (not the SKILL.md or refs/). Therefore, these refs are loaded during A.7 alongside the other refs, but because A.7 is a subagent spawn (the builder runs in its own context), the loading is sequential: the SKILL.md orchestrator loads build-request-template.md to construct the prompt, and the builder subagent loads agent-prompts.md, synthesis-mapping.md, and validation-checklists.md. Net effect: the orchestrator never loads more than 2 refs; the builder loads what it needs in its own context.

## 3. Functional Requirements

### FR-PRD-R.1: Decomposed SKILL.md Under 500 Lines

**Description**: The refactored SKILL.md contains only behavioral protocol (WHAT/WHEN) content and explicit loading declarations for refs/ files. Total line count is 430-480 lines.

**Acceptance Criteria**:
- [ ] SKILL.md line count is between 430 and 500 lines (430 is a soft floor — below is acceptable if it results from B30 deduplication; 500 is a hard ceiling)
- [ ] SKILL.md contains: frontmatter, purpose/header, input section, tier selection, output locations, execution overview, Stage A protocol (A.1-A.6 + A.7 spawning instruction + A.8 verification), Stage B delegation, critical rules, research quality signals, artifact locations, session management, updating an existing PRD
- [ ] SKILL.md does NOT contain any agent prompt templates, validation checklists, synthesis mapping tables, assembly process steps, content rules tables, BUILD_REQUEST format, or output structure reference
- [ ] SKILL.md contains explicit loading declarations at A.7 referencing the specific refs/ files to load
- [ ] All cross-references formerly pointing to "section in SKILL.md" now point to the correct refs/ file path

**Dependencies**: None

### FR-PRD-R.2: refs/agent-prompts.md — All 8 Agent Templates

**Description**: Contains all 8 agent prompt templates moved word-for-word from the original SKILL.md lines 553-967.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/agent-prompts.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains these 8 agent prompt templates, each word-for-word identical to the original:
  1. Codebase Research Agent Prompt (original lines 558-637)
  2. Web Research Agent Prompt (original lines 639-686)
  3. Synthesis Agent Prompt (original lines 688-720)
  4. Research Analyst Agent Prompt / rf-analyst Completeness Verification (original lines 722-759)
  5. Research QA Agent Prompt / rf-qa Research Gate (original lines 761-804)
  6. Synthesis QA Agent Prompt / rf-qa Synthesis Gate (original lines 806-846)
  7. Report Validation QA Agent Prompt / rf-qa Report Validation (original lines 848-895)
  8. Assembly Agent Prompt / rf-assembler PRD Assembly (original lines 897-967)
- [ ] Includes the section header "Agent Prompt Templates" and introductory paragraph (original lines 553-557)
- [ ] Includes the "Common web research topics for PRDs" list after the Web Research prompt (original lines 679-686)
- [ ] Diff of each prompt template against the original SKILL.md shows zero content changes (whitespace normalization permitted)

**Dependencies**: None

### FR-PRD-R.3: refs/validation-checklists.md — All Checklists + Assembly Process + Content Rules

**Description**: Contains the Synthesis Quality Review Checklist, Assembly Process (Steps 8-11), Validation Checklist (18+4 items), and Content Rules table, all moved word-for-word from the original SKILL.md lines 1108-1254.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/validation-checklists.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains the Synthesis Quality Review Checklist (9 criteria) word-for-word from original lines 1108-1128
- [ ] Contains the Assembly Process (Steps 8-11) word-for-word from original lines 1130-1193
- [ ] Contains the Validation Checklist (18 structural/semantic items + 4 content quality checks) word-for-word from original lines 1195-1235
- [ ] Contains the Content Rules table (10 rows) word-for-word from original lines 1237-1254
- [ ] Retains all "> **Note:**" reference documentation markers from the original
- [ ] Diff against original line ranges shows zero content changes

**Dependencies**: None

### FR-PRD-R.4: refs/synthesis-mapping.md — Mapping Table + Output Structure

**Description**: Contains the Output Structure reference (PRD section outline) and the Synthesis Mapping Table, moved word-for-word from the original SKILL.md lines 969-1106.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/synthesis-mapping.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains the Output Structure section word-for-word from original lines 969-1085 (including the full PRD section outline from "1. Executive Summary" through "Document Approval")
- [ ] Contains the Synthesis Mapping Table word-for-word from original lines 1087-1106 (9-row table mapping synth files to template sections)
- [ ] Retains all "> **Note:**" reference documentation markers from the original
- [ ] Diff against original line ranges shows zero content changes

**Dependencies**: None

### FR-PRD-R.5: refs/build-request-template.md — BUILD_REQUEST Format

**Description**: Contains the complete BUILD_REQUEST format block currently embedded in A.7 (original lines 347-508), including the TEMPLATE 02 PATTERN MAPPING, SKILL PHASES TO ENCODE, GRANULARITY REQUIREMENT, ESCALATION rules, and STEPS list.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/build-request-template.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains the complete BUILD_REQUEST format block word-for-word from original lines 347-508
- [ ] The SKILL CONTEXT FILE reference within BUILD_REQUEST is updated from `.claude/skills/prd/SKILL.md` section references to the correct refs/ file paths:
  - `"Agent Prompt Templates" section` becomes `refs/agent-prompts.md`
  - `"Synthesis Mapping Table" section` becomes `refs/synthesis-mapping.md`
  - `"Synthesis Quality Review Checklist" section` becomes `refs/validation-checklists.md`
  - `"Assembly Process" section` becomes `refs/validation-checklists.md`
  - `"Validation Checklist" section` becomes `refs/validation-checklists.md`
  - `"Content Rules" section` becomes `refs/validation-checklists.md`
  - `"Tier Selection" section` remains referencing `SKILL.md` (it stays in SKILL.md)
- [ ] All other content in the BUILD_REQUEST is word-for-word identical to the original
- [ ] Diff against original lines 347-508 shows only the SKILL CONTEXT FILE path changes listed above

**Dependencies**: FR-PRD-R.2, FR-PRD-R.3, FR-PRD-R.4 (must know the destination file paths)

### FR-PRD-R.6: Per-Phase Loading Declarations in SKILL.md

**Description**: The refactored SKILL.md contains explicit instructions declaring which refs/ files to load at which phase, following the pattern from the Developer Guide Section 5.6.

**Acceptance Criteria**:
- [ ] Stage A.7 section in SKILL.md contains a loading declaration block that distinguishes orchestrator loading from builder loading:
  - **Orchestrator loads**: `refs/build-request-template.md` (to construct the builder prompt)
  - **Builder subagent loads** (referenced within the BUILD_REQUEST): `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`
- [ ] The loading declaration uses concrete inline reference format (following the sc-adversarial-protocol `See refs/...` pattern):
  ```markdown
  ### A.7: Build the Task File

  **Reference files for this phase:**
  - Read `refs/build-request-template.md` for the BUILD_REQUEST format
  - The BUILD_REQUEST directs the builder to read `refs/agent-prompts.md`,
    `refs/synthesis-mapping.md`, and `refs/validation-checklists.md`
  ```
- [ ] No other phase in SKILL.md loads refs/ files (Stage A.1-A.6 use only SKILL.md content; Stage B delegates to /task which reads the task file, not SKILL.md)
- [ ] The orchestrator context loads at most 2 refs simultaneously (SKILL.md + build-request-template.md); the builder subagent loads the remaining 3 refs in its own context window

**Dependencies**: FR-PRD-R.1

### FR-PRD-R.7: Fidelity Verification — Zero Content Loss

**Description**: Every line of instructional content from the original 1,373-line SKILL.md appears either in the refactored SKILL.md or in one of the 4 refs/ files. Zero content dropped, zero semantic drift, zero paraphrasing.

**Acceptance Criteria**:
- [ ] The fidelity index at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` maps every content block with line ranges and destination files
- [ ] `diff` of each agent prompt template (8 templates) between original and `refs/agent-prompts.md` shows zero content changes
- [ ] `diff` of each checklist/table between original and `refs/validation-checklists.md` shows zero content changes
- [ ] `diff` of output structure and synthesis mapping table between original and `refs/synthesis-mapping.md` shows zero content changes
- [ ] `diff` of BUILD_REQUEST between original and `refs/build-request-template.md` shows only the documented SKILL CONTEXT FILE reference path changes
- [ ] All behavioral content in the refactored SKILL.md matches the original line-for-line (except removal of moved blocks and addition of loading declarations)
- [ ] Combined line count of SKILL.md + all refs/ files is between 1,370 and 1,400 lines (original 1,373 plus ref file headers ~12-20 lines, minus deduplicated B30 rows absorbed into B05)

**Dependencies**: FR-PRD-R.1 through FR-PRD-R.6

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `.claude/skills/prd/refs/agent-prompts.md` | All 8 agent prompt templates for the PRD pipeline (Codebase Research, Web Research, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly) | None |
| `.claude/skills/prd/refs/build-request-template.md` | Complete BUILD_REQUEST format for spawning the rf-task-builder subagent, including phase-to-template mapping, granularity requirements, escalation rules, and builder steps | refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md (referenced within) |
| `.claude/skills/prd/refs/synthesis-mapping.md` | PRD output structure reference (section outline) and synthesis file-to-template-section mapping table | None |
| `.claude/skills/prd/refs/validation-checklists.md` | Synthesis Quality Review (9 items), Assembly Process (Steps 8-11), Validation Checklist (18+4 items), Content Rules table (10 rules) | None |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `.claude/skills/prd/SKILL.md` | Reduced from 1,373 to ~430-480 lines. Agent prompts, BUILD_REQUEST, synthesis mapping, output structure, validation checklists, assembly process, and content rules moved to refs/. Loading declarations added at A.7. Duplicate Artifact Locations table (B30) merged with Output Locations (B05). | Comply with 500-line SKILL.md guidance; enable per-phase lazy loading |

### 4.3 Removed Files

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| No files removed | Content moves to refs/, nothing is deleted | All content preserved in new locations |

### 4.4 Module Dependency Graph

```
SKILL.md (behavioral protocol)
  |
  +-- [Stage A.7] --> refs/build-request-template.md
  |                     |
  |                     +-- references --> refs/agent-prompts.md
  |                     +-- references --> refs/synthesis-mapping.md
  |                     +-- references --> refs/validation-checklists.md
  |
  +-- [Stage B] --> /task skill (reads task file, NOT SKILL.md or refs/)
```

### 4.6 Implementation Order

```
1. Create refs/ directory                           -- prerequisite for all refs files
2. Create refs/agent-prompts.md                     -- copy lines 553-967 verbatim (except header text)
   Create refs/synthesis-mapping.md                 -- [parallel with step 2] copy lines 969-1106 verbatim
   Create refs/validation-checklists.md             -- [parallel with step 2] copy lines 1108-1254 verbatim
3. Create refs/build-request-template.md            -- depends on step 2 (needs to know refs/ paths for cross-reference updates)
4. Refactor SKILL.md                                -- depends on 2, 3 (remove moved blocks, add loading declarations, merge duplicate artifact table)
5. Fidelity verification                            -- depends on 4 (diff every block against original)
6. make sync-dev                                    -- depends on 5 (propagate to src/superclaude/skills/prd/)
```

## 5. Interface Contracts

### 5.3 Phase Contracts

The refactored skill's external interface is unchanged. Internally, the phase-to-refs loading contract is:

```yaml
phase_contracts:
  invocation:
    loads: [SKILL.md]
    tokens: ~2000
    
  stage_a_1_through_a_6:
    loads: []  # No refs needed — behavioral protocol in SKILL.md
    additional_tokens: 0
    
  stage_a_7_build_task_file:
    loads:
      - refs/build-request-template.md  # ~165 lines, ~700 tokens
      - refs/agent-prompts.md           # ~415 lines, ~1500 tokens (loaded by builder subagent)
      - refs/synthesis-mapping.md       # ~137 lines, ~500 tokens (loaded by builder subagent)
      - refs/validation-checklists.md   # ~127 lines, ~500 tokens (loaded by builder subagent)
    note: "Orchestrator loads build-request-template.md to construct the builder prompt. Builder subagent loads the other 3 refs in its own context window."
    max_concurrent_in_orchestrator: 2  # build-request-template + SKILL.md
    
  stage_a_8_verify:
    loads: []  # Reads task file output, no refs needed
    
  stage_b_delegation:
    loads: []  # /task reads the task file, not SKILL.md or refs/
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-PRD-R.1 | SKILL.md token budget | <= 2,000 tokens on invocation | Estimate from line count: 430-480 lines at ~4.5 tokens/line = ~1,935-2,160 tokens |
| NFR-PRD-R.2 | Per-phase token overhead | Max 2 refs loaded by orchestrator at any point | Count refs loaded per phase in the loading declarations |
| NFR-PRD-R.3 | Session start cost | ~50 tokens (name + description only) | Unchanged from current — frontmatter stays the same |
| NFR-PRD-R.4 | Zero behavioral regression | Identical execution behavior before and after refactoring | End-to-end test: invoke skill on a test product and compare output structure |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Content loss during decomposition — agent prompt word or line dropped | Low | High | Word-for-word fidelity audit using diff against original line ranges. Fidelity index provides first/last 10-word markers for each block. |
| Cross-reference breakage — BUILD_REQUEST still says "read the Agent Prompt Templates section" instead of refs/ path | Medium | High | Explicit cross-reference map in fidelity index lists every reference that must change. Grep for "section" references in the BUILD_REQUEST after refactoring. |
| Loading order wrong — refs loaded at wrong phase or not loaded at all | Low | Medium | Phase-to-ref dependency matrix in Section 5.3. Only one phase (A.7) loads refs. Simple to verify. |
| Builder subagent can't find refs/ files | Low | Medium | Builder is spawned from the SKILL.md directory. Refs/ paths are relative to the skill directory. Test by spawning builder and verifying it can read all 4 refs/ files. |
| Duplicate Artifact Locations table (B30) merged incorrectly | Low | Low | B30 is a near-duplicate of B05. Merge by keeping B05 (the primary table at lines 95-126) and adding any unique entries from B30 (lines 1327-1347). The additional entries in B30 are the analyst/QA report paths — these should be appended to B05's table. |
| refs/ file missing or renamed after refactoring | Low | Medium | Builder fails explicitly with file-not-found. Rollback: revert to monolithic SKILL.md from git history. Failure is obvious and self-diagnosing. |
| Spec freshness — SKILL.md modified between spec creation and implementation | Low | Medium | Implement this refactoring before any content changes to the PRD skill. All line ranges in the fidelity index are pinned to the current version. If SKILL.md changes, re-verify fidelity index line ranges before implementing. |

## 8. Test Plan

### 8.1 Fidelity Tests

| Test | Validates |
|------|-----------|
| Diff each of 8 agent prompts against original SKILL.md lines | Zero content change in refs/agent-prompts.md |
| Diff synthesis mapping table against original lines 1087-1106 | Zero content change in refs/synthesis-mapping.md |
| Diff output structure against original lines 969-1085 | Zero content change in refs/synthesis-mapping.md |
| Diff synthesis quality review against original lines 1108-1128 | Zero content change in refs/validation-checklists.md |
| Diff assembly process against original lines 1130-1193 | Zero content change in refs/validation-checklists.md |
| Diff validation checklist against original lines 1195-1235 | Zero content change in refs/validation-checklists.md |
| Diff content rules against original lines 1237-1254 | Zero content change in refs/validation-checklists.md |
| Diff BUILD_REQUEST against original lines 347-508 | Only documented SKILL CONTEXT FILE path changes |

### 8.2 Structural Tests

| Test | Validates |
|------|-----------|
| `wc -l SKILL.md` returns 430-500 | SKILL.md under 500-line ceiling |
| `ls refs/` returns exactly 4 files | Correct number of refs/ files created |
| `wc -l refs/agent-prompts.md` returns ~415 | Agent prompts file has expected content |
| `wc -l refs/build-request-template.md` returns ~165 | BUILD_REQUEST file has expected content |
| `wc -l refs/synthesis-mapping.md` returns ~137 | Synthesis mapping file has expected content |
| `wc -l refs/validation-checklists.md` returns ~127 | Validation checklists file has expected content |
| Combined line count of all 5 files is between 1,370 and 1,400 | No content lost or duplicated |
| `grep -c 'Agent Prompt' SKILL.md` returns 0 or 1 (only loading declaration reference) | Agent prompts removed from SKILL.md, not just duplicated into refs/ |
| `grep -c 'Assembly Process' SKILL.md` returns 0 | Assembly process removed from SKILL.md |
| `grep -c 'Content Rules' SKILL.md` returns 0 | Content rules removed from SKILL.md |
| `grep -c 'Validation Checklist' SKILL.md` returns 0 or 1 (only loading declaration reference) | Validation checklist removed from SKILL.md |

### 8.3 Cross-Reference Tests

| Test | Validates |
|------|-----------|
| `grep -c 'Agent Prompt Templates section' SKILL.md` returns 0 | No stale section references in SKILL.md |
| `grep -c 'Synthesis Mapping Table section' SKILL.md` returns 0 | No stale section references in SKILL.md |
| `grep -c 'Assembly Process section' SKILL.md` returns 0 | No stale section references in SKILL.md |
| `grep -c 'Validation Checklist section' SKILL.md` returns 0 | No stale section references in SKILL.md |
| `grep -c 'Content Rules section' SKILL.md` returns 0 | No stale section references in SKILL.md |
| `grep 'refs/' SKILL.md` shows loading declarations at A.7 | Loading declarations present |
| `grep 'refs/agent-prompts.md' refs/build-request-template.md` returns match | BUILD_REQUEST references updated to refs/ paths |
| `grep -c '".*section"' refs/build-request-template.md` returns 0 (or only "Tier Selection" which stays in SKILL.md) | No stale prose "section" references surviving in BUILD_REQUEST |
| `grep -c 'Agent Prompt Templates section' refs/build-request-template.md` returns 0 | BUILD_REQUEST doesn't reference removed SKILL.md sections |

### 8.4 Functional Test (Manual / E2E)

| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| Invoke PRD skill on a test product | Run the PRD skill against a small codebase product | Stage A completes, task file created with all agent prompts baked in. Stage B completes with all task file checklist items checked and a PRD file written to the expected output location. Pass criterion: identical execution behavior to the monolithic version — content quality is out of scope for this refactoring test. |
| Verify builder reads refs/ files | During A.7, check that the builder subagent successfully reads all 4 refs/ files | Builder creates task file with correct embedded prompts |
| Verify no stale references | Grep task file output for "section" references to SKILL.md | Zero matches — all references should be to refs/ file paths or baked-in content |

## 9. Migration & Rollout

- **Breaking changes**: None. The skill's external interface (command invocation, inputs, outputs) is completely unchanged. The internal decomposition is transparent to callers.
- **Backwards compatibility**: Full. The `/task` skill reads the task file (created during A.7), not SKILL.md. Agent prompts and validation criteria are baked into the task file during A.7, so downstream execution is unaffected by where the source content lives.
- **Rollback plan**: Revert the commit. The original monolithic SKILL.md is preserved in git history. Single `git revert <commit>` restores the previous state.
- **Migration steps**:
  1. Implement all changes in a single commit on the feature branch
  2. Run `make sync-dev` to propagate from `.claude/skills/prd/` to `src/superclaude/skills/prd/` (or vice versa depending on edit location)
  3. Run `make verify-sync` to confirm both locations match
  4. Run fidelity tests (Section 8.1) to verify zero content loss
  5. Run structural tests (Section 8.2) to verify line counts
  6. Merge to integration branch for testing

## 10. Downstream Inputs

### For sc:roadmap
This is a self-contained refactoring with no downstream roadmap impact. The PRD skill's capabilities and interface remain identical.

### For sc:tasklist
Single task: "Decompose prd/SKILL.md into SKILL.md + 4 refs/ files following the fidelity index at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`." Estimated effort: 1-2 hours. Can be completed in a single session.

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| None | All questions resolved during analysis | N/A | N/A |

## 12. Gap Analysis

### 12.1 Content Block Inventory

The complete content block inventory with 32 blocks (B01-B32) is documented in the fidelity index at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`. Summary:

| Category | Blocks | Total Lines | Destination |
|----------|--------|-------------|-------------|
| Behavioral (WHAT/WHEN) | B01-B10, B12-B13, B28-B32 | ~530 | SKILL.md (after removing moved content and adding loading declarations: ~430-480 lines) |
| Agent Prompts (HOW) | B14-B21 | ~415 | refs/agent-prompts.md |
| BUILD_REQUEST (HOW) | B11 | ~165 | refs/build-request-template.md |
| Output Structure + Mapping (HOW) | B22-B23 | ~137 | refs/synthesis-mapping.md |
| Checklists + Process + Rules (HOW) | B24-B27 | ~127 | refs/validation-checklists.md |
| **Total** | **32 blocks** | **~1,374** | **5 files** |

### 12.2 Cross-Reference Update Map

The BUILD_REQUEST (block B11, lines 344-508) contains a SKILL CONTEXT FILE section that tells the builder where to find reference content. These references must be updated:

| Original Reference (line ~412) | Updated Reference |
|--------------------------------|-------------------|
| `Read the "Agent Prompt Templates" section` | `Read refs/agent-prompts.md` |
| `Read the "Synthesis Mapping Table" section for the standard synth-file-to-PRD-section mapping` | `Read refs/synthesis-mapping.md for the standard synth-file-to-PRD-section mapping` |
| `Read the "Synthesis Quality Review Checklist" section for post-synthesis verification` | `Read refs/validation-checklists.md for post-synthesis verification` |
| `Read the "Assembly Process" section for PRD assembly steps` | `Read refs/validation-checklists.md for PRD assembly steps (Assembly Process section)` |
| `Read the "Validation Checklist" section for Phase 6 validation criteria` | `Read refs/validation-checklists.md for Phase 6 validation criteria (Validation Checklist section)` |
| `Read the "Content Rules" section for writing standards` | `Read refs/validation-checklists.md for writing standards (Content Rules section)` |
| `Read the "Tier Selection" section for depth tier line budgets and agent counts` | No change — Tier Selection stays in SKILL.md |

Additionally, in Phase 2 task file items (line ~454): `full codebase research agent prompt from SKILL.md` becomes `full codebase research agent prompt from refs/agent-prompts.md`. Same pattern for all phase references to agent prompts and validation content.

**Note on B13 (Stage B, line ~550)**: The reference to `refs/agent-prompts.md` and `refs/validation-checklists.md` in Stage B is **informational only** — Stage B does not load refs/ files. This text explains what content was baked into the task file during A.7, not an instruction for the agent to load refs/ at that point.

### 12.3 Fidelity Manifest

The fidelity manifest is the complete fidelity index document at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`. It provides:
- Every content block with exact line ranges
- Destination file for each block
- First/last 10-word verification markers
- Cross-reference map showing every reference that must be updated
- Verification protocol for post-implementation auditing

### 12.4 Gaps Found During Analysis

| Gap ID | Description | Severity | Affected Section | Resolution |
|--------|-------------|----------|-----------------|------------|
| GAP-01 | Duplicate Artifact Locations table (B30, lines 1327-1347) is a near-copy of Output Locations (B05, lines 95-126) with additional QA report paths | Low | Section 4.2 (Modified Files) | **Merge strategy: Append (Option A).** Keep B05's generalized pattern rows intact (`qa/analyst-report-[gate].md`, `qa/qa-report-[gate].md`). Append B30's 6 specific QA paths as additional rows below (analyst-completeness-report, analyst-synthesis-review, qa-research-gate-report, qa-synthesis-gate-report, qa-report-validation, qa-qualitative-review). Add a note row: "Specific QA paths listed below; generalized patterns above." Also preserve B05's naming convention `[NN]-[topic-name].md` — B30's variant `[NN]-[topic].md` is a cosmetic inconsistency in the original that should NOT be resolved during this refactoring (content preservation). Remove the standalone B30 section. |
| GAP-02 | The BUILD_REQUEST SKILL CONTEXT FILE block (line ~411-412) references sections by prose name ("the Agent Prompt Templates section") rather than file path | Medium | Section 3 (FR-PRD-R.5) | Update all section name references to refs/ file paths as documented in the cross-reference map (Section 12.2) |

No other gaps found. All 1,373 lines of the original are accounted for in the fidelity index.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| SKILL.md | The main manifest file for a SuperClaude skill, containing behavioral protocol (WHAT/WHEN) |
| refs/ | Directory within a skill containing reference material (HOW content) loaded on demand per phase |
| BUILD_REQUEST | The structured prompt format passed to the rf-task-builder subagent to create an MDTM task file |
| MDTM | Markdown-Driven Task Management — the task file format used for persistent progress tracking |
| rf-task-builder | The subagent that creates MDTM task files from BUILD_REQUEST prompts |
| Lazy loading | Loading refs/ files only when needed for a specific phase, not pre-loading all at invocation |
| Fidelity index | A document mapping every content block from source to destination with verification markers |
| B2 pattern | Self-contained checklist items in MDTM task files — each item is a complete prompt |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `.claude/skills/prd/SKILL.md` | Original monolithic file being refactored (source of truth for content) |
| `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Defines the skill architecture best practices (Sections 5, 6, 9) that this refactoring implements |
| `.claude/skills/sc-adversarial-protocol/SKILL.md` | Gold-standard reference implementation of a decomposed skill with refs/ |
| `.claude/skills/sc-adversarial-protocol/refs/` | Example refs/ files showing the pattern (agent-specs.md, artifact-templates.md, debate-protocol.md, scoring-protocol.md) |
| `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` | Content block inventory and cross-reference map for this refactoring |
| `src/superclaude/examples/release-spec-template.md` | Template used to create this spec |
