---
spec_source: "tdd-command-layer-spec.md"
generated: "2026-04-03T00:00:00Z"
generator: "requirements-extraction-agent/opus-4.6"
functional_requirements: 3
nonfunctional_requirements: 5
total_requirements: 8
complexity_score: 0.25
complexity_class: LOW
domains_detected: [documentation, cli, architecture]
risks_identified: 5
dependencies_identified: 4
success_criteria_count: 12
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 83.0, started_at: "2026-04-03T20:03:40.186910+00:00", finished_at: "2026-04-03T20:05:03.198365+00:00"}
---

## Functional Requirements

### FR-TDD-CMD.1: Thin Command Layer — `commands/sc/tdd.md`

**Source**: Spec Section 3, FR-TDD-CMD.1
**Priority**: Critical — resolves Developer Guide architectural violation
**Description**: Create a thin command file at `.claude/commands/sc/tdd.md` (~120-150 lines) following the `commands/sc/adversarial.md` gold-standard pattern. The command provides the user-facing interface and hands off to the skill via the Activation pattern. Contains zero protocol logic.

**Sub-requirements**:

- **FR-TDD-CMD.1a — File Creation**: File exists at `.claude/commands/sc/tdd.md` with canonical source at `src/superclaude/commands/tdd.md`
- **FR-TDD-CMD.1b — Frontmatter**: Contains `name: tdd`, `description`, `category: documentation`, `complexity: advanced`, `allowed-tools`, `mcp-servers`, `personas`
- **FR-TDD-CMD.1c — Required Input Section**: Documents the mandatory `<component>` positional argument
- **FR-TDD-CMD.1d — Usage Section**: Shows invocation patterns: `/sc:tdd <component> [options]`
- **FR-TDD-CMD.1e — Arguments Section**: Describes `<component>` positional argument and optional PRD reference
- **FR-TDD-CMD.1f — Options Table**: Documents all 7 flags:
  - `<component>` (positional, required)
  - `--tier` / `-t` (enum: lightweight|standard|heavyweight, default: Auto)
  - `--prd` (path, optional)
  - `--resume` / `-r` (boolean, default: false)
  - `--output` / `-o` (path, default: Auto)
  - `--focus` / `-f` (comma-string, default: All)
  - `--from-prd` (boolean, default: false)
- **FR-TDD-CMD.1g — Behavioral Summary**: One-paragraph overview of two-stage process (scope discovery + task file execution via `/task` delegation) with zero protocol details
- **FR-TDD-CMD.1h — Examples Section**: 5-6 examples including:
  1. Strong: all four inputs (component, PRD reference, focus dirs, output path)
  2. Strong: PRD-to-TDD translation with explicit PRD path
  3. Strong: design from scratch with clear scope
  4. Weak (annotated): topic only
  5. Resume: `--resume` with existing task folder
  6. Tier override: explicit `--tier heavyweight`
- **FR-TDD-CMD.1i — Activation Section**: Mandatory handoff via `> Skill tdd` with "Do NOT proceed" guard language
- **FR-TDD-CMD.1j — Boundaries Section**: Will/Will Not list:
  - **Will**: Create TDDs through systematic codebase investigation and web research; Translate PRDs into engineering specifications; Support three depth tiers; Resume from existing task files; Validate output through multi-agent QA pipeline
  - **Will Not**: Modify source code; Implement designs; Generate running code; Create PRDs; Make product decisions
- **FR-TDD-CMD.1k — Related Commands Table**: References `/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`
- **FR-TDD-CMD.1l — Line Budget**: Command file between 100 and 170 lines
- **FR-TDD-CMD.1m — Zero Protocol Logic**: No Stage A/B details, no agent spawning instructions, no phase descriptions, no loading declarations

**Dependencies**: None

---

### FR-TDD-CMD.2: Content Migration from SKILL.md to Command

