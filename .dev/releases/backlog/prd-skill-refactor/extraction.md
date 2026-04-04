---
spec_source: "prd-refactor-spec-v2.md"
generated: "2026-04-03T12:00:00Z"
generator: "requirements-extraction-agent/opus-4.6"
functional_requirements: 9
nonfunctional_requirements: 5
total_requirements: 14
complexity_score: 0.45
complexity_class: MEDIUM
domains_detected: [architecture, documentation, developer-tooling]
risks_identified: 9
dependencies_identified: 8
success_criteria_count: 12
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 137.0, started_at: "2026-04-03T19:52:08.722609+00:00", finished_at: "2026-04-03T19:54:25.742930+00:00"}
---

## Functional Requirements

### FR-PRD-R.0: Thin Command Layer — `commands/sc/prd.md`

**Priority**: Critical (addresses Violation 2 — missing command layer)
**Description**: Create a thin command file at `.claude/commands/sc/prd.md` (~130-150 lines) following the `commands/sc/adversarial.md` pattern. Provides user-facing interface (flags, usage, examples, boundaries) and hands off to the skill via the Activation pattern. Contains zero protocol logic.

**Sub-requirements**:
- FR-PRD-R.0a: File exists at `.claude/commands/sc/prd.md` with correct frontmatter (`name: prd`, `description`, `category: documentation`, `complexity: advanced`, `allowed-tools`, `mcp-servers`, `personas`)
- FR-PRD-R.0b: `## Required Input` section documents mandatory `<product>` positional argument
- FR-PRD-R.0c: `## Usage` section shows invocation patterns: `/sc:prd <product> [options]`
- FR-PRD-R.0d: `## Arguments` section describes the `<product>` positional argument
- FR-PRD-R.0e: `## Options` table documents 7 flags: `<product>`, `--tier`, `--resume`, `--output`, `--scope`, `--focus`, `--purpose` with short forms, defaults, and descriptions
- FR-PRD-R.0f: `## Behavioral Summary` contains one-paragraph overview of two-stage process (scope discovery then task file execution) with no protocol details
- FR-PRD-R.0g: `## Examples` section contains 4-5 examples migrated from SKILL.md B03 (Effective Prompt Examples) plus resume and tier-override examples
- FR-PRD-R.0h: `## Activation` section contains mandatory handoff: `Skill prd` invocation with "Do NOT proceed" warning
- FR-PRD-R.0i: `## Boundaries` section contains Will/Will Not lists as specified
- FR-PRD-R.0j: `## Related Commands` table references `/tdd`, `/sc:workflow`, `/sc:design`, `/sc:brainstorm`
- FR-PRD-R.0k: Line count between 100 and 170 lines
- FR-PRD-R.0l: Command contains zero protocol logic — no Stage A/B details, no agent spawning instructions, no phase descriptions

**Dependencies**: None

---

### FR-PRD-R.1: Decomposed SKILL.md Under 500 Lines

**Priority**: Critical (addresses Violation 1 — monolithic SKILL.md)
**Description**: Refactored SKILL.md contains only behavioral protocol (WHAT/WHEN) content and explicit loading declarations for refs/ files. Interface content (prompt examples, tier table) moved to command file.

**Sub-requirements**:
- FR-PRD-R.1a: Line count between 400 (soft floor) and 500 (hard ceiling)
- FR-PRD-R.1b: Retained content: frontmatter, purpose/header, input parsing logic (4 parameters + incomplete prompt template), tier selection rules (decision logic only), output locations, execution overview, Stage A protocol (A.1-A.6 + A.7 loading declaration + A.8 verification), Stage B delegation, critical rules, research quality signals, session management, updating existing PRD
- FR-PRD-R.1c: Removed content: agent prompt templates, validation checklists, synthesis mapping tables, assembly process steps, content rules tables, BUILD_REQUEST format, output structure reference, effective prompt examples, tier selection table
- FR-PRD-R.1d: Explicit loading declarations at A.7 referencing specific refs/ files (see FR-PRD-R.6)
- FR-PRD-R.1e: All cross-references formerly pointing to "section in SKILL.md" now point to correct refs/ file paths
- FR-PRD-R.1f: B30 (duplicate Artifact Locations table) merged into B05 (Output Locations): B05 generalized pattern rows retained, B30's 6 specific QA paths appended, standalone B30 section removed

**Dependencies**: FR-PRD-R.0 (command file absorbs B03 examples + B04 table)

---

### FR-PRD-R.2: refs/agent-prompts.md — All 8 Agent Templates

