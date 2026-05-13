# TDD Skill Refactoring -- Brainstorm Output

> **Generated**: 2026-04-03
> **Input**: `.dev/releases/complete/v3.65-tdd-skill-refactor/01-brainstorm-prompt.md`
> **Mode**: `--seq --ultrathink`
> **Source files read**: TDD SKILL.md (438 lines, post-decomposition), adversarial command (167 lines), PRD brainstorm output (484 lines), PRD spec v2 (FR-PRD-R.0 + FR-PRD-R.8), existing TDD refactor spec (407 lines), TDD fidelity index (150 lines), Developer Guide (Three-Tier Architecture, Activation Pattern, Sections 9.3, 9.7), release-spec-template.md (265 lines)

---

## Preliminary Finding: Decomposition Status

The TDD skill's refs/ decomposition is **COMPLETE**. Unlike the PRD skill (which had partially-created refs/ but an untrimmed SKILL.md), the TDD skill is fully decomposed:

- `SKILL.md`: 438 lines (under 500-line ceiling)
- `refs/agent-prompts.md`: exists (23,247 bytes)
- `refs/build-request-template.md`: exists (15,326 bytes)
- `refs/synthesis-mapping.md`: exists (6,914 bytes)
- `refs/validation-checklists.md`: exists (10,035 bytes)
- `refs/operational-guidance.md`: exists (8,146 bytes)

The SKILL.md already contains proper loading declarations (FR-TDD-R.6a through FR-TDD-R.6d) and the Phase Loading Contract table. The existing TDD refactor spec (tdd-refactor-spec.md) covers FR-TDD-R.1 through FR-TDD-R.7, all of which are now complete.

**The single remaining gap is the missing thin command layer** -- no `commands/sc/tdd.md` exists. This is the exact same gap identified in the PRD brainstorm (Dimension 1 and Dimension 6) and resolved in PRD spec v2 via FR-PRD-R.0 and FR-PRD-R.8.

---

## Dimension 1: Thin Command Layer Design

### Current State

The TDD skill has **no command file**. Users invoke it via `Skill tdd` or it activates through the skill description matcher. This violates:

1. **Developer Guide Three-Tier Architecture**: "Every skill MUST have a command in front of it."
2. **Developer Guide Section 9.3**: "Create a thin command layer (`commands/<name>.md`, ~80-150 lines) for every skill -- flags, usage, examples, boundaries, and an `## Activation` section that invokes the skill. No exceptions."
3. **Developer Guide Section 9.7 Anti-Pattern table**: "Skill without command layer -- Skill handles both interface and protocol concerns, creating a monolith."

### Option A: Minimal Command (~80-100 lines)

Bare essentials: frontmatter, brief usage, required input, 2-3 examples, activation, boundaries. No options table, no explicit flags.

**Trade-offs**: Fast to create, lowest maintenance surface. But fails to formalize tier selection, PRD reference, resume, focus directories, and output path as explicit flags. Users must know the skill's internal parameter model to invoke it precisely -- defeating the purpose of having a command layer.

### Option B: Standard Command (~120-150 lines) -- **Recommended**

Full adversarial-style command: frontmatter, required input, usage block, arguments, options table with explicit flags, behavioral summary, 4-5 examples, activation, boundaries, related commands.

