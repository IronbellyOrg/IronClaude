# PRD Skill Refactoring — Release Specification (v2)

```yaml
---
title: "Decompose monolithic PRD skill into three-tier architecture: Command → SKILL.md + refs/"
version: "2.0.0"
status: draft
feature_id: FR-PRD-REFACTOR
parent_feature: null
spec_type: refactoring
complexity_score: 0.45
complexity_class: MEDIUM
target_release: v3.8
authors: [user, claude]
created: 2026-04-03
supersedes: ".dev/releases/complete/v3.65-prd-refactor/prd-refactor-spec.md (v1.0.0)"
quality_scores:
  clarity: 9.5
  completeness: 9.5
  testability: 9.5
  consistency: 9.5
  overall: 9.5
---
```

## 1. Problem Statement

The PRD skill at `.claude/skills/prd/SKILL.md` has two architectural violations:

**Violation 1 — Monolithic SKILL.md (1,369 lines):** The file exceeds the 500-line SKILL.md ceiling (Developer Guide Section 9.3) by 2.7x. Agent prompt templates, validation checklists, synthesis mapping tables, assembly process instructions, and the BUILD_REQUEST template are embedded inline. When invoked, ~5,000+ tokens load into context regardless of which phase is executing.

**Violation 2 — Missing command layer:** The skill has no command file at `commands/sc/prd.md`. The Developer Guide mandates: "Every skill MUST have a command in front of it" (Three-Tier Architecture). Section 9.7 lists "Skill without command layer" as an anti-pattern: "Skill handles both interface and protocol concerns, creating a monolith; no standardized user-facing entry point." The Skill-Authoring Checklist (Section 5.10) lists "Thin command layer exists" as its first item.

The v1 spec (`.dev/releases/complete/v3.65-prd-refactor/prd-refactor-spec.md`) addressed Violation 1 only. This v2 spec addresses both violations and supersedes v1.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| SKILL.md is 1,369 lines — 2.7x the 500-line guidance | `.claude/skills/prd/SKILL.md` | ~5,000+ tokens loaded on every invocation regardless of phase |
| 8 agent prompt templates embedded inline (~415 lines total) | Lines 553-967 of SKILL.md | Loaded even when executing scope discovery (Stage A) which never uses them |
| Validation checklists, assembly process, content rules embedded inline (~147 lines) | Lines 1108-1254 of SKILL.md | Loaded during Stage A when only Stage B Phase 6 needs them |
| BUILD_REQUEST template embedded inline (~165 lines) | Lines 344-508 of SKILL.md | Only needed during A.7 but loaded for all phases |
| Output structure + synthesis mapping embedded inline (~137 lines) | Lines 969-1106 of SKILL.md | Only needed during Phase 5-6 but loaded for all phases |
| No command file exists | `ls .claude/commands/sc/prd*` returns empty | Users invoke skill directly — no standardized entry point with flags, examples, or boundaries |
| Developer Guide Section 9.7 anti-pattern: "Monolithic SKILL.md" | Developer Guide line ~1155 | Explicit anti-pattern with solution "Split into SKILL.md + refs/" |
| Developer Guide Section 9.7 anti-pattern: "Skill without command layer" | Developer Guide line ~1155 | Explicit anti-pattern with solution "Create a thin command file" |
| Skill-Authoring Checklist first item: "Thin command layer exists" | Developer Guide Section 5.10 | Mandatory checklist item for every skill |
| sc-adversarial-protocol demonstrates the correct three-tier pattern | `.claude/commands/sc/adversarial.md` (167 lines) + `.claude/skills/sc-adversarial-protocol/SKILL.md` + 4 refs/ | Reference implementation: thin command → skill → refs/ |
| 3 of 4 refs/ files already created but SKILL.md not trimmed | `.claude/skills/prd/refs/` | Content duplicated across SKILL.md and refs/ — partial implementation of v1 spec |

### 1.2 Scope Boundary

**In scope**:
- Creating `commands/sc/prd.md` (~130-150 lines) as the thin command layer
- Decomposing the PRD SKILL.md into SKILL.md (~420-450 lines) + 4 refs/ files
- Migrating interface content (prompt examples, tier table) from SKILL.md to command file
- Creating `refs/build-request-template.md` (the one ref not yet extracted)
- Trimming SKILL.md to remove content already in refs/ and content moving to command
- Updating internal cross-references (BUILD_REQUEST section references become refs/ paths)
- Adding explicit per-phase loading declarations in SKILL.md
- Verifying existing refs/ files match original SKILL.md content
- `make sync-dev` + `make verify-sync` for both skills/ and commands/

**Out of scope**:
- Modifying the PRD skill's pipeline logic, phase structure, or execution behavior
- Changing agent prompt content, validation criteria, or content rules
- Adding new features or capabilities to the PRD skill
- Renaming the skill directory (stays as `prd/`, not `sc-prd-protocol/`)
- Modifying any files outside `prd/` skill directory and `commands/sc/prd.md`

## 2. Solution Overview

Refactor the monolithic `prd/SKILL.md` (1,369 lines) into a three-tier architecture following the `sc-adversarial` pattern:

```
.claude/commands/sc/prd.md              (~130-150 lines — thin command layer)
.claude/skills/prd/
  SKILL.md                              (~420-450 lines — behavioral protocol only)
  refs/
    agent-prompts.md                    (~415 lines — all 8 agent prompt templates) [EXISTS]
    build-request-template.md           (~165 lines — BUILD_REQUEST format) [NEW]
    synthesis-mapping.md                (~137 lines — output structure + mapping) [EXISTS]
    validation-checklists.md            (~127 lines — checklists + assembly + rules) [EXISTS]
```

The command file provides the user-facing interface (flags, usage, examples, boundaries) and hands off to the skill via the Activation pattern. The SKILL.md retains all behavioral protocol (WHAT/WHEN). The refs/ files contain all HOW content loaded per-wave.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Create command file | YES — `commands/sc/prd.md` | Skip command (v1 approach) | Developer Guide mandates command layer for every skill. Without it, the skill handles both interface and protocol concerns. |
| Command style | Standard (~130-150 lines) with explicit flags | Minimal (~100 lines, no flags); Heavy (~180+ lines, inline tables) | Standard matches the adversarial gold standard. Explicit flags (`--tier`, `--resume`, `--output`, `--scope`, `--focus`, `--purpose`) formalize implicit parameters currently buried in SKILL.md Input section. |
| Content migration to command | Move prompt examples + tier table | Move entire Input section; Move nothing | Prompt examples are usage examples (command territory). Tier table documents the `--tier` flag. Input parsing logic and tier selection rules stay in skill (behavioral protocol). |
| Directory rename | NO — keep `prd/` | `sc-prd-protocol/`, `sc-prd/`, `prd-protocol/` | PRD is a dual-purpose utility (invocable by users AND by other skills). The `sc-` prefix convention is for protocol-only skills backing a single command. Renaming adds overhead for zero functional benefit. |
| Number of refs/ files | 4 files (unchanged from v1) | 8 files (per-agent), 2 files (prompts + everything else) | 4 files groups content by usage phase. Agent prompts load together at A.7. Validation content loads together at A.7 (by builder). |
| BUILD_REQUEST as separate ref | Dedicated `refs/build-request-template.md` | Keep in SKILL.md, merge with agent-prompts | BUILD_REQUEST is ~165 lines of template content only needed during A.7. Keeping it inline would push SKILL.md over the 500-line ceiling. |
| Behavioral blocks in SKILL.md | Critical Rules, Quality Signals, Session Mgmt stay | Move to refs/ | These are WHAT/WHEN content applying across ALL phases — must be available on invocation. Moving to refs/ would require loading at every phase. |

### 2.2 Workflow / Data Flow

```
User invokes /sc:prd <product> [flags]
  |
  v
commands/sc/prd.md loaded (~130-150 lines)
  Parses flags, shows usage/examples/boundaries
  |
  v [Activation: Skill prd]
skills/prd/SKILL.md loaded (~420-450 lines, ~2000 tokens)
  Contains: purpose, input parsing, tier selection rules,
            output locations, execution overview, Stage A protocol
            (A.1-A.6), Stage B delegation, critical rules,
            quality signals, session management, update flow
  |
  v
Stage A: Scope Discovery (A.1 through A.6)
  No refs/ loaded — all behavioral content in SKILL.md
  |
  v
Stage A.7: Build Task File
  Orchestrator loads: refs/build-request-template.md (~165 lines)
  Builder subagent loads: refs/agent-prompts.md (~415 lines)
                          refs/synthesis-mapping.md (~137 lines)
                          refs/validation-checklists.md (~127 lines)
  [Builder creates MDTM task file with all prompts baked in]
  |
  v
Stage A.8: Verify Task File
  Refs unloaded (no longer needed)
  |
  v
Stage B: Delegate to /task skill
  /task reads the task file (NOT SKILL.md or refs/)
```

**Loading budget compliance**: Orchestrator loads at most 2 files simultaneously (SKILL.md + build-request-template.md at A.7). Builder subagent loads 3 refs in its own context. Complies with "at most 2-3 refs loaded at any point" guidance.

## 3. Functional Requirements

### FR-PRD-R.0: Thin Command Layer — `commands/sc/prd.md`

**Description**: Create a thin command file at `.claude/commands/sc/prd.md` (~130-150 lines) following the `commands/sc/adversarial.md` pattern. The command provides the user-facing interface and hands off to the skill via the Activation pattern. The command contains zero protocol logic.

**Acceptance Criteria**:
- [ ] File exists at `.claude/commands/sc/prd.md`
- [ ] Frontmatter contains: `name: prd`, `description`, `category: documentation`, `complexity: advanced`, `allowed-tools`, `mcp-servers`, `personas`
- [ ] `## Required Input` section documents the mandatory `<product>` positional argument
- [ ] `## Usage` section shows invocation patterns: `/sc:prd <product> [options]`
- [ ] `## Arguments` section describes the `<product>` positional argument
- [ ] `## Options` table documents these flags:

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<product>` | - | Yes | - | Product, feature, or platform to document |
| `--tier` | `-t` | No | Auto | `lightweight`, `standard`, `heavyweight` |
| `--resume` | `-r` | No | `false` | Resume from existing task file |
| `--output` | `-o` | No | Auto | Output path for final PRD |
| `--scope` | `-s` | No | Auto | `product` or `feature` (PRD scope classification) |
| `--focus` | `-f` | No | All | Comma-separated directories/subsystems to focus on |
| `--purpose` | `-p` | No | - | What this PRD is for (engineering planning, investor materials, etc.) |

- [ ] `## Behavioral Summary` contains a one-paragraph overview of the two-stage process (scope discovery → task file execution) without protocol details
- [ ] `## Examples` section contains 4-5 examples migrated from SKILL.md B03 (Effective Prompt Examples) plus resume and tier-override examples:
  - Strong: all four inputs (product, purpose, focus dirs, output path)
  - Strong: clear scope + purpose
  - Strong: consolidation focus
  - Resume: `--resume` with existing task folder
  - Tier override: explicit `--tier heavyweight`