**Source**: Spec Section 3, FR-TDD-CMD.2
**Priority**: Required — architectural correctness per Developer Guide Section 9.3
**Description**: Migrate ~23 lines of interface-concern content from SKILL.md to the command file. Content is removed from SKILL.md (not duplicated).

**Sub-requirements**:

- **FR-TDD-CMD.2a — Prompt Examples Migration**: Effective Prompt Examples (SKILL.md lines 48-63, ~16 lines) appear in `commands/sc/tdd.md` Examples section, adapted to command invocation syntax
- **FR-TDD-CMD.2b — Tier Table Migration**: Tier Selection table (SKILL.md lines 82-88, header + 3 data rows, ~7 lines) appears in `commands/sc/tdd.md` Options section as `--tier` reference
- **FR-TDD-CMD.2c — SKILL.md Input Retention**: SKILL.md Input section retains: 4-input description (lines 34-46) and "What to Do If Prompt Is Incomplete" template (lines 65-76)
- **FR-TDD-CMD.2d — SKILL.md Tier Rules Retention**: SKILL.md Tier Selection section retains introductory sentence + selection rules (lines 90-94) but not the full table
- **FR-TDD-CMD.2e — No Duplication**: No content appears in BOTH the command file and SKILL.md (except brief cross-references)
- **FR-TDD-CMD.2f — Post-Migration Line Count**: SKILL.md line count between 400 and 440 lines

**Dependencies**: FR-TDD-CMD.1

---

### FR-TDD-CMD.3: Fidelity Verification

**Source**: Spec Section 3, FR-TDD-CMD.3
**Priority**: Required — ensures migration correctness and zero regression
**Description**: Migrated content appears in the command file verbatim (adapted to command context) and is cleanly removed from SKILL.md with no collateral damage.

**Sub-requirements**:

- **FR-TDD-CMD.3a — Strong Examples Present**: All 3 strong prompt examples from SKILL.md lines 48-57 appear in command Examples
- **FR-TDD-CMD.3b — Weak Examples Present**: Both weak prompt examples from SKILL.md lines 59-63 appear in command Examples (annotated)
- **FR-TDD-CMD.3c — Tier Table Rows**: Tier table's 3 data rows (Lightweight, Standard, Heavyweight) with all 5 columns appear in command Options
- **FR-TDD-CMD.3d — Behavioral Protocol Untouched**: SKILL.md behavioral protocol (Stage A, Stage B, critical rules, session management) is completely unmodified
- **FR-TDD-CMD.3e — Loading Declarations Untouched**: SKILL.md loading declarations and Phase Loading Contract table are completely unmodified
- **FR-TDD-CMD.3f — Refs Files Untouched**: All 5 refs/ files have zero changes:
  - `refs/build-request-template.md`
  - `refs/agent-prompts.md`
  - `refs/synthesis-mapping.md`
  - `refs/validation-checklists.md`
  - `refs/operational-guidance.md`

**Dependencies**: FR-TDD-CMD.1, FR-TDD-CMD.2

---

## Non-Functional Requirements

### NFR-TDD-CMD.1: Command File Size

**Source**: Spec Section 6
**Description**: Command file must be between 100 and 170 lines.
**Target**: 100-170 lines
**Measurement**: `wc -l commands/sc/tdd.md`

### NFR-TDD-CMD.2: Zero Protocol Leakage

**Source**: Spec Section 6
**Description**: Command contains no Stage A/B references, no agent spawning instructions, no phase logic.
**Target**: Zero matches for prohibited keywords (`Stage A`, `Stage B`, `rf-task-builder`, `subagent`, phase-specific terms)
**Measurement**: Grep for prohibited keywords returns 0 matches

### NFR-TDD-CMD.3: Post-Migration SKILL.md Size

**Source**: Spec Section 6
**Description**: SKILL.md remains within expected line budget after content migration.
**Target**: 400-440 lines
**Measurement**: `wc -l skills/tdd/SKILL.md`

### NFR-TDD-CMD.4: Activation Correctness