Explicit flags to surface:

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<component>` | - | Yes | - | Component, service, or system to design |
| `--tier` | `-t` | No | Auto | `lightweight`, `standard`, `heavyweight` |
| `--prd` | - | No | - | Path to PRD that this TDD implements |
| `--resume` | `-r` | No | `false` | Resume from existing task file |
| `--output` | `-o` | No | Auto | Output path for final TDD |
| `--focus` | `-f` | No | All | Comma-separated directories/subsystems to focus on |
| `--from-prd` | - | No | `false` | Explicit PRD-to-TDD translation mode |

**Trade-offs**: Slightly more work than Option A, but formalizes the 4 implicit input parameters from SKILL.md's Input section as explicit flags. Matches the adversarial command pattern precisely. Matches the PRD brainstorm's recommended Option B (Standard Command, ~130-150 lines).

### Option C: Heavy Command (~180+ lines)

Includes inline tier selection table with agent counts and target lines, full prompt examples with quality annotations, and the "What to Do If Prompt Is Incomplete" template.

**Trade-offs**: Pushes too much content into the command. The tier table with agent counts and target line ranges is behavioral protocol content guiding the skill's A.3 and A.6 logic. The prompt completeness template drives A.2 triage logic. These belong in the skill.

### Option D: Two Commands (tdd.md + tdd-update.md)

Separate command for updating an existing TDD (lines 1349-1361 of original SKILL.md, now in refs/operational-guidance.md).

**Trade-offs**: Over-splitting. The update flow is a minor variant (check for existing task file in A.1), not a distinct command. The `--resume` flag on the main command suffices for re-entry.

### Recommendation: Option B (Standard Command, ~120-150 lines)

A command file at `commands/sc/tdd.md` with explicit flags for tier, prd, resume, output, focus, and from-prd. This follows the adversarial gold standard and mirrors the PRD brainstorm recommendation exactly.

**What moves from SKILL.md to command:**
1. **Effective Prompt Examples** (SKILL.md lines 48-63) -> Examples section of command
2. **Tier Selection table** (SKILL.md lines 84-88, the table rows only) -> Options section as `--tier` reference

**What stays in SKILL.md:**
1. The 4-input description (lines 34-46) -- the skill needs this for A.2 parsing
2. "What to Do If Prompt Is Incomplete" template (lines 65-76) -- behavioral protocol for A.2 triage
3. Tier selection rules (lines 90-94) -- behavioral protocol for A.3/A.6
4. Output Locations full table -- execution context for Stage A
5. All Stage A/B behavioral protocol

**Activation section:**
```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill tdd

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.
```

**Confidence**: High
**Impact on existing spec**: Requires a new FR (FR-TDD-CMD.1) for the command file. SKILL.md line count decreases by ~20 lines as prompt examples and tier table move to command.

---

## Dimension 2: Content Migration from SKILL.md to Command

### Context

The TDD SKILL.md is already 438 lines (under 500). Content migration is **optional for line budget reasons** but **recommended for architectural correctness**. The Developer Guide Section 9.3 explicitly says: "Put flags, usage examples, or CLI interface concerns in SKILL.md (belongs in the command)" is a "do not."

### Block-by-Block Analysis

#### B03: Input Section (lines 33-77, ~45 lines)

**Sub-block 1: 4-input description (lines 34-46, ~13 lines)**
- What: WHAT/PRD_REF/WHERE/OUTPUT parameters with explanations
- Verdict: **BOTH** -- Brief version in command's Arguments section, full version stays in SKILL.md for A.2 parsing

**Sub-block 2: Effective Prompt Examples (lines 48-63, ~16 lines)**
- What: 3 strong examples, 2 weak examples with quality annotations
- Verdict: **COMMAND** -- These are usage examples demonstrating invocation patterns. They are the command's Examples section territory. The skill does not need prompt examples to execute; it uses A.2 triage logic based on what the user provides.

**Sub-block 3: "What to Do If Prompt Is Incomplete" template (lines 65-76, ~12 lines)**
- What: Template for asking user to clarify vague requests
- Verdict: **SKILL** -- Behavioral protocol for A.2 triage. The skill needs this template to decide when and how to ask for clarification.

#### B04: Tier Selection (lines 80-95, ~16 lines)

**Sub-block 1: Tier table (lines 82-88, ~7 lines including header)**
- What: Lightweight/Standard/Heavyweight table with When/Agents/Web Agents/Target Lines
- Verdict: **COMMAND** -- Documents the `--tier` flag options. The brief table moves to the Options section.

**Sub-block 2: Selection rules (lines 90-94, ~5 lines)**
- What: Decision logic ("Default to Standard", "If user says detailed -> Heavyweight")
- Verdict: **SKILL** -- Behavioral protocol for A.3/A.6 tier selection. The command provides the flag; the skill applies the rules.

### Summary of Content Migration

| Content | Lines | From | To | Net effect on SKILL.md |
|---------|-------|------|----|------------------------|
| Effective Prompt Examples | ~16 | B03 in SKILL.md | Command Examples | -16 lines |
| Tier Selection table | ~7 | B04 in SKILL.md | Command Options | -7 lines |
| Brief 4-input description | ~13 | B03 in SKILL.md | Command Arguments | 0 (stays in both; command gets brief version) |
| "Prompt Is Incomplete" template | ~12 | B03 in SKILL.md | stays in SKILL.md | 0 |
| Tier selection rules | ~5 | B04 in SKILL.md | stays in SKILL.md | 0 |
| Output Locations | ~33 | B05 in SKILL.md | stays in SKILL.md | 0 |

**Net SKILL.md reduction**: ~23 lines (438 -> ~415 lines)

### Recommendation

Move the Effective Prompt Examples and the Tier Selection table to the command file. Keep the 4-input description (brief in command, full in skill), the incomplete prompt template, the tier selection rules, and all output locations in SKILL.md.

This migration is OPTIONAL for line budget (438 is already under 500) but RECOMMENDED for architectural correctness: the Developer Guide says usage examples and flag documentation belong in the command, not the skill.

**Confidence**: High
**Impact on existing spec**: Requires new FR (FR-TDD-CMD.2) for content migration. Fidelity index B03 and B04 destinations need updating to show partial migration to command.

---

## Dimension 3: Naming Convention

### Current State

- Skill directory: `.claude/skills/tdd/` (no `sc-` prefix)
- Skill name in frontmatter: `tdd`
- Invocation: `Skill tdd`

### Option A: Keep `tdd/` -- **Recommended**

Keep the current directory name. Create the command as `commands/sc/tdd.md`. Activation says `Skill tdd`.

**Analysis**: The Developer Guide Section 5.7 says skills prefixed with `sc-` have a special relationship with commands (they are protocol skills exclusively backing a single command). Skills without `sc-` (like `confidence-check`, `prd`, `tdd`) are standalone utilities invocable by any command or agent.

The TDD skill is a dual-purpose utility:
- User-facing: invoked via `/sc:tdd` for standalone TDD creation
- Composable: other skills could invoke it (e.g., a workflow skill orchestrating PRD-to-TDD translation)

The `sc-` prefix would lock it into single-command protocol territory and reduce portability.

**Precedent**: The PRD brainstorm recommended keeping `prd/` for identical reasons. The existing `prd/` and `tdd/` skills are standalone utilities. `sc-adversarial-protocol/` is the protocol-only pattern.

### Option B: Rename to `sc-tdd-protocol/`

Matches `sc-adversarial-protocol/` exactly.

**Trade-offs**: Requires renaming directory, updating frontmatter name field, updating all references in spec, fidelity index, and any cross-references. More work for cosmetic alignment. Reduces composability.

### Option C: Rename to `sc-tdd/`

Shorter, matches `sc-task-unified/`.

**Trade-offs**: Same rename overhead as Option B with no benefit over keeping `tdd/`.

### Recommendation: Option A (keep `tdd/`)

No rename. The command at `commands/sc/tdd.md` with `Skill tdd` activation provides the user-facing entry point. The skill remains composable by other skills. This is identical to the PRD brainstorm recommendation.

**Confidence**: High
**Impact on existing spec**: None -- the spec already uses `tdd/` naming.

---

## Dimension 4: Gaps in the Existing Spec

The existing spec at `.dev/releases/complete/v3.65-tdd-skill-refactor/tdd-refactor-spec.md` was written for the refs/ decomposition only. It has **one critical gap**: it completely omits the thin command layer.

### Gap 1: No Command File FR (CRITICAL)

**What is missing**: No functional requirement for creating `commands/sc/tdd.md`. The spec's scope boundary (Section 1.2) says "In scope: Refactoring TDD skill architecture only (file decomposition, per-phase loading declarations, cross-reference updates, fidelity mapping, validation strategy)." The command file is outside this scope.

**Impact**: The refactored skill still violates the Developer Guide's three-tier mandate. The spec solves "Monolithic SKILL.md" but not "Skill without command layer."

**Required additions**:
- New FR-TDD-CMD.1: Create `commands/sc/tdd.md` (~120-150 lines) with flags, usage, examples, boundaries, activation
- Expand scope boundary to include `commands/sc/tdd.md`
- Update Architecture 4.1 with command file
- Update Architecture 4.4 dependency graph to three-tier chain

### Gap 2: No Content Migration FR

**What is missing**: No requirement for moving interface content (prompt examples, tier table) from SKILL.md to the command.

**Required addition**: New FR-TDD-CMD.2 for content migration.

### Gap 3: No Command Layer Tests

**Required additions to Test Plan**:
- Structural test: Command file exists at `commands/sc/tdd.md`, line count 80-170
- Activation test: Command contains `## Activation` section with `Skill tdd`
- Flag test: Command documents `--tier`, `--prd`, `--resume`, `--output`, `--focus`, `--from-prd` flags
- Boundary test: Command has `## Boundaries` with Will/Will Not sections