- [ ] `## Activation` section contains the mandatory handoff:
  ```
  **MANDATORY**: Before executing any protocol steps, invoke:
  > Skill prd
  
  Do NOT proceed with protocol execution using only this command file.
  The full behavioral specification is in the protocol skill.
  ```
- [ ] `## Boundaries` section contains Will/Will Not:
  - **Will**: Create PRDs through systematic codebase investigation and web research; Support three depth tiers; Resume from existing task files; Validate output through multi-agent QA pipeline
  - **Will Not**: Modify source code; Make architectural decisions; Execute PRD recommendations; Create specifications beyond PRDs (use `/tdd`, `/tech-reference`)
- [ ] `## Related Commands` table references `/tdd`, `/sc:workflow`, `/sc:design`, `/sc:brainstorm`
- [ ] Command file line count is between 100 and 170 lines
- [ ] Command contains zero protocol logic — no Stage A/B details, no agent spawning instructions, no phase descriptions

**Dependencies**: None

### FR-PRD-R.1: Decomposed SKILL.md Under 500 Lines

**Description**: The refactored SKILL.md contains only behavioral protocol (WHAT/WHEN) content and explicit loading declarations for refs/ files. Interface content (prompt examples, tier table) has moved to the command file.

**Acceptance Criteria**:
- [ ] SKILL.md line count is between 400 and 500 lines (400 is a soft floor; 500 is a hard ceiling)
- [ ] SKILL.md contains: frontmatter, purpose/header, input parsing logic (4 parameters + incomplete prompt template), tier selection rules (decision logic only — table moved to command), output locations, execution overview, Stage A protocol (A.1-A.6 + A.7 loading declaration + A.8 verification), Stage B delegation, critical rules, research quality signals, session management, updating an existing PRD
- [ ] SKILL.md does NOT contain: agent prompt templates, validation checklists, synthesis mapping tables, assembly process steps, content rules tables, BUILD_REQUEST format, output structure reference, effective prompt examples (moved to command), tier selection table (moved to command)
- [ ] SKILL.md contains explicit loading declarations at A.7 referencing the specific refs/ files to load (see FR-PRD-R.6)
- [ ] All cross-references formerly pointing to "section in SKILL.md" now point to the correct refs/ file path
- [ ] B30 (duplicate Artifact Locations table) is merged into B05 (Output Locations): B05's generalized pattern rows retained, B30's 6 specific QA paths appended, standalone B30 section removed

**Dependencies**: FR-PRD-R.0 (command file absorbs B03 examples + B04 table)

### FR-PRD-R.2: refs/agent-prompts.md — All 8 Agent Templates

**Description**: Contains all 8 agent prompt templates moved word-for-word from the original SKILL.md lines 553-967. This file already exists at 422 lines — verify fidelity, do not recreate.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/agent-prompts.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains these 8 agent prompt templates, each word-for-word identical to the original:
  1. Codebase Research Agent Prompt (original lines 558-637)
  2. Web Research Agent Prompt (original lines 639-686)
  3. Synthesis Agent Prompt (original lines 688-720)
  4. Research Analyst Agent Prompt / rf-analyst (original lines 722-759)
  5. Research QA Agent Prompt / rf-qa Research Gate (original lines 761-804)
  6. Synthesis QA Agent Prompt / rf-qa Synthesis Gate (original lines 806-846)
  7. Report Validation QA Agent Prompt / rf-qa (original lines 848-895)
  8. Assembly Agent Prompt / rf-assembler (original lines 897-967)
- [ ] Includes the section header "Agent Prompt Templates" and introductory paragraph (original lines 553-557)
- [ ] Includes the "Common web research topics for PRDs" list (original lines 679-686)
- [ ] Diff of each prompt template against the original SKILL.md shows zero content changes (whitespace normalization permitted)

**Dependencies**: None

### FR-PRD-R.3: refs/validation-checklists.md — All Checklists + Assembly Process + Content Rules

**Description**: Contains the Synthesis Quality Review Checklist, Assembly Process (Steps 8-11), Validation Checklist (18+4 items), and Content Rules table. This file already exists at 153 lines — verify fidelity, do not recreate.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/validation-checklists.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains the Synthesis Quality Review Checklist (9 criteria) word-for-word from original lines 1108-1128
- [ ] Contains the Assembly Process (Steps 8-11) word-for-word from original lines 1130-1193
- [ ] Contains the Validation Checklist (18+4 items) word-for-word from original lines 1195-1235
- [ ] Contains the Content Rules table (10 rows) word-for-word from original lines 1237-1254
- [ ] Retains all "> **Note:**" reference documentation markers from the original
- [ ] Diff against original line ranges shows zero content changes

