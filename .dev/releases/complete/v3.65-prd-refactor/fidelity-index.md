# PRD Skill Refactoring — Fidelity Index

> **Purpose**: Maps every content block from the original `.claude/skills/prd/SKILL.md` (1,373 lines) to its destination in the refactored structure.
> Each entry includes: line range, block type, destination file, execution phase dependency, and first/last 10-word markers for verification.
>
> **Original file**: `.claude/skills/prd/SKILL.md` (1,373 lines)
> **Generated**: 2026-04-02

---

## Legend

| Column | Meaning |
|--------|---------|
| **Block ID** | Sequential identifier for cross-referencing |
| **Lines** | Start-end line range in original SKILL.md |
| **Type** | `behavioral` (WHAT/WHEN) = stays in SKILL.md; `reference` (HOW) = moves to refs/ |
| **Phase** | Which execution phase needs this content |
| **Destination** | File in the refactored structure |
| **First 10 Words** | First ~10 words of the block content (verification marker) |
| **Last 10 Words** | Last ~10 words of the block content (verification marker) |

---

## Content Block Inventory

### B01: Frontmatter
| Field | Value |
|-------|-------|
| Lines | 1–4 |
| Type | behavioral |
| Phase | Invocation |
| Destination | `SKILL.md` (frontmatter) |
| First 10 | `name: prd description: "Create or populate a Product Requirements` |
| Last 10 | `or when the user says 'define the product' in` |

### B02: Skill Header + Process Description
| Field | Value |
|-------|-------|
| Lines | 6–30 |
| Type | behavioral |
| Phase | Invocation |
| Destination | `SKILL.md` (header section) |
| First 10 | `# PRD Creator A skill for creating comprehensive Product` |
| Last 10 | `findings survive context compression, can be re-verified later, and feed` |

### B03: Input Section
| Field | Value |
|-------|-------|
| Lines | 32–73 |
| Type | behavioral |
| Phase | Invocation / Stage A |
| Destination | `SKILL.md` (Input section) |
| First 10 | `## Input The skill needs four pieces of information` |
| Last 10 | `Proceed once you have at least #1 answered clearly. Items` |

### B04: Tier Selection
| Field | Value |
|-------|-------|
| Lines | 75–93 |
| Type | behavioral |
| Phase | Stage A (A.3/A.6) |
| Destination | `SKILL.md` (Tier Selection section — brief, needed at invocation) |
| First 10 | `## Tier Selection Match the tier to product scope.` |
| Last 10 | `architectural layers, or integration boundaries — always Heavyweight` |

### B05: Output Locations
| Field | Value |
|-------|-------|
| Lines | 95–126 |
| Type | behavioral |
| Phase | Stage A (A.3) |
| Destination | `SKILL.md` (Output Locations section) |
| First 10 | `## Output Locations All persistent artifacts go into the` |
| Last 10 | `prior research exists on the same product, read it first` |

### B06: Execution Overview
| Field | Value |
|-------|-------|
| Lines | 128–157 |
| Type | behavioral |
| Phase | Stage A / Stage B |
| Destination | `SKILL.md` (Execution Overview section) |
| First 10 | `## Execution Overview The skill operates in two stages:` |
| Last 10 | `resume from the first unchecked item.` |

### B07: Stage A — A.1 through A.3
| Field | Value |
|-------|-------|
| Lines | 159–255 |
| Type | behavioral |
| Phase | Stage A |
| Destination | `SKILL.md` (Stage A: Scope Discovery protocol) |
| First 10 | `## Stage A: Scope Discovery & Task File Creation` |
| Last 10 | `those notes as input for A.4.` |

### B08: Stage A — A.4 Research Notes File
| Field | Value |
|-------|-------|
| Lines | 257–299 |
| Type | behavioral |
| Phase | Stage A |
| Destination | `SKILL.md` (Stage A: A.4 section) |
| First 10 | `### A.4: Write Research Notes File (MANDATORY) Write the` |
| Last 10 | `"None — intent is clear from the request and codebase context."` |