**Priority**: High
**Description**: Contains all 8 agent prompt templates moved word-for-word from original SKILL.md lines 553-967. File already exists at 422 lines — verify fidelity, do not recreate.

**Sub-requirements**:
- FR-PRD-R.2a: File exists at `.claude/skills/prd/refs/agent-prompts.md` with header explaining purpose/loading context
- FR-PRD-R.2b: Contains all 8 named agent prompt templates, each word-for-word identical to the original: (1) Codebase Research Agent, (2) Web Research Agent, (3) Synthesis Agent, (4) Research Analyst / rf-analyst, (5) Research QA / rf-qa Research Gate, (6) Synthesis QA / rf-qa Synthesis Gate, (7) Report Validation QA / rf-qa, (8) Assembly Agent / rf-assembler
- FR-PRD-R.2c: Includes "Agent Prompt Templates" section header and introductory paragraph (original lines 553-557)
- FR-PRD-R.2d: Includes "Common web research topics for PRDs" list (original lines 679-686)
- FR-PRD-R.2e: Diff of each prompt template against original SKILL.md shows zero content changes (whitespace normalization permitted)

**Dependencies**: None

---

### FR-PRD-R.3: refs/validation-checklists.md — All Checklists + Assembly Process + Content Rules

**Priority**: High
**Description**: Contains Synthesis Quality Review Checklist, Assembly Process (Steps 8-11), Validation Checklist (18+4 items), and Content Rules table. File already exists at 153 lines — verify fidelity, do not recreate.

**Sub-requirements**:
- FR-PRD-R.3a: File exists at `.claude/skills/prd/refs/validation-checklists.md` with header
- FR-PRD-R.3b: Synthesis Quality Review Checklist (9 criteria) word-for-word from original lines 1108-1128
- FR-PRD-R.3c: Assembly Process (Steps 8-11) word-for-word from original lines 1130-1193
- FR-PRD-R.3d: Validation Checklist (18+4 items) word-for-word from original lines 1195-1235
- FR-PRD-R.3e: Content Rules table (10 rows) word-for-word from original lines 1237-1254
- FR-PRD-R.3f: All `> **Note:**` reference documentation markers retained
- FR-PRD-R.3g: Diff against original line ranges shows zero content changes

**Dependencies**: None

---

### FR-PRD-R.4: refs/synthesis-mapping.md — Mapping Table + Output Structure

**Priority**: High
**Description**: Contains Output Structure reference (PRD section outline) and Synthesis Mapping Table. File already exists at 142 lines — verify fidelity, do not recreate.

**Sub-requirements**:
- FR-PRD-R.4a: File exists at `.claude/skills/prd/refs/synthesis-mapping.md` with header
- FR-PRD-R.4b: Output Structure section word-for-word from original lines 969-1085
- FR-PRD-R.4c: Synthesis Mapping Table word-for-word from original lines 1087-1106
- FR-PRD-R.4d: All `> **Note:**` reference documentation markers retained
- FR-PRD-R.4e: Diff against original line ranges shows zero content changes

**Dependencies**: None

---

### FR-PRD-R.5: refs/build-request-template.md — BUILD_REQUEST Format

**Priority**: High (only ref that does NOT yet exist)
**Description**: Contains complete BUILD_REQUEST format block from original lines 347-508. Cross-references within updated from section names to refs/ paths per documented mapping.

**Sub-requirements**:
- FR-PRD-R.5a: File exists at `.claude/skills/prd/refs/build-request-template.md` with header
- FR-PRD-R.5b: Contains complete BUILD_REQUEST format block from original lines 347-508
- FR-PRD-R.5c: 6 SKILL CONTEXT FILE references updated per mapping:
  - `"Agent Prompt Templates" section` → `refs/agent-prompts.md`
  - `"Synthesis Mapping Table" section` → `refs/synthesis-mapping.md`
  - `"Synthesis Quality Review Checklist" section` → `refs/validation-checklists.md`
  - `"Assembly Process" section` → `refs/validation-checklists.md (Assembly Process section)`
  - `"Validation Checklist" section` → `refs/validation-checklists.md (Validation Checklist section)`
  - `"Content Rules" section` → `refs/validation-checklists.md (Content Rules section)`
- FR-PRD-R.5d: `"Tier Selection" section` reference unchanged (stays in SKILL.md)
- FR-PRD-R.5e: All other content word-for-word identical to original
- FR-PRD-R.5f: Diff against original lines 347-508 shows only the 6 documented path changes

**Dependencies**: FR-PRD-R.2, FR-PRD-R.3, FR-PRD-R.4 (destination paths must be known)

---