**Dependencies**: None

### FR-PRD-R.4: refs/synthesis-mapping.md — Mapping Table + Output Structure

**Description**: Contains the Output Structure reference (PRD section outline) and the Synthesis Mapping Table. This file already exists at 142 lines — verify fidelity, do not recreate.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/synthesis-mapping.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains the Output Structure section word-for-word from original lines 969-1085
- [ ] Contains the Synthesis Mapping Table word-for-word from original lines 1087-1106
- [ ] Retains all "> **Note:**" reference documentation markers from the original
- [ ] Diff against original line ranges shows zero content changes

**Dependencies**: None

### FR-PRD-R.5: refs/build-request-template.md — BUILD_REQUEST Format

**Description**: Contains the complete BUILD_REQUEST format block currently embedded in A.7 (original lines 347-508). This is the only ref that does NOT yet exist — must be created.

**Acceptance Criteria**:
- [ ] File exists at `.claude/skills/prd/refs/build-request-template.md`
- [ ] Contains header explaining purpose and loading context
- [ ] Contains the complete BUILD_REQUEST format block from original lines 347-508
- [ ] The SKILL CONTEXT FILE references within BUILD_REQUEST are updated from section names to refs/ paths:

| Original Reference | Updated Reference |
|--------------------|-------------------|
| `Read the "Agent Prompt Templates" section` | `Read refs/agent-prompts.md` |
| `Read the "Synthesis Mapping Table" section` | `Read refs/synthesis-mapping.md` |
| `Read the "Synthesis Quality Review Checklist" section` | `Read refs/validation-checklists.md` |
| `Read the "Assembly Process" section` | `Read refs/validation-checklists.md (Assembly Process section)` |
| `Read the "Validation Checklist" section` | `Read refs/validation-checklists.md (Validation Checklist section)` |
| `Read the "Content Rules" section` | `Read refs/validation-checklists.md (Content Rules section)` |
| `Read the "Tier Selection" section` | No change — Tier Selection stays in SKILL.md |

- [ ] All other content in the BUILD_REQUEST is word-for-word identical to the original
- [ ] Diff against original lines 347-508 shows only the SKILL CONTEXT FILE path changes listed above

**Dependencies**: FR-PRD-R.2, FR-PRD-R.3, FR-PRD-R.4 (must know destination paths)

### FR-PRD-R.6: Per-Phase Loading Declarations in SKILL.md

**Description**: The refactored SKILL.md contains explicit instructions declaring which refs/ files to load at which phase.

**Acceptance Criteria**:
- [ ] Stage A.7 section in SKILL.md contains a loading declaration block:
  ```markdown
  ### A.7: Build the Task File

  **Refs Loaded (orchestrator):** The BUILD_REQUEST format is in `refs/build-request-template.md`. Read it before constructing the builder prompt.

  **Refs Loaded (builder subagent):** The BUILD_REQUEST instructs the builder to load these during task file construction:
  - `refs/agent-prompts.md` — agent prompt templates to embed in Phase 2 checklist items
  - `refs/synthesis-mapping.md` — template section mapping to embed in Phase 5 items
  - `refs/validation-checklists.md` — validation criteria to embed in Phase 3, 5, and 6 items

  The orchestrator uses only SKILL.md during Stage A. The builder subagent loads the 3 refs listed above within its own context.
  ```
- [ ] No other phase in SKILL.md loads refs/ files (Stage A.1-A.6 use only SKILL.md content; Stage B delegates to /task which reads the task file)
- [ ] The orchestrator context loads at most 2 files simultaneously (SKILL.md + build-request-template.md)

**Dependencies**: FR-PRD-R.1

### FR-PRD-R.7: Fidelity Verification — Zero Content Loss

**Description**: Every line of instructional content from the original 1,369-line SKILL.md appears in exactly one of: the refactored SKILL.md, one of the 4 refs/ files, or the command file. Zero content dropped, zero semantic drift, zero paraphrasing.

**Acceptance Criteria**:
- [ ] The fidelity index at `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` maps every content block with line ranges and destination files (update B03/B04 destinations for command-layer split)
- [ ] `diff` of each agent prompt template (8 templates) between original and `refs/agent-prompts.md` shows zero content changes
- [ ] `diff` of each checklist/table between original and `refs/validation-checklists.md` shows zero content changes
- [ ] `diff` of output structure and synthesis mapping between original and `refs/synthesis-mapping.md` shows zero content changes
- [ ] `diff` of BUILD_REQUEST between original and `refs/build-request-template.md` shows only the 6 documented SKILL CONTEXT FILE path changes
- [ ] Effective Prompt Examples (B03 partial, lines 46-60) appear in `commands/sc/prd.md` Examples section
- [ ] Tier Selection table (B04 partial, lines 79-85) appears in `commands/sc/prd.md` Options section
- [ ] Combined line count of command + SKILL.md + all refs/ files is between 1,380 and 1,520 lines (original 1,369 + command ~140 + ref headers ~12-20 + B30→B05 dedup savings ~-10)