### Gap 4: Architecture Missing Three-Tier Diagram

**What changes**: Section 4.4 shows only skill + refs/ (2-tier). Needs:

```
commands/sc/tdd.md (thin command, ~130 lines)
  |
  v [Activation: Skill tdd]
skills/tdd/SKILL.md (behavioral protocol, ~415 lines)
  |
  +-- [Stage A.7 orchestrator] --> refs/build-request-template.md
  |
  +-- [Stage A.7 builder] --> refs/agent-prompts.md
  |                       --> refs/synthesis-mapping.md
  |                       --> refs/validation-checklists.md
  |                       --> refs/operational-guidance.md
  |
  +-- [Stage B] --> /task skill
```

### Gap 5: Migration Steps Missing Command Sync

Section 9 mentions `make sync-dev` for skills but does not mention syncing the command file to `src/superclaude/commands/`.

---

## Dimension 5: Complexity and Risk Rating

### Complexity Score: 0.25

| Factor | Score | Rationale |
|--------|-------|-----------|
| Files changed | 0.2 | 1 new file (command), 1 edited file (SKILL.md -- remove ~23 lines of examples/table). No new refs/ needed. |
| Cross-references | 0.1 | Zero cross-reference updates needed -- no refs/ paths change. |
| Content migration complexity | 0.2 | ~23 lines of verbatim removal from SKILL.md. Prompt examples and tier table are contiguous, well-bounded blocks. |
| New files created | 0.3 | 1 new file: command file (from scratch, templated from adversarial + PRD pattern). |
| Behavioral change risk | 0.0 | Zero behavioral change. Purely additive (command) plus cosmetic removal (examples/table). |
| **Weighted average** | **0.25** | |

### Risk Assessment