### B09: Stage A — A.5 Research Sufficiency Gate
| Field | Value |
|-------|-------|
| Lines | 301–324 |
| Type | behavioral |
| Phase | Stage A |
| Destination | `SKILL.md` (Stage A: A.5 section) |
| First 10 | `### A.5: Review Research Sufficiency (MANDATORY GATE) You MUST` |
| Last 10 | `relies on what you provide.` |

### B10: Stage A — A.6 Template Triage
| Field | Value |
|-------|-------|
| Lines | 326–342 |
| Type | behavioral |
| Phase | Stage A |
| Destination | `SKILL.md` (Stage A: A.6 section) |
| First 10 | `### A.6: Template Triage Determine which MDTM template the` |
| Last 10 | `synthesis, quality gates, and assembly.` |

### B11: Stage A — A.7 BUILD_REQUEST Format
| Field | Value |
|-------|-------|
| Lines | 344–508 |
| Type | reference (HOW — agent prompt / template) |
| Phase | Stage A (A.7) |
| Destination | `refs/build-request-template.md` |
| First 10 | `### A.7: Build the Task File Spawn the rf-task-builder` |
| Last 10 | `7. Return the task file path` |

### B12: Stage A — A.7 Builder Spawning + A.8 Verification
| Field | Value |
|-------|-------|
| Lines | 510–527 |
| Type | behavioral |
| Phase | Stage A |
| Destination | `SKILL.md` (Stage A: A.7 spawning + A.8 verification) |
| First 10 | `**Spawning the builder:** Use the Agent tool with subagent_type:` |
| Last 10 | `re-run the builder with specific corrections. Otherwise, proceed to Stage B.` |

### B13: Stage B — Task File Execution + Delegation Protocol
| Field | Value |
|-------|-------|
| Lines | 529–551 |
| Type | behavioral |
| Phase | Stage B |
| Destination | `SKILL.md` (Stage B section) |
| First 10 | `## Stage B: Task File Execution Stage B delegates execution` |
| Last 10 | `do not modify it; do not fabricate product capabilities;` |

### B14: Codebase Research Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 553–637 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 2 (Deep Investigation) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `## Agent Prompt Templates These templates are provided to` |
| Last 10 | `Only reading the actual source code of X verifies X exists.` |

### B15: Web Research Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 639–686 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 4 (Web Research) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `### Web Research Agent Prompt Research this topic externally` |
| Last 10 | `Pricing models and monetization patterns in the space` |

### B16: Synthesis Agent Prompt
| Field | Value |
|-------|-------|
| Lines | 688–720 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 5 (Synthesis) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `### Synthesis Agent Prompt Read the research files listed` |
| Last 10 | `including all table structures and headers from the template.` |

### B17: Research Analyst Agent Prompt (rf-analyst)
| Field | Value |
|-------|-------|
| Lines | 722–759 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 3 (Completeness Verification) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)` |
| Last 10 | `your job is to find problems, not confirm things work.` |

### B18: Research QA Agent Prompt (rf-qa — Research Gate)
| Field | Value |
|-------|-------|
| Lines | 761–804 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 3 (Research Gate) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `### Research QA Agent Prompt (rf-qa — Research Gate)` |
| Last 10 | `Zero tolerance — if you can't verify it, it fails.` |