**Dependencies**: FR-PRD-R.0 through FR-PRD-R.6

### FR-PRD-R.8: Content Migration from SKILL.md to Command

**Description**: Specific interface-concern content moves from SKILL.md to the command file. This content is removed from SKILL.md (not duplicated).

**Acceptance Criteria**:
- [ ] Effective Prompt Examples (original lines 46-60, ~15 lines) are present in command's Examples section and absent from SKILL.md
- [ ] Tier Selection table (original lines 79-85, ~7 lines) is present in command's Options section as `--tier` flag documentation and absent from SKILL.md (tier selection RULES at lines 87-92 remain in SKILL.md)
- [ ] SKILL.md Input section retains: 4-input parameter descriptions (lines 34-44), "What to Do If Prompt Is Incomplete" template (lines 62-73)
- [ ] SKILL.md Tier Selection section retains: selection rules (lines 87-92) but not the table header rows
- [ ] No content appears in BOTH the command file and SKILL.md (except brief cross-references)

**Dependencies**: FR-PRD-R.0, FR-PRD-R.1

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `.claude/commands/sc/prd.md` | Thin command layer: flags, usage, examples, boundaries, Activation handoff to `Skill prd` | None |
| `.claude/skills/prd/refs/build-request-template.md` | Complete BUILD_REQUEST format for spawning the rf-task-builder subagent | refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md (referenced within) |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `.claude/skills/prd/SKILL.md` | Reduced from 1,369 to ~420-450 lines. Agent prompts, BUILD_REQUEST, synthesis mapping, output structure, validation checklists, assembly process, content rules removed (to refs/). Prompt examples and tier table removed (to command). Loading declarations added at A.7. B30 merged into B05. | Comply with 500-line ceiling; enable three-tier architecture |

### 4.3 Removed Files

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| No files removed | Content moves to refs/ and command; nothing deleted | All content preserved in new locations |

### 4.4 Module Dependency Graph

```
commands/sc/prd.md (thin command, ~140 lines)
  |
  v [Activation: Skill prd]
skills/prd/SKILL.md (behavioral protocol, ~435 lines)
  |
  +-- [Stage A.1-A.6] no refs loaded
  |
  +-- [Stage A.7] --> refs/build-request-template.md (~165 lines)
  |                     |
  |                     +-- references --> refs/agent-prompts.md (~415 lines)
  |                     +-- references --> refs/synthesis-mapping.md (~137 lines)
  |                     +-- references --> refs/validation-checklists.md (~127 lines)
  |
  +-- [Stage B] --> /task skill (reads task file, NOT SKILL.md or refs/)
```

### 4.6 Implementation Order

```
1. Create commands/sc/prd.md                        -- no dependencies; template from adversarial.md
   Verify refs/agent-prompts.md fidelity            -- [parallel with step 1]
   Verify refs/synthesis-mapping.md fidelity         -- [parallel with step 1]
   Verify refs/validation-checklists.md fidelity     -- [parallel with step 1]
2. Create refs/build-request-template.md            -- depends on step 1 (needs verified refs/ paths)
3. Trim SKILL.md                                     -- depends on 1, 2 (remove moved content,
                                                        add loading declarations, merge B30→B05,
                                                        remove prompt examples + tier table)
4. Fidelity verification                             -- depends on 3 (diff every block against original)
5. make sync-dev && make verify-sync                 -- depends on 4 (propagate to src/superclaude/)
```

## 5. Interface Contracts

### 5.1 Command Interface