### FR-PRD-R.6: Per-Phase Loading Declarations in SKILL.md

**Priority**: High
**Description**: Refactored SKILL.md contains explicit instructions declaring which refs/ files load at which phase.

**Sub-requirements**:
- FR-PRD-R.6a: Stage A.7 section contains orchestrator loading declaration for `refs/build-request-template.md`
- FR-PRD-R.6b: Stage A.7 section contains builder subagent loading declaration listing `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`
- FR-PRD-R.6c: No other phase in SKILL.md loads refs/ files (A.1-A.6 use SKILL.md only; Stage B delegates to /task)
- FR-PRD-R.6d: Orchestrator context loads at most 2 files simultaneously (SKILL.md + build-request-template.md)

**Dependencies**: FR-PRD-R.1

---

### FR-PRD-R.7: Fidelity Verification — Zero Content Loss

**Priority**: Critical (validation gate)
**Description**: Every line of instructional content from the original 1,369-line SKILL.md appears in exactly one of: refactored SKILL.md, one of the 4 refs/ files, or the command file. Zero content dropped, zero semantic drift, zero paraphrasing.

**Sub-requirements**:
- FR-PRD-R.7a: Fidelity index at `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` updated with B03/B04 command-layer destinations
- FR-PRD-R.7b: Diff of each of 8 agent prompt templates shows zero content changes
- FR-PRD-R.7c: Diff of each checklist/table against original shows zero content changes
- FR-PRD-R.7d: Diff of output structure and synthesis mapping shows zero content changes
- FR-PRD-R.7e: Diff of BUILD_REQUEST shows only the 6 documented SKILL CONTEXT FILE path changes
- FR-PRD-R.7f: Effective Prompt Examples (B03, lines 46-60) appear in `commands/sc/prd.md` Examples section
- FR-PRD-R.7g: Tier Selection table (B04, lines 79-85) appears in `commands/sc/prd.md` Options section
- FR-PRD-R.7h: Combined line count of command + SKILL.md + all refs/ files is between 1,380 and 1,520 lines

**Dependencies**: FR-PRD-R.0 through FR-PRD-R.6

---

### FR-PRD-R.8: Content Migration from SKILL.md to Command

**Priority**: High
**Description**: Specific interface-concern content moves from SKILL.md to the command file. Content is removed from SKILL.md (not duplicated).

**Sub-requirements**:
- FR-PRD-R.8a: Effective Prompt Examples (original lines 46-60, ~15 lines) present in command's Examples section and absent from SKILL.md
- FR-PRD-R.8b: Tier Selection table (original lines 79-85, ~7 lines) present in command's Options section as `--tier` flag documentation and absent from SKILL.md
- FR-PRD-R.8c: SKILL.md Input section retains: 4-input parameter descriptions (lines 34-44), "What to Do If Prompt Is Incomplete" template (lines 62-73)
- FR-PRD-R.8d: SKILL.md Tier Selection section retains: selection rules (lines 87-92) but not the table header rows
- FR-PRD-R.8e: No content appears in BOTH command file and SKILL.md (except brief cross-references)

**Dependencies**: FR-PRD-R.0, FR-PRD-R.1

---

## Non-Functional Requirements

### NFR-PRD-R.1: SKILL.md Token Budget

**Target**: <= 2,000 tokens on invocation
**Measurement**: 420-450 lines at ~4.5 tokens/line = ~1,890-2,025 tokens
**Rationale**: Original loads ~5,000+ tokens regardless of phase. Refactored SKILL.md loads ~60% less on invocation.

### NFR-PRD-R.2: Per-Phase Token Overhead

**Target**: Max 2 files loaded by orchestrator at any point
**Measurement**: Count files loaded per phase in the loading declarations
**Rationale**: Complies with "at most 2-3 refs loaded at any point" guidance. Builder subagent has its own context.

### NFR-PRD-R.3: Session Start Cost

**Target**: ~50 tokens (name + description only)
**Measurement**: Unchanged from current — frontmatter stays the same
**Rationale**: Skills load only frontmatter at session start. Refactoring doesn't affect this.

### NFR-PRD-R.4: Zero Behavioral Regression

**Target**: Identical execution behavior before and after refactoring
**Measurement**: End-to-end test: invoke skill on a test product and compare output structure
**Rationale**: This is a pure structural refactoring. No pipeline logic, phase structure, or execution behavior changes.

### NFR-PRD-R.5: Command File Line Budget

**Target**: 100-170 lines
**Measurement**: `wc -l commands/sc/prd.md`
**Rationale**: Matches the "thin command layer" pattern exemplified by `adversarial.md` (167 lines).

---