| Risk Category | Rating | Detail |
|---------------|--------|--------|
| **Content loss** | VERY LOW | Only ~23 lines move from SKILL.md to command. These are prompt examples and a table -- well-bounded, contiguous blocks. Easy to verify. |
| **Cross-reference breakage** | NONE | No cross-references change. The refs/ decomposition is already complete and working. |
| **Naming collision** | NONE | Keeping `tdd/` directory name. No rename. |
| **Regression risk** | NONE | Command is purely additive. The SKILL.md content removal (examples, tier table) has zero effect on execution behavior -- A.2 triage uses the full 4-input description and incomplete prompt template (both staying), not the examples. A.3/A.6 uses tier selection rules (staying), not the table. |
| **Scope creep** | LOW | The scope is narrow: 1 new file, ~23 lines removed from 1 existing file. The temptation to also improve TDD skill content is mitigated by the narrow spec. |
| **Fidelity drift** | LOW | The content being removed is small and self-contained. Diff verification is straightforward. |

### Effort Estimate

| Metric | Estimate |
|--------|----------|
| Files in final state | 2 changed: `commands/sc/tdd.md` (NEW, ~130 lines), `skills/tdd/SKILL.md` (EDITED, ~415 lines) |
| Total net new lines | ~130 (command file) - ~23 (removed from SKILL.md) = ~107 net new |
| Single session? | Yes -- estimated ~30-45 minutes. The command file is templated from the adversarial pattern and the PRD command (when created). |
| Implementation order | 1. Create command file -> 2. Remove migrated content from SKILL.md -> 3. Verify SKILL.md structure -> 4. `make sync-dev` + `make verify-sync` |

### Complexity Class: LOW

