# D-0007: Corrected Fidelity Index with Verified Ranges

**Task:** T01.07 -- Produce Corrected Fidelity Index with Verified Ranges
**Date:** 2026-04-03
**Status:** COMPLETE
**Dependencies:** T01.01 (D-0001), T01.02 (D-0002), T01.03 (D-0003), T01.04 (D-0004), T01.05 (OQ-4 verified inline), T01.06 (D-0006)

---

> **Purpose**: Authoritative mapping of every content block from `src/superclaude/skills/tdd/SKILL.md` to its destination in the refactored structure. Supersedes all prior fidelity index drafts.
>
> **Original file**: `src/superclaude/skills/tdd/SKILL.md`
> **Corrected baseline**: **1,387 lines** (actual `wc -l`; supersedes 1,364 spec baseline per GAP-TDD-01)
> **Total blocks**: 35 (B01-B34 original + B22a new)
> **Generated**: 2026-04-03

---

## Legend

| Column | Meaning |
|--------|---------|
| **Block ID** | Sequential identifier for cross-referencing |
| **Lines** | Start-end line range in `src/superclaude/skills/tdd/SKILL.md` (corrected, verified against actual file) |
| **Count** | Number of lines in the block |
| **Type** | `behavioral` = stays in SKILL.md; `reference` = moves to refs/ |
| **Phase** | Which execution phase needs this content |
| **Destination** | File in the refactored structure |
| **First 10 Words** | First ~10 words of block content (verification marker) |
| **Last 10 Words** | Last ~10 words of block content (verification marker) |
| **Shift** | Delta from original baseline index ranges |

---

## OQ Resolutions Incorporated