**Source**: Spec Section 6
**Description**: Command hands off to skill using the correct Activation pattern.
**Target**: Contains `Skill tdd` invocation in Activation section
**Measurement**: Grep for activation pattern

### NFR-TDD-CMD.5: Zero Behavioral Regression

**Source**: Spec Section 6
**Description**: Identical TDD skill execution behavior before and after the change.
**Target**: All SKILL.md behavioral sections remain unmodified
**Measurement**: Diff of behavioral sections pre/post migration shows zero changes

---

## Complexity Assessment

**Score**: 0.25 / 1.0
**Class**: LOW

**Scoring Rationale**:

| Dimension | Score | Justification |
|-----------|-------|---------------|
| **Scope** | 0.2 | 2 new files (command canonical + dev copy), 2 modified files (SKILL.md canonical + dev copy). ~130 lines of new content, ~23 lines relocated. |
| **Novelty** | 0.1 | Exact pattern already established by adversarial.md gold standard and PRD spec v2. Zero design ambiguity. |
| **Integration risk** | 0.2 | Content migration could theoretically damage SKILL.md, but moved blocks are contiguous and self-contained. |
| **Technical depth** | 0.1 | No code execution, no API changes, no dependency changes. Pure Markdown file creation and editing. |
| **Testing burden** | 0.3 | 13 structural tests + 7 migration tests + 6 integration tests = 26 total verifications, but all are simple grep/wc/diff commands. |
| **Rollback complexity** | 0.1 | Single `git revert` restores everything. |

**Weighted average**: 0.25 — comfortably LOW complexity. This is a well-scoped, pattern-following, additive refactoring task with established precedent.

---

## Architectural Constraints

1. **Three-Tier Architecture Mandate**: Every skill MUST have a command in front of it (Developer Guide). Command → Skill → refs/ is the mandatory structure.

2. **Source-of-Truth Convention**: `src/superclaude/` is the canonical location. Changes must be made there first, then synced via `make sync-dev` to `.claude/`.

3. **Separation of Concerns (Developer Guide 9.3)**: Command layer owns flags, usage examples, CLI interface concerns. Skill layer owns behavioral protocol (WHAT/WHEN). Refs/ own reference material (HOW).

4. **Activation Pattern**: Commands must contain a `## Activation` section with `> Skill <name>` handoff and guard language preventing direct protocol execution from the command file.

5. **Zero Protocol Logic in Commands**: Commands must contain zero Stage/Phase/Agent spawning details. All protocol content stays in the skill layer.

6. **Gold-Standard Template**: `commands/sc/adversarial.md` (167 lines) defines the structural template: frontmatter → required input → usage → arguments → options → behavioral summary → examples → activation → boundaries → related commands.

7. **Component Sync Pipeline**: All changes require `make sync-dev` followed by `make verify-sync` before commit.

8. **No Behavioral Changes**: This spec explicitly prohibits any modification to TDD skill execution behavior — only structural/organizational changes are in scope.

---

## Risk Inventory

1. **RISK-01: Content loss during migration** — Severity: **Low**
   - Probability: Very Low
   - Impact: Low
   - Description: Migrated ~23 lines could be partially lost or corrupted during relocation
   - Mitigation: Blocks are contiguous (lines 48-63, 82-88); diff verification after migration confirms completeness

2. **RISK-02: Protocol leakage into command** — Severity: **Medium**
   - Probability: Low
   - Impact: Medium
   - Description: Command file inadvertently includes Stage A/B details, agent spawning instructions, or phase logic
   - Mitigation: Review against adversarial gold standard; automated grep tests for prohibited keywords (Stage A, Stage B, rf-task-builder, subagent)

3. **RISK-03: Scope creep to improve TDD content** — Severity: **Medium**
   - Probability: Low
   - Impact: Medium
   - Description: Implementer may be tempted to improve or enhance TDD skill behavior while creating the command layer
   - Mitigation: Strict spec boundary: only create command + remove migrated content. Zero behavioral changes. FR-TDD-CMD.3d-f verify no collateral modifications.