## Complexity Assessment

**Score**: 0.45 / MEDIUM

**Scoring Rationale**:

| Factor | Score | Justification |
|--------|-------|---------------|
| Technical complexity | 0.3 | Pure file restructuring — no new logic, no runtime changes, no API changes |
| Content volume | 0.5 | 1,369 lines to decompose across 6 files with zero content loss |
| Fidelity risk | 0.6 | Word-for-word preservation across 32 content blocks requires careful diffing |
| Cross-reference management | 0.5 | 6 BUILD_REQUEST references need updating; stale references must be eliminated |
| Dependency complexity | 0.3 | Implementation order is linear with one parallel step; no external system dependencies |
| Testing complexity | 0.4 | Tests are primarily structural (grep, wc, diff) — no behavioral test infrastructure needed |
| Rollback risk | 0.2 | Single git revert restores previous state; no data migration or schema changes |

**Aggregate**: Weighted average ~0.45. The primary risk is content fidelity during decomposition, not technical complexity. The task is well-defined with clear acceptance criteria and mechanical verification steps.

---

## Architectural Constraints

1. **500-line SKILL.md ceiling**: Developer Guide Section 9.3 mandates SKILL.md files must not exceed 500 lines. Hard ceiling, not a guideline.

2. **Three-tier architecture mandate**: Developer Guide requires Command → Skill → Agents/refs/ for every skill. No skill may exist without a command layer in front.

3. **Activation pattern**: Command files must contain an `## Activation` section with `Skill <name>` handoff. Commands contain zero protocol logic.

4. **Thin command layer pattern**: Commands are ~80-150 lines providing interface only (flags, examples, boundaries). The `adversarial.md` (167 lines) is the gold-standard template.

5. **refs/ lazy loading**: Reference files load per-phase, not pre-loaded at invocation. Max 2-3 refs loaded at any point in orchestrator context.

6. **Content separation**: SKILL.md = WHAT/WHEN (behavioral protocol). refs/ = HOW (reference material). Command = interface (flags, usage, examples, boundaries).

7. **Source-of-truth workflow**: `src/superclaude/` is canonical. Edit there first, then `make sync-dev` to propagate to `.claude/`. Must pass `make verify-sync` before committing.

8. **Directory naming**: PRD skill stays as `prd/` (not `sc-prd-protocol/`). The `sc-` prefix is for protocol-only skills backing a single command. PRD is dual-purpose.

9. **No behavioral changes**: This is a structural refactoring only. Pipeline logic, phase structure, agent prompt content, and execution behavior must remain identical.

10. **Feature branch requirement**: All changes on feature branch. Never commit directly to master/main.

---

## Risk Inventory

1. **[HIGH] Content loss during SKILL.md trimming** — Removing ~900 lines from SKILL.md risks accidentally dropping instructional content. *Mitigation*: Fidelity index with first/last 10-word markers. Diff every block against original line ranges. FR-PRD-R.7 provides the verification gate.

2. **[HIGH] Cross-reference breakage in BUILD_REQUEST** — 6 references must change from section names to refs/ paths. Missing or incorrect updates break builder subagent behavior. *Mitigation*: Cross-reference map (Section 12.2) enumerates every reference. Post-implementation grep for stale "section" references.

3. **[HIGH] Command file incorrect Activation** — Wrong activation pattern prevents skill from loading. *Mitigation*: Single-line pattern (`Skill prd`). Verified by invoking `/sc:prd` and confirming skill loads.

4. **[MEDIUM] Scope creep — improving content during migration** — Temptation to "fix" or "improve" content while moving it introduces semantic drift. *Mitigation*: Strict rule: zero content changes except documented B03/B04→command migration and BUILD_REQUEST path updates. Diff audit catches violations.

5. **[MEDIUM] Existing refs/ files drifted from SKILL.md** — 3 of 4 refs/ were created during v1 partial implementation. They may have diverged from the original SKILL.md content. *Mitigation*: Verify all 3 existing refs against original SKILL.md line ranges before trimming. If drift found, re-extract from SKILL.md.

6. **[MEDIUM] Prompt examples lose context when moved to command** — Examples currently sit near input parsing logic in SKILL.md. Moving to command may reduce contextual understanding. *Mitigation*: Examples are self-contained strings. Command's Examples section provides equivalent framing.

7. **[MEDIUM] Tier table in command diverges from selection rules in skill** — Table (what tiers ARE) in command; rules (WHEN to pick each) in skill. Could drift independently. *Mitigation*: Table is reference documentation; rules are behavioral protocol. They're independently correct. FR-PRD-R.8e ensures no duplication.