### B19: Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)
| Field | Value |
|-------|-------|
| Lines | 806–846 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 5 (Synthesis Gate) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)` |
| Last 10 | `FAIL: Issues found (list with specific fixes, note which` |

### B20: Report Validation QA Agent Prompt (rf-qa — Report Validation)
| Field | Value |
|-------|-------|
| Lines | 848–895 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 6 (Report Validation) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `### Report Validation QA Agent Prompt (rf-qa — Report` |
| Last 10 | `Fix every issue you find. Report honestly.` |

### B21: Assembly Agent Prompt (rf-assembler)
| Field | Value |
|-------|-------|
| Lines | 897–967 |
| Type | reference (HOW — agent prompt) |
| Phase | Phase 6 (Assembly) |
| Destination | `refs/agent-prompts.md` |
| First 10 | `### Assembly Agent Prompt (rf-assembler — PRD Assembly) Assemble` |
| Last 10 | `After assembly, the source docs should be candidates for archival` |

### B22: Output Structure
| Field | Value |
|-------|-------|
| Lines | 969–1085 |
| Type | reference (HOW — template structure) |
| Phase | Phase 5/6 (Synthesis + Assembly) |
| Destination | `refs/synthesis-mapping.md` |
| First 10 | `## Output Structure Note: This section is reference documentation.` |
| Last 10 | `Appendices. Document Approval. Approval signature table.` |

### B23: Synthesis Mapping Table
| Field | Value |
|-------|-------|
| Lines | 1087–1106 |
| Type | reference (HOW — mapping table) |
| Phase | Phase 5 (Synthesis) |
| Destination | `refs/synthesis-mapping.md` |
| First 10 | `## Synthesis Mapping Table (Reference) Note: This section is` |
| Last 10 | `existing docs, all research files, gaps log` |

### B24: Synthesis Quality Review Checklist
| Field | Value |
|-------|-------|
| Lines | 1108–1128 |
| Type | reference (HOW — checklist) |
| Phase | Phase 5 (Synthesis QA Gate) |
| Destination | `refs/validation-checklists.md` |
| First 10 | `## Synthesis Quality Review Checklist Note: This section is` |
| Last 10 | `trigger re-synthesis of the affected files.` |

### B25: Assembly Process (Steps 8-11)
| Field | Value |
|-------|-------|
| Lines | 1130–1193 |
| Type | reference (HOW — process steps) |
| Phase | Phase 6 (Assembly) |
| Destination | `refs/validation-checklists.md` (Assembly Process subsection) |
| First 10 | `## Assembly Process ### Step 8: Assemble the PRD Read` |
| Last 10 | `Update any references to the archived files in other documents.` |

### B26: Validation Checklist (Structural + Content + Evidence + Format)
| Field | Value |
|-------|-------|
| Lines | 1195–1235 |
| Type | reference (HOW — checklist) |
| Phase | Phase 6 (Report Validation) |
| Destination | `refs/validation-checklists.md` |
| First 10 | `## Validation Checklist Note: This section is reference documentation.` |
| Last 10 | `Document Provenance appendix present if consolidating existing docs` |

### B27: Content Rules Table
| Field | Value |
|-------|-------|
| Lines | 1237–1254 |
| Type | reference (HOW — content rules) |
| Phase | Phase 5/6 (Synthesis + Assembly) |
| Destination | `refs/validation-checklists.md` (Content Rules subsection) |
| First 10 | `## Content Rules (From Template — Non-Negotiable) These rules` |
| Last 10 | `Vague "Q3" or "soon" dates without structure` |

### B28: Critical Rules
| Field | Value |
|-------|-------|
| Lines | 1256–1294 |
| Type | behavioral |
| Phase | All phases |
| Destination | `SKILL.md` (Critical Rules section) |
| First 10 | `## Critical Rules (Non-Negotiable) These are SKILL-SPECIFIC content` |
| Last 10 | `not executed during PRD creation.` |

### B29: Research Quality Signals
| Field | Value |
|-------|-------|
| Lines | 1296–1325 |
| Type | behavioral |
| Phase | Phase 2/3 (Investigation + Verification) |
| Destination | `SKILL.md` (Research Quality Signals section) |
| First 10 | `## Research Quality Signals ### Strong Investigation Signals Findings` |
| Last 10 | `rf-analyst or rf-qa identify coverage gaps requiring targeted investigation` |

### B30: Artifact Locations (duplicate table)
| Field | Value |
|-------|-------|
| Lines | 1327–1347 |
| Type | behavioral |
| Phase | All phases |
| Destination | `SKILL.md` — merge with B05 (Output Locations). This is a near-duplicate. |
| First 10 | `## Artifact Locations Artifact Location MDTM Task File .dev/tasks/to-do/` |
| Last 10 | `can be re-used when the document needs updating.` |

### B31: Session Management
| Field | Value |
|-------|-------|
| Lines | 1349–1359 |
| Type | behavioral |
| Phase | Session resume |
| Destination | `SKILL.md` (Session Management section) |
| First 10 | `## Session Management Session management is provided by the` |
| Last 10 | `the user likely needs to restart from Stage A (scope discovery).` |

### B32: Updating an Existing PRD
| Field | Value |
|-------|-------|
| Lines | 1361–1373 |
| Type | behavioral |
| Phase | Update flow |
| Destination | `SKILL.md` (Updating an Existing PRD section) |
| First 10 | `## Updating an Existing PRD When the user wants to` |
| Last 10 | `Update Document History with what changed` |

---

## Cross-Reference Map

These are locations in the original SKILL.md where one block references another, and how those references change in the refactored structure.

| Reference Location | Original Reference | New Reference (post-refactor) |
|--------------------|--------------------|-------------------------------|
| B11 (BUILD_REQUEST, line ~412) | `Read the "Agent Prompt Templates" section` | `Load refs/agent-prompts.md` |
| B11 (BUILD_REQUEST, line ~412) | `Read the "Synthesis Mapping Table" section` | `Load refs/synthesis-mapping.md` |
| B11 (BUILD_REQUEST, line ~412) | `Read the "Synthesis Quality Review Checklist" section` | `Load refs/validation-checklists.md` |
| B11 (BUILD_REQUEST, line ~412) | `Read the "Assembly Process" section` | `Load refs/validation-checklists.md` |
| B11 (BUILD_REQUEST, line ~412) | `Read the "Validation Checklist" section` | `Load refs/validation-checklists.md` |
| B11 (BUILD_REQUEST, line ~412) | `Read the "Content Rules" section` | `Load refs/validation-checklists.md` |
| B11 (BUILD_REQUEST, line ~412) | `Read the "Tier Selection" section` | Stays in SKILL.md (no ref change needed) |
| B11 (BUILD_REQUEST, line ~454) | `full codebase research agent prompt from SKILL.md` | `codebase research agent prompt from refs/agent-prompts.md` |
| B11 (BUILD_REQUEST, line ~478) | `synthesis agent prompt from SKILL.md` | `synthesis agent prompt from refs/agent-prompts.md` |
| B11 (BUILD_REQUEST, line ~483) | `Assembly Process steps from SKILL.md` | `Assembly Process steps from refs/validation-checklists.md` |
| B11 (BUILD_REQUEST, line ~484) | `Content Rules from SKILL.md` | `Content Rules from refs/validation-checklists.md` |
| B11 (BUILD_REQUEST, line ~484) | `Validation Checklist from SKILL.md` | `Validation Checklist from refs/validation-checklists.md` |
| B13 (Stage B, line ~550) | `agent prompts, validation criteria, and content rules` | `from refs/agent-prompts.md and refs/validation-checklists.md` |

---

## Destination File Summary

| Destination File | Source Blocks | Est. Lines | Content Description |
|------------------|---------------|------------|---------------------|
| `SKILL.md` (refactored) | B01-B10, B12-B13, B28-B32 | ~430-480 | Frontmatter, purpose, input, tier selection, output locations, execution overview, Stage A behavioral protocol (A.1-A.6, A.7 spawning, A.8 verify), Stage B delegation, critical rules, quality signals, session management, update flow |
| `refs/agent-prompts.md` | B14-B21 | ~415 | All 8 agent prompt templates: Codebase Research, Web Research, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly |
| `refs/build-request-template.md` | B11 | ~165 | Complete BUILD_REQUEST format including SKILL PHASES TO ENCODE, TEMPLATE 02 PATTERN MAPPING, GRANULARITY REQUIREMENT, ESCALATION, STEPS |
| `refs/synthesis-mapping.md` | B22, B23 | ~137 | Output Structure (PRD section reference) + Synthesis Mapping Table |
| `refs/validation-checklists.md` | B24, B25, B26, B27 | ~127 | Synthesis Quality Review (9 items), Assembly Process (Steps 8-11), Validation Checklist (18+4 items), Content Rules table |

**Total original lines**: 1,373
**Total mapped lines**: 1,373 (B01 line 1 through B32 line 1,373 — full coverage, zero gaps)

---

## Verification Protocol

To verify fidelity after implementation:

1. For each block in this index, extract the content from the destination file
2. Compare against the original SKILL.md at the specified line range
3. Verify the first-10 and last-10 word markers match
4. Confirm zero content was dropped, paraphrased, or rewritten
5. Confirm all cross-references in the BUILD_REQUEST were updated from "section in SKILL.md" to the correct "refs/ file path"