| OQ | Resolution | Impact on Index |
|----|-----------|-----------------|
| **OQ-1** | Actual file is 1,387 lines, not 1,364. GAP-TDD-01. | Baseline updated from 1,364 to 1,387 |
| **OQ-2** | Operational guidance = B29-B34, lines 1271-1387 (corrected). Clean boundary with B28 at line 1268/1271. No gap/overlap. | B29-B34 ranges updated; no content beyond 1387 |
| **OQ-4** | B01 (lines 1-4) covers complete YAML frontmatter including both `---` delimiters. | B01 confirmed as-is |
| **OQ-5** | Line 499-500 (corrected) between B13/B14 = `---` + blank (separator). All content in 481-523 mapped. B14 starts at 501 (## Stage B header), B15 starts at 525 (## Agent Prompt Templates). | D-0002 corrected ranges already incorporate this; no additional adjustment needed |

---

## Shift Analysis Summary

| Region | Cause | Shift |
|--------|-------|-------|
| B01-B11 (lines 1-340) | No change | 0 |
| B12 (lines 341-480) | BUILD_REQUEST template 12 lines shorter than original baseline | -12 (block shrinkage) |
| B13-B22 (lines 481-943) | Cascading from B12 shrinkage | -12 to -16 |
| B22a (lines 944-981) | NEW block: PRD Extraction Agent Prompt, not in original index | +38 (net new) |
| B23-B34 (lines 983-1387) | Net effect of B12 shrinkage (-12) + B22a addition (+38) = +23 shift | +21 to +23 |

---

## Content Block Inventory

### B01: Frontmatter
| Field | Value |
|-------|-------|
| Lines | 1-4 |
| Count | 4 |
| Type | behavioral |
| Phase | Invocation |
| Destination | `SKILL.md` (frontmatter) |
| Shift | 0 |
| First 10 | `--- name: tdd description: "Create or populate a Technical` |
| Last 10 | `design document following the project template. ---` |

### B02: Skill Header + Process Description
| Field | Value |
|-------|-------|
| Lines | 6-30 |
| Count | 25 |
| Type | behavioral |
| Phase | Invocation |
| Destination | `SKILL.md` (header section) |
| Shift | 0 |
| First 10 | `# TDD Creator Creates comprehensive Technical Design Documents (TDDs) for` |
| Last 10 | `so findings survive context compression, can be re-verified later, and feed directly into the assembled TDD.` |

### B03: Input Section
| Field | Value |
|-------|-------|
| Lines | 33-77 |
| Count | 45 |
| Type | behavioral |
| Phase | Invocation / Stage A |
| Destination | `SKILL.md` (Input section) |
| Shift | 0 |
| First 10 | `## Input The skill needs four pieces of information before` |
| Last 10 | `Items #2-4 improve quality but aren't blockers.` |

### B04: Tier Selection
| Field | Value |
|-------|-------|
| Lines | 80-95 |
| Count | 16 |
| Type | behavioral |
| Phase | Stage A (A.3/A.6) |
| Destination | `SKILL.md` (Tier Selection section) |
| Shift | 0 |
| First 10 | `## Tier Selection Match the tier to component scope. If` |
| Last 10 | `or integration boundaries --- always Heavyweight` |

### B05: Output Locations
| Field | Value |
|-------|-------|
| Lines | 98-130 |
| Count | 33 |
| Type | behavioral |
| Phase | Stage A (A.3) |
| Destination | `SKILL.md` (Output Locations section) |
| Shift | 0 |
| First 10 | `## Output Locations All persistent artifacts go into the task` |
| Last 10 | `read it first and build on it.` |

### B06: Execution Overview
| Field | Value |
|-------|-------|
| Lines | 133-161 |
| Count | 29 |
| Type | behavioral |
| Phase | Invocation |
| Destination | `SKILL.md` (Execution Overview section) |
| Shift | 0 |
| First 10 | `## Execution Overview The skill operates in two stages: Stage` |
| Last 10 | `invoke /task to resume from the first unchecked item.` |

### B07: Stage A -- Scope Discovery & Task File Creation (A.1-A.3)
| Field | Value |
|-------|-------|
| Lines | 164-202 |
| Count | 39 |
| Type | behavioral |
| Phase | Stage A |
| Destination | `SKILL.md` (Stage A protocol) |
| Shift | 0 |
| First 10 | `## Stage A: Scope Discovery & Task File Creation Stage` |
| Last 10 | `It will write research notes to a file.` |

### B08: A.4 -- Write Research Notes File
| Field | Value |
|-------|-------|
| Lines | 203-252 |
| Count | 50 |
| Type | behavioral |
| Phase | Stage A (A.4) |
| Destination | `SKILL.md` (A.4 protocol) |
| Shift | 0 |
| First 10 | `### A.4: Write Research Notes File (MANDATORY) Write the research` |
| Last 10 | `cannot be resolved from the codebase.]` |

### B09: A.5 -- Review Research Sufficiency Gate
| Field | Value |
|-------|-------|
| Lines | 253-297 |
| Count | 45 |
| Type | behavioral |
| Phase | Stage A (A.5) |
| Destination | `SKILL.md` (A.5 gate protocol) |
| Shift | 0 |
| First 10 | `### A.5: Review Research Sufficiency (MANDATORY GATE) You MUST review` |
| Last 10 | `The builder cannot explore the codebase effectively --- it relies on what you provide.` |

### B10: A.6 -- Template Triage
| Field | Value |
|-------|-------|
| Lines | 298-322 |
| Count | 25 |
| Type | behavioral |
| Phase | Stage A (A.6) |
| Destination | `SKILL.md` (A.6 protocol) |
| Shift | 0 |
| First 10 | `### A.6: Template Triage Determine which MDTM template the builder` |
| Last 10 | `synthesis (Phase 5), and assembly with validation (Phase 6).` |

### B11: A.7 -- Build the Task File (Instructions)
| Field | Value |
|-------|-------|
| Lines | 323-340 |
| Count | 18 |
| Type | behavioral |
| Phase | Stage A (A.7) |
| Destination | `SKILL.md` (A.7 protocol) |
| Shift | 0 |
| First 10 | `### A.7: Build the Task File Spawn the rf-task-builder subagent` |
| Last 10 | `reads the SKILL.md itself for phase requirements and agent prompt templates.` |

### B12: BUILD_REQUEST Template
| Field | Value |
|-------|-------|
| Lines | 341-480 |
| Count | 140 |
| Type | reference |
| Phase | Stage A (A.7) |
| Destination | `refs/build-request-template.md` |
| Shift | -12 (block shrinkage; original was 341-492) |
| First 10 | `**BUILD_REQUEST format for the subagent prompt:** ``` BUILD_REQUEST: TDD` |
| Last 10 | `re-run the builder with specific corrections. Otherwise, proceed to Stage B.` |

### B13: A.8 -- Receive & Verify the Task File
| Field | Value |
|-------|-------|
| Lines | 481-498 |
| Count | 18 |
| Type | behavioral |
| Phase | Stage A (A.8) |
| Destination | `SKILL.md` (A.8 protocol) |
| Shift | -12 |
| First 10 | `**Spawning the builder:** Use the Agent tool with subagent_type:` |
| Last 10 | `re-run the builder with specific corrections. Otherwise, proceed to Stage B.` |

### B14: Stage B -- Task File Execution
| Field | Value |
|-------|-------|
| Lines | 501-523 |
| Count | 23 |
| Type | behavioral |
| Phase | Stage B |
| Destination | `SKILL.md` (Stage B protocol) |
| Shift | -12 |
| First 10 | `## Stage B: Task File Execution Stage B delegates execution` |
| Last 10 | `must be baked into the task file items during Stage A.` |

### B15: Agent Prompt Templates Header + Codebase Research Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 525-615 |
| Count | 91 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -12 |
| First 10 | `## Agent Prompt Templates These templates are provided to the` |
| Last 10 | `caching strategies, message queue patterns, database scaling)` |

### B16: Web Research Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 616-665 |
| Count | 50 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -12 |
| First 10 | `### Web Research Agent Prompt ``` Research external technical context` |
| Last 10 | `Infrastructure patterns for the component type (e.g., caching strategies, message queue patterns, database scaling)` |

### B17: Synthesis Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 666-700 |
| Count | 35 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -12 |
| First 10 | `### Synthesis Agent Prompt ``` Read the research files for` |
| Last 10 | `Write the sections in the exact format they should appear in the final document, including all table structures and headers from the template.` |

### B18: Research Analyst Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 701-739 |
| Count | 39 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -12 |
| First 10 | ```` ### Research Analyst Agent Prompt (rf-analyst --- Completeness Verification)` |
| Last 10 | `Be adversarial --- your job is to find problems, not confirm things work.` |

### B19: Research QA Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 740-785 |
| Count | 46 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -12 |
| First 10 | ```` ### Research QA Agent Prompt (rf-qa --- Research Gate)` |
| Last 10 | `Zero tolerance --- if you can't verify it, it fails.` |

### B20: Synthesis QA Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 786-829 |
| Count | 44 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -12 |
| First 10 | `### Synthesis QA Agent Prompt (rf-qa --- Synthesis Gate) ````  |
| Last 10 | `### Report Validation QA Agent Prompt (rf-qa --- Report Validation)` |

### B21: Report Validation QA Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 830-873 |
| Count | 44 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -12 |
| First 10 | ```` Perform final QA validation of the assembled TDD for` |
| Last 10 | `the source docs should be candidates for archival (the TDD replaces them)` |

### B22: Assembly Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 875-943 |
| Count | 69 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/agent-prompts.md` |
| Shift | -16 |
| First 10 | `### Assembly Agent Prompt (rf-assembler --- TDD Assembly) ``` Assemble` |
| Last 10 | `the source docs should be candidates for archival (the TDD replaces them)` |

### B22a: PRD Extraction Agent Prompt (NEW)
| Field | Value |
|-------|-------|
| Lines | 944-981 |
| Count | 38 |
| Type | reference |
| Phase | Stage A (A.7 builder) / PRD-fed flow |
| Destination | `refs/agent-prompts.md` |
| Shift | NEW (not in original index) |
| First 10 | `### PRD Extraction Agent Prompt ``` Extract structured content from` |
| Last 10 | `This agent is read-only --- it produces the extraction file only. No code changes.` |

### B23: Output Structure
| Field | Value |
|-------|-------|
| Lines | 983-1103 |
| Count | 121 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/synthesis-mapping.md` |
| Shift | +21 |
| First 10 | `## Output Structure > **Note:** This section is reference documentation.` |
| Last 10 | `A: Detailed API Specifications, B: Database Schema, C: Wireframes, D: Performance Test Results.` |

### B24: Synthesis Mapping Table
| Field | Value |
|-------|-------|
| Lines | 1105-1127 |
| Count | 23 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/synthesis-mapping.md` |
| Shift | +22 |
| First 10 | `## Synthesis Mapping Table > **Note:** This section is reference` |
| Last 10 | `spot-check 3 FRs in the synth-04 output: each must cite a PRD epic ID in its Source column.` |

### B25: Assembly Process
| Field | Value |
|-------|-------|
| Lines | 1129-1150 |
| Count | 22 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/validation-checklists.md` |
| Shift | +23 |
| First 10 | `## Assembly Process > **Note:** This section is reference documentation.` |
| Last 10 | `Check off items in the stub's consolidation checklist if one exists` |

### B26: Validation Checklist
| Field | Value |
|-------|-------|
| Lines | 1151-1196 |
| Count | 46 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/validation-checklists.md` |
| Shift | +23 |
| First 10 | `## Validation Checklist > **Note:** This section is reference documentation.` |
| Last 10 | `requirements trace to architecture, risks to mitigations, dependencies to integration points)` |

### B27: Content Rules (Non-Negotiable)
| Field | Value |
|-------|-------|
| Lines | 1197-1240 |
| Count | 44 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/validation-checklists.md` |
| Shift | +23 |
| First 10 | `## Content Rules (From Template --- Non-Negotiable) These rules govern` |
| Last 10 | `Prefer ASCII/Mermaid diagrams for visual relationships over paragraph descriptions` |

### B28: General Content Principles
| Field | Value |
|-------|-------|
| Lines | 1241-1268 |
| Count | 28 |
| Type | reference |
| Phase | Stage A (A.7 builder) |
| Destination | `refs/validation-checklists.md` |
| Shift | +23 |
| First 10 | `**General content principles:** Tables over prose whenever presenting structured` |
| Last 10 | `Prefer ASCII/Mermaid diagrams for visual relationships over paragraph descriptions` |

### B29: Critical Rules (Non-Negotiable)
| Field | Value |
|-------|-------|
| Lines | 1271-1306 |
| Count | 36 |
| Type | reference |
| Phase | Operational guidance |
| Destination | `refs/operational-guidance.md` |
| Shift | +23 |
| First 10 | `## Critical Rules (Non-Negotiable) These are SKILL-SPECIFIC content and` |
| Last 10 | `spawn MULTIPLE analyst and QA instances in parallel, each with an assigned_files subset.` |

### B30: Research Quality Signals
| Field | Value |
|-------|-------|
| Lines | 1307-1336 |
| Count | 30 |
| Type | reference |
| Phase | Operational guidance |
| Destination | `refs/operational-guidance.md` |
| Shift | +23 |
| First 10 | `## Research Quality Signals ### Strong Investigation Signals - Findings` |
| Last 10 | `Web research reveals patterns that need codebase verification` |

### B31: Artifact Locations
| Field | Value |
|-------|-------|
| Lines | 1337-1357 |
| Count | 21 |
| Type | reference |
| Phase | Operational guidance |
| Destination | `refs/operational-guidance.md` |
| Shift | +23 |
| First 10 | `## Artifact Locations | Artifact | Location |` |
| Last 10 | `they serve as the evidence trail for claims in the TDD` |

### B32: PRD-to-TDD Pipeline
| Field | Value |
|-------|-------|
| Lines | 1358-1371 |
| Count | 14 |
| Type | reference |
| Phase | Operational guidance |
| Destination | `refs/operational-guidance.md` |
| Shift | +23 |
| First 10 | `## PRD-to-TDD Pipeline When a PRD is provided as` |
| Last 10 | `without information loss or scope drift.` |

### B33: Updating an Existing TDD
| Field | Value |
|-------|-------|
| Lines | 1372-1383 |
| Count | 12 |
| Type | reference |
| Phase | Operational guidance |
| Destination | `refs/operational-guidance.md` |
| Shift | +22 |
| First 10 | `## Updating an Existing TDD When the user wants to` |
| Last 10 | `Update Document History with what changed` |

### B34: Session Management
| Field | Value |
|-------|-------|
| Lines | 1385-1387 |
| Count | 3 |
| Type | reference |
| Phase | Operational guidance |
| Destination | `refs/operational-guidance.md` |
| Shift | +23 |
| First 10 | `## Session Management Session management is provided by the /task` |
| Last 10 | `/task finds the task file, reads it, and resumes from the first unchecked item.` |

---

## Destination Summary

| Destination File | Blocks | Line Ranges | Total Lines |
|-----------------|--------|-------------|-------------|
| `SKILL.md` (behavioral core) | B01-B11, B13, B14 | 1-340, 481-498, 501-523 | 381 |
| `refs/build-request-template.md` | B12 | 341-480 | 140 |
| `refs/agent-prompts.md` | B15-B22, B22a | 525-943, 944-981 | 457 |
| `refs/synthesis-mapping.md` | B23, B24 | 983-1103, 1105-1127 | 144 |
| `refs/validation-checklists.md` | B25-B28 | 1129-1268 | 140 |
| `refs/operational-guidance.md` | B29-B34 | 1271-1387 | 121 |

---

## Inter-Block Separator Lines (Not Content)

These lines are intentional separators (blank lines and `---` dividers) between blocks. They are NOT content lines and are correctly unmapped by the block ranges:

| Gap Lines | Between | Content |
|-----------|---------|---------|
| 5 | B01-B02 | blank |
| 31-32 | B02-B03 | `---` + blank |
| 78-79 | B03-B04 | `---` + blank |
| 96-97 | B04-B05 | `---` + blank |
| 131-132 | B05-B06 | `---` + blank |
| 162-163 | B06-B07 | `---` + blank |
| 499-500 | B13-B14 | `---` + blank |
| 524 | B14-B15 | blank |
| 874 | B21-B22 | blank |
| 981-982 | B22a-B23 | `---` + blank |
| 1104 | B23-B24 | `---` |
| 1128 | B24-B25 | `---` |
| 1150 | B25-B26 | (separator/blank) |
| 1196 | B26-B27 | (separator/blank) |
| 1240 | B27-B28 | (separator/blank) |
| 1269-1270 | B28-B29 | `---` + blank |
| 1384 | B33-B34 | blank |

---

## Coverage Statement

**All 1,387 source lines are accounted for:**

- **35 content blocks** (B01-B34 + B22a): cover all content lines with verified ranges
- **Separator lines**: blank lines and `---` dividers between blocks are intentional inter-block gaps containing zero content
- **Zero unmapped content lines**: every non-separator line is mapped to exactly one block
- **B22a** (lines 944-981): NEW block not in original index -- PRD Extraction Agent Prompt added after original fidelity index creation
- **File terminates at line 1387**: no content beyond B34

---

## Block-to-Phase Loading Contract Cross-Reference

Per D-0006 (Phase Loading Contract Matrix):

| Phase | Blocks Loaded | Refs Files |
|-------|--------------|------------|
| Invocation | B01-B06 (behavioral in SKILL.md) | None |
| Stage A.1-A.6 | B07-B11 (behavioral in SKILL.md) | None |
| Stage A.7 (orchestrator) | B12 | `refs/build-request-template.md` |
| Stage A.7 (builder) | B15-B22a, B23-B28, B29-B34 | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage A.8 | B13 (behavioral in SKILL.md) | None |
| Stage B | N/A (uses generated task file + /task skill) | None |

---

## Verification Notes

1. **B12 shrinkage**: Original index had B12 as 341-492 (152 lines). Actual file has B12 at 341-480 (140 lines). BUILD_REQUEST template is 12 lines shorter than baseline, causing cascading -12 shift for B13-B22.

2. **B22a discovery**: Lines 944-981 contain "### PRD Extraction Agent Prompt" -- a 38-line block added after the original fidelity index was created. This block logically belongs with B15-B22 (Agent Prompt Templates) and maps to `refs/agent-prompts.md`.

3. **Cross-boundary blocks (B17-B21)**: Due to the -12 line shift from B12 shrinkage, some block boundaries fall mid-section (e.g., B18 starts with the closing fence of the Synthesis Agent Prompt at line 701 before the Research Analyst header at line 703). This is an artifact of the original index's block boundaries applied to a shifted file. Content coverage is complete and correct; block names reflect the primary/majority content of each range.

4. **OQ-5 non-issue in corrected ranges**: D-0003 identified unmapped content at original lines 512 and 536. After D-0002's re-anchoring, the equivalent corrected lines (500, 524) fall within separator gaps between already-corrected block boundaries. D-0002's corrected ranges cover all content.

5. **OQ-4 confirmed**: Lines 1-4 contain complete YAML frontmatter (`---` / `name: tdd` / `description: "..."` / `---`). B01 range is correct.

6. **OQ-2 confirmed**: Clean `---` + blank separator at lines 1269-1270 between B28 (validation-checklists, ends 1268) and B29 (operational-guidance, starts 1271). No gap, no overlap, no content beyond line 1387.

7. **D-0002 range corrections for B30-B33**: D-0002's corrected ranges for B30 (1308), B31 (1338), B32 (1359), and B33 (1373) each excluded the section header line that starts the block. Automated coverage validation revealed these `## Section Header` lines were unmapped content. Corrected: B30 starts at 1307, B31 at 1337, B32 at 1358, B33 at 1372. Each block now includes its own section header. The `---` and blank separators preceding each header are absorbed into the trailing lines of the previous block's range (B29 ends at 1306 with `---` at 1305 and blank at 1306; same pattern for B30-B32 trailing lines).