4. **RISK-04: Sync failure (command not in src/)** — Severity: **Low**
   - Probability: Low
   - Impact: Low
   - Description: Command created in `.claude/` but not in `src/superclaude/`, causing sync drift
   - Mitigation: `make verify-sync` catches immediately; spec explicitly requires canonical source creation first

5. **RISK-05: Prompt examples lose context when adapted** — Severity: **Low**
   - Probability: Very Low
   - Impact: Low
   - Description: Examples may lose meaning when moved from SKILL.md context to command invocation syntax
   - Mitigation: Examples are self-contained strings; command provides equivalent framing with usage context

---

## Dependency Inventory

### Internal Dependencies

1. **`commands/sc/adversarial.md`** — Gold-standard structural template (167 lines). Used as the pattern reference for section ordering and content style. Must be read before implementation.

2. **`.claude/skills/tdd/SKILL.md`** — Current TDD skill file (438 lines). Source of migrated content (lines 48-63, 82-88). Must be read and modified.

3. **`make sync-dev` / `make verify-sync`** — Build system commands for propagating changes from `src/superclaude/` to `.claude/` and verifying parity. Required post-implementation.

4. **Developer Guide** (`docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`) — Authoritative source for three-tier architecture rules, Activation pattern, Section 9.3 separation of concerns, Section 9.7 anti-patterns, Section 5.10 checklist.

### External Dependencies

None. This is a pure Markdown refactoring task with no external library, service, or API dependencies.

---

## Success Criteria

| # | Criterion | Acceptance Threshold | Measurement Method |
|---|-----------|---------------------|--------------------|
| SC-1 | Command file exists at both canonical and dev-copy locations | Both `src/superclaude/commands/tdd.md` and `.claude/commands/sc/tdd.md` exist | `test -f` on both paths |
| SC-2 | Command file within line budget | 100-170 lines | `wc -l` |
| SC-3 | All 7 flags documented in Options table | `--tier`, `--prd`, `--resume`, `--output`, `--focus`, `--from-prd`, `<component>` all present | Grep for each flag |
| SC-4 | Activation section correctly invokes skill | Contains `Skill tdd` | Grep for activation pattern |
| SC-5 | Zero protocol leakage | 0 matches for `Stage A`, `rf-task-builder`, `subagent` | Grep returns 0 |
| SC-6 | All prompt examples migrated to command | 3 strong + 2 weak examples present in command | Grep for distinctive example strings |
| SC-7 | Tier table migrated to command | 3 data rows (Lightweight, Standard, Heavyweight) present | Grep for tier names |
| SC-8 | Migrated content removed from SKILL.md | 0 matches for migrated example strings in SKILL.md | Grep returns 0 |
| SC-9 | SKILL.md post-migration line count | 400-440 lines | `wc -l` |
| SC-10 | SKILL.md behavioral protocol unmodified | Stage A, Stage B, critical rules, session management sections identical to pre-migration | Diff of behavioral sections |
| SC-11 | All 5 refs/ files unmodified | Zero diff on all refs/ files | `git diff` on refs/ directory |
| SC-12 | Sync verification passes | `make verify-sync` exits 0 | Command exit code |

---

## Open Questions

| # | Question | Context | Impact | Status |
|---|----------|---------|--------|--------|
| 1 | **None identified** | Spec Section 11 explicitly states: "All questions resolved during brainstorm analysis" | N/A | Resolved |

**Note**: The spec is unusually complete for its complexity class. The combination of an established gold-standard template (adversarial.md), a direct pattern precedent (PRD spec v2 FR-PRD-R.0), explicit line references for migrated content, and comprehensive test plan leaves no ambiguities requiring stakeholder clarification. All design decisions are documented in Section 2.1 with alternatives considered and rationale provided.