```
/sc:prd <product> [--tier lightweight|standard|heavyweight] [--resume]
        [--output <path>] [--scope product|feature]
        [--focus <dirs>] [--purpose <text>]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `<product>` | string | (required) | Product, feature, or platform to document |
| `--tier` | enum | Auto | Depth tier: `lightweight`, `standard`, `heavyweight` |
| `--resume` | bool | `false` | Resume from existing TASK-PRD-* task file |
| `--output` | path | Auto | Output path for final PRD |
| `--scope` | enum | Auto | `product` or `feature` (PRD scope classification) |
| `--focus` | string | All | Comma-separated directories/subsystems to focus on |
| `--purpose` | string | - | What this PRD is for |

### 5.3 Phase Contracts

The refactored skill's external interface is unchanged. Internally, the phase-to-refs loading contract is:

```yaml
phase_contracts:
  command_dispatch:
    loads: [commands/sc/prd.md]
    tokens: ~600
    action: "Parse flags, display interface, invoke Skill prd"
    
  invocation:
    loads: [SKILL.md]
    tokens: ~2000

  stage_a_1_through_a_6:
    loads: []  # No refs needed — behavioral protocol in SKILL.md
    additional_tokens: 0

  stage_a_7_build_task_file:
    loads:
      orchestrator: [refs/build-request-template.md]  # ~165 lines, ~700 tokens
      builder_subagent:
        - refs/agent-prompts.md       # ~415 lines, ~1500 tokens
        - refs/synthesis-mapping.md   # ~137 lines, ~500 tokens
        - refs/validation-checklists.md  # ~127 lines, ~500 tokens
    max_concurrent_in_orchestrator: 2  # SKILL.md + build-request-template

  stage_a_8_verify:
    loads: []  # Reads task file output, no refs needed

  stage_b_delegation:
    loads: []  # /task reads the task file, not SKILL.md or refs/
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-PRD-R.1 | SKILL.md token budget | <= 2,000 tokens on invocation | 420-450 lines at ~4.5 tokens/line = ~1,890-2,025 tokens |
| NFR-PRD-R.2 | Per-phase token overhead | At most 2 files loaded simultaneously by orchestrator | Count files loaded per phase in the loading declarations |
| NFR-PRD-R.3 | Session start cost | ~50 tokens (name + description only) | Unchanged from current — frontmatter stays the same |
| NFR-PRD-R.4 | Zero behavioral regression | Identical execution behavior before and after refactoring | End-to-end test: invoke skill on a test product and compare output structure |
| NFR-PRD-R.5 | Command file line budget | 100-170 lines | `wc -l commands/sc/prd.md` |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Content loss during SKILL.md trimming | Low | High | Fidelity index with first/last 10-word markers. Diff every block against original line ranges. |
| Cross-reference breakage in BUILD_REQUEST | Medium | High | Cross-reference map (Section 12.2) lists every reference. Grep for stale "section" references after implementation. |
| Command file incorrect Activation | Low | High | Single-line pattern: `Skill prd`. Verified by invoking `/sc:prd` and confirming skill loads. |
| Prompt examples lose context when moved to command | Low | Medium | Examples are self-contained strings that don't depend on surrounding SKILL.md context. The command's Examples section provides equivalent framing. |
| Tier table in command diverges from selection rules in skill | Low | Medium | Table is reference documentation (what the tiers ARE). Rules in skill are behavioral protocol (WHEN to pick each tier). They're independently correct. |
| Builder subagent can't find refs/ files | Low | Medium | Builder is spawned from the SKILL.md directory. Refs/ paths are relative. Test by spawning builder. |
| B30→B05 merge loses QA report paths | Low | Low | B30's 6 specific QA paths appended to B05's table. Diff verifies all paths present. |
| Scope creep — improving content during migration | Medium | Medium | Strict rule: zero content changes except documented B03/B04→command migration and BUILD_REQUEST path updates. Diff audit catches violations. |
| Existing refs/ files drifted from SKILL.md | Low | Medium | Verify all 3 existing refs against original SKILL.md line ranges before trimming SKILL.md. If drift found, re-extract from SKILL.md. |

## 8. Test Plan

### 8.1 Command Layer Tests

| Test | Validates |
|------|-----------|
| `test -f .claude/commands/sc/prd.md` | Command file exists |
| `wc -l .claude/commands/sc/prd.md` returns 100-170 | Command within line budget |
| `grep '## Activation' .claude/commands/sc/prd.md` returns match | Activation section present |
| `grep 'Skill prd' .claude/commands/sc/prd.md` returns match | Correct skill invocation |
| `grep '## Boundaries' .claude/commands/sc/prd.md` returns match | Boundaries section present |
| `grep -c '## Examples' .claude/commands/sc/prd.md` returns 1 | Examples section present |
| `grep -- '--tier' .claude/commands/sc/prd.md` returns match | Tier flag documented |
| `grep -- '--resume' .claude/commands/sc/prd.md` returns match | Resume flag documented |
| `grep 'wizard configuration' .claude/commands/sc/prd.md` returns match | Effective Prompt Example migrated from SKILL.md |

### 8.2 Fidelity Tests

| Test | Validates |
|------|-----------|
| Diff each of 8 agent prompts against original SKILL.md lines | Zero content change in refs/agent-prompts.md |
| Diff synthesis mapping table against original lines 1087-1106 | Zero content change in refs/synthesis-mapping.md |
| Diff output structure against original lines 969-1085 | Zero content change in refs/synthesis-mapping.md |
| Diff synthesis quality review against original lines 1108-1128 | Zero content change in refs/validation-checklists.md |
| Diff assembly process against original lines 1130-1193 | Zero content change in refs/validation-checklists.md |
| Diff validation checklist against original lines 1195-1235 | Zero content change in refs/validation-checklists.md |
| Diff content rules against original lines 1237-1254 | Zero content change in refs/validation-checklists.md |
| Diff BUILD_REQUEST against original lines 347-508 | Only 6 documented SKILL CONTEXT FILE path changes |

### 8.3 Structural Tests

| Test | Validates |
|------|-----------|
| `wc -l SKILL.md` returns 400-500 | SKILL.md under 500-line ceiling |
| `ls refs/` returns exactly 4 .md files (+ .gitkeep) | Correct number of refs/ files |
| `wc -l refs/agent-prompts.md` returns ~415-425 | Agent prompts file has expected content |
| `wc -l refs/build-request-template.md` returns ~160-175 | BUILD_REQUEST file has expected content |
| `wc -l refs/synthesis-mapping.md` returns ~135-145 | Synthesis mapping file has expected content |
| `wc -l refs/validation-checklists.md` returns ~125-155 | Validation checklists file has expected content |
| `grep -c 'Codebase Research Agent Prompt' SKILL.md` returns 0 | Agent prompts removed from SKILL.md |
| `grep -c 'Assembly Process' SKILL.md` returns 0 | Assembly process removed from SKILL.md |
| `grep -c 'Content Rules' SKILL.md` returns 0 | Content rules removed from SKILL.md |
| `grep -c 'BUILD_REQUEST' SKILL.md` returns 0 or 1 (loading declaration reference only) | BUILD_REQUEST removed from SKILL.md body |