8. **[MEDIUM] Builder subagent can't find refs/ files** — Path resolution failure if builder spawns from unexpected directory. *Mitigation*: Builder is spawned from the SKILL.md directory. Paths are relative. Test by spawning builder during E2E validation.

9. **[LOW] B30→B05 merge loses QA report paths** — Merging duplicate table sections could drop rows. *Mitigation*: B30's 6 specific QA paths appended to B05's table. Diff verifies all paths present.

---

## Dependency Inventory

| # | Dependency | Type | Usage |
|---|-----------|------|-------|
| 1 | `.claude/commands/sc/adversarial.md` | Template | Gold-standard thin command layer (~167 lines) — structural template for `prd.md` |
| 2 | `.claude/skills/prd/SKILL.md` (original) | Source content | 1,369-line monolithic file being decomposed — source of truth for all content |
| 3 | `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` | Verification artifact | Content block inventory with line ranges — must be updated for v2 |
| 4 | `make sync-dev` | Build tool | Propagates `.claude/` changes to `src/superclaude/` |
| 5 | `make verify-sync` | Build tool | Confirms `.claude/` and `src/superclaude/` match |
| 6 | `/task` skill | Runtime dependency | Stage B delegates to /task; reads task file (not SKILL.md or refs/) |
| 7 | `rf-task-builder` agent | Runtime dependency | Subagent spawned during A.7 that reads refs/ files |
| 8 | `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Governance | Defines three-tier architecture mandate, 500-line ceiling, anti-patterns |

---

## Success Criteria

| # | Criterion | Threshold | Measurement Method |
|---|-----------|-----------|-------------------|
| 1 | SKILL.md line count | 400-500 lines | `wc -l SKILL.md` |
| 2 | Command file line count | 100-170 lines | `wc -l commands/sc/prd.md` |
| 3 | SKILL.md token budget | <= 2,000 tokens | Line count × ~4.5 tokens/line |
| 4 | refs/ file count | Exactly 4 .md files | `ls refs/*.md \| wc -l` |
| 5 | Agent prompt fidelity | Zero content changes across all 8 templates | Diff against original SKILL.md line ranges |
| 6 | BUILD_REQUEST fidelity | Exactly 6 documented path changes, zero other changes | Diff against original lines 347-508 |
| 7 | Content migration completeness | B03 examples + B04 tier table in command, absent from SKILL.md | Grep verification (Section 8.5 tests) |
| 8 | Stale reference elimination | Zero "section" references in SKILL.md or refs/ (except "Tier Selection") | Grep for stale section name patterns |
| 9 | Combined line count | 1,380-1,520 lines across all 6 files | Sum of `wc -l` for command + SKILL.md + 4 refs/ |
| 10 | Zero behavioral regression | Identical output structure when invoked on test product | E2E invocation comparison |
| 11 | Sync verification | `make verify-sync` passes | Build tool output |
| 12 | Activation correctness | `/sc:prd` triggers `Skill prd` load | Manual invocation test |

---

## Open Questions

| # | Question | Impact | Status |
|---|----------|--------|--------|
| 1 | **No open questions** | The spec explicitly states "All questions resolved during brainstorm analysis" (Section 11) | Resolved |

**Implicit questions identified during extraction**:

| # | Question | Impact | Recommended Resolution |
|---|----------|--------|----------------------|
| IQ-1 | Should the fidelity index update (FR-PRD-R.7a) be done before or after implementation, and is it a blocking gate? | Low — affects verification ordering | Update fidelity index as part of Step 4 (fidelity verification) in the implementation order. Non-blocking for implementation but blocking for merge. |
| IQ-2 | The spec mentions `refs/.gitkeep` alongside 4 .md files — should `.gitkeep` be removed once refs/ is populated, or kept? | Negligible | Keep `.gitkeep` per convention; structural tests already account for it. |
| IQ-3 | NFR-PRD-R.1 targets <= 2,000 tokens but the calculation shows 420-450 lines × 4.5 = 1,890-2,025 — the upper bound (2,025) exceeds the 2,000 target. Is the 450-line soft upper bound or the 2,000-token budget the binding constraint? | Low — 25 token margin | The 500-line hard ceiling is binding. The 2,000 token target is approximate. 420-450 lines is within acceptable range given token/line ratio variance. |
| IQ-4 | The spec says B30 "6 specific QA paths" are appended to B05 — are these 6 paths documented anywhere with exact content, or must they be extracted from the current SKILL.md during implementation? | Low — discoverable | Extract from current SKILL.md B30 section during implementation. The fidelity index maps B30's line range. |