This is significantly simpler than the PRD command-layer addition (which was rated MEDIUM at 0.40) because:
- The TDD SKILL.md decomposition is already complete (PRD's was not)
- No new refs/ files need creation (PRD needed `build-request-template.md`)
- No cross-reference updates needed (PRD had 7)
- Fewer lines migrate (~23 vs ~22 but PRD also had B30 dedup and BUILD_REQUEST extraction)

---

## Consolidated Recommendation

### The Implementation Plan (4 Steps)

1. **Create `commands/sc/tdd.md`** (~120-150 lines)
   - Modeled after `commands/sc/adversarial.md` (gold standard)
   - Frontmatter: name, description, category, complexity, allowed-tools, mcp-servers, personas
   - Required input: `<component>` -- component, service, or system to design
   - Flags: `--tier`, `--prd`, `--resume`, `--output`, `--focus`, `--from-prd`
   - Examples: migrated from SKILL.md lines 48-63 (Effective Prompt Examples), plus resume and tier-override examples
   - Behavioral Summary: one-paragraph overview of the two-stage process
   - Activation: `Skill tdd`
   - Boundaries: Will (create TDDs, investigate codebase, translate PRDs, validate quality) / Will Not (modify source code, implement designs, generate running code, create PRDs)
   - Related Commands: `/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`

2. **Remove migrated content from SKILL.md** (~23 lines)
   - Remove Effective Prompt Examples (lines 48-63, ~16 lines)
   - Remove Tier Selection table rows (lines 84-88, ~7 lines)
   - Keep: 4-input description, incomplete prompt template, tier selection rules, all behavioral protocol

3. **Verify structural integrity**
   - SKILL.md is ~415 lines (still well under 500)
   - All loading declarations intact
   - Phase Loading Contract table intact
   - No behavioral content affected

4. **Sync and verify**
   - Create `src/superclaude/commands/tdd.md` as canonical source
   - `make sync-dev` to propagate to `.claude/`
   - `make verify-sync` to confirm parity

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Create command file | YES -- `commands/sc/tdd.md` | Developer Guide mandate; every skill needs a command |
| Command style | Standard (~130 lines) with flags | Matches adversarial pattern, formalizes implicit parameters |
| Content migration | Move examples + tier table to command | Architectural correctness per Developer Guide 9.3 |
| Directory rename | NO -- keep `tdd/` | Dual-purpose utility; `sc-` is for protocol-only skills |
| refs/ changes | NONE | Decomposition already complete |

---

## Complexity/Risk Scorecard

| Metric | Rating |
|--------|--------|
| **Overall Complexity** | **0.25** (LOW) |
| **Content Loss Risk** | VERY LOW |
| **Cross-Reference Breakage Risk** | NONE |
| **Naming Collision Risk** | NONE |
| **Regression Risk** | NONE |
| **Scope Creep Risk** | LOW |
| **Fidelity Drift Risk** | LOW |
| **Estimated Effort** | Single session, ~30-45 minutes |
| **Files Created** | 1 (command file) |
| **Files Modified** | 1 (SKILL.md -- remove ~23 lines) |
| **Files Unchanged** | 5 (all refs/ files) |
| **Total Files in Final State** | 7 (1 command + 1 SKILL.md + 5 refs/) |
| **Can Complete in Single Session** | YES |

### Spec Revision Required

The existing TDD refactor spec needs these additive updates:

1. **Add FR-TDD-CMD.1** for the command file (modeled on FR-PRD-R.0)
2. **Add FR-TDD-CMD.2** for content migration (modeled on FR-PRD-R.8)
3. **Expand scope boundary** to include `commands/sc/tdd.md`
4. **Update Architecture 4.1** with command file entry
5. **Update Architecture 4.4** to three-tier dependency graph
6. **Add command-layer tests** (structural, activation, flags, boundaries)
7. **Update Migration 9** with command sync steps
8. **Update Implementation Order 4.6** to add command creation as step 0

These are purely additive -- the existing spec's refs/ decomposition and fidelity work are complete and unchanged.

---

## Draft Revised Spec: TDD Command Layer Addition

```yaml
---
title: "Add thin command layer for TDD skill to complete three-tier architecture"
version: "1.0.0"
status: draft
feature_id: FR-TDD-CMD
parent_feature: FR-TDD-REFACTOR
spec_type: refactoring
complexity_score: 0.25
complexity_class: LOW
target_release: v3.65
authors: [user, claude]
created: 2026-04-03
related_specs:
  - ".dev/releases/complete/v3.65-tdd-skill-refactor/tdd-refactor-spec.md (refs/ decomposition -- COMPLETE)"
quality_scores:
  clarity: 9.5
  completeness: 9.5
  testability: 9.5
  consistency: 9.5
  overall: 9.5
---
```

### 1. Problem Statement

The TDD skill at `.claude/skills/tdd/SKILL.md` is missing its thin command layer. While the refs/ decomposition is complete (SKILL.md is 438 lines with 5 refs/ files), no command file exists at `commands/sc/tdd.md`. This violates the Developer Guide's three-tier architecture mandate.

The Developer Guide states: "Every skill MUST have a command in front of it. The command is the user-facing entry point; the skill is the behavioral engine. A skill without a command is an architectural violation." (Three-Tier Architecture section)

Additionally, the SKILL.md contains ~23 lines of interface content (usage examples, tier selection table) that belong in the command layer per Developer Guide Section 9.3: "Put flags, usage examples, or CLI interface concerns in SKILL.md (belongs in the command)" is listed as a "do not."

#### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| No command file exists for TDD skill | `ls .claude/commands/sc/tdd*` returns empty | Users invoke skill directly -- no standardized entry point with flags, examples, or boundaries |
| Developer Guide mandate: "Every skill MUST have a command in front of it" | Developer Guide, Three-Tier Architecture section | TDD skill violates mandatory architecture |
| Developer Guide anti-pattern: "Skill without command layer" | Developer Guide Section 9.7 | Explicitly listed anti-pattern with solution: "Create a thin command file" |
| Skill-Authoring Checklist item 1: "Thin command layer exists" | Developer Guide Section 5.10 | Mandatory checklist item not satisfied |
| Usage examples in SKILL.md lines 48-63 | `.claude/skills/tdd/SKILL.md` | Interface content in skill file violates separation of concerns |
| Tier selection table in SKILL.md lines 82-88 | `.claude/skills/tdd/SKILL.md` | Flag documentation in skill file instead of command |
| PRD skill had identical gap, resolved in PRD spec v2 | `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec-v2.md` FR-PRD-R.0 | Established pattern for this exact fix |
| adversarial command demonstrates correct pattern | `.claude/commands/sc/adversarial.md` (167 lines) | Gold-standard thin command layer reference |

#### 1.2 Scope Boundary

**In scope**:
- Creating `commands/sc/tdd.md` (~120-150 lines) as the thin command layer
- Migrating interface content (prompt examples, tier table) from SKILL.md to command
- Corresponding `src/superclaude/commands/tdd.md` as canonical source
- `make sync-dev` + `make verify-sync` for commands/

**Out of scope**:
- Modifying TDD skill refs/ files (decomposition is complete)
- Modifying TDD skill pipeline logic, phase structure, or execution behavior
- Renaming the skill directory (stays as `tdd/`)
- Changing agent prompt content, validation criteria, or content rules
- Adding new features or capabilities to the TDD skill

### 2. Solution Overview

Create a thin command file at `commands/sc/tdd.md` (~120-150 lines) following the `commands/sc/adversarial.md` gold standard. Migrate ~23 lines of interface content (usage examples, tier selection table) from SKILL.md to the command. This completes the three-tier architecture: Command -> Skill -> refs/.

#### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Create command file | YES -- `commands/sc/tdd.md` | Skip command (current state) | Developer Guide mandates command layer for every skill |
| Command style | Standard (~130 lines) with explicit flags | Minimal (~100, no flags); Heavy (~180+, inline tables) | Standard matches adversarial gold standard and PRD pattern |
| Content migration | Move prompt examples + tier table | Move nothing; Move entire Input section | Examples are usage patterns (command territory). Tier table documents `--tier` flag. Parsing logic and selection rules stay in skill. |
| Directory rename | NO -- keep `tdd/` | `sc-tdd-protocol/`, `sc-tdd/` | Dual-purpose utility; `sc-` prefix is for protocol-only skills |
| TDD-specific flags | `--prd`, `--from-prd` in addition to standard flags | Omit PRD flags | PRD-to-TDD translation is a core use case documented in SKILL.md description |

#### 2.2 Workflow / Data Flow

```
User invokes /sc:tdd <component> [flags]
  |
  v
commands/sc/tdd.md loaded (~130 lines)
  Parses flags, shows usage/examples/boundaries
  |
  v [Activation: Skill tdd]
skills/tdd/SKILL.md loaded (~415 lines, post-migration)
  Contains: purpose, input parsing, tier selection rules,
            output locations, execution overview, Stage A protocol,
            Stage B delegation, phase loading contract
  |
  v
Stage A: Scope Discovery (A.1 through A.6)
  No refs/ loaded -- all behavioral content in SKILL.md
  |
  v
Stage A.7: Build Task File
  Orchestrator loads: refs/build-request-template.md
  Builder loads: refs/agent-prompts.md, refs/synthesis-mapping.md,
                 refs/validation-checklists.md, refs/operational-guidance.md
  |
  v
Stage A.8: Verify task file
  |
  v
Stage B: Delegate to /task skill
  /task executes self-contained checklist items from task file
```

### 3. Functional Requirements

#### FR-TDD-CMD.1: Thin Command Layer -- `commands/sc/tdd.md`

**Description**: Create a thin command file at `.claude/commands/sc/tdd.md` (~120-150 lines) following the `commands/sc/adversarial.md` pattern. The command provides the user-facing interface and hands off to the skill via the Activation pattern. The command contains zero protocol logic.

**Acceptance Criteria**:
- [ ] File exists at `.claude/commands/sc/tdd.md`
- [ ] Canonical source exists at `src/superclaude/commands/tdd.md`
- [ ] Frontmatter contains: `name: tdd`, `description`, `category: documentation`, `complexity: advanced`, `allowed-tools`, `mcp-servers`, `personas`
- [ ] `## Required Input` section documents the mandatory `<component>` positional argument
- [ ] `## Usage` section shows invocation patterns: `/sc:tdd <component> [options]`
- [ ] `## Arguments` section describes the `<component>` positional argument and optional PRD reference
- [ ] `## Options` table documents these flags:

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<component>` | - | Yes | - | Component, service, or system to design |
| `--tier` | `-t` | No | Auto | `lightweight`, `standard`, `heavyweight` |
| `--prd` | - | No | - | Path to PRD that this TDD implements |
| `--resume` | `-r` | No | `false` | Resume from existing task file |
| `--output` | `-o` | No | Auto | Output path for final TDD |
| `--focus` | `-f` | No | All | Comma-separated directories/subsystems to focus on |
| `--from-prd` | - | No | `false` | Explicit PRD-to-TDD translation mode |

- [ ] `## Behavioral Summary` contains a one-paragraph overview of the two-stage process (scope discovery with task file creation, then task file execution via `/task` delegation) without protocol details
- [ ] `## Examples` section contains 5-6 examples migrated from SKILL.md lines 48-63 (Effective Prompt Examples) plus TDD-specific examples:
  - Strong: all four inputs (component, PRD reference, focus dirs, output path)
  - Strong: PRD-to-TDD translation with explicit PRD path
  - Strong: design from scratch with clear scope
  - Weak (annotated): topic only (demonstrates what minimal input looks like)
  - Resume: `--resume` with existing task folder
  - Tier override: explicit `--tier heavyweight`
- [ ] `## Activation` section contains the mandatory handoff:
  ```
  **MANDATORY**: Before executing any protocol steps, invoke:
  > Skill tdd

  Do NOT proceed with protocol execution using only this command file.
  The full behavioral specification is in the protocol skill.
  ```
- [ ] `## Boundaries` section contains Will/Will Not:
  - **Will**: Create TDDs through systematic codebase investigation and web research; Translate PRDs into engineering specifications; Support three depth tiers (Lightweight, Standard, Heavyweight); Resume from existing task files; Validate output through multi-agent QA pipeline
  - **Will Not**: Modify source code; Implement the designs described in the TDD; Generate running code (documents existing patterns only); Create PRDs (use `/sc:prd`); Make product decisions
- [ ] `## Related Commands` table references `/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`
- [ ] Command file line count is between 100 and 170 lines
- [ ] Command contains zero protocol logic -- no Stage A/B details, no agent spawning instructions, no phase descriptions, no loading declarations

**Dependencies**: None

#### FR-TDD-CMD.2: Content Migration from SKILL.md to Command

**Description**: Specific interface-concern content moves from SKILL.md to the command file. This content is removed from SKILL.md (not duplicated).

**Acceptance Criteria**:
- [ ] Effective Prompt Examples (SKILL.md lines 48-63) appear in `commands/sc/tdd.md` Examples section, adapted to command invocation syntax (e.g., `/sc:tdd <component> --prd <path> --focus <dirs>`)
- [ ] Tier Selection table (SKILL.md lines 82-88, the header + 3 data rows) appears in `commands/sc/tdd.md` Options section as `--tier` reference
- [ ] SKILL.md Input section retains: 4-input description (lines 34-46), "What to Do If Prompt Is Incomplete" template (lines 65-76)
- [ ] SKILL.md Tier Selection section retains: introductory sentence + selection rules (lines 90-94) but not the full table
- [ ] No content appears in BOTH the command file and SKILL.md (except brief cross-references such as "See `commands/sc/tdd.md` for usage examples")
- [ ] Post-migration SKILL.md line count is between 400 and 440 lines

**Dependencies**: FR-TDD-CMD.1

### 4. Architecture

#### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/commands/tdd.md` | Canonical thin command layer for TDD skill | None |
| `.claude/commands/sc/tdd.md` | Dev-copy mirror for Claude Code runtime | Produced via `make sync-dev` |

#### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/skills/tdd/SKILL.md` | Remove ~23 lines of interface content (prompt examples, tier table) | Content migrates to command per Developer Guide 9.3 |
| `.claude/skills/tdd/SKILL.md` | Synced dev-copy of canonical SKILL.md | Runtime parity after `make sync-dev` |

#### 4.3 Removed Files

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| None | No files removed. Content within SKILL.md is relocated, not deleted. | Prompt examples -> command Examples section. Tier table -> command Options section. |

#### 4.4 Module Dependency Graph

```
commands/sc/tdd.md (thin command, ~130 lines)
  |
  v [Activation: Skill tdd]
skills/tdd/SKILL.md (behavioral protocol, ~415 lines)
  |
  +-- [Stage A.7 orchestrator] --> refs/build-request-template.md
  |
  +-- [Stage A.7 builder] --> refs/agent-prompts.md
  |                       --> refs/synthesis-mapping.md
  |                       --> refs/validation-checklists.md
  |                       --> refs/operational-guidance.md
  |
  +-- [Stage B] --> /task skill (canonical F1 execution loop)
```

#### 4.6 Implementation Order

```
1. Create src/superclaude/commands/tdd.md         -- New command file from adversarial template
2. Remove interface content from src/.../SKILL.md  -- Parallel with step 1 if desired
3. Verify SKILL.md structural integrity            -- Depends on 2
4. make sync-dev                                   -- Depends on 1, 2
5. make verify-sync                                -- Depends on 4
```

### 5. Interface Contracts

#### 5.1 Command Interface

```
/sc:tdd <component> [--tier lightweight|standard|heavyweight] [--prd <path>]
        [--resume] [--output <path>] [--focus <dirs>] [--from-prd]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<component>` | positional string | (required) | Component, service, or system to design |
| `--tier` | enum | Auto | Depth tier: lightweight, standard, heavyweight |
| `--prd` | path | - | PRD file that this TDD implements |
| `--resume` | boolean | false | Resume from existing MDTM task file |
| `--output` | path | Auto | Output path for final TDD |
| `--focus` | comma-string | All | Directories/subsystems to focus investigation on |
| `--from-prd` | boolean | false | Explicit PRD-to-TDD translation mode |

### 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-TDD-CMD.1 | Command file size | 100-170 lines | `wc -l commands/sc/tdd.md` |
| NFR-TDD-CMD.2 | Zero protocol leakage | Command contains no Stage A/B, no agent spawning, no phase logic | Manual review |
| NFR-TDD-CMD.3 | Post-migration SKILL.md size | 400-440 lines | `wc -l skills/tdd/SKILL.md` |
| NFR-TDD-CMD.4 | Activation correctness | Command hands off to `Skill tdd` | Grep for activation pattern |

### 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Content loss during migration | Very Low | Low | Only ~23 lines move; contiguous blocks; diff verification |
| Protocol leakage into command | Low | Medium | Review against adversarial gold standard; no Stage/Phase/Agent keywords in command |
| Scope creep to improve TDD content | Low | Medium | Strict spec: only create command + remove migrated content. Zero behavioral changes. |
| Sync failure (command not in src/) | Low | Low | `make verify-sync` catches immediately |

### 8. Test Plan

#### 8.1 Command Layer Tests

| Test | File | Validates |
|------|------|-----------|
| Command existence test | `commands/sc/tdd.md` | File exists, line count 100-170 |
| Frontmatter test | `commands/sc/tdd.md` | Contains required frontmatter fields: name, description, category, complexity, allowed-tools |
| Activation test | `commands/sc/tdd.md` | Contains `## Activation` section with `Skill tdd` invocation |
| Flag documentation test | `commands/sc/tdd.md` | Options table documents `--tier`, `--prd`, `--resume`, `--output`, `--focus`, `--from-prd` |
| Boundary test | `commands/sc/tdd.md` | Contains `## Boundaries` with Will/Will Not sections |
| Zero-protocol test | `commands/sc/tdd.md` | No occurrences of: "Stage A", "Stage B", "A.1", "A.2", "A.3", "A.7", "rf-task-builder", "subagent", "Phase 2", "Phase 3", "Phase 5", "Phase 6", "checklist item" |
| Examples test | `commands/sc/tdd.md` | Contains `## Examples` with at least 4 usage examples |
| Related commands test | `commands/sc/tdd.md` | Contains `## Related Commands` table |

#### 8.2 Content Migration Tests

| Test | Validates |
|------|-----------|
| Examples removed from SKILL.md | Lines matching "Strong --" and "Weak --" prompt example patterns no longer appear in SKILL.md Input section |
| Tier table removed from SKILL.md | Full tier table (Lightweight/Standard/Heavyweight rows with agent counts) no longer in SKILL.md |
| Tier rules retained in SKILL.md | "Default to Standard" and "always Heavyweight" selection rules remain in SKILL.md |
| Input parsing retained in SKILL.md | 4-input description and incomplete prompt template remain in SKILL.md |
| SKILL.md line count | Post-migration line count is 400-440 |
| No duplication | Content that appears in command does not appear in SKILL.md (except brief "see command" cross-references) |

#### 8.3 Integration Tests

| Test | Validates |
|------|-----------|
| Sync integrity | `make sync-dev` creates `.claude/commands/sc/tdd.md` from `src/superclaude/commands/tdd.md` |
| Sync verification | `make verify-sync` passes with no src-to-dev drift |
| Canonical source exists | `src/superclaude/commands/tdd.md` exists and matches `.claude/commands/sc/tdd.md` |
| SKILL.md refs/ loading intact | Loading declarations in SKILL.md still reference all 5 refs/ files correctly |
| Phase Loading Contract intact | FR-TDD-R.6c table in SKILL.md is unmodified |

#### 8.4 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| Command-to-skill handoff | Read `commands/sc/tdd.md`, verify Activation section invokes `Skill tdd` | Activation pattern matches Developer Guide template exactly |
| Gold-standard comparison | Diff `commands/sc/tdd.md` structure against `commands/sc/adversarial.md` | Same structural sections in same order: frontmatter, required input, usage, arguments, options, behavioral summary, examples, activation, boundaries, related commands |
| Three-tier completeness | Verify all three tiers exist: command at `commands/sc/`, skill at `skills/tdd/`, refs at `skills/tdd/refs/` | All three tiers present |

### 9. Migration and Rollout

- **Breaking changes**: None. This is purely additive (new command file) plus cosmetic cleanup (interface content moves from skill to command).
- **Backwards compatibility**: Preserved. Direct `Skill tdd` invocation continues to work. The command file adds a new, standardized entry point without removing the existing one.
- **Rollback plan**: Delete `commands/sc/tdd.md` and restore the ~23 lines to SKILL.md via git revert.
- **Migration path**: Single commit containing command file creation + SKILL.md content removal + sync. Run `make sync-dev` then `make verify-sync`.

### 10. Downstream Inputs

#### For sc:roadmap
This spec is a minor additive item under the v3.65 TDD refactor release. No behavioral feature delta.

#### For sc:tasklist
Generate 4 implementation tasks from Section 4.6:
1. Create `src/superclaude/commands/tdd.md` (command file)
2. Remove migrated content from `src/superclaude/skills/tdd/SKILL.md`
3. Run `make sync-dev` and `make verify-sync`
4. Run test plan verification

### 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| None | All questions resolved during brainstorm analysis | - | - |

### 12. Brainstorm Gap Analysis

| Gap ID | Description | Severity | Affected Section | Resolution |
|--------|-------------|----------|------------------|------------|
| GAP-CMD-01 | Existing TDD refactor spec omits command layer entirely | Critical | Scope, Architecture, Tests | This spec (FR-TDD-CMD) addresses as a companion/addendum to the existing spec |
| GAP-CMD-02 | SKILL.md contains ~23 lines of interface content (examples, tier table) | Minor | Content migration | FR-TDD-CMD.2 moves this content to command |
| GAP-CMD-03 | Three-tier dependency graph missing from existing spec | Major | Architecture 4.4 | This spec provides the complete three-tier graph |

---

### Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Thin command layer | The ~80-150 line command file providing flags, usage, examples, boundaries, and Activation handoff to a skill |
| Three-tier architecture | Command -> Skill -> Agents/refs/ pattern mandated by Developer Guide |
| Activation pattern | The `## Activation` section in a command that hands off to a skill via `Skill <name>` |
| Interface content | Flags, usage examples, tier tables -- content belonging in the command layer |
| Protocol content | Behavioral logic (WHAT/WHEN) -- content belonging in the skill layer |

### Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `.claude/commands/sc/adversarial.md` | Gold-standard thin command layer (167 lines) |
| `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec-v2.md` | PRD spec v2 with FR-PRD-R.0 (command layer) and FR-PRD-R.8 (content migration) -- direct pattern for this spec |
| `.dev/releases/backlog/prd-skill-refactor/02-brainstorm-output.md` | PRD brainstorm output with Dimension 1 (command layer design) analysis |
| `.dev/releases/complete/v3.65-tdd-skill-refactor/tdd-refactor-spec.md` | Existing TDD refactor spec (refs/ decomposition -- COMPLETE) |
| `.dev/releases/complete/v3.65-tdd-skill-refactor/fidelity-index.md` | TDD fidelity index mapping all source blocks to destinations |
| `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Developer Guide: Three-Tier Architecture, Activation Pattern, Sections 9.3, 9.7 |
| `src/superclaude/examples/release-spec-template.md` | Release spec template |
| `.claude/skills/tdd/SKILL.md` | Current TDD skill (438 lines, post-decomposition) |