### 8.4 Cross-Reference Tests

| Test | Validates |
|------|-----------|
| `grep -c 'Agent Prompt Templates section' SKILL.md` returns 0 | No stale section references in SKILL.md |
| `grep -c 'Synthesis Mapping Table section' SKILL.md` returns 0 | No stale section references |
| `grep -c 'Assembly Process section' SKILL.md` returns 0 | No stale section references |
| `grep -c 'Validation Checklist section' SKILL.md` returns 0 | No stale section references |
| `grep -c 'Content Rules section' SKILL.md` returns 0 | No stale section references |
| `grep 'refs/' SKILL.md` shows loading declarations at A.7 | Loading declarations present |
| `grep 'refs/agent-prompts.md' refs/build-request-template.md` returns match | BUILD_REQUEST references updated |
| `grep -c '".*section"' refs/build-request-template.md` returns 0 or 1 (only "Tier Selection" which stays in SKILL.md) | No stale prose section references |

### 8.5 Content Migration Tests

| Test | Validates |
|------|-----------|
| `grep 'Create a PRD for the GameFrame' .claude/commands/sc/prd.md` returns match | Strong prompt example migrated to command |
| `grep -c 'Create a PRD for the GameFrame' SKILL.md` returns 0 | Prompt example removed from SKILL.md |
| `grep 'Lightweight.*Single feature' .claude/commands/sc/prd.md` returns match | Tier table migrated to command |
| `grep -c '| **Lightweight**' SKILL.md` returns 0 | Tier table removed from SKILL.md |
| `grep 'What to Do If the Prompt Is Incomplete' SKILL.md` returns match | Incomplete prompt template stays in SKILL.md |
| `grep 'If in doubt, pick Standard' SKILL.md` returns match | Tier selection rules stay in SKILL.md |

### 8.6 Functional Test (Manual / E2E)

| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| Invoke via command | `/sc:prd "wizard system" --tier standard` | Command loads, activation triggers `Skill prd`, Stage A completes, task file created with all agent prompts baked in |
| Verify builder reads refs/ | During A.7, check builder subagent reads all 4 refs/ | Builder creates task file with correct embedded prompts |
| Verify no stale references | Grep task file for "section" references to SKILL.md | Zero matches — all references are to refs/ paths or baked-in content |
| Resume flow | `/sc:prd "wizard system" --resume` | Skill finds existing TASK-PRD-* folder, invokes /task to resume |

## 9. Migration & Rollout

- **Breaking changes**: None. The skill's external invocation pattern (`Skill prd`) is unchanged. The new command file (`/sc:prd`) is additive — it provides a standardized entry point that didn't exist before.
- **Backwards compatibility**: Full. The `/task` skill reads the task file (created during A.7), not SKILL.md or refs/. Agent prompts and validation criteria are baked into the task file during A.7, so downstream execution is unaffected.
- **Rollback plan**: Revert the commit. The original monolithic SKILL.md is preserved in git history. Single `git revert <commit>` restores the previous state.
- **Migration steps**:
  1. Implement all changes on the feature branch (`feat/v3.65-prd-tdd-Refactor` or a dedicated branch)
  2. Verify existing refs/ against original SKILL.md (step 1 in implementation order)
  3. Create command file and build-request-template.md
  4. Trim SKILL.md
  5. Run fidelity tests (Section 8.2) to verify zero content loss
  6. Run structural tests (Section 8.3) to verify line counts
  7. Run cross-reference tests (Section 8.4) to verify no stale references
  8. Run content migration tests (Section 8.5) to verify B03/B04 split
  9. `make sync-dev` to propagate `.claude/skills/prd/` → `src/superclaude/skills/prd/` AND `.claude/commands/sc/prd.md` → `src/superclaude/commands/prd.md`
  10. `make verify-sync` to confirm both locations match
  11. Merge to integration branch for testing

## 10. Downstream Inputs

### For sc:roadmap
Self-contained refactoring with no downstream roadmap impact. The PRD skill's capabilities and interface remain identical. The new command file is additive.

### For sc:tasklist
Two tasks:
1. "Create `commands/sc/prd.md` thin command layer following adversarial.md pattern, migrating B03 examples and B04 tier table from SKILL.md"
2. "Trim `SKILL.md` to ~435 lines: remove content now in refs/ and command, add loading declarations, merge B30→B05, create `refs/build-request-template.md`"

Estimated effort: 1-2 hours. Can be completed in a single session.

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| None | All questions resolved during brainstorm analysis | N/A | N/A |

## 12. Brainstorm Gap Analysis

> Analysis from `.dev/releases/backlog/prd-skill-refactor/02-brainstorm-output.md`

### 12.1 Content Block Inventory

The complete content block inventory with 32 blocks (B01-B32) is documented in the fidelity index at `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md`. Summary with v2 updates:

| Category | Blocks | Total Lines | Destination |
|----------|--------|-------------|-------------|
| Command interface | B03 partial, B04 partial | ~22 | `commands/sc/prd.md` (NEW in v2) |
| Behavioral (WHAT/WHEN) | B01-B02, B03 partial, B04 partial, B05-B10, B12-B13, B28-B32 | ~445 | SKILL.md |
| Agent Prompts (HOW) | B14-B21 | ~415 | refs/agent-prompts.md |
| BUILD_REQUEST (HOW) | B11 | ~165 | refs/build-request-template.md |
| Output Structure + Mapping (HOW) | B22-B23 | ~137 | refs/synthesis-mapping.md |
| Checklists + Process + Rules (HOW) | B24-B27 | ~127 | refs/validation-checklists.md |
| **Total** | **32 blocks** | **~1,311 (skill) + ~140 (command)** | **6 files** |

### 12.2 Cross-Reference Update Map

| Original Reference (in BUILD_REQUEST) | Updated Reference |
|----------------------------------------|-------------------|
| `Read the "Agent Prompt Templates" section` | `Read refs/agent-prompts.md` |
| `Read the "Synthesis Mapping Table" section` | `Read refs/synthesis-mapping.md` |
| `Read the "Synthesis Quality Review Checklist" section` | `Read refs/validation-checklists.md` |
| `Read the "Assembly Process" section` | `Read refs/validation-checklists.md (Assembly Process section)` |
| `Read the "Validation Checklist" section` | `Read refs/validation-checklists.md (Validation Checklist section)` |
| `Read the "Content Rules" section` | `Read refs/validation-checklists.md (Content Rules section)` |
| `Read the "Tier Selection" section` | No change — stays in SKILL.md |

### 12.3 Fidelity Index Updates Required

The fidelity index at `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` needs these updates for v2:

| Block | v1 Destination | v2 Destination | Change |
|-------|---------------|---------------|--------|
| B03 | `SKILL.md (Input section)` | `SKILL.md (Input section, partial)` + `commands/sc/prd.md (Examples)` | Effective Prompt Examples (lines 46-60) move to command |
| B04 | `SKILL.md (Tier Selection section)` | `SKILL.md (Tier Selection rules only)` + `commands/sc/prd.md (Options)` | Tier table (lines 79-85) moves to command; selection rules (87-92) stay |

All other block destinations are unchanged from v1.

### 12.4 Gaps Identified in v1 Spec

| Gap ID | Description | Severity | Resolution in v2 |
|--------|-------------|----------|-------------------|
| GAP-01 | v1 completely omits the thin command layer | Critical | Added FR-PRD-R.0 (command file) and FR-PRD-R.8 (content migration) |
| GAP-02 | v1 scope boundary excludes files outside `prd/` directory | Critical | Expanded scope to include `commands/sc/prd.md` |
| GAP-03 | v1 architecture diagram shows only skill+refs/ (2-tier) | Major | Updated 4.4 to show command→skill→refs/ (3-tier) |
| GAP-04 | v1 test plan has no command-layer tests | Major | Added Section 8.1 (Command Layer Tests) and 8.5 (Content Migration Tests) |
| GAP-05 | v1 migration steps don't mention command file sync | Minor | Updated Section 9 with command sync steps |
| GAP-06 | v1 fidelity index B03/B04 don't account for command split | Minor | Documented in Section 12.3 |
| GAP-07 | B30→B05 merge strategy not detailed in v1 | Low | Included in FR-PRD-R.1 acceptance criteria |
| GAP-08 | BUILD_REQUEST cross-references use section names not paths | Medium | Documented in FR-PRD-R.5 with full update map |

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Three-tier architecture | Command → Skill → Agents/refs/ — the mandatory architecture for SuperClaude components |
| Thin command layer | A ~80-150 line command file providing user-facing interface (flags, examples, boundaries) with zero protocol logic |
| Activation pattern | The `## Activation` section in a command that hands off to a skill via `Skill <name>` |
| SKILL.md | The main manifest file for a skill, containing behavioral protocol (WHAT/WHEN), max 500 lines |
| refs/ | Directory within a skill containing reference material (HOW content) loaded on demand per phase |
| BUILD_REQUEST | Structured prompt format passed to rf-task-builder to create an MDTM task file |
| MDTM | Markdown-Driven Task Management — the task file format for persistent progress tracking |
| Lazy loading | Loading refs/ files only when needed for a specific phase, not pre-loading all at invocation |
| Fidelity index | Document mapping every content block from source to destination with verification markers |
| B2 pattern | Self-contained checklist items in MDTM task files — each item is a complete prompt |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `.claude/skills/prd/SKILL.md` | Original monolithic file being refactored (1,369 lines — source of truth for content) |
| `.claude/commands/sc/adversarial.md` | Gold-standard thin command layer (167 lines — template for prd.md) |
| `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Three-tier architecture mandate, Skill-Authoring Checklist, anti-patterns |
| `.claude/skills/sc-adversarial-protocol/SKILL.md` + `refs/` | Reference implementation of decomposed skill with refs/ |
| `.dev/releases/complete/v3.65-prd-refactor/prd-refactor-spec.md` | v1 spec (superseded — addressed only refs/ decomposition) |
| `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` | Content block inventory — needs B03/B04 destination updates for v2 |
| `.dev/releases/backlog/prd-skill-refactor/02-brainstorm-output.md` | Brainstorm analysis with 6-dimension evaluation |
